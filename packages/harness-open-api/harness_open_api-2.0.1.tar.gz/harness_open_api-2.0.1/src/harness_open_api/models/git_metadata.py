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

class GitMetadata(object):
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
        'detected_name': 'str',
        'detected_variant': 'str',
        'drone_correlated': 'bool',
        'provider': 'str',
        'pull_request_number': 'int',
        'repository_http': 'str',
        'repository_path': 'list[str]',
        'repository_ssh': 'str',
        'source_branch': 'str',
        'target_branch': 'str',
        'workspace': 'str'
    }

    attribute_map = {
        'detected_name': 'detectedName',
        'detected_variant': 'detectedVariant',
        'drone_correlated': 'droneCorrelated',
        'provider': 'provider',
        'pull_request_number': 'pullRequestNumber',
        'repository_http': 'repositoryHttp',
        'repository_path': 'repositoryPath',
        'repository_ssh': 'repositorySsh',
        'source_branch': 'sourceBranch',
        'target_branch': 'targetBranch',
        'workspace': 'workspace'
    }

    def __init__(self, detected_name=None, detected_variant=None, drone_correlated=None, provider=None, pull_request_number=None, repository_http=None, repository_path=None, repository_ssh=None, source_branch=None, target_branch=None, workspace=None):  # noqa: E501
        """GitMetadata - a model defined in Swagger"""  # noqa: E501
        self._detected_name = None
        self._detected_variant = None
        self._drone_correlated = None
        self._provider = None
        self._pull_request_number = None
        self._repository_http = None
        self._repository_path = None
        self._repository_ssh = None
        self._source_branch = None
        self._target_branch = None
        self._workspace = None
        self.discriminator = None
        if detected_name is not None:
            self.detected_name = detected_name
        if detected_variant is not None:
            self.detected_variant = detected_variant
        if drone_correlated is not None:
            self.drone_correlated = drone_correlated
        if provider is not None:
            self.provider = provider
        if pull_request_number is not None:
            self.pull_request_number = pull_request_number
        if repository_http is not None:
            self.repository_http = repository_http
        if repository_path is not None:
            self.repository_path = repository_path
        if repository_ssh is not None:
            self.repository_ssh = repository_ssh
        if source_branch is not None:
            self.source_branch = source_branch
        if target_branch is not None:
            self.target_branch = target_branch
        if workspace is not None:
            self.workspace = workspace

    @property
    def detected_name(self):
        """Gets the detected_name of this GitMetadata.  # noqa: E501

        Detected Name  # noqa: E501

        :return: The detected_name of this GitMetadata.  # noqa: E501
        :rtype: str
        """
        return self._detected_name

    @detected_name.setter
    def detected_name(self, detected_name):
        """Sets the detected_name of this GitMetadata.

        Detected Name  # noqa: E501

        :param detected_name: The detected_name of this GitMetadata.  # noqa: E501
        :type: str
        """

        self._detected_name = detected_name

    @property
    def detected_variant(self):
        """Gets the detected_variant of this GitMetadata.  # noqa: E501

        Detected Variant  # noqa: E501

        :return: The detected_variant of this GitMetadata.  # noqa: E501
        :rtype: str
        """
        return self._detected_variant

    @detected_variant.setter
    def detected_variant(self, detected_variant):
        """Sets the detected_variant of this GitMetadata.

        Detected Variant  # noqa: E501

        :param detected_variant: The detected_variant of this GitMetadata.  # noqa: E501
        :type: str
        """

        self._detected_variant = detected_variant

    @property
    def drone_correlated(self):
        """Gets the drone_correlated of this GitMetadata.  # noqa: E501

        Drone Correlated  # noqa: E501

        :return: The drone_correlated of this GitMetadata.  # noqa: E501
        :rtype: bool
        """
        return self._drone_correlated

    @drone_correlated.setter
    def drone_correlated(self, drone_correlated):
        """Sets the drone_correlated of this GitMetadata.

        Drone Correlated  # noqa: E501

        :param drone_correlated: The drone_correlated of this GitMetadata.  # noqa: E501
        :type: bool
        """

        self._drone_correlated = drone_correlated

    @property
    def provider(self):
        """Gets the provider of this GitMetadata.  # noqa: E501

        Git Provider  # noqa: E501

        :return: The provider of this GitMetadata.  # noqa: E501
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """Sets the provider of this GitMetadata.

        Git Provider  # noqa: E501

        :param provider: The provider of this GitMetadata.  # noqa: E501
        :type: str
        """

        self._provider = provider

    @property
    def pull_request_number(self):
        """Gets the pull_request_number of this GitMetadata.  # noqa: E501

        Git Pull Request Number  # noqa: E501

        :return: The pull_request_number of this GitMetadata.  # noqa: E501
        :rtype: int
        """
        return self._pull_request_number

    @pull_request_number.setter
    def pull_request_number(self, pull_request_number):
        """Sets the pull_request_number of this GitMetadata.

        Git Pull Request Number  # noqa: E501

        :param pull_request_number: The pull_request_number of this GitMetadata.  # noqa: E501
        :type: int
        """

        self._pull_request_number = pull_request_number

    @property
    def repository_http(self):
        """Gets the repository_http of this GitMetadata.  # noqa: E501

        Git HTTP Repository  # noqa: E501

        :return: The repository_http of this GitMetadata.  # noqa: E501
        :rtype: str
        """
        return self._repository_http

    @repository_http.setter
    def repository_http(self, repository_http):
        """Sets the repository_http of this GitMetadata.

        Git HTTP Repository  # noqa: E501

        :param repository_http: The repository_http of this GitMetadata.  # noqa: E501
        :type: str
        """

        self._repository_http = repository_http

    @property
    def repository_path(self):
        """Gets the repository_path of this GitMetadata.  # noqa: E501

        Git Repository Path  # noqa: E501

        :return: The repository_path of this GitMetadata.  # noqa: E501
        :rtype: list[str]
        """
        return self._repository_path

    @repository_path.setter
    def repository_path(self, repository_path):
        """Sets the repository_path of this GitMetadata.

        Git Repository Path  # noqa: E501

        :param repository_path: The repository_path of this GitMetadata.  # noqa: E501
        :type: list[str]
        """

        self._repository_path = repository_path

    @property
    def repository_ssh(self):
        """Gets the repository_ssh of this GitMetadata.  # noqa: E501

        Git SSH Repository  # noqa: E501

        :return: The repository_ssh of this GitMetadata.  # noqa: E501
        :rtype: str
        """
        return self._repository_ssh

    @repository_ssh.setter
    def repository_ssh(self, repository_ssh):
        """Sets the repository_ssh of this GitMetadata.

        Git SSH Repository  # noqa: E501

        :param repository_ssh: The repository_ssh of this GitMetadata.  # noqa: E501
        :type: str
        """

        self._repository_ssh = repository_ssh

    @property
    def source_branch(self):
        """Gets the source_branch of this GitMetadata.  # noqa: E501

        Git Source Branch  # noqa: E501

        :return: The source_branch of this GitMetadata.  # noqa: E501
        :rtype: str
        """
        return self._source_branch

    @source_branch.setter
    def source_branch(self, source_branch):
        """Sets the source_branch of this GitMetadata.

        Git Source Branch  # noqa: E501

        :param source_branch: The source_branch of this GitMetadata.  # noqa: E501
        :type: str
        """

        self._source_branch = source_branch

    @property
    def target_branch(self):
        """Gets the target_branch of this GitMetadata.  # noqa: E501

        Git Target Branch  # noqa: E501

        :return: The target_branch of this GitMetadata.  # noqa: E501
        :rtype: str
        """
        return self._target_branch

    @target_branch.setter
    def target_branch(self, target_branch):
        """Sets the target_branch of this GitMetadata.

        Git Target Branch  # noqa: E501

        :param target_branch: The target_branch of this GitMetadata.  # noqa: E501
        :type: str
        """

        self._target_branch = target_branch

    @property
    def workspace(self):
        """Gets the workspace of this GitMetadata.  # noqa: E501

        Git Workspace Root  # noqa: E501

        :return: The workspace of this GitMetadata.  # noqa: E501
        :rtype: str
        """
        return self._workspace

    @workspace.setter
    def workspace(self, workspace):
        """Sets the workspace of this GitMetadata.

        Git Workspace Root  # noqa: E501

        :param workspace: The workspace of this GitMetadata.  # noqa: E501
        :type: str
        """

        self._workspace = workspace

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
        if issubclass(GitMetadata, dict):
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
        if not isinstance(other, GitMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
