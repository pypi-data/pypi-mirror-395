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

class LevelOrBuilder(object):
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
        'descriptor_for_type': 'Descriptor',
        'group': 'str',
        'group_bytes': 'ByteString',
        'identifier': 'str',
        'identifier_bytes': 'ByteString',
        'initialization_error_string': 'str',
        'initialized': 'bool',
        'node_type': 'str',
        'node_type_bytes': 'ByteString',
        'original_identifier': 'str',
        'original_identifier_bytes': 'ByteString',
        'retry_index': 'int',
        'runtime_id': 'str',
        'runtime_id_bytes': 'ByteString',
        'setup_id': 'str',
        'setup_id_bytes': 'ByteString',
        'skip_expression_chain': 'bool',
        'start_ts': 'int',
        'step_type': 'StepType',
        'step_type_or_builder': 'StepTypeOrBuilder',
        'strategy_info': 'StrategyInfo',
        'strategy_info_or_builder': 'StrategyInfoOrBuilder',
        'strategy_metadata': 'StrategyMetadata',
        'strategy_metadata_or_builder': 'StrategyMetadataOrBuilder',
        'unknown_fields': 'UnknownFieldSet'
    }

    attribute_map = {
        'all_fields': 'allFields',
        'default_instance_for_type': 'defaultInstanceForType',
        'descriptor_for_type': 'descriptorForType',
        'group': 'group',
        'group_bytes': 'groupBytes',
        'identifier': 'identifier',
        'identifier_bytes': 'identifierBytes',
        'initialization_error_string': 'initializationErrorString',
        'initialized': 'initialized',
        'node_type': 'nodeType',
        'node_type_bytes': 'nodeTypeBytes',
        'original_identifier': 'originalIdentifier',
        'original_identifier_bytes': 'originalIdentifierBytes',
        'retry_index': 'retryIndex',
        'runtime_id': 'runtimeId',
        'runtime_id_bytes': 'runtimeIdBytes',
        'setup_id': 'setupId',
        'setup_id_bytes': 'setupIdBytes',
        'skip_expression_chain': 'skipExpressionChain',
        'start_ts': 'startTs',
        'step_type': 'stepType',
        'step_type_or_builder': 'stepTypeOrBuilder',
        'strategy_info': 'strategyInfo',
        'strategy_info_or_builder': 'strategyInfoOrBuilder',
        'strategy_metadata': 'strategyMetadata',
        'strategy_metadata_or_builder': 'strategyMetadataOrBuilder',
        'unknown_fields': 'unknownFields'
    }

    def __init__(self, all_fields=None, default_instance_for_type=None, descriptor_for_type=None, group=None, group_bytes=None, identifier=None, identifier_bytes=None, initialization_error_string=None, initialized=None, node_type=None, node_type_bytes=None, original_identifier=None, original_identifier_bytes=None, retry_index=None, runtime_id=None, runtime_id_bytes=None, setup_id=None, setup_id_bytes=None, skip_expression_chain=None, start_ts=None, step_type=None, step_type_or_builder=None, strategy_info=None, strategy_info_or_builder=None, strategy_metadata=None, strategy_metadata_or_builder=None, unknown_fields=None):  # noqa: E501
        """LevelOrBuilder - a model defined in Swagger"""  # noqa: E501
        self._all_fields = None
        self._default_instance_for_type = None
        self._descriptor_for_type = None
        self._group = None
        self._group_bytes = None
        self._identifier = None
        self._identifier_bytes = None
        self._initialization_error_string = None
        self._initialized = None
        self._node_type = None
        self._node_type_bytes = None
        self._original_identifier = None
        self._original_identifier_bytes = None
        self._retry_index = None
        self._runtime_id = None
        self._runtime_id_bytes = None
        self._setup_id = None
        self._setup_id_bytes = None
        self._skip_expression_chain = None
        self._start_ts = None
        self._step_type = None
        self._step_type_or_builder = None
        self._strategy_info = None
        self._strategy_info_or_builder = None
        self._strategy_metadata = None
        self._strategy_metadata_or_builder = None
        self._unknown_fields = None
        self.discriminator = None
        if all_fields is not None:
            self.all_fields = all_fields
        if default_instance_for_type is not None:
            self.default_instance_for_type = default_instance_for_type
        if descriptor_for_type is not None:
            self.descriptor_for_type = descriptor_for_type
        if group is not None:
            self.group = group
        if group_bytes is not None:
            self.group_bytes = group_bytes
        if identifier is not None:
            self.identifier = identifier
        if identifier_bytes is not None:
            self.identifier_bytes = identifier_bytes
        if initialization_error_string is not None:
            self.initialization_error_string = initialization_error_string
        if initialized is not None:
            self.initialized = initialized
        if node_type is not None:
            self.node_type = node_type
        if node_type_bytes is not None:
            self.node_type_bytes = node_type_bytes
        if original_identifier is not None:
            self.original_identifier = original_identifier
        if original_identifier_bytes is not None:
            self.original_identifier_bytes = original_identifier_bytes
        if retry_index is not None:
            self.retry_index = retry_index
        if runtime_id is not None:
            self.runtime_id = runtime_id
        if runtime_id_bytes is not None:
            self.runtime_id_bytes = runtime_id_bytes
        if setup_id is not None:
            self.setup_id = setup_id
        if setup_id_bytes is not None:
            self.setup_id_bytes = setup_id_bytes
        if skip_expression_chain is not None:
            self.skip_expression_chain = skip_expression_chain
        if start_ts is not None:
            self.start_ts = start_ts
        if step_type is not None:
            self.step_type = step_type
        if step_type_or_builder is not None:
            self.step_type_or_builder = step_type_or_builder
        if strategy_info is not None:
            self.strategy_info = strategy_info
        if strategy_info_or_builder is not None:
            self.strategy_info_or_builder = strategy_info_or_builder
        if strategy_metadata is not None:
            self.strategy_metadata = strategy_metadata
        if strategy_metadata_or_builder is not None:
            self.strategy_metadata_or_builder = strategy_metadata_or_builder
        if unknown_fields is not None:
            self.unknown_fields = unknown_fields

    @property
    def all_fields(self):
        """Gets the all_fields of this LevelOrBuilder.  # noqa: E501


        :return: The all_fields of this LevelOrBuilder.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._all_fields

    @all_fields.setter
    def all_fields(self, all_fields):
        """Sets the all_fields of this LevelOrBuilder.


        :param all_fields: The all_fields of this LevelOrBuilder.  # noqa: E501
        :type: dict(str, object)
        """

        self._all_fields = all_fields

    @property
    def default_instance_for_type(self):
        """Gets the default_instance_for_type of this LevelOrBuilder.  # noqa: E501


        :return: The default_instance_for_type of this LevelOrBuilder.  # noqa: E501
        :rtype: Message
        """
        return self._default_instance_for_type

    @default_instance_for_type.setter
    def default_instance_for_type(self, default_instance_for_type):
        """Sets the default_instance_for_type of this LevelOrBuilder.


        :param default_instance_for_type: The default_instance_for_type of this LevelOrBuilder.  # noqa: E501
        :type: Message
        """

        self._default_instance_for_type = default_instance_for_type

    @property
    def descriptor_for_type(self):
        """Gets the descriptor_for_type of this LevelOrBuilder.  # noqa: E501


        :return: The descriptor_for_type of this LevelOrBuilder.  # noqa: E501
        :rtype: Descriptor
        """
        return self._descriptor_for_type

    @descriptor_for_type.setter
    def descriptor_for_type(self, descriptor_for_type):
        """Sets the descriptor_for_type of this LevelOrBuilder.


        :param descriptor_for_type: The descriptor_for_type of this LevelOrBuilder.  # noqa: E501
        :type: Descriptor
        """

        self._descriptor_for_type = descriptor_for_type

    @property
    def group(self):
        """Gets the group of this LevelOrBuilder.  # noqa: E501


        :return: The group of this LevelOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._group

    @group.setter
    def group(self, group):
        """Sets the group of this LevelOrBuilder.


        :param group: The group of this LevelOrBuilder.  # noqa: E501
        :type: str
        """

        self._group = group

    @property
    def group_bytes(self):
        """Gets the group_bytes of this LevelOrBuilder.  # noqa: E501


        :return: The group_bytes of this LevelOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._group_bytes

    @group_bytes.setter
    def group_bytes(self, group_bytes):
        """Sets the group_bytes of this LevelOrBuilder.


        :param group_bytes: The group_bytes of this LevelOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._group_bytes = group_bytes

    @property
    def identifier(self):
        """Gets the identifier of this LevelOrBuilder.  # noqa: E501


        :return: The identifier of this LevelOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this LevelOrBuilder.


        :param identifier: The identifier of this LevelOrBuilder.  # noqa: E501
        :type: str
        """

        self._identifier = identifier

    @property
    def identifier_bytes(self):
        """Gets the identifier_bytes of this LevelOrBuilder.  # noqa: E501


        :return: The identifier_bytes of this LevelOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._identifier_bytes

    @identifier_bytes.setter
    def identifier_bytes(self, identifier_bytes):
        """Sets the identifier_bytes of this LevelOrBuilder.


        :param identifier_bytes: The identifier_bytes of this LevelOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._identifier_bytes = identifier_bytes

    @property
    def initialization_error_string(self):
        """Gets the initialization_error_string of this LevelOrBuilder.  # noqa: E501


        :return: The initialization_error_string of this LevelOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._initialization_error_string

    @initialization_error_string.setter
    def initialization_error_string(self, initialization_error_string):
        """Sets the initialization_error_string of this LevelOrBuilder.


        :param initialization_error_string: The initialization_error_string of this LevelOrBuilder.  # noqa: E501
        :type: str
        """

        self._initialization_error_string = initialization_error_string

    @property
    def initialized(self):
        """Gets the initialized of this LevelOrBuilder.  # noqa: E501


        :return: The initialized of this LevelOrBuilder.  # noqa: E501
        :rtype: bool
        """
        return self._initialized

    @initialized.setter
    def initialized(self, initialized):
        """Sets the initialized of this LevelOrBuilder.


        :param initialized: The initialized of this LevelOrBuilder.  # noqa: E501
        :type: bool
        """

        self._initialized = initialized

    @property
    def node_type(self):
        """Gets the node_type of this LevelOrBuilder.  # noqa: E501


        :return: The node_type of this LevelOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._node_type

    @node_type.setter
    def node_type(self, node_type):
        """Sets the node_type of this LevelOrBuilder.


        :param node_type: The node_type of this LevelOrBuilder.  # noqa: E501
        :type: str
        """

        self._node_type = node_type

    @property
    def node_type_bytes(self):
        """Gets the node_type_bytes of this LevelOrBuilder.  # noqa: E501


        :return: The node_type_bytes of this LevelOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._node_type_bytes

    @node_type_bytes.setter
    def node_type_bytes(self, node_type_bytes):
        """Sets the node_type_bytes of this LevelOrBuilder.


        :param node_type_bytes: The node_type_bytes of this LevelOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._node_type_bytes = node_type_bytes

    @property
    def original_identifier(self):
        """Gets the original_identifier of this LevelOrBuilder.  # noqa: E501


        :return: The original_identifier of this LevelOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._original_identifier

    @original_identifier.setter
    def original_identifier(self, original_identifier):
        """Sets the original_identifier of this LevelOrBuilder.


        :param original_identifier: The original_identifier of this LevelOrBuilder.  # noqa: E501
        :type: str
        """

        self._original_identifier = original_identifier

    @property
    def original_identifier_bytes(self):
        """Gets the original_identifier_bytes of this LevelOrBuilder.  # noqa: E501


        :return: The original_identifier_bytes of this LevelOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._original_identifier_bytes

    @original_identifier_bytes.setter
    def original_identifier_bytes(self, original_identifier_bytes):
        """Sets the original_identifier_bytes of this LevelOrBuilder.


        :param original_identifier_bytes: The original_identifier_bytes of this LevelOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._original_identifier_bytes = original_identifier_bytes

    @property
    def retry_index(self):
        """Gets the retry_index of this LevelOrBuilder.  # noqa: E501


        :return: The retry_index of this LevelOrBuilder.  # noqa: E501
        :rtype: int
        """
        return self._retry_index

    @retry_index.setter
    def retry_index(self, retry_index):
        """Sets the retry_index of this LevelOrBuilder.


        :param retry_index: The retry_index of this LevelOrBuilder.  # noqa: E501
        :type: int
        """

        self._retry_index = retry_index

    @property
    def runtime_id(self):
        """Gets the runtime_id of this LevelOrBuilder.  # noqa: E501


        :return: The runtime_id of this LevelOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._runtime_id

    @runtime_id.setter
    def runtime_id(self, runtime_id):
        """Sets the runtime_id of this LevelOrBuilder.


        :param runtime_id: The runtime_id of this LevelOrBuilder.  # noqa: E501
        :type: str
        """

        self._runtime_id = runtime_id

    @property
    def runtime_id_bytes(self):
        """Gets the runtime_id_bytes of this LevelOrBuilder.  # noqa: E501


        :return: The runtime_id_bytes of this LevelOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._runtime_id_bytes

    @runtime_id_bytes.setter
    def runtime_id_bytes(self, runtime_id_bytes):
        """Sets the runtime_id_bytes of this LevelOrBuilder.


        :param runtime_id_bytes: The runtime_id_bytes of this LevelOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._runtime_id_bytes = runtime_id_bytes

    @property
    def setup_id(self):
        """Gets the setup_id of this LevelOrBuilder.  # noqa: E501


        :return: The setup_id of this LevelOrBuilder.  # noqa: E501
        :rtype: str
        """
        return self._setup_id

    @setup_id.setter
    def setup_id(self, setup_id):
        """Sets the setup_id of this LevelOrBuilder.


        :param setup_id: The setup_id of this LevelOrBuilder.  # noqa: E501
        :type: str
        """

        self._setup_id = setup_id

    @property
    def setup_id_bytes(self):
        """Gets the setup_id_bytes of this LevelOrBuilder.  # noqa: E501


        :return: The setup_id_bytes of this LevelOrBuilder.  # noqa: E501
        :rtype: ByteString
        """
        return self._setup_id_bytes

    @setup_id_bytes.setter
    def setup_id_bytes(self, setup_id_bytes):
        """Sets the setup_id_bytes of this LevelOrBuilder.


        :param setup_id_bytes: The setup_id_bytes of this LevelOrBuilder.  # noqa: E501
        :type: ByteString
        """

        self._setup_id_bytes = setup_id_bytes

    @property
    def skip_expression_chain(self):
        """Gets the skip_expression_chain of this LevelOrBuilder.  # noqa: E501


        :return: The skip_expression_chain of this LevelOrBuilder.  # noqa: E501
        :rtype: bool
        """
        return self._skip_expression_chain

    @skip_expression_chain.setter
    def skip_expression_chain(self, skip_expression_chain):
        """Sets the skip_expression_chain of this LevelOrBuilder.


        :param skip_expression_chain: The skip_expression_chain of this LevelOrBuilder.  # noqa: E501
        :type: bool
        """

        self._skip_expression_chain = skip_expression_chain

    @property
    def start_ts(self):
        """Gets the start_ts of this LevelOrBuilder.  # noqa: E501


        :return: The start_ts of this LevelOrBuilder.  # noqa: E501
        :rtype: int
        """
        return self._start_ts

    @start_ts.setter
    def start_ts(self, start_ts):
        """Sets the start_ts of this LevelOrBuilder.


        :param start_ts: The start_ts of this LevelOrBuilder.  # noqa: E501
        :type: int
        """

        self._start_ts = start_ts

    @property
    def step_type(self):
        """Gets the step_type of this LevelOrBuilder.  # noqa: E501


        :return: The step_type of this LevelOrBuilder.  # noqa: E501
        :rtype: StepType
        """
        return self._step_type

    @step_type.setter
    def step_type(self, step_type):
        """Sets the step_type of this LevelOrBuilder.


        :param step_type: The step_type of this LevelOrBuilder.  # noqa: E501
        :type: StepType
        """

        self._step_type = step_type

    @property
    def step_type_or_builder(self):
        """Gets the step_type_or_builder of this LevelOrBuilder.  # noqa: E501


        :return: The step_type_or_builder of this LevelOrBuilder.  # noqa: E501
        :rtype: StepTypeOrBuilder
        """
        return self._step_type_or_builder

    @step_type_or_builder.setter
    def step_type_or_builder(self, step_type_or_builder):
        """Sets the step_type_or_builder of this LevelOrBuilder.


        :param step_type_or_builder: The step_type_or_builder of this LevelOrBuilder.  # noqa: E501
        :type: StepTypeOrBuilder
        """

        self._step_type_or_builder = step_type_or_builder

    @property
    def strategy_info(self):
        """Gets the strategy_info of this LevelOrBuilder.  # noqa: E501


        :return: The strategy_info of this LevelOrBuilder.  # noqa: E501
        :rtype: StrategyInfo
        """
        return self._strategy_info

    @strategy_info.setter
    def strategy_info(self, strategy_info):
        """Sets the strategy_info of this LevelOrBuilder.


        :param strategy_info: The strategy_info of this LevelOrBuilder.  # noqa: E501
        :type: StrategyInfo
        """

        self._strategy_info = strategy_info

    @property
    def strategy_info_or_builder(self):
        """Gets the strategy_info_or_builder of this LevelOrBuilder.  # noqa: E501


        :return: The strategy_info_or_builder of this LevelOrBuilder.  # noqa: E501
        :rtype: StrategyInfoOrBuilder
        """
        return self._strategy_info_or_builder

    @strategy_info_or_builder.setter
    def strategy_info_or_builder(self, strategy_info_or_builder):
        """Sets the strategy_info_or_builder of this LevelOrBuilder.


        :param strategy_info_or_builder: The strategy_info_or_builder of this LevelOrBuilder.  # noqa: E501
        :type: StrategyInfoOrBuilder
        """

        self._strategy_info_or_builder = strategy_info_or_builder

    @property
    def strategy_metadata(self):
        """Gets the strategy_metadata of this LevelOrBuilder.  # noqa: E501


        :return: The strategy_metadata of this LevelOrBuilder.  # noqa: E501
        :rtype: StrategyMetadata
        """
        return self._strategy_metadata

    @strategy_metadata.setter
    def strategy_metadata(self, strategy_metadata):
        """Sets the strategy_metadata of this LevelOrBuilder.


        :param strategy_metadata: The strategy_metadata of this LevelOrBuilder.  # noqa: E501
        :type: StrategyMetadata
        """

        self._strategy_metadata = strategy_metadata

    @property
    def strategy_metadata_or_builder(self):
        """Gets the strategy_metadata_or_builder of this LevelOrBuilder.  # noqa: E501


        :return: The strategy_metadata_or_builder of this LevelOrBuilder.  # noqa: E501
        :rtype: StrategyMetadataOrBuilder
        """
        return self._strategy_metadata_or_builder

    @strategy_metadata_or_builder.setter
    def strategy_metadata_or_builder(self, strategy_metadata_or_builder):
        """Sets the strategy_metadata_or_builder of this LevelOrBuilder.


        :param strategy_metadata_or_builder: The strategy_metadata_or_builder of this LevelOrBuilder.  # noqa: E501
        :type: StrategyMetadataOrBuilder
        """

        self._strategy_metadata_or_builder = strategy_metadata_or_builder

    @property
    def unknown_fields(self):
        """Gets the unknown_fields of this LevelOrBuilder.  # noqa: E501


        :return: The unknown_fields of this LevelOrBuilder.  # noqa: E501
        :rtype: UnknownFieldSet
        """
        return self._unknown_fields

    @unknown_fields.setter
    def unknown_fields(self, unknown_fields):
        """Sets the unknown_fields of this LevelOrBuilder.


        :param unknown_fields: The unknown_fields of this LevelOrBuilder.  # noqa: E501
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
        if issubclass(LevelOrBuilder, dict):
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
        if not isinstance(other, LevelOrBuilder):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
