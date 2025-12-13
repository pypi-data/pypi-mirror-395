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

class Commit(object):
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
        'author': 'Signature',
        'author_or_builder': 'SignatureOrBuilder',
        'committer': 'Signature',
        'committer_or_builder': 'SignatureOrBuilder',
        'default_instance_for_type': 'Commit',
        'descriptor_for_type': 'Descriptor',
        'initialization_error_string': 'str',
        'initialized': 'bool',
        'link': 'str',
        'link_bytes': 'ByteString',
        'memoized_serialized_size': 'int',
        'message': 'str',
        'message_bytes': 'ByteString',
        'parser_for_type': 'ParserCommit',
        'serialized_size': 'int',
        'sha': 'str',
        'sha_bytes': 'ByteString',
        'unknown_fields': 'UnknownFieldSet'
    }

    attribute_map = {
        'all_fields': 'allFields',
        'author': 'author',
        'author_or_builder': 'authorOrBuilder',
        'committer': 'committer',
        'committer_or_builder': 'committerOrBuilder',
        'default_instance_for_type': 'defaultInstanceForType',
        'descriptor_for_type': 'descriptorForType',
        'initialization_error_string': 'initializationErrorString',
        'initialized': 'initialized',
        'link': 'link',
        'link_bytes': 'linkBytes',
        'memoized_serialized_size': 'memoizedSerializedSize',
        'message': 'message',
        'message_bytes': 'messageBytes',
        'parser_for_type': 'parserForType',
        'serialized_size': 'serializedSize',
        'sha': 'sha',
        'sha_bytes': 'shaBytes',
        'unknown_fields': 'unknownFields'
    }

    def __init__(self, all_fields=None, author=None, author_or_builder=None, committer=None, committer_or_builder=None, default_instance_for_type=None, descriptor_for_type=None, initialization_error_string=None, initialized=None, link=None, link_bytes=None, memoized_serialized_size=None, message=None, message_bytes=None, parser_for_type=None, serialized_size=None, sha=None, sha_bytes=None, unknown_fields=None):  # noqa: E501
        """Commit - a model defined in Swagger"""  # noqa: E501
        self._all_fields = None
        self._author = None
        self._author_or_builder = None
        self._committer = None
        self._committer_or_builder = None
        self._default_instance_for_type = None
        self._descriptor_for_type = None
        self._initialization_error_string = None
        self._initialized = None
        self._link = None
        self._link_bytes = None
        self._memoized_serialized_size = None
        self._message = None
        self._message_bytes = None
        self._parser_for_type = None
        self._serialized_size = None
        self._sha = None
        self._sha_bytes = None
        self._unknown_fields = None
        self.discriminator = None
        if all_fields is not None:
            self.all_fields = all_fields
        if author is not None:
            self.author = author
        if author_or_builder is not None:
            self.author_or_builder = author_or_builder
        if committer is not None:
            self.committer = committer
        if committer_or_builder is not None:
            self.committer_or_builder = committer_or_builder
        if default_instance_for_type is not None:
            self.default_instance_for_type = default_instance_for_type
        if descriptor_for_type is not None:
            self.descriptor_for_type = descriptor_for_type
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
        if message is not None:
            self.message = message
        if message_bytes is not None:
            self.message_bytes = message_bytes
        if parser_for_type is not None:
            self.parser_for_type = parser_for_type
        if serialized_size is not None:
            self.serialized_size = serialized_size
        if sha is not None:
            self.sha = sha
        if sha_bytes is not None:
            self.sha_bytes = sha_bytes
        if unknown_fields is not None:
            self.unknown_fields = unknown_fields

    @property
    def all_fields(self):
        """Gets the all_fields of this Commit.  # noqa: E501


        :return: The all_fields of this Commit.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._all_fields

    @all_fields.setter
    def all_fields(self, all_fields):
        """Sets the all_fields of this Commit.


        :param all_fields: The all_fields of this Commit.  # noqa: E501
        :type: dict(str, object)
        """

        self._all_fields = all_fields

    @property
    def author(self):
        """Gets the author of this Commit.  # noqa: E501


        :return: The author of this Commit.  # noqa: E501
        :rtype: Signature
        """
        return self._author

    @author.setter
    def author(self, author):
        """Sets the author of this Commit.


        :param author: The author of this Commit.  # noqa: E501
        :type: Signature
        """

        self._author = author

    @property
    def author_or_builder(self):
        """Gets the author_or_builder of this Commit.  # noqa: E501


        :return: The author_or_builder of this Commit.  # noqa: E501
        :rtype: SignatureOrBuilder
        """
        return self._author_or_builder

    @author_or_builder.setter
    def author_or_builder(self, author_or_builder):
        """Sets the author_or_builder of this Commit.


        :param author_or_builder: The author_or_builder of this Commit.  # noqa: E501
        :type: SignatureOrBuilder
        """

        self._author_or_builder = author_or_builder

    @property
    def committer(self):
        """Gets the committer of this Commit.  # noqa: E501


        :return: The committer of this Commit.  # noqa: E501
        :rtype: Signature
        """
        return self._committer

    @committer.setter
    def committer(self, committer):
        """Sets the committer of this Commit.


        :param committer: The committer of this Commit.  # noqa: E501
        :type: Signature
        """

        self._committer = committer

    @property
    def committer_or_builder(self):
        """Gets the committer_or_builder of this Commit.  # noqa: E501


        :return: The committer_or_builder of this Commit.  # noqa: E501
        :rtype: SignatureOrBuilder
        """
        return self._committer_or_builder

    @committer_or_builder.setter
    def committer_or_builder(self, committer_or_builder):
        """Sets the committer_or_builder of this Commit.


        :param committer_or_builder: The committer_or_builder of this Commit.  # noqa: E501
        :type: SignatureOrBuilder
        """

        self._committer_or_builder = committer_or_builder

    @property
    def default_instance_for_type(self):
        """Gets the default_instance_for_type of this Commit.  # noqa: E501


        :return: The default_instance_for_type of this Commit.  # noqa: E501
        :rtype: Commit
        """
        return self._default_instance_for_type

    @default_instance_for_type.setter
    def default_instance_for_type(self, default_instance_for_type):
        """Sets the default_instance_for_type of this Commit.


        :param default_instance_for_type: The default_instance_for_type of this Commit.  # noqa: E501
        :type: Commit
        """

        self._default_instance_for_type = default_instance_for_type

    @property
    def descriptor_for_type(self):
        """Gets the descriptor_for_type of this Commit.  # noqa: E501


        :return: The descriptor_for_type of this Commit.  # noqa: E501
        :rtype: Descriptor
        """
        return self._descriptor_for_type

    @descriptor_for_type.setter
    def descriptor_for_type(self, descriptor_for_type):
        """Sets the descriptor_for_type of this Commit.


        :param descriptor_for_type: The descriptor_for_type of this Commit.  # noqa: E501
        :type: Descriptor
        """

        self._descriptor_for_type = descriptor_for_type

    @property
    def initialization_error_string(self):
        """Gets the initialization_error_string of this Commit.  # noqa: E501


        :return: The initialization_error_string of this Commit.  # noqa: E501
        :rtype: str
        """
        return self._initialization_error_string

    @initialization_error_string.setter
    def initialization_error_string(self, initialization_error_string):
        """Sets the initialization_error_string of this Commit.


        :param initialization_error_string: The initialization_error_string of this Commit.  # noqa: E501
        :type: str
        """

        self._initialization_error_string = initialization_error_string

    @property
    def initialized(self):
        """Gets the initialized of this Commit.  # noqa: E501


        :return: The initialized of this Commit.  # noqa: E501
        :rtype: bool
        """
        return self._initialized

    @initialized.setter
    def initialized(self, initialized):
        """Sets the initialized of this Commit.


        :param initialized: The initialized of this Commit.  # noqa: E501
        :type: bool
        """

        self._initialized = initialized

    @property
    def link(self):
        """Gets the link of this Commit.  # noqa: E501


        :return: The link of this Commit.  # noqa: E501
        :rtype: str
        """
        return self._link

    @link.setter
    def link(self, link):
        """Sets the link of this Commit.


        :param link: The link of this Commit.  # noqa: E501
        :type: str
        """

        self._link = link

    @property
    def link_bytes(self):
        """Gets the link_bytes of this Commit.  # noqa: E501


        :return: The link_bytes of this Commit.  # noqa: E501
        :rtype: ByteString
        """
        return self._link_bytes

    @link_bytes.setter
    def link_bytes(self, link_bytes):
        """Sets the link_bytes of this Commit.


        :param link_bytes: The link_bytes of this Commit.  # noqa: E501
        :type: ByteString
        """

        self._link_bytes = link_bytes

    @property
    def memoized_serialized_size(self):
        """Gets the memoized_serialized_size of this Commit.  # noqa: E501


        :return: The memoized_serialized_size of this Commit.  # noqa: E501
        :rtype: int
        """
        return self._memoized_serialized_size

    @memoized_serialized_size.setter
    def memoized_serialized_size(self, memoized_serialized_size):
        """Sets the memoized_serialized_size of this Commit.


        :param memoized_serialized_size: The memoized_serialized_size of this Commit.  # noqa: E501
        :type: int
        """

        self._memoized_serialized_size = memoized_serialized_size

    @property
    def message(self):
        """Gets the message of this Commit.  # noqa: E501


        :return: The message of this Commit.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this Commit.


        :param message: The message of this Commit.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def message_bytes(self):
        """Gets the message_bytes of this Commit.  # noqa: E501


        :return: The message_bytes of this Commit.  # noqa: E501
        :rtype: ByteString
        """
        return self._message_bytes

    @message_bytes.setter
    def message_bytes(self, message_bytes):
        """Sets the message_bytes of this Commit.


        :param message_bytes: The message_bytes of this Commit.  # noqa: E501
        :type: ByteString
        """

        self._message_bytes = message_bytes

    @property
    def parser_for_type(self):
        """Gets the parser_for_type of this Commit.  # noqa: E501


        :return: The parser_for_type of this Commit.  # noqa: E501
        :rtype: ParserCommit
        """
        return self._parser_for_type

    @parser_for_type.setter
    def parser_for_type(self, parser_for_type):
        """Sets the parser_for_type of this Commit.


        :param parser_for_type: The parser_for_type of this Commit.  # noqa: E501
        :type: ParserCommit
        """

        self._parser_for_type = parser_for_type

    @property
    def serialized_size(self):
        """Gets the serialized_size of this Commit.  # noqa: E501


        :return: The serialized_size of this Commit.  # noqa: E501
        :rtype: int
        """
        return self._serialized_size

    @serialized_size.setter
    def serialized_size(self, serialized_size):
        """Sets the serialized_size of this Commit.


        :param serialized_size: The serialized_size of this Commit.  # noqa: E501
        :type: int
        """

        self._serialized_size = serialized_size

    @property
    def sha(self):
        """Gets the sha of this Commit.  # noqa: E501


        :return: The sha of this Commit.  # noqa: E501
        :rtype: str
        """
        return self._sha

    @sha.setter
    def sha(self, sha):
        """Sets the sha of this Commit.


        :param sha: The sha of this Commit.  # noqa: E501
        :type: str
        """

        self._sha = sha

    @property
    def sha_bytes(self):
        """Gets the sha_bytes of this Commit.  # noqa: E501


        :return: The sha_bytes of this Commit.  # noqa: E501
        :rtype: ByteString
        """
        return self._sha_bytes

    @sha_bytes.setter
    def sha_bytes(self, sha_bytes):
        """Sets the sha_bytes of this Commit.


        :param sha_bytes: The sha_bytes of this Commit.  # noqa: E501
        :type: ByteString
        """

        self._sha_bytes = sha_bytes

    @property
    def unknown_fields(self):
        """Gets the unknown_fields of this Commit.  # noqa: E501


        :return: The unknown_fields of this Commit.  # noqa: E501
        :rtype: UnknownFieldSet
        """
        return self._unknown_fields

    @unknown_fields.setter
    def unknown_fields(self, unknown_fields):
        """Sets the unknown_fields of this Commit.


        :param unknown_fields: The unknown_fields of this Commit.  # noqa: E501
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
        if issubclass(Commit, dict):
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
        if not isinstance(other, Commit):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
