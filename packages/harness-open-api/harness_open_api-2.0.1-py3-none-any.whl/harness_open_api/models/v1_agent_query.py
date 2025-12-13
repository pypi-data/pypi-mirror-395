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

class V1AgentQuery(object):
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
        'account_identifier': 'str',
        'connected_status': 'V1ConnectedStatus',
        'dr_identifier': 'str',
        'filter': 'object',
        'health_status': 'Servicev1HealthStatus',
        'identifier': 'str',
        'ignore_scope': 'bool',
        'include_secondary': 'bool',
        'mapped_projects': 'Servicev1AppProjectMapping',
        'metadata_only': 'bool',
        'name': 'str',
        'org_identifier': 'str',
        'page_index': 'int',
        'page_size': 'int',
        'project_identifier': 'str',
        'scope': 'V1AgentScope',
        'search_term': 'str',
        'sort_by': 'AgentQueryAgentSortByOptions',
        'sort_order': 'V1SortOrderOptions',
        'tags': 'list[str]',
        'type': 'V1AgentType',
        'with_credentials': 'bool'
    }

    attribute_map = {
        'account_identifier': 'accountIdentifier',
        'connected_status': 'connectedStatus',
        'dr_identifier': 'drIdentifier',
        'filter': 'filter',
        'health_status': 'healthStatus',
        'identifier': 'identifier',
        'ignore_scope': 'ignoreScope',
        'include_secondary': 'includeSecondary',
        'mapped_projects': 'mappedProjects',
        'metadata_only': 'metadataOnly',
        'name': 'name',
        'org_identifier': 'orgIdentifier',
        'page_index': 'pageIndex',
        'page_size': 'pageSize',
        'project_identifier': 'projectIdentifier',
        'scope': 'scope',
        'search_term': 'searchTerm',
        'sort_by': 'sortBy',
        'sort_order': 'sortOrder',
        'tags': 'tags',
        'type': 'type',
        'with_credentials': 'withCredentials'
    }

    def __init__(self, account_identifier=None, connected_status=None, dr_identifier=None, filter=None, health_status=None, identifier=None, ignore_scope=None, include_secondary=None, mapped_projects=None, metadata_only=None, name=None, org_identifier=None, page_index=None, page_size=None, project_identifier=None, scope=None, search_term=None, sort_by=None, sort_order=None, tags=None, type=None, with_credentials=None):  # noqa: E501
        """V1AgentQuery - a model defined in Swagger"""  # noqa: E501
        self._account_identifier = None
        self._connected_status = None
        self._dr_identifier = None
        self._filter = None
        self._health_status = None
        self._identifier = None
        self._ignore_scope = None
        self._include_secondary = None
        self._mapped_projects = None
        self._metadata_only = None
        self._name = None
        self._org_identifier = None
        self._page_index = None
        self._page_size = None
        self._project_identifier = None
        self._scope = None
        self._search_term = None
        self._sort_by = None
        self._sort_order = None
        self._tags = None
        self._type = None
        self._with_credentials = None
        self.discriminator = None
        if account_identifier is not None:
            self.account_identifier = account_identifier
        if connected_status is not None:
            self.connected_status = connected_status
        if dr_identifier is not None:
            self.dr_identifier = dr_identifier
        if filter is not None:
            self.filter = filter
        if health_status is not None:
            self.health_status = health_status
        if identifier is not None:
            self.identifier = identifier
        if ignore_scope is not None:
            self.ignore_scope = ignore_scope
        if include_secondary is not None:
            self.include_secondary = include_secondary
        if mapped_projects is not None:
            self.mapped_projects = mapped_projects
        if metadata_only is not None:
            self.metadata_only = metadata_only
        if name is not None:
            self.name = name
        if org_identifier is not None:
            self.org_identifier = org_identifier
        if page_index is not None:
            self.page_index = page_index
        if page_size is not None:
            self.page_size = page_size
        if project_identifier is not None:
            self.project_identifier = project_identifier
        if scope is not None:
            self.scope = scope
        if search_term is not None:
            self.search_term = search_term
        if sort_by is not None:
            self.sort_by = sort_by
        if sort_order is not None:
            self.sort_order = sort_order
        if tags is not None:
            self.tags = tags
        if type is not None:
            self.type = type
        if with_credentials is not None:
            self.with_credentials = with_credentials

    @property
    def account_identifier(self):
        """Gets the account_identifier of this V1AgentQuery.  # noqa: E501

        Account Identifier for the Entity.  # noqa: E501

        :return: The account_identifier of this V1AgentQuery.  # noqa: E501
        :rtype: str
        """
        return self._account_identifier

    @account_identifier.setter
    def account_identifier(self, account_identifier):
        """Sets the account_identifier of this V1AgentQuery.

        Account Identifier for the Entity.  # noqa: E501

        :param account_identifier: The account_identifier of this V1AgentQuery.  # noqa: E501
        :type: str
        """

        self._account_identifier = account_identifier

    @property
    def connected_status(self):
        """Gets the connected_status of this V1AgentQuery.  # noqa: E501


        :return: The connected_status of this V1AgentQuery.  # noqa: E501
        :rtype: V1ConnectedStatus
        """
        return self._connected_status

    @connected_status.setter
    def connected_status(self, connected_status):
        """Sets the connected_status of this V1AgentQuery.


        :param connected_status: The connected_status of this V1AgentQuery.  # noqa: E501
        :type: V1ConnectedStatus
        """

        self._connected_status = connected_status

    @property
    def dr_identifier(self):
        """Gets the dr_identifier of this V1AgentQuery.  # noqa: E501


        :return: The dr_identifier of this V1AgentQuery.  # noqa: E501
        :rtype: str
        """
        return self._dr_identifier

    @dr_identifier.setter
    def dr_identifier(self, dr_identifier):
        """Sets the dr_identifier of this V1AgentQuery.


        :param dr_identifier: The dr_identifier of this V1AgentQuery.  # noqa: E501
        :type: str
        """

        self._dr_identifier = dr_identifier

    @property
    def filter(self):
        """Gets the filter of this V1AgentQuery.  # noqa: E501

        Filters for Agents.  # noqa: E501

        :return: The filter of this V1AgentQuery.  # noqa: E501
        :rtype: object
        """
        return self._filter

    @filter.setter
    def filter(self, filter):
        """Sets the filter of this V1AgentQuery.

        Filters for Agents.  # noqa: E501

        :param filter: The filter of this V1AgentQuery.  # noqa: E501
        :type: object
        """

        self._filter = filter

    @property
    def health_status(self):
        """Gets the health_status of this V1AgentQuery.  # noqa: E501


        :return: The health_status of this V1AgentQuery.  # noqa: E501
        :rtype: Servicev1HealthStatus
        """
        return self._health_status

    @health_status.setter
    def health_status(self, health_status):
        """Sets the health_status of this V1AgentQuery.


        :param health_status: The health_status of this V1AgentQuery.  # noqa: E501
        :type: Servicev1HealthStatus
        """

        self._health_status = health_status

    @property
    def identifier(self):
        """Gets the identifier of this V1AgentQuery.  # noqa: E501


        :return: The identifier of this V1AgentQuery.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this V1AgentQuery.


        :param identifier: The identifier of this V1AgentQuery.  # noqa: E501
        :type: str
        """

        self._identifier = identifier

    @property
    def ignore_scope(self):
        """Gets the ignore_scope of this V1AgentQuery.  # noqa: E501


        :return: The ignore_scope of this V1AgentQuery.  # noqa: E501
        :rtype: bool
        """
        return self._ignore_scope

    @ignore_scope.setter
    def ignore_scope(self, ignore_scope):
        """Sets the ignore_scope of this V1AgentQuery.


        :param ignore_scope: The ignore_scope of this V1AgentQuery.  # noqa: E501
        :type: bool
        """

        self._ignore_scope = ignore_scope

    @property
    def include_secondary(self):
        """Gets the include_secondary of this V1AgentQuery.  # noqa: E501


        :return: The include_secondary of this V1AgentQuery.  # noqa: E501
        :rtype: bool
        """
        return self._include_secondary

    @include_secondary.setter
    def include_secondary(self, include_secondary):
        """Sets the include_secondary of this V1AgentQuery.


        :param include_secondary: The include_secondary of this V1AgentQuery.  # noqa: E501
        :type: bool
        """

        self._include_secondary = include_secondary

    @property
    def mapped_projects(self):
        """Gets the mapped_projects of this V1AgentQuery.  # noqa: E501


        :return: The mapped_projects of this V1AgentQuery.  # noqa: E501
        :rtype: Servicev1AppProjectMapping
        """
        return self._mapped_projects

    @mapped_projects.setter
    def mapped_projects(self, mapped_projects):
        """Sets the mapped_projects of this V1AgentQuery.


        :param mapped_projects: The mapped_projects of this V1AgentQuery.  # noqa: E501
        :type: Servicev1AppProjectMapping
        """

        self._mapped_projects = mapped_projects

    @property
    def metadata_only(self):
        """Gets the metadata_only of this V1AgentQuery.  # noqa: E501


        :return: The metadata_only of this V1AgentQuery.  # noqa: E501
        :rtype: bool
        """
        return self._metadata_only

    @metadata_only.setter
    def metadata_only(self, metadata_only):
        """Sets the metadata_only of this V1AgentQuery.


        :param metadata_only: The metadata_only of this V1AgentQuery.  # noqa: E501
        :type: bool
        """

        self._metadata_only = metadata_only

    @property
    def name(self):
        """Gets the name of this V1AgentQuery.  # noqa: E501


        :return: The name of this V1AgentQuery.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V1AgentQuery.


        :param name: The name of this V1AgentQuery.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def org_identifier(self):
        """Gets the org_identifier of this V1AgentQuery.  # noqa: E501

        Organization Identifier for the Entity.  # noqa: E501

        :return: The org_identifier of this V1AgentQuery.  # noqa: E501
        :rtype: str
        """
        return self._org_identifier

    @org_identifier.setter
    def org_identifier(self, org_identifier):
        """Sets the org_identifier of this V1AgentQuery.

        Organization Identifier for the Entity.  # noqa: E501

        :param org_identifier: The org_identifier of this V1AgentQuery.  # noqa: E501
        :type: str
        """

        self._org_identifier = org_identifier

    @property
    def page_index(self):
        """Gets the page_index of this V1AgentQuery.  # noqa: E501


        :return: The page_index of this V1AgentQuery.  # noqa: E501
        :rtype: int
        """
        return self._page_index

    @page_index.setter
    def page_index(self, page_index):
        """Sets the page_index of this V1AgentQuery.


        :param page_index: The page_index of this V1AgentQuery.  # noqa: E501
        :type: int
        """

        self._page_index = page_index

    @property
    def page_size(self):
        """Gets the page_size of this V1AgentQuery.  # noqa: E501


        :return: The page_size of this V1AgentQuery.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this V1AgentQuery.


        :param page_size: The page_size of this V1AgentQuery.  # noqa: E501
        :type: int
        """

        self._page_size = page_size

    @property
    def project_identifier(self):
        """Gets the project_identifier of this V1AgentQuery.  # noqa: E501

        Project Identifier for the Entity.  # noqa: E501

        :return: The project_identifier of this V1AgentQuery.  # noqa: E501
        :rtype: str
        """
        return self._project_identifier

    @project_identifier.setter
    def project_identifier(self, project_identifier):
        """Sets the project_identifier of this V1AgentQuery.

        Project Identifier for the Entity.  # noqa: E501

        :param project_identifier: The project_identifier of this V1AgentQuery.  # noqa: E501
        :type: str
        """

        self._project_identifier = project_identifier

    @property
    def scope(self):
        """Gets the scope of this V1AgentQuery.  # noqa: E501


        :return: The scope of this V1AgentQuery.  # noqa: E501
        :rtype: V1AgentScope
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this V1AgentQuery.


        :param scope: The scope of this V1AgentQuery.  # noqa: E501
        :type: V1AgentScope
        """

        self._scope = scope

    @property
    def search_term(self):
        """Gets the search_term of this V1AgentQuery.  # noqa: E501


        :return: The search_term of this V1AgentQuery.  # noqa: E501
        :rtype: str
        """
        return self._search_term

    @search_term.setter
    def search_term(self, search_term):
        """Sets the search_term of this V1AgentQuery.


        :param search_term: The search_term of this V1AgentQuery.  # noqa: E501
        :type: str
        """

        self._search_term = search_term

    @property
    def sort_by(self):
        """Gets the sort_by of this V1AgentQuery.  # noqa: E501


        :return: The sort_by of this V1AgentQuery.  # noqa: E501
        :rtype: AgentQueryAgentSortByOptions
        """
        return self._sort_by

    @sort_by.setter
    def sort_by(self, sort_by):
        """Sets the sort_by of this V1AgentQuery.


        :param sort_by: The sort_by of this V1AgentQuery.  # noqa: E501
        :type: AgentQueryAgentSortByOptions
        """

        self._sort_by = sort_by

    @property
    def sort_order(self):
        """Gets the sort_order of this V1AgentQuery.  # noqa: E501


        :return: The sort_order of this V1AgentQuery.  # noqa: E501
        :rtype: V1SortOrderOptions
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """Sets the sort_order of this V1AgentQuery.


        :param sort_order: The sort_order of this V1AgentQuery.  # noqa: E501
        :type: V1SortOrderOptions
        """

        self._sort_order = sort_order

    @property
    def tags(self):
        """Gets the tags of this V1AgentQuery.  # noqa: E501


        :return: The tags of this V1AgentQuery.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this V1AgentQuery.


        :param tags: The tags of this V1AgentQuery.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def type(self):
        """Gets the type of this V1AgentQuery.  # noqa: E501


        :return: The type of this V1AgentQuery.  # noqa: E501
        :rtype: V1AgentType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this V1AgentQuery.


        :param type: The type of this V1AgentQuery.  # noqa: E501
        :type: V1AgentType
        """

        self._type = type

    @property
    def with_credentials(self):
        """Gets the with_credentials of this V1AgentQuery.  # noqa: E501

        Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.  # noqa: E501

        :return: The with_credentials of this V1AgentQuery.  # noqa: E501
        :rtype: bool
        """
        return self._with_credentials

    @with_credentials.setter
    def with_credentials(self, with_credentials):
        """Sets the with_credentials of this V1AgentQuery.

        Applicable when trying to retrieve an agent. Set to true to include the credentials for the agent in the response. (Private key may not be included in response if agent is already connected to harness). NOTE: Setting this to true requires the user to have edit permissions on Agent.  # noqa: E501

        :param with_credentials: The with_credentials of this V1AgentQuery.  # noqa: E501
        :type: bool
        """

        self._with_credentials = with_credentials

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
        if issubclass(V1AgentQuery, dict):
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
        if not isinstance(other, V1AgentQuery):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
