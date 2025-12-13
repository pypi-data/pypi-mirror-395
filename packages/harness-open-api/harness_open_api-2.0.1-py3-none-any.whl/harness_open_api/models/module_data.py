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

class ModuleData(object):
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
        'account': 'str',
        'download_url': 'str',
        'error': 'dict(str, str)',
        'examples_paths': 'list[str]',
        'git_tag': 'str',
        'metadata': 'str',
        'name': 'str',
        'repo_url': 'str',
        'submodule_name': 'str',
        'submodule_paths': 'list[str]',
        'system': 'str',
        'version': 'str'
    }

    attribute_map = {
        'account': 'account',
        'download_url': 'download_url',
        'error': 'error',
        'examples_paths': 'examples_paths',
        'git_tag': 'git_tag',
        'metadata': 'metadata',
        'name': 'name',
        'repo_url': 'repo_url',
        'submodule_name': 'submodule_name',
        'submodule_paths': 'submodule_paths',
        'system': 'system',
        'version': 'version'
    }

    def __init__(self, account=None, download_url=None, error=None, examples_paths=None, git_tag=None, metadata=None, name=None, repo_url=None, submodule_name=None, submodule_paths=None, system=None, version=None):  # noqa: E501
        """ModuleData - a model defined in Swagger"""  # noqa: E501
        self._account = None
        self._download_url = None
        self._error = None
        self._examples_paths = None
        self._git_tag = None
        self._metadata = None
        self._name = None
        self._repo_url = None
        self._submodule_name = None
        self._submodule_paths = None
        self._system = None
        self._version = None
        self.discriminator = None
        self.account = account
        self.download_url = download_url
        if error is not None:
            self.error = error
        if examples_paths is not None:
            self.examples_paths = examples_paths
        self.git_tag = git_tag
        self.metadata = metadata
        self.name = name
        if repo_url is not None:
            self.repo_url = repo_url
        if submodule_name is not None:
            self.submodule_name = submodule_name
        if submodule_paths is not None:
            self.submodule_paths = submodule_paths
        self.system = system
        self.version = version

    @property
    def account(self):
        """Gets the account of this ModuleData.  # noqa: E501

        account name  # noqa: E501

        :return: The account of this ModuleData.  # noqa: E501
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this ModuleData.

        account name  # noqa: E501

        :param account: The account of this ModuleData.  # noqa: E501
        :type: str
        """
        if account is None:
            raise ValueError("Invalid value for `account`, must not be `None`")  # noqa: E501

        self._account = account

    @property
    def download_url(self):
        """Gets the download_url of this ModuleData.  # noqa: E501

        download url of the module  # noqa: E501

        :return: The download_url of this ModuleData.  # noqa: E501
        :rtype: str
        """
        return self._download_url

    @download_url.setter
    def download_url(self, download_url):
        """Sets the download_url of this ModuleData.

        download url of the module  # noqa: E501

        :param download_url: The download_url of this ModuleData.  # noqa: E501
        :type: str
        """
        if download_url is None:
            raise ValueError("Invalid value for `download_url`, must not be `None`")  # noqa: E501

        self._download_url = download_url

    @property
    def error(self):
        """Gets the error of this ModuleData.  # noqa: E501

        error from the tag operation  # noqa: E501

        :return: The error of this ModuleData.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this ModuleData.

        error from the tag operation  # noqa: E501

        :param error: The error of this ModuleData.  # noqa: E501
        :type: dict(str, str)
        """

        self._error = error

    @property
    def examples_paths(self):
        """Gets the examples_paths of this ModuleData.  # noqa: E501

        path of the examples relative to the module  # noqa: E501

        :return: The examples_paths of this ModuleData.  # noqa: E501
        :rtype: list[str]
        """
        return self._examples_paths

    @examples_paths.setter
    def examples_paths(self, examples_paths):
        """Sets the examples_paths of this ModuleData.

        path of the examples relative to the module  # noqa: E501

        :param examples_paths: The examples_paths of this ModuleData.  # noqa: E501
        :type: list[str]
        """

        self._examples_paths = examples_paths

    @property
    def git_tag(self):
        """Gets the git_tag of this ModuleData.  # noqa: E501

        git tag of the module  # noqa: E501

        :return: The git_tag of this ModuleData.  # noqa: E501
        :rtype: str
        """
        return self._git_tag

    @git_tag.setter
    def git_tag(self, git_tag):
        """Sets the git_tag of this ModuleData.

        git tag of the module  # noqa: E501

        :param git_tag: The git_tag of this ModuleData.  # noqa: E501
        :type: str
        """
        if git_tag is None:
            raise ValueError("Invalid value for `git_tag`, must not be `None`")  # noqa: E501

        self._git_tag = git_tag

    @property
    def metadata(self):
        """Gets the metadata of this ModuleData.  # noqa: E501

        metadata to be parsed  # noqa: E501

        :return: The metadata of this ModuleData.  # noqa: E501
        :rtype: str
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this ModuleData.

        metadata to be parsed  # noqa: E501

        :param metadata: The metadata of this ModuleData.  # noqa: E501
        :type: str
        """
        if metadata is None:
            raise ValueError("Invalid value for `metadata`, must not be `None`")  # noqa: E501

        self._metadata = metadata

    @property
    def name(self):
        """Gets the name of this ModuleData.  # noqa: E501

        module name  # noqa: E501

        :return: The name of this ModuleData.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ModuleData.

        module name  # noqa: E501

        :param name: The name of this ModuleData.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def repo_url(self):
        """Gets the repo_url of this ModuleData.  # noqa: E501

        url pointing to the repo  # noqa: E501

        :return: The repo_url of this ModuleData.  # noqa: E501
        :rtype: str
        """
        return self._repo_url

    @repo_url.setter
    def repo_url(self, repo_url):
        """Sets the repo_url of this ModuleData.

        url pointing to the repo  # noqa: E501

        :param repo_url: The repo_url of this ModuleData.  # noqa: E501
        :type: str
        """

        self._repo_url = repo_url

    @property
    def submodule_name(self):
        """Gets the submodule_name of this ModuleData.  # noqa: E501

        name of the submodule been processed  # noqa: E501

        :return: The submodule_name of this ModuleData.  # noqa: E501
        :rtype: str
        """
        return self._submodule_name

    @submodule_name.setter
    def submodule_name(self, submodule_name):
        """Sets the submodule_name of this ModuleData.

        name of the submodule been processed  # noqa: E501

        :param submodule_name: The submodule_name of this ModuleData.  # noqa: E501
        :type: str
        """

        self._submodule_name = submodule_name

    @property
    def submodule_paths(self):
        """Gets the submodule_paths of this ModuleData.  # noqa: E501

        path of the submodules relative to the module  # noqa: E501

        :return: The submodule_paths of this ModuleData.  # noqa: E501
        :rtype: list[str]
        """
        return self._submodule_paths

    @submodule_paths.setter
    def submodule_paths(self, submodule_paths):
        """Sets the submodule_paths of this ModuleData.

        path of the submodules relative to the module  # noqa: E501

        :param submodule_paths: The submodule_paths of this ModuleData.  # noqa: E501
        :type: list[str]
        """

        self._submodule_paths = submodule_paths

    @property
    def system(self):
        """Gets the system of this ModuleData.  # noqa: E501

        system name  # noqa: E501

        :return: The system of this ModuleData.  # noqa: E501
        :rtype: str
        """
        return self._system

    @system.setter
    def system(self, system):
        """Sets the system of this ModuleData.

        system name  # noqa: E501

        :param system: The system of this ModuleData.  # noqa: E501
        :type: str
        """
        if system is None:
            raise ValueError("Invalid value for `system`, must not be `None`")  # noqa: E501

        self._system = system

    @property
    def version(self):
        """Gets the version of this ModuleData.  # noqa: E501

        version of the module  # noqa: E501

        :return: The version of this ModuleData.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ModuleData.

        version of the module  # noqa: E501

        :param version: The version of this ModuleData.  # noqa: E501
        :type: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

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
        if issubclass(ModuleData, dict):
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
        if not isinstance(other, ModuleData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
