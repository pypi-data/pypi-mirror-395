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

class PipelineExecutionSummary(object):
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
        'aborted_by': 'AbortedBy',
        'allow_stage_executions': 'bool',
        'can_re_execute': 'bool',
        'can_retry': 'bool',
        'connector_ref': 'str',
        'created_at': 'int',
        'dynamic_execution': 'bool',
        'end_ts': 'int',
        'execution_error_info': 'ExecutionErrorInfo',
        'execution_input_configured': 'bool',
        'execution_mode': 'str',
        'execution_trigger_info': 'ExecutionTriggerInfo',
        'failed_stages_count': 'int',
        'failure_info': 'FailureInfoDTO',
        'git_details': 'PipelineEntityGitDetails',
        'governance_metadata': 'PipelineGovernanceMetadata',
        'input_set_identifiers': 'list[str]',
        'is_dynamic_execution': 'bool',
        'is_original_yaml_used_on_rerun': 'bool',
        'is_retried_execution': 'bool',
        'is_stages_execution': 'bool',
        'labels': 'list[NGLabel]',
        'layout_node_map': 'dict(str, GraphLayoutNode)',
        'module_info': 'dict(str, dict(str, object))',
        'modules': 'list[str]',
        'name': 'str',
        'notes_exist_for_plan_execution_id': 'bool',
        'org_identifier': 'str',
        'original_yaml_used_on_rerun': 'bool',
        'parent_stage_info': 'PipelineStageInfo',
        'pipeline_identifier': 'str',
        'plan_execution_id': 'str',
        'project_identifier': 'str',
        'queued_reason': 'str',
        'queued_type': 'str',
        'retried_execution': 'bool',
        'retry_execution_metadata': 'RetryExecutionMetadata',
        'run_sequence': 'int',
        'running_stages_count': 'int',
        'should_use_simplified_key': 'bool',
        'show_retry_history': 'bool',
        'stages_executed': 'list[str]',
        'stages_executed_names': 'dict(str, str)',
        'stages_execution': 'bool',
        'start_ts': 'int',
        'starting_node_id': 'str',
        'status': 'str',
        'store_type': 'str',
        'successful_stages_count': 'int',
        'tags': 'list[NGTag]',
        'template_reference_summary': 'TemplateReferenceSummary',
        'total_stages_count': 'int',
        'yaml_version': 'str'
    }

    attribute_map = {
        'aborted_by': 'abortedBy',
        'allow_stage_executions': 'allowStageExecutions',
        'can_re_execute': 'canReExecute',
        'can_retry': 'canRetry',
        'connector_ref': 'connectorRef',
        'created_at': 'createdAt',
        'dynamic_execution': 'dynamicExecution',
        'end_ts': 'endTs',
        'execution_error_info': 'executionErrorInfo',
        'execution_input_configured': 'executionInputConfigured',
        'execution_mode': 'executionMode',
        'execution_trigger_info': 'executionTriggerInfo',
        'failed_stages_count': 'failedStagesCount',
        'failure_info': 'failureInfo',
        'git_details': 'gitDetails',
        'governance_metadata': 'governanceMetadata',
        'input_set_identifiers': 'inputSetIdentifiers',
        'is_dynamic_execution': 'isDynamicExecution',
        'is_original_yaml_used_on_rerun': 'isOriginalYamlUsedOnRerun',
        'is_retried_execution': 'isRetriedExecution',
        'is_stages_execution': 'isStagesExecution',
        'labels': 'labels',
        'layout_node_map': 'layoutNodeMap',
        'module_info': 'moduleInfo',
        'modules': 'modules',
        'name': 'name',
        'notes_exist_for_plan_execution_id': 'notesExistForPlanExecutionId',
        'org_identifier': 'orgIdentifier',
        'original_yaml_used_on_rerun': 'originalYamlUsedOnRerun',
        'parent_stage_info': 'parentStageInfo',
        'pipeline_identifier': 'pipelineIdentifier',
        'plan_execution_id': 'planExecutionId',
        'project_identifier': 'projectIdentifier',
        'queued_reason': 'queuedReason',
        'queued_type': 'queuedType',
        'retried_execution': 'retriedExecution',
        'retry_execution_metadata': 'retryExecutionMetadata',
        'run_sequence': 'runSequence',
        'running_stages_count': 'runningStagesCount',
        'should_use_simplified_key': 'shouldUseSimplifiedKey',
        'show_retry_history': 'showRetryHistory',
        'stages_executed': 'stagesExecuted',
        'stages_executed_names': 'stagesExecutedNames',
        'stages_execution': 'stagesExecution',
        'start_ts': 'startTs',
        'starting_node_id': 'startingNodeId',
        'status': 'status',
        'store_type': 'storeType',
        'successful_stages_count': 'successfulStagesCount',
        'tags': 'tags',
        'template_reference_summary': 'templateReferenceSummary',
        'total_stages_count': 'totalStagesCount',
        'yaml_version': 'yamlVersion'
    }

    def __init__(self, aborted_by=None, allow_stage_executions=None, can_re_execute=None, can_retry=None, connector_ref=None, created_at=None, dynamic_execution=None, end_ts=None, execution_error_info=None, execution_input_configured=None, execution_mode=None, execution_trigger_info=None, failed_stages_count=None, failure_info=None, git_details=None, governance_metadata=None, input_set_identifiers=None, is_dynamic_execution=None, is_original_yaml_used_on_rerun=None, is_retried_execution=None, is_stages_execution=None, labels=None, layout_node_map=None, module_info=None, modules=None, name=None, notes_exist_for_plan_execution_id=None, org_identifier=None, original_yaml_used_on_rerun=None, parent_stage_info=None, pipeline_identifier=None, plan_execution_id=None, project_identifier=None, queued_reason=None, queued_type=None, retried_execution=None, retry_execution_metadata=None, run_sequence=None, running_stages_count=None, should_use_simplified_key=None, show_retry_history=None, stages_executed=None, stages_executed_names=None, stages_execution=None, start_ts=None, starting_node_id=None, status=None, store_type=None, successful_stages_count=None, tags=None, template_reference_summary=None, total_stages_count=None, yaml_version=None):  # noqa: E501
        """PipelineExecutionSummary - a model defined in Swagger"""  # noqa: E501
        self._aborted_by = None
        self._allow_stage_executions = None
        self._can_re_execute = None
        self._can_retry = None
        self._connector_ref = None
        self._created_at = None
        self._dynamic_execution = None
        self._end_ts = None
        self._execution_error_info = None
        self._execution_input_configured = None
        self._execution_mode = None
        self._execution_trigger_info = None
        self._failed_stages_count = None
        self._failure_info = None
        self._git_details = None
        self._governance_metadata = None
        self._input_set_identifiers = None
        self._is_dynamic_execution = None
        self._is_original_yaml_used_on_rerun = None
        self._is_retried_execution = None
        self._is_stages_execution = None
        self._labels = None
        self._layout_node_map = None
        self._module_info = None
        self._modules = None
        self._name = None
        self._notes_exist_for_plan_execution_id = None
        self._org_identifier = None
        self._original_yaml_used_on_rerun = None
        self._parent_stage_info = None
        self._pipeline_identifier = None
        self._plan_execution_id = None
        self._project_identifier = None
        self._queued_reason = None
        self._queued_type = None
        self._retried_execution = None
        self._retry_execution_metadata = None
        self._run_sequence = None
        self._running_stages_count = None
        self._should_use_simplified_key = None
        self._show_retry_history = None
        self._stages_executed = None
        self._stages_executed_names = None
        self._stages_execution = None
        self._start_ts = None
        self._starting_node_id = None
        self._status = None
        self._store_type = None
        self._successful_stages_count = None
        self._tags = None
        self._template_reference_summary = None
        self._total_stages_count = None
        self._yaml_version = None
        self.discriminator = None
        if aborted_by is not None:
            self.aborted_by = aborted_by
        if allow_stage_executions is not None:
            self.allow_stage_executions = allow_stage_executions
        if can_re_execute is not None:
            self.can_re_execute = can_re_execute
        if can_retry is not None:
            self.can_retry = can_retry
        if connector_ref is not None:
            self.connector_ref = connector_ref
        if created_at is not None:
            self.created_at = created_at
        if dynamic_execution is not None:
            self.dynamic_execution = dynamic_execution
        if end_ts is not None:
            self.end_ts = end_ts
        if execution_error_info is not None:
            self.execution_error_info = execution_error_info
        if execution_input_configured is not None:
            self.execution_input_configured = execution_input_configured
        if execution_mode is not None:
            self.execution_mode = execution_mode
        if execution_trigger_info is not None:
            self.execution_trigger_info = execution_trigger_info
        if failed_stages_count is not None:
            self.failed_stages_count = failed_stages_count
        if failure_info is not None:
            self.failure_info = failure_info
        if git_details is not None:
            self.git_details = git_details
        if governance_metadata is not None:
            self.governance_metadata = governance_metadata
        if input_set_identifiers is not None:
            self.input_set_identifiers = input_set_identifiers
        if is_dynamic_execution is not None:
            self.is_dynamic_execution = is_dynamic_execution
        if is_original_yaml_used_on_rerun is not None:
            self.is_original_yaml_used_on_rerun = is_original_yaml_used_on_rerun
        if is_retried_execution is not None:
            self.is_retried_execution = is_retried_execution
        if is_stages_execution is not None:
            self.is_stages_execution = is_stages_execution
        if labels is not None:
            self.labels = labels
        if layout_node_map is not None:
            self.layout_node_map = layout_node_map
        if module_info is not None:
            self.module_info = module_info
        if modules is not None:
            self.modules = modules
        if name is not None:
            self.name = name
        if notes_exist_for_plan_execution_id is not None:
            self.notes_exist_for_plan_execution_id = notes_exist_for_plan_execution_id
        self.org_identifier = org_identifier
        if original_yaml_used_on_rerun is not None:
            self.original_yaml_used_on_rerun = original_yaml_used_on_rerun
        if parent_stage_info is not None:
            self.parent_stage_info = parent_stage_info
        if pipeline_identifier is not None:
            self.pipeline_identifier = pipeline_identifier
        if plan_execution_id is not None:
            self.plan_execution_id = plan_execution_id
        self.project_identifier = project_identifier
        if queued_reason is not None:
            self.queued_reason = queued_reason
        if queued_type is not None:
            self.queued_type = queued_type
        if retried_execution is not None:
            self.retried_execution = retried_execution
        if retry_execution_metadata is not None:
            self.retry_execution_metadata = retry_execution_metadata
        if run_sequence is not None:
            self.run_sequence = run_sequence
        if running_stages_count is not None:
            self.running_stages_count = running_stages_count
        if should_use_simplified_key is not None:
            self.should_use_simplified_key = should_use_simplified_key
        if show_retry_history is not None:
            self.show_retry_history = show_retry_history
        if stages_executed is not None:
            self.stages_executed = stages_executed
        if stages_executed_names is not None:
            self.stages_executed_names = stages_executed_names
        if stages_execution is not None:
            self.stages_execution = stages_execution
        if start_ts is not None:
            self.start_ts = start_ts
        if starting_node_id is not None:
            self.starting_node_id = starting_node_id
        if status is not None:
            self.status = status
        if store_type is not None:
            self.store_type = store_type
        if successful_stages_count is not None:
            self.successful_stages_count = successful_stages_count
        if tags is not None:
            self.tags = tags
        if template_reference_summary is not None:
            self.template_reference_summary = template_reference_summary
        if total_stages_count is not None:
            self.total_stages_count = total_stages_count
        if yaml_version is not None:
            self.yaml_version = yaml_version

    @property
    def aborted_by(self):
        """Gets the aborted_by of this PipelineExecutionSummary.  # noqa: E501


        :return: The aborted_by of this PipelineExecutionSummary.  # noqa: E501
        :rtype: AbortedBy
        """
        return self._aborted_by

    @aborted_by.setter
    def aborted_by(self, aborted_by):
        """Sets the aborted_by of this PipelineExecutionSummary.


        :param aborted_by: The aborted_by of this PipelineExecutionSummary.  # noqa: E501
        :type: AbortedBy
        """

        self._aborted_by = aborted_by

    @property
    def allow_stage_executions(self):
        """Gets the allow_stage_executions of this PipelineExecutionSummary.  # noqa: E501


        :return: The allow_stage_executions of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._allow_stage_executions

    @allow_stage_executions.setter
    def allow_stage_executions(self, allow_stage_executions):
        """Sets the allow_stage_executions of this PipelineExecutionSummary.


        :param allow_stage_executions: The allow_stage_executions of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._allow_stage_executions = allow_stage_executions

    @property
    def can_re_execute(self):
        """Gets the can_re_execute of this PipelineExecutionSummary.  # noqa: E501


        :return: The can_re_execute of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._can_re_execute

    @can_re_execute.setter
    def can_re_execute(self, can_re_execute):
        """Sets the can_re_execute of this PipelineExecutionSummary.


        :param can_re_execute: The can_re_execute of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._can_re_execute = can_re_execute

    @property
    def can_retry(self):
        """Gets the can_retry of this PipelineExecutionSummary.  # noqa: E501


        :return: The can_retry of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._can_retry

    @can_retry.setter
    def can_retry(self, can_retry):
        """Sets the can_retry of this PipelineExecutionSummary.


        :param can_retry: The can_retry of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._can_retry = can_retry

    @property
    def connector_ref(self):
        """Gets the connector_ref of this PipelineExecutionSummary.  # noqa: E501


        :return: The connector_ref of this PipelineExecutionSummary.  # noqa: E501
        :rtype: str
        """
        return self._connector_ref

    @connector_ref.setter
    def connector_ref(self, connector_ref):
        """Sets the connector_ref of this PipelineExecutionSummary.


        :param connector_ref: The connector_ref of this PipelineExecutionSummary.  # noqa: E501
        :type: str
        """

        self._connector_ref = connector_ref

    @property
    def created_at(self):
        """Gets the created_at of this PipelineExecutionSummary.  # noqa: E501


        :return: The created_at of this PipelineExecutionSummary.  # noqa: E501
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this PipelineExecutionSummary.


        :param created_at: The created_at of this PipelineExecutionSummary.  # noqa: E501
        :type: int
        """

        self._created_at = created_at

    @property
    def dynamic_execution(self):
        """Gets the dynamic_execution of this PipelineExecutionSummary.  # noqa: E501


        :return: The dynamic_execution of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._dynamic_execution

    @dynamic_execution.setter
    def dynamic_execution(self, dynamic_execution):
        """Sets the dynamic_execution of this PipelineExecutionSummary.


        :param dynamic_execution: The dynamic_execution of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._dynamic_execution = dynamic_execution

    @property
    def end_ts(self):
        """Gets the end_ts of this PipelineExecutionSummary.  # noqa: E501


        :return: The end_ts of this PipelineExecutionSummary.  # noqa: E501
        :rtype: int
        """
        return self._end_ts

    @end_ts.setter
    def end_ts(self, end_ts):
        """Sets the end_ts of this PipelineExecutionSummary.


        :param end_ts: The end_ts of this PipelineExecutionSummary.  # noqa: E501
        :type: int
        """

        self._end_ts = end_ts

    @property
    def execution_error_info(self):
        """Gets the execution_error_info of this PipelineExecutionSummary.  # noqa: E501


        :return: The execution_error_info of this PipelineExecutionSummary.  # noqa: E501
        :rtype: ExecutionErrorInfo
        """
        return self._execution_error_info

    @execution_error_info.setter
    def execution_error_info(self, execution_error_info):
        """Sets the execution_error_info of this PipelineExecutionSummary.


        :param execution_error_info: The execution_error_info of this PipelineExecutionSummary.  # noqa: E501
        :type: ExecutionErrorInfo
        """

        self._execution_error_info = execution_error_info

    @property
    def execution_input_configured(self):
        """Gets the execution_input_configured of this PipelineExecutionSummary.  # noqa: E501


        :return: The execution_input_configured of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._execution_input_configured

    @execution_input_configured.setter
    def execution_input_configured(self, execution_input_configured):
        """Sets the execution_input_configured of this PipelineExecutionSummary.


        :param execution_input_configured: The execution_input_configured of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._execution_input_configured = execution_input_configured

    @property
    def execution_mode(self):
        """Gets the execution_mode of this PipelineExecutionSummary.  # noqa: E501


        :return: The execution_mode of this PipelineExecutionSummary.  # noqa: E501
        :rtype: str
        """
        return self._execution_mode

    @execution_mode.setter
    def execution_mode(self, execution_mode):
        """Sets the execution_mode of this PipelineExecutionSummary.


        :param execution_mode: The execution_mode of this PipelineExecutionSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["UNDEFINED_MODE", "NORMAL", "POST_EXECUTION_ROLLBACK", "PIPELINE_ROLLBACK", "UNRECOGNIZED"]  # noqa: E501
        if execution_mode not in allowed_values:
            raise ValueError(
                "Invalid value for `execution_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(execution_mode, allowed_values)
            )

        self._execution_mode = execution_mode

    @property
    def execution_trigger_info(self):
        """Gets the execution_trigger_info of this PipelineExecutionSummary.  # noqa: E501


        :return: The execution_trigger_info of this PipelineExecutionSummary.  # noqa: E501
        :rtype: ExecutionTriggerInfo
        """
        return self._execution_trigger_info

    @execution_trigger_info.setter
    def execution_trigger_info(self, execution_trigger_info):
        """Sets the execution_trigger_info of this PipelineExecutionSummary.


        :param execution_trigger_info: The execution_trigger_info of this PipelineExecutionSummary.  # noqa: E501
        :type: ExecutionTriggerInfo
        """

        self._execution_trigger_info = execution_trigger_info

    @property
    def failed_stages_count(self):
        """Gets the failed_stages_count of this PipelineExecutionSummary.  # noqa: E501


        :return: The failed_stages_count of this PipelineExecutionSummary.  # noqa: E501
        :rtype: int
        """
        return self._failed_stages_count

    @failed_stages_count.setter
    def failed_stages_count(self, failed_stages_count):
        """Sets the failed_stages_count of this PipelineExecutionSummary.


        :param failed_stages_count: The failed_stages_count of this PipelineExecutionSummary.  # noqa: E501
        :type: int
        """

        self._failed_stages_count = failed_stages_count

    @property
    def failure_info(self):
        """Gets the failure_info of this PipelineExecutionSummary.  # noqa: E501


        :return: The failure_info of this PipelineExecutionSummary.  # noqa: E501
        :rtype: FailureInfoDTO
        """
        return self._failure_info

    @failure_info.setter
    def failure_info(self, failure_info):
        """Sets the failure_info of this PipelineExecutionSummary.


        :param failure_info: The failure_info of this PipelineExecutionSummary.  # noqa: E501
        :type: FailureInfoDTO
        """

        self._failure_info = failure_info

    @property
    def git_details(self):
        """Gets the git_details of this PipelineExecutionSummary.  # noqa: E501


        :return: The git_details of this PipelineExecutionSummary.  # noqa: E501
        :rtype: PipelineEntityGitDetails
        """
        return self._git_details

    @git_details.setter
    def git_details(self, git_details):
        """Sets the git_details of this PipelineExecutionSummary.


        :param git_details: The git_details of this PipelineExecutionSummary.  # noqa: E501
        :type: PipelineEntityGitDetails
        """

        self._git_details = git_details

    @property
    def governance_metadata(self):
        """Gets the governance_metadata of this PipelineExecutionSummary.  # noqa: E501


        :return: The governance_metadata of this PipelineExecutionSummary.  # noqa: E501
        :rtype: PipelineGovernanceMetadata
        """
        return self._governance_metadata

    @governance_metadata.setter
    def governance_metadata(self, governance_metadata):
        """Sets the governance_metadata of this PipelineExecutionSummary.


        :param governance_metadata: The governance_metadata of this PipelineExecutionSummary.  # noqa: E501
        :type: PipelineGovernanceMetadata
        """

        self._governance_metadata = governance_metadata

    @property
    def input_set_identifiers(self):
        """Gets the input_set_identifiers of this PipelineExecutionSummary.  # noqa: E501


        :return: The input_set_identifiers of this PipelineExecutionSummary.  # noqa: E501
        :rtype: list[str]
        """
        return self._input_set_identifiers

    @input_set_identifiers.setter
    def input_set_identifiers(self, input_set_identifiers):
        """Sets the input_set_identifiers of this PipelineExecutionSummary.


        :param input_set_identifiers: The input_set_identifiers of this PipelineExecutionSummary.  # noqa: E501
        :type: list[str]
        """

        self._input_set_identifiers = input_set_identifiers

    @property
    def is_dynamic_execution(self):
        """Gets the is_dynamic_execution of this PipelineExecutionSummary.  # noqa: E501


        :return: The is_dynamic_execution of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._is_dynamic_execution

    @is_dynamic_execution.setter
    def is_dynamic_execution(self, is_dynamic_execution):
        """Sets the is_dynamic_execution of this PipelineExecutionSummary.


        :param is_dynamic_execution: The is_dynamic_execution of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._is_dynamic_execution = is_dynamic_execution

    @property
    def is_original_yaml_used_on_rerun(self):
        """Gets the is_original_yaml_used_on_rerun of this PipelineExecutionSummary.  # noqa: E501


        :return: The is_original_yaml_used_on_rerun of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._is_original_yaml_used_on_rerun

    @is_original_yaml_used_on_rerun.setter
    def is_original_yaml_used_on_rerun(self, is_original_yaml_used_on_rerun):
        """Sets the is_original_yaml_used_on_rerun of this PipelineExecutionSummary.


        :param is_original_yaml_used_on_rerun: The is_original_yaml_used_on_rerun of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._is_original_yaml_used_on_rerun = is_original_yaml_used_on_rerun

    @property
    def is_retried_execution(self):
        """Gets the is_retried_execution of this PipelineExecutionSummary.  # noqa: E501


        :return: The is_retried_execution of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._is_retried_execution

    @is_retried_execution.setter
    def is_retried_execution(self, is_retried_execution):
        """Sets the is_retried_execution of this PipelineExecutionSummary.


        :param is_retried_execution: The is_retried_execution of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._is_retried_execution = is_retried_execution

    @property
    def is_stages_execution(self):
        """Gets the is_stages_execution of this PipelineExecutionSummary.  # noqa: E501


        :return: The is_stages_execution of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._is_stages_execution

    @is_stages_execution.setter
    def is_stages_execution(self, is_stages_execution):
        """Sets the is_stages_execution of this PipelineExecutionSummary.


        :param is_stages_execution: The is_stages_execution of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._is_stages_execution = is_stages_execution

    @property
    def labels(self):
        """Gets the labels of this PipelineExecutionSummary.  # noqa: E501


        :return: The labels of this PipelineExecutionSummary.  # noqa: E501
        :rtype: list[NGLabel]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this PipelineExecutionSummary.


        :param labels: The labels of this PipelineExecutionSummary.  # noqa: E501
        :type: list[NGLabel]
        """

        self._labels = labels

    @property
    def layout_node_map(self):
        """Gets the layout_node_map of this PipelineExecutionSummary.  # noqa: E501


        :return: The layout_node_map of this PipelineExecutionSummary.  # noqa: E501
        :rtype: dict(str, GraphLayoutNode)
        """
        return self._layout_node_map

    @layout_node_map.setter
    def layout_node_map(self, layout_node_map):
        """Sets the layout_node_map of this PipelineExecutionSummary.


        :param layout_node_map: The layout_node_map of this PipelineExecutionSummary.  # noqa: E501
        :type: dict(str, GraphLayoutNode)
        """

        self._layout_node_map = layout_node_map

    @property
    def module_info(self):
        """Gets the module_info of this PipelineExecutionSummary.  # noqa: E501


        :return: The module_info of this PipelineExecutionSummary.  # noqa: E501
        :rtype: dict(str, dict(str, object))
        """
        return self._module_info

    @module_info.setter
    def module_info(self, module_info):
        """Sets the module_info of this PipelineExecutionSummary.


        :param module_info: The module_info of this PipelineExecutionSummary.  # noqa: E501
        :type: dict(str, dict(str, object))
        """

        self._module_info = module_info

    @property
    def modules(self):
        """Gets the modules of this PipelineExecutionSummary.  # noqa: E501


        :return: The modules of this PipelineExecutionSummary.  # noqa: E501
        :rtype: list[str]
        """
        return self._modules

    @modules.setter
    def modules(self, modules):
        """Sets the modules of this PipelineExecutionSummary.


        :param modules: The modules of this PipelineExecutionSummary.  # noqa: E501
        :type: list[str]
        """

        self._modules = modules

    @property
    def name(self):
        """Gets the name of this PipelineExecutionSummary.  # noqa: E501


        :return: The name of this PipelineExecutionSummary.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PipelineExecutionSummary.


        :param name: The name of this PipelineExecutionSummary.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def notes_exist_for_plan_execution_id(self):
        """Gets the notes_exist_for_plan_execution_id of this PipelineExecutionSummary.  # noqa: E501


        :return: The notes_exist_for_plan_execution_id of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._notes_exist_for_plan_execution_id

    @notes_exist_for_plan_execution_id.setter
    def notes_exist_for_plan_execution_id(self, notes_exist_for_plan_execution_id):
        """Sets the notes_exist_for_plan_execution_id of this PipelineExecutionSummary.


        :param notes_exist_for_plan_execution_id: The notes_exist_for_plan_execution_id of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._notes_exist_for_plan_execution_id = notes_exist_for_plan_execution_id

    @property
    def org_identifier(self):
        """Gets the org_identifier of this PipelineExecutionSummary.  # noqa: E501


        :return: The org_identifier of this PipelineExecutionSummary.  # noqa: E501
        :rtype: str
        """
        return self._org_identifier

    @org_identifier.setter
    def org_identifier(self, org_identifier):
        """Sets the org_identifier of this PipelineExecutionSummary.


        :param org_identifier: The org_identifier of this PipelineExecutionSummary.  # noqa: E501
        :type: str
        """
        if org_identifier is None:
            raise ValueError("Invalid value for `org_identifier`, must not be `None`")  # noqa: E501

        self._org_identifier = org_identifier

    @property
    def original_yaml_used_on_rerun(self):
        """Gets the original_yaml_used_on_rerun of this PipelineExecutionSummary.  # noqa: E501


        :return: The original_yaml_used_on_rerun of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._original_yaml_used_on_rerun

    @original_yaml_used_on_rerun.setter
    def original_yaml_used_on_rerun(self, original_yaml_used_on_rerun):
        """Sets the original_yaml_used_on_rerun of this PipelineExecutionSummary.


        :param original_yaml_used_on_rerun: The original_yaml_used_on_rerun of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._original_yaml_used_on_rerun = original_yaml_used_on_rerun

    @property
    def parent_stage_info(self):
        """Gets the parent_stage_info of this PipelineExecutionSummary.  # noqa: E501


        :return: The parent_stage_info of this PipelineExecutionSummary.  # noqa: E501
        :rtype: PipelineStageInfo
        """
        return self._parent_stage_info

    @parent_stage_info.setter
    def parent_stage_info(self, parent_stage_info):
        """Sets the parent_stage_info of this PipelineExecutionSummary.


        :param parent_stage_info: The parent_stage_info of this PipelineExecutionSummary.  # noqa: E501
        :type: PipelineStageInfo
        """

        self._parent_stage_info = parent_stage_info

    @property
    def pipeline_identifier(self):
        """Gets the pipeline_identifier of this PipelineExecutionSummary.  # noqa: E501


        :return: The pipeline_identifier of this PipelineExecutionSummary.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_identifier

    @pipeline_identifier.setter
    def pipeline_identifier(self, pipeline_identifier):
        """Sets the pipeline_identifier of this PipelineExecutionSummary.


        :param pipeline_identifier: The pipeline_identifier of this PipelineExecutionSummary.  # noqa: E501
        :type: str
        """

        self._pipeline_identifier = pipeline_identifier

    @property
    def plan_execution_id(self):
        """Gets the plan_execution_id of this PipelineExecutionSummary.  # noqa: E501


        :return: The plan_execution_id of this PipelineExecutionSummary.  # noqa: E501
        :rtype: str
        """
        return self._plan_execution_id

    @plan_execution_id.setter
    def plan_execution_id(self, plan_execution_id):
        """Sets the plan_execution_id of this PipelineExecutionSummary.


        :param plan_execution_id: The plan_execution_id of this PipelineExecutionSummary.  # noqa: E501
        :type: str
        """

        self._plan_execution_id = plan_execution_id

    @property
    def project_identifier(self):
        """Gets the project_identifier of this PipelineExecutionSummary.  # noqa: E501


        :return: The project_identifier of this PipelineExecutionSummary.  # noqa: E501
        :rtype: str
        """
        return self._project_identifier

    @project_identifier.setter
    def project_identifier(self, project_identifier):
        """Sets the project_identifier of this PipelineExecutionSummary.


        :param project_identifier: The project_identifier of this PipelineExecutionSummary.  # noqa: E501
        :type: str
        """
        if project_identifier is None:
            raise ValueError("Invalid value for `project_identifier`, must not be `None`")  # noqa: E501

        self._project_identifier = project_identifier

    @property
    def queued_reason(self):
        """Gets the queued_reason of this PipelineExecutionSummary.  # noqa: E501


        :return: The queued_reason of this PipelineExecutionSummary.  # noqa: E501
        :rtype: str
        """
        return self._queued_reason

    @queued_reason.setter
    def queued_reason(self, queued_reason):
        """Sets the queued_reason of this PipelineExecutionSummary.


        :param queued_reason: The queued_reason of this PipelineExecutionSummary.  # noqa: E501
        :type: str
        """

        self._queued_reason = queued_reason

    @property
    def queued_type(self):
        """Gets the queued_type of this PipelineExecutionSummary.  # noqa: E501


        :return: The queued_type of this PipelineExecutionSummary.  # noqa: E501
        :rtype: str
        """
        return self._queued_type

    @queued_type.setter
    def queued_type(self, queued_type):
        """Sets the queued_type of this PipelineExecutionSummary.


        :param queued_type: The queued_type of this PipelineExecutionSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["MAX_CONCURRENCY_REACHED", "MAX_CONCURRENCY_NOT_REACHED", "PRIORITY_CONCURRENCY_REACHED"]  # noqa: E501
        if queued_type not in allowed_values:
            raise ValueError(
                "Invalid value for `queued_type` ({0}), must be one of {1}"  # noqa: E501
                .format(queued_type, allowed_values)
            )

        self._queued_type = queued_type

    @property
    def retried_execution(self):
        """Gets the retried_execution of this PipelineExecutionSummary.  # noqa: E501


        :return: The retried_execution of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._retried_execution

    @retried_execution.setter
    def retried_execution(self, retried_execution):
        """Sets the retried_execution of this PipelineExecutionSummary.


        :param retried_execution: The retried_execution of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._retried_execution = retried_execution

    @property
    def retry_execution_metadata(self):
        """Gets the retry_execution_metadata of this PipelineExecutionSummary.  # noqa: E501


        :return: The retry_execution_metadata of this PipelineExecutionSummary.  # noqa: E501
        :rtype: RetryExecutionMetadata
        """
        return self._retry_execution_metadata

    @retry_execution_metadata.setter
    def retry_execution_metadata(self, retry_execution_metadata):
        """Sets the retry_execution_metadata of this PipelineExecutionSummary.


        :param retry_execution_metadata: The retry_execution_metadata of this PipelineExecutionSummary.  # noqa: E501
        :type: RetryExecutionMetadata
        """

        self._retry_execution_metadata = retry_execution_metadata

    @property
    def run_sequence(self):
        """Gets the run_sequence of this PipelineExecutionSummary.  # noqa: E501


        :return: The run_sequence of this PipelineExecutionSummary.  # noqa: E501
        :rtype: int
        """
        return self._run_sequence

    @run_sequence.setter
    def run_sequence(self, run_sequence):
        """Sets the run_sequence of this PipelineExecutionSummary.


        :param run_sequence: The run_sequence of this PipelineExecutionSummary.  # noqa: E501
        :type: int
        """

        self._run_sequence = run_sequence

    @property
    def running_stages_count(self):
        """Gets the running_stages_count of this PipelineExecutionSummary.  # noqa: E501


        :return: The running_stages_count of this PipelineExecutionSummary.  # noqa: E501
        :rtype: int
        """
        return self._running_stages_count

    @running_stages_count.setter
    def running_stages_count(self, running_stages_count):
        """Sets the running_stages_count of this PipelineExecutionSummary.


        :param running_stages_count: The running_stages_count of this PipelineExecutionSummary.  # noqa: E501
        :type: int
        """

        self._running_stages_count = running_stages_count

    @property
    def should_use_simplified_key(self):
        """Gets the should_use_simplified_key of this PipelineExecutionSummary.  # noqa: E501


        :return: The should_use_simplified_key of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._should_use_simplified_key

    @should_use_simplified_key.setter
    def should_use_simplified_key(self, should_use_simplified_key):
        """Sets the should_use_simplified_key of this PipelineExecutionSummary.


        :param should_use_simplified_key: The should_use_simplified_key of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._should_use_simplified_key = should_use_simplified_key

    @property
    def show_retry_history(self):
        """Gets the show_retry_history of this PipelineExecutionSummary.  # noqa: E501


        :return: The show_retry_history of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._show_retry_history

    @show_retry_history.setter
    def show_retry_history(self, show_retry_history):
        """Sets the show_retry_history of this PipelineExecutionSummary.


        :param show_retry_history: The show_retry_history of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._show_retry_history = show_retry_history

    @property
    def stages_executed(self):
        """Gets the stages_executed of this PipelineExecutionSummary.  # noqa: E501


        :return: The stages_executed of this PipelineExecutionSummary.  # noqa: E501
        :rtype: list[str]
        """
        return self._stages_executed

    @stages_executed.setter
    def stages_executed(self, stages_executed):
        """Sets the stages_executed of this PipelineExecutionSummary.


        :param stages_executed: The stages_executed of this PipelineExecutionSummary.  # noqa: E501
        :type: list[str]
        """

        self._stages_executed = stages_executed

    @property
    def stages_executed_names(self):
        """Gets the stages_executed_names of this PipelineExecutionSummary.  # noqa: E501


        :return: The stages_executed_names of this PipelineExecutionSummary.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._stages_executed_names

    @stages_executed_names.setter
    def stages_executed_names(self, stages_executed_names):
        """Sets the stages_executed_names of this PipelineExecutionSummary.


        :param stages_executed_names: The stages_executed_names of this PipelineExecutionSummary.  # noqa: E501
        :type: dict(str, str)
        """

        self._stages_executed_names = stages_executed_names

    @property
    def stages_execution(self):
        """Gets the stages_execution of this PipelineExecutionSummary.  # noqa: E501


        :return: The stages_execution of this PipelineExecutionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._stages_execution

    @stages_execution.setter
    def stages_execution(self, stages_execution):
        """Sets the stages_execution of this PipelineExecutionSummary.


        :param stages_execution: The stages_execution of this PipelineExecutionSummary.  # noqa: E501
        :type: bool
        """

        self._stages_execution = stages_execution

    @property
    def start_ts(self):
        """Gets the start_ts of this PipelineExecutionSummary.  # noqa: E501


        :return: The start_ts of this PipelineExecutionSummary.  # noqa: E501
        :rtype: int
        """
        return self._start_ts

    @start_ts.setter
    def start_ts(self, start_ts):
        """Sets the start_ts of this PipelineExecutionSummary.


        :param start_ts: The start_ts of this PipelineExecutionSummary.  # noqa: E501
        :type: int
        """

        self._start_ts = start_ts

    @property
    def starting_node_id(self):
        """Gets the starting_node_id of this PipelineExecutionSummary.  # noqa: E501


        :return: The starting_node_id of this PipelineExecutionSummary.  # noqa: E501
        :rtype: str
        """
        return self._starting_node_id

    @starting_node_id.setter
    def starting_node_id(self, starting_node_id):
        """Sets the starting_node_id of this PipelineExecutionSummary.


        :param starting_node_id: The starting_node_id of this PipelineExecutionSummary.  # noqa: E501
        :type: str
        """

        self._starting_node_id = starting_node_id

    @property
    def status(self):
        """Gets the status of this PipelineExecutionSummary.  # noqa: E501

        This is the Execution Status of the entity  # noqa: E501

        :return: The status of this PipelineExecutionSummary.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this PipelineExecutionSummary.

        This is the Execution Status of the entity  # noqa: E501

        :param status: The status of this PipelineExecutionSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["Running", "AsyncWaiting", "TaskWaiting", "TimedWaiting", "Failed", "Errored", "IgnoreFailed", "NotStarted", "Expired", "Aborted", "Discontinuing", "Queued", "Paused", "ResourceWaiting", "InterventionWaiting", "ApprovalWaiting", "WaitStepRunning", "QueuedLicenseLimitReached", "QueuedExecutionConcurrencyReached", "Success", "Suspended", "Skipped", "Pausing", "ApprovalRejected", "InputWaiting", "AbortedByFreeze", "UploadWaiting", "NOT_STARTED", "INTERVENTION_WAITING", "APPROVAL_WAITING", "APPROVAL_REJECTED", "Waiting", "Queued", "Queued", "Queued", "Queued"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def store_type(self):
        """Gets the store_type of this PipelineExecutionSummary.  # noqa: E501


        :return: The store_type of this PipelineExecutionSummary.  # noqa: E501
        :rtype: str
        """
        return self._store_type

    @store_type.setter
    def store_type(self, store_type):
        """Sets the store_type of this PipelineExecutionSummary.


        :param store_type: The store_type of this PipelineExecutionSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["INLINE", "REMOTE", "INLINE_HC"]  # noqa: E501
        if store_type not in allowed_values:
            raise ValueError(
                "Invalid value for `store_type` ({0}), must be one of {1}"  # noqa: E501
                .format(store_type, allowed_values)
            )

        self._store_type = store_type

    @property
    def successful_stages_count(self):
        """Gets the successful_stages_count of this PipelineExecutionSummary.  # noqa: E501


        :return: The successful_stages_count of this PipelineExecutionSummary.  # noqa: E501
        :rtype: int
        """
        return self._successful_stages_count

    @successful_stages_count.setter
    def successful_stages_count(self, successful_stages_count):
        """Sets the successful_stages_count of this PipelineExecutionSummary.


        :param successful_stages_count: The successful_stages_count of this PipelineExecutionSummary.  # noqa: E501
        :type: int
        """

        self._successful_stages_count = successful_stages_count

    @property
    def tags(self):
        """Gets the tags of this PipelineExecutionSummary.  # noqa: E501


        :return: The tags of this PipelineExecutionSummary.  # noqa: E501
        :rtype: list[NGTag]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this PipelineExecutionSummary.


        :param tags: The tags of this PipelineExecutionSummary.  # noqa: E501
        :type: list[NGTag]
        """

        self._tags = tags

    @property
    def template_reference_summary(self):
        """Gets the template_reference_summary of this PipelineExecutionSummary.  # noqa: E501


        :return: The template_reference_summary of this PipelineExecutionSummary.  # noqa: E501
        :rtype: TemplateReferenceSummary
        """
        return self._template_reference_summary

    @template_reference_summary.setter
    def template_reference_summary(self, template_reference_summary):
        """Sets the template_reference_summary of this PipelineExecutionSummary.


        :param template_reference_summary: The template_reference_summary of this PipelineExecutionSummary.  # noqa: E501
        :type: TemplateReferenceSummary
        """

        self._template_reference_summary = template_reference_summary

    @property
    def total_stages_count(self):
        """Gets the total_stages_count of this PipelineExecutionSummary.  # noqa: E501


        :return: The total_stages_count of this PipelineExecutionSummary.  # noqa: E501
        :rtype: int
        """
        return self._total_stages_count

    @total_stages_count.setter
    def total_stages_count(self, total_stages_count):
        """Sets the total_stages_count of this PipelineExecutionSummary.


        :param total_stages_count: The total_stages_count of this PipelineExecutionSummary.  # noqa: E501
        :type: int
        """

        self._total_stages_count = total_stages_count

    @property
    def yaml_version(self):
        """Gets the yaml_version of this PipelineExecutionSummary.  # noqa: E501


        :return: The yaml_version of this PipelineExecutionSummary.  # noqa: E501
        :rtype: str
        """
        return self._yaml_version

    @yaml_version.setter
    def yaml_version(self, yaml_version):
        """Sets the yaml_version of this PipelineExecutionSummary.


        :param yaml_version: The yaml_version of this PipelineExecutionSummary.  # noqa: E501
        :type: str
        """

        self._yaml_version = yaml_version

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
        if issubclass(PipelineExecutionSummary, dict):
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
        if not isinstance(other, PipelineExecutionSummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
