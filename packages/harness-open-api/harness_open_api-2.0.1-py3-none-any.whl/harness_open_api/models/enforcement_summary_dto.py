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

class EnforcementSummaryDTO(object):
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
        'account_id': 'str',
        'allow_list_violation_count': 'float',
        'artifact': 'Artifact1',
        'created': 'float',
        'deny_list_violation_count': 'float',
        'enforcement_id': 'str',
        'exempted_component_count': 'float',
        'orchestration_id': 'str',
        'org_identifier': 'str',
        'pipeline_execution_id': 'str',
        'project_identifier': 'str',
        'status': 'str'
    }

    attribute_map = {
        'account_id': 'account_id',
        'allow_list_violation_count': 'allow_list_violation_count',
        'artifact': 'artifact',
        'created': 'created',
        'deny_list_violation_count': 'deny_list_violation_count',
        'enforcement_id': 'enforcement_id',
        'exempted_component_count': 'exempted_component_count',
        'orchestration_id': 'orchestration_id',
        'org_identifier': 'org_identifier',
        'pipeline_execution_id': 'pipeline_execution_id',
        'project_identifier': 'project_identifier',
        'status': 'status'
    }

    def __init__(self, account_id=None, allow_list_violation_count=None, artifact=None, created=None, deny_list_violation_count=None, enforcement_id=None, exempted_component_count=None, orchestration_id=None, org_identifier=None, pipeline_execution_id=None, project_identifier=None, status=None):  # noqa: E501
        """EnforcementSummaryDTO - a model defined in Swagger"""  # noqa: E501
        self._account_id = None
        self._allow_list_violation_count = None
        self._artifact = None
        self._created = None
        self._deny_list_violation_count = None
        self._enforcement_id = None
        self._exempted_component_count = None
        self._orchestration_id = None
        self._org_identifier = None
        self._pipeline_execution_id = None
        self._project_identifier = None
        self._status = None
        self.discriminator = None
        self.account_id = account_id
        self.allow_list_violation_count = allow_list_violation_count
        self.artifact = artifact
        self.created = created
        self.deny_list_violation_count = deny_list_violation_count
        self.enforcement_id = enforcement_id
        if exempted_component_count is not None:
            self.exempted_component_count = exempted_component_count
        self.orchestration_id = orchestration_id
        self.org_identifier = org_identifier
        self.pipeline_execution_id = pipeline_execution_id
        self.project_identifier = project_identifier
        self.status = status

    @property
    def account_id(self):
        """Gets the account_id of this EnforcementSummaryDTO.  # noqa: E501


        :return: The account_id of this EnforcementSummaryDTO.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this EnforcementSummaryDTO.


        :param account_id: The account_id of this EnforcementSummaryDTO.  # noqa: E501
        :type: str
        """
        if account_id is None:
            raise ValueError("Invalid value for `account_id`, must not be `None`")  # noqa: E501

        self._account_id = account_id

    @property
    def allow_list_violation_count(self):
        """Gets the allow_list_violation_count of this EnforcementSummaryDTO.  # noqa: E501


        :return: The allow_list_violation_count of this EnforcementSummaryDTO.  # noqa: E501
        :rtype: float
        """
        return self._allow_list_violation_count

    @allow_list_violation_count.setter
    def allow_list_violation_count(self, allow_list_violation_count):
        """Sets the allow_list_violation_count of this EnforcementSummaryDTO.


        :param allow_list_violation_count: The allow_list_violation_count of this EnforcementSummaryDTO.  # noqa: E501
        :type: float
        """
        if allow_list_violation_count is None:
            raise ValueError("Invalid value for `allow_list_violation_count`, must not be `None`")  # noqa: E501

        self._allow_list_violation_count = allow_list_violation_count

    @property
    def artifact(self):
        """Gets the artifact of this EnforcementSummaryDTO.  # noqa: E501


        :return: The artifact of this EnforcementSummaryDTO.  # noqa: E501
        :rtype: Artifact1
        """
        return self._artifact

    @artifact.setter
    def artifact(self, artifact):
        """Sets the artifact of this EnforcementSummaryDTO.


        :param artifact: The artifact of this EnforcementSummaryDTO.  # noqa: E501
        :type: Artifact1
        """
        if artifact is None:
            raise ValueError("Invalid value for `artifact`, must not be `None`")  # noqa: E501

        self._artifact = artifact

    @property
    def created(self):
        """Gets the created of this EnforcementSummaryDTO.  # noqa: E501


        :return: The created of this EnforcementSummaryDTO.  # noqa: E501
        :rtype: float
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this EnforcementSummaryDTO.


        :param created: The created of this EnforcementSummaryDTO.  # noqa: E501
        :type: float
        """
        if created is None:
            raise ValueError("Invalid value for `created`, must not be `None`")  # noqa: E501

        self._created = created

    @property
    def deny_list_violation_count(self):
        """Gets the deny_list_violation_count of this EnforcementSummaryDTO.  # noqa: E501


        :return: The deny_list_violation_count of this EnforcementSummaryDTO.  # noqa: E501
        :rtype: float
        """
        return self._deny_list_violation_count

    @deny_list_violation_count.setter
    def deny_list_violation_count(self, deny_list_violation_count):
        """Sets the deny_list_violation_count of this EnforcementSummaryDTO.


        :param deny_list_violation_count: The deny_list_violation_count of this EnforcementSummaryDTO.  # noqa: E501
        :type: float
        """
        if deny_list_violation_count is None:
            raise ValueError("Invalid value for `deny_list_violation_count`, must not be `None`")  # noqa: E501

        self._deny_list_violation_count = deny_list_violation_count

    @property
    def enforcement_id(self):
        """Gets the enforcement_id of this EnforcementSummaryDTO.  # noqa: E501


        :return: The enforcement_id of this EnforcementSummaryDTO.  # noqa: E501
        :rtype: str
        """
        return self._enforcement_id

    @enforcement_id.setter
    def enforcement_id(self, enforcement_id):
        """Sets the enforcement_id of this EnforcementSummaryDTO.


        :param enforcement_id: The enforcement_id of this EnforcementSummaryDTO.  # noqa: E501
        :type: str
        """
        if enforcement_id is None:
            raise ValueError("Invalid value for `enforcement_id`, must not be `None`")  # noqa: E501

        self._enforcement_id = enforcement_id

    @property
    def exempted_component_count(self):
        """Gets the exempted_component_count of this EnforcementSummaryDTO.  # noqa: E501


        :return: The exempted_component_count of this EnforcementSummaryDTO.  # noqa: E501
        :rtype: float
        """
        return self._exempted_component_count

    @exempted_component_count.setter
    def exempted_component_count(self, exempted_component_count):
        """Sets the exempted_component_count of this EnforcementSummaryDTO.


        :param exempted_component_count: The exempted_component_count of this EnforcementSummaryDTO.  # noqa: E501
        :type: float
        """

        self._exempted_component_count = exempted_component_count

    @property
    def orchestration_id(self):
        """Gets the orchestration_id of this EnforcementSummaryDTO.  # noqa: E501


        :return: The orchestration_id of this EnforcementSummaryDTO.  # noqa: E501
        :rtype: str
        """
        return self._orchestration_id

    @orchestration_id.setter
    def orchestration_id(self, orchestration_id):
        """Sets the orchestration_id of this EnforcementSummaryDTO.


        :param orchestration_id: The orchestration_id of this EnforcementSummaryDTO.  # noqa: E501
        :type: str
        """
        if orchestration_id is None:
            raise ValueError("Invalid value for `orchestration_id`, must not be `None`")  # noqa: E501

        self._orchestration_id = orchestration_id

    @property
    def org_identifier(self):
        """Gets the org_identifier of this EnforcementSummaryDTO.  # noqa: E501


        :return: The org_identifier of this EnforcementSummaryDTO.  # noqa: E501
        :rtype: str
        """
        return self._org_identifier

    @org_identifier.setter
    def org_identifier(self, org_identifier):
        """Sets the org_identifier of this EnforcementSummaryDTO.


        :param org_identifier: The org_identifier of this EnforcementSummaryDTO.  # noqa: E501
        :type: str
        """
        if org_identifier is None:
            raise ValueError("Invalid value for `org_identifier`, must not be `None`")  # noqa: E501

        self._org_identifier = org_identifier

    @property
    def pipeline_execution_id(self):
        """Gets the pipeline_execution_id of this EnforcementSummaryDTO.  # noqa: E501


        :return: The pipeline_execution_id of this EnforcementSummaryDTO.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_execution_id

    @pipeline_execution_id.setter
    def pipeline_execution_id(self, pipeline_execution_id):
        """Sets the pipeline_execution_id of this EnforcementSummaryDTO.


        :param pipeline_execution_id: The pipeline_execution_id of this EnforcementSummaryDTO.  # noqa: E501
        :type: str
        """
        if pipeline_execution_id is None:
            raise ValueError("Invalid value for `pipeline_execution_id`, must not be `None`")  # noqa: E501

        self._pipeline_execution_id = pipeline_execution_id

    @property
    def project_identifier(self):
        """Gets the project_identifier of this EnforcementSummaryDTO.  # noqa: E501


        :return: The project_identifier of this EnforcementSummaryDTO.  # noqa: E501
        :rtype: str
        """
        return self._project_identifier

    @project_identifier.setter
    def project_identifier(self, project_identifier):
        """Sets the project_identifier of this EnforcementSummaryDTO.


        :param project_identifier: The project_identifier of this EnforcementSummaryDTO.  # noqa: E501
        :type: str
        """
        if project_identifier is None:
            raise ValueError("Invalid value for `project_identifier`, must not be `None`")  # noqa: E501

        self._project_identifier = project_identifier

    @property
    def status(self):
        """Gets the status of this EnforcementSummaryDTO.  # noqa: E501


        :return: The status of this EnforcementSummaryDTO.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this EnforcementSummaryDTO.


        :param status: The status of this EnforcementSummaryDTO.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

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
        if issubclass(EnforcementSummaryDTO, dict):
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
        if not isinstance(other, EnforcementSummaryDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
