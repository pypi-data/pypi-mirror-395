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

class CreateExemptionRequestBody(object):
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
        'exempt_future_occurrences': 'bool',
        'expiration': 'int',
        'issue_id': 'str',
        'link': 'str',
        'occurrences': 'list[int]',
        'pending_changes': 'PendingChanges',
        'pipeline_id': 'str',
        'reason': 'str',
        'requester_email': 'str',
        'requester_id': 'str',
        'requester_name': 'str',
        'scan_id': 'str',
        'search': 'str',
        'target_id': 'str',
        'type': 'str'
    }

    attribute_map = {
        'exempt_future_occurrences': 'exemptFutureOccurrences',
        'expiration': 'expiration',
        'issue_id': 'issueId',
        'link': 'link',
        'occurrences': 'occurrences',
        'pending_changes': 'pendingChanges',
        'pipeline_id': 'pipelineId',
        'reason': 'reason',
        'requester_email': 'requesterEmail',
        'requester_id': 'requesterId',
        'requester_name': 'requesterName',
        'scan_id': 'scanId',
        'search': 'search',
        'target_id': 'targetId',
        'type': 'type'
    }

    def __init__(self, exempt_future_occurrences=True, expiration=None, issue_id=None, link=None, occurrences=None, pending_changes=None, pipeline_id=None, reason=None, requester_email=None, requester_id=None, requester_name=None, scan_id=None, search=None, target_id=None, type=None):  # noqa: E501
        """CreateExemptionRequestBody - a model defined in Swagger"""  # noqa: E501
        self._exempt_future_occurrences = None
        self._expiration = None
        self._issue_id = None
        self._link = None
        self._occurrences = None
        self._pending_changes = None
        self._pipeline_id = None
        self._reason = None
        self._requester_email = None
        self._requester_id = None
        self._requester_name = None
        self._scan_id = None
        self._search = None
        self._target_id = None
        self._type = None
        self.discriminator = None
        if exempt_future_occurrences is not None:
            self.exempt_future_occurrences = exempt_future_occurrences
        if expiration is not None:
            self.expiration = expiration
        self.issue_id = issue_id
        if link is not None:
            self.link = link
        if occurrences is not None:
            self.occurrences = occurrences
        self.pending_changes = pending_changes
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        self.reason = reason
        if requester_email is not None:
            self.requester_email = requester_email
        self.requester_id = requester_id
        if requester_name is not None:
            self.requester_name = requester_name
        if scan_id is not None:
            self.scan_id = scan_id
        if search is not None:
            self.search = search
        if target_id is not None:
            self.target_id = target_id
        self.type = type

    @property
    def exempt_future_occurrences(self):
        """Gets the exempt_future_occurrences of this CreateExemptionRequestBody.  # noqa: E501

        States if the user wants to exempt future occurrences of the issue  # noqa: E501

        :return: The exempt_future_occurrences of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: bool
        """
        return self._exempt_future_occurrences

    @exempt_future_occurrences.setter
    def exempt_future_occurrences(self, exempt_future_occurrences):
        """Sets the exempt_future_occurrences of this CreateExemptionRequestBody.

        States if the user wants to exempt future occurrences of the issue  # noqa: E501

        :param exempt_future_occurrences: The exempt_future_occurrences of this CreateExemptionRequestBody.  # noqa: E501
        :type: bool
        """

        self._exempt_future_occurrences = exempt_future_occurrences

    @property
    def expiration(self):
        """Gets the expiration of this CreateExemptionRequestBody.  # noqa: E501

        Unix timestamp at which this Exemption will expire  # noqa: E501

        :return: The expiration of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: int
        """
        return self._expiration

    @expiration.setter
    def expiration(self, expiration):
        """Sets the expiration of this CreateExemptionRequestBody.

        Unix timestamp at which this Exemption will expire  # noqa: E501

        :param expiration: The expiration of this CreateExemptionRequestBody.  # noqa: E501
        :type: int
        """

        self._expiration = expiration

    @property
    def issue_id(self):
        """Gets the issue_id of this CreateExemptionRequestBody.  # noqa: E501

        Issue ID associated with the Exemption  # noqa: E501

        :return: The issue_id of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._issue_id

    @issue_id.setter
    def issue_id(self, issue_id):
        """Sets the issue_id of this CreateExemptionRequestBody.

        Issue ID associated with the Exemption  # noqa: E501

        :param issue_id: The issue_id of this CreateExemptionRequestBody.  # noqa: E501
        :type: str
        """
        if issue_id is None:
            raise ValueError("Invalid value for `issue_id`, must not be `None`")  # noqa: E501

        self._issue_id = issue_id

    @property
    def link(self):
        """Gets the link of this CreateExemptionRequestBody.  # noqa: E501

        Link to a related ticket  # noqa: E501

        :return: The link of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._link

    @link.setter
    def link(self, link):
        """Sets the link of this CreateExemptionRequestBody.

        Link to a related ticket  # noqa: E501

        :param link: The link of this CreateExemptionRequestBody.  # noqa: E501
        :type: str
        """

        self._link = link

    @property
    def occurrences(self):
        """Gets the occurrences of this CreateExemptionRequestBody.  # noqa: E501

        Array of occurrence Ids  # noqa: E501

        :return: The occurrences of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: list[int]
        """
        return self._occurrences

    @occurrences.setter
    def occurrences(self, occurrences):
        """Sets the occurrences of this CreateExemptionRequestBody.

        Array of occurrence Ids  # noqa: E501

        :param occurrences: The occurrences of this CreateExemptionRequestBody.  # noqa: E501
        :type: list[int]
        """

        self._occurrences = occurrences

    @property
    def pending_changes(self):
        """Gets the pending_changes of this CreateExemptionRequestBody.  # noqa: E501


        :return: The pending_changes of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: PendingChanges
        """
        return self._pending_changes

    @pending_changes.setter
    def pending_changes(self, pending_changes):
        """Sets the pending_changes of this CreateExemptionRequestBody.


        :param pending_changes: The pending_changes of this CreateExemptionRequestBody.  # noqa: E501
        :type: PendingChanges
        """
        if pending_changes is None:
            raise ValueError("Invalid value for `pending_changes`, must not be `None`")  # noqa: E501

        self._pending_changes = pending_changes

    @property
    def pipeline_id(self):
        """Gets the pipeline_id of this CreateExemptionRequestBody.  # noqa: E501

        ID of the Harness Pipeline to which the exemption applies. You must also specify \"projectId\" and \"orgId\". Cannot be specified alongside \"targetId\".  # noqa: E501

        :return: The pipeline_id of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_id

    @pipeline_id.setter
    def pipeline_id(self, pipeline_id):
        """Sets the pipeline_id of this CreateExemptionRequestBody.

        ID of the Harness Pipeline to which the exemption applies. You must also specify \"projectId\" and \"orgId\". Cannot be specified alongside \"targetId\".  # noqa: E501

        :param pipeline_id: The pipeline_id of this CreateExemptionRequestBody.  # noqa: E501
        :type: str
        """

        self._pipeline_id = pipeline_id

    @property
    def reason(self):
        """Gets the reason of this CreateExemptionRequestBody.  # noqa: E501

        Text describing why this Exemption is necessary  # noqa: E501

        :return: The reason of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this CreateExemptionRequestBody.

        Text describing why this Exemption is necessary  # noqa: E501

        :param reason: The reason of this CreateExemptionRequestBody.  # noqa: E501
        :type: str
        """
        if reason is None:
            raise ValueError("Invalid value for `reason`, must not be `None`")  # noqa: E501

        self._reason = reason

    @property
    def requester_email(self):
        """Gets the requester_email of this CreateExemptionRequestBody.  # noqa: E501

        Email of the user who requested this Exemption  # noqa: E501

        :return: The requester_email of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._requester_email

    @requester_email.setter
    def requester_email(self, requester_email):
        """Sets the requester_email of this CreateExemptionRequestBody.

        Email of the user who requested this Exemption  # noqa: E501

        :param requester_email: The requester_email of this CreateExemptionRequestBody.  # noqa: E501
        :type: str
        """

        self._requester_email = requester_email

    @property
    def requester_id(self):
        """Gets the requester_id of this CreateExemptionRequestBody.  # noqa: E501

        User ID of the user who requested this Exemption  # noqa: E501

        :return: The requester_id of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._requester_id

    @requester_id.setter
    def requester_id(self, requester_id):
        """Sets the requester_id of this CreateExemptionRequestBody.

        User ID of the user who requested this Exemption  # noqa: E501

        :param requester_id: The requester_id of this CreateExemptionRequestBody.  # noqa: E501
        :type: str
        """
        if requester_id is None:
            raise ValueError("Invalid value for `requester_id`, must not be `None`")  # noqa: E501

        self._requester_id = requester_id

    @property
    def requester_name(self):
        """Gets the requester_name of this CreateExemptionRequestBody.  # noqa: E501

        Name of the user who requested this Exemption  # noqa: E501

        :return: The requester_name of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._requester_name

    @requester_name.setter
    def requester_name(self, requester_name):
        """Sets the requester_name of this CreateExemptionRequestBody.

        Name of the user who requested this Exemption  # noqa: E501

        :param requester_name: The requester_name of this CreateExemptionRequestBody.  # noqa: E501
        :type: str
        """

        self._requester_name = requester_name

    @property
    def scan_id(self):
        """Gets the scan_id of this CreateExemptionRequestBody.  # noqa: E501

        ID of the Harness Scan to determine all the occurrences for the scan-issue. You must also specify \"projectId\", \"orgId\" and \"targetId\". Cannot be specified alongside \"pipelineId\".  # noqa: E501

        :return: The scan_id of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._scan_id

    @scan_id.setter
    def scan_id(self, scan_id):
        """Sets the scan_id of this CreateExemptionRequestBody.

        ID of the Harness Scan to determine all the occurrences for the scan-issue. You must also specify \"projectId\", \"orgId\" and \"targetId\". Cannot be specified alongside \"pipelineId\".  # noqa: E501

        :param scan_id: The scan_id of this CreateExemptionRequestBody.  # noqa: E501
        :type: str
        """

        self._scan_id = scan_id

    @property
    def search(self):
        """Gets the search of this CreateExemptionRequestBody.  # noqa: E501

        Search parameter to find filtered occurrences of the issue  # noqa: E501

        :return: The search of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._search

    @search.setter
    def search(self, search):
        """Sets the search of this CreateExemptionRequestBody.

        Search parameter to find filtered occurrences of the issue  # noqa: E501

        :param search: The search of this CreateExemptionRequestBody.  # noqa: E501
        :type: str
        """

        self._search = search

    @property
    def target_id(self):
        """Gets the target_id of this CreateExemptionRequestBody.  # noqa: E501

        ID of the Target to which the exemption applies. Cannot be specified alongside \"projectId\" or \"pipelineId\".  # noqa: E501

        :return: The target_id of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """Sets the target_id of this CreateExemptionRequestBody.

        ID of the Target to which the exemption applies. Cannot be specified alongside \"projectId\" or \"pipelineId\".  # noqa: E501

        :param target_id: The target_id of this CreateExemptionRequestBody.  # noqa: E501
        :type: str
        """

        self._target_id = target_id

    @property
    def type(self):
        """Gets the type of this CreateExemptionRequestBody.  # noqa: E501

        Type of Exemption (Compensating Controls / Acceptable Use / Acceptable Risk / False Positive / Fix Unavailable / Other)  # noqa: E501

        :return: The type of this CreateExemptionRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CreateExemptionRequestBody.

        Type of Exemption (Compensating Controls / Acceptable Use / Acceptable Risk / False Positive / Fix Unavailable / Other)  # noqa: E501

        :param type: The type of this CreateExemptionRequestBody.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["Compensating Controls", "Acceptable Use", "Acceptable Risk", "False Positive", "Fix Unavailable", "Other"]  # noqa: E501
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
        if issubclass(CreateExemptionRequestBody, dict):
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
        if not isinstance(other, CreateExemptionRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
