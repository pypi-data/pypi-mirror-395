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

class TemplateReferenceSummary(object):
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
        'default_instance_for_type': 'TemplateReferenceSummary',
        'descriptor_for_type': 'Descriptor',
        'git_branch': 'str',
        'git_branch_bytes': 'ByteString',
        'initialization_error_string': 'str',
        'initialized': 'bool',
        'memoized_serialized_size': 'int',
        'parser_for_type': 'ParserTemplateReferenceSummary',
        'serialized_size': 'int',
        'template_ref': 'str',
        'template_ref_bytes': 'ByteString',
        'unknown_fields': 'UnknownFieldSet',
        'version_label': 'str',
        'version_label_bytes': 'ByteString'
    }

    attribute_map = {
        'all_fields': 'allFields',
        'default_instance_for_type': 'defaultInstanceForType',
        'descriptor_for_type': 'descriptorForType',
        'git_branch': 'gitBranch',
        'git_branch_bytes': 'gitBranchBytes',
        'initialization_error_string': 'initializationErrorString',
        'initialized': 'initialized',
        'memoized_serialized_size': 'memoizedSerializedSize',
        'parser_for_type': 'parserForType',
        'serialized_size': 'serializedSize',
        'template_ref': 'templateRef',
        'template_ref_bytes': 'templateRefBytes',
        'unknown_fields': 'unknownFields',
        'version_label': 'versionLabel',
        'version_label_bytes': 'versionLabelBytes'
    }

    def __init__(self, all_fields=None, default_instance_for_type=None, descriptor_for_type=None, git_branch=None, git_branch_bytes=None, initialization_error_string=None, initialized=None, memoized_serialized_size=None, parser_for_type=None, serialized_size=None, template_ref=None, template_ref_bytes=None, unknown_fields=None, version_label=None, version_label_bytes=None):  # noqa: E501
        """TemplateReferenceSummary - a model defined in Swagger"""  # noqa: E501
        self._all_fields = None
        self._default_instance_for_type = None
        self._descriptor_for_type = None
        self._git_branch = None
        self._git_branch_bytes = None
        self._initialization_error_string = None
        self._initialized = None
        self._memoized_serialized_size = None
        self._parser_for_type = None
        self._serialized_size = None
        self._template_ref = None
        self._template_ref_bytes = None
        self._unknown_fields = None
        self._version_label = None
        self._version_label_bytes = None
        self.discriminator = None
        if all_fields is not None:
            self.all_fields = all_fields
        if default_instance_for_type is not None:
            self.default_instance_for_type = default_instance_for_type
        if descriptor_for_type is not None:
            self.descriptor_for_type = descriptor_for_type
        if git_branch is not None:
            self.git_branch = git_branch
        if git_branch_bytes is not None:
            self.git_branch_bytes = git_branch_bytes
        if initialization_error_string is not None:
            self.initialization_error_string = initialization_error_string
        if initialized is not None:
            self.initialized = initialized
        if memoized_serialized_size is not None:
            self.memoized_serialized_size = memoized_serialized_size
        if parser_for_type is not None:
            self.parser_for_type = parser_for_type
        if serialized_size is not None:
            self.serialized_size = serialized_size
        if template_ref is not None:
            self.template_ref = template_ref
        if template_ref_bytes is not None:
            self.template_ref_bytes = template_ref_bytes
        if unknown_fields is not None:
            self.unknown_fields = unknown_fields
        if version_label is not None:
            self.version_label = version_label
        if version_label_bytes is not None:
            self.version_label_bytes = version_label_bytes

    @property
    def all_fields(self):
        """Gets the all_fields of this TemplateReferenceSummary.  # noqa: E501


        :return: The all_fields of this TemplateReferenceSummary.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._all_fields

    @all_fields.setter
    def all_fields(self, all_fields):
        """Sets the all_fields of this TemplateReferenceSummary.


        :param all_fields: The all_fields of this TemplateReferenceSummary.  # noqa: E501
        :type: dict(str, object)
        """

        self._all_fields = all_fields

    @property
    def default_instance_for_type(self):
        """Gets the default_instance_for_type of this TemplateReferenceSummary.  # noqa: E501


        :return: The default_instance_for_type of this TemplateReferenceSummary.  # noqa: E501
        :rtype: TemplateReferenceSummary
        """
        return self._default_instance_for_type

    @default_instance_for_type.setter
    def default_instance_for_type(self, default_instance_for_type):
        """Sets the default_instance_for_type of this TemplateReferenceSummary.


        :param default_instance_for_type: The default_instance_for_type of this TemplateReferenceSummary.  # noqa: E501
        :type: TemplateReferenceSummary
        """

        self._default_instance_for_type = default_instance_for_type

    @property
    def descriptor_for_type(self):
        """Gets the descriptor_for_type of this TemplateReferenceSummary.  # noqa: E501


        :return: The descriptor_for_type of this TemplateReferenceSummary.  # noqa: E501
        :rtype: Descriptor
        """
        return self._descriptor_for_type

    @descriptor_for_type.setter
    def descriptor_for_type(self, descriptor_for_type):
        """Sets the descriptor_for_type of this TemplateReferenceSummary.


        :param descriptor_for_type: The descriptor_for_type of this TemplateReferenceSummary.  # noqa: E501
        :type: Descriptor
        """

        self._descriptor_for_type = descriptor_for_type

    @property
    def git_branch(self):
        """Gets the git_branch of this TemplateReferenceSummary.  # noqa: E501


        :return: The git_branch of this TemplateReferenceSummary.  # noqa: E501
        :rtype: str
        """
        return self._git_branch

    @git_branch.setter
    def git_branch(self, git_branch):
        """Sets the git_branch of this TemplateReferenceSummary.


        :param git_branch: The git_branch of this TemplateReferenceSummary.  # noqa: E501
        :type: str
        """

        self._git_branch = git_branch

    @property
    def git_branch_bytes(self):
        """Gets the git_branch_bytes of this TemplateReferenceSummary.  # noqa: E501


        :return: The git_branch_bytes of this TemplateReferenceSummary.  # noqa: E501
        :rtype: ByteString
        """
        return self._git_branch_bytes

    @git_branch_bytes.setter
    def git_branch_bytes(self, git_branch_bytes):
        """Sets the git_branch_bytes of this TemplateReferenceSummary.


        :param git_branch_bytes: The git_branch_bytes of this TemplateReferenceSummary.  # noqa: E501
        :type: ByteString
        """

        self._git_branch_bytes = git_branch_bytes

    @property
    def initialization_error_string(self):
        """Gets the initialization_error_string of this TemplateReferenceSummary.  # noqa: E501


        :return: The initialization_error_string of this TemplateReferenceSummary.  # noqa: E501
        :rtype: str
        """
        return self._initialization_error_string

    @initialization_error_string.setter
    def initialization_error_string(self, initialization_error_string):
        """Sets the initialization_error_string of this TemplateReferenceSummary.


        :param initialization_error_string: The initialization_error_string of this TemplateReferenceSummary.  # noqa: E501
        :type: str
        """

        self._initialization_error_string = initialization_error_string

    @property
    def initialized(self):
        """Gets the initialized of this TemplateReferenceSummary.  # noqa: E501


        :return: The initialized of this TemplateReferenceSummary.  # noqa: E501
        :rtype: bool
        """
        return self._initialized

    @initialized.setter
    def initialized(self, initialized):
        """Sets the initialized of this TemplateReferenceSummary.


        :param initialized: The initialized of this TemplateReferenceSummary.  # noqa: E501
        :type: bool
        """

        self._initialized = initialized

    @property
    def memoized_serialized_size(self):
        """Gets the memoized_serialized_size of this TemplateReferenceSummary.  # noqa: E501


        :return: The memoized_serialized_size of this TemplateReferenceSummary.  # noqa: E501
        :rtype: int
        """
        return self._memoized_serialized_size

    @memoized_serialized_size.setter
    def memoized_serialized_size(self, memoized_serialized_size):
        """Sets the memoized_serialized_size of this TemplateReferenceSummary.


        :param memoized_serialized_size: The memoized_serialized_size of this TemplateReferenceSummary.  # noqa: E501
        :type: int
        """

        self._memoized_serialized_size = memoized_serialized_size

    @property
    def parser_for_type(self):
        """Gets the parser_for_type of this TemplateReferenceSummary.  # noqa: E501


        :return: The parser_for_type of this TemplateReferenceSummary.  # noqa: E501
        :rtype: ParserTemplateReferenceSummary
        """
        return self._parser_for_type

    @parser_for_type.setter
    def parser_for_type(self, parser_for_type):
        """Sets the parser_for_type of this TemplateReferenceSummary.


        :param parser_for_type: The parser_for_type of this TemplateReferenceSummary.  # noqa: E501
        :type: ParserTemplateReferenceSummary
        """

        self._parser_for_type = parser_for_type

    @property
    def serialized_size(self):
        """Gets the serialized_size of this TemplateReferenceSummary.  # noqa: E501


        :return: The serialized_size of this TemplateReferenceSummary.  # noqa: E501
        :rtype: int
        """
        return self._serialized_size

    @serialized_size.setter
    def serialized_size(self, serialized_size):
        """Sets the serialized_size of this TemplateReferenceSummary.


        :param serialized_size: The serialized_size of this TemplateReferenceSummary.  # noqa: E501
        :type: int
        """

        self._serialized_size = serialized_size

    @property
    def template_ref(self):
        """Gets the template_ref of this TemplateReferenceSummary.  # noqa: E501


        :return: The template_ref of this TemplateReferenceSummary.  # noqa: E501
        :rtype: str
        """
        return self._template_ref

    @template_ref.setter
    def template_ref(self, template_ref):
        """Sets the template_ref of this TemplateReferenceSummary.


        :param template_ref: The template_ref of this TemplateReferenceSummary.  # noqa: E501
        :type: str
        """

        self._template_ref = template_ref

    @property
    def template_ref_bytes(self):
        """Gets the template_ref_bytes of this TemplateReferenceSummary.  # noqa: E501


        :return: The template_ref_bytes of this TemplateReferenceSummary.  # noqa: E501
        :rtype: ByteString
        """
        return self._template_ref_bytes

    @template_ref_bytes.setter
    def template_ref_bytes(self, template_ref_bytes):
        """Sets the template_ref_bytes of this TemplateReferenceSummary.


        :param template_ref_bytes: The template_ref_bytes of this TemplateReferenceSummary.  # noqa: E501
        :type: ByteString
        """

        self._template_ref_bytes = template_ref_bytes

    @property
    def unknown_fields(self):
        """Gets the unknown_fields of this TemplateReferenceSummary.  # noqa: E501


        :return: The unknown_fields of this TemplateReferenceSummary.  # noqa: E501
        :rtype: UnknownFieldSet
        """
        return self._unknown_fields

    @unknown_fields.setter
    def unknown_fields(self, unknown_fields):
        """Sets the unknown_fields of this TemplateReferenceSummary.


        :param unknown_fields: The unknown_fields of this TemplateReferenceSummary.  # noqa: E501
        :type: UnknownFieldSet
        """

        self._unknown_fields = unknown_fields

    @property
    def version_label(self):
        """Gets the version_label of this TemplateReferenceSummary.  # noqa: E501


        :return: The version_label of this TemplateReferenceSummary.  # noqa: E501
        :rtype: str
        """
        return self._version_label

    @version_label.setter
    def version_label(self, version_label):
        """Sets the version_label of this TemplateReferenceSummary.


        :param version_label: The version_label of this TemplateReferenceSummary.  # noqa: E501
        :type: str
        """

        self._version_label = version_label

    @property
    def version_label_bytes(self):
        """Gets the version_label_bytes of this TemplateReferenceSummary.  # noqa: E501


        :return: The version_label_bytes of this TemplateReferenceSummary.  # noqa: E501
        :rtype: ByteString
        """
        return self._version_label_bytes

    @version_label_bytes.setter
    def version_label_bytes(self, version_label_bytes):
        """Sets the version_label_bytes of this TemplateReferenceSummary.


        :param version_label_bytes: The version_label_bytes of this TemplateReferenceSummary.  # noqa: E501
        :type: ByteString
        """

        self._version_label_bytes = version_label_bytes

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
        if issubclass(TemplateReferenceSummary, dict):
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
        if not isinstance(other, TemplateReferenceSummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
