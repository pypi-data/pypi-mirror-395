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

class FailureDataOrBuilder(object):
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
        'code': 'str',
        'code_bytes': 'ByteString',
        'default_instance_for_type': 'Message',
        'descriptor_for_type': 'Descriptor',
        'failure_type_infos_count': 'int',
        'failure_type_infos_list': 'list[FailureTypeInfo]',
        'failure_type_infos_or_builder_list': 'list[FailureTypeInfoOrBuilder]',
        'failure_types_count': 'int',
        'failure_types_list': 'list[str]',
        'failure_types_value_list': 'list[int]',
        'initialization_error_string': 'str',
        'initialized': 'bool',
        'level': 'str',
        'level_bytes': 'ByteString',
        'message': 'str',
        'message_bytes': 'ByteString',
        'stage_identifier': 'str',
        'stage_identifier_bytes': 'ByteString',
        'step_identifier': 'str',
        'step_identifier_bytes': 'ByteString',
        'unknown_fields': 'UnknownFieldSet'
    }

    attribute_map = {
        'all_fields': 'allFields',
        'code': 'code',
        'code_bytes': 'codeBytes',
        'default_instance_for_type': 'defaultInstanceForType',
        'descriptor_for_type': 'descriptorForType',
        'failure_type_infos_count': 'failureTypeInfosCount',
        'failure_type_infos_list': 'failureTypeInfosList',
        'failure_type_infos_or_builder_list': 'failureTypeInfosOrBuilderList',
        'failure_types_count': 'failureTypesCount',
        'failure_types_list': 'failureTypesList',
        'failure_types_value_list': 'failureTypesValueList',
        'initialization_error_string': 'initializationErrorString',
        'initialized': 'initialized',
        'level': 'level',
        'level_bytes': 'levelBytes',
        'message': 'message',
        'message_bytes': 'messageBytes',
        'stage_identifier': 'stageIdentifier',
        'stage_identifier_bytes': 'stageIdentifierBytes',
        'step_identifier': 'stepIdentifier',
        'step_identifier_bytes': 'stepIdentifierBytes',
        'unknown_fields': 'unknownFields'
    }

    def __init__(self, all_fields=None, code=None, code_bytes=None, default_instance_for_type=None, descriptor_for_type=None, failure_type_infos_count=None, failure_type_infos_list=None, failure_type_infos_or_builder_list=None, failure_types_count=None, failure_types_list=None, failure_types_value_list=None, initialization_error_string=None, initialized=None, level=None, level_bytes=None, message=None, message_bytes=None, stage_identifier=None, stage_identifier_bytes=None, step_identifier=None, step_identifier_bytes=None, unknown_fields=None):  # noqa: E501
        """FailureDataOrBuilder - a model defined in Swagger"""  # noqa: E501
        self._all_fields = None
        self._code = None
        self._code_bytes = None
        self._default_instance_for_type = None
        self._descriptor_for_type = None
        self._failure_type_infos_count = None
        self._failure_type_infos_list = None
        self._failure_type_infos_or_builder_list = None
        self._failure_types_count = None
        self._failure_types_list = None
        self._failure_types_value_list = None
        self._initialization_error_string = None
        self._initialized = None
        self._level = None
        self._level_bytes = None
        self._message = None
        self._message_bytes = None
        self._stage_identifier = None
        self._stage_identifier_bytes = None
        self._step_identifier = None
        self._step_identifier_bytes = None
        self._unknown_fields = None
        self.discriminator = None
        if all_fields is not None:
            self.all_fields = all_fields
        if code is not None:
            self.code = code
        if code_bytes is not None:
            self.code_bytes = code_bytes
        if default_instance_for_type is not None:
            self.default_instance_for_type = default_instance_for_type
        if descriptor_for_type is not None:
            self.descriptor_for_type = descriptor_for_type
        if failure_type_infos_count is not None:
            self.failure_type_infos_count = failure_type_infos_count
        if failure_type_infos_list is not None:
            self.failure_type_infos_list = failure_type_infos_list
        if failure_type_infos_or_builder_list is not None:
            self.failure_type_infos_or_builder_list = failure_type_infos_or_builder_list
        if failure_types_count is not None:
            self.failure_types_count = failure_types_count
        if failure_types_list is not None:
            self.failure_types_list = failure_types_list
        if failure_types_value_list is not None:
            self.failure_types_value_list = failure_types_value_list
        if initialization_error_string is not None:
            self.initialization_error_string = initialization_error_string
        if initialized is not None:
            self.initialized = initialized
        if level is not None:
            self.level = level
        if level_bytes is not None:
            self.level_bytes = level_bytes
        if message is not None:
            self.message = message
        if message_bytes is not None:
            self.message_bytes = message_bytes
        if stage_identifier is not None:
            self.stage_identifier = stage_identifier
        if stage_identifier_bytes is not None:
            self.stage_identifier_bytes = stage_identifier_bytes
        if step_identifier is not None:
            self.step_identifier = step_identifier
        if step_identifier_bytes is not None:
            self.step_identifier_bytes = step_identifier_bytes
        if unknown_fields is not None:
            self.unknown_fields = unknown_fields

    @property
    def all_fields(self):
        """Gets the all_fields of this FailureDataOrBuilder.  # noqa: E501


        :return: The all_fields of this FailureDataOrBuilder.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._all_fields

    @all_fields.setter
    def all_fields(self, all_fields):
        """Sets the all_fields of this FailureDataOrBuilder.


        :param all_fields: The all_fields of this FailureDataOrBuilder.  # noqa: E501
        :type: dict(str, object)
        """

        self._all_fields = all_fields

    @property
    def code(self):
        """Gets the code of this FailureDataOrBuilder.  # noqa: E501


        :return: The code of this FailureDataOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this FailureDataOrBuilder.


        :param code: The code of this FailureDataOrBuilder.  # noqa: E501
        :type: str
        """

        self._code = code

    @property
    def code_bytes(self):
        """Gets the code_bytes of this FailureDataOrBuilder.  # noqa: E501


        :return: The code_bytes of this FailureDataOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._code_bytes

    @code_bytes.setter
    def code_bytes(self, code_bytes):
        """Sets the code_bytes of this FailureDataOrBuilder.


        :param code_bytes: The code_bytes of this FailureDataOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._code_bytes = code_bytes

    @property
    def default_instance_for_type(self):
        """Gets the default_instance_for_type of this FailureDataOrBuilder.  # noqa: E501


        :return: The default_instance_for_type of this FailureDataOrBuilder.  # noqa: E501
        :rtype: Message
        """
        return self._default_instance_for_type

    @default_instance_for_type.setter
    def default_instance_for_type(self, default_instance_for_type):
        """Sets the default_instance_for_type of this FailureDataOrBuilder.


        :param default_instance_for_type: The default_instance_for_type of this FailureDataOrBuilder.  # noqa: E501
        :type: Message
        """

        self._default_instance_for_type = default_instance_for_type

    @property
    def descriptor_for_type(self):
        """Gets the descriptor_for_type of this FailureDataOrBuilder.  # noqa: E501


        :return: The descriptor_for_type of this FailureDataOrBuilder.  # noqa: E501
        :rtype: Descriptor
        """
        return self._descriptor_for_type

    @descriptor_for_type.setter
    def descriptor_for_type(self, descriptor_for_type):
        """Sets the descriptor_for_type of this FailureDataOrBuilder.


        :param descriptor_for_type: The descriptor_for_type of this FailureDataOrBuilder.  # noqa: E501
        :type: Descriptor
        """

        self._descriptor_for_type = descriptor_for_type

    @property
    def failure_type_infos_count(self):
        """Gets the failure_type_infos_count of this FailureDataOrBuilder.  # noqa: E501


        :return: The failure_type_infos_count of this FailureDataOrBuilder.  # noqa: E501
        :rtype: int
        """
        return self._failure_type_infos_count

    @failure_type_infos_count.setter
    def failure_type_infos_count(self, failure_type_infos_count):
        """Sets the failure_type_infos_count of this FailureDataOrBuilder.


        :param failure_type_infos_count: The failure_type_infos_count of this FailureDataOrBuilder.  # noqa: E501
        :type: int
        """

        self._failure_type_infos_count = failure_type_infos_count

    @property
    def failure_type_infos_list(self):
        """Gets the failure_type_infos_list of this FailureDataOrBuilder.  # noqa: E501


        :return: The failure_type_infos_list of this FailureDataOrBuilder.  # noqa: E501
        :rtype: list[FailureTypeInfo]
        """
        return self._failure_type_infos_list

    @failure_type_infos_list.setter
    def failure_type_infos_list(self, failure_type_infos_list):
        """Sets the failure_type_infos_list of this FailureDataOrBuilder.


        :param failure_type_infos_list: The failure_type_infos_list of this FailureDataOrBuilder.  # noqa: E501
        :type: list[FailureTypeInfo]
        """

        self._failure_type_infos_list = failure_type_infos_list

    @property
    def failure_type_infos_or_builder_list(self):
        """Gets the failure_type_infos_or_builder_list of this FailureDataOrBuilder.  # noqa: E501


        :return: The failure_type_infos_or_builder_list of this FailureDataOrBuilder.  # noqa: E501
        :rtype: list[FailureTypeInfoOrBuilder]
        """
        return self._failure_type_infos_or_builder_list

    @failure_type_infos_or_builder_list.setter
    def failure_type_infos_or_builder_list(self, failure_type_infos_or_builder_list):
        """Sets the failure_type_infos_or_builder_list of this FailureDataOrBuilder.


        :param failure_type_infos_or_builder_list: The failure_type_infos_or_builder_list of this FailureDataOrBuilder.  # noqa: E501
        :type: list[FailureTypeInfoOrBuilder]
        """

        self._failure_type_infos_or_builder_list = failure_type_infos_or_builder_list

    @property
    def failure_types_count(self):
        """Gets the failure_types_count of this FailureDataOrBuilder.  # noqa: E501


        :return: The failure_types_count of this FailureDataOrBuilder.  # noqa: E501
        :rtype: int
        """
        return self._failure_types_count

    @failure_types_count.setter
    def failure_types_count(self, failure_types_count):
        """Sets the failure_types_count of this FailureDataOrBuilder.


        :param failure_types_count: The failure_types_count of this FailureDataOrBuilder.  # noqa: E501
        :type: int
        """

        self._failure_types_count = failure_types_count

    @property
    def failure_types_list(self):
        """Gets the failure_types_list of this FailureDataOrBuilder.  # noqa: E501


        :return: The failure_types_list of this FailureDataOrBuilder.  # noqa: E501
        :rtype: list[str]
        """
        return self._failure_types_list

    @failure_types_list.setter
    def failure_types_list(self, failure_types_list):
        """Sets the failure_types_list of this FailureDataOrBuilder.


        :param failure_types_list: The failure_types_list of this FailureDataOrBuilder.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["UNKNOWN_FAILURE", "DELEGATE_PROVISIONING_FAILURE", "CONNECTIVITY_FAILURE", "AUTHENTICATION_FAILURE", "VERIFICATION_FAILURE", "APPLICATION_FAILURE", "AUTHORIZATION_FAILURE", "TIMEOUT_FAILURE", "SKIPPING_FAILURE", "POLICY_EVALUATION_FAILURE", "INPUT_TIMEOUT_FAILURE", "FREEZE_ACTIVE_FAILURE", "APPROVAL_REJECTION", "DELEGATE_RESTART", "USER_MARKED_FAILURE", "UNRECOGNIZED"]  # noqa: E501
        if not set(failure_types_list).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `failure_types_list` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(failure_types_list) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._failure_types_list = failure_types_list

    @property
    def failure_types_value_list(self):
        """Gets the failure_types_value_list of this FailureDataOrBuilder.  # noqa: E501


        :return: The failure_types_value_list of this FailureDataOrBuilder.  # noqa: E501
        :rtype: list[int]
        """
        return self._failure_types_value_list

    @failure_types_value_list.setter
    def failure_types_value_list(self, failure_types_value_list):
        """Sets the failure_types_value_list of this FailureDataOrBuilder.


        :param failure_types_value_list: The failure_types_value_list of this FailureDataOrBuilder.  # noqa: E501
        :type: list[int]
        """

        self._failure_types_value_list = failure_types_value_list

    @property
    def initialization_error_string(self):
        """Gets the initialization_error_string of this FailureDataOrBuilder.  # noqa: E501


        :return: The initialization_error_string of this FailureDataOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._initialization_error_string

    @initialization_error_string.setter
    def initialization_error_string(self, initialization_error_string):
        """Sets the initialization_error_string of this FailureDataOrBuilder.


        :param initialization_error_string: The initialization_error_string of this FailureDataOrBuilder.  # noqa: E501
        :type: str
        """

        self._initialization_error_string = initialization_error_string

    @property
    def initialized(self):
        """Gets the initialized of this FailureDataOrBuilder.  # noqa: E501


        :return: The initialized of this FailureDataOrBuilder.  # noqa: E501
        :rtype: bool
        """
        return self._initialized

    @initialized.setter
    def initialized(self, initialized):
        """Sets the initialized of this FailureDataOrBuilder.


        :param initialized: The initialized of this FailureDataOrBuilder.  # noqa: E501
        :type: bool
        """

        self._initialized = initialized

    @property
    def level(self):
        """Gets the level of this FailureDataOrBuilder.  # noqa: E501


        :return: The level of this FailureDataOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._level

    @level.setter
    def level(self, level):
        """Sets the level of this FailureDataOrBuilder.


        :param level: The level of this FailureDataOrBuilder.  # noqa: E501
        :type: str
        """

        self._level = level

    @property
    def level_bytes(self):
        """Gets the level_bytes of this FailureDataOrBuilder.  # noqa: E501


        :return: The level_bytes of this FailureDataOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._level_bytes

    @level_bytes.setter
    def level_bytes(self, level_bytes):
        """Sets the level_bytes of this FailureDataOrBuilder.


        :param level_bytes: The level_bytes of this FailureDataOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._level_bytes = level_bytes

    @property
    def message(self):
        """Gets the message of this FailureDataOrBuilder.  # noqa: E501


        :return: The message of this FailureDataOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this FailureDataOrBuilder.


        :param message: The message of this FailureDataOrBuilder.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def message_bytes(self):
        """Gets the message_bytes of this FailureDataOrBuilder.  # noqa: E501


        :return: The message_bytes of this FailureDataOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._message_bytes

    @message_bytes.setter
    def message_bytes(self, message_bytes):
        """Sets the message_bytes of this FailureDataOrBuilder.


        :param message_bytes: The message_bytes of this FailureDataOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._message_bytes = message_bytes

    @property
    def stage_identifier(self):
        """Gets the stage_identifier of this FailureDataOrBuilder.  # noqa: E501


        :return: The stage_identifier of this FailureDataOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._stage_identifier

    @stage_identifier.setter
    def stage_identifier(self, stage_identifier):
        """Sets the stage_identifier of this FailureDataOrBuilder.


        :param stage_identifier: The stage_identifier of this FailureDataOrBuilder.  # noqa: E501
        :type: str
        """

        self._stage_identifier = stage_identifier

    @property
    def stage_identifier_bytes(self):
        """Gets the stage_identifier_bytes of this FailureDataOrBuilder.  # noqa: E501


        :return: The stage_identifier_bytes of this FailureDataOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._stage_identifier_bytes

    @stage_identifier_bytes.setter
    def stage_identifier_bytes(self, stage_identifier_bytes):
        """Sets the stage_identifier_bytes of this FailureDataOrBuilder.


        :param stage_identifier_bytes: The stage_identifier_bytes of this FailureDataOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._stage_identifier_bytes = stage_identifier_bytes

    @property
    def step_identifier(self):
        """Gets the step_identifier of this FailureDataOrBuilder.  # noqa: E501


        :return: The step_identifier of this FailureDataOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._step_identifier

    @step_identifier.setter
    def step_identifier(self, step_identifier):
        """Sets the step_identifier of this FailureDataOrBuilder.


        :param step_identifier: The step_identifier of this FailureDataOrBuilder.  # noqa: E501
        :type: str
        """

        self._step_identifier = step_identifier

    @property
    def step_identifier_bytes(self):
        """Gets the step_identifier_bytes of this FailureDataOrBuilder.  # noqa: E501


        :return: The step_identifier_bytes of this FailureDataOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._step_identifier_bytes

    @step_identifier_bytes.setter
    def step_identifier_bytes(self, step_identifier_bytes):
        """Sets the step_identifier_bytes of this FailureDataOrBuilder.


        :param step_identifier_bytes: The step_identifier_bytes of this FailureDataOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._step_identifier_bytes = step_identifier_bytes

    @property
    def unknown_fields(self):
        """Gets the unknown_fields of this FailureDataOrBuilder.  # noqa: E501


        :return: The unknown_fields of this FailureDataOrBuilder.  # noqa: E501
        :rtype: UnknownFieldSet
        """
        return self._unknown_fields

    @unknown_fields.setter
    def unknown_fields(self, unknown_fields):
        """Sets the unknown_fields of this FailureDataOrBuilder.


        :param unknown_fields: The unknown_fields of this FailureDataOrBuilder.  # noqa: E501
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
        if issubclass(FailureDataOrBuilder, dict):
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
        if not isinstance(other, FailureDataOrBuilder):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
