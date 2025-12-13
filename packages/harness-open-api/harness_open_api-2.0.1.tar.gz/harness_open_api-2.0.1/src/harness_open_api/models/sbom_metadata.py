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

class SbomMetadata(object):
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
        'build_url': 'str',
        'format': 'str',
        'pipeline_execution_id': 'str',
        'pipeline_identifier': 'str',
        'sequence_id': 'str',
        'stage_execution_id': 'str',
        'stage_identifier': 'str',
        'stage_name': 'str',
        'step_execution_id': 'str',
        'step_identifier': 'str',
        'step_name': 'str',
        'tool': 'str'
    }

    attribute_map = {
        'build_url': 'build_url',
        'format': 'format',
        'pipeline_execution_id': 'pipeline_execution_id',
        'pipeline_identifier': 'pipeline_identifier',
        'sequence_id': 'sequence_id',
        'stage_execution_id': 'stage_execution_id',
        'stage_identifier': 'stage_identifier',
        'stage_name': 'stage_name',
        'step_execution_id': 'step_execution_id',
        'step_identifier': 'step_identifier',
        'step_name': 'step_name',
        'tool': 'tool'
    }

    def __init__(self, build_url=None, format=None, pipeline_execution_id=None, pipeline_identifier=None, sequence_id=None, stage_execution_id=None, stage_identifier=None, stage_name=None, step_execution_id=None, step_identifier=None, step_name=None, tool=None):  # noqa: E501
        """SbomMetadata - a model defined in Swagger"""  # noqa: E501
        self._build_url = None
        self._format = None
        self._pipeline_execution_id = None
        self._pipeline_identifier = None
        self._sequence_id = None
        self._stage_execution_id = None
        self._stage_identifier = None
        self._stage_name = None
        self._step_execution_id = None
        self._step_identifier = None
        self._step_name = None
        self._tool = None
        self.discriminator = None
        if build_url is not None:
            self.build_url = build_url
        self.format = format
        self.pipeline_execution_id = pipeline_execution_id
        self.pipeline_identifier = pipeline_identifier
        if sequence_id is not None:
            self.sequence_id = sequence_id
        if stage_execution_id is not None:
            self.stage_execution_id = stage_execution_id
        self.stage_identifier = stage_identifier
        if stage_name is not None:
            self.stage_name = stage_name
        self.step_execution_id = step_execution_id
        self.step_identifier = step_identifier
        if step_name is not None:
            self.step_name = step_name
        self.tool = tool

    @property
    def build_url(self):
        """Gets the build_url of this SbomMetadata.  # noqa: E501

        BuildURL  # noqa: E501

        :return: The build_url of this SbomMetadata.  # noqa: E501
        :rtype: str
        """
        return self._build_url

    @build_url.setter
    def build_url(self, build_url):
        """Sets the build_url of this SbomMetadata.

        BuildURL  # noqa: E501

        :param build_url: The build_url of this SbomMetadata.  # noqa: E501
        :type: str
        """

        self._build_url = build_url

    @property
    def format(self):
        """Gets the format of this SbomMetadata.  # noqa: E501

        stage name where sbom is generated  # noqa: E501

        :return: The format of this SbomMetadata.  # noqa: E501
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """Sets the format of this SbomMetadata.

        stage name where sbom is generated  # noqa: E501

        :param format: The format of this SbomMetadata.  # noqa: E501
        :type: str
        """
        if format is None:
            raise ValueError("Invalid value for `format`, must not be `None`")  # noqa: E501

        self._format = format

    @property
    def pipeline_execution_id(self):
        """Gets the pipeline_execution_id of this SbomMetadata.  # noqa: E501

        name of the package  # noqa: E501

        :return: The pipeline_execution_id of this SbomMetadata.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_execution_id

    @pipeline_execution_id.setter
    def pipeline_execution_id(self, pipeline_execution_id):
        """Sets the pipeline_execution_id of this SbomMetadata.

        name of the package  # noqa: E501

        :param pipeline_execution_id: The pipeline_execution_id of this SbomMetadata.  # noqa: E501
        :type: str
        """
        if pipeline_execution_id is None:
            raise ValueError("Invalid value for `pipeline_execution_id`, must not be `None`")  # noqa: E501

        self._pipeline_execution_id = pipeline_execution_id

    @property
    def pipeline_identifier(self):
        """Gets the pipeline_identifier of this SbomMetadata.  # noqa: E501

        name of the package  # noqa: E501

        :return: The pipeline_identifier of this SbomMetadata.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_identifier

    @pipeline_identifier.setter
    def pipeline_identifier(self, pipeline_identifier):
        """Sets the pipeline_identifier of this SbomMetadata.

        name of the package  # noqa: E501

        :param pipeline_identifier: The pipeline_identifier of this SbomMetadata.  # noqa: E501
        :type: str
        """
        if pipeline_identifier is None:
            raise ValueError("Invalid value for `pipeline_identifier`, must not be `None`")  # noqa: E501

        self._pipeline_identifier = pipeline_identifier

    @property
    def sequence_id(self):
        """Gets the sequence_id of this SbomMetadata.  # noqa: E501

        name of the package  # noqa: E501

        :return: The sequence_id of this SbomMetadata.  # noqa: E501
        :rtype: str
        """
        return self._sequence_id

    @sequence_id.setter
    def sequence_id(self, sequence_id):
        """Sets the sequence_id of this SbomMetadata.

        name of the package  # noqa: E501

        :param sequence_id: The sequence_id of this SbomMetadata.  # noqa: E501
        :type: str
        """

        self._sequence_id = sequence_id

    @property
    def stage_execution_id(self):
        """Gets the stage_execution_id of this SbomMetadata.  # noqa: E501


        :return: The stage_execution_id of this SbomMetadata.  # noqa: E501
        :rtype: str
        """
        return self._stage_execution_id

    @stage_execution_id.setter
    def stage_execution_id(self, stage_execution_id):
        """Sets the stage_execution_id of this SbomMetadata.


        :param stage_execution_id: The stage_execution_id of this SbomMetadata.  # noqa: E501
        :type: str
        """

        self._stage_execution_id = stage_execution_id

    @property
    def stage_identifier(self):
        """Gets the stage_identifier of this SbomMetadata.  # noqa: E501

        name of the Stage  # noqa: E501

        :return: The stage_identifier of this SbomMetadata.  # noqa: E501
        :rtype: str
        """
        return self._stage_identifier

    @stage_identifier.setter
    def stage_identifier(self, stage_identifier):
        """Sets the stage_identifier of this SbomMetadata.

        name of the Stage  # noqa: E501

        :param stage_identifier: The stage_identifier of this SbomMetadata.  # noqa: E501
        :type: str
        """
        if stage_identifier is None:
            raise ValueError("Invalid value for `stage_identifier`, must not be `None`")  # noqa: E501

        self._stage_identifier = stage_identifier

    @property
    def stage_name(self):
        """Gets the stage_name of this SbomMetadata.  # noqa: E501


        :return: The stage_name of this SbomMetadata.  # noqa: E501
        :rtype: str
        """
        return self._stage_name

    @stage_name.setter
    def stage_name(self, stage_name):
        """Sets the stage_name of this SbomMetadata.


        :param stage_name: The stage_name of this SbomMetadata.  # noqa: E501
        :type: str
        """

        self._stage_name = stage_name

    @property
    def step_execution_id(self):
        """Gets the step_execution_id of this SbomMetadata.  # noqa: E501

        StepExecutionId  # noqa: E501

        :return: The step_execution_id of this SbomMetadata.  # noqa: E501
        :rtype: str
        """
        return self._step_execution_id

    @step_execution_id.setter
    def step_execution_id(self, step_execution_id):
        """Sets the step_execution_id of this SbomMetadata.

        StepExecutionId  # noqa: E501

        :param step_execution_id: The step_execution_id of this SbomMetadata.  # noqa: E501
        :type: str
        """
        if step_execution_id is None:
            raise ValueError("Invalid value for `step_execution_id`, must not be `None`")  # noqa: E501

        self._step_execution_id = step_execution_id

    @property
    def step_identifier(self):
        """Gets the step_identifier of this SbomMetadata.  # noqa: E501

        id of the step  # noqa: E501

        :return: The step_identifier of this SbomMetadata.  # noqa: E501
        :rtype: str
        """
        return self._step_identifier

    @step_identifier.setter
    def step_identifier(self, step_identifier):
        """Sets the step_identifier of this SbomMetadata.

        id of the step  # noqa: E501

        :param step_identifier: The step_identifier of this SbomMetadata.  # noqa: E501
        :type: str
        """
        if step_identifier is None:
            raise ValueError("Invalid value for `step_identifier`, must not be `None`")  # noqa: E501

        self._step_identifier = step_identifier

    @property
    def step_name(self):
        """Gets the step_name of this SbomMetadata.  # noqa: E501


        :return: The step_name of this SbomMetadata.  # noqa: E501
        :rtype: str
        """
        return self._step_name

    @step_name.setter
    def step_name(self, step_name):
        """Sets the step_name of this SbomMetadata.


        :param step_name: The step_name of this SbomMetadata.  # noqa: E501
        :type: str
        """

        self._step_name = step_name

    @property
    def tool(self):
        """Gets the tool of this SbomMetadata.  # noqa: E501

        name of the package  # noqa: E501

        :return: The tool of this SbomMetadata.  # noqa: E501
        :rtype: str
        """
        return self._tool

    @tool.setter
    def tool(self, tool):
        """Sets the tool of this SbomMetadata.

        name of the package  # noqa: E501

        :param tool: The tool of this SbomMetadata.  # noqa: E501
        :type: str
        """
        if tool is None:
            raise ValueError("Invalid value for `tool`, must not be `None`")  # noqa: E501

        self._tool = tool

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
        if issubclass(SbomMetadata, dict):
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
        if not isinstance(other, SbomMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
