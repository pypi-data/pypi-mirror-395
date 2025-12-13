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

class Dashboard(object):
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
        'created_at': 'str',
        'data_source': 'list[str]',
        'description': 'str',
        'favorite_count': 'int',
        'folder': 'DashboardFolder',
        'id': 'str',
        'last_accessed_at': 'str',
        'models': 'list[str]',
        'resource_identifier': 'str',
        'title': 'str',
        'type': 'str',
        'view_count': 'int'
    }

    attribute_map = {
        'created_at': 'created_at',
        'data_source': 'data_source',
        'description': 'description',
        'favorite_count': 'favorite_count',
        'folder': 'folder',
        'id': 'id',
        'last_accessed_at': 'last_accessed_at',
        'models': 'models',
        'resource_identifier': 'resourceIdentifier',
        'title': 'title',
        'type': 'type',
        'view_count': 'view_count'
    }

    def __init__(self, created_at=None, data_source=None, description=None, favorite_count=None, folder=None, id=None, last_accessed_at=None, models=None, resource_identifier=None, title=None, type=None, view_count=None):  # noqa: E501
        """Dashboard - a model defined in Swagger"""  # noqa: E501
        self._created_at = None
        self._data_source = None
        self._description = None
        self._favorite_count = None
        self._folder = None
        self._id = None
        self._last_accessed_at = None
        self._models = None
        self._resource_identifier = None
        self._title = None
        self._type = None
        self._view_count = None
        self.discriminator = None
        self.created_at = created_at
        self.data_source = data_source
        self.description = description
        self.favorite_count = favorite_count
        self.folder = folder
        self.id = id
        self.last_accessed_at = last_accessed_at
        self.models = models
        self.resource_identifier = resource_identifier
        self.title = title
        self.type = type
        self.view_count = view_count

    @property
    def created_at(self):
        """Gets the created_at of this Dashboard.  # noqa: E501


        :return: The created_at of this Dashboard.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Dashboard.


        :param created_at: The created_at of this Dashboard.  # noqa: E501
        :type: str
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def data_source(self):
        """Gets the data_source of this Dashboard.  # noqa: E501


        :return: The data_source of this Dashboard.  # noqa: E501
        :rtype: list[str]
        """
        return self._data_source

    @data_source.setter
    def data_source(self, data_source):
        """Sets the data_source of this Dashboard.


        :param data_source: The data_source of this Dashboard.  # noqa: E501
        :type: list[str]
        """
        if data_source is None:
            raise ValueError("Invalid value for `data_source`, must not be `None`")  # noqa: E501
        allowed_values = ["CD", "CE", "CET", "CF", "CHAOS", "CI", "DBOPS", "HARNESS", "IACM", "IDP", "SRM", "SSCA", "STO", "UNIVERSAL"]  # noqa: E501
        if not set(data_source).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `data_source` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(data_source) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._data_source = data_source

    @property
    def description(self):
        """Gets the description of this Dashboard.  # noqa: E501


        :return: The description of this Dashboard.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Dashboard.


        :param description: The description of this Dashboard.  # noqa: E501
        :type: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description

    @property
    def favorite_count(self):
        """Gets the favorite_count of this Dashboard.  # noqa: E501


        :return: The favorite_count of this Dashboard.  # noqa: E501
        :rtype: int
        """
        return self._favorite_count

    @favorite_count.setter
    def favorite_count(self, favorite_count):
        """Sets the favorite_count of this Dashboard.


        :param favorite_count: The favorite_count of this Dashboard.  # noqa: E501
        :type: int
        """
        if favorite_count is None:
            raise ValueError("Invalid value for `favorite_count`, must not be `None`")  # noqa: E501

        self._favorite_count = favorite_count

    @property
    def folder(self):
        """Gets the folder of this Dashboard.  # noqa: E501


        :return: The folder of this Dashboard.  # noqa: E501
        :rtype: DashboardFolder
        """
        return self._folder

    @folder.setter
    def folder(self, folder):
        """Sets the folder of this Dashboard.


        :param folder: The folder of this Dashboard.  # noqa: E501
        :type: DashboardFolder
        """
        if folder is None:
            raise ValueError("Invalid value for `folder`, must not be `None`")  # noqa: E501

        self._folder = folder

    @property
    def id(self):
        """Gets the id of this Dashboard.  # noqa: E501


        :return: The id of this Dashboard.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Dashboard.


        :param id: The id of this Dashboard.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def last_accessed_at(self):
        """Gets the last_accessed_at of this Dashboard.  # noqa: E501


        :return: The last_accessed_at of this Dashboard.  # noqa: E501
        :rtype: str
        """
        return self._last_accessed_at

    @last_accessed_at.setter
    def last_accessed_at(self, last_accessed_at):
        """Sets the last_accessed_at of this Dashboard.


        :param last_accessed_at: The last_accessed_at of this Dashboard.  # noqa: E501
        :type: str
        """
        if last_accessed_at is None:
            raise ValueError("Invalid value for `last_accessed_at`, must not be `None`")  # noqa: E501

        self._last_accessed_at = last_accessed_at

    @property
    def models(self):
        """Gets the models of this Dashboard.  # noqa: E501


        :return: The models of this Dashboard.  # noqa: E501
        :rtype: list[str]
        """
        return self._models

    @models.setter
    def models(self, models):
        """Sets the models of this Dashboard.


        :param models: The models of this Dashboard.  # noqa: E501
        :type: list[str]
        """
        if models is None:
            raise ValueError("Invalid value for `models`, must not be `None`")  # noqa: E501
        allowed_values = ["CD", "CE", "CET", "CF", "CG_CD", "CHAOS", "CI", "CI_TI", "DBOPS", "IACM", "IDP", "SRM", "SSCA", "STO", "UNIVERSAL"]  # noqa: E501
        if not set(models).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `models` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(models) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._models = models

    @property
    def resource_identifier(self):
        """Gets the resource_identifier of this Dashboard.  # noqa: E501


        :return: The resource_identifier of this Dashboard.  # noqa: E501
        :rtype: str
        """
        return self._resource_identifier

    @resource_identifier.setter
    def resource_identifier(self, resource_identifier):
        """Sets the resource_identifier of this Dashboard.


        :param resource_identifier: The resource_identifier of this Dashboard.  # noqa: E501
        :type: str
        """
        if resource_identifier is None:
            raise ValueError("Invalid value for `resource_identifier`, must not be `None`")  # noqa: E501

        self._resource_identifier = resource_identifier

    @property
    def title(self):
        """Gets the title of this Dashboard.  # noqa: E501


        :return: The title of this Dashboard.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Dashboard.


        :param title: The title of this Dashboard.  # noqa: E501
        :type: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501

        self._title = title

    @property
    def type(self):
        """Gets the type of this Dashboard.  # noqa: E501


        :return: The type of this Dashboard.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Dashboard.


        :param type: The type of this Dashboard.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["ACCOUNT", "SHARED"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def view_count(self):
        """Gets the view_count of this Dashboard.  # noqa: E501


        :return: The view_count of this Dashboard.  # noqa: E501
        :rtype: int
        """
        return self._view_count

    @view_count.setter
    def view_count(self, view_count):
        """Sets the view_count of this Dashboard.


        :param view_count: The view_count of this Dashboard.  # noqa: E501
        :type: int
        """
        if view_count is None:
            raise ValueError("Invalid value for `view_count`, must not be `None`")  # noqa: E501

        self._view_count = view_count

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
        if issubclass(Dashboard, dict):
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
        if not isinstance(other, Dashboard):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
