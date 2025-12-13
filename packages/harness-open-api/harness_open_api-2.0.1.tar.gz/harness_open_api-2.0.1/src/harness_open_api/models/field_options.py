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

class FieldOptions(object):
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
        'all_fields_raw': 'dict(str, object)',
        'ctype': 'str',
        'debug_redact': 'bool',
        'default_instance_for_type': 'FieldOptions',
        'deprecated': 'bool',
        'descriptor_for_type': 'Descriptor',
        'edition_defaults_count': 'int',
        'edition_defaults_list': 'list[EditionDefault]',
        'edition_defaults_or_builder_list': 'list[EditionDefaultOrBuilder]',
        'feature_support': 'FeatureSupport',
        'feature_support_or_builder': 'FeatureSupportOrBuilder',
        'features': 'FeatureSet',
        'features_or_builder': 'FeatureSetOrBuilder',
        'initialization_error_string': 'str',
        'initialized': 'bool',
        'jstype': 'str',
        'lazy': 'bool',
        'memoized_serialized_size': 'int',
        'packed': 'bool',
        'parser_for_type': 'ParserFieldOptions',
        'retention': 'str',
        'serialized_size': 'int',
        'targets_count': 'int',
        'targets_list': 'list[str]',
        'uninterpreted_option_count': 'int',
        'uninterpreted_option_list': 'list[UninterpretedOption]',
        'uninterpreted_option_or_builder_list': 'list[UninterpretedOptionOrBuilder]',
        'unknown_fields': 'UnknownFieldSet',
        'unverified_lazy': 'bool',
        'weak': 'bool'
    }

    attribute_map = {
        'all_fields': 'allFields',
        'all_fields_raw': 'allFieldsRaw',
        'ctype': 'ctype',
        'debug_redact': 'debugRedact',
        'default_instance_for_type': 'defaultInstanceForType',
        'deprecated': 'deprecated',
        'descriptor_for_type': 'descriptorForType',
        'edition_defaults_count': 'editionDefaultsCount',
        'edition_defaults_list': 'editionDefaultsList',
        'edition_defaults_or_builder_list': 'editionDefaultsOrBuilderList',
        'feature_support': 'featureSupport',
        'feature_support_or_builder': 'featureSupportOrBuilder',
        'features': 'features',
        'features_or_builder': 'featuresOrBuilder',
        'initialization_error_string': 'initializationErrorString',
        'initialized': 'initialized',
        'jstype': 'jstype',
        'lazy': 'lazy',
        'memoized_serialized_size': 'memoizedSerializedSize',
        'packed': 'packed',
        'parser_for_type': 'parserForType',
        'retention': 'retention',
        'serialized_size': 'serializedSize',
        'targets_count': 'targetsCount',
        'targets_list': 'targetsList',
        'uninterpreted_option_count': 'uninterpretedOptionCount',
        'uninterpreted_option_list': 'uninterpretedOptionList',
        'uninterpreted_option_or_builder_list': 'uninterpretedOptionOrBuilderList',
        'unknown_fields': 'unknownFields',
        'unverified_lazy': 'unverifiedLazy',
        'weak': 'weak'
    }

    def __init__(self, all_fields=None, all_fields_raw=None, ctype=None, debug_redact=None, default_instance_for_type=None, deprecated=None, descriptor_for_type=None, edition_defaults_count=None, edition_defaults_list=None, edition_defaults_or_builder_list=None, feature_support=None, feature_support_or_builder=None, features=None, features_or_builder=None, initialization_error_string=None, initialized=None, jstype=None, lazy=None, memoized_serialized_size=None, packed=None, parser_for_type=None, retention=None, serialized_size=None, targets_count=None, targets_list=None, uninterpreted_option_count=None, uninterpreted_option_list=None, uninterpreted_option_or_builder_list=None, unknown_fields=None, unverified_lazy=None, weak=None):  # noqa: E501
        """FieldOptions - a model defined in Swagger"""  # noqa: E501
        self._all_fields = None
        self._all_fields_raw = None
        self._ctype = None
        self._debug_redact = None
        self._default_instance_for_type = None
        self._deprecated = None
        self._descriptor_for_type = None
        self._edition_defaults_count = None
        self._edition_defaults_list = None
        self._edition_defaults_or_builder_list = None
        self._feature_support = None
        self._feature_support_or_builder = None
        self._features = None
        self._features_or_builder = None
        self._initialization_error_string = None
        self._initialized = None
        self._jstype = None
        self._lazy = None
        self._memoized_serialized_size = None
        self._packed = None
        self._parser_for_type = None
        self._retention = None
        self._serialized_size = None
        self._targets_count = None
        self._targets_list = None
        self._uninterpreted_option_count = None
        self._uninterpreted_option_list = None
        self._uninterpreted_option_or_builder_list = None
        self._unknown_fields = None
        self._unverified_lazy = None
        self._weak = None
        self.discriminator = None
        if all_fields is not None:
            self.all_fields = all_fields
        if all_fields_raw is not None:
            self.all_fields_raw = all_fields_raw
        if ctype is not None:
            self.ctype = ctype
        if debug_redact is not None:
            self.debug_redact = debug_redact
        if default_instance_for_type is not None:
            self.default_instance_for_type = default_instance_for_type
        if deprecated is not None:
            self.deprecated = deprecated
        if descriptor_for_type is not None:
            self.descriptor_for_type = descriptor_for_type
        if edition_defaults_count is not None:
            self.edition_defaults_count = edition_defaults_count
        if edition_defaults_list is not None:
            self.edition_defaults_list = edition_defaults_list
        if edition_defaults_or_builder_list is not None:
            self.edition_defaults_or_builder_list = edition_defaults_or_builder_list
        if feature_support is not None:
            self.feature_support = feature_support
        if feature_support_or_builder is not None:
            self.feature_support_or_builder = feature_support_or_builder
        if features is not None:
            self.features = features
        if features_or_builder is not None:
            self.features_or_builder = features_or_builder
        if initialization_error_string is not None:
            self.initialization_error_string = initialization_error_string
        if initialized is not None:
            self.initialized = initialized
        if jstype is not None:
            self.jstype = jstype
        if lazy is not None:
            self.lazy = lazy
        if memoized_serialized_size is not None:
            self.memoized_serialized_size = memoized_serialized_size
        if packed is not None:
            self.packed = packed
        if parser_for_type is not None:
            self.parser_for_type = parser_for_type
        if retention is not None:
            self.retention = retention
        if serialized_size is not None:
            self.serialized_size = serialized_size
        if targets_count is not None:
            self.targets_count = targets_count
        if targets_list is not None:
            self.targets_list = targets_list
        if uninterpreted_option_count is not None:
            self.uninterpreted_option_count = uninterpreted_option_count
        if uninterpreted_option_list is not None:
            self.uninterpreted_option_list = uninterpreted_option_list
        if uninterpreted_option_or_builder_list is not None:
            self.uninterpreted_option_or_builder_list = uninterpreted_option_or_builder_list
        if unknown_fields is not None:
            self.unknown_fields = unknown_fields
        if unverified_lazy is not None:
            self.unverified_lazy = unverified_lazy
        if weak is not None:
            self.weak = weak

    @property
    def all_fields(self):
        """Gets the all_fields of this FieldOptions.  # noqa: E501


        :return: The all_fields of this FieldOptions.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._all_fields

    @all_fields.setter
    def all_fields(self, all_fields):
        """Sets the all_fields of this FieldOptions.


        :param all_fields: The all_fields of this FieldOptions.  # noqa: E501
        :type: dict(str, object)
        """

        self._all_fields = all_fields

    @property
    def all_fields_raw(self):
        """Gets the all_fields_raw of this FieldOptions.  # noqa: E501


        :return: The all_fields_raw of this FieldOptions.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._all_fields_raw

    @all_fields_raw.setter
    def all_fields_raw(self, all_fields_raw):
        """Sets the all_fields_raw of this FieldOptions.


        :param all_fields_raw: The all_fields_raw of this FieldOptions.  # noqa: E501
        :type: dict(str, object)
        """

        self._all_fields_raw = all_fields_raw

    @property
    def ctype(self):
        """Gets the ctype of this FieldOptions.  # noqa: E501


        :return: The ctype of this FieldOptions.  # noqa: E501
        :rtype: str
        """
        return self._ctype

    @ctype.setter
    def ctype(self, ctype):
        """Sets the ctype of this FieldOptions.


        :param ctype: The ctype of this FieldOptions.  # noqa: E501
        :type: str
        """
        allowed_values = ["STRING", "CORD", "STRING_PIECE"]  # noqa: E501
        if ctype not in allowed_values:
            raise ValueError(
                "Invalid value for `ctype` ({0}), must be one of {1}"  # noqa: E501
                .format(ctype, allowed_values)
            )

        self._ctype = ctype

    @property
    def debug_redact(self):
        """Gets the debug_redact of this FieldOptions.  # noqa: E501


        :return: The debug_redact of this FieldOptions.  # noqa: E501
        :rtype: bool
        """
        return self._debug_redact

    @debug_redact.setter
    def debug_redact(self, debug_redact):
        """Sets the debug_redact of this FieldOptions.


        :param debug_redact: The debug_redact of this FieldOptions.  # noqa: E501
        :type: bool
        """

        self._debug_redact = debug_redact

    @property
    def default_instance_for_type(self):
        """Gets the default_instance_for_type of this FieldOptions.  # noqa: E501


        :return: The default_instance_for_type of this FieldOptions.  # noqa: E501
        :rtype: FieldOptions
        """
        return self._default_instance_for_type

    @default_instance_for_type.setter
    def default_instance_for_type(self, default_instance_for_type):
        """Sets the default_instance_for_type of this FieldOptions.


        :param default_instance_for_type: The default_instance_for_type of this FieldOptions.  # noqa: E501
        :type: FieldOptions
        """

        self._default_instance_for_type = default_instance_for_type

    @property
    def deprecated(self):
        """Gets the deprecated of this FieldOptions.  # noqa: E501


        :return: The deprecated of this FieldOptions.  # noqa: E501
        :rtype: bool
        """
        return self._deprecated

    @deprecated.setter
    def deprecated(self, deprecated):
        """Sets the deprecated of this FieldOptions.


        :param deprecated: The deprecated of this FieldOptions.  # noqa: E501
        :type: bool
        """

        self._deprecated = deprecated

    @property
    def descriptor_for_type(self):
        """Gets the descriptor_for_type of this FieldOptions.  # noqa: E501


        :return: The descriptor_for_type of this FieldOptions.  # noqa: E501
        :rtype: Descriptor
        """
        return self._descriptor_for_type

    @descriptor_for_type.setter
    def descriptor_for_type(self, descriptor_for_type):
        """Sets the descriptor_for_type of this FieldOptions.


        :param descriptor_for_type: The descriptor_for_type of this FieldOptions.  # noqa: E501
        :type: Descriptor
        """

        self._descriptor_for_type = descriptor_for_type

    @property
    def edition_defaults_count(self):
        """Gets the edition_defaults_count of this FieldOptions.  # noqa: E501


        :return: The edition_defaults_count of this FieldOptions.  # noqa: E501
        :rtype: int
        """
        return self._edition_defaults_count

    @edition_defaults_count.setter
    def edition_defaults_count(self, edition_defaults_count):
        """Sets the edition_defaults_count of this FieldOptions.


        :param edition_defaults_count: The edition_defaults_count of this FieldOptions.  # noqa: E501
        :type: int
        """

        self._edition_defaults_count = edition_defaults_count

    @property
    def edition_defaults_list(self):
        """Gets the edition_defaults_list of this FieldOptions.  # noqa: E501


        :return: The edition_defaults_list of this FieldOptions.  # noqa: E501
        :rtype: list[EditionDefault]
        """
        return self._edition_defaults_list

    @edition_defaults_list.setter
    def edition_defaults_list(self, edition_defaults_list):
        """Sets the edition_defaults_list of this FieldOptions.


        :param edition_defaults_list: The edition_defaults_list of this FieldOptions.  # noqa: E501
        :type: list[EditionDefault]
        """

        self._edition_defaults_list = edition_defaults_list

    @property
    def edition_defaults_or_builder_list(self):
        """Gets the edition_defaults_or_builder_list of this FieldOptions.  # noqa: E501


        :return: The edition_defaults_or_builder_list of this FieldOptions.  # noqa: E501
        :rtype: list[EditionDefaultOrBuilder]
        """
        return self._edition_defaults_or_builder_list

    @edition_defaults_or_builder_list.setter
    def edition_defaults_or_builder_list(self, edition_defaults_or_builder_list):
        """Sets the edition_defaults_or_builder_list of this FieldOptions.


        :param edition_defaults_or_builder_list: The edition_defaults_or_builder_list of this FieldOptions.  # noqa: E501
        :type: list[EditionDefaultOrBuilder]
        """

        self._edition_defaults_or_builder_list = edition_defaults_or_builder_list

    @property
    def feature_support(self):
        """Gets the feature_support of this FieldOptions.  # noqa: E501


        :return: The feature_support of this FieldOptions.  # noqa: E501
        :rtype: FeatureSupport
        """
        return self._feature_support

    @feature_support.setter
    def feature_support(self, feature_support):
        """Sets the feature_support of this FieldOptions.


        :param feature_support: The feature_support of this FieldOptions.  # noqa: E501
        :type: FeatureSupport
        """

        self._feature_support = feature_support

    @property
    def feature_support_or_builder(self):
        """Gets the feature_support_or_builder of this FieldOptions.  # noqa: E501


        :return: The feature_support_or_builder of this FieldOptions.  # noqa: E501
        :rtype: FeatureSupportOrBuilder
        """
        return self._feature_support_or_builder

    @feature_support_or_builder.setter
    def feature_support_or_builder(self, feature_support_or_builder):
        """Sets the feature_support_or_builder of this FieldOptions.


        :param feature_support_or_builder: The feature_support_or_builder of this FieldOptions.  # noqa: E501
        :type: FeatureSupportOrBuilder
        """

        self._feature_support_or_builder = feature_support_or_builder

    @property
    def features(self):
        """Gets the features of this FieldOptions.  # noqa: E501


        :return: The features of this FieldOptions.  # noqa: E501
        :rtype: FeatureSet
        """
        return self._features

    @features.setter
    def features(self, features):
        """Sets the features of this FieldOptions.


        :param features: The features of this FieldOptions.  # noqa: E501
        :type: FeatureSet
        """

        self._features = features

    @property
    def features_or_builder(self):
        """Gets the features_or_builder of this FieldOptions.  # noqa: E501


        :return: The features_or_builder of this FieldOptions.  # noqa: E501
        :rtype: FeatureSetOrBuilder
        """
        return self._features_or_builder

    @features_or_builder.setter
    def features_or_builder(self, features_or_builder):
        """Sets the features_or_builder of this FieldOptions.


        :param features_or_builder: The features_or_builder of this FieldOptions.  # noqa: E501
        :type: FeatureSetOrBuilder
        """

        self._features_or_builder = features_or_builder

    @property
    def initialization_error_string(self):
        """Gets the initialization_error_string of this FieldOptions.  # noqa: E501


        :return: The initialization_error_string of this FieldOptions.  # noqa: E501
        :rtype: str
        """
        return self._initialization_error_string

    @initialization_error_string.setter
    def initialization_error_string(self, initialization_error_string):
        """Sets the initialization_error_string of this FieldOptions.


        :param initialization_error_string: The initialization_error_string of this FieldOptions.  # noqa: E501
        :type: str
        """

        self._initialization_error_string = initialization_error_string

    @property
    def initialized(self):
        """Gets the initialized of this FieldOptions.  # noqa: E501


        :return: The initialized of this FieldOptions.  # noqa: E501
        :rtype: bool
        """
        return self._initialized

    @initialized.setter
    def initialized(self, initialized):
        """Sets the initialized of this FieldOptions.


        :param initialized: The initialized of this FieldOptions.  # noqa: E501
        :type: bool
        """

        self._initialized = initialized

    @property
    def jstype(self):
        """Gets the jstype of this FieldOptions.  # noqa: E501


        :return: The jstype of this FieldOptions.  # noqa: E501
        :rtype: str
        """
        return self._jstype

    @jstype.setter
    def jstype(self, jstype):
        """Sets the jstype of this FieldOptions.


        :param jstype: The jstype of this FieldOptions.  # noqa: E501
        :type: str
        """
        allowed_values = ["JS_NORMAL", "JS_STRING", "JS_NUMBER"]  # noqa: E501
        if jstype not in allowed_values:
            raise ValueError(
                "Invalid value for `jstype` ({0}), must be one of {1}"  # noqa: E501
                .format(jstype, allowed_values)
            )

        self._jstype = jstype

    @property
    def lazy(self):
        """Gets the lazy of this FieldOptions.  # noqa: E501


        :return: The lazy of this FieldOptions.  # noqa: E501
        :rtype: bool
        """
        return self._lazy

    @lazy.setter
    def lazy(self, lazy):
        """Sets the lazy of this FieldOptions.


        :param lazy: The lazy of this FieldOptions.  # noqa: E501
        :type: bool
        """

        self._lazy = lazy

    @property
    def memoized_serialized_size(self):
        """Gets the memoized_serialized_size of this FieldOptions.  # noqa: E501


        :return: The memoized_serialized_size of this FieldOptions.  # noqa: E501
        :rtype: int
        """
        return self._memoized_serialized_size

    @memoized_serialized_size.setter
    def memoized_serialized_size(self, memoized_serialized_size):
        """Sets the memoized_serialized_size of this FieldOptions.


        :param memoized_serialized_size: The memoized_serialized_size of this FieldOptions.  # noqa: E501
        :type: int
        """

        self._memoized_serialized_size = memoized_serialized_size

    @property
    def packed(self):
        """Gets the packed of this FieldOptions.  # noqa: E501


        :return: The packed of this FieldOptions.  # noqa: E501
        :rtype: bool
        """
        return self._packed

    @packed.setter
    def packed(self, packed):
        """Sets the packed of this FieldOptions.


        :param packed: The packed of this FieldOptions.  # noqa: E501
        :type: bool
        """

        self._packed = packed

    @property
    def parser_for_type(self):
        """Gets the parser_for_type of this FieldOptions.  # noqa: E501


        :return: The parser_for_type of this FieldOptions.  # noqa: E501
        :rtype: ParserFieldOptions
        """
        return self._parser_for_type

    @parser_for_type.setter
    def parser_for_type(self, parser_for_type):
        """Sets the parser_for_type of this FieldOptions.


        :param parser_for_type: The parser_for_type of this FieldOptions.  # noqa: E501
        :type: ParserFieldOptions
        """

        self._parser_for_type = parser_for_type

    @property
    def retention(self):
        """Gets the retention of this FieldOptions.  # noqa: E501


        :return: The retention of this FieldOptions.  # noqa: E501
        :rtype: str
        """
        return self._retention

    @retention.setter
    def retention(self, retention):
        """Sets the retention of this FieldOptions.


        :param retention: The retention of this FieldOptions.  # noqa: E501
        :type: str
        """
        allowed_values = ["RETENTION_UNKNOWN", "RETENTION_RUNTIME", "RETENTION_SOURCE"]  # noqa: E501
        if retention not in allowed_values:
            raise ValueError(
                "Invalid value for `retention` ({0}), must be one of {1}"  # noqa: E501
                .format(retention, allowed_values)
            )

        self._retention = retention

    @property
    def serialized_size(self):
        """Gets the serialized_size of this FieldOptions.  # noqa: E501


        :return: The serialized_size of this FieldOptions.  # noqa: E501
        :rtype: int
        """
        return self._serialized_size

    @serialized_size.setter
    def serialized_size(self, serialized_size):
        """Sets the serialized_size of this FieldOptions.


        :param serialized_size: The serialized_size of this FieldOptions.  # noqa: E501
        :type: int
        """

        self._serialized_size = serialized_size

    @property
    def targets_count(self):
        """Gets the targets_count of this FieldOptions.  # noqa: E501


        :return: The targets_count of this FieldOptions.  # noqa: E501
        :rtype: int
        """
        return self._targets_count

    @targets_count.setter
    def targets_count(self, targets_count):
        """Sets the targets_count of this FieldOptions.


        :param targets_count: The targets_count of this FieldOptions.  # noqa: E501
        :type: int
        """

        self._targets_count = targets_count

    @property
    def targets_list(self):
        """Gets the targets_list of this FieldOptions.  # noqa: E501


        :return: The targets_list of this FieldOptions.  # noqa: E501
        :rtype: list[str]
        """
        return self._targets_list

    @targets_list.setter
    def targets_list(self, targets_list):
        """Sets the targets_list of this FieldOptions.


        :param targets_list: The targets_list of this FieldOptions.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["TARGET_TYPE_UNKNOWN", "TARGET_TYPE_FILE", "TARGET_TYPE_EXTENSION_RANGE", "TARGET_TYPE_MESSAGE", "TARGET_TYPE_FIELD", "TARGET_TYPE_ONEOF", "TARGET_TYPE_ENUM", "TARGET_TYPE_ENUM_ENTRY", "TARGET_TYPE_SERVICE", "TARGET_TYPE_METHOD"]  # noqa: E501
        if not set(targets_list).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `targets_list` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(targets_list) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._targets_list = targets_list

    @property
    def uninterpreted_option_count(self):
        """Gets the uninterpreted_option_count of this FieldOptions.  # noqa: E501


        :return: The uninterpreted_option_count of this FieldOptions.  # noqa: E501
        :rtype: int
        """
        return self._uninterpreted_option_count

    @uninterpreted_option_count.setter
    def uninterpreted_option_count(self, uninterpreted_option_count):
        """Sets the uninterpreted_option_count of this FieldOptions.


        :param uninterpreted_option_count: The uninterpreted_option_count of this FieldOptions.  # noqa: E501
        :type: int
        """

        self._uninterpreted_option_count = uninterpreted_option_count

    @property
    def uninterpreted_option_list(self):
        """Gets the uninterpreted_option_list of this FieldOptions.  # noqa: E501


        :return: The uninterpreted_option_list of this FieldOptions.  # noqa: E501
        :rtype: list[UninterpretedOption]
        """
        return self._uninterpreted_option_list

    @uninterpreted_option_list.setter
    def uninterpreted_option_list(self, uninterpreted_option_list):
        """Sets the uninterpreted_option_list of this FieldOptions.


        :param uninterpreted_option_list: The uninterpreted_option_list of this FieldOptions.  # noqa: E501
        :type: list[UninterpretedOption]
        """

        self._uninterpreted_option_list = uninterpreted_option_list

    @property
    def uninterpreted_option_or_builder_list(self):
        """Gets the uninterpreted_option_or_builder_list of this FieldOptions.  # noqa: E501


        :return: The uninterpreted_option_or_builder_list of this FieldOptions.  # noqa: E501
        :rtype: list[UninterpretedOptionOrBuilder]
        """
        return self._uninterpreted_option_or_builder_list

    @uninterpreted_option_or_builder_list.setter
    def uninterpreted_option_or_builder_list(self, uninterpreted_option_or_builder_list):
        """Sets the uninterpreted_option_or_builder_list of this FieldOptions.


        :param uninterpreted_option_or_builder_list: The uninterpreted_option_or_builder_list of this FieldOptions.  # noqa: E501
        :type: list[UninterpretedOptionOrBuilder]
        """

        self._uninterpreted_option_or_builder_list = uninterpreted_option_or_builder_list

    @property
    def unknown_fields(self):
        """Gets the unknown_fields of this FieldOptions.  # noqa: E501


        :return: The unknown_fields of this FieldOptions.  # noqa: E501
        :rtype: UnknownFieldSet
        """
        return self._unknown_fields

    @unknown_fields.setter
    def unknown_fields(self, unknown_fields):
        """Sets the unknown_fields of this FieldOptions.


        :param unknown_fields: The unknown_fields of this FieldOptions.  # noqa: E501
        :type: UnknownFieldSet
        """

        self._unknown_fields = unknown_fields

    @property
    def unverified_lazy(self):
        """Gets the unverified_lazy of this FieldOptions.  # noqa: E501


        :return: The unverified_lazy of this FieldOptions.  # noqa: E501
        :rtype: bool
        """
        return self._unverified_lazy

    @unverified_lazy.setter
    def unverified_lazy(self, unverified_lazy):
        """Sets the unverified_lazy of this FieldOptions.


        :param unverified_lazy: The unverified_lazy of this FieldOptions.  # noqa: E501
        :type: bool
        """

        self._unverified_lazy = unverified_lazy

    @property
    def weak(self):
        """Gets the weak of this FieldOptions.  # noqa: E501


        :return: The weak of this FieldOptions.  # noqa: E501
        :rtype: bool
        """
        return self._weak

    @weak.setter
    def weak(self, weak):
        """Sets the weak of this FieldOptions.


        :param weak: The weak of this FieldOptions.  # noqa: E501
        :type: bool
        """

        self._weak = weak

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
        if issubclass(FieldOptions, dict):
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
        if not isinstance(other, FieldOptions):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
