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

class EntityResponse(object):
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
        'cache_response_data': 'CacheResponseData',
        'description': 'str',
        'entity_ref': 'str',
        'entity_validity_details': 'EntityResponseEntityValidityDetails',
        'git_details': 'GitDetails1',
        'groups': 'list[EntityResponseGroups]',
        'identifier': 'str',
        'kind': 'str',
        'lifecycle': 'str',
        'metadata': 'object',
        'name': 'str',
        'org_identifier': 'str',
        'org_name': 'str',
        'owner': 'str',
        'project_identifier': 'str',
        'project_name': 'str',
        'reference_type': 'str',
        'scope': 'str',
        'scorecards': 'EntityResponseScorecards',
        'starred': 'bool',
        'status': 'list[EntityResponseStatus]',
        'tags': 'list[str]',
        'type': 'str',
        'yaml': 'str'
    }

    attribute_map = {
        'cache_response_data': 'cache_response_data',
        'description': 'description',
        'entity_ref': 'entity_ref',
        'entity_validity_details': 'entity_validity_details',
        'git_details': 'git_details',
        'groups': 'groups',
        'identifier': 'identifier',
        'kind': 'kind',
        'lifecycle': 'lifecycle',
        'metadata': 'metadata',
        'name': 'name',
        'org_identifier': 'orgIdentifier',
        'org_name': 'org_name',
        'owner': 'owner',
        'project_identifier': 'projectIdentifier',
        'project_name': 'project_name',
        'reference_type': 'referenceType',
        'scope': 'scope',
        'scorecards': 'scorecards',
        'starred': 'starred',
        'status': 'status',
        'tags': 'tags',
        'type': 'type',
        'yaml': 'yaml'
    }

    def __init__(self, cache_response_data=None, description=None, entity_ref=None, entity_validity_details=None, git_details=None, groups=None, identifier=None, kind=None, lifecycle=None, metadata=None, name=None, org_identifier=None, org_name=None, owner=None, project_identifier=None, project_name=None, reference_type=None, scope=None, scorecards=None, starred=None, status=None, tags=None, type=None, yaml=None):  # noqa: E501
        """EntityResponse - a model defined in Swagger"""  # noqa: E501
        self._cache_response_data = None
        self._description = None
        self._entity_ref = None
        self._entity_validity_details = None
        self._git_details = None
        self._groups = None
        self._identifier = None
        self._kind = None
        self._lifecycle = None
        self._metadata = None
        self._name = None
        self._org_identifier = None
        self._org_name = None
        self._owner = None
        self._project_identifier = None
        self._project_name = None
        self._reference_type = None
        self._scope = None
        self._scorecards = None
        self._starred = None
        self._status = None
        self._tags = None
        self._type = None
        self._yaml = None
        self.discriminator = None
        if cache_response_data is not None:
            self.cache_response_data = cache_response_data
        if description is not None:
            self.description = description
        self.entity_ref = entity_ref
        if entity_validity_details is not None:
            self.entity_validity_details = entity_validity_details
        if git_details is not None:
            self.git_details = git_details
        if groups is not None:
            self.groups = groups
        self.identifier = identifier
        self.kind = kind
        if lifecycle is not None:
            self.lifecycle = lifecycle
        if metadata is not None:
            self.metadata = metadata
        if name is not None:
            self.name = name
        if org_identifier is not None:
            self.org_identifier = org_identifier
        if org_name is not None:
            self.org_name = org_name
        if owner is not None:
            self.owner = owner
        if project_identifier is not None:
            self.project_identifier = project_identifier
        if project_name is not None:
            self.project_name = project_name
        self.reference_type = reference_type
        self.scope = scope
        if scorecards is not None:
            self.scorecards = scorecards
        if starred is not None:
            self.starred = starred
        if status is not None:
            self.status = status
        if tags is not None:
            self.tags = tags
        if type is not None:
            self.type = type
        self.yaml = yaml

    @property
    def cache_response_data(self):
        """Gets the cache_response_data of this EntityResponse.  # noqa: E501


        :return: The cache_response_data of this EntityResponse.  # noqa: E501
        :rtype: CacheResponseData
        """
        return self._cache_response_data

    @cache_response_data.setter
    def cache_response_data(self, cache_response_data):
        """Sets the cache_response_data of this EntityResponse.


        :param cache_response_data: The cache_response_data of this EntityResponse.  # noqa: E501
        :type: CacheResponseData
        """

        self._cache_response_data = cache_response_data

    @property
    def description(self):
        """Gets the description of this EntityResponse.  # noqa: E501

        Descriptive text about the entity  # noqa: E501

        :return: The description of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this EntityResponse.

        Descriptive text about the entity  # noqa: E501

        :param description: The description of this EntityResponse.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def entity_ref(self):
        """Gets the entity_ref of this EntityResponse.  # noqa: E501

        Full entity reference in the format scope/kind/identifier  # noqa: E501

        :return: The entity_ref of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._entity_ref

    @entity_ref.setter
    def entity_ref(self, entity_ref):
        """Sets the entity_ref of this EntityResponse.

        Full entity reference in the format scope/kind/identifier  # noqa: E501

        :param entity_ref: The entity_ref of this EntityResponse.  # noqa: E501
        :type: str
        """
        if entity_ref is None:
            raise ValueError("Invalid value for `entity_ref`, must not be `None`")  # noqa: E501

        self._entity_ref = entity_ref

    @property
    def entity_validity_details(self):
        """Gets the entity_validity_details of this EntityResponse.  # noqa: E501


        :return: The entity_validity_details of this EntityResponse.  # noqa: E501
        :rtype: EntityResponseEntityValidityDetails
        """
        return self._entity_validity_details

    @entity_validity_details.setter
    def entity_validity_details(self, entity_validity_details):
        """Sets the entity_validity_details of this EntityResponse.


        :param entity_validity_details: The entity_validity_details of this EntityResponse.  # noqa: E501
        :type: EntityResponseEntityValidityDetails
        """

        self._entity_validity_details = entity_validity_details

    @property
    def git_details(self):
        """Gets the git_details of this EntityResponse.  # noqa: E501


        :return: The git_details of this EntityResponse.  # noqa: E501
        :rtype: GitDetails1
        """
        return self._git_details

    @git_details.setter
    def git_details(self, git_details):
        """Sets the git_details of this EntityResponse.


        :param git_details: The git_details of this EntityResponse.  # noqa: E501
        :type: GitDetails1
        """

        self._git_details = git_details

    @property
    def groups(self):
        """Gets the groups of this EntityResponse.  # noqa: E501

        Groups that the entity belongs to  # noqa: E501

        :return: The groups of this EntityResponse.  # noqa: E501
        :rtype: list[EntityResponseGroups]
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """Sets the groups of this EntityResponse.

        Groups that the entity belongs to  # noqa: E501

        :param groups: The groups of this EntityResponse.  # noqa: E501
        :type: list[EntityResponseGroups]
        """

        self._groups = groups

    @property
    def identifier(self):
        """Gets the identifier of this EntityResponse.  # noqa: E501

        Unique identifier of the entity within its scope and kind  # noqa: E501

        :return: The identifier of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this EntityResponse.

        Unique identifier of the entity within its scope and kind  # noqa: E501

        :param identifier: The identifier of this EntityResponse.  # noqa: E501
        :type: str
        """
        if identifier is None:
            raise ValueError("Invalid value for `identifier`, must not be `None`")  # noqa: E501

        self._identifier = identifier

    @property
    def kind(self):
        """Gets the kind of this EntityResponse.  # noqa: E501

        Kind of the entity (defines its core purpose)  # noqa: E501

        :return: The kind of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this EntityResponse.

        Kind of the entity (defines its core purpose)  # noqa: E501

        :param kind: The kind of this EntityResponse.  # noqa: E501
        :type: str
        """
        if kind is None:
            raise ValueError("Invalid value for `kind`, must not be `None`")  # noqa: E501
        # 2025-09-10
        # WARNING
        # At the time of this comment, the 'system' option is not being automatically added
        # and is not listed as allowed value in the API
        allowed_values = ["api", "component", "group", "resource", "user", "workflow", "system"]  # noqa: E501
        if kind not in allowed_values:
            raise ValueError(
                "Invalid value for `kind` ({0}), must be one of {1}"  # noqa: E501
                .format(kind, allowed_values)
            )

        self._kind = kind

    @property
    def lifecycle(self):
        """Gets the lifecycle of this EntityResponse.  # noqa: E501

        Lifecycle stage of the entity (e.g., experimental, production)  # noqa: E501

        :return: The lifecycle of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._lifecycle

    @lifecycle.setter
    def lifecycle(self, lifecycle):
        """Sets the lifecycle of this EntityResponse.

        Lifecycle stage of the entity (e.g., experimental, production)  # noqa: E501

        :param lifecycle: The lifecycle of this EntityResponse.  # noqa: E501
        :type: str
        """

        self._lifecycle = lifecycle

    @property
    def metadata(self):
        """Gets the metadata of this EntityResponse.  # noqa: E501

        Additional metadata associated with the entity  # noqa: E501

        :return: The metadata of this EntityResponse.  # noqa: E501
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this EntityResponse.

        Additional metadata associated with the entity  # noqa: E501

        :param metadata: The metadata of this EntityResponse.  # noqa: E501
        :type: object
        """

        self._metadata = metadata

    @property
    def name(self):
        """Gets the name of this EntityResponse.  # noqa: E501

        Display name of the entity  # noqa: E501

        :return: The name of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this EntityResponse.

        Display name of the entity  # noqa: E501

        :param name: The name of this EntityResponse.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def org_identifier(self):
        """Gets the org_identifier of this EntityResponse.  # noqa: E501

        Identifier of the organization that the entity belongs to  # noqa: E501

        :return: The org_identifier of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._org_identifier

    @org_identifier.setter
    def org_identifier(self, org_identifier):
        """Sets the org_identifier of this EntityResponse.

        Identifier of the organization that the entity belongs to  # noqa: E501

        :param org_identifier: The org_identifier of this EntityResponse.  # noqa: E501
        :type: str
        """

        self._org_identifier = org_identifier

    @property
    def org_name(self):
        """Gets the org_name of this EntityResponse.  # noqa: E501

        Display name of the organization that the entity belongs to  # noqa: E501

        :return: The org_name of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._org_name

    @org_name.setter
    def org_name(self, org_name):
        """Sets the org_name of this EntityResponse.

        Display name of the organization that the entity belongs to  # noqa: E501

        :param org_name: The org_name of this EntityResponse.  # noqa: E501
        :type: str
        """

        self._org_name = org_name

    @property
    def owner(self):
        """Gets the owner of this EntityResponse.  # noqa: E501

        Owner reference for the entity (user or group)  # noqa: E501

        :return: The owner of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this EntityResponse.

        Owner reference for the entity (user or group)  # noqa: E501

        :param owner: The owner of this EntityResponse.  # noqa: E501
        :type: str
        """

        self._owner = owner

    @property
    def project_identifier(self):
        """Gets the project_identifier of this EntityResponse.  # noqa: E501

        Identifier of the project that the entity belongs to  # noqa: E501

        :return: The project_identifier of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._project_identifier

    @project_identifier.setter
    def project_identifier(self, project_identifier):
        """Sets the project_identifier of this EntityResponse.

        Identifier of the project that the entity belongs to  # noqa: E501

        :param project_identifier: The project_identifier of this EntityResponse.  # noqa: E501
        :type: str
        """

        self._project_identifier = project_identifier

    @property
    def project_name(self):
        """Gets the project_name of this EntityResponse.  # noqa: E501

        Display name of the project that the entity belongs to  # noqa: E501

        :return: The project_name of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this EntityResponse.

        Display name of the project that the entity belongs to  # noqa: E501

        :param project_name: The project_name of this EntityResponse.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

    @property
    def reference_type(self):
        """Gets the reference_type of this EntityResponse.  # noqa: E501

        Type of reference for the entity (inline definition or Git-sourced)  # noqa: E501

        :return: The reference_type of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._reference_type

    @reference_type.setter
    def reference_type(self, reference_type):
        """Sets the reference_type of this EntityResponse.

        Type of reference for the entity (inline definition or Git-sourced)  # noqa: E501

        :param reference_type: The reference_type of this EntityResponse.  # noqa: E501
        :type: str
        """
        if reference_type is None:
            raise ValueError("Invalid value for `reference_type`, must not be `None`")  # noqa: E501
        allowed_values = ["INLINE", "GIT"]  # noqa: E501
        if reference_type not in allowed_values:
            raise ValueError(
                "Invalid value for `reference_type` ({0}), must be one of {1}"  # noqa: E501
                .format(reference_type, allowed_values)
            )

        self._reference_type = reference_type

    @property
    def scope(self):
        """Gets the scope of this EntityResponse.  # noqa: E501

        Scope of the entity (account, organization, or project level)  # noqa: E501

        :return: The scope of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this EntityResponse.

        Scope of the entity (account, organization, or project level)  # noqa: E501

        :param scope: The scope of this EntityResponse.  # noqa: E501
        :type: str
        """
        if scope is None:
            raise ValueError("Invalid value for `scope`, must not be `None`")  # noqa: E501
        allowed_values = ["ACCOUNT", "ORGANIZATION", "PROJECT"]  # noqa: E501
        if scope not in allowed_values:
            raise ValueError(
                "Invalid value for `scope` ({0}), must be one of {1}"  # noqa: E501
                .format(scope, allowed_values)
            )

        self._scope = scope

    @property
    def scorecards(self):
        """Gets the scorecards of this EntityResponse.  # noqa: E501


        :return: The scorecards of this EntityResponse.  # noqa: E501
        :rtype: EntityResponseScorecards
        """
        return self._scorecards

    @scorecards.setter
    def scorecards(self, scorecards):
        """Sets the scorecards of this EntityResponse.


        :param scorecards: The scorecards of this EntityResponse.  # noqa: E501
        :type: EntityResponseScorecards
        """

        self._scorecards = scorecards

    @property
    def starred(self):
        """Gets the starred of this EntityResponse.  # noqa: E501

        Whether the entity is marked as a favorite by the current user  # noqa: E501

        :return: The starred of this EntityResponse.  # noqa: E501
        :rtype: bool
        """
        return self._starred

    @starred.setter
    def starred(self, starred):
        """Sets the starred of this EntityResponse.

        Whether the entity is marked as a favorite by the current user  # noqa: E501

        :param starred: The starred of this EntityResponse.  # noqa: E501
        :type: bool
        """

        self._starred = starred

    @property
    def status(self):
        """Gets the status of this EntityResponse.  # noqa: E501

        Status information for the entity  # noqa: E501

        :return: The status of this EntityResponse.  # noqa: E501
        :rtype: list[EntityResponseStatus]
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this EntityResponse.

        Status information for the entity  # noqa: E501

        :param status: The status of this EntityResponse.  # noqa: E501
        :type: list[EntityResponseStatus]
        """

        self._status = status

    @property
    def tags(self):
        """Gets the tags of this EntityResponse.  # noqa: E501

        Tags associated with the entity for categorization  # noqa: E501

        :return: The tags of this EntityResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this EntityResponse.

        Tags associated with the entity for categorization  # noqa: E501

        :param tags: The tags of this EntityResponse.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def type(self):
        """Gets the type of this EntityResponse.  # noqa: E501

        Type of the entity within its kind (e.g., Service, Website)  # noqa: E501

        :return: The type of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this EntityResponse.

        Type of the entity within its kind (e.g., Service, Website)  # noqa: E501

        :param type: The type of this EntityResponse.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def yaml(self):
        """Gets the yaml of this EntityResponse.  # noqa: E501

        Complete entity YAML definition  # noqa: E501

        :return: The yaml of this EntityResponse.  # noqa: E501
        :rtype: str
        """
        return self._yaml

    @yaml.setter
    def yaml(self, yaml):
        """Sets the yaml of this EntityResponse.

        Complete entity YAML definition  # noqa: E501

        :param yaml: The yaml of this EntityResponse.  # noqa: E501
        :type: str
        """
        if yaml is None:
            raise ValueError("Invalid value for `yaml`, must not be `None`")  # noqa: E501

        self._yaml = yaml

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
        if issubclass(EntityResponse, dict):
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
        if not isinstance(other, EntityResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
