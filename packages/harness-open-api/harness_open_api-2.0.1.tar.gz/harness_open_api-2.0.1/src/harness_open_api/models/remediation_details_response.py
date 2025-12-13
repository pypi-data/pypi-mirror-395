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

class RemediationDetailsResponse(object):
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
        'artifacts': 'int',
        'artifacts_excluded': 'int',
        'closed_by': 'str',
        'comments': 'str',
        'component': 'str',
        'contact': 'ContactInfo',
        'created_by_email': 'str',
        'created_by_name': 'str',
        'cve': 'str',
        'deployments_count': 'DeploymentsCount',
        'end_time_milli': 'int',
        'environments': 'int',
        'id': 'str',
        'new_artifacts_count': 'int',
        'new_environments_count': 'int',
        'remediation_condition': 'RemediationCondition',
        'severity': 'VulnerabilitySeverity',
        'start_time_milli': 'int',
        'status': 'RemediationStatus',
        'target_date': 'str',
        'ticket': 'TicketInfo',
        'vulnerability_description': 'str'
    }

    attribute_map = {
        'artifacts': 'artifacts',
        'artifacts_excluded': 'artifacts_excluded',
        'closed_by': 'closed_by',
        'comments': 'comments',
        'component': 'component',
        'contact': 'contact',
        'created_by_email': 'created_by_email',
        'created_by_name': 'created_by_name',
        'cve': 'cve',
        'deployments_count': 'deployments_count',
        'end_time_milli': 'end_time_milli',
        'environments': 'environments',
        'id': 'id',
        'new_artifacts_count': 'new_artifacts_count',
        'new_environments_count': 'new_environments_count',
        'remediation_condition': 'remediation_condition',
        'severity': 'severity',
        'start_time_milli': 'start_time_milli',
        'status': 'status',
        'target_date': 'target_date',
        'ticket': 'ticket',
        'vulnerability_description': 'vulnerability_description'
    }

    def __init__(self, artifacts=None, artifacts_excluded=None, closed_by=None, comments=None, component=None, contact=None, created_by_email=None, created_by_name=None, cve=None, deployments_count=None, end_time_milli=None, environments=None, id=None, new_artifacts_count=None, new_environments_count=None, remediation_condition=None, severity=None, start_time_milli=None, status=None, target_date=None, ticket=None, vulnerability_description=None):  # noqa: E501
        """RemediationDetailsResponse - a model defined in Swagger"""  # noqa: E501
        self._artifacts = None
        self._artifacts_excluded = None
        self._closed_by = None
        self._comments = None
        self._component = None
        self._contact = None
        self._created_by_email = None
        self._created_by_name = None
        self._cve = None
        self._deployments_count = None
        self._end_time_milli = None
        self._environments = None
        self._id = None
        self._new_artifacts_count = None
        self._new_environments_count = None
        self._remediation_condition = None
        self._severity = None
        self._start_time_milli = None
        self._status = None
        self._target_date = None
        self._ticket = None
        self._vulnerability_description = None
        self.discriminator = None
        self.artifacts = artifacts
        self.artifacts_excluded = artifacts_excluded
        if closed_by is not None:
            self.closed_by = closed_by
        if comments is not None:
            self.comments = comments
        self.component = component
        if contact is not None:
            self.contact = contact
        if created_by_email is not None:
            self.created_by_email = created_by_email
        if created_by_name is not None:
            self.created_by_name = created_by_name
        if cve is not None:
            self.cve = cve
        self.deployments_count = deployments_count
        if end_time_milli is not None:
            self.end_time_milli = end_time_milli
        self.environments = environments
        self.id = id
        self.new_artifacts_count = new_artifacts_count
        self.new_environments_count = new_environments_count
        self.remediation_condition = remediation_condition
        self.severity = severity
        self.start_time_milli = start_time_milli
        self.status = status
        if target_date is not None:
            self.target_date = target_date
        if ticket is not None:
            self.ticket = ticket
        if vulnerability_description is not None:
            self.vulnerability_description = vulnerability_description

    @property
    def artifacts(self):
        """Gets the artifacts of this RemediationDetailsResponse.  # noqa: E501

        Total distinct artifacts included in the tracker.  # noqa: E501

        :return: The artifacts of this RemediationDetailsResponse.  # noqa: E501
        :rtype: int
        """
        return self._artifacts

    @artifacts.setter
    def artifacts(self, artifacts):
        """Sets the artifacts of this RemediationDetailsResponse.

        Total distinct artifacts included in the tracker.  # noqa: E501

        :param artifacts: The artifacts of this RemediationDetailsResponse.  # noqa: E501
        :type: int
        """
        if artifacts is None:
            raise ValueError("Invalid value for `artifacts`, must not be `None`")  # noqa: E501

        self._artifacts = artifacts

    @property
    def artifacts_excluded(self):
        """Gets the artifacts_excluded of this RemediationDetailsResponse.  # noqa: E501

        Total Number of Excluded Artifacts.  # noqa: E501

        :return: The artifacts_excluded of this RemediationDetailsResponse.  # noqa: E501
        :rtype: int
        """
        return self._artifacts_excluded

    @artifacts_excluded.setter
    def artifacts_excluded(self, artifacts_excluded):
        """Sets the artifacts_excluded of this RemediationDetailsResponse.

        Total Number of Excluded Artifacts.  # noqa: E501

        :param artifacts_excluded: The artifacts_excluded of this RemediationDetailsResponse.  # noqa: E501
        :type: int
        """
        if artifacts_excluded is None:
            raise ValueError("Invalid value for `artifacts_excluded`, must not be `None`")  # noqa: E501

        self._artifacts_excluded = artifacts_excluded

    @property
    def closed_by(self):
        """Gets the closed_by of this RemediationDetailsResponse.  # noqa: E501

        If Remediation Tracker was closed manually , name of the user who closed it.  # noqa: E501

        :return: The closed_by of this RemediationDetailsResponse.  # noqa: E501
        :rtype: str
        """
        return self._closed_by

    @closed_by.setter
    def closed_by(self, closed_by):
        """Sets the closed_by of this RemediationDetailsResponse.

        If Remediation Tracker was closed manually , name of the user who closed it.  # noqa: E501

        :param closed_by: The closed_by of this RemediationDetailsResponse.  # noqa: E501
        :type: str
        """

        self._closed_by = closed_by

    @property
    def comments(self):
        """Gets the comments of this RemediationDetailsResponse.  # noqa: E501

        Description/comments for the tracker.  # noqa: E501

        :return: The comments of this RemediationDetailsResponse.  # noqa: E501
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """Sets the comments of this RemediationDetailsResponse.

        Description/comments for the tracker.  # noqa: E501

        :param comments: The comments of this RemediationDetailsResponse.  # noqa: E501
        :type: str
        """

        self._comments = comments

    @property
    def component(self):
        """Gets the component of this RemediationDetailsResponse.  # noqa: E501

        Component Name.  # noqa: E501

        :return: The component of this RemediationDetailsResponse.  # noqa: E501
        :rtype: str
        """
        return self._component

    @component.setter
    def component(self, component):
        """Sets the component of this RemediationDetailsResponse.

        Component Name.  # noqa: E501

        :param component: The component of this RemediationDetailsResponse.  # noqa: E501
        :type: str
        """
        if component is None:
            raise ValueError("Invalid value for `component`, must not be `None`")  # noqa: E501

        self._component = component

    @property
    def contact(self):
        """Gets the contact of this RemediationDetailsResponse.  # noqa: E501


        :return: The contact of this RemediationDetailsResponse.  # noqa: E501
        :rtype: ContactInfo
        """
        return self._contact

    @contact.setter
    def contact(self, contact):
        """Sets the contact of this RemediationDetailsResponse.


        :param contact: The contact of this RemediationDetailsResponse.  # noqa: E501
        :type: ContactInfo
        """

        self._contact = contact

    @property
    def created_by_email(self):
        """Gets the created_by_email of this RemediationDetailsResponse.  # noqa: E501

        Email of the User who created the Remediation Tracker.  # noqa: E501

        :return: The created_by_email of this RemediationDetailsResponse.  # noqa: E501
        :rtype: str
        """
        return self._created_by_email

    @created_by_email.setter
    def created_by_email(self, created_by_email):
        """Sets the created_by_email of this RemediationDetailsResponse.

        Email of the User who created the Remediation Tracker.  # noqa: E501

        :param created_by_email: The created_by_email of this RemediationDetailsResponse.  # noqa: E501
        :type: str
        """

        self._created_by_email = created_by_email

    @property
    def created_by_name(self):
        """Gets the created_by_name of this RemediationDetailsResponse.  # noqa: E501

        Name of the User who created the Remediation Tracker.  # noqa: E501

        :return: The created_by_name of this RemediationDetailsResponse.  # noqa: E501
        :rtype: str
        """
        return self._created_by_name

    @created_by_name.setter
    def created_by_name(self, created_by_name):
        """Sets the created_by_name of this RemediationDetailsResponse.

        Name of the User who created the Remediation Tracker.  # noqa: E501

        :param created_by_name: The created_by_name of this RemediationDetailsResponse.  # noqa: E501
        :type: str
        """

        self._created_by_name = created_by_name

    @property
    def cve(self):
        """Gets the cve of this RemediationDetailsResponse.  # noqa: E501

        CVE number.  # noqa: E501

        :return: The cve of this RemediationDetailsResponse.  # noqa: E501
        :rtype: str
        """
        return self._cve

    @cve.setter
    def cve(self, cve):
        """Sets the cve of this RemediationDetailsResponse.

        CVE number.  # noqa: E501

        :param cve: The cve of this RemediationDetailsResponse.  # noqa: E501
        :type: str
        """

        self._cve = cve

    @property
    def deployments_count(self):
        """Gets the deployments_count of this RemediationDetailsResponse.  # noqa: E501


        :return: The deployments_count of this RemediationDetailsResponse.  # noqa: E501
        :rtype: DeploymentsCount
        """
        return self._deployments_count

    @deployments_count.setter
    def deployments_count(self, deployments_count):
        """Sets the deployments_count of this RemediationDetailsResponse.


        :param deployments_count: The deployments_count of this RemediationDetailsResponse.  # noqa: E501
        :type: DeploymentsCount
        """
        if deployments_count is None:
            raise ValueError("Invalid value for `deployments_count`, must not be `None`")  # noqa: E501

        self._deployments_count = deployments_count

    @property
    def end_time_milli(self):
        """Gets the end_time_milli of this RemediationDetailsResponse.  # noqa: E501


        :return: The end_time_milli of this RemediationDetailsResponse.  # noqa: E501
        :rtype: int
        """
        return self._end_time_milli

    @end_time_milli.setter
    def end_time_milli(self, end_time_milli):
        """Sets the end_time_milli of this RemediationDetailsResponse.


        :param end_time_milli: The end_time_milli of this RemediationDetailsResponse.  # noqa: E501
        :type: int
        """

        self._end_time_milli = end_time_milli

    @property
    def environments(self):
        """Gets the environments of this RemediationDetailsResponse.  # noqa: E501

        Total environments included in the tracker.  # noqa: E501

        :return: The environments of this RemediationDetailsResponse.  # noqa: E501
        :rtype: int
        """
        return self._environments

    @environments.setter
    def environments(self, environments):
        """Sets the environments of this RemediationDetailsResponse.

        Total environments included in the tracker.  # noqa: E501

        :param environments: The environments of this RemediationDetailsResponse.  # noqa: E501
        :type: int
        """
        if environments is None:
            raise ValueError("Invalid value for `environments`, must not be `None`")  # noqa: E501

        self._environments = environments

    @property
    def id(self):
        """Gets the id of this RemediationDetailsResponse.  # noqa: E501

        Remediation Id.  # noqa: E501

        :return: The id of this RemediationDetailsResponse.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this RemediationDetailsResponse.

        Remediation Id.  # noqa: E501

        :param id: The id of this RemediationDetailsResponse.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def new_artifacts_count(self):
        """Gets the new_artifacts_count of this RemediationDetailsResponse.  # noqa: E501

        Total Number of New Artifacts.  # noqa: E501

        :return: The new_artifacts_count of this RemediationDetailsResponse.  # noqa: E501
        :rtype: int
        """
        return self._new_artifacts_count

    @new_artifacts_count.setter
    def new_artifacts_count(self, new_artifacts_count):
        """Sets the new_artifacts_count of this RemediationDetailsResponse.

        Total Number of New Artifacts.  # noqa: E501

        :param new_artifacts_count: The new_artifacts_count of this RemediationDetailsResponse.  # noqa: E501
        :type: int
        """
        if new_artifacts_count is None:
            raise ValueError("Invalid value for `new_artifacts_count`, must not be `None`")  # noqa: E501

        self._new_artifacts_count = new_artifacts_count

    @property
    def new_environments_count(self):
        """Gets the new_environments_count of this RemediationDetailsResponse.  # noqa: E501

        Total Number of New Environments.  # noqa: E501

        :return: The new_environments_count of this RemediationDetailsResponse.  # noqa: E501
        :rtype: int
        """
        return self._new_environments_count

    @new_environments_count.setter
    def new_environments_count(self, new_environments_count):
        """Sets the new_environments_count of this RemediationDetailsResponse.

        Total Number of New Environments.  # noqa: E501

        :param new_environments_count: The new_environments_count of this RemediationDetailsResponse.  # noqa: E501
        :type: int
        """
        if new_environments_count is None:
            raise ValueError("Invalid value for `new_environments_count`, must not be `None`")  # noqa: E501

        self._new_environments_count = new_environments_count

    @property
    def remediation_condition(self):
        """Gets the remediation_condition of this RemediationDetailsResponse.  # noqa: E501


        :return: The remediation_condition of this RemediationDetailsResponse.  # noqa: E501
        :rtype: RemediationCondition
        """
        return self._remediation_condition

    @remediation_condition.setter
    def remediation_condition(self, remediation_condition):
        """Sets the remediation_condition of this RemediationDetailsResponse.


        :param remediation_condition: The remediation_condition of this RemediationDetailsResponse.  # noqa: E501
        :type: RemediationCondition
        """
        if remediation_condition is None:
            raise ValueError("Invalid value for `remediation_condition`, must not be `None`")  # noqa: E501

        self._remediation_condition = remediation_condition

    @property
    def severity(self):
        """Gets the severity of this RemediationDetailsResponse.  # noqa: E501


        :return: The severity of this RemediationDetailsResponse.  # noqa: E501
        :rtype: VulnerabilitySeverity
        """
        return self._severity

    @severity.setter
    def severity(self, severity):
        """Sets the severity of this RemediationDetailsResponse.


        :param severity: The severity of this RemediationDetailsResponse.  # noqa: E501
        :type: VulnerabilitySeverity
        """
        if severity is None:
            raise ValueError("Invalid value for `severity`, must not be `None`")  # noqa: E501

        self._severity = severity

    @property
    def start_time_milli(self):
        """Gets the start_time_milli of this RemediationDetailsResponse.  # noqa: E501


        :return: The start_time_milli of this RemediationDetailsResponse.  # noqa: E501
        :rtype: int
        """
        return self._start_time_milli

    @start_time_milli.setter
    def start_time_milli(self, start_time_milli):
        """Sets the start_time_milli of this RemediationDetailsResponse.


        :param start_time_milli: The start_time_milli of this RemediationDetailsResponse.  # noqa: E501
        :type: int
        """
        if start_time_milli is None:
            raise ValueError("Invalid value for `start_time_milli`, must not be `None`")  # noqa: E501

        self._start_time_milli = start_time_milli

    @property
    def status(self):
        """Gets the status of this RemediationDetailsResponse.  # noqa: E501


        :return: The status of this RemediationDetailsResponse.  # noqa: E501
        :rtype: RemediationStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this RemediationDetailsResponse.


        :param status: The status of this RemediationDetailsResponse.  # noqa: E501
        :type: RemediationStatus
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def target_date(self):
        """Gets the target_date of this RemediationDetailsResponse.  # noqa: E501

        End date set by the user.  # noqa: E501

        :return: The target_date of this RemediationDetailsResponse.  # noqa: E501
        :rtype: str
        """
        return self._target_date

    @target_date.setter
    def target_date(self, target_date):
        """Sets the target_date of this RemediationDetailsResponse.

        End date set by the user.  # noqa: E501

        :param target_date: The target_date of this RemediationDetailsResponse.  # noqa: E501
        :type: str
        """

        self._target_date = target_date

    @property
    def ticket(self):
        """Gets the ticket of this RemediationDetailsResponse.  # noqa: E501


        :return: The ticket of this RemediationDetailsResponse.  # noqa: E501
        :rtype: TicketInfo
        """
        return self._ticket

    @ticket.setter
    def ticket(self, ticket):
        """Sets the ticket of this RemediationDetailsResponse.


        :param ticket: The ticket of this RemediationDetailsResponse.  # noqa: E501
        :type: TicketInfo
        """

        self._ticket = ticket

    @property
    def vulnerability_description(self):
        """Gets the vulnerability_description of this RemediationDetailsResponse.  # noqa: E501

        Details of the vulnerability.  # noqa: E501

        :return: The vulnerability_description of this RemediationDetailsResponse.  # noqa: E501
        :rtype: str
        """
        return self._vulnerability_description

    @vulnerability_description.setter
    def vulnerability_description(self, vulnerability_description):
        """Sets the vulnerability_description of this RemediationDetailsResponse.

        Details of the vulnerability.  # noqa: E501

        :param vulnerability_description: The vulnerability_description of this RemediationDetailsResponse.  # noqa: E501
        :type: str
        """

        self._vulnerability_description = vulnerability_description

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
        if issubclass(RemediationDetailsResponse, dict):
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
        if not isinstance(other, RemediationDetailsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
