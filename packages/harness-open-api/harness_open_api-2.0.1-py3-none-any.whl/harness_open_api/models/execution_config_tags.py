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

class ExecutionConfigTags(object):
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
        'artifactory_tag': 'str',
        'default_tag': 'str',
        'git_clone_tag': 'str',
        'mongo_tag': 'str',
        'spanner_tag': 'str'
    }

    attribute_map = {
        'artifactory_tag': 'artifactoryTag',
        'default_tag': 'defaultTag',
        'git_clone_tag': 'gitCloneTag',
        'mongo_tag': 'mongoTag',
        'spanner_tag': 'spannerTag'
    }

    def __init__(self, artifactory_tag=None, default_tag=None, git_clone_tag=None, mongo_tag=None, spanner_tag=None):  # noqa: E501
        """ExecutionConfigTags - a model defined in Swagger"""  # noqa: E501
        self._artifactory_tag = None
        self._default_tag = None
        self._git_clone_tag = None
        self._mongo_tag = None
        self._spanner_tag = None
        self.discriminator = None
        if artifactory_tag is not None:
            self.artifactory_tag = artifactory_tag
        if default_tag is not None:
            self.default_tag = default_tag
        if git_clone_tag is not None:
            self.git_clone_tag = git_clone_tag
        if mongo_tag is not None:
            self.mongo_tag = mongo_tag
        if spanner_tag is not None:
            self.spanner_tag = spanner_tag

    @property
    def artifactory_tag(self):
        """Gets the artifactory_tag of this ExecutionConfigTags.  # noqa: E501


        :return: The artifactory_tag of this ExecutionConfigTags.  # noqa: E501
        :rtype: str
        """
        return self._artifactory_tag

    @artifactory_tag.setter
    def artifactory_tag(self, artifactory_tag):
        """Sets the artifactory_tag of this ExecutionConfigTags.


        :param artifactory_tag: The artifactory_tag of this ExecutionConfigTags.  # noqa: E501
        :type: str
        """

        self._artifactory_tag = artifactory_tag

    @property
    def default_tag(self):
        """Gets the default_tag of this ExecutionConfigTags.  # noqa: E501


        :return: The default_tag of this ExecutionConfigTags.  # noqa: E501
        :rtype: str
        """
        return self._default_tag

    @default_tag.setter
    def default_tag(self, default_tag):
        """Sets the default_tag of this ExecutionConfigTags.


        :param default_tag: The default_tag of this ExecutionConfigTags.  # noqa: E501
        :type: str
        """

        self._default_tag = default_tag

    @property
    def git_clone_tag(self):
        """Gets the git_clone_tag of this ExecutionConfigTags.  # noqa: E501


        :return: The git_clone_tag of this ExecutionConfigTags.  # noqa: E501
        :rtype: str
        """
        return self._git_clone_tag

    @git_clone_tag.setter
    def git_clone_tag(self, git_clone_tag):
        """Sets the git_clone_tag of this ExecutionConfigTags.


        :param git_clone_tag: The git_clone_tag of this ExecutionConfigTags.  # noqa: E501
        :type: str
        """

        self._git_clone_tag = git_clone_tag

    @property
    def mongo_tag(self):
        """Gets the mongo_tag of this ExecutionConfigTags.  # noqa: E501


        :return: The mongo_tag of this ExecutionConfigTags.  # noqa: E501
        :rtype: str
        """
        return self._mongo_tag

    @mongo_tag.setter
    def mongo_tag(self, mongo_tag):
        """Sets the mongo_tag of this ExecutionConfigTags.


        :param mongo_tag: The mongo_tag of this ExecutionConfigTags.  # noqa: E501
        :type: str
        """

        self._mongo_tag = mongo_tag

    @property
    def spanner_tag(self):
        """Gets the spanner_tag of this ExecutionConfigTags.  # noqa: E501


        :return: The spanner_tag of this ExecutionConfigTags.  # noqa: E501
        :rtype: str
        """
        return self._spanner_tag

    @spanner_tag.setter
    def spanner_tag(self, spanner_tag):
        """Sets the spanner_tag of this ExecutionConfigTags.


        :param spanner_tag: The spanner_tag of this ExecutionConfigTags.  # noqa: E501
        :type: str
        """

        self._spanner_tag = spanner_tag

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
        if issubclass(ExecutionConfigTags, dict):
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
        if not isinstance(other, ExecutionConfigTags):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
