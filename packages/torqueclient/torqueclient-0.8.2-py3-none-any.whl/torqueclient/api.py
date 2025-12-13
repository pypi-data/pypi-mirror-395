import mwclient
import json
import warnings

import dateutil.parser

from .cache import DiskCache, MemoryCache
from .version import __version__
from datetime import datetime


class Torque:
    """The entrypoint to accessing a torque system.

    This is the main object that code using the client should instantiate.
    It manages the connection to the server, as well as handling all the
    plumbing required to translate the http calls using the mwclient library.

    Attributes
    ----------
    site : mwclient.Site
        The site object holding the connection
    cache : cache.Cache
        The local cache strategy
    collections : Collections
        All the collections that are available from the server
    information : dict
        The server configuration, for things like version and aliases
    group : str
        A group to act-as or emulate, if the user is an admin.

    When started up, an alias is fetched from the server.  This alias
    is then set as a synonym alias for collections.  For example, if the
    COLLECTIONS_ALIAS on the server is set to "competitions", then there's
    an additional attribute as follows:

    competition : Collections
        All the competitions available from the server

    Methods
    -------
    search(search_term, collection_name=None)
        searches for documents
    bulk_fetch(documents, num_threads=10)
        eager loads the documents
    """

    def __init__(self, url, username, password, cache=None, group=None):
        """Initializes to a running torque system available from
        a mediawiki instance at URL that is accessed using USERNAME
        and PASSWORD.

        URL must be fully qualified with the protocol, ie
        http://your.domain.tld/

        CACHE is an optional cache that implements cache.Cache,
        defaulting to the DiskCache"""
        (scheme, host) = url.split("://")
        self.url = url
        self.site = mwclient.Site(host, path="/", scheme=scheme, reqs={"timeout": 300})
        self.site.login(username, password)
        self.cache = cache
        if not self.cache:
            self.cache = DiskCache()

        self._group = group

        self.collections = Collections(self)

        information = self._get_data("/system")
        self.documents_alias = None
        if "collections_alias" in information:
            self.documents_alias = information["documents_alias"]

            setattr(self, information["collections_alias"], self.collections)

        if information["server_version"] != __version__:
            warnings.warn(
                "API version %s does not match server version %s (run pip install -I torqueclient==%s)"
                % (
                    __version__,
                    information["server_version"],
                    information["server_version"],
                ),
                UserWarning,
            )

    @property
    def group(self):
        """Returns the group that this Torque instance is acting as, if any."""
        return self._group

    def call_api(self, action, *args, **kwargs):
        if self._group:
            kwargs['group'] = self._group

        return self.site.api(action, *args, **kwargs)

    def search(self, search_term, collection_name=None, filters={}, num_per_page=None, offset=None, include_snippets=False, **kwargs):
        """Search the connected torque system for SEARCH_TERM.

        Optionally pass in a COLLECTION_NAME to restrict the results
        to that collection."""

        if include_snippets:
            kwargs['include_snippets'] = 'true'

        path = (
            "/collections/%s/search" % collection_name if collection_name else "/search"
        )

        if filters:
            kwargs["f"] = json.dumps(filters)
        if num_per_page:
            kwargs["num_per_page"] = num_per_page
        if offset:
            kwargs["offset"] = offset

        results = []
        for result in self.call_api("torque", format="json", path=path, q=search_term, **kwargs)[
            "result"
        ]:
            uri = result["uri"]
            parts = uri.split("/", 4)
            collection = self.collections[parts[2]]
            key = parts[4]

            results.append(
                SearchResult(
                    self,
                    collection,
                    key,
                    result.get("snippets"),
                )
            )

        return results

    def _get_data(self, path):
        """Internal utility method to get data from the server located at PATH"""
        return self.call_api("torque", format="json", path=path)["result"]

    def bulk_fetch(self, documents, num_threads=10):
        """Fetch DOCUMENTS in bulk, split over NUM_THREADS threads.

        As DOCUMENTS are lazy loaded in the system, this greedily fills
        them with the data from the server.  This is done in a multi threaded
        way to save time.

        DOCUMENTS can either be [Document*], or a Documents object, so it can
        be used with either the result of search() or
        collections['somekey'].documents"""
        if isinstance(documents, list):
            docs_to_process = documents.copy()
        elif isinstance(documents, Documents):
            docs_to_process = [doc for doc in documents]
        else:
            raise Exception("bulk_fetch expects list or Documents")

        import threading

        lock = threading.Lock()

        def fetch_document():
            document = True
            while document:
                with lock:
                    if len(docs_to_process) > 0:
                        document = docs_to_process.pop()
                    else:
                        document = None
                if document:
                    document._get_data()

        threads = [threading.Thread(target=fetch_document) for x in range(num_threads)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


class Collections:
    """
    A container object for all the collections on the server.

    This is a list/dict like class that represents the collections on the server.
    This isn't just a dict in order to lazy load the collections from the
    server.  If not, then when connecting to torque would then make N
    queries, one for each collection.

    It can be indexed like a dict, but also iterated over like a list.  So the
    following work:

        Torque(...).collections["XYZ"]

    and

        for collection in Torque(...).collections:
           ...

    Attributes
    ----------
    torque : Torque
        The parent torque object
    collection_data : dict
        The in memory cache of the actual collections after loading
    names : list
        The names of the available collections
    """

    def __init__(self, torque):
        """Initializes a lazy loaded list of collections

        Additionally fetches the list of available collections."""
        self.torque = torque
        self.collection_data = {}
        self.names = self.torque._get_data("/collections")

    def keys(self):
        """Returns the available collection names."""
        return self.names

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx < len(self.names):
            collection_name = self.names[self.idx]
            self.idx += 1
            return self[collection_name]
        else:
            raise StopIteration()

    def __getitem__(self, collection_name):
        """Returns a Collection object represented by COLLECTION_NAME.

        If this doesn't exist yet in memory, lazily instantiate it, which will
        involve server calls to populating it."""
        if collection_name not in self.collection_data:
            self.collection_data[collection_name] = Collection(
                self.torque, collection_name
            )

        return self.collection_data[collection_name]


class Collection:
    """A Collection of documents.

    Not only the interface to get various documents, but also handles
    the cache invalidation of those objects, as that information exists
    at the collection leve on the server.

    A note that this will only hold the documents that the logged in user
    has acccess to.

    Attributes
    ----------
    torque : Torque
        the parent torque object
    name : str
        the name of this collection
    documents : Documents
        the documents in this collection
    last_updated : Timestamp
        the time this collection last an an update on the server,
        as from an edit or addition.
    fields : List
        all the fields that the user has access to on the server

    Like Torque above, an alias is created if there's a DOCUMENTS_ALIAS
    on the server.  For instance, if "proposals" is set to DOCUMENTS_ALIAS,
    then there will be an attribute as follows:

    proposals : Documents
        the proposals in the competition

    Methods
    -------
    search(search_term, [filters, num_per_page, offset])
        search for documents in this collection
    """

    def __init__(self, torque, name):
        self.torque = torque
        self.name = name

        self.documents = Documents(self.torque, self)
        if torque.documents_alias:
            setattr(self, torque.documents_alias, self.documents)

        self._refresh_from_server()

    def search(
        self,
        search_term,
        filters={},
        num_per_page=None,
        offset=None,
        include_snippets=False,
    ):
        """Return Documents mathing SEARCH_TERM in this collection."""
        return self.torque.search(
            search_term,
            self.name,
            filters=filters,
            num_per_page=num_per_page,
            offset=offset,
            include_snippets=include_snippets,
        )

    def _refresh_from_server(self):
        """Internal method to update the last_updated, which is used
        for cache invalidation for documents."""
        collection_information = self.torque._get_data("/collections/%s" % self.name)
        self.fields = collection_information["fields"]
        self.last_updated = dateutil.parser.isoparse(
            collection_information["last_updated"]
        )
        self.refreshed_at = datetime.now()

    def _evaluate_cache(self):
        """Refresh data from the server if it's been too long since last looked,
        depending on the information from the Torque Cache"""
        if (
            self.torque.cache is not None
            and (datetime.now() - self.refreshed_at).seconds
            > self.torque.cache.cache_timeout()
        ):
            self._refresh_from_server()


class Documents:
    """
    A container object for all the documents in given Collection.

    This is a list/dict like class that represents the documents on the server.
    This isn't just a dict in order to lazy load the documents from the
    server.

    It can be indexed like a dict, but also iterated over like a list.  So the
    following work:

        Torque(...).collections["XYZ"].documents["123"]

    and

        for collection in Torque(...).collections:
            for document in collection.documents:
                ...

    It does not store the documents in memory (unlike Collections) above, because
    we want to respect whatever caching strategy the user is using.  That means
    that the following will fetch from the server twice:

        Torque(...).collections["XYZ"].documents["123"]
        Torque(...).collections["XYZ"].documents["123"]

    Also, the list of keys is not retrieved from the server until used for iteration.
    When using access, torqueclient assumes you know what you're doing.

    Attributes
    ----------
    torque : Torque
        The parent torque object
    collection: Collection
        The parent Collection object
    keys : list
        The keys for the available documents
    """

    def __init__(self, torque, collection):
        self.torque = torque
        self.collection = collection
        self.keys = None

    def __iter__(self):
        """Fetches the keys on the first use"""
        if self.keys is None:
            self.keys = self.torque._get_data(
                "/collections/%s/documents" % self.collection.name
            )
        self.idx = 0
        return self

    def __next__(self):
        if self.idx < len(self.keys):
            key = self.keys[self.idx]
            self.idx += 1
            return self[key]
        else:
            raise StopIteration()

    def __getitem__(self, key):
        # We always return a new Document here because we want to respect whatever
        # caching strategy the end user has decided to use.
        return Document(self.torque, self.collection, key)


class Document:
    """A Document

    A lazy loaded instance of a document on the torque server.  This does
    not load any data from the server until accessed (via keys(), or __getitem__
    methods)

    A note that this will only hold the fields that the logged in user
    has acccess to.

    Attributes
    ----------
    torque : Torque
        the parent torque object
    collection : Torque
        the parent collection object
    key : str
        the identifying key from the server
    data : dict
        initially set to None (until lazy loaded), a dictionary of names to values

    Methods
    -------
    keys()
        all the field keys
    upload_attachment(name, column, stream)
        upload an attachment
    attachments()
        the attachments for this document
    uri()
        the uri of the document, which is a useful index when creating a cache
    original()
        the original form of the document, as uploaded in the collection
    latest()
        the most recent form of the document, which is the default
    """

    def __init__(self, torque, collection, key):
        self.torque = torque
        self.collection = collection
        self.key = key
        self.data = None
        self.version = "latest"

    def __getitem__(self, field):
        return self._get_data()[field]

    def __setitem__(self, field, new_value):
        """Sets the field value not only in memory, but also pushes the change
        to the server."""
        self._get_data()

        if field not in self.keys():
            raise KeyError(field)

        self.torque.call_api(
            "torque",
            format="json",
            path="%s/fields/%s" % (self.uri(), field),
            new_value=json.dumps(new_value),
        )
        self.data[field] = new_value

        self.collection._refresh_from_server()

    def latest(self):
        d = Document(self.torque, self.collection, self.key)
        d.version = "latest"
        return d

    def original(self):
        d = Document(self.torque, self.collection, self.key)
        d.version = "original"
        return d

    def uri(self):
        """Returns the uri of the doucment on the server."""
        version_string = ""
        if self.version != "latest":
            version_string = "/version/" + self.version
        return "/collections/%s/documents/%s%s" % (
            self.collection.name,
            self.key,
            version_string,
        )

    def keys(self):
        """Returns the list of all the field keys available on the server."""
        return self._get_data().keys()

    def upload_attachment(self, name, column, stream):
        """Uploads an attachment named via NAME, permissioned to column
        COLUMN, and provided by the file stream STREAM.  This attachment
        will get attached to the current document.

        The user must have torque-admin permissions to upload."""
        self.torque.site.raw_call(
            "api",
            {
                "action": "torqueuploadattachment",
                "format": "json",
                "collection_name": self.collection.name,
                "object_id": self.key,
                "permissions_field": column,
                "attachment_name": name,
            },
            {"attachment": stream.read()},
        )

    def attachments(self):
        """Returns the list of all attachments for this document."""
        return Attachments(self.torque, self)

    def _get_data(self):
        """Gets the data for the document from the server.

        There's logic here as well that will refresh data if new, as well
        as pull from cache as appropriate."""
        if self.data is None:
            if self.torque.cache is not None:
                self.collection._evaluate_cache()
                if self.torque.cache.contains_document_data(
                    self, self.collection.last_updated, self.torque.group
                ):
                    self.data = self.torque.cache.retrieve_document_data(self, self.torque.group)

            if self.data is None:
                self.data = self.torque._get_data(self.uri())

            if (
                self.torque.cache is not None
                and not self.torque.cache.contains_document_data(
                    self, self.collection.last_updated, self.torque.group
                )
            ):
                self.torque.cache.persist_document(self, self.collection.last_updated, self.torque.group)

        return self.data


class SearchResult(Document):
    """A SearchResult

    A document that has been returned as a result of a search,
    plus any relevant snippets from that document.

    Attributes
    ----------
    torque : Torque
        the parent torque object
    collection : Torque
        the parent collection object
    key : str
        the identifying key from the server
    snippets : str[] | None
        relevant document snippets returned from search, if any

    Methods
    -------
    See Document methods.
    """

    def __init__(self, torque, collection, key, snippets=None):
        self.snippets = snippets
        super().__init__(torque, collection, key)


class Attachments:
    """
    A container object for all the attachments on given Document.

    This is a list/dict like class that represents the attachments on the server.

    It can indexed like a dict, but also iterated over like a list.  So the
    following work:

        Torque(...).collections["XYZ"].documents["123"].attachments["attachment_1.pdf"]

    and

        for collection in Torque(...).collections:
            for document in collection.documents:
                for attachment in document.attachments:
                    ...

    It stores the list of attachments in memory, so getting the list of attachments
    requires calling into document.attachments again.  However, each time `.get()` is
    called, it will fetch the most recent version of the attachment from the server.

    Attributes
    ----------
    torque : Torque
        The parent torque object
    document: Collection
        The parent Collection object
    names: list
        The names of the available attachments
    """

    def __init__(self, torque, document):
        self.torque = torque
        self.document = document
        self.attachments = {
            a["name"]: Attachment(torque, document, a["name"], a["size"])
            for a in self.torque._get_data(
                "/collections/%s/documents/%s/attachments"
                % (document.collection.name, document.key)
            )
        }
        self.names = self.attachments.keys()

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx < len(self.names):
            name = self.names[self.idx]
            self.idx += 1
            return self.attachments[name]
        else:
            raise StopIteration()

    def __getitem__(self, name):
        return self.attachments[name]


class Attachment:
    """An Attachment

    A lazy loaded instance of an attachment on the torque server.  This does
    not load any data from the server until accessed (via get())

    Attributes
    ----------
    torque : Torque
        the parent torque object
    collection : Torque
        the parent collection object
    name : str
        the name of the attachment
    size : int
        the size of the attachment

    Methods
    -------
    download(destination=None)
        retrieves the attachment from the server and writes it to destination if provided,
        otherwise returns it
    """

    def __init__(self, torque, document, name, size):
        self.torque = torque
        self.document = document
        self.name = name
        self.size = size

    def download(self, destination=None):
        url = (
            "%s/index.php/Special:TorqueAttachment?collection_name=%s&id=%s&attachment=%s"
            % (
                self.torque.url,
                self.document.collection.name,
                self.document.key,
                self.name,
            )
        )
        if destination is not None:
            res = self.torque.site.connection.get(url, stream=True)
            for chunk in res.iter_content(1024):
                destination.write(chunk)
        else:
            return self.torque.site.connection.get(url).content
