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

class InfrastructureExecution(object):
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
        'approvals': 'list[InstanceApproval]',
        'completed_instance_ids': 'list[str]',
        'events': 'list[ExecutionEvent]',
        'id': 'str',
        'infrastructure_id': 'str',
        'instance_ids': 'list[str]',
        'message': 'str',
        'outputs': 'dict(str, ExecutionOutput)',
        'pipeline_url': 'str',
        'progress': 'InfrastructureProgress',
        'spec': 'Infrastructure1',
        'spec_revision': 'int',
        'started_at': 'str',
        'stopped_at': 'str',
        'target_state': 'State'
    }

    attribute_map = {
        'approvals': 'approvals',
        'completed_instance_ids': 'completedInstanceIds',
        'events': 'events',
        'id': 'id',
        'infrastructure_id': 'infrastructureId',
        'instance_ids': 'instanceIds',
        'message': 'message',
        'outputs': 'outputs',
        'pipeline_url': 'pipelineUrl',
        'progress': 'progress',
        'spec': 'spec',
        'spec_revision': 'specRevision',
        'started_at': 'startedAt',
        'stopped_at': 'stoppedAt',
        'target_state': 'targetState'
    }

    def __init__(self, approvals=None, completed_instance_ids=None, events=None, id=None, infrastructure_id=None, instance_ids=None, message=None, outputs=None, pipeline_url=None, progress=None, spec=None, spec_revision=None, started_at=None, stopped_at=None, target_state=None):  # noqa: E501
        """InfrastructureExecution - a model defined in Swagger"""  # noqa: E501
        self._approvals = None
        self._completed_instance_ids = None
        self._events = None
        self._id = None
        self._infrastructure_id = None
        self._instance_ids = None
        self._message = None
        self._outputs = None
        self._pipeline_url = None
        self._progress = None
        self._spec = None
        self._spec_revision = None
        self._started_at = None
        self._stopped_at = None
        self._target_state = None
        self.discriminator = None
        if approvals is not None:
            self.approvals = approvals
        self.completed_instance_ids = completed_instance_ids
        if events is not None:
            self.events = events
        self.id = id
        self.infrastructure_id = infrastructure_id
        self.instance_ids = instance_ids
        if message is not None:
            self.message = message
        if outputs is not None:
            self.outputs = outputs
        if pipeline_url is not None:
            self.pipeline_url = pipeline_url
        self.progress = progress
        self.spec = spec
        self.spec_revision = spec_revision
        self.started_at = started_at
        if stopped_at is not None:
            self.stopped_at = stopped_at
        self.target_state = target_state

    @property
    def approvals(self):
        """Gets the approvals of this InfrastructureExecution.  # noqa: E501


        :return: The approvals of this InfrastructureExecution.  # noqa: E501
        :rtype: list[InstanceApproval]
        """
        return self._approvals

    @approvals.setter
    def approvals(self, approvals):
        """Sets the approvals of this InfrastructureExecution.


        :param approvals: The approvals of this InfrastructureExecution.  # noqa: E501
        :type: list[InstanceApproval]
        """

        self._approvals = approvals

    @property
    def completed_instance_ids(self):
        """Gets the completed_instance_ids of this InfrastructureExecution.  # noqa: E501

        Instances fully updated by the execution  # noqa: E501

        :return: The completed_instance_ids of this InfrastructureExecution.  # noqa: E501
        :rtype: list[str]
        """
        return self._completed_instance_ids

    @completed_instance_ids.setter
    def completed_instance_ids(self, completed_instance_ids):
        """Sets the completed_instance_ids of this InfrastructureExecution.

        Instances fully updated by the execution  # noqa: E501

        :param completed_instance_ids: The completed_instance_ids of this InfrastructureExecution.  # noqa: E501
        :type: list[str]
        """
        if completed_instance_ids is None:
            raise ValueError("Invalid value for `completed_instance_ids`, must not be `None`")  # noqa: E501

        self._completed_instance_ids = completed_instance_ids

    @property
    def events(self):
        """Gets the events of this InfrastructureExecution.  # noqa: E501


        :return: The events of this InfrastructureExecution.  # noqa: E501
        :rtype: list[ExecutionEvent]
        """
        return self._events

    @events.setter
    def events(self, events):
        """Sets the events of this InfrastructureExecution.


        :param events: The events of this InfrastructureExecution.  # noqa: E501
        :type: list[ExecutionEvent]
        """

        self._events = events

    @property
    def id(self):
        """Gets the id of this InfrastructureExecution.  # noqa: E501


        :return: The id of this InfrastructureExecution.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InfrastructureExecution.


        :param id: The id of this InfrastructureExecution.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def infrastructure_id(self):
        """Gets the infrastructure_id of this InfrastructureExecution.  # noqa: E501


        :return: The infrastructure_id of this InfrastructureExecution.  # noqa: E501
        :rtype: str
        """
        return self._infrastructure_id

    @infrastructure_id.setter
    def infrastructure_id(self, infrastructure_id):
        """Sets the infrastructure_id of this InfrastructureExecution.


        :param infrastructure_id: The infrastructure_id of this InfrastructureExecution.  # noqa: E501
        :type: str
        """
        if infrastructure_id is None:
            raise ValueError("Invalid value for `infrastructure_id`, must not be `None`")  # noqa: E501

        self._infrastructure_id = infrastructure_id

    @property
    def instance_ids(self):
        """Gets the instance_ids of this InfrastructureExecution.  # noqa: E501

        Instances updated by the execution  # noqa: E501

        :return: The instance_ids of this InfrastructureExecution.  # noqa: E501
        :rtype: list[str]
        """
        return self._instance_ids

    @instance_ids.setter
    def instance_ids(self, instance_ids):
        """Sets the instance_ids of this InfrastructureExecution.

        Instances updated by the execution  # noqa: E501

        :param instance_ids: The instance_ids of this InfrastructureExecution.  # noqa: E501
        :type: list[str]
        """
        if instance_ids is None:
            raise ValueError("Invalid value for `instance_ids`, must not be `None`")  # noqa: E501

        self._instance_ids = instance_ids

    @property
    def message(self):
        """Gets the message of this InfrastructureExecution.  # noqa: E501

        Message associated with the execution  # noqa: E501

        :return: The message of this InfrastructureExecution.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this InfrastructureExecution.

        Message associated with the execution  # noqa: E501

        :param message: The message of this InfrastructureExecution.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def outputs(self):
        """Gets the outputs of this InfrastructureExecution.  # noqa: E501

        Outputs of the infrastructure execution  # noqa: E501

        :return: The outputs of this InfrastructureExecution.  # noqa: E501
        :rtype: dict(str, ExecutionOutput)
        """
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        """Sets the outputs of this InfrastructureExecution.

        Outputs of the infrastructure execution  # noqa: E501

        :param outputs: The outputs of this InfrastructureExecution.  # noqa: E501
        :type: dict(str, ExecutionOutput)
        """

        self._outputs = outputs

    @property
    def pipeline_url(self):
        """Gets the pipeline_url of this InfrastructureExecution.  # noqa: E501


        :return: The pipeline_url of this InfrastructureExecution.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_url

    @pipeline_url.setter
    def pipeline_url(self, pipeline_url):
        """Sets the pipeline_url of this InfrastructureExecution.


        :param pipeline_url: The pipeline_url of this InfrastructureExecution.  # noqa: E501
        :type: str
        """

        self._pipeline_url = pipeline_url

    @property
    def progress(self):
        """Gets the progress of this InfrastructureExecution.  # noqa: E501


        :return: The progress of this InfrastructureExecution.  # noqa: E501
        :rtype: InfrastructureProgress
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """Sets the progress of this InfrastructureExecution.


        :param progress: The progress of this InfrastructureExecution.  # noqa: E501
        :type: InfrastructureProgress
        """
        if progress is None:
            raise ValueError("Invalid value for `progress`, must not be `None`")  # noqa: E501

        self._progress = progress

    @property
    def spec(self):
        """Gets the spec of this InfrastructureExecution.  # noqa: E501


        :return: The spec of this InfrastructureExecution.  # noqa: E501
        :rtype: Infrastructure1
        """
        return self._spec

    @spec.setter
    def spec(self, spec):
        """Sets the spec of this InfrastructureExecution.


        :param spec: The spec of this InfrastructureExecution.  # noqa: E501
        :type: Infrastructure1
        """
        if spec is None:
            raise ValueError("Invalid value for `spec`, must not be `None`")  # noqa: E501

        self._spec = spec

    @property
    def spec_revision(self):
        """Gets the spec_revision of this InfrastructureExecution.  # noqa: E501


        :return: The spec_revision of this InfrastructureExecution.  # noqa: E501
        :rtype: int
        """
        return self._spec_revision

    @spec_revision.setter
    def spec_revision(self, spec_revision):
        """Sets the spec_revision of this InfrastructureExecution.


        :param spec_revision: The spec_revision of this InfrastructureExecution.  # noqa: E501
        :type: int
        """
        if spec_revision is None:
            raise ValueError("Invalid value for `spec_revision`, must not be `None`")  # noqa: E501

        self._spec_revision = spec_revision

    @property
    def started_at(self):
        """Gets the started_at of this InfrastructureExecution.  # noqa: E501


        :return: The started_at of this InfrastructureExecution.  # noqa: E501
        :rtype: str
        """
        return self._started_at

    @started_at.setter
    def started_at(self, started_at):
        """Sets the started_at of this InfrastructureExecution.


        :param started_at: The started_at of this InfrastructureExecution.  # noqa: E501
        :type: str
        """
        if started_at is None:
            raise ValueError("Invalid value for `started_at`, must not be `None`")  # noqa: E501

        self._started_at = started_at

    @property
    def stopped_at(self):
        """Gets the stopped_at of this InfrastructureExecution.  # noqa: E501


        :return: The stopped_at of this InfrastructureExecution.  # noqa: E501
        :rtype: str
        """
        return self._stopped_at

    @stopped_at.setter
    def stopped_at(self, stopped_at):
        """Sets the stopped_at of this InfrastructureExecution.


        :param stopped_at: The stopped_at of this InfrastructureExecution.  # noqa: E501
        :type: str
        """

        self._stopped_at = stopped_at

    @property
    def target_state(self):
        """Gets the target_state of this InfrastructureExecution.  # noqa: E501


        :return: The target_state of this InfrastructureExecution.  # noqa: E501
        :rtype: State
        """
        return self._target_state

    @target_state.setter
    def target_state(self, target_state):
        """Sets the target_state of this InfrastructureExecution.


        :param target_state: The target_state of this InfrastructureExecution.  # noqa: E501
        :type: State
        """
        if target_state is None:
            raise ValueError("Invalid value for `target_state`, must not be `None`")  # noqa: E501

        self._target_state = target_state

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
        if issubclass(InfrastructureExecution, dict):
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
        if not isinstance(other, InfrastructureExecution):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
