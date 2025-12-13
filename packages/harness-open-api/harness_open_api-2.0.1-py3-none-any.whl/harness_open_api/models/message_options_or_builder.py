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

class MessageOptionsOrBuilder(object):
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
        'deprecated': 'bool',
        'deprecated_legacy_json_field_conflicts': 'bool',
        'descriptor_for_type': 'Descriptor',
        'features': 'FeatureSet',
        'features_or_builder': 'FeatureSetOrBuilder',
        'initialization_error_string': 'str',
        'initialized': 'bool',
        'map_entry': 'bool',
        'message_set_wire_format': 'bool',
        'no_standard_descriptor_accessor': 'bool',
        'uninterpreted_option_count': 'int',
        'uninterpreted_option_list': 'list[UninterpretedOption]',
        'uninterpreted_option_or_builder_list': 'list[UninterpretedOptionOrBuilder]',
        'unknown_fields': 'UnknownFieldSet'
    }

    attribute_map = {
        'all_fields': 'allFields',
        'default_instance_for_type': 'defaultInstanceForType',
        'deprecated': 'deprecated',
        'deprecated_legacy_json_field_conflicts': 'deprecatedLegacyJsonFieldConflicts',
        'descriptor_for_type': 'descriptorForType',
        'features': 'features',
        'features_or_builder': 'featuresOrBuilder',
        'initialization_error_string': 'initializationErrorString',
        'initialized': 'initialized',
        'map_entry': 'mapEntry',
        'message_set_wire_format': 'messageSetWireFormat',
        'no_standard_descriptor_accessor': 'noStandardDescriptorAccessor',
        'uninterpreted_option_count': 'uninterpretedOptionCount',
        'uninterpreted_option_list': 'uninterpretedOptionList',
        'uninterpreted_option_or_builder_list': 'uninterpretedOptionOrBuilderList',
        'unknown_fields': 'unknownFields'
    }

    def __init__(self, all_fields=None, default_instance_for_type=None, deprecated=None, deprecated_legacy_json_field_conflicts=None, descriptor_for_type=None, features=None, features_or_builder=None, initialization_error_string=None, initialized=None, map_entry=None, message_set_wire_format=None, no_standard_descriptor_accessor=None, uninterpreted_option_count=None, uninterpreted_option_list=None, uninterpreted_option_or_builder_list=None, unknown_fields=None):  # noqa: E501
        """MessageOptionsOrBuilder - a model defined in Swagger"""  # noqa: E501
        self._all_fields = None
        self._default_instance_for_type = None
        self._deprecated = None
        self._deprecated_legacy_json_field_conflicts = None
        self._descriptor_for_type = None
        self._features = None
        self._features_or_builder = None
        self._initialization_error_string = None
        self._initialized = None
        self._map_entry = None
        self._message_set_wire_format = None
        self._no_standard_descriptor_accessor = None
        self._uninterpreted_option_count = None
        self._uninterpreted_option_list = None
        self._uninterpreted_option_or_builder_list = None
        self._unknown_fields = None
        self.discriminator = None
        if all_fields is not None:
            self.all_fields = all_fields
        if default_instance_for_type is not None:
            self.default_instance_for_type = default_instance_for_type
        if deprecated is not None:
            self.deprecated = deprecated
        if deprecated_legacy_json_field_conflicts is not None:
            self.deprecated_legacy_json_field_conflicts = deprecated_legacy_json_field_conflicts
        if descriptor_for_type is not None:
            self.descriptor_for_type = descriptor_for_type
        if features is not None:
            self.features = features
        if features_or_builder is not None:
            self.features_or_builder = features_or_builder
        if initialization_error_string is not None:
            self.initialization_error_string = initialization_error_string
        if initialized is not None:
            self.initialized = initialized
        if map_entry is not None:
            self.map_entry = map_entry
        if message_set_wire_format is not None:
            self.message_set_wire_format = message_set_wire_format
        if no_standard_descriptor_accessor is not None:
            self.no_standard_descriptor_accessor = no_standard_descriptor_accessor
        if uninterpreted_option_count is not None:
            self.uninterpreted_option_count = uninterpreted_option_count
        if uninterpreted_option_list is not None:
            self.uninterpreted_option_list = uninterpreted_option_list
        if uninterpreted_option_or_builder_list is not None:
            self.uninterpreted_option_or_builder_list = uninterpreted_option_or_builder_list
        if unknown_fields is not None:
            self.unknown_fields = unknown_fields

    @property
    def all_fields(self):
        """Gets the all_fields of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The all_fields of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._all_fields

    @all_fields.setter
    def all_fields(self, all_fields):
        """Sets the all_fields of this MessageOptionsOrBuilder.


        :param all_fields: The all_fields of this MessageOptionsOrBuilder.  # noqa: E501
        :type: dict(str, object)
        """

        self._all_fields = all_fields

    @property
    def default_instance_for_type(self):
        """Gets the default_instance_for_type of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The default_instance_for_type of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: Message
        """
        return self._default_instance_for_type

    @default_instance_for_type.setter
    def default_instance_for_type(self, default_instance_for_type):
        """Sets the default_instance_for_type of this MessageOptionsOrBuilder.


        :param default_instance_for_type: The default_instance_for_type of this MessageOptionsOrBuilder.  # noqa: E501
        :type: Message
        """

        self._default_instance_for_type = default_instance_for_type

    @property
    def deprecated(self):
        """Gets the deprecated of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The deprecated of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: bool
        """
        return self._deprecated

    @deprecated.setter
    def deprecated(self, deprecated):
        """Sets the deprecated of this MessageOptionsOrBuilder.


        :param deprecated: The deprecated of this MessageOptionsOrBuilder.  # noqa: E501
        :type: bool
        """

        self._deprecated = deprecated

    @property
    def deprecated_legacy_json_field_conflicts(self):
        """Gets the deprecated_legacy_json_field_conflicts of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The deprecated_legacy_json_field_conflicts of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: bool
        """
        return self._deprecated_legacy_json_field_conflicts

    @deprecated_legacy_json_field_conflicts.setter
    def deprecated_legacy_json_field_conflicts(self, deprecated_legacy_json_field_conflicts):
        """Sets the deprecated_legacy_json_field_conflicts of this MessageOptionsOrBuilder.


        :param deprecated_legacy_json_field_conflicts: The deprecated_legacy_json_field_conflicts of this MessageOptionsOrBuilder.  # noqa: E501
        :type: bool
        """

        self._deprecated_legacy_json_field_conflicts = deprecated_legacy_json_field_conflicts

    @property
    def descriptor_for_type(self):
        """Gets the descriptor_for_type of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The descriptor_for_type of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: Descriptor
        """
        return self._descriptor_for_type

    @descriptor_for_type.setter
    def descriptor_for_type(self, descriptor_for_type):
        """Sets the descriptor_for_type of this MessageOptionsOrBuilder.


        :param descriptor_for_type: The descriptor_for_type of this MessageOptionsOrBuilder.  # noqa: E501
        :type: Descriptor
        """

        self._descriptor_for_type = descriptor_for_type

    @property
    def features(self):
        """Gets the features of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The features of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: FeatureSet
        """
        return self._features

    @features.setter
    def features(self, features):
        """Sets the features of this MessageOptionsOrBuilder.


        :param features: The features of this MessageOptionsOrBuilder.  # noqa: E501
        :type: FeatureSet
        """

        self._features = features

    @property
    def features_or_builder(self):
        """Gets the features_or_builder of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The features_or_builder of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: FeatureSetOrBuilder
        """
        return self._features_or_builder

    @features_or_builder.setter
    def features_or_builder(self, features_or_builder):
        """Sets the features_or_builder of this MessageOptionsOrBuilder.


        :param features_or_builder: The features_or_builder of this MessageOptionsOrBuilder.  # noqa: E501
        :type: FeatureSetOrBuilder
        """

        self._features_or_builder = features_or_builder

    @property
    def initialization_error_string(self):
        """Gets the initialization_error_string of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The initialization_error_string of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._initialization_error_string

    @initialization_error_string.setter
    def initialization_error_string(self, initialization_error_string):
        """Sets the initialization_error_string of this MessageOptionsOrBuilder.


        :param initialization_error_string: The initialization_error_string of this MessageOptionsOrBuilder.  # noqa: E501
        :type: str
        """

        self._initialization_error_string = initialization_error_string

    @property
    def initialized(self):
        """Gets the initialized of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The initialized of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: bool
        """
        return self._initialized

    @initialized.setter
    def initialized(self, initialized):
        """Sets the initialized of this MessageOptionsOrBuilder.


        :param initialized: The initialized of this MessageOptionsOrBuilder.  # noqa: E501
        :type: bool
        """

        self._initialized = initialized

    @property
    def map_entry(self):
        """Gets the map_entry of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The map_entry of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: bool
        """
        return self._map_entry

    @map_entry.setter
    def map_entry(self, map_entry):
        """Sets the map_entry of this MessageOptionsOrBuilder.


        :param map_entry: The map_entry of this MessageOptionsOrBuilder.  # noqa: E501
        :type: bool
        """

        self._map_entry = map_entry

    @property
    def message_set_wire_format(self):
        """Gets the message_set_wire_format of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The message_set_wire_format of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: bool
        """
        return self._message_set_wire_format

    @message_set_wire_format.setter
    def message_set_wire_format(self, message_set_wire_format):
        """Sets the message_set_wire_format of this MessageOptionsOrBuilder.


        :param message_set_wire_format: The message_set_wire_format of this MessageOptionsOrBuilder.  # noqa: E501
        :type: bool
        """

        self._message_set_wire_format = message_set_wire_format

    @property
    def no_standard_descriptor_accessor(self):
        """Gets the no_standard_descriptor_accessor of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The no_standard_descriptor_accessor of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: bool
        """
        return self._no_standard_descriptor_accessor

    @no_standard_descriptor_accessor.setter
    def no_standard_descriptor_accessor(self, no_standard_descriptor_accessor):
        """Sets the no_standard_descriptor_accessor of this MessageOptionsOrBuilder.


        :param no_standard_descriptor_accessor: The no_standard_descriptor_accessor of this MessageOptionsOrBuilder.  # noqa: E501
        :type: bool
        """

        self._no_standard_descriptor_accessor = no_standard_descriptor_accessor

    @property
    def uninterpreted_option_count(self):
        """Gets the uninterpreted_option_count of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The uninterpreted_option_count of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: int
        """
        return self._uninterpreted_option_count

    @uninterpreted_option_count.setter
    def uninterpreted_option_count(self, uninterpreted_option_count):
        """Sets the uninterpreted_option_count of this MessageOptionsOrBuilder.


        :param uninterpreted_option_count: The uninterpreted_option_count of this MessageOptionsOrBuilder.  # noqa: E501
        :type: int
        """

        self._uninterpreted_option_count = uninterpreted_option_count

    @property
    def uninterpreted_option_list(self):
        """Gets the uninterpreted_option_list of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The uninterpreted_option_list of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: list[UninterpretedOption]
        """
        return self._uninterpreted_option_list

    @uninterpreted_option_list.setter
    def uninterpreted_option_list(self, uninterpreted_option_list):
        """Sets the uninterpreted_option_list of this MessageOptionsOrBuilder.


        :param uninterpreted_option_list: The uninterpreted_option_list of this MessageOptionsOrBuilder.  # noqa: E501
        :type: list[UninterpretedOption]
        """

        self._uninterpreted_option_list = uninterpreted_option_list

    @property
    def uninterpreted_option_or_builder_list(self):
        """Gets the uninterpreted_option_or_builder_list of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The uninterpreted_option_or_builder_list of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: list[UninterpretedOptionOrBuilder]
        """
        return self._uninterpreted_option_or_builder_list

    @uninterpreted_option_or_builder_list.setter
    def uninterpreted_option_or_builder_list(self, uninterpreted_option_or_builder_list):
        """Sets the uninterpreted_option_or_builder_list of this MessageOptionsOrBuilder.


        :param uninterpreted_option_or_builder_list: The uninterpreted_option_or_builder_list of this MessageOptionsOrBuilder.  # noqa: E501
        :type: list[UninterpretedOptionOrBuilder]
        """

        self._uninterpreted_option_or_builder_list = uninterpreted_option_or_builder_list

    @property
    def unknown_fields(self):
        """Gets the unknown_fields of this MessageOptionsOrBuilder.  # noqa: E501


        :return: The unknown_fields of this MessageOptionsOrBuilder.  # noqa: E501
        :rtype: UnknownFieldSet
        """
        return self._unknown_fields

    @unknown_fields.setter
    def unknown_fields(self, unknown_fields):
        """Sets the unknown_fields of this MessageOptionsOrBuilder.


        :param unknown_fields: The unknown_fields of this MessageOptionsOrBuilder.  # noqa: E501
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
        if issubclass(MessageOptionsOrBuilder, dict):
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
        if not isinstance(other, MessageOptionsOrBuilder):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
