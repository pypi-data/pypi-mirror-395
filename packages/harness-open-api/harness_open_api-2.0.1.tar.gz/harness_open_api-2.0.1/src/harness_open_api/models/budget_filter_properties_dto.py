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

class BudgetFilterPropertiesDTO(object):
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
        'created_by': 'str',
        'folder_ids': 'list[str]',
        'last_modified_end_time': 'int',
        'last_modified_start_time': 'int',
        'limit': 'int',
        'max_budget_amount': 'float',
        'min_budget_amount': 'float',
        'offset': 'int',
        'period': 'str',
        'perspective_id': 'str',
        'search_key': 'str'
    }

    attribute_map = {
        'created_by': 'createdBy',
        'folder_ids': 'folderIds',
        'last_modified_end_time': 'lastModifiedEndTime',
        'last_modified_start_time': 'lastModifiedStartTime',
        'limit': 'limit',
        'max_budget_amount': 'maxBudgetAmount',
        'min_budget_amount': 'minBudgetAmount',
        'offset': 'offset',
        'period': 'period',
        'perspective_id': 'perspectiveId',
        'search_key': 'searchKey'
    }

    def __init__(self, created_by=None, folder_ids=None, last_modified_end_time=None, last_modified_start_time=None, limit=None, max_budget_amount=None, min_budget_amount=None, offset=None, period=None, perspective_id=None, search_key=None):  # noqa: E501
        """BudgetFilterPropertiesDTO - a model defined in Swagger"""  # noqa: E501
        self._created_by = None
        self._folder_ids = None
        self._last_modified_end_time = None
        self._last_modified_start_time = None
        self._limit = None
        self._max_budget_amount = None
        self._min_budget_amount = None
        self._offset = None
        self._period = None
        self._perspective_id = None
        self._search_key = None
        self.discriminator = None
        if created_by is not None:
            self.created_by = created_by
        if folder_ids is not None:
            self.folder_ids = folder_ids
        if last_modified_end_time is not None:
            self.last_modified_end_time = last_modified_end_time
        if last_modified_start_time is not None:
            self.last_modified_start_time = last_modified_start_time
        if limit is not None:
            self.limit = limit
        if max_budget_amount is not None:
            self.max_budget_amount = max_budget_amount
        if min_budget_amount is not None:
            self.min_budget_amount = min_budget_amount
        if offset is not None:
            self.offset = offset
        if period is not None:
            self.period = period
        if perspective_id is not None:
            self.perspective_id = perspective_id
        if search_key is not None:
            self.search_key = search_key

    @property
    def created_by(self):
        """Gets the created_by of this BudgetFilterPropertiesDTO.  # noqa: E501

        Filter by creator user ID  # noqa: E501

        :return: The created_by of this BudgetFilterPropertiesDTO.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this BudgetFilterPropertiesDTO.

        Filter by creator user ID  # noqa: E501

        :param created_by: The created_by of this BudgetFilterPropertiesDTO.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def folder_ids(self):
        """Gets the folder_ids of this BudgetFilterPropertiesDTO.  # noqa: E501

        Filter by multiple folder IDs  # noqa: E501

        :return: The folder_ids of this BudgetFilterPropertiesDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._folder_ids

    @folder_ids.setter
    def folder_ids(self, folder_ids):
        """Sets the folder_ids of this BudgetFilterPropertiesDTO.

        Filter by multiple folder IDs  # noqa: E501

        :param folder_ids: The folder_ids of this BudgetFilterPropertiesDTO.  # noqa: E501
        :type: list[str]
        """

        self._folder_ids = folder_ids

    @property
    def last_modified_end_time(self):
        """Gets the last_modified_end_time of this BudgetFilterPropertiesDTO.  # noqa: E501

        End time for last modified filter (timestamp in milliseconds)  # noqa: E501

        :return: The last_modified_end_time of this BudgetFilterPropertiesDTO.  # noqa: E501
        :rtype: int
        """
        return self._last_modified_end_time

    @last_modified_end_time.setter
    def last_modified_end_time(self, last_modified_end_time):
        """Sets the last_modified_end_time of this BudgetFilterPropertiesDTO.

        End time for last modified filter (timestamp in milliseconds)  # noqa: E501

        :param last_modified_end_time: The last_modified_end_time of this BudgetFilterPropertiesDTO.  # noqa: E501
        :type: int
        """

        self._last_modified_end_time = last_modified_end_time

    @property
    def last_modified_start_time(self):
        """Gets the last_modified_start_time of this BudgetFilterPropertiesDTO.  # noqa: E501

        Start time for last modified filter (timestamp in milliseconds)  # noqa: E501

        :return: The last_modified_start_time of this BudgetFilterPropertiesDTO.  # noqa: E501
        :rtype: int
        """
        return self._last_modified_start_time

    @last_modified_start_time.setter
    def last_modified_start_time(self, last_modified_start_time):
        """Sets the last_modified_start_time of this BudgetFilterPropertiesDTO.

        Start time for last modified filter (timestamp in milliseconds)  # noqa: E501

        :param last_modified_start_time: The last_modified_start_time of this BudgetFilterPropertiesDTO.  # noqa: E501
        :type: int
        """

        self._last_modified_start_time = last_modified_start_time

    @property
    def limit(self):
        """Gets the limit of this BudgetFilterPropertiesDTO.  # noqa: E501

        Maximum number of results to return  # noqa: E501

        :return: The limit of this BudgetFilterPropertiesDTO.  # noqa: E501
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this BudgetFilterPropertiesDTO.

        Maximum number of results to return  # noqa: E501

        :param limit: The limit of this BudgetFilterPropertiesDTO.  # noqa: E501
        :type: int
        """

        self._limit = limit

    @property
    def max_budget_amount(self):
        """Gets the max_budget_amount of this BudgetFilterPropertiesDTO.  # noqa: E501

        Maximum budget amount  # noqa: E501

        :return: The max_budget_amount of this BudgetFilterPropertiesDTO.  # noqa: E501
        :rtype: float
        """
        return self._max_budget_amount

    @max_budget_amount.setter
    def max_budget_amount(self, max_budget_amount):
        """Sets the max_budget_amount of this BudgetFilterPropertiesDTO.

        Maximum budget amount  # noqa: E501

        :param max_budget_amount: The max_budget_amount of this BudgetFilterPropertiesDTO.  # noqa: E501
        :type: float
        """

        self._max_budget_amount = max_budget_amount

    @property
    def min_budget_amount(self):
        """Gets the min_budget_amount of this BudgetFilterPropertiesDTO.  # noqa: E501

        Minimum budget amount  # noqa: E501

        :return: The min_budget_amount of this BudgetFilterPropertiesDTO.  # noqa: E501
        :rtype: float
        """
        return self._min_budget_amount

    @min_budget_amount.setter
    def min_budget_amount(self, min_budget_amount):
        """Sets the min_budget_amount of this BudgetFilterPropertiesDTO.

        Minimum budget amount  # noqa: E501

        :param min_budget_amount: The min_budget_amount of this BudgetFilterPropertiesDTO.  # noqa: E501
        :type: float
        """

        self._min_budget_amount = min_budget_amount

    @property
    def offset(self):
        """Gets the offset of this BudgetFilterPropertiesDTO.  # noqa: E501

        Number of results to skip  # noqa: E501

        :return: The offset of this BudgetFilterPropertiesDTO.  # noqa: E501
        :rtype: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this BudgetFilterPropertiesDTO.

        Number of results to skip  # noqa: E501

        :param offset: The offset of this BudgetFilterPropertiesDTO.  # noqa: E501
        :type: int
        """

        self._offset = offset

    @property
    def period(self):
        """Gets the period of this BudgetFilterPropertiesDTO.  # noqa: E501

        Filter by budget period  # noqa: E501

        :return: The period of this BudgetFilterPropertiesDTO.  # noqa: E501
        :rtype: str
        """
        return self._period

    @period.setter
    def period(self, period):
        """Sets the period of this BudgetFilterPropertiesDTO.

        Filter by budget period  # noqa: E501

        :param period: The period of this BudgetFilterPropertiesDTO.  # noqa: E501
        :type: str
        """
        allowed_values = ["DAILY", "WEEKLY", "MONTHLY", "QUARTERLY", "YEARLY"]  # noqa: E501
        if period not in allowed_values:
            raise ValueError(
                "Invalid value for `period` ({0}), must be one of {1}"  # noqa: E501
                .format(period, allowed_values)
            )

        self._period = period

    @property
    def perspective_id(self):
        """Gets the perspective_id of this BudgetFilterPropertiesDTO.  # noqa: E501

        Filter by perspective ID  # noqa: E501

        :return: The perspective_id of this BudgetFilterPropertiesDTO.  # noqa: E501
        :rtype: str
        """
        return self._perspective_id

    @perspective_id.setter
    def perspective_id(self, perspective_id):
        """Sets the perspective_id of this BudgetFilterPropertiesDTO.

        Filter by perspective ID  # noqa: E501

        :param perspective_id: The perspective_id of this BudgetFilterPropertiesDTO.  # noqa: E501
        :type: str
        """

        self._perspective_id = perspective_id

    @property
    def search_key(self):
        """Gets the search_key of this BudgetFilterPropertiesDTO.  # noqa: E501

        Search text to filter budgets by name (case-insensitive)  # noqa: E501

        :return: The search_key of this BudgetFilterPropertiesDTO.  # noqa: E501
        :rtype: str
        """
        return self._search_key

    @search_key.setter
    def search_key(self, search_key):
        """Sets the search_key of this BudgetFilterPropertiesDTO.

        Search text to filter budgets by name (case-insensitive)  # noqa: E501

        :param search_key: The search_key of this BudgetFilterPropertiesDTO.  # noqa: E501
        :type: str
        """

        self._search_key = search_key

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
        if issubclass(BudgetFilterPropertiesDTO, dict):
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
        if not isinstance(other, BudgetFilterPropertiesDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
