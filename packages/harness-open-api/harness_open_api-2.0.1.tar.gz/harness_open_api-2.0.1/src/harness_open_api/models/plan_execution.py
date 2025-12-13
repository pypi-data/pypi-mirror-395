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

class PlanExecution(object):
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
        'ambiance': 'Ambiance',
        'created_at': 'int',
        'end_ts': 'int',
        'expression_functor_token': 'int',
        'failure_info': 'FailureInfo',
        'governance_metadata': 'PipelineGovernanceMetadata',
        'last_updated_at': 'int',
        'metadata': 'ExecutionMetadata',
        'next_iteration': 'int',
        'node_id': 'str',
        'node_type': 'str',
        'plan_id': 'str',
        'post_execution_rollback_infos': 'list[PostExecutionRollbackInfo]',
        'priority_type': 'str',
        'processed_yaml': 'str',
        'setup_abstractions': 'dict(str, str)',
        'stage_expression_values_map': 'dict(str, object)',
        'stages_execution_metadata': 'StagesExecutionMetadata',
        'start_ts': 'int',
        'status': 'str',
        'trigger_header': 'list[HeaderConfig]',
        'trigger_json_payload': 'str',
        'trigger_payload': 'TriggerPayload',
        'uuid': 'str',
        'valid_until': 'datetime',
        'version': 'int'
    }

    attribute_map = {
        'ambiance': 'ambiance',
        'created_at': 'createdAt',
        'end_ts': 'endTs',
        'expression_functor_token': 'expressionFunctorToken',
        'failure_info': 'failureInfo',
        'governance_metadata': 'governanceMetadata',
        'last_updated_at': 'lastUpdatedAt',
        'metadata': 'metadata',
        'next_iteration': 'nextIteration',
        'node_id': 'nodeId',
        'node_type': 'nodeType',
        'plan_id': 'planId',
        'post_execution_rollback_infos': 'postExecutionRollbackInfos',
        'priority_type': 'priorityType',
        'processed_yaml': 'processedYaml',
        'setup_abstractions': 'setupAbstractions',
        'stage_expression_values_map': 'stageExpressionValuesMap',
        'stages_execution_metadata': 'stagesExecutionMetadata',
        'start_ts': 'startTs',
        'status': 'status',
        'trigger_header': 'triggerHeader',
        'trigger_json_payload': 'triggerJsonPayload',
        'trigger_payload': 'triggerPayload',
        'uuid': 'uuid',
        'valid_until': 'validUntil',
        'version': 'version'
    }

    def __init__(self, ambiance=None, created_at=None, end_ts=None, expression_functor_token=None, failure_info=None, governance_metadata=None, last_updated_at=None, metadata=None, next_iteration=None, node_id=None, node_type=None, plan_id=None, post_execution_rollback_infos=None, priority_type=None, processed_yaml=None, setup_abstractions=None, stage_expression_values_map=None, stages_execution_metadata=None, start_ts=None, status=None, trigger_header=None, trigger_json_payload=None, trigger_payload=None, uuid=None, valid_until=None, version=None):  # noqa: E501
        """PlanExecution - a model defined in Swagger"""  # noqa: E501
        self._ambiance = None
        self._created_at = None
        self._end_ts = None
        self._expression_functor_token = None
        self._failure_info = None
        self._governance_metadata = None
        self._last_updated_at = None
        self._metadata = None
        self._next_iteration = None
        self._node_id = None
        self._node_type = None
        self._plan_id = None
        self._post_execution_rollback_infos = None
        self._priority_type = None
        self._processed_yaml = None
        self._setup_abstractions = None
        self._stage_expression_values_map = None
        self._stages_execution_metadata = None
        self._start_ts = None
        self._status = None
        self._trigger_header = None
        self._trigger_json_payload = None
        self._trigger_payload = None
        self._uuid = None
        self._valid_until = None
        self._version = None
        self.discriminator = None
        if ambiance is not None:
            self.ambiance = ambiance
        if created_at is not None:
            self.created_at = created_at
        if end_ts is not None:
            self.end_ts = end_ts
        if expression_functor_token is not None:
            self.expression_functor_token = expression_functor_token
        if failure_info is not None:
            self.failure_info = failure_info
        if governance_metadata is not None:
            self.governance_metadata = governance_metadata
        if last_updated_at is not None:
            self.last_updated_at = last_updated_at
        if metadata is not None:
            self.metadata = metadata
        if next_iteration is not None:
            self.next_iteration = next_iteration
        if node_id is not None:
            self.node_id = node_id
        if node_type is not None:
            self.node_type = node_type
        if plan_id is not None:
            self.plan_id = plan_id
        if post_execution_rollback_infos is not None:
            self.post_execution_rollback_infos = post_execution_rollback_infos
        if priority_type is not None:
            self.priority_type = priority_type
        if processed_yaml is not None:
            self.processed_yaml = processed_yaml
        if setup_abstractions is not None:
            self.setup_abstractions = setup_abstractions
        if stage_expression_values_map is not None:
            self.stage_expression_values_map = stage_expression_values_map
        if stages_execution_metadata is not None:
            self.stages_execution_metadata = stages_execution_metadata
        if start_ts is not None:
            self.start_ts = start_ts
        if status is not None:
            self.status = status
        if trigger_header is not None:
            self.trigger_header = trigger_header
        if trigger_json_payload is not None:
            self.trigger_json_payload = trigger_json_payload
        if trigger_payload is not None:
            self.trigger_payload = trigger_payload
        if uuid is not None:
            self.uuid = uuid
        if valid_until is not None:
            self.valid_until = valid_until
        if version is not None:
            self.version = version

    @property
    def ambiance(self):
        """Gets the ambiance of this PlanExecution.  # noqa: E501


        :return: The ambiance of this PlanExecution.  # noqa: E501
        :rtype: Ambiance
        """
        return self._ambiance

    @ambiance.setter
    def ambiance(self, ambiance):
        """Sets the ambiance of this PlanExecution.


        :param ambiance: The ambiance of this PlanExecution.  # noqa: E501
        :type: Ambiance
        """

        self._ambiance = ambiance

    @property
    def created_at(self):
        """Gets the created_at of this PlanExecution.  # noqa: E501


        :return: The created_at of this PlanExecution.  # noqa: E501
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this PlanExecution.


        :param created_at: The created_at of this PlanExecution.  # noqa: E501
        :type: int
        """

        self._created_at = created_at

    @property
    def end_ts(self):
        """Gets the end_ts of this PlanExecution.  # noqa: E501


        :return: The end_ts of this PlanExecution.  # noqa: E501
        :rtype: int
        """
        return self._end_ts

    @end_ts.setter
    def end_ts(self, end_ts):
        """Sets the end_ts of this PlanExecution.


        :param end_ts: The end_ts of this PlanExecution.  # noqa: E501
        :type: int
        """

        self._end_ts = end_ts

    @property
    def expression_functor_token(self):
        """Gets the expression_functor_token of this PlanExecution.  # noqa: E501


        :return: The expression_functor_token of this PlanExecution.  # noqa: E501
        :rtype: int
        """
        return self._expression_functor_token

    @expression_functor_token.setter
    def expression_functor_token(self, expression_functor_token):
        """Sets the expression_functor_token of this PlanExecution.


        :param expression_functor_token: The expression_functor_token of this PlanExecution.  # noqa: E501
        :type: int
        """

        self._expression_functor_token = expression_functor_token

    @property
    def failure_info(self):
        """Gets the failure_info of this PlanExecution.  # noqa: E501


        :return: The failure_info of this PlanExecution.  # noqa: E501
        :rtype: FailureInfo
        """
        return self._failure_info

    @failure_info.setter
    def failure_info(self, failure_info):
        """Sets the failure_info of this PlanExecution.


        :param failure_info: The failure_info of this PlanExecution.  # noqa: E501
        :type: FailureInfo
        """

        self._failure_info = failure_info

    @property
    def governance_metadata(self):
        """Gets the governance_metadata of this PlanExecution.  # noqa: E501


        :return: The governance_metadata of this PlanExecution.  # noqa: E501
        :rtype: PipelineGovernanceMetadata
        """
        return self._governance_metadata

    @governance_metadata.setter
    def governance_metadata(self, governance_metadata):
        """Sets the governance_metadata of this PlanExecution.


        :param governance_metadata: The governance_metadata of this PlanExecution.  # noqa: E501
        :type: PipelineGovernanceMetadata
        """

        self._governance_metadata = governance_metadata

    @property
    def last_updated_at(self):
        """Gets the last_updated_at of this PlanExecution.  # noqa: E501


        :return: The last_updated_at of this PlanExecution.  # noqa: E501
        :rtype: int
        """
        return self._last_updated_at

    @last_updated_at.setter
    def last_updated_at(self, last_updated_at):
        """Sets the last_updated_at of this PlanExecution.


        :param last_updated_at: The last_updated_at of this PlanExecution.  # noqa: E501
        :type: int
        """

        self._last_updated_at = last_updated_at

    @property
    def metadata(self):
        """Gets the metadata of this PlanExecution.  # noqa: E501


        :return: The metadata of this PlanExecution.  # noqa: E501
        :rtype: ExecutionMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this PlanExecution.


        :param metadata: The metadata of this PlanExecution.  # noqa: E501
        :type: ExecutionMetadata
        """

        self._metadata = metadata

    @property
    def next_iteration(self):
        """Gets the next_iteration of this PlanExecution.  # noqa: E501


        :return: The next_iteration of this PlanExecution.  # noqa: E501
        :rtype: int
        """
        return self._next_iteration

    @next_iteration.setter
    def next_iteration(self, next_iteration):
        """Sets the next_iteration of this PlanExecution.


        :param next_iteration: The next_iteration of this PlanExecution.  # noqa: E501
        :type: int
        """

        self._next_iteration = next_iteration

    @property
    def node_id(self):
        """Gets the node_id of this PlanExecution.  # noqa: E501


        :return: The node_id of this PlanExecution.  # noqa: E501
        :rtype: str
        """
        return self._node_id

    @node_id.setter
    def node_id(self, node_id):
        """Sets the node_id of this PlanExecution.


        :param node_id: The node_id of this PlanExecution.  # noqa: E501
        :type: str
        """

        self._node_id = node_id

    @property
    def node_type(self):
        """Gets the node_type of this PlanExecution.  # noqa: E501


        :return: The node_type of this PlanExecution.  # noqa: E501
        :rtype: str
        """
        return self._node_type

    @node_type.setter
    def node_type(self, node_type):
        """Sets the node_type of this PlanExecution.


        :param node_type: The node_type of this PlanExecution.  # noqa: E501
        :type: str
        """
        allowed_values = ["PLAN", "PLAN_NODE", "IDENTITY_PLAN_NODE"]  # noqa: E501
        if node_type not in allowed_values:
            raise ValueError(
                "Invalid value for `node_type` ({0}), must be one of {1}"  # noqa: E501
                .format(node_type, allowed_values)
            )

        self._node_type = node_type

    @property
    def plan_id(self):
        """Gets the plan_id of this PlanExecution.  # noqa: E501


        :return: The plan_id of this PlanExecution.  # noqa: E501
        :rtype: str
        """
        return self._plan_id

    @plan_id.setter
    def plan_id(self, plan_id):
        """Sets the plan_id of this PlanExecution.


        :param plan_id: The plan_id of this PlanExecution.  # noqa: E501
        :type: str
        """

        self._plan_id = plan_id

    @property
    def post_execution_rollback_infos(self):
        """Gets the post_execution_rollback_infos of this PlanExecution.  # noqa: E501


        :return: The post_execution_rollback_infos of this PlanExecution.  # noqa: E501
        :rtype: list[PostExecutionRollbackInfo]
        """
        return self._post_execution_rollback_infos

    @post_execution_rollback_infos.setter
    def post_execution_rollback_infos(self, post_execution_rollback_infos):
        """Sets the post_execution_rollback_infos of this PlanExecution.


        :param post_execution_rollback_infos: The post_execution_rollback_infos of this PlanExecution.  # noqa: E501
        :type: list[PostExecutionRollbackInfo]
        """

        self._post_execution_rollback_infos = post_execution_rollback_infos

    @property
    def priority_type(self):
        """Gets the priority_type of this PlanExecution.  # noqa: E501


        :return: The priority_type of this PlanExecution.  # noqa: E501
        :rtype: str
        """
        return self._priority_type

    @priority_type.setter
    def priority_type(self, priority_type):
        """Sets the priority_type of this PlanExecution.


        :param priority_type: The priority_type of this PlanExecution.  # noqa: E501
        :type: str
        """
        allowed_values = ["HIGH", "LOW", "NORMAL"]  # noqa: E501
        if priority_type not in allowed_values:
            raise ValueError(
                "Invalid value for `priority_type` ({0}), must be one of {1}"  # noqa: E501
                .format(priority_type, allowed_values)
            )

        self._priority_type = priority_type

    @property
    def processed_yaml(self):
        """Gets the processed_yaml of this PlanExecution.  # noqa: E501


        :return: The processed_yaml of this PlanExecution.  # noqa: E501
        :rtype: str
        """
        return self._processed_yaml

    @processed_yaml.setter
    def processed_yaml(self, processed_yaml):
        """Sets the processed_yaml of this PlanExecution.


        :param processed_yaml: The processed_yaml of this PlanExecution.  # noqa: E501
        :type: str
        """

        self._processed_yaml = processed_yaml

    @property
    def setup_abstractions(self):
        """Gets the setup_abstractions of this PlanExecution.  # noqa: E501


        :return: The setup_abstractions of this PlanExecution.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._setup_abstractions

    @setup_abstractions.setter
    def setup_abstractions(self, setup_abstractions):
        """Sets the setup_abstractions of this PlanExecution.


        :param setup_abstractions: The setup_abstractions of this PlanExecution.  # noqa: E501
        :type: dict(str, str)
        """

        self._setup_abstractions = setup_abstractions

    @property
    def stage_expression_values_map(self):
        """Gets the stage_expression_values_map of this PlanExecution.  # noqa: E501


        :return: The stage_expression_values_map of this PlanExecution.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._stage_expression_values_map

    @stage_expression_values_map.setter
    def stage_expression_values_map(self, stage_expression_values_map):
        """Sets the stage_expression_values_map of this PlanExecution.


        :param stage_expression_values_map: The stage_expression_values_map of this PlanExecution.  # noqa: E501
        :type: dict(str, object)
        """

        self._stage_expression_values_map = stage_expression_values_map

    @property
    def stages_execution_metadata(self):
        """Gets the stages_execution_metadata of this PlanExecution.  # noqa: E501


        :return: The stages_execution_metadata of this PlanExecution.  # noqa: E501
        :rtype: StagesExecutionMetadata
        """
        return self._stages_execution_metadata

    @stages_execution_metadata.setter
    def stages_execution_metadata(self, stages_execution_metadata):
        """Sets the stages_execution_metadata of this PlanExecution.


        :param stages_execution_metadata: The stages_execution_metadata of this PlanExecution.  # noqa: E501
        :type: StagesExecutionMetadata
        """

        self._stages_execution_metadata = stages_execution_metadata

    @property
    def start_ts(self):
        """Gets the start_ts of this PlanExecution.  # noqa: E501


        :return: The start_ts of this PlanExecution.  # noqa: E501
        :rtype: int
        """
        return self._start_ts

    @start_ts.setter
    def start_ts(self, start_ts):
        """Sets the start_ts of this PlanExecution.


        :param start_ts: The start_ts of this PlanExecution.  # noqa: E501
        :type: int
        """

        self._start_ts = start_ts

    @property
    def status(self):
        """Gets the status of this PlanExecution.  # noqa: E501


        :return: The status of this PlanExecution.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this PlanExecution.


        :param status: The status of this PlanExecution.  # noqa: E501
        :type: str
        """
        allowed_values = ["NO_OP", "RUNNING", "INTERVENTION_WAITING", "TIMED_WAITING", "ASYNC_WAITING", "TASK_WAITING", "DISCONTINUING", "PAUSING", "QUEUED", "SKIPPED", "PAUSED", "ABORTED", "ERRORED", "FAILED", "EXPIRED", "SUSPENDED", "SUCCEEDED", "IGNORE_FAILED", "APPROVAL_WAITING", "RESOURCE_WAITING", "APPROVAL_REJECTED", "INPUT_WAITING", "WAIT_STEP_RUNNING", "FREEZE_FAILED", "QUEUED_LICENSE_LIMIT_REACHED", "QUEUED_EXECUTION_CONCURRENCY_REACHED", "QUEUED_STEP_LIMIT_REACHED", "STARTING_QUEUED_STEP", "UPLOAD_WAITING", "QUEUED_PLAN_CREATION", "STARTING_PLAN_CREATION", "UNRECOGNIZED"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def trigger_header(self):
        """Gets the trigger_header of this PlanExecution.  # noqa: E501


        :return: The trigger_header of this PlanExecution.  # noqa: E501
        :rtype: list[HeaderConfig]
        """
        return self._trigger_header

    @trigger_header.setter
    def trigger_header(self, trigger_header):
        """Sets the trigger_header of this PlanExecution.


        :param trigger_header: The trigger_header of this PlanExecution.  # noqa: E501
        :type: list[HeaderConfig]
        """

        self._trigger_header = trigger_header

    @property
    def trigger_json_payload(self):
        """Gets the trigger_json_payload of this PlanExecution.  # noqa: E501


        :return: The trigger_json_payload of this PlanExecution.  # noqa: E501
        :rtype: str
        """
        return self._trigger_json_payload

    @trigger_json_payload.setter
    def trigger_json_payload(self, trigger_json_payload):
        """Sets the trigger_json_payload of this PlanExecution.


        :param trigger_json_payload: The trigger_json_payload of this PlanExecution.  # noqa: E501
        :type: str
        """

        self._trigger_json_payload = trigger_json_payload

    @property
    def trigger_payload(self):
        """Gets the trigger_payload of this PlanExecution.  # noqa: E501


        :return: The trigger_payload of this PlanExecution.  # noqa: E501
        :rtype: TriggerPayload
        """
        return self._trigger_payload

    @trigger_payload.setter
    def trigger_payload(self, trigger_payload):
        """Sets the trigger_payload of this PlanExecution.


        :param trigger_payload: The trigger_payload of this PlanExecution.  # noqa: E501
        :type: TriggerPayload
        """

        self._trigger_payload = trigger_payload

    @property
    def uuid(self):
        """Gets the uuid of this PlanExecution.  # noqa: E501


        :return: The uuid of this PlanExecution.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this PlanExecution.


        :param uuid: The uuid of this PlanExecution.  # noqa: E501
        :type: str
        """

        self._uuid = uuid

    @property
    def valid_until(self):
        """Gets the valid_until of this PlanExecution.  # noqa: E501


        :return: The valid_until of this PlanExecution.  # noqa: E501
        :rtype: datetime
        """
        return self._valid_until

    @valid_until.setter
    def valid_until(self, valid_until):
        """Sets the valid_until of this PlanExecution.


        :param valid_until: The valid_until of this PlanExecution.  # noqa: E501
        :type: datetime
        """

        self._valid_until = valid_until

    @property
    def version(self):
        """Gets the version of this PlanExecution.  # noqa: E501


        :return: The version of this PlanExecution.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this PlanExecution.


        :param version: The version of this PlanExecution.  # noqa: E501
        :type: int
        """

        self._version = version

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
        if issubclass(PlanExecution, dict):
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
        if not isinstance(other, PlanExecution):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
