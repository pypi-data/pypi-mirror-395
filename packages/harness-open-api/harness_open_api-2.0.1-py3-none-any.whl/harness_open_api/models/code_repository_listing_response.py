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

class CodeRepositoryListingResponse(object):
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
        'dependencies_count': 'int',
        'id': 'str',
        'last_scan': 'PipelineDetails',
        'name': 'str',
        'orchestration_id': 'str',
        'repository_platform': 'RepositoryPlatform',
        'risk_and_compliance': 'RiskAndCompliance',
        'scorecard': 'Scorecard1',
        'sto_issue_count': 'StoIssueCount',
        'url': 'str',
        'variant': 'ArtifactVariant'
    }

    attribute_map = {
        'dependencies_count': 'dependencies_count',
        'id': 'id',
        'last_scan': 'last_scan',
        'name': 'name',
        'orchestration_id': 'orchestration_id',
        'repository_platform': 'repository_platform',
        'risk_and_compliance': 'risk_and_compliance',
        'scorecard': 'scorecard',
        'sto_issue_count': 'sto_issue_count',
        'url': 'url',
        'variant': 'variant'
    }

    def __init__(self, dependencies_count=None, id=None, last_scan=None, name=None, orchestration_id=None, repository_platform=None, risk_and_compliance=None, scorecard=None, sto_issue_count=None, url=None, variant=None):  # noqa: E501
        """CodeRepositoryListingResponse - a model defined in Swagger"""  # noqa: E501
        self._dependencies_count = None
        self._id = None
        self._last_scan = None
        self._name = None
        self._orchestration_id = None
        self._repository_platform = None
        self._risk_and_compliance = None
        self._scorecard = None
        self._sto_issue_count = None
        self._url = None
        self._variant = None
        self.discriminator = None
        if dependencies_count is not None:
            self.dependencies_count = dependencies_count
        if id is not None:
            self.id = id
        if last_scan is not None:
            self.last_scan = last_scan
        if name is not None:
            self.name = name
        if orchestration_id is not None:
            self.orchestration_id = orchestration_id
        if repository_platform is not None:
            self.repository_platform = repository_platform
        if risk_and_compliance is not None:
            self.risk_and_compliance = risk_and_compliance
        if scorecard is not None:
            self.scorecard = scorecard
        if sto_issue_count is not None:
            self.sto_issue_count = sto_issue_count
        if url is not None:
            self.url = url
        if variant is not None:
            self.variant = variant

    @property
    def dependencies_count(self):
        """Gets the dependencies_count of this CodeRepositoryListingResponse.  # noqa: E501

        Number of dependencies of the repository  # noqa: E501

        :return: The dependencies_count of this CodeRepositoryListingResponse.  # noqa: E501
        :rtype: int
        """
        return self._dependencies_count

    @dependencies_count.setter
    def dependencies_count(self, dependencies_count):
        """Sets the dependencies_count of this CodeRepositoryListingResponse.

        Number of dependencies of the repository  # noqa: E501

        :param dependencies_count: The dependencies_count of this CodeRepositoryListingResponse.  # noqa: E501
        :type: int
        """

        self._dependencies_count = dependencies_count

    @property
    def id(self):
        """Gets the id of this CodeRepositoryListingResponse.  # noqa: E501

        Code Respository ID  # noqa: E501

        :return: The id of this CodeRepositoryListingResponse.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this CodeRepositoryListingResponse.

        Code Respository ID  # noqa: E501

        :param id: The id of this CodeRepositoryListingResponse.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def last_scan(self):
        """Gets the last_scan of this CodeRepositoryListingResponse.  # noqa: E501


        :return: The last_scan of this CodeRepositoryListingResponse.  # noqa: E501
        :rtype: PipelineDetails
        """
        return self._last_scan

    @last_scan.setter
    def last_scan(self, last_scan):
        """Sets the last_scan of this CodeRepositoryListingResponse.


        :param last_scan: The last_scan of this CodeRepositoryListingResponse.  # noqa: E501
        :type: PipelineDetails
        """

        self._last_scan = last_scan

    @property
    def name(self):
        """Gets the name of this CodeRepositoryListingResponse.  # noqa: E501

        Code Repository Name  # noqa: E501

        :return: The name of this CodeRepositoryListingResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CodeRepositoryListingResponse.

        Code Repository Name  # noqa: E501

        :param name: The name of this CodeRepositoryListingResponse.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def orchestration_id(self):
        """Gets the orchestration_id of this CodeRepositoryListingResponse.  # noqa: E501


        :return: The orchestration_id of this CodeRepositoryListingResponse.  # noqa: E501
        :rtype: str
        """
        return self._orchestration_id

    @orchestration_id.setter
    def orchestration_id(self, orchestration_id):
        """Sets the orchestration_id of this CodeRepositoryListingResponse.


        :param orchestration_id: The orchestration_id of this CodeRepositoryListingResponse.  # noqa: E501
        :type: str
        """

        self._orchestration_id = orchestration_id

    @property
    def repository_platform(self):
        """Gets the repository_platform of this CodeRepositoryListingResponse.  # noqa: E501


        :return: The repository_platform of this CodeRepositoryListingResponse.  # noqa: E501
        :rtype: RepositoryPlatform
        """
        return self._repository_platform

    @repository_platform.setter
    def repository_platform(self, repository_platform):
        """Sets the repository_platform of this CodeRepositoryListingResponse.


        :param repository_platform: The repository_platform of this CodeRepositoryListingResponse.  # noqa: E501
        :type: RepositoryPlatform
        """

        self._repository_platform = repository_platform

    @property
    def risk_and_compliance(self):
        """Gets the risk_and_compliance of this CodeRepositoryListingResponse.  # noqa: E501


        :return: The risk_and_compliance of this CodeRepositoryListingResponse.  # noqa: E501
        :rtype: RiskAndCompliance
        """
        return self._risk_and_compliance

    @risk_and_compliance.setter
    def risk_and_compliance(self, risk_and_compliance):
        """Sets the risk_and_compliance of this CodeRepositoryListingResponse.


        :param risk_and_compliance: The risk_and_compliance of this CodeRepositoryListingResponse.  # noqa: E501
        :type: RiskAndCompliance
        """

        self._risk_and_compliance = risk_and_compliance

    @property
    def scorecard(self):
        """Gets the scorecard of this CodeRepositoryListingResponse.  # noqa: E501


        :return: The scorecard of this CodeRepositoryListingResponse.  # noqa: E501
        :rtype: Scorecard1
        """
        return self._scorecard

    @scorecard.setter
    def scorecard(self, scorecard):
        """Sets the scorecard of this CodeRepositoryListingResponse.


        :param scorecard: The scorecard of this CodeRepositoryListingResponse.  # noqa: E501
        :type: Scorecard1
        """

        self._scorecard = scorecard

    @property
    def sto_issue_count(self):
        """Gets the sto_issue_count of this CodeRepositoryListingResponse.  # noqa: E501


        :return: The sto_issue_count of this CodeRepositoryListingResponse.  # noqa: E501
        :rtype: StoIssueCount
        """
        return self._sto_issue_count

    @sto_issue_count.setter
    def sto_issue_count(self, sto_issue_count):
        """Sets the sto_issue_count of this CodeRepositoryListingResponse.


        :param sto_issue_count: The sto_issue_count of this CodeRepositoryListingResponse.  # noqa: E501
        :type: StoIssueCount
        """

        self._sto_issue_count = sto_issue_count

    @property
    def url(self):
        """Gets the url of this CodeRepositoryListingResponse.  # noqa: E501

        Code Repository URL  # noqa: E501

        :return: The url of this CodeRepositoryListingResponse.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this CodeRepositoryListingResponse.

        Code Repository URL  # noqa: E501

        :param url: The url of this CodeRepositoryListingResponse.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def variant(self):
        """Gets the variant of this CodeRepositoryListingResponse.  # noqa: E501


        :return: The variant of this CodeRepositoryListingResponse.  # noqa: E501
        :rtype: ArtifactVariant
        """
        return self._variant

    @variant.setter
    def variant(self, variant):
        """Sets the variant of this CodeRepositoryListingResponse.


        :param variant: The variant of this CodeRepositoryListingResponse.  # noqa: E501
        :type: ArtifactVariant
        """

        self._variant = variant

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
        if issubclass(CodeRepositoryListingResponse, dict):
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
        if not isinstance(other, CodeRepositoryListingResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
