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

class FeatureSupportOrBuilder(object):
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
        'default_instance_for_type': 'Message',
        'deprecation_warning': 'str',
        'deprecation_warning_bytes': 'ByteString',
        'descriptor_for_type': 'Descriptor',
        'edition_deprecated': 'str',
        'edition_introduced': 'str',
        'edition_removed': 'str',
        'initialization_error_string': 'str',
        'initialized': 'bool',
        'unknown_fields': 'UnknownFieldSet'
    }

    attribute_map = {
        'all_fields': 'allFields',
        'default_instance_for_type': 'defaultInstanceForType',
        'deprecation_warning': 'deprecationWarning',
        'deprecation_warning_bytes': 'deprecationWarningBytes',
        'descriptor_for_type': 'descriptorForType',
        'edition_deprecated': 'editionDeprecated',
        'edition_introduced': 'editionIntroduced',
        'edition_removed': 'editionRemoved',
        'initialization_error_string': 'initializationErrorString',
        'initialized': 'initialized',
        'unknown_fields': 'unknownFields'
    }

    def __init__(self, all_fields=None, default_instance_for_type=None, deprecation_warning=None, deprecation_warning_bytes=None, descriptor_for_type=None, edition_deprecated=None, edition_introduced=None, edition_removed=None, initialization_error_string=None, initialized=None, unknown_fields=None):  # noqa: E501
        """FeatureSupportOrBuilder - a model defined in Swagger"""  # noqa: E501
        self._all_fields = None
        self._default_instance_for_type = None
        self._deprecation_warning = None
        self._deprecation_warning_bytes = None
        self._descriptor_for_type = None
        self._edition_deprecated = None
        self._edition_introduced = None
        self._edition_removed = None
        self._initialization_error_string = None
        self._initialized = None
        self._unknown_fields = None
        self.discriminator = None
        if all_fields is not None:
            self.all_fields = all_fields
        if default_instance_for_type is not None:
            self.default_instance_for_type = default_instance_for_type
        if deprecation_warning is not None:
            self.deprecation_warning = deprecation_warning
        if deprecation_warning_bytes is not None:
            self.deprecation_warning_bytes = deprecation_warning_bytes
        if descriptor_for_type is not None:
            self.descriptor_for_type = descriptor_for_type
        if edition_deprecated is not None:
            self.edition_deprecated = edition_deprecated
        if edition_introduced is not None:
            self.edition_introduced = edition_introduced
        if edition_removed is not None:
            self.edition_removed = edition_removed
        if initialization_error_string is not None:
            self.initialization_error_string = initialization_error_string
        if initialized is not None:
            self.initialized = initialized
        if unknown_fields is not None:
            self.unknown_fields = unknown_fields

    @property
    def all_fields(self):
        """Gets the all_fields of this FeatureSupportOrBuilder.  # noqa: E501


        :return: The all_fields of this FeatureSupportOrBuilder.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._all_fields

    @all_fields.setter
    def all_fields(self, all_fields):
        """Sets the all_fields of this FeatureSupportOrBuilder.


        :param all_fields: The all_fields of this FeatureSupportOrBuilder.  # noqa: E501
        :type: dict(str, object)
        """

        self._all_fields = all_fields

    @property
    def default_instance_for_type(self):
        """Gets the default_instance_for_type of this FeatureSupportOrBuilder.  # noqa: E501


        :return: The default_instance_for_type of this FeatureSupportOrBuilder.  # noqa: E501
        :rtype: Message
        """
        return self._default_instance_for_type

    @default_instance_for_type.setter
    def default_instance_for_type(self, default_instance_for_type):
        """Sets the default_instance_for_type of this FeatureSupportOrBuilder.


        :param default_instance_for_type: The default_instance_for_type of this FeatureSupportOrBuilder.  # noqa: E501
        :type: Message
        """

        self._default_instance_for_type = default_instance_for_type

    @property
    def deprecation_warning(self):
        """Gets the deprecation_warning of this FeatureSupportOrBuilder.  # noqa: E501


        :return: The deprecation_warning of this FeatureSupportOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._deprecation_warning

    @deprecation_warning.setter
    def deprecation_warning(self, deprecation_warning):
        """Sets the deprecation_warning of this FeatureSupportOrBuilder.


        :param deprecation_warning: The deprecation_warning of this FeatureSupportOrBuilder.  # noqa: E501
        :type: str
        """

        self._deprecation_warning = deprecation_warning

    @property
    def deprecation_warning_bytes(self):
        """Gets the deprecation_warning_bytes of this FeatureSupportOrBuilder.  # noqa: E501


        :return: The deprecation_warning_bytes of this FeatureSupportOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._deprecation_warning_bytes

    @deprecation_warning_bytes.setter
    def deprecation_warning_bytes(self, deprecation_warning_bytes):
        """Sets the deprecation_warning_bytes of this FeatureSupportOrBuilder.


        :param deprecation_warning_bytes: The deprecation_warning_bytes of this FeatureSupportOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._deprecation_warning_bytes = deprecation_warning_bytes

    @property
    def descriptor_for_type(self):
        """Gets the descriptor_for_type of this FeatureSupportOrBuilder.  # noqa: E501


        :return: The descriptor_for_type of this FeatureSupportOrBuilder.  # noqa: E501
        :rtype: Descriptor
        """
        return self._descriptor_for_type

    @descriptor_for_type.setter
    def descriptor_for_type(self, descriptor_for_type):
        """Sets the descriptor_for_type of this FeatureSupportOrBuilder.


        :param descriptor_for_type: The descriptor_for_type of this FeatureSupportOrBuilder.  # noqa: E501
        :type: Descriptor
        """

        self._descriptor_for_type = descriptor_for_type

    @property
    def edition_deprecated(self):
        """Gets the edition_deprecated of this FeatureSupportOrBuilder.  # noqa: E501


        :return: The edition_deprecated of this FeatureSupportOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._edition_deprecated

    @edition_deprecated.setter
    def edition_deprecated(self, edition_deprecated):
        """Sets the edition_deprecated of this FeatureSupportOrBuilder.


        :param edition_deprecated: The edition_deprecated of this FeatureSupportOrBuilder.  # noqa: E501
        :type: str
        """
        allowed_values = ["EDITION_UNKNOWN", "EDITION_LEGACY", "EDITION_PROTO2", "EDITION_PROTO3", "EDITION_2023", "EDITION_2024", "EDITION_1_TEST_ONLY", "EDITION_2_TEST_ONLY", "EDITION_99997_TEST_ONLY", "EDITION_99998_TEST_ONLY", "EDITION_99999_TEST_ONLY", "EDITION_MAX"]  # noqa: E501
        if edition_deprecated not in allowed_values:
            raise ValueError(
                "Invalid value for `edition_deprecated` ({0}), must be one of {1}"  # noqa: E501
                .format(edition_deprecated, allowed_values)
            )

        self._edition_deprecated = edition_deprecated

    @property
    def edition_introduced(self):
        """Gets the edition_introduced of this FeatureSupportOrBuilder.  # noqa: E501


        :return: The edition_introduced of this FeatureSupportOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._edition_introduced

    @edition_introduced.setter
    def edition_introduced(self, edition_introduced):
        """Sets the edition_introduced of this FeatureSupportOrBuilder.


        :param edition_introduced: The edition_introduced of this FeatureSupportOrBuilder.  # noqa: E501
        :type: str
        """
        allowed_values = ["EDITION_UNKNOWN", "EDITION_LEGACY", "EDITION_PROTO2", "EDITION_PROTO3", "EDITION_2023", "EDITION_2024", "EDITION_1_TEST_ONLY", "EDITION_2_TEST_ONLY", "EDITION_99997_TEST_ONLY", "EDITION_99998_TEST_ONLY", "EDITION_99999_TEST_ONLY", "EDITION_MAX"]  # noqa: E501
        if edition_introduced not in allowed_values:
            raise ValueError(
                "Invalid value for `edition_introduced` ({0}), must be one of {1}"  # noqa: E501
                .format(edition_introduced, allowed_values)
            )

        self._edition_introduced = edition_introduced

    @property
    def edition_removed(self):
        """Gets the edition_removed of this FeatureSupportOrBuilder.  # noqa: E501


        :return: The edition_removed of this FeatureSupportOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._edition_removed

    @edition_removed.setter
    def edition_removed(self, edition_removed):
        """Sets the edition_removed of this FeatureSupportOrBuilder.


        :param edition_removed: The edition_removed of this FeatureSupportOrBuilder.  # noqa: E501
        :type: str
        """
        allowed_values = ["EDITION_UNKNOWN", "EDITION_LEGACY", "EDITION_PROTO2", "EDITION_PROTO3", "EDITION_2023", "EDITION_2024", "EDITION_1_TEST_ONLY", "EDITION_2_TEST_ONLY", "EDITION_99997_TEST_ONLY", "EDITION_99998_TEST_ONLY", "EDITION_99999_TEST_ONLY", "EDITION_MAX"]  # noqa: E501
        if edition_removed not in allowed_values:
            raise ValueError(
                "Invalid value for `edition_removed` ({0}), must be one of {1}"  # noqa: E501
                .format(edition_removed, allowed_values)
            )

        self._edition_removed = edition_removed

    @property
    def initialization_error_string(self):
        """Gets the initialization_error_string of this FeatureSupportOrBuilder.  # noqa: E501


        :return: The initialization_error_string of this FeatureSupportOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._initialization_error_string

    @initialization_error_string.setter
    def initialization_error_string(self, initialization_error_string):
        """Sets the initialization_error_string of this FeatureSupportOrBuilder.


        :param initialization_error_string: The initialization_error_string of this FeatureSupportOrBuilder.  # noqa: E501
        :type: str
        """

        self._initialization_error_string = initialization_error_string

    @property
    def initialized(self):
        """Gets the initialized of this FeatureSupportOrBuilder.  # noqa: E501


        :return: The initialized of this FeatureSupportOrBuilder.  # noqa: E501
        :rtype: bool
        """
        return self._initialized

    @initialized.setter
    def initialized(self, initialized):
        """Sets the initialized of this FeatureSupportOrBuilder.


        :param initialized: The initialized of this FeatureSupportOrBuilder.  # noqa: E501
        :type: bool
        """

        self._initialized = initialized

    @property
    def unknown_fields(self):
        """Gets the unknown_fields of this FeatureSupportOrBuilder.  # noqa: E501


        :return: The unknown_fields of this FeatureSupportOrBuilder.  # noqa: E501
        :rtype: UnknownFieldSet
        """
        return self._unknown_fields

    @unknown_fields.setter
    def unknown_fields(self, unknown_fields):
        """Sets the unknown_fields of this FeatureSupportOrBuilder.


        :param unknown_fields: The unknown_fields of this FeatureSupportOrBuilder.  # noqa: E501
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
        if issubclass(FeatureSupportOrBuilder, dict):
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
        if not isinstance(other, FeatureSupportOrBuilder):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
