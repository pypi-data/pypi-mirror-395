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

class ScanIssueCountsWithExecutionInfo(object):
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
        'artifact_fingerprint': 'str',
        'execution_id': 'str',
        'last_scanned': 'int',
        'pipeline_id': 'str',
        'scanners': 'list[MinimalIssueCountsPerScanner]',
        'target_id': 'str',
        'target_name': 'str',
        'target_variant_id': 'str',
        'target_variant_name': 'str',
        'type': 'str'
    }

    attribute_map = {
        'artifact_fingerprint': 'artifactFingerprint',
        'execution_id': 'executionId',
        'last_scanned': 'lastScanned',
        'pipeline_id': 'pipelineId',
        'scanners': 'scanners',
        'target_id': 'targetId',
        'target_name': 'targetName',
        'target_variant_id': 'targetVariantId',
        'target_variant_name': 'targetVariantName',
        'type': 'type'
    }

    def __init__(self, artifact_fingerprint=None, execution_id=None, last_scanned=None, pipeline_id=None, scanners=None, target_id=None, target_name=None, target_variant_id=None, target_variant_name=None, type=None):  # noqa: E501
        """ScanIssueCountsWithExecutionInfo - a model defined in Swagger"""  # noqa: E501
        self._artifact_fingerprint = None
        self._execution_id = None
        self._last_scanned = None
        self._pipeline_id = None
        self._scanners = None
        self._target_id = None
        self._target_name = None
        self._target_variant_id = None
        self._target_variant_name = None
        self._type = None
        self.discriminator = None
        if artifact_fingerprint is not None:
            self.artifact_fingerprint = artifact_fingerprint
        self.execution_id = execution_id
        self.last_scanned = last_scanned
        self.pipeline_id = pipeline_id
        self.scanners = scanners
        self.target_id = target_id
        self.target_name = target_name
        self.target_variant_id = target_variant_id
        self.target_variant_name = target_variant_name
        self.type = type

    @property
    def artifact_fingerprint(self):
        """Gets the artifact_fingerprint of this ScanIssueCountsWithExecutionInfo.  # noqa: E501

        Fingerprint which identifies an artifact  # noqa: E501

        :return: The artifact_fingerprint of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :rtype: str
        """
        return self._artifact_fingerprint

    @artifact_fingerprint.setter
    def artifact_fingerprint(self, artifact_fingerprint):
        """Sets the artifact_fingerprint of this ScanIssueCountsWithExecutionInfo.

        Fingerprint which identifies an artifact  # noqa: E501

        :param artifact_fingerprint: The artifact_fingerprint of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :type: str
        """

        self._artifact_fingerprint = artifact_fingerprint

    @property
    def execution_id(self):
        """Gets the execution_id of this ScanIssueCountsWithExecutionInfo.  # noqa: E501

        Harness Execution ID  # noqa: E501

        :return: The execution_id of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :rtype: str
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id):
        """Sets the execution_id of this ScanIssueCountsWithExecutionInfo.

        Harness Execution ID  # noqa: E501

        :param execution_id: The execution_id of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :type: str
        """
        if execution_id is None:
            raise ValueError("Invalid value for `execution_id`, must not be `None`")  # noqa: E501

        self._execution_id = execution_id

    @property
    def last_scanned(self):
        """Gets the last_scanned of this ScanIssueCountsWithExecutionInfo.  # noqa: E501

        Timestamp at which the target variant was last scanned  # noqa: E501

        :return: The last_scanned of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :rtype: int
        """
        return self._last_scanned

    @last_scanned.setter
    def last_scanned(self, last_scanned):
        """Sets the last_scanned of this ScanIssueCountsWithExecutionInfo.

        Timestamp at which the target variant was last scanned  # noqa: E501

        :param last_scanned: The last_scanned of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :type: int
        """
        if last_scanned is None:
            raise ValueError("Invalid value for `last_scanned`, must not be `None`")  # noqa: E501

        self._last_scanned = last_scanned

    @property
    def pipeline_id(self):
        """Gets the pipeline_id of this ScanIssueCountsWithExecutionInfo.  # noqa: E501

        Harness Pipeline ID  # noqa: E501

        :return: The pipeline_id of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_id

    @pipeline_id.setter
    def pipeline_id(self, pipeline_id):
        """Sets the pipeline_id of this ScanIssueCountsWithExecutionInfo.

        Harness Pipeline ID  # noqa: E501

        :param pipeline_id: The pipeline_id of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :type: str
        """
        if pipeline_id is None:
            raise ValueError("Invalid value for `pipeline_id`, must not be `None`")  # noqa: E501

        self._pipeline_id = pipeline_id

    @property
    def scanners(self):
        """Gets the scanners of this ScanIssueCountsWithExecutionInfo.  # noqa: E501

        List of security issue counts grouped by scanner  # noqa: E501

        :return: The scanners of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :rtype: list[MinimalIssueCountsPerScanner]
        """
        return self._scanners

    @scanners.setter
    def scanners(self, scanners):
        """Sets the scanners of this ScanIssueCountsWithExecutionInfo.

        List of security issue counts grouped by scanner  # noqa: E501

        :param scanners: The scanners of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :type: list[MinimalIssueCountsPerScanner]
        """
        if scanners is None:
            raise ValueError("Invalid value for `scanners`, must not be `None`")  # noqa: E501

        self._scanners = scanners

    @property
    def target_id(self):
        """Gets the target_id of this ScanIssueCountsWithExecutionInfo.  # noqa: E501

        Associated Target ID  # noqa: E501

        :return: The target_id of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """Sets the target_id of this ScanIssueCountsWithExecutionInfo.

        Associated Target ID  # noqa: E501

        :param target_id: The target_id of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :type: str
        """
        if target_id is None:
            raise ValueError("Invalid value for `target_id`, must not be `None`")  # noqa: E501

        self._target_id = target_id

    @property
    def target_name(self):
        """Gets the target_name of this ScanIssueCountsWithExecutionInfo.  # noqa: E501

        Name of the Scan Target  # noqa: E501

        :return: The target_name of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :rtype: str
        """
        return self._target_name

    @target_name.setter
    def target_name(self, target_name):
        """Sets the target_name of this ScanIssueCountsWithExecutionInfo.

        Name of the Scan Target  # noqa: E501

        :param target_name: The target_name of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :type: str
        """
        if target_name is None:
            raise ValueError("Invalid value for `target_name`, must not be `None`")  # noqa: E501

        self._target_name = target_name

    @property
    def target_variant_id(self):
        """Gets the target_variant_id of this ScanIssueCountsWithExecutionInfo.  # noqa: E501

        Associated Target Variant ID  # noqa: E501

        :return: The target_variant_id of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :rtype: str
        """
        return self._target_variant_id

    @target_variant_id.setter
    def target_variant_id(self, target_variant_id):
        """Sets the target_variant_id of this ScanIssueCountsWithExecutionInfo.

        Associated Target Variant ID  # noqa: E501

        :param target_variant_id: The target_variant_id of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :type: str
        """
        if target_variant_id is None:
            raise ValueError("Invalid value for `target_variant_id`, must not be `None`")  # noqa: E501

        self._target_variant_id = target_variant_id

    @property
    def target_variant_name(self):
        """Gets the target_variant_name of this ScanIssueCountsWithExecutionInfo.  # noqa: E501

        Name of the Scan Target  # noqa: E501

        :return: The target_variant_name of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :rtype: str
        """
        return self._target_variant_name

    @target_variant_name.setter
    def target_variant_name(self, target_variant_name):
        """Sets the target_variant_name of this ScanIssueCountsWithExecutionInfo.

        Name of the Scan Target  # noqa: E501

        :param target_variant_name: The target_variant_name of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :type: str
        """
        if target_variant_name is None:
            raise ValueError("Invalid value for `target_variant_name`, must not be `None`")  # noqa: E501

        self._target_variant_name = target_variant_name

    @property
    def type(self):
        """Gets the type of this ScanIssueCountsWithExecutionInfo.  # noqa: E501

        Scan Target's type  # noqa: E501

        :return: The type of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ScanIssueCountsWithExecutionInfo.

        Scan Target's type  # noqa: E501

        :param type: The type of this ScanIssueCountsWithExecutionInfo.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
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
        if issubclass(ScanIssueCountsWithExecutionInfo, dict):
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
        if not isinstance(other, ScanIssueCountsWithExecutionInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
