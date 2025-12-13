# coding: utf-8

"""
    Harness NextGen Software Delivery Platform API Reference

    The Harness Software Delivery Platform uses OpenAPI Specification v3.0. Harness constantly improves these APIs. Please be aware that some improvements could cause breaking changes. # Introduction     The Harness API allows you to integrate and use all the services and modules we provide on the Harness Platform. If you use client-side SDKs, Harness functionality can be integrated with your client-side automation, helping you reduce manual efforts and deploy code faster.    For more information about how Harness works, read our [documentation](https://developer.harness.io/docs/getting-started) or visit the [Harness Developer Hub](https://developer.harness.io/).  ## How it works    The Harness API is a RESTful API that uses standard HTTP verbs. You can send requests in JSON, YAML, or form-data format. The format of the response matches the format of your request. You must send a single request at a time and ensure that you include your authentication key. For more information about this, go to [Authentication](#section/Introduction/Authentication).  ## Get started    Before you start integrating, get to know our API better by reading the following topics:    * [Harness key concepts](https://developer.harness.io/docs/getting-started/learn-harness-key-concepts/)   * [Authentication](#section/Introduction/Authentication)   * [Requests and responses](#section/Introduction/Requests-and-Responses)   * [Common Parameters](#section/Introduction/Common-Parameters-Beta)   * [Status Codes](#section/Introduction/Status-Codes)   * [Errors](#tag/Error-Response)   * [Versioning](#section/Introduction/Versioning-Beta)   * [Pagination](/#section/Introduction/Pagination-Beta)    The methods you need to integrate with depend on the functionality you want to use. Work with  your Harness Solutions Engineer to determine which methods you need.  ## Authentication  To authenticate with the Harness API, you need to:   1. Generate an API token on the Harness Platform.   2. Send the API token you generate in the `x-api-key` header in each request.  ### Generate an API token  To generate an API token, complete the following steps:   1. Go to the [Harness Platform](https://app.harness.io/).   2. On the left-hand navigation, click **My Profile**.   3. Click **+API Key**, enter a name for your key and then click **Save**.   4. Within the API Key tile, click **+Token**.   5. Enter a name for your token and click **Generate Token**. **Important**: Make sure to save your token securely. Harness does not store the API token for future reference, so make sure to save your token securely before you leave the page.  ### Send the API token in your requests  Send the token you created in the Harness Platform in the x-api-key header. For example:   `x-api-key: YOUR_API_KEY_HERE`  ## Requests and Responses    The structure for each request and response is outlined in the API documentation. We have examples in JSON and YAML for every request and response. You can use our online editor to test the examples.  ## Common Parameters [Beta]  | Field Name | Type    | Default | Description    | |------------|---------|---------|----------------| | identifier | string  | none    | URL-friendly version of the name, used to identify a resource within it's scope and so needs to be unique within the scope.                                                                                                            | | name       | string  | none    | Human-friendly name for the resource.                                                                                       | | org        | string  | none    | Limit to provided org identifiers.                                                                                                                     | | project    | string  | none    | Limit to provided project identifiers.                                                                                                                 | | description| string  | none    | More information about the specific resource.                                                                                    | | tags       | map[string]string  | none    | List of labels applied to the resource.                                                                                                                         | | order      | string  | desc    | Order to use when sorting the specified fields. Type: enum(asc,desc).                                                                                                                                     | | sort       | string  | none    | Fields on which to sort. Note: Specify the fields that you want to use for sorting. When doing so, consider the operational overhead of sorting fields. | | limit      | int     | 30      | Pagination: Number of items to return.                                                                                                                 | | page       | int     | 1       | Pagination page number strategy: Specify the page number within the paginated collection related to the number of items in each page.                  | | created    | int64   | none    | Unix timestamp that shows when the resource was created (in milliseconds).                                                               | | updated    | int64   | none    | Unix timestamp that shows when the resource was last edited (in milliseconds).                                                           |   ## Status Codes    Harness uses conventional HTTP status codes to indicate the status of an API request.    Generally, 2xx responses are reserved for success and 4xx status codes are reserved for failures. A 5xx response code indicates an error on the Harness server.    | Error Code  | Description |   |-------------|-------------|   | 200         |     OK      |   | 201         |   Created   |   | 202         |   Accepted  |   | 204         |  No Content |   | 400         | Bad Request |   | 401         | Unauthorized |   | 403         | Forbidden |   | 412         | Precondition Failed |   | 415         | Unsupported Media Type |   | 500         | Server Error |    To view our error response structures, go [here](#tag/Error-Response).  ## Versioning [Beta]  ### Harness Version   The current version of our Beta APIs is yet to be announced. The version number will use the date-header format and will be valid only for our Beta APIs.  ### Generation   All our beta APIs are versioned as a Generation, and this version is included in the path to every API resource. For example, v1 beta APIs begin with `app.harness.io/v1/`, where v1 is the API Generation.    The version number represents the core API and does not change frequently. The version number changes only if there is a significant departure from the basic underpinnings of the existing API. For example, when Harness performs a system-wide refactoring of core concepts or resources.  ## Pagination [Beta]  We use pagination to place limits on the number of responses associated with list endpoints. Pagination is achieved by the use of limit query parameters. The limit defaults to 30. Its maximum value is 100.  Following are the pagination headers supported in the response bodies of paginated APIs:   1. X-Total-Elements : Indicates the total number of entries in a paginated response.   2. X-Page-Number : Indicates the page number currently returned for a paginated response.   3. X-Page-Size : Indicates the number of entries per page for a paginated response.  For example:    ``` X-Total-Elements : 30 X-Page-Number : 0 X-Page-Size : 10   ```   # noqa: E501

    OpenAPI spec version: 1.0
    Contact: contact@harness.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Repository(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'all_fields': 'dict(str, object)',
        'branch': 'str',
        'branch_bytes': 'ByteString',
        'clone': 'str',
        'clone_bytes': 'ByteString',
        'clone_ssh': 'str',
        'clone_ssh_bytes': 'ByteString',
        'created': 'Timestamp',
        'created_or_builder': 'TimestampOrBuilder',
        'default_instance_for_type': 'Repository',
        'descriptor_for_type': 'Descriptor',
        'id': 'str',
        'id_bytes': 'ByteString',
        'initialization_error_string': 'str',
        'initialized': 'bool',
        'link': 'str',
        'link_bytes': 'ByteString',
        'memoized_serialized_size': 'int',
        'name': 'str',
        'name_bytes': 'ByteString',
        'namespace': 'str',
        'namespace_bytes': 'ByteString',
        'parser_for_type': 'ParserRepository',
        'perm': 'Perm',
        'perm_or_builder': 'PermOrBuilder',
        'private': 'bool',
        'serialized_size': 'int',
        'unknown_fields': 'UnknownFieldSet',
        'updated': 'Timestamp',
        'updated_or_builder': 'TimestampOrBuilder'
    }

    attribute_map = {
        'all_fields': 'allFields',
        'branch': 'branch',
        'branch_bytes': 'branchBytes',
        'clone': 'clone',
        'clone_bytes': 'cloneBytes',
        'clone_ssh': 'cloneSsh',
        'clone_ssh_bytes': 'cloneSshBytes',
        'created': 'created',
        'created_or_builder': 'createdOrBuilder',
        'default_instance_for_type': 'defaultInstanceForType',
        'descriptor_for_type': 'descriptorForType',
        'id': 'id',
        'id_bytes': 'idBytes',
        'initialization_error_string': 'initializationErrorString',
        'initialized': 'initialized',
        'link': 'link',
        'link_bytes': 'linkBytes',
        'memoized_serialized_size': 'memoizedSerializedSize',
        'name': 'name',
        'name_bytes': 'nameBytes',
        'namespace': 'namespace',
        'namespace_bytes': 'namespaceBytes',
        'parser_for_type': 'parserForType',
        'perm': 'perm',
        'perm_or_builder': 'permOrBuilder',
        'private': 'private',
        'serialized_size': 'serializedSize',
        'unknown_fields': 'unknownFields',
        'updated': 'updated',
        'updated_or_builder': 'updatedOrBuilder'
    }

    def __init__(self, all_fields=None, branch=None, branch_bytes=None, clone=None, clone_bytes=None, clone_ssh=None, clone_ssh_bytes=None, created=None, created_or_builder=None, default_instance_for_type=None, descriptor_for_type=None, id=None, id_bytes=None, initialization_error_string=None, initialized=None, link=None, link_bytes=None, memoized_serialized_size=None, name=None, name_bytes=None, namespace=None, namespace_bytes=None, parser_for_type=None, perm=None, perm_or_builder=None, private=None, serialized_size=None, unknown_fields=None, updated=None, updated_or_builder=None):  # noqa: E501
        """Repository - a model defined in Swagger"""  # noqa: E501
        self._all_fields = None
        self._branch = None
        self._branch_bytes = None
        self._clone = None
        self._clone_bytes = None
        self._clone_ssh = None
        self._clone_ssh_bytes = None
        self._created = None
        self._created_or_builder = None
        self._default_instance_for_type = None
        self._descriptor_for_type = None
        self._id = None
        self._id_bytes = None
        self._initialization_error_string = None
        self._initialized = None
        self._link = None
        self._link_bytes = None
        self._memoized_serialized_size = None
        self._name = None
        self._name_bytes = None
        self._namespace = None
        self._namespace_bytes = None
        self._parser_for_type = None
        self._perm = None
        self._perm_or_builder = None
        self._private = None
        self._serialized_size = None
        self._unknown_fields = None
        self._updated = None
        self._updated_or_builder = None
        self.discriminator = None
        if all_fields is not None:
            self.all_fields = all_fields
        if branch is not None:
            self.branch = branch
        if branch_bytes is not None:
            self.branch_bytes = branch_bytes
        if clone is not None:
            self.clone = clone
        if clone_bytes is not None:
            self.clone_bytes = clone_bytes
        if clone_ssh is not None:
            self.clone_ssh = clone_ssh
        if clone_ssh_bytes is not None:
            self.clone_ssh_bytes = clone_ssh_bytes
        if created is not None:
            self.created = created
        if created_or_builder is not None:
            self.created_or_builder = created_or_builder
        if default_instance_for_type is not None:
            self.default_instance_for_type = default_instance_for_type
        if descriptor_for_type is not None:
            self.descriptor_for_type = descriptor_for_type
        if id is not None:
            self.id = id
        if id_bytes is not None:
            self.id_bytes = id_bytes
        if initialization_error_string is not None:
            self.initialization_error_string = initialization_error_string
        if initialized is not None:
            self.initialized = initialized
        if link is not None:
            self.link = link
        if link_bytes is not None:
            self.link_bytes = link_bytes
        if memoized_serialized_size is not None:
            self.memoized_serialized_size = memoized_serialized_size
        if name is not None:
            self.name = name
        if name_bytes is not None:
            self.name_bytes = name_bytes
        if namespace is not None:
            self.namespace = namespace
        if namespace_bytes is not None:
            self.namespace_bytes = namespace_bytes
        if parser_for_type is not None:
            self.parser_for_type = parser_for_type
        if perm is not None:
            self.perm = perm
        if perm_or_builder is not None:
            self.perm_or_builder = perm_or_builder
        if private is not None:
            self.private = private
        if serialized_size is not None:
            self.serialized_size = serialized_size
        if unknown_fields is not None:
            self.unknown_fields = unknown_fields
        if updated is not None:
            self.updated = updated
        if updated_or_builder is not None:
            self.updated_or_builder = updated_or_builder

    @property
    def all_fields(self):
        """Gets the all_fields of this Repository.  # noqa: E501


        :return: The all_fields of this Repository.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._all_fields

    @all_fields.setter
    def all_fields(self, all_fields):
        """Sets the all_fields of this Repository.


        :param all_fields: The all_fields of this Repository.  # noqa: E501
        :type: dict(str, object)
        """

        self._all_fields = all_fields

    @property
    def branch(self):
        """Gets the branch of this Repository.  # noqa: E501


        :return: The branch of this Repository.  # noqa: E501
        :rtype: str
        """
        return self._branch

    @branch.setter
    def branch(self, branch):
        """Sets the branch of this Repository.


        :param branch: The branch of this Repository.  # noqa: E501
        :type: str
        """

        self._branch = branch

    @property
    def branch_bytes(self):
        """Gets the branch_bytes of this Repository.  # noqa: E501


        :return: The branch_bytes of this Repository.  # noqa: E501
        :rtype: ByteString
        """
        return self._branch_bytes

    @branch_bytes.setter
    def branch_bytes(self, branch_bytes):
        """Sets the branch_bytes of this Repository.


        :param branch_bytes: The branch_bytes of this Repository.  # noqa: E501
        :type: ByteString
        """

        self._branch_bytes = branch_bytes

    @property
    def clone(self):
        """Gets the clone of this Repository.  # noqa: E501


        :return: The clone of this Repository.  # noqa: E501
        :rtype: str
        """
        return self._clone

    @clone.setter
    def clone(self, clone):
        """Sets the clone of this Repository.


        :param clone: The clone of this Repository.  # noqa: E501
        :type: str
        """

        self._clone = clone

    @property
    def clone_bytes(self):
        """Gets the clone_bytes of this Repository.  # noqa: E501


        :return: The clone_bytes of this Repository.  # noqa: E501
        :rtype: ByteString
        """
        return self._clone_bytes

    @clone_bytes.setter
    def clone_bytes(self, clone_bytes):
        """Sets the clone_bytes of this Repository.


        :param clone_bytes: The clone_bytes of this Repository.  # noqa: E501
        :type: ByteString
        """

        self._clone_bytes = clone_bytes

    @property
    def clone_ssh(self):
        """Gets the clone_ssh of this Repository.  # noqa: E501


        :return: The clone_ssh of this Repository.  # noqa: E501
        :rtype: str
        """
        return self._clone_ssh

    @clone_ssh.setter
    def clone_ssh(self, clone_ssh):
        """Sets the clone_ssh of this Repository.


        :param clone_ssh: The clone_ssh of this Repository.  # noqa: E501
        :type: str
        """

        self._clone_ssh = clone_ssh

    @property
    def clone_ssh_bytes(self):
        """Gets the clone_ssh_bytes of this Repository.  # noqa: E501


        :return: The clone_ssh_bytes of this Repository.  # noqa: E501
        :rtype: ByteString
        """
        return self._clone_ssh_bytes

    @clone_ssh_bytes.setter
    def clone_ssh_bytes(self, clone_ssh_bytes):
        """Sets the clone_ssh_bytes of this Repository.


        :param clone_ssh_bytes: The clone_ssh_bytes of this Repository.  # noqa: E501
        :type: ByteString
        """

        self._clone_ssh_bytes = clone_ssh_bytes

    @property
    def created(self):
        """Gets the created of this Repository.  # noqa: E501


        :return: The created of this Repository.  # noqa: E501
        :rtype: Timestamp
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this Repository.


        :param created: The created of this Repository.  # noqa: E501
        :type: Timestamp
        """

        self._created = created

    @property
    def created_or_builder(self):
        """Gets the created_or_builder of this Repository.  # noqa: E501


        :return: The created_or_builder of this Repository.  # noqa: E501
        :rtype: TimestampOrBuilder
        """
        return self._created_or_builder

    @created_or_builder.setter
    def created_or_builder(self, created_or_builder):
        """Sets the created_or_builder of this Repository.


        :param created_or_builder: The created_or_builder of this Repository.  # noqa: E501
        :type: TimestampOrBuilder
        """

        self._created_or_builder = created_or_builder

    @property
    def default_instance_for_type(self):
        """Gets the default_instance_for_type of this Repository.  # noqa: E501


        :return: The default_instance_for_type of this Repository.  # noqa: E501
        :rtype: Repository
        """
        return self._default_instance_for_type

    @default_instance_for_type.setter
    def default_instance_for_type(self, default_instance_for_type):
        """Sets the default_instance_for_type of this Repository.


        :param default_instance_for_type: The default_instance_for_type of this Repository.  # noqa: E501
        :type: Repository
        """

        self._default_instance_for_type = default_instance_for_type

    @property
    def descriptor_for_type(self):
        """Gets the descriptor_for_type of this Repository.  # noqa: E501


        :return: The descriptor_for_type of this Repository.  # noqa: E501
        :rtype: Descriptor
        """
        return self._descriptor_for_type

    @descriptor_for_type.setter
    def descriptor_for_type(self, descriptor_for_type):
        """Sets the descriptor_for_type of this Repository.


        :param descriptor_for_type: The descriptor_for_type of this Repository.  # noqa: E501
        :type: Descriptor
        """

        self._descriptor_for_type = descriptor_for_type

    @property
    def id(self):
        """Gets the id of this Repository.  # noqa: E501


        :return: The id of this Repository.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Repository.


        :param id: The id of this Repository.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def id_bytes(self):
        """Gets the id_bytes of this Repository.  # noqa: E501


        :return: The id_bytes of this Repository.  # noqa: E501
        :rtype: ByteString
        """
        return self._id_bytes

    @id_bytes.setter
    def id_bytes(self, id_bytes):
        """Sets the id_bytes of this Repository.


        :param id_bytes: The id_bytes of this Repository.  # noqa: E501
        :type: ByteString
        """

        self._id_bytes = id_bytes

    @property
    def initialization_error_string(self):
        """Gets the initialization_error_string of this Repository.  # noqa: E501


        :return: The initialization_error_string of this Repository.  # noqa: E501
        :rtype: str
        """
        return self._initialization_error_string

    @initialization_error_string.setter
    def initialization_error_string(self, initialization_error_string):
        """Sets the initialization_error_string of this Repository.


        :param initialization_error_string: The initialization_error_string of this Repository.  # noqa: E501
        :type: str
        """

        self._initialization_error_string = initialization_error_string

    @property
    def initialized(self):
        """Gets the initialized of this Repository.  # noqa: E501


        :return: The initialized of this Repository.  # noqa: E501
        :rtype: bool
        """
        return self._initialized

    @initialized.setter
    def initialized(self, initialized):
        """Sets the initialized of this Repository.


        :param initialized: The initialized of this Repository.  # noqa: E501
        :type: bool
        """

        self._initialized = initialized

    @property
    def link(self):
        """Gets the link of this Repository.  # noqa: E501


        :return: The link of this Repository.  # noqa: E501
        :rtype: str
        """
        return self._link

    @link.setter
    def link(self, link):
        """Sets the link of this Repository.


        :param link: The link of this Repository.  # noqa: E501
        :type: str
        """

        self._link = link

    @property
    def link_bytes(self):
        """Gets the link_bytes of this Repository.  # noqa: E501


        :return: The link_bytes of this Repository.  # noqa: E501
        :rtype: ByteString
        """
        return self._link_bytes

    @link_bytes.setter
    def link_bytes(self, link_bytes):
        """Sets the link_bytes of this Repository.


        :param link_bytes: The link_bytes of this Repository.  # noqa: E501
        :type: ByteString
        """

        self._link_bytes = link_bytes

    @property
    def memoized_serialized_size(self):
        """Gets the memoized_serialized_size of this Repository.  # noqa: E501


        :return: The memoized_serialized_size of this Repository.  # noqa: E501
        :rtype: int
        """
        return self._memoized_serialized_size

    @memoized_serialized_size.setter
    def memoized_serialized_size(self, memoized_serialized_size):
        """Sets the memoized_serialized_size of this Repository.


        :param memoized_serialized_size: The memoized_serialized_size of this Repository.  # noqa: E501
        :type: int
        """

        self._memoized_serialized_size = memoized_serialized_size

    @property
    def name(self):
        """Gets the name of this Repository.  # noqa: E501


        :return: The name of this Repository.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Repository.


        :param name: The name of this Repository.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def name_bytes(self):
        """Gets the name_bytes of this Repository.  # noqa: E501


        :return: The name_bytes of this Repository.  # noqa: E501
        :rtype: ByteString
        """
        return self._name_bytes

    @name_bytes.setter
    def name_bytes(self, name_bytes):
        """Sets the name_bytes of this Repository.


        :param name_bytes: The name_bytes of this Repository.  # noqa: E501
        :type: ByteString
        """

        self._name_bytes = name_bytes

    @property
    def namespace(self):
        """Gets the namespace of this Repository.  # noqa: E501


        :return: The namespace of this Repository.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this Repository.


        :param namespace: The namespace of this Repository.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def namespace_bytes(self):
        """Gets the namespace_bytes of this Repository.  # noqa: E501


        :return: The namespace_bytes of this Repository.  # noqa: E501
        :rtype: ByteString
        """
        return self._namespace_bytes

    @namespace_bytes.setter
    def namespace_bytes(self, namespace_bytes):
        """Sets the namespace_bytes of this Repository.


        :param namespace_bytes: The namespace_bytes of this Repository.  # noqa: E501
        :type: ByteString
        """

        self._namespace_bytes = namespace_bytes

    @property
    def parser_for_type(self):
        """Gets the parser_for_type of this Repository.  # noqa: E501


        :return: The parser_for_type of this Repository.  # noqa: E501
        :rtype: ParserRepository
        """
        return self._parser_for_type

    @parser_for_type.setter
    def parser_for_type(self, parser_for_type):
        """Sets the parser_for_type of this Repository.


        :param parser_for_type: The parser_for_type of this Repository.  # noqa: E501
        :type: ParserRepository
        """

        self._parser_for_type = parser_for_type

    @property
    def perm(self):
        """Gets the perm of this Repository.  # noqa: E501


        :return: The perm of this Repository.  # noqa: E501
        :rtype: Perm
        """
        return self._perm

    @perm.setter
    def perm(self, perm):
        """Sets the perm of this Repository.


        :param perm: The perm of this Repository.  # noqa: E501
        :type: Perm
        """

        self._perm = perm

    @property
    def perm_or_builder(self):
        """Gets the perm_or_builder of this Repository.  # noqa: E501


        :return: The perm_or_builder of this Repository.  # noqa: E501
        :rtype: PermOrBuilder
        """
        return self._perm_or_builder

    @perm_or_builder.setter
    def perm_or_builder(self, perm_or_builder):
        """Sets the perm_or_builder of this Repository.


        :param perm_or_builder: The perm_or_builder of this Repository.  # noqa: E501
        :type: PermOrBuilder
        """

        self._perm_or_builder = perm_or_builder

    @property
    def private(self):
        """Gets the private of this Repository.  # noqa: E501


        :return: The private of this Repository.  # noqa: E501
        :rtype: bool
        """
        return self._private

    @private.setter
    def private(self, private):
        """Sets the private of this Repository.


        :param private: The private of this Repository.  # noqa: E501
        :type: bool
        """

        self._private = private

    @property
    def serialized_size(self):
        """Gets the serialized_size of this Repository.  # noqa: E501


        :return: The serialized_size of this Repository.  # noqa: E501
        :rtype: int
        """
        return self._serialized_size

    @serialized_size.setter
    def serialized_size(self, serialized_size):
        """Sets the serialized_size of this Repository.


        :param serialized_size: The serialized_size of this Repository.  # noqa: E501
        :type: int
        """

        self._serialized_size = serialized_size

    @property
    def unknown_fields(self):
        """Gets the unknown_fields of this Repository.  # noqa: E501


        :return: The unknown_fields of this Repository.  # noqa: E501
        :rtype: UnknownFieldSet
        """
        return self._unknown_fields

    @unknown_fields.setter
    def unknown_fields(self, unknown_fields):
        """Sets the unknown_fields of this Repository.


        :param unknown_fields: The unknown_fields of this Repository.  # noqa: E501
        :type: UnknownFieldSet
        """

        self._unknown_fields = unknown_fields

    @property
    def updated(self):
        """Gets the updated of this Repository.  # noqa: E501


        :return: The updated of this Repository.  # noqa: E501
        :rtype: Timestamp
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this Repository.


        :param updated: The updated of this Repository.  # noqa: E501
        :type: Timestamp
        """

        self._updated = updated

    @property
    def updated_or_builder(self):
        """Gets the updated_or_builder of this Repository.  # noqa: E501


        :return: The updated_or_builder of this Repository.  # noqa: E501
        :rtype: TimestampOrBuilder
        """
        return self._updated_or_builder

    @updated_or_builder.setter
    def updated_or_builder(self, updated_or_builder):
        """Sets the updated_or_builder of this Repository.


        :param updated_or_builder: The updated_or_builder of this Repository.  # noqa: E501
        :type: TimestampOrBuilder
        """

        self._updated_or_builder = updated_or_builder

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Repository, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Repository):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
