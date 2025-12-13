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

class DashboardFilter(object):
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
        'dashboard_id': 'str',
        'default_value': 'str',
        'explore': 'str',
        'id': 'str',
        'model': 'str',
        'name': 'str',
        'row': 'int',
        'title': 'str',
        'ui_config': 'object'
    }

    attribute_map = {
        'dashboard_id': 'dashboard_id',
        'default_value': 'default_value',
        'explore': 'explore',
        'id': 'id',
        'model': 'model',
        'name': 'name',
        'row': 'row',
        'title': 'title',
        'ui_config': 'ui_config'
    }

    def __init__(self, dashboard_id=None, default_value=None, explore=None, id=None, model=None, name=None, row=None, title=None, ui_config=None):  # noqa: E501
        """DashboardFilter - a model defined in Swagger"""  # noqa: E501
        self._dashboard_id = None
        self._default_value = None
        self._explore = None
        self._id = None
        self._model = None
        self._name = None
        self._row = None
        self._title = None
        self._ui_config = None
        self.discriminator = None
        self.dashboard_id = dashboard_id
        self.default_value = default_value
        self.explore = explore
        self.id = id
        self.model = model
        if name is not None:
            self.name = name
        if row is not None:
            self.row = row
        if title is not None:
            self.title = title
        self.ui_config = ui_config

    @property
    def dashboard_id(self):
        """Gets the dashboard_id of this DashboardFilter.  # noqa: E501


        :return: The dashboard_id of this DashboardFilter.  # noqa: E501
        :rtype: str
        """
        return self._dashboard_id

    @dashboard_id.setter
    def dashboard_id(self, dashboard_id):
        """Sets the dashboard_id of this DashboardFilter.


        :param dashboard_id: The dashboard_id of this DashboardFilter.  # noqa: E501
        :type: str
        """
        if dashboard_id is None:
            raise ValueError("Invalid value for `dashboard_id`, must not be `None`")  # noqa: E501

        self._dashboard_id = dashboard_id

    @property
    def default_value(self):
        """Gets the default_value of this DashboardFilter.  # noqa: E501


        :return: The default_value of this DashboardFilter.  # noqa: E501
        :rtype: str
        """
        return self._default_value

    @default_value.setter
    def default_value(self, default_value):
        """Sets the default_value of this DashboardFilter.


        :param default_value: The default_value of this DashboardFilter.  # noqa: E501
        :type: str
        """
        if default_value is None:
            raise ValueError("Invalid value for `default_value`, must not be `None`")  # noqa: E501

        self._default_value = default_value

    @property
    def explore(self):
        """Gets the explore of this DashboardFilter.  # noqa: E501


        :return: The explore of this DashboardFilter.  # noqa: E501
        :rtype: str
        """
        return self._explore

    @explore.setter
    def explore(self, explore):
        """Sets the explore of this DashboardFilter.


        :param explore: The explore of this DashboardFilter.  # noqa: E501
        :type: str
        """
        if explore is None:
            raise ValueError("Invalid value for `explore`, must not be `None`")  # noqa: E501

        self._explore = explore

    @property
    def id(self):
        """Gets the id of this DashboardFilter.  # noqa: E501


        :return: The id of this DashboardFilter.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DashboardFilter.


        :param id: The id of this DashboardFilter.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def model(self):
        """Gets the model of this DashboardFilter.  # noqa: E501


        :return: The model of this DashboardFilter.  # noqa: E501
        :rtype: str
        """
        return self._model

    @model.setter
    def model(self, model):
        """Sets the model of this DashboardFilter.


        :param model: The model of this DashboardFilter.  # noqa: E501
        :type: str
        """
        if model is None:
            raise ValueError("Invalid value for `model`, must not be `None`")  # noqa: E501

        self._model = model

    @property
    def name(self):
        """Gets the name of this DashboardFilter.  # noqa: E501


        :return: The name of this DashboardFilter.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DashboardFilter.


        :param name: The name of this DashboardFilter.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def row(self):
        """Gets the row of this DashboardFilter.  # noqa: E501


        :return: The row of this DashboardFilter.  # noqa: E501
        :rtype: int
        """
        return self._row

    @row.setter
    def row(self, row):
        """Sets the row of this DashboardFilter.


        :param row: The row of this DashboardFilter.  # noqa: E501
        :type: int
        """

        self._row = row

    @property
    def title(self):
        """Gets the title of this DashboardFilter.  # noqa: E501


        :return: The title of this DashboardFilter.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this DashboardFilter.


        :param title: The title of this DashboardFilter.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def ui_config(self):
        """Gets the ui_config of this DashboardFilter.  # noqa: E501


        :return: The ui_config of this DashboardFilter.  # noqa: E501
        :rtype: object
        """
        return self._ui_config

    @ui_config.setter
    def ui_config(self, ui_config):
        """Sets the ui_config of this DashboardFilter.


        :param ui_config: The ui_config of this DashboardFilter.  # noqa: E501
        :type: object
        """
        if ui_config is None:
            raise ValueError("Invalid value for `ui_config`, must not be `None`")  # noqa: E501

        self._ui_config = ui_config

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
        if issubclass(DashboardFilter, dict):
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
        if not isinstance(other, DashboardFilter):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
