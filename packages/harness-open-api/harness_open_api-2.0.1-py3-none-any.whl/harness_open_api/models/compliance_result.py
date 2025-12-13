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

class ComplianceResult(object):
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
        'category': 'str',
        'category_id': 'str',
        'compliance_id': 'str',
        'compliance_val': 'int',
        'description': 'str',
        'entity': 'ComplianceCheckEntityType',
        'occurrences': 'list[ComplianceOccurrenceDTO]',
        'reason': 'str',
        'remediation': 'str',
        'severity': 'ComplianceCheckSeverity',
        'standards': 'list[ComplianceStandardType]',
        'status': 'ComplianceResultStatus',
        'sub_category': 'str',
        'sub_category_id': 'str',
        'tags': 'list[str]',
        'title': 'str',
        'url': 'str'
    }

    attribute_map = {
        'category': 'category',
        'category_id': 'category_id',
        'compliance_id': 'compliance_id',
        'compliance_val': 'compliance_val',
        'description': 'description',
        'entity': 'entity',
        'occurrences': 'occurrences',
        'reason': 'reason',
        'remediation': 'remediation',
        'severity': 'severity',
        'standards': 'standards',
        'status': 'status',
        'sub_category': 'sub_category',
        'sub_category_id': 'sub_category_id',
        'tags': 'tags',
        'title': 'title',
        'url': 'url'
    }

    def __init__(self, category=None, category_id=None, compliance_id=None, compliance_val=None, description=None, entity=None, occurrences=None, reason=None, remediation=None, severity=None, standards=None, status=None, sub_category=None, sub_category_id=None, tags=None, title=None, url=None):  # noqa: E501
        """ComplianceResult - a model defined in Swagger"""  # noqa: E501
        self._category = None
        self._category_id = None
        self._compliance_id = None
        self._compliance_val = None
        self._description = None
        self._entity = None
        self._occurrences = None
        self._reason = None
        self._remediation = None
        self._severity = None
        self._standards = None
        self._status = None
        self._sub_category = None
        self._sub_category_id = None
        self._tags = None
        self._title = None
        self._url = None
        self.discriminator = None
        self.category = category
        self.category_id = category_id
        self.compliance_id = compliance_id
        self.compliance_val = compliance_val
        if description is not None:
            self.description = description
        self.entity = entity
        if occurrences is not None:
            self.occurrences = occurrences
        self.reason = reason
        self.remediation = remediation
        self.severity = severity
        self.standards = standards
        self.status = status
        self.sub_category = sub_category
        self.sub_category_id = sub_category_id
        if tags is not None:
            self.tags = tags
        if title is not None:
            self.title = title
        if url is not None:
            self.url = url

    @property
    def category(self):
        """Gets the category of this ComplianceResult.  # noqa: E501


        :return: The category of this ComplianceResult.  # noqa: E501
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this ComplianceResult.


        :param category: The category of this ComplianceResult.  # noqa: E501
        :type: str
        """
        if category is None:
            raise ValueError("Invalid value for `category`, must not be `None`")  # noqa: E501

        self._category = category

    @property
    def category_id(self):
        """Gets the category_id of this ComplianceResult.  # noqa: E501


        :return: The category_id of this ComplianceResult.  # noqa: E501
        :rtype: str
        """
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        """Sets the category_id of this ComplianceResult.


        :param category_id: The category_id of this ComplianceResult.  # noqa: E501
        :type: str
        """
        if category_id is None:
            raise ValueError("Invalid value for `category_id`, must not be `None`")  # noqa: E501

        self._category_id = category_id

    @property
    def compliance_id(self):
        """Gets the compliance_id of this ComplianceResult.  # noqa: E501


        :return: The compliance_id of this ComplianceResult.  # noqa: E501
        :rtype: str
        """
        return self._compliance_id

    @compliance_id.setter
    def compliance_id(self, compliance_id):
        """Sets the compliance_id of this ComplianceResult.


        :param compliance_id: The compliance_id of this ComplianceResult.  # noqa: E501
        :type: str
        """
        if compliance_id is None:
            raise ValueError("Invalid value for `compliance_id`, must not be `None`")  # noqa: E501

        self._compliance_id = compliance_id

    @property
    def compliance_val(self):
        """Gets the compliance_val of this ComplianceResult.  # noqa: E501


        :return: The compliance_val of this ComplianceResult.  # noqa: E501
        :rtype: int
        """
        return self._compliance_val

    @compliance_val.setter
    def compliance_val(self, compliance_val):
        """Sets the compliance_val of this ComplianceResult.


        :param compliance_val: The compliance_val of this ComplianceResult.  # noqa: E501
        :type: int
        """
        if compliance_val is None:
            raise ValueError("Invalid value for `compliance_val`, must not be `None`")  # noqa: E501

        self._compliance_val = compliance_val

    @property
    def description(self):
        """Gets the description of this ComplianceResult.  # noqa: E501


        :return: The description of this ComplianceResult.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ComplianceResult.


        :param description: The description of this ComplianceResult.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def entity(self):
        """Gets the entity of this ComplianceResult.  # noqa: E501


        :return: The entity of this ComplianceResult.  # noqa: E501
        :rtype: ComplianceCheckEntityType
        """
        return self._entity

    @entity.setter
    def entity(self, entity):
        """Sets the entity of this ComplianceResult.


        :param entity: The entity of this ComplianceResult.  # noqa: E501
        :type: ComplianceCheckEntityType
        """
        if entity is None:
            raise ValueError("Invalid value for `entity`, must not be `None`")  # noqa: E501

        self._entity = entity

    @property
    def occurrences(self):
        """Gets the occurrences of this ComplianceResult.  # noqa: E501


        :return: The occurrences of this ComplianceResult.  # noqa: E501
        :rtype: list[ComplianceOccurrenceDTO]
        """
        return self._occurrences

    @occurrences.setter
    def occurrences(self, occurrences):
        """Sets the occurrences of this ComplianceResult.


        :param occurrences: The occurrences of this ComplianceResult.  # noqa: E501
        :type: list[ComplianceOccurrenceDTO]
        """

        self._occurrences = occurrences

    @property
    def reason(self):
        """Gets the reason of this ComplianceResult.  # noqa: E501


        :return: The reason of this ComplianceResult.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this ComplianceResult.


        :param reason: The reason of this ComplianceResult.  # noqa: E501
        :type: str
        """
        if reason is None:
            raise ValueError("Invalid value for `reason`, must not be `None`")  # noqa: E501

        self._reason = reason

    @property
    def remediation(self):
        """Gets the remediation of this ComplianceResult.  # noqa: E501


        :return: The remediation of this ComplianceResult.  # noqa: E501
        :rtype: str
        """
        return self._remediation

    @remediation.setter
    def remediation(self, remediation):
        """Sets the remediation of this ComplianceResult.


        :param remediation: The remediation of this ComplianceResult.  # noqa: E501
        :type: str
        """
        if remediation is None:
            raise ValueError("Invalid value for `remediation`, must not be `None`")  # noqa: E501

        self._remediation = remediation

    @property
    def severity(self):
        """Gets the severity of this ComplianceResult.  # noqa: E501


        :return: The severity of this ComplianceResult.  # noqa: E501
        :rtype: ComplianceCheckSeverity
        """
        return self._severity

    @severity.setter
    def severity(self, severity):
        """Sets the severity of this ComplianceResult.


        :param severity: The severity of this ComplianceResult.  # noqa: E501
        :type: ComplianceCheckSeverity
        """
        if severity is None:
            raise ValueError("Invalid value for `severity`, must not be `None`")  # noqa: E501

        self._severity = severity

    @property
    def standards(self):
        """Gets the standards of this ComplianceResult.  # noqa: E501


        :return: The standards of this ComplianceResult.  # noqa: E501
        :rtype: list[ComplianceStandardType]
        """
        return self._standards

    @standards.setter
    def standards(self, standards):
        """Sets the standards of this ComplianceResult.


        :param standards: The standards of this ComplianceResult.  # noqa: E501
        :type: list[ComplianceStandardType]
        """
        if standards is None:
            raise ValueError("Invalid value for `standards`, must not be `None`")  # noqa: E501

        self._standards = standards

    @property
    def status(self):
        """Gets the status of this ComplianceResult.  # noqa: E501


        :return: The status of this ComplianceResult.  # noqa: E501
        :rtype: ComplianceResultStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ComplianceResult.


        :param status: The status of this ComplianceResult.  # noqa: E501
        :type: ComplianceResultStatus
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def sub_category(self):
        """Gets the sub_category of this ComplianceResult.  # noqa: E501


        :return: The sub_category of this ComplianceResult.  # noqa: E501
        :rtype: str
        """
        return self._sub_category

    @sub_category.setter
    def sub_category(self, sub_category):
        """Sets the sub_category of this ComplianceResult.


        :param sub_category: The sub_category of this ComplianceResult.  # noqa: E501
        :type: str
        """
        if sub_category is None:
            raise ValueError("Invalid value for `sub_category`, must not be `None`")  # noqa: E501

        self._sub_category = sub_category

    @property
    def sub_category_id(self):
        """Gets the sub_category_id of this ComplianceResult.  # noqa: E501


        :return: The sub_category_id of this ComplianceResult.  # noqa: E501
        :rtype: str
        """
        return self._sub_category_id

    @sub_category_id.setter
    def sub_category_id(self, sub_category_id):
        """Sets the sub_category_id of this ComplianceResult.


        :param sub_category_id: The sub_category_id of this ComplianceResult.  # noqa: E501
        :type: str
        """
        if sub_category_id is None:
            raise ValueError("Invalid value for `sub_category_id`, must not be `None`")  # noqa: E501

        self._sub_category_id = sub_category_id

    @property
    def tags(self):
        """Gets the tags of this ComplianceResult.  # noqa: E501


        :return: The tags of this ComplianceResult.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this ComplianceResult.


        :param tags: The tags of this ComplianceResult.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def title(self):
        """Gets the title of this ComplianceResult.  # noqa: E501


        :return: The title of this ComplianceResult.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this ComplianceResult.


        :param title: The title of this ComplianceResult.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def url(self):
        """Gets the url of this ComplianceResult.  # noqa: E501


        :return: The url of this ComplianceResult.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this ComplianceResult.


        :param url: The url of this ComplianceResult.  # noqa: E501
        :type: str
        """

        self._url = url

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
        if issubclass(ComplianceResult, dict):
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
        if not isinstance(other, ComplianceResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
