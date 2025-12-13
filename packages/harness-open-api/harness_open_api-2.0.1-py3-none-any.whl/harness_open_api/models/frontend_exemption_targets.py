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

class FrontendExemptionTargets(object):
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
        'execution_id': 'str',
        'hash': 'str',
        'last_scanned': 'float',
        'name': 'str',
        'num_exempted_occurrences': 'int',
        'num_occurrences': 'int',
        'org_id': 'str',
        'parameters': 'dict(str, str)',
        'pipeline_id': 'str',
        'project_id': 'str',
        'scan_id': 'str',
        'target_id': 'str',
        'type': 'str'
    }

    attribute_map = {
        'execution_id': 'executionId',
        'hash': 'hash',
        'last_scanned': 'lastScanned',
        'name': 'name',
        'num_exempted_occurrences': 'numExemptedOccurrences',
        'num_occurrences': 'numOccurrences',
        'org_id': 'orgId',
        'parameters': 'parameters',
        'pipeline_id': 'pipelineId',
        'project_id': 'projectId',
        'scan_id': 'scanId',
        'target_id': 'targetId',
        'type': 'type'
    }

    def __init__(self, execution_id=None, hash=None, last_scanned=None, name=None, num_exempted_occurrences=0, num_occurrences=0, org_id=None, parameters=None, pipeline_id=None, project_id=None, scan_id=None, target_id=None, type=None):  # noqa: E501
        """FrontendExemptionTargets - a model defined in Swagger"""  # noqa: E501
        self._execution_id = None
        self._hash = None
        self._last_scanned = None
        self._name = None
        self._num_exempted_occurrences = None
        self._num_occurrences = None
        self._org_id = None
        self._parameters = None
        self._pipeline_id = None
        self._project_id = None
        self._scan_id = None
        self._target_id = None
        self._type = None
        self.discriminator = None
        if execution_id is not None:
            self.execution_id = execution_id
        if hash is not None:
            self.hash = hash
        if last_scanned is not None:
            self.last_scanned = last_scanned
        if name is not None:
            self.name = name
        if num_exempted_occurrences is not None:
            self.num_exempted_occurrences = num_exempted_occurrences
        if num_occurrences is not None:
            self.num_occurrences = num_occurrences
        if org_id is not None:
            self.org_id = org_id
        self.parameters = parameters
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if project_id is not None:
            self.project_id = project_id
        if scan_id is not None:
            self.scan_id = scan_id
        self.target_id = target_id
        if type is not None:
            self.type = type

    @property
    def execution_id(self):
        """Gets the execution_id of this FrontendExemptionTargets.  # noqa: E501

        Harness Execution ID  # noqa: E501

        :return: The execution_id of this FrontendExemptionTargets.  # noqa: E501
        :rtype: str
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id):
        """Sets the execution_id of this FrontendExemptionTargets.

        Harness Execution ID  # noqa: E501

        :param execution_id: The execution_id of this FrontendExemptionTargets.  # noqa: E501
        :type: str
        """

        self._execution_id = execution_id

    @property
    def hash(self):
        """Gets the hash of this FrontendExemptionTargets.  # noqa: E501

        Git Commit or Container Image hash  # noqa: E501

        :return: The hash of this FrontendExemptionTargets.  # noqa: E501
        :rtype: str
        """
        return self._hash

    @hash.setter
    def hash(self, hash):
        """Sets the hash of this FrontendExemptionTargets.

        Git Commit or Container Image hash  # noqa: E501

        :param hash: The hash of this FrontendExemptionTargets.  # noqa: E501
        :type: str
        """

        self._hash = hash

    @property
    def last_scanned(self):
        """Gets the last_scanned of this FrontendExemptionTargets.  # noqa: E501

        Timestamp of the last detection of this issue  # noqa: E501

        :return: The last_scanned of this FrontendExemptionTargets.  # noqa: E501
        :rtype: float
        """
        return self._last_scanned

    @last_scanned.setter
    def last_scanned(self, last_scanned):
        """Sets the last_scanned of this FrontendExemptionTargets.

        Timestamp of the last detection of this issue  # noqa: E501

        :param last_scanned: The last_scanned of this FrontendExemptionTargets.  # noqa: E501
        :type: float
        """

        self._last_scanned = last_scanned

    @property
    def name(self):
        """Gets the name of this FrontendExemptionTargets.  # noqa: E501

        Name of the Test Target  # noqa: E501

        :return: The name of this FrontendExemptionTargets.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this FrontendExemptionTargets.

        Name of the Test Target  # noqa: E501

        :param name: The name of this FrontendExemptionTargets.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def num_exempted_occurrences(self):
        """Gets the num_exempted_occurrences of this FrontendExemptionTargets.  # noqa: E501

        Total number of occurrences exempted for an impacted target  # noqa: E501

        :return: The num_exempted_occurrences of this FrontendExemptionTargets.  # noqa: E501
        :rtype: int
        """
        return self._num_exempted_occurrences

    @num_exempted_occurrences.setter
    def num_exempted_occurrences(self, num_exempted_occurrences):
        """Sets the num_exempted_occurrences of this FrontendExemptionTargets.

        Total number of occurrences exempted for an impacted target  # noqa: E501

        :param num_exempted_occurrences: The num_exempted_occurrences of this FrontendExemptionTargets.  # noqa: E501
        :type: int
        """

        self._num_exempted_occurrences = num_exempted_occurrences

    @property
    def num_occurrences(self):
        """Gets the num_occurrences of this FrontendExemptionTargets.  # noqa: E501

        Total number of occurrences for an impacted target  # noqa: E501

        :return: The num_occurrences of this FrontendExemptionTargets.  # noqa: E501
        :rtype: int
        """
        return self._num_occurrences

    @num_occurrences.setter
    def num_occurrences(self, num_occurrences):
        """Sets the num_occurrences of this FrontendExemptionTargets.

        Total number of occurrences for an impacted target  # noqa: E501

        :param num_occurrences: The num_occurrences of this FrontendExemptionTargets.  # noqa: E501
        :type: int
        """

        self._num_occurrences = num_occurrences

    @property
    def org_id(self):
        """Gets the org_id of this FrontendExemptionTargets.  # noqa: E501

        Harness Organization ID  # noqa: E501

        :return: The org_id of this FrontendExemptionTargets.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Sets the org_id of this FrontendExemptionTargets.

        Harness Organization ID  # noqa: E501

        :param org_id: The org_id of this FrontendExemptionTargets.  # noqa: E501
        :type: str
        """

        self._org_id = org_id

    @property
    def parameters(self):
        """Gets the parameters of this FrontendExemptionTargets.  # noqa: E501

        Parameters for this Variant, as a JSON-encoded string  # noqa: E501

        :return: The parameters of this FrontendExemptionTargets.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this FrontendExemptionTargets.

        Parameters for this Variant, as a JSON-encoded string  # noqa: E501

        :param parameters: The parameters of this FrontendExemptionTargets.  # noqa: E501
        :type: dict(str, str)
        """
        if parameters is None:
            raise ValueError("Invalid value for `parameters`, must not be `None`")  # noqa: E501

        self._parameters = parameters

    @property
    def pipeline_id(self):
        """Gets the pipeline_id of this FrontendExemptionTargets.  # noqa: E501

        ID of the Harness pipeline of the scan  # noqa: E501

        :return: The pipeline_id of this FrontendExemptionTargets.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_id

    @pipeline_id.setter
    def pipeline_id(self, pipeline_id):
        """Sets the pipeline_id of this FrontendExemptionTargets.

        ID of the Harness pipeline of the scan  # noqa: E501

        :param pipeline_id: The pipeline_id of this FrontendExemptionTargets.  # noqa: E501
        :type: str
        """

        self._pipeline_id = pipeline_id

    @property
    def project_id(self):
        """Gets the project_id of this FrontendExemptionTargets.  # noqa: E501

        Harness Project ID  # noqa: E501

        :return: The project_id of this FrontendExemptionTargets.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this FrontendExemptionTargets.

        Harness Project ID  # noqa: E501

        :param project_id: The project_id of this FrontendExemptionTargets.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def scan_id(self):
        """Gets the scan_id of this FrontendExemptionTargets.  # noqa: E501

        The Security Scan execution that detected this Security Issue  # noqa: E501

        :return: The scan_id of this FrontendExemptionTargets.  # noqa: E501
        :rtype: str
        """
        return self._scan_id

    @scan_id.setter
    def scan_id(self, scan_id):
        """Sets the scan_id of this FrontendExemptionTargets.

        The Security Scan execution that detected this Security Issue  # noqa: E501

        :param scan_id: The scan_id of this FrontendExemptionTargets.  # noqa: E501
        :type: str
        """

        self._scan_id = scan_id

    @property
    def target_id(self):
        """Gets the target_id of this FrontendExemptionTargets.  # noqa: E501

        Associated Target ID  # noqa: E501

        :return: The target_id of this FrontendExemptionTargets.  # noqa: E501
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """Sets the target_id of this FrontendExemptionTargets.

        Associated Target ID  # noqa: E501

        :param target_id: The target_id of this FrontendExemptionTargets.  # noqa: E501
        :type: str
        """
        if target_id is None:
            raise ValueError("Invalid value for `target_id`, must not be `None`")  # noqa: E501

        self._target_id = target_id

    @property
    def type(self):
        """Gets the type of this FrontendExemptionTargets.  # noqa: E501

        Test Target's type  # noqa: E501

        :return: The type of this FrontendExemptionTargets.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this FrontendExemptionTargets.

        Test Target's type  # noqa: E501

        :param type: The type of this FrontendExemptionTargets.  # noqa: E501
        :type: str
        """
        allowed_values = ["container", "repository", "instance", "configuration"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

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
        if issubclass(FrontendExemptionTargets, dict):
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
        if not isinstance(other, FrontendExemptionTargets):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
