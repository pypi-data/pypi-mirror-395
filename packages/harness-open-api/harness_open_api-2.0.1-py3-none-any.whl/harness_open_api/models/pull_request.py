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

class PullRequest(object):
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
        'author': 'PipelineUser',
        'author_or_builder': 'UserOrBuilder',
        'base': 'Reference',
        'base_or_builder': 'ReferenceOrBuilder',
        'body': 'str',
        'body_bytes': 'ByteString',
        'closed': 'bool',
        'commits_count': 'int',
        'commits_list': 'list[Commit]',
        'commits_or_builder_list': 'list[CommitOrBuilder]',
        'created': 'Timestamp',
        'created_or_builder': 'TimestampOrBuilder',
        'default_instance_for_type': 'PullRequest',
        'descriptor_for_type': 'Descriptor',
        'fork': 'str',
        'fork_bytes': 'ByteString',
        'head': 'Reference',
        'head_or_builder': 'ReferenceOrBuilder',
        'initialization_error_string': 'str',
        'initialized': 'bool',
        'labels_count': 'int',
        'labels_list': 'list[Label]',
        'labels_or_builder_list': 'list[LabelOrBuilder]',
        'link': 'str',
        'link_bytes': 'ByteString',
        'memoized_serialized_size': 'int',
        'merge_sha': 'str',
        'merge_sha_bytes': 'ByteString',
        'merged': 'bool',
        'number': 'int',
        'parser_for_type': 'ParserPullRequest',
        'ref': 'str',
        'ref_bytes': 'ByteString',
        'serialized_size': 'int',
        'sha': 'str',
        'sha_bytes': 'ByteString',
        'source': 'str',
        'source_bytes': 'ByteString',
        'target': 'str',
        'target_bytes': 'ByteString',
        'title': 'str',
        'title_bytes': 'ByteString',
        'unknown_fields': 'UnknownFieldSet',
        'updated': 'Timestamp',
        'updated_or_builder': 'TimestampOrBuilder'
    }

    attribute_map = {
        'all_fields': 'allFields',
        'author': 'author',
        'author_or_builder': 'authorOrBuilder',
        'base': 'base',
        'base_or_builder': 'baseOrBuilder',
        'body': 'body',
        'body_bytes': 'bodyBytes',
        'closed': 'closed',
        'commits_count': 'commitsCount',
        'commits_list': 'commitsList',
        'commits_or_builder_list': 'commitsOrBuilderList',
        'created': 'created',
        'created_or_builder': 'createdOrBuilder',
        'default_instance_for_type': 'defaultInstanceForType',
        'descriptor_for_type': 'descriptorForType',
        'fork': 'fork',
        'fork_bytes': 'forkBytes',
        'head': 'head',
        'head_or_builder': 'headOrBuilder',
        'initialization_error_string': 'initializationErrorString',
        'initialized': 'initialized',
        'labels_count': 'labelsCount',
        'labels_list': 'labelsList',
        'labels_or_builder_list': 'labelsOrBuilderList',
        'link': 'link',
        'link_bytes': 'linkBytes',
        'memoized_serialized_size': 'memoizedSerializedSize',
        'merge_sha': 'mergeSha',
        'merge_sha_bytes': 'mergeShaBytes',
        'merged': 'merged',
        'number': 'number',
        'parser_for_type': 'parserForType',
        'ref': 'ref',
        'ref_bytes': 'refBytes',
        'serialized_size': 'serializedSize',
        'sha': 'sha',
        'sha_bytes': 'shaBytes',
        'source': 'source',
        'source_bytes': 'sourceBytes',
        'target': 'target',
        'target_bytes': 'targetBytes',
        'title': 'title',
        'title_bytes': 'titleBytes',
        'unknown_fields': 'unknownFields',
        'updated': 'updated',
        'updated_or_builder': 'updatedOrBuilder'
    }

    def __init__(self, all_fields=None, author=None, author_or_builder=None, base=None, base_or_builder=None, body=None, body_bytes=None, closed=None, commits_count=None, commits_list=None, commits_or_builder_list=None, created=None, created_or_builder=None, default_instance_for_type=None, descriptor_for_type=None, fork=None, fork_bytes=None, head=None, head_or_builder=None, initialization_error_string=None, initialized=None, labels_count=None, labels_list=None, labels_or_builder_list=None, link=None, link_bytes=None, memoized_serialized_size=None, merge_sha=None, merge_sha_bytes=None, merged=None, number=None, parser_for_type=None, ref=None, ref_bytes=None, serialized_size=None, sha=None, sha_bytes=None, source=None, source_bytes=None, target=None, target_bytes=None, title=None, title_bytes=None, unknown_fields=None, updated=None, updated_or_builder=None):  # noqa: E501
        """PullRequest - a model defined in Swagger"""  # noqa: E501
        self._all_fields = None
        self._author = None
        self._author_or_builder = None
        self._base = None
        self._base_or_builder = None
        self._body = None
        self._body_bytes = None
        self._closed = None
        self._commits_count = None
        self._commits_list = None
        self._commits_or_builder_list = None
        self._created = None
        self._created_or_builder = None
        self._default_instance_for_type = None
        self._descriptor_for_type = None
        self._fork = None
        self._fork_bytes = None
        self._head = None
        self._head_or_builder = None
        self._initialization_error_string = None
        self._initialized = None
        self._labels_count = None
        self._labels_list = None
        self._labels_or_builder_list = None
        self._link = None
        self._link_bytes = None
        self._memoized_serialized_size = None
        self._merge_sha = None
        self._merge_sha_bytes = None
        self._merged = None
        self._number = None
        self._parser_for_type = None
        self._ref = None
        self._ref_bytes = None
        self._serialized_size = None
        self._sha = None
        self._sha_bytes = None
        self._source = None
        self._source_bytes = None
        self._target = None
        self._target_bytes = None
        self._title = None
        self._title_bytes = None
        self._unknown_fields = None
        self._updated = None
        self._updated_or_builder = None
        self.discriminator = None
        if all_fields is not None:
            self.all_fields = all_fields
        if author is not None:
            self.author = author
        if author_or_builder is not None:
            self.author_or_builder = author_or_builder
        if base is not None:
            self.base = base
        if base_or_builder is not None:
            self.base_or_builder = base_or_builder
        if body is not None:
            self.body = body
        if body_bytes is not None:
            self.body_bytes = body_bytes
        if closed is not None:
            self.closed = closed
        if commits_count is not None:
            self.commits_count = commits_count
        if commits_list is not None:
            self.commits_list = commits_list
        if commits_or_builder_list is not None:
            self.commits_or_builder_list = commits_or_builder_list
        if created is not None:
            self.created = created
        if created_or_builder is not None:
            self.created_or_builder = created_or_builder
        if default_instance_for_type is not None:
            self.default_instance_for_type = default_instance_for_type
        if descriptor_for_type is not None:
            self.descriptor_for_type = descriptor_for_type
        if fork is not None:
            self.fork = fork
        if fork_bytes is not None:
            self.fork_bytes = fork_bytes
        if head is not None:
            self.head = head
        if head_or_builder is not None:
            self.head_or_builder = head_or_builder
        if initialization_error_string is not None:
            self.initialization_error_string = initialization_error_string
        if initialized is not None:
            self.initialized = initialized
        if labels_count is not None:
            self.labels_count = labels_count
        if labels_list is not None:
            self.labels_list = labels_list
        if labels_or_builder_list is not None:
            self.labels_or_builder_list = labels_or_builder_list
        if link is not None:
            self.link = link
        if link_bytes is not None:
            self.link_bytes = link_bytes
        if memoized_serialized_size is not None:
            self.memoized_serialized_size = memoized_serialized_size
        if merge_sha is not None:
            self.merge_sha = merge_sha
        if merge_sha_bytes is not None:
            self.merge_sha_bytes = merge_sha_bytes
        if merged is not None:
            self.merged = merged
        if number is not None:
            self.number = number
        if parser_for_type is not None:
            self.parser_for_type = parser_for_type
        if ref is not None:
            self.ref = ref
        if ref_bytes is not None:
            self.ref_bytes = ref_bytes
        if serialized_size is not None:
            self.serialized_size = serialized_size
        if sha is not None:
            self.sha = sha
        if sha_bytes is not None:
            self.sha_bytes = sha_bytes
        if source is not None:
            self.source = source
        if source_bytes is not None:
            self.source_bytes = source_bytes
        if target is not None:
            self.target = target
        if target_bytes is not None:
            self.target_bytes = target_bytes
        if title is not None:
            self.title = title
        if title_bytes is not None:
            self.title_bytes = title_bytes
        if unknown_fields is not None:
            self.unknown_fields = unknown_fields
        if updated is not None:
            self.updated = updated
        if updated_or_builder is not None:
            self.updated_or_builder = updated_or_builder

    @property
    def all_fields(self):
        """Gets the all_fields of this PullRequest.  # noqa: E501


        :return: The all_fields of this PullRequest.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._all_fields

    @all_fields.setter
    def all_fields(self, all_fields):
        """Sets the all_fields of this PullRequest.


        :param all_fields: The all_fields of this PullRequest.  # noqa: E501
        :type: dict(str, object)
        """

        self._all_fields = all_fields

    @property
    def author(self):
        """Gets the author of this PullRequest.  # noqa: E501


        :return: The author of this PullRequest.  # noqa: E501
        :rtype: PipelineUser
        """
        return self._author

    @author.setter
    def author(self, author):
        """Sets the author of this PullRequest.


        :param author: The author of this PullRequest.  # noqa: E501
        :type: PipelineUser
        """

        self._author = author

    @property
    def author_or_builder(self):
        """Gets the author_or_builder of this PullRequest.  # noqa: E501


        :return: The author_or_builder of this PullRequest.  # noqa: E501
        :rtype: UserOrBuilder
        """
        return self._author_or_builder

    @author_or_builder.setter
    def author_or_builder(self, author_or_builder):
        """Sets the author_or_builder of this PullRequest.


        :param author_or_builder: The author_or_builder of this PullRequest.  # noqa: E501
        :type: UserOrBuilder
        """

        self._author_or_builder = author_or_builder

    @property
    def base(self):
        """Gets the base of this PullRequest.  # noqa: E501


        :return: The base of this PullRequest.  # noqa: E501
        :rtype: Reference
        """
        return self._base

    @base.setter
    def base(self, base):
        """Sets the base of this PullRequest.


        :param base: The base of this PullRequest.  # noqa: E501
        :type: Reference
        """

        self._base = base

    @property
    def base_or_builder(self):
        """Gets the base_or_builder of this PullRequest.  # noqa: E501


        :return: The base_or_builder of this PullRequest.  # noqa: E501
        :rtype: ReferenceOrBuilder
        """
        return self._base_or_builder

    @base_or_builder.setter
    def base_or_builder(self, base_or_builder):
        """Sets the base_or_builder of this PullRequest.


        :param base_or_builder: The base_or_builder of this PullRequest.  # noqa: E501
        :type: ReferenceOrBuilder
        """

        self._base_or_builder = base_or_builder

    @property
    def body(self):
        """Gets the body of this PullRequest.  # noqa: E501


        :return: The body of this PullRequest.  # noqa: E501
        :rtype: str
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this PullRequest.


        :param body: The body of this PullRequest.  # noqa: E501
        :type: str
        """

        self._body = body

    @property
    def body_bytes(self):
        """Gets the body_bytes of this PullRequest.  # noqa: E501


        :return: The body_bytes of this PullRequest.  # noqa: E501
        :rtype: ByteString
        """
        return self._body_bytes

    @body_bytes.setter
    def body_bytes(self, body_bytes):
        """Sets the body_bytes of this PullRequest.


        :param body_bytes: The body_bytes of this PullRequest.  # noqa: E501
        :type: ByteString
        """

        self._body_bytes = body_bytes

    @property
    def closed(self):
        """Gets the closed of this PullRequest.  # noqa: E501


        :return: The closed of this PullRequest.  # noqa: E501
        :rtype: bool
        """
        return self._closed

    @closed.setter
    def closed(self, closed):
        """Sets the closed of this PullRequest.


        :param closed: The closed of this PullRequest.  # noqa: E501
        :type: bool
        """

        self._closed = closed

    @property
    def commits_count(self):
        """Gets the commits_count of this PullRequest.  # noqa: E501


        :return: The commits_count of this PullRequest.  # noqa: E501
        :rtype: int
        """
        return self._commits_count

    @commits_count.setter
    def commits_count(self, commits_count):
        """Sets the commits_count of this PullRequest.


        :param commits_count: The commits_count of this PullRequest.  # noqa: E501
        :type: int
        """

        self._commits_count = commits_count

    @property
    def commits_list(self):
        """Gets the commits_list of this PullRequest.  # noqa: E501


        :return: The commits_list of this PullRequest.  # noqa: E501
        :rtype: list[Commit]
        """
        return self._commits_list

    @commits_list.setter
    def commits_list(self, commits_list):
        """Sets the commits_list of this PullRequest.


        :param commits_list: The commits_list of this PullRequest.  # noqa: E501
        :type: list[Commit]
        """

        self._commits_list = commits_list

    @property
    def commits_or_builder_list(self):
        """Gets the commits_or_builder_list of this PullRequest.  # noqa: E501


        :return: The commits_or_builder_list of this PullRequest.  # noqa: E501
        :rtype: list[CommitOrBuilder]
        """
        return self._commits_or_builder_list

    @commits_or_builder_list.setter
    def commits_or_builder_list(self, commits_or_builder_list):
        """Sets the commits_or_builder_list of this PullRequest.


        :param commits_or_builder_list: The commits_or_builder_list of this PullRequest.  # noqa: E501
        :type: list[CommitOrBuilder]
        """

        self._commits_or_builder_list = commits_or_builder_list

    @property
    def created(self):
        """Gets the created of this PullRequest.  # noqa: E501


        :return: The created of this PullRequest.  # noqa: E501
        :rtype: Timestamp
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this PullRequest.


        :param created: The created of this PullRequest.  # noqa: E501
        :type: Timestamp
        """

        self._created = created

    @property
    def created_or_builder(self):
        """Gets the created_or_builder of this PullRequest.  # noqa: E501


        :return: The created_or_builder of this PullRequest.  # noqa: E501
        :rtype: TimestampOrBuilder
        """
        return self._created_or_builder

    @created_or_builder.setter
    def created_or_builder(self, created_or_builder):
        """Sets the created_or_builder of this PullRequest.


        :param created_or_builder: The created_or_builder of this PullRequest.  # noqa: E501
        :type: TimestampOrBuilder
        """

        self._created_or_builder = created_or_builder

    @property
    def default_instance_for_type(self):
        """Gets the default_instance_for_type of this PullRequest.  # noqa: E501


        :return: The default_instance_for_type of this PullRequest.  # noqa: E501
        :rtype: PullRequest
        """
        return self._default_instance_for_type

    @default_instance_for_type.setter
    def default_instance_for_type(self, default_instance_for_type):
        """Sets the default_instance_for_type of this PullRequest.


        :param default_instance_for_type: The default_instance_for_type of this PullRequest.  # noqa: E501
        :type: PullRequest
        """

        self._default_instance_for_type = default_instance_for_type

    @property
    def descriptor_for_type(self):
        """Gets the descriptor_for_type of this PullRequest.  # noqa: E501


        :return: The descriptor_for_type of this PullRequest.  # noqa: E501
        :rtype: Descriptor
        """
        return self._descriptor_for_type

    @descriptor_for_type.setter
    def descriptor_for_type(self, descriptor_for_type):
        """Sets the descriptor_for_type of this PullRequest.


        :param descriptor_for_type: The descriptor_for_type of this PullRequest.  # noqa: E501
        :type: Descriptor
        """

        self._descriptor_for_type = descriptor_for_type

    @property
    def fork(self):
        """Gets the fork of this PullRequest.  # noqa: E501


        :return: The fork of this PullRequest.  # noqa: E501
        :rtype: str
        """
        return self._fork

    @fork.setter
    def fork(self, fork):
        """Sets the fork of this PullRequest.


        :param fork: The fork of this PullRequest.  # noqa: E501
        :type: str
        """

        self._fork = fork

    @property
    def fork_bytes(self):
        """Gets the fork_bytes of this PullRequest.  # noqa: E501


        :return: The fork_bytes of this PullRequest.  # noqa: E501
        :rtype: ByteString
        """
        return self._fork_bytes

    @fork_bytes.setter
    def fork_bytes(self, fork_bytes):
        """Sets the fork_bytes of this PullRequest.


        :param fork_bytes: The fork_bytes of this PullRequest.  # noqa: E501
        :type: ByteString
        """

        self._fork_bytes = fork_bytes

    @property
    def head(self):
        """Gets the head of this PullRequest.  # noqa: E501


        :return: The head of this PullRequest.  # noqa: E501
        :rtype: Reference
        """
        return self._head

    @head.setter
    def head(self, head):
        """Sets the head of this PullRequest.


        :param head: The head of this PullRequest.  # noqa: E501
        :type: Reference
        """

        self._head = head

    @property
    def head_or_builder(self):
        """Gets the head_or_builder of this PullRequest.  # noqa: E501


        :return: The head_or_builder of this PullRequest.  # noqa: E501
        :rtype: ReferenceOrBuilder
        """
        return self._head_or_builder

    @head_or_builder.setter
    def head_or_builder(self, head_or_builder):
        """Sets the head_or_builder of this PullRequest.


        :param head_or_builder: The head_or_builder of this PullRequest.  # noqa: E501
        :type: ReferenceOrBuilder
        """

        self._head_or_builder = head_or_builder

    @property
    def initialization_error_string(self):
        """Gets the initialization_error_string of this PullRequest.  # noqa: E501


        :return: The initialization_error_string of this PullRequest.  # noqa: E501
        :rtype: str
        """
        return self._initialization_error_string

    @initialization_error_string.setter
    def initialization_error_string(self, initialization_error_string):
        """Sets the initialization_error_string of this PullRequest.


        :param initialization_error_string: The initialization_error_string of this PullRequest.  # noqa: E501
        :type: str
        """

        self._initialization_error_string = initialization_error_string

    @property
    def initialized(self):
        """Gets the initialized of this PullRequest.  # noqa: E501


        :return: The initialized of this PullRequest.  # noqa: E501
        :rtype: bool
        """
        return self._initialized

    @initialized.setter
    def initialized(self, initialized):
        """Sets the initialized of this PullRequest.


        :param initialized: The initialized of this PullRequest.  # noqa: E501
        :type: bool
        """

        self._initialized = initialized

    @property
    def labels_count(self):
        """Gets the labels_count of this PullRequest.  # noqa: E501


        :return: The labels_count of this PullRequest.  # noqa: E501
        :rtype: int
        """
        return self._labels_count

    @labels_count.setter
    def labels_count(self, labels_count):
        """Sets the labels_count of this PullRequest.


        :param labels_count: The labels_count of this PullRequest.  # noqa: E501
        :type: int
        """

        self._labels_count = labels_count

    @property
    def labels_list(self):
        """Gets the labels_list of this PullRequest.  # noqa: E501


        :return: The labels_list of this PullRequest.  # noqa: E501
        :rtype: list[Label]
        """
        return self._labels_list

    @labels_list.setter
    def labels_list(self, labels_list):
        """Sets the labels_list of this PullRequest.


        :param labels_list: The labels_list of this PullRequest.  # noqa: E501
        :type: list[Label]
        """

        self._labels_list = labels_list

    @property
    def labels_or_builder_list(self):
        """Gets the labels_or_builder_list of this PullRequest.  # noqa: E501


        :return: The labels_or_builder_list of this PullRequest.  # noqa: E501
        :rtype: list[LabelOrBuilder]
        """
        return self._labels_or_builder_list

    @labels_or_builder_list.setter
    def labels_or_builder_list(self, labels_or_builder_list):
        """Sets the labels_or_builder_list of this PullRequest.


        :param labels_or_builder_list: The labels_or_builder_list of this PullRequest.  # noqa: E501
        :type: list[LabelOrBuilder]
        """

        self._labels_or_builder_list = labels_or_builder_list

    @property
    def link(self):
        """Gets the link of this PullRequest.  # noqa: E501


        :return: The link of this PullRequest.  # noqa: E501
        :rtype: str
        """
        return self._link

    @link.setter
    def link(self, link):
        """Sets the link of this PullRequest.


        :param link: The link of this PullRequest.  # noqa: E501
        :type: str
        """

        self._link = link

    @property
    def link_bytes(self):
        """Gets the link_bytes of this PullRequest.  # noqa: E501


        :return: The link_bytes of this PullRequest.  # noqa: E501
        :rtype: ByteString
        """
        return self._link_bytes

    @link_bytes.setter
    def link_bytes(self, link_bytes):
        """Sets the link_bytes of this PullRequest.


        :param link_bytes: The link_bytes of this PullRequest.  # noqa: E501
        :type: ByteString
        """

        self._link_bytes = link_bytes

    @property
    def memoized_serialized_size(self):
        """Gets the memoized_serialized_size of this PullRequest.  # noqa: E501


        :return: The memoized_serialized_size of this PullRequest.  # noqa: E501
        :rtype: int
        """
        return self._memoized_serialized_size

    @memoized_serialized_size.setter
    def memoized_serialized_size(self, memoized_serialized_size):
        """Sets the memoized_serialized_size of this PullRequest.


        :param memoized_serialized_size: The memoized_serialized_size of this PullRequest.  # noqa: E501
        :type: int
        """

        self._memoized_serialized_size = memoized_serialized_size

    @property
    def merge_sha(self):
        """Gets the merge_sha of this PullRequest.  # noqa: E501


        :return: The merge_sha of this PullRequest.  # noqa: E501
        :rtype: str
        """
        return self._merge_sha

    @merge_sha.setter
    def merge_sha(self, merge_sha):
        """Sets the merge_sha of this PullRequest.


        :param merge_sha: The merge_sha of this PullRequest.  # noqa: E501
        :type: str
        """

        self._merge_sha = merge_sha

    @property
    def merge_sha_bytes(self):
        """Gets the merge_sha_bytes of this PullRequest.  # noqa: E501


        :return: The merge_sha_bytes of this PullRequest.  # noqa: E501
        :rtype: ByteString
        """
        return self._merge_sha_bytes

    @merge_sha_bytes.setter
    def merge_sha_bytes(self, merge_sha_bytes):
        """Sets the merge_sha_bytes of this PullRequest.


        :param merge_sha_bytes: The merge_sha_bytes of this PullRequest.  # noqa: E501
        :type: ByteString
        """

        self._merge_sha_bytes = merge_sha_bytes

    @property
    def merged(self):
        """Gets the merged of this PullRequest.  # noqa: E501


        :return: The merged of this PullRequest.  # noqa: E501
        :rtype: bool
        """
        return self._merged

    @merged.setter
    def merged(self, merged):
        """Sets the merged of this PullRequest.


        :param merged: The merged of this PullRequest.  # noqa: E501
        :type: bool
        """

        self._merged = merged

    @property
    def number(self):
        """Gets the number of this PullRequest.  # noqa: E501


        :return: The number of this PullRequest.  # noqa: E501
        :rtype: int
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this PullRequest.


        :param number: The number of this PullRequest.  # noqa: E501
        :type: int
        """

        self._number = number

    @property
    def parser_for_type(self):
        """Gets the parser_for_type of this PullRequest.  # noqa: E501


        :return: The parser_for_type of this PullRequest.  # noqa: E501
        :rtype: ParserPullRequest
        """
        return self._parser_for_type

    @parser_for_type.setter
    def parser_for_type(self, parser_for_type):
        """Sets the parser_for_type of this PullRequest.


        :param parser_for_type: The parser_for_type of this PullRequest.  # noqa: E501
        :type: ParserPullRequest
        """

        self._parser_for_type = parser_for_type

    @property
    def ref(self):
        """Gets the ref of this PullRequest.  # noqa: E501


        :return: The ref of this PullRequest.  # noqa: E501
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """Sets the ref of this PullRequest.


        :param ref: The ref of this PullRequest.  # noqa: E501
        :type: str
        """

        self._ref = ref

    @property
    def ref_bytes(self):
        """Gets the ref_bytes of this PullRequest.  # noqa: E501


        :return: The ref_bytes of this PullRequest.  # noqa: E501
        :rtype: ByteString
        """
        return self._ref_bytes

    @ref_bytes.setter
    def ref_bytes(self, ref_bytes):
        """Sets the ref_bytes of this PullRequest.


        :param ref_bytes: The ref_bytes of this PullRequest.  # noqa: E501
        :type: ByteString
        """

        self._ref_bytes = ref_bytes

    @property
    def serialized_size(self):
        """Gets the serialized_size of this PullRequest.  # noqa: E501


        :return: The serialized_size of this PullRequest.  # noqa: E501
        :rtype: int
        """
        return self._serialized_size

    @serialized_size.setter
    def serialized_size(self, serialized_size):
        """Sets the serialized_size of this PullRequest.


        :param serialized_size: The serialized_size of this PullRequest.  # noqa: E501
        :type: int
        """

        self._serialized_size = serialized_size

    @property
    def sha(self):
        """Gets the sha of this PullRequest.  # noqa: E501


        :return: The sha of this PullRequest.  # noqa: E501
        :rtype: str
        """
        return self._sha

    @sha.setter
    def sha(self, sha):
        """Sets the sha of this PullRequest.


        :param sha: The sha of this PullRequest.  # noqa: E501
        :type: str
        """

        self._sha = sha

    @property
    def sha_bytes(self):
        """Gets the sha_bytes of this PullRequest.  # noqa: E501


        :return: The sha_bytes of this PullRequest.  # noqa: E501
        :rtype: ByteString
        """
        return self._sha_bytes

    @sha_bytes.setter
    def sha_bytes(self, sha_bytes):
        """Sets the sha_bytes of this PullRequest.


        :param sha_bytes: The sha_bytes of this PullRequest.  # noqa: E501
        :type: ByteString
        """

        self._sha_bytes = sha_bytes

    @property
    def source(self):
        """Gets the source of this PullRequest.  # noqa: E501


        :return: The source of this PullRequest.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this PullRequest.


        :param source: The source of this PullRequest.  # noqa: E501
        :type: str
        """

        self._source = source

    @property
    def source_bytes(self):
        """Gets the source_bytes of this PullRequest.  # noqa: E501


        :return: The source_bytes of this PullRequest.  # noqa: E501
        :rtype: ByteString
        """
        return self._source_bytes

    @source_bytes.setter
    def source_bytes(self, source_bytes):
        """Sets the source_bytes of this PullRequest.


        :param source_bytes: The source_bytes of this PullRequest.  # noqa: E501
        :type: ByteString
        """

        self._source_bytes = source_bytes

    @property
    def target(self):
        """Gets the target of this PullRequest.  # noqa: E501


        :return: The target of this PullRequest.  # noqa: E501
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """Sets the target of this PullRequest.


        :param target: The target of this PullRequest.  # noqa: E501
        :type: str
        """

        self._target = target

    @property
    def target_bytes(self):
        """Gets the target_bytes of this PullRequest.  # noqa: E501


        :return: The target_bytes of this PullRequest.  # noqa: E501
        :rtype: ByteString
        """
        return self._target_bytes

    @target_bytes.setter
    def target_bytes(self, target_bytes):
        """Sets the target_bytes of this PullRequest.


        :param target_bytes: The target_bytes of this PullRequest.  # noqa: E501
        :type: ByteString
        """

        self._target_bytes = target_bytes

    @property
    def title(self):
        """Gets the title of this PullRequest.  # noqa: E501


        :return: The title of this PullRequest.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this PullRequest.


        :param title: The title of this PullRequest.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def title_bytes(self):
        """Gets the title_bytes of this PullRequest.  # noqa: E501


        :return: The title_bytes of this PullRequest.  # noqa: E501
        :rtype: ByteString
        """
        return self._title_bytes

    @title_bytes.setter
    def title_bytes(self, title_bytes):
        """Sets the title_bytes of this PullRequest.


        :param title_bytes: The title_bytes of this PullRequest.  # noqa: E501
        :type: ByteString
        """

        self._title_bytes = title_bytes

    @property
    def unknown_fields(self):
        """Gets the unknown_fields of this PullRequest.  # noqa: E501


        :return: The unknown_fields of this PullRequest.  # noqa: E501
        :rtype: UnknownFieldSet
        """
        return self._unknown_fields

    @unknown_fields.setter
    def unknown_fields(self, unknown_fields):
        """Sets the unknown_fields of this PullRequest.


        :param unknown_fields: The unknown_fields of this PullRequest.  # noqa: E501
        :type: UnknownFieldSet
        """

        self._unknown_fields = unknown_fields

    @property
    def updated(self):
        """Gets the updated of this PullRequest.  # noqa: E501


        :return: The updated of this PullRequest.  # noqa: E501
        :rtype: Timestamp
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this PullRequest.


        :param updated: The updated of this PullRequest.  # noqa: E501
        :type: Timestamp
        """

        self._updated = updated

    @property
    def updated_or_builder(self):
        """Gets the updated_or_builder of this PullRequest.  # noqa: E501


        :return: The updated_or_builder of this PullRequest.  # noqa: E501
        :rtype: TimestampOrBuilder
        """
        return self._updated_or_builder

    @updated_or_builder.setter
    def updated_or_builder(self, updated_or_builder):
        """Sets the updated_or_builder of this PullRequest.


        :param updated_or_builder: The updated_or_builder of this PullRequest.  # noqa: E501
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
        if issubclass(PullRequest, dict):
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
        if not isinstance(other, PullRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
