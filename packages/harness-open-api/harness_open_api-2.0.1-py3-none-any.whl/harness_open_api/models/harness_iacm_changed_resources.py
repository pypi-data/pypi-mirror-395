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

class HarnessIacmChangedResources(object):
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
        'data_sources': 'ResourceCollection',
        'drift_changes': 'ChangedResourceCollection',
        'outputs': 'OutputCollection2',
        'pipeline_execution': 'str',
        'pipeline_stage': 'str',
        'planned_changes': 'ChangedResourceCollection',
        'resources': 'ResourceCollection',
        'stage_id': 'str',
        'workspace_id': 'str'
    }

    attribute_map = {
        'data_sources': 'data_sources',
        'drift_changes': 'drift_changes',
        'outputs': 'outputs',
        'pipeline_execution': 'pipeline_execution',
        'pipeline_stage': 'pipeline_stage',
        'planned_changes': 'planned_changes',
        'resources': 'resources',
        'stage_id': 'stage_id',
        'workspace_id': 'workspace_id'
    }

    def __init__(self, data_sources=None, drift_changes=None, outputs=None, pipeline_execution=None, pipeline_stage=None, planned_changes=None, resources=None, stage_id=None, workspace_id=None):  # noqa: E501
        """HarnessIacmChangedResources - a model defined in Swagger"""  # noqa: E501
        self._data_sources = None
        self._drift_changes = None
        self._outputs = None
        self._pipeline_execution = None
        self._pipeline_stage = None
        self._planned_changes = None
        self._resources = None
        self._stage_id = None
        self._workspace_id = None
        self.discriminator = None
        self.data_sources = data_sources
        self.drift_changes = drift_changes
        self.outputs = outputs
        self.pipeline_execution = pipeline_execution
        if pipeline_stage is not None:
            self.pipeline_stage = pipeline_stage
        self.planned_changes = planned_changes
        self.resources = resources
        self.stage_id = stage_id
        self.workspace_id = workspace_id

    @property
    def data_sources(self):
        """Gets the data_sources of this HarnessIacmChangedResources.  # noqa: E501


        :return: The data_sources of this HarnessIacmChangedResources.  # noqa: E501
        :rtype: ResourceCollection
        """
        return self._data_sources

    @data_sources.setter
    def data_sources(self, data_sources):
        """Sets the data_sources of this HarnessIacmChangedResources.


        :param data_sources: The data_sources of this HarnessIacmChangedResources.  # noqa: E501
        :type: ResourceCollection
        """
        if data_sources is None:
            raise ValueError("Invalid value for `data_sources`, must not be `None`")  # noqa: E501

        self._data_sources = data_sources

    @property
    def drift_changes(self):
        """Gets the drift_changes of this HarnessIacmChangedResources.  # noqa: E501


        :return: The drift_changes of this HarnessIacmChangedResources.  # noqa: E501
        :rtype: ChangedResourceCollection
        """
        return self._drift_changes

    @drift_changes.setter
    def drift_changes(self, drift_changes):
        """Sets the drift_changes of this HarnessIacmChangedResources.


        :param drift_changes: The drift_changes of this HarnessIacmChangedResources.  # noqa: E501
        :type: ChangedResourceCollection
        """
        if drift_changes is None:
            raise ValueError("Invalid value for `drift_changes`, must not be `None`")  # noqa: E501

        self._drift_changes = drift_changes

    @property
    def outputs(self):
        """Gets the outputs of this HarnessIacmChangedResources.  # noqa: E501


        :return: The outputs of this HarnessIacmChangedResources.  # noqa: E501
        :rtype: OutputCollection2
        """
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        """Sets the outputs of this HarnessIacmChangedResources.


        :param outputs: The outputs of this HarnessIacmChangedResources.  # noqa: E501
        :type: OutputCollection2
        """
        if outputs is None:
            raise ValueError("Invalid value for `outputs`, must not be `None`")  # noqa: E501

        self._outputs = outputs

    @property
    def pipeline_execution(self):
        """Gets the pipeline_execution of this HarnessIacmChangedResources.  # noqa: E501

        the identifier of the pipeline execution changes were made from.  # noqa: E501

        :return: The pipeline_execution of this HarnessIacmChangedResources.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_execution

    @pipeline_execution.setter
    def pipeline_execution(self, pipeline_execution):
        """Sets the pipeline_execution of this HarnessIacmChangedResources.

        the identifier of the pipeline execution changes were made from.  # noqa: E501

        :param pipeline_execution: The pipeline_execution of this HarnessIacmChangedResources.  # noqa: E501
        :type: str
        """
        if pipeline_execution is None:
            raise ValueError("Invalid value for `pipeline_execution`, must not be `None`")  # noqa: E501

        self._pipeline_execution = pipeline_execution

    @property
    def pipeline_stage(self):
        """Gets the pipeline_stage of this HarnessIacmChangedResources.  # noqa: E501

        the identifier of the pipeline stage execution changes were made from.  # noqa: E501

        :return: The pipeline_stage of this HarnessIacmChangedResources.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_stage

    @pipeline_stage.setter
    def pipeline_stage(self, pipeline_stage):
        """Sets the pipeline_stage of this HarnessIacmChangedResources.

        the identifier of the pipeline stage execution changes were made from.  # noqa: E501

        :param pipeline_stage: The pipeline_stage of this HarnessIacmChangedResources.  # noqa: E501
        :type: str
        """

        self._pipeline_stage = pipeline_stage

    @property
    def planned_changes(self):
        """Gets the planned_changes of this HarnessIacmChangedResources.  # noqa: E501


        :return: The planned_changes of this HarnessIacmChangedResources.  # noqa: E501
        :rtype: ChangedResourceCollection
        """
        return self._planned_changes

    @planned_changes.setter
    def planned_changes(self, planned_changes):
        """Sets the planned_changes of this HarnessIacmChangedResources.


        :param planned_changes: The planned_changes of this HarnessIacmChangedResources.  # noqa: E501
        :type: ChangedResourceCollection
        """
        if planned_changes is None:
            raise ValueError("Invalid value for `planned_changes`, must not be `None`")  # noqa: E501

        self._planned_changes = planned_changes

    @property
    def resources(self):
        """Gets the resources of this HarnessIacmChangedResources.  # noqa: E501


        :return: The resources of this HarnessIacmChangedResources.  # noqa: E501
        :rtype: ResourceCollection
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this HarnessIacmChangedResources.


        :param resources: The resources of this HarnessIacmChangedResources.  # noqa: E501
        :type: ResourceCollection
        """
        if resources is None:
            raise ValueError("Invalid value for `resources`, must not be `None`")  # noqa: E501

        self._resources = resources

    @property
    def stage_id(self):
        """Gets the stage_id of this HarnessIacmChangedResources.  # noqa: E501

        The stage ID  # noqa: E501

        :return: The stage_id of this HarnessIacmChangedResources.  # noqa: E501
        :rtype: str
        """
        return self._stage_id

    @stage_id.setter
    def stage_id(self, stage_id):
        """Sets the stage_id of this HarnessIacmChangedResources.

        The stage ID  # noqa: E501

        :param stage_id: The stage_id of this HarnessIacmChangedResources.  # noqa: E501
        :type: str
        """
        if stage_id is None:
            raise ValueError("Invalid value for `stage_id`, must not be `None`")  # noqa: E501

        self._stage_id = stage_id

    @property
    def workspace_id(self):
        """Gets the workspace_id of this HarnessIacmChangedResources.  # noqa: E501

        identifier of the workspace associated with the data  # noqa: E501

        :return: The workspace_id of this HarnessIacmChangedResources.  # noqa: E501
        :rtype: str
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id):
        """Sets the workspace_id of this HarnessIacmChangedResources.

        identifier of the workspace associated with the data  # noqa: E501

        :param workspace_id: The workspace_id of this HarnessIacmChangedResources.  # noqa: E501
        :type: str
        """
        if workspace_id is None:
            raise ValueError("Invalid value for `workspace_id`, must not be `None`")  # noqa: E501

        self._workspace_id = workspace_id

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
        if issubclass(HarnessIacmChangedResources, dict):
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
        if not isinstance(other, HarnessIacmChangedResources):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
