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

class PushHookOrBuilder(object):
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
        'after': 'str',
        'after_bytes': 'ByteString',
        'all_fields': 'dict(str, object)',
        'base_ref': 'str',
        'base_ref_bytes': 'ByteString',
        'before': 'str',
        'before_bytes': 'ByteString',
        'commit': 'Commit',
        'commit_or_builder': 'CommitOrBuilder',
        'commits_count': 'int',
        'commits_list': 'list[Commit]',
        'commits_or_builder_list': 'list[CommitOrBuilder]',
        'default_instance_for_type': 'Message',
        'descriptor_for_type': 'Descriptor',
        'initialization_error_string': 'str',
        'initialized': 'bool',
        'ref': 'str',
        'ref_bytes': 'ByteString',
        'repo': 'Repository',
        'repo_or_builder': 'RepositoryOrBuilder',
        'sender': 'PipelineUser',
        'sender_or_builder': 'UserOrBuilder',
        'unknown_fields': 'UnknownFieldSet'
    }

    attribute_map = {
        'after': 'after',
        'after_bytes': 'afterBytes',
        'all_fields': 'allFields',
        'base_ref': 'baseRef',
        'base_ref_bytes': 'baseRefBytes',
        'before': 'before',
        'before_bytes': 'beforeBytes',
        'commit': 'commit',
        'commit_or_builder': 'commitOrBuilder',
        'commits_count': 'commitsCount',
        'commits_list': 'commitsList',
        'commits_or_builder_list': 'commitsOrBuilderList',
        'default_instance_for_type': 'defaultInstanceForType',
        'descriptor_for_type': 'descriptorForType',
        'initialization_error_string': 'initializationErrorString',
        'initialized': 'initialized',
        'ref': 'ref',
        'ref_bytes': 'refBytes',
        'repo': 'repo',
        'repo_or_builder': 'repoOrBuilder',
        'sender': 'sender',
        'sender_or_builder': 'senderOrBuilder',
        'unknown_fields': 'unknownFields'
    }

    def __init__(self, after=None, after_bytes=None, all_fields=None, base_ref=None, base_ref_bytes=None, before=None, before_bytes=None, commit=None, commit_or_builder=None, commits_count=None, commits_list=None, commits_or_builder_list=None, default_instance_for_type=None, descriptor_for_type=None, initialization_error_string=None, initialized=None, ref=None, ref_bytes=None, repo=None, repo_or_builder=None, sender=None, sender_or_builder=None, unknown_fields=None):  # noqa: E501
        """PushHookOrBuilder - a model defined in Swagger"""  # noqa: E501
        self._after = None
        self._after_bytes = None
        self._all_fields = None
        self._base_ref = None
        self._base_ref_bytes = None
        self._before = None
        self._before_bytes = None
        self._commit = None
        self._commit_or_builder = None
        self._commits_count = None
        self._commits_list = None
        self._commits_or_builder_list = None
        self._default_instance_for_type = None
        self._descriptor_for_type = None
        self._initialization_error_string = None
        self._initialized = None
        self._ref = None
        self._ref_bytes = None
        self._repo = None
        self._repo_or_builder = None
        self._sender = None
        self._sender_or_builder = None
        self._unknown_fields = None
        self.discriminator = None
        if after is not None:
            self.after = after
        if after_bytes is not None:
            self.after_bytes = after_bytes
        if all_fields is not None:
            self.all_fields = all_fields
        if base_ref is not None:
            self.base_ref = base_ref
        if base_ref_bytes is not None:
            self.base_ref_bytes = base_ref_bytes
        if before is not None:
            self.before = before
        if before_bytes is not None:
            self.before_bytes = before_bytes
        if commit is not None:
            self.commit = commit
        if commit_or_builder is not None:
            self.commit_or_builder = commit_or_builder
        if commits_count is not None:
            self.commits_count = commits_count
        if commits_list is not None:
            self.commits_list = commits_list
        if commits_or_builder_list is not None:
            self.commits_or_builder_list = commits_or_builder_list
        if default_instance_for_type is not None:
            self.default_instance_for_type = default_instance_for_type
        if descriptor_for_type is not None:
            self.descriptor_for_type = descriptor_for_type
        if initialization_error_string is not None:
            self.initialization_error_string = initialization_error_string
        if initialized is not None:
            self.initialized = initialized
        if ref is not None:
            self.ref = ref
        if ref_bytes is not None:
            self.ref_bytes = ref_bytes
        if repo is not None:
            self.repo = repo
        if repo_or_builder is not None:
            self.repo_or_builder = repo_or_builder
        if sender is not None:
            self.sender = sender
        if sender_or_builder is not None:
            self.sender_or_builder = sender_or_builder
        if unknown_fields is not None:
            self.unknown_fields = unknown_fields

    @property
    def after(self):
        """Gets the after of this PushHookOrBuilder.  # noqa: E501


        :return: The after of this PushHookOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._after

    @after.setter
    def after(self, after):
        """Sets the after of this PushHookOrBuilder.


        :param after: The after of this PushHookOrBuilder.  # noqa: E501
        :type: str
        """

        self._after = after

    @property
    def after_bytes(self):
        """Gets the after_bytes of this PushHookOrBuilder.  # noqa: E501


        :return: The after_bytes of this PushHookOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._after_bytes

    @after_bytes.setter
    def after_bytes(self, after_bytes):
        """Sets the after_bytes of this PushHookOrBuilder.


        :param after_bytes: The after_bytes of this PushHookOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._after_bytes = after_bytes

    @property
    def all_fields(self):
        """Gets the all_fields of this PushHookOrBuilder.  # noqa: E501


        :return: The all_fields of this PushHookOrBuilder.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._all_fields

    @all_fields.setter
    def all_fields(self, all_fields):
        """Sets the all_fields of this PushHookOrBuilder.


        :param all_fields: The all_fields of this PushHookOrBuilder.  # noqa: E501
        :type: dict(str, object)
        """

        self._all_fields = all_fields

    @property
    def base_ref(self):
        """Gets the base_ref of this PushHookOrBuilder.  # noqa: E501


        :return: The base_ref of this PushHookOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._base_ref

    @base_ref.setter
    def base_ref(self, base_ref):
        """Sets the base_ref of this PushHookOrBuilder.


        :param base_ref: The base_ref of this PushHookOrBuilder.  # noqa: E501
        :type: str
        """

        self._base_ref = base_ref

    @property
    def base_ref_bytes(self):
        """Gets the base_ref_bytes of this PushHookOrBuilder.  # noqa: E501


        :return: The base_ref_bytes of this PushHookOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._base_ref_bytes

    @base_ref_bytes.setter
    def base_ref_bytes(self, base_ref_bytes):
        """Sets the base_ref_bytes of this PushHookOrBuilder.


        :param base_ref_bytes: The base_ref_bytes of this PushHookOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._base_ref_bytes = base_ref_bytes

    @property
    def before(self):
        """Gets the before of this PushHookOrBuilder.  # noqa: E501


        :return: The before of this PushHookOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._before

    @before.setter
    def before(self, before):
        """Sets the before of this PushHookOrBuilder.


        :param before: The before of this PushHookOrBuilder.  # noqa: E501
        :type: str
        """

        self._before = before

    @property
    def before_bytes(self):
        """Gets the before_bytes of this PushHookOrBuilder.  # noqa: E501


        :return: The before_bytes of this PushHookOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._before_bytes

    @before_bytes.setter
    def before_bytes(self, before_bytes):
        """Sets the before_bytes of this PushHookOrBuilder.


        :param before_bytes: The before_bytes of this PushHookOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._before_bytes = before_bytes

    @property
    def commit(self):
        """Gets the commit of this PushHookOrBuilder.  # noqa: E501


        :return: The commit of this PushHookOrBuilder.  # noqa: E501
        :rtype: Commit
        """
        return self._commit

    @commit.setter
    def commit(self, commit):
        """Sets the commit of this PushHookOrBuilder.


        :param commit: The commit of this PushHookOrBuilder.  # noqa: E501
        :type: Commit
        """

        self._commit = commit

    @property
    def commit_or_builder(self):
        """Gets the commit_or_builder of this PushHookOrBuilder.  # noqa: E501


        :return: The commit_or_builder of this PushHookOrBuilder.  # noqa: E501
        :rtype: CommitOrBuilder
        """
        return self._commit_or_builder

    @commit_or_builder.setter
    def commit_or_builder(self, commit_or_builder):
        """Sets the commit_or_builder of this PushHookOrBuilder.


        :param commit_or_builder: The commit_or_builder of this PushHookOrBuilder.  # noqa: E501
        :type: CommitOrBuilder
        """

        self._commit_or_builder = commit_or_builder

    @property
    def commits_count(self):
        """Gets the commits_count of this PushHookOrBuilder.  # noqa: E501


        :return: The commits_count of this PushHookOrBuilder.  # noqa: E501
        :rtype: int
        """
        return self._commits_count

    @commits_count.setter
    def commits_count(self, commits_count):
        """Sets the commits_count of this PushHookOrBuilder.


        :param commits_count: The commits_count of this PushHookOrBuilder.  # noqa: E501
        :type: int
        """

        self._commits_count = commits_count

    @property
    def commits_list(self):
        """Gets the commits_list of this PushHookOrBuilder.  # noqa: E501


        :return: The commits_list of this PushHookOrBuilder.  # noqa: E501
        :rtype: list[Commit]
        """
        return self._commits_list

    @commits_list.setter
    def commits_list(self, commits_list):
        """Sets the commits_list of this PushHookOrBuilder.


        :param commits_list: The commits_list of this PushHookOrBuilder.  # noqa: E501
        :type: list[Commit]
        """

        self._commits_list = commits_list

    @property
    def commits_or_builder_list(self):
        """Gets the commits_or_builder_list of this PushHookOrBuilder.  # noqa: E501


        :return: The commits_or_builder_list of this PushHookOrBuilder.  # noqa: E501
        :rtype: list[CommitOrBuilder]
        """
        return self._commits_or_builder_list

    @commits_or_builder_list.setter
    def commits_or_builder_list(self, commits_or_builder_list):
        """Sets the commits_or_builder_list of this PushHookOrBuilder.


        :param commits_or_builder_list: The commits_or_builder_list of this PushHookOrBuilder.  # noqa: E501
        :type: list[CommitOrBuilder]
        """

        self._commits_or_builder_list = commits_or_builder_list

    @property
    def default_instance_for_type(self):
        """Gets the default_instance_for_type of this PushHookOrBuilder.  # noqa: E501


        :return: The default_instance_for_type of this PushHookOrBuilder.  # noqa: E501
        :rtype: Message
        """
        return self._default_instance_for_type

    @default_instance_for_type.setter
    def default_instance_for_type(self, default_instance_for_type):
        """Sets the default_instance_for_type of this PushHookOrBuilder.


        :param default_instance_for_type: The default_instance_for_type of this PushHookOrBuilder.  # noqa: E501
        :type: Message
        """

        self._default_instance_for_type = default_instance_for_type

    @property
    def descriptor_for_type(self):
        """Gets the descriptor_for_type of this PushHookOrBuilder.  # noqa: E501


        :return: The descriptor_for_type of this PushHookOrBuilder.  # noqa: E501
        :rtype: Descriptor
        """
        return self._descriptor_for_type

    @descriptor_for_type.setter
    def descriptor_for_type(self, descriptor_for_type):
        """Sets the descriptor_for_type of this PushHookOrBuilder.


        :param descriptor_for_type: The descriptor_for_type of this PushHookOrBuilder.  # noqa: E501
        :type: Descriptor
        """

        self._descriptor_for_type = descriptor_for_type

    @property
    def initialization_error_string(self):
        """Gets the initialization_error_string of this PushHookOrBuilder.  # noqa: E501


        :return: The initialization_error_string of this PushHookOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._initialization_error_string

    @initialization_error_string.setter
    def initialization_error_string(self, initialization_error_string):
        """Sets the initialization_error_string of this PushHookOrBuilder.


        :param initialization_error_string: The initialization_error_string of this PushHookOrBuilder.  # noqa: E501
        :type: str
        """

        self._initialization_error_string = initialization_error_string

    @property
    def initialized(self):
        """Gets the initialized of this PushHookOrBuilder.  # noqa: E501


        :return: The initialized of this PushHookOrBuilder.  # noqa: E501
        :rtype: bool
        """
        return self._initialized

    @initialized.setter
    def initialized(self, initialized):
        """Sets the initialized of this PushHookOrBuilder.


        :param initialized: The initialized of this PushHookOrBuilder.  # noqa: E501
        :type: bool
        """

        self._initialized = initialized

    @property
    def ref(self):
        """Gets the ref of this PushHookOrBuilder.  # noqa: E501


        :return: The ref of this PushHookOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """Sets the ref of this PushHookOrBuilder.


        :param ref: The ref of this PushHookOrBuilder.  # noqa: E501
        :type: str
        """

        self._ref = ref

    @property
    def ref_bytes(self):
        """Gets the ref_bytes of this PushHookOrBuilder.  # noqa: E501


        :return: The ref_bytes of this PushHookOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._ref_bytes

    @ref_bytes.setter
    def ref_bytes(self, ref_bytes):
        """Sets the ref_bytes of this PushHookOrBuilder.


        :param ref_bytes: The ref_bytes of this PushHookOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._ref_bytes = ref_bytes

    @property
    def repo(self):
        """Gets the repo of this PushHookOrBuilder.  # noqa: E501


        :return: The repo of this PushHookOrBuilder.  # noqa: E501
        :rtype: Repository
        """
        return self._repo

    @repo.setter
    def repo(self, repo):
        """Sets the repo of this PushHookOrBuilder.


        :param repo: The repo of this PushHookOrBuilder.  # noqa: E501
        :type: Repository
        """

        self._repo = repo

    @property
    def repo_or_builder(self):
        """Gets the repo_or_builder of this PushHookOrBuilder.  # noqa: E501


        :return: The repo_or_builder of this PushHookOrBuilder.  # noqa: E501
        :rtype: RepositoryOrBuilder
        """
        return self._repo_or_builder

    @repo_or_builder.setter
    def repo_or_builder(self, repo_or_builder):
        """Sets the repo_or_builder of this PushHookOrBuilder.


        :param repo_or_builder: The repo_or_builder of this PushHookOrBuilder.  # noqa: E501
        :type: RepositoryOrBuilder
        """

        self._repo_or_builder = repo_or_builder

    @property
    def sender(self):
        """Gets the sender of this PushHookOrBuilder.  # noqa: E501


        :return: The sender of this PushHookOrBuilder.  # noqa: E501
        :rtype: PipelineUser
        """
        return self._sender

    @sender.setter
    def sender(self, sender):
        """Sets the sender of this PushHookOrBuilder.


        :param sender: The sender of this PushHookOrBuilder.  # noqa: E501
        :type: PipelineUser
        """

        self._sender = sender

    @property
    def sender_or_builder(self):
        """Gets the sender_or_builder of this PushHookOrBuilder.  # noqa: E501


        :return: The sender_or_builder of this PushHookOrBuilder.  # noqa: E501
        :rtype: UserOrBuilder
        """
        return self._sender_or_builder

    @sender_or_builder.setter
    def sender_or_builder(self, sender_or_builder):
        """Sets the sender_or_builder of this PushHookOrBuilder.


        :param sender_or_builder: The sender_or_builder of this PushHookOrBuilder.  # noqa: E501
        :type: UserOrBuilder
        """

        self._sender_or_builder = sender_or_builder

    @property
    def unknown_fields(self):
        """Gets the unknown_fields of this PushHookOrBuilder.  # noqa: E501


        :return: The unknown_fields of this PushHookOrBuilder.  # noqa: E501
        :rtype: UnknownFieldSet
        """
        return self._unknown_fields

    @unknown_fields.setter
    def unknown_fields(self, unknown_fields):
        """Sets the unknown_fields of this PushHookOrBuilder.


        :param unknown_fields: The unknown_fields of this PushHookOrBuilder.  # noqa: E501
        :type: UnknownFieldSet
        """

        self._unknown_fields = unknown_fields

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
        if issubclass(PushHookOrBuilder, dict):
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
        if not isinstance(other, PushHookOrBuilder):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
