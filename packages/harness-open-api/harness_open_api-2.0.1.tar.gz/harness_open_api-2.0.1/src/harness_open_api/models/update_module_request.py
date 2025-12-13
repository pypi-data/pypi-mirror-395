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

class UpdateModuleRequest(object):
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
        'description': 'str',
        'git_tag_style': 'str',
        'name': 'str',
        'onboarding_pipeline': 'str',
        'onboarding_pipeline_org': 'str',
        'onboarding_pipeline_project': 'str',
        'org': 'str',
        'project': 'str',
        'repository': 'str',
        'repository_branch': 'str',
        'repository_commit': 'str',
        'repository_connector': 'str',
        'repository_path': 'str',
        'storage_type': 'str',
        'system': 'str',
        'tags': 'str'
    }

    attribute_map = {
        'description': 'description',
        'git_tag_style': 'git_tag_style',
        'name': 'name',
        'onboarding_pipeline': 'onboarding_pipeline',
        'onboarding_pipeline_org': 'onboarding_pipeline_org',
        'onboarding_pipeline_project': 'onboarding_pipeline_project',
        'org': 'org',
        'project': 'project',
        'repository': 'repository',
        'repository_branch': 'repository_branch',
        'repository_commit': 'repository_commit',
        'repository_connector': 'repository_connector',
        'repository_path': 'repository_path',
        'storage_type': 'storage_type',
        'system': 'system',
        'tags': 'tags'
    }

    def __init__(self, description=None, git_tag_style=None, name=None, onboarding_pipeline=None, onboarding_pipeline_org=None, onboarding_pipeline_project=None, org=None, project=None, repository=None, repository_branch=None, repository_commit=None, repository_connector=None, repository_path='', storage_type='git_reference', system=None, tags=None):  # noqa: E501
        """UpdateModuleRequest - a model defined in Swagger"""  # noqa: E501
        self._description = None
        self._git_tag_style = None
        self._name = None
        self._onboarding_pipeline = None
        self._onboarding_pipeline_org = None
        self._onboarding_pipeline_project = None
        self._org = None
        self._project = None
        self._repository = None
        self._repository_branch = None
        self._repository_commit = None
        self._repository_connector = None
        self._repository_path = None
        self._storage_type = None
        self._system = None
        self._tags = None
        self.discriminator = None
        if description is not None:
            self.description = description
        if git_tag_style is not None:
            self.git_tag_style = git_tag_style
        self.name = name
        if onboarding_pipeline is not None:
            self.onboarding_pipeline = onboarding_pipeline
        if onboarding_pipeline_org is not None:
            self.onboarding_pipeline_org = onboarding_pipeline_org
        if onboarding_pipeline_project is not None:
            self.onboarding_pipeline_project = onboarding_pipeline_project
        if org is not None:
            self.org = org
        if project is not None:
            self.project = project
        if repository is not None:
            self.repository = repository
        if repository_branch is not None:
            self.repository_branch = repository_branch
        if repository_commit is not None:
            self.repository_commit = repository_commit
        if repository_connector is not None:
            self.repository_connector = repository_connector
        if repository_path is not None:
            self.repository_path = repository_path
        if storage_type is not None:
            self.storage_type = storage_type
        self.system = system
        if tags is not None:
            self.tags = tags

    @property
    def description(self):
        """Gets the description of this UpdateModuleRequest.  # noqa: E501

        description of the module  # noqa: E501

        :return: The description of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpdateModuleRequest.

        description of the module  # noqa: E501

        :param description: The description of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def git_tag_style(self):
        """Gets the git_tag_style of this UpdateModuleRequest.  # noqa: E501

        Git Tag Style  # noqa: E501

        :return: The git_tag_style of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._git_tag_style

    @git_tag_style.setter
    def git_tag_style(self, git_tag_style):
        """Sets the git_tag_style of this UpdateModuleRequest.

        Git Tag Style  # noqa: E501

        :param git_tag_style: The git_tag_style of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """

        self._git_tag_style = git_tag_style

    @property
    def name(self):
        """Gets the name of this UpdateModuleRequest.  # noqa: E501

        module name  # noqa: E501

        :return: The name of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateModuleRequest.

        module name  # noqa: E501

        :param name: The name of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def onboarding_pipeline(self):
        """Gets the onboarding_pipeline of this UpdateModuleRequest.  # noqa: E501

        Onboarding Pipeline  # noqa: E501

        :return: The onboarding_pipeline of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._onboarding_pipeline

    @onboarding_pipeline.setter
    def onboarding_pipeline(self, onboarding_pipeline):
        """Sets the onboarding_pipeline of this UpdateModuleRequest.

        Onboarding Pipeline  # noqa: E501

        :param onboarding_pipeline: The onboarding_pipeline of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """

        self._onboarding_pipeline = onboarding_pipeline

    @property
    def onboarding_pipeline_org(self):
        """Gets the onboarding_pipeline_org of this UpdateModuleRequest.  # noqa: E501

        Onboarding Pipeline Org  # noqa: E501

        :return: The onboarding_pipeline_org of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._onboarding_pipeline_org

    @onboarding_pipeline_org.setter
    def onboarding_pipeline_org(self, onboarding_pipeline_org):
        """Sets the onboarding_pipeline_org of this UpdateModuleRequest.

        Onboarding Pipeline Org  # noqa: E501

        :param onboarding_pipeline_org: The onboarding_pipeline_org of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """

        self._onboarding_pipeline_org = onboarding_pipeline_org

    @property
    def onboarding_pipeline_project(self):
        """Gets the onboarding_pipeline_project of this UpdateModuleRequest.  # noqa: E501

        Onboarding Pipeline Project  # noqa: E501

        :return: The onboarding_pipeline_project of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._onboarding_pipeline_project

    @onboarding_pipeline_project.setter
    def onboarding_pipeline_project(self, onboarding_pipeline_project):
        """Sets the onboarding_pipeline_project of this UpdateModuleRequest.

        Onboarding Pipeline Project  # noqa: E501

        :param onboarding_pipeline_project: The onboarding_pipeline_project of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """

        self._onboarding_pipeline_project = onboarding_pipeline_project

    @property
    def org(self):
        """Gets the org of this UpdateModuleRequest.  # noqa: E501

        org that owns the module  # noqa: E501

        :return: The org of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._org

    @org.setter
    def org(self, org):
        """Sets the org of this UpdateModuleRequest.

        org that owns the module  # noqa: E501

        :param org: The org of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """

        self._org = org

    @property
    def project(self):
        """Gets the project of this UpdateModuleRequest.  # noqa: E501

        project that owns the module  # noqa: E501

        :return: The project of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this UpdateModuleRequest.

        project that owns the module  # noqa: E501

        :param project: The project of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """

        self._project = project

    @property
    def repository(self):
        """Gets the repository of this UpdateModuleRequest.  # noqa: E501

        Repository is the name of the repository to use.  # noqa: E501

        :return: The repository of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._repository

    @repository.setter
    def repository(self, repository):
        """Sets the repository of this UpdateModuleRequest.

        Repository is the name of the repository to use.  # noqa: E501

        :param repository: The repository of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """

        self._repository = repository

    @property
    def repository_branch(self):
        """Gets the repository_branch of this UpdateModuleRequest.  # noqa: E501

        Repository Branch in which the code should be accessed.  # noqa: E501

        :return: The repository_branch of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._repository_branch

    @repository_branch.setter
    def repository_branch(self, repository_branch):
        """Sets the repository_branch of this UpdateModuleRequest.

        Repository Branch in which the code should be accessed.  # noqa: E501

        :param repository_branch: The repository_branch of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """

        self._repository_branch = repository_branch

    @property
    def repository_commit(self):
        """Gets the repository_commit of this UpdateModuleRequest.  # noqa: E501

        Repository Commit/Tag in which the code should be accessed.  # noqa: E501

        :return: The repository_commit of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._repository_commit

    @repository_commit.setter
    def repository_commit(self, repository_commit):
        """Sets the repository_commit of this UpdateModuleRequest.

        Repository Commit/Tag in which the code should be accessed.  # noqa: E501

        :param repository_commit: The repository_commit of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """

        self._repository_commit = repository_commit

    @property
    def repository_connector(self):
        """Gets the repository_connector of this UpdateModuleRequest.  # noqa: E501

        Repository Connector is the reference to the connector to use for this code.  # noqa: E501

        :return: The repository_connector of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._repository_connector

    @repository_connector.setter
    def repository_connector(self, repository_connector):
        """Sets the repository_connector of this UpdateModuleRequest.

        Repository Connector is the reference to the connector to use for this code.  # noqa: E501

        :param repository_connector: The repository_connector of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """

        self._repository_connector = repository_connector

    @property
    def repository_path(self):
        """Gets the repository_path of this UpdateModuleRequest.  # noqa: E501

        Repository Path is the path in which the infra code resides.  # noqa: E501

        :return: The repository_path of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._repository_path

    @repository_path.setter
    def repository_path(self, repository_path):
        """Sets the repository_path of this UpdateModuleRequest.

        Repository Path is the path in which the infra code resides.  # noqa: E501

        :param repository_path: The repository_path of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """

        self._repository_path = repository_path

    @property
    def storage_type(self):
        """Gets the storage_type of this UpdateModuleRequest.  # noqa: E501

        How to storage the artifact  # noqa: E501

        :return: The storage_type of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._storage_type

    @storage_type.setter
    def storage_type(self, storage_type):
        """Sets the storage_type of this UpdateModuleRequest.

        How to storage the artifact  # noqa: E501

        :param storage_type: The storage_type of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["git_reference", "artifact"]  # noqa: E501
        if storage_type not in allowed_values:
            raise ValueError(
                "Invalid value for `storage_type` ({0}), must be one of {1}"  # noqa: E501
                .format(storage_type, allowed_values)
            )

        self._storage_type = storage_type

    @property
    def system(self):
        """Gets the system of this UpdateModuleRequest.  # noqa: E501

        system name  # noqa: E501

        :return: The system of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._system

    @system.setter
    def system(self, system):
        """Sets the system of this UpdateModuleRequest.

        system name  # noqa: E501

        :param system: The system of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """
        if system is None:
            raise ValueError("Invalid value for `system`, must not be `None`")  # noqa: E501

        self._system = system

    @property
    def tags(self):
        """Gets the tags of this UpdateModuleRequest.  # noqa: E501

        tags defining the module  # noqa: E501

        :return: The tags of this UpdateModuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this UpdateModuleRequest.

        tags defining the module  # noqa: E501

        :param tags: The tags of this UpdateModuleRequest.  # noqa: E501
        :type: str
        """

        self._tags = tags

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
        if issubclass(UpdateModuleRequest, dict):
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
        if not isinstance(other, UpdateModuleRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
