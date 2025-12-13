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

class PipelineExecutionOutline(object):
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
        'account_identifier': 'str',
        'created_at': 'int',
        'end_ts': 'int',
        'failure_info': 'str',
        'last_updated_at': 'int',
        'modules': 'list[str]',
        'name': 'str',
        'org_identifier': 'str',
        'pipeline_identifier': 'str',
        'plan_execution_id': 'str',
        'project_identifier': 'str',
        'run_sequence': 'int',
        'runtime_input_yaml': 'str',
        'stages_map': 'dict(str, NodeExecutionOutline)',
        'start_ts': 'int',
        'starting_node_id': 'str',
        'status': 'str'
    }

    attribute_map = {
        'account_identifier': 'accountIdentifier',
        'created_at': 'createdAt',
        'end_ts': 'endTs',
        'failure_info': 'failureInfo',
        'last_updated_at': 'lastUpdatedAt',
        'modules': 'modules',
        'name': 'name',
        'org_identifier': 'orgIdentifier',
        'pipeline_identifier': 'pipelineIdentifier',
        'plan_execution_id': 'planExecutionId',
        'project_identifier': 'projectIdentifier',
        'run_sequence': 'runSequence',
        'runtime_input_yaml': 'runtimeInputYaml',
        'stages_map': 'stagesMap',
        'start_ts': 'startTs',
        'starting_node_id': 'startingNodeId',
        'status': 'status'
    }

    def __init__(self, account_identifier=None, created_at=None, end_ts=None, failure_info=None, last_updated_at=None, modules=None, name=None, org_identifier=None, pipeline_identifier=None, plan_execution_id=None, project_identifier=None, run_sequence=None, runtime_input_yaml=None, stages_map=None, start_ts=None, starting_node_id=None, status=None):  # noqa: E501
        """PipelineExecutionOutline - a model defined in Swagger"""  # noqa: E501
        self._account_identifier = None
        self._created_at = None
        self._end_ts = None
        self._failure_info = None
        self._last_updated_at = None
        self._modules = None
        self._name = None
        self._org_identifier = None
        self._pipeline_identifier = None
        self._plan_execution_id = None
        self._project_identifier = None
        self._run_sequence = None
        self._runtime_input_yaml = None
        self._stages_map = None
        self._start_ts = None
        self._starting_node_id = None
        self._status = None
        self.discriminator = None
        self.account_identifier = account_identifier
        if created_at is not None:
            self.created_at = created_at
        if end_ts is not None:
            self.end_ts = end_ts
        if failure_info is not None:
            self.failure_info = failure_info
        if last_updated_at is not None:
            self.last_updated_at = last_updated_at
        if modules is not None:
            self.modules = modules
        if name is not None:
            self.name = name
        self.org_identifier = org_identifier
        if pipeline_identifier is not None:
            self.pipeline_identifier = pipeline_identifier
        if plan_execution_id is not None:
            self.plan_execution_id = plan_execution_id
        self.project_identifier = project_identifier
        if run_sequence is not None:
            self.run_sequence = run_sequence
        if runtime_input_yaml is not None:
            self.runtime_input_yaml = runtime_input_yaml
        if stages_map is not None:
            self.stages_map = stages_map
        if start_ts is not None:
            self.start_ts = start_ts
        if starting_node_id is not None:
            self.starting_node_id = starting_node_id
        if status is not None:
            self.status = status

    @property
    def account_identifier(self):
        """Gets the account_identifier of this PipelineExecutionOutline.  # noqa: E501


        :return: The account_identifier of this PipelineExecutionOutline.  # noqa: E501
        :rtype: str
        """
        return self._account_identifier

    @account_identifier.setter
    def account_identifier(self, account_identifier):
        """Sets the account_identifier of this PipelineExecutionOutline.


        :param account_identifier: The account_identifier of this PipelineExecutionOutline.  # noqa: E501
        :type: str
        """
        if account_identifier is None:
            raise ValueError("Invalid value for `account_identifier`, must not be `None`")  # noqa: E501

        self._account_identifier = account_identifier

    @property
    def created_at(self):
        """Gets the created_at of this PipelineExecutionOutline.  # noqa: E501


        :return: The created_at of this PipelineExecutionOutline.  # noqa: E501
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this PipelineExecutionOutline.


        :param created_at: The created_at of this PipelineExecutionOutline.  # noqa: E501
        :type: int
        """

        self._created_at = created_at

    @property
    def end_ts(self):
        """Gets the end_ts of this PipelineExecutionOutline.  # noqa: E501


        :return: The end_ts of this PipelineExecutionOutline.  # noqa: E501
        :rtype: int
        """
        return self._end_ts

    @end_ts.setter
    def end_ts(self, end_ts):
        """Sets the end_ts of this PipelineExecutionOutline.


        :param end_ts: The end_ts of this PipelineExecutionOutline.  # noqa: E501
        :type: int
        """

        self._end_ts = end_ts

    @property
    def failure_info(self):
        """Gets the failure_info of this PipelineExecutionOutline.  # noqa: E501


        :return: The failure_info of this PipelineExecutionOutline.  # noqa: E501
        :rtype: str
        """
        return self._failure_info

    @failure_info.setter
    def failure_info(self, failure_info):
        """Sets the failure_info of this PipelineExecutionOutline.


        :param failure_info: The failure_info of this PipelineExecutionOutline.  # noqa: E501
        :type: str
        """

        self._failure_info = failure_info

    @property
    def last_updated_at(self):
        """Gets the last_updated_at of this PipelineExecutionOutline.  # noqa: E501


        :return: The last_updated_at of this PipelineExecutionOutline.  # noqa: E501
        :rtype: int
        """
        return self._last_updated_at

    @last_updated_at.setter
    def last_updated_at(self, last_updated_at):
        """Sets the last_updated_at of this PipelineExecutionOutline.


        :param last_updated_at: The last_updated_at of this PipelineExecutionOutline.  # noqa: E501
        :type: int
        """

        self._last_updated_at = last_updated_at

    @property
    def modules(self):
        """Gets the modules of this PipelineExecutionOutline.  # noqa: E501


        :return: The modules of this PipelineExecutionOutline.  # noqa: E501
        :rtype: list[str]
        """
        return self._modules

    @modules.setter
    def modules(self, modules):
        """Sets the modules of this PipelineExecutionOutline.


        :param modules: The modules of this PipelineExecutionOutline.  # noqa: E501
        :type: list[str]
        """

        self._modules = modules

    @property
    def name(self):
        """Gets the name of this PipelineExecutionOutline.  # noqa: E501


        :return: The name of this PipelineExecutionOutline.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PipelineExecutionOutline.


        :param name: The name of this PipelineExecutionOutline.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def org_identifier(self):
        """Gets the org_identifier of this PipelineExecutionOutline.  # noqa: E501


        :return: The org_identifier of this PipelineExecutionOutline.  # noqa: E501
        :rtype: str
        """
        return self._org_identifier

    @org_identifier.setter
    def org_identifier(self, org_identifier):
        """Sets the org_identifier of this PipelineExecutionOutline.


        :param org_identifier: The org_identifier of this PipelineExecutionOutline.  # noqa: E501
        :type: str
        """
        if org_identifier is None:
            raise ValueError("Invalid value for `org_identifier`, must not be `None`")  # noqa: E501

        self._org_identifier = org_identifier

    @property
    def pipeline_identifier(self):
        """Gets the pipeline_identifier of this PipelineExecutionOutline.  # noqa: E501


        :return: The pipeline_identifier of this PipelineExecutionOutline.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_identifier

    @pipeline_identifier.setter
    def pipeline_identifier(self, pipeline_identifier):
        """Sets the pipeline_identifier of this PipelineExecutionOutline.


        :param pipeline_identifier: The pipeline_identifier of this PipelineExecutionOutline.  # noqa: E501
        :type: str
        """

        self._pipeline_identifier = pipeline_identifier

    @property
    def plan_execution_id(self):
        """Gets the plan_execution_id of this PipelineExecutionOutline.  # noqa: E501


        :return: The plan_execution_id of this PipelineExecutionOutline.  # noqa: E501
        :rtype: str
        """
        return self._plan_execution_id

    @plan_execution_id.setter
    def plan_execution_id(self, plan_execution_id):
        """Sets the plan_execution_id of this PipelineExecutionOutline.


        :param plan_execution_id: The plan_execution_id of this PipelineExecutionOutline.  # noqa: E501
        :type: str
        """

        self._plan_execution_id = plan_execution_id

    @property
    def project_identifier(self):
        """Gets the project_identifier of this PipelineExecutionOutline.  # noqa: E501


        :return: The project_identifier of this PipelineExecutionOutline.  # noqa: E501
        :rtype: str
        """
        return self._project_identifier

    @project_identifier.setter
    def project_identifier(self, project_identifier):
        """Sets the project_identifier of this PipelineExecutionOutline.


        :param project_identifier: The project_identifier of this PipelineExecutionOutline.  # noqa: E501
        :type: str
        """
        if project_identifier is None:
            raise ValueError("Invalid value for `project_identifier`, must not be `None`")  # noqa: E501

        self._project_identifier = project_identifier

    @property
    def run_sequence(self):
        """Gets the run_sequence of this PipelineExecutionOutline.  # noqa: E501


        :return: The run_sequence of this PipelineExecutionOutline.  # noqa: E501
        :rtype: int
        """
        return self._run_sequence

    @run_sequence.setter
    def run_sequence(self, run_sequence):
        """Sets the run_sequence of this PipelineExecutionOutline.


        :param run_sequence: The run_sequence of this PipelineExecutionOutline.  # noqa: E501
        :type: int
        """

        self._run_sequence = run_sequence

    @property
    def runtime_input_yaml(self):
        """Gets the runtime_input_yaml of this PipelineExecutionOutline.  # noqa: E501


        :return: The runtime_input_yaml of this PipelineExecutionOutline.  # noqa: E501
        :rtype: str
        """
        return self._runtime_input_yaml

    @runtime_input_yaml.setter
    def runtime_input_yaml(self, runtime_input_yaml):
        """Sets the runtime_input_yaml of this PipelineExecutionOutline.


        :param runtime_input_yaml: The runtime_input_yaml of this PipelineExecutionOutline.  # noqa: E501
        :type: str
        """

        self._runtime_input_yaml = runtime_input_yaml

    @property
    def stages_map(self):
        """Gets the stages_map of this PipelineExecutionOutline.  # noqa: E501


        :return: The stages_map of this PipelineExecutionOutline.  # noqa: E501
        :rtype: dict(str, NodeExecutionOutline)
        """
        return self._stages_map

    @stages_map.setter
    def stages_map(self, stages_map):
        """Sets the stages_map of this PipelineExecutionOutline.


        :param stages_map: The stages_map of this PipelineExecutionOutline.  # noqa: E501
        :type: dict(str, NodeExecutionOutline)
        """

        self._stages_map = stages_map

    @property
    def start_ts(self):
        """Gets the start_ts of this PipelineExecutionOutline.  # noqa: E501


        :return: The start_ts of this PipelineExecutionOutline.  # noqa: E501
        :rtype: int
        """
        return self._start_ts

    @start_ts.setter
    def start_ts(self, start_ts):
        """Sets the start_ts of this PipelineExecutionOutline.


        :param start_ts: The start_ts of this PipelineExecutionOutline.  # noqa: E501
        :type: int
        """

        self._start_ts = start_ts

    @property
    def starting_node_id(self):
        """Gets the starting_node_id of this PipelineExecutionOutline.  # noqa: E501


        :return: The starting_node_id of this PipelineExecutionOutline.  # noqa: E501
        :rtype: str
        """
        return self._starting_node_id

    @starting_node_id.setter
    def starting_node_id(self, starting_node_id):
        """Sets the starting_node_id of this PipelineExecutionOutline.


        :param starting_node_id: The starting_node_id of this PipelineExecutionOutline.  # noqa: E501
        :type: str
        """

        self._starting_node_id = starting_node_id

    @property
    def status(self):
        """Gets the status of this PipelineExecutionOutline.  # noqa: E501

        This is the Execution Status of the entity  # noqa: E501

        :return: The status of this PipelineExecutionOutline.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this PipelineExecutionOutline.

        This is the Execution Status of the entity  # noqa: E501

        :param status: The status of this PipelineExecutionOutline.  # noqa: E501
        :type: str
        """
        allowed_values = ["Running", "AsyncWaiting", "TaskWaiting", "TimedWaiting", "Failed", "Errored", "IgnoreFailed", "NotStarted", "Expired", "Aborted", "Discontinuing", "Queued", "Paused", "ResourceWaiting", "InterventionWaiting", "ApprovalWaiting", "WaitStepRunning", "QueuedLicenseLimitReached", "QueuedExecutionConcurrencyReached", "Success", "Suspended", "Skipped", "Pausing", "ApprovalRejected", "InputWaiting", "AbortedByFreeze", "UploadWaiting", "NOT_STARTED", "INTERVENTION_WAITING", "APPROVAL_WAITING", "APPROVAL_REJECTED", "Waiting", "Queued", "Queued", "Queued", "Queued"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

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
        if issubclass(PipelineExecutionOutline, dict):
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
        if not isinstance(other, PipelineExecutionOutline):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
