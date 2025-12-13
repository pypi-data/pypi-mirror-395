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

class Registry(object):
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
        'allowed_pattern': 'list[str]',
        'blocked_pattern': 'list[str]',
        'cleanup_policy': 'list[CleanupPolicy]',
        'config': 'RegistryConfig',
        'created_at': 'str',
        'description': 'str',
        'identifier': 'str',
        'is_public': 'bool',
        'labels': 'list[str]',
        'modified_at': 'str',
        'package_type': 'PackageType',
        'policy_refs': 'list[str]',
        'scanners': 'list[Scanner]',
        'url': 'str'
    }

    attribute_map = {
        'allowed_pattern': 'allowedPattern',
        'blocked_pattern': 'blockedPattern',
        'cleanup_policy': 'cleanupPolicy',
        'config': 'config',
        'created_at': 'createdAt',
        'description': 'description',
        'identifier': 'identifier',
        'is_public': 'isPublic',
        'labels': 'labels',
        'modified_at': 'modifiedAt',
        'package_type': 'packageType',
        'policy_refs': 'policyRefs',
        'scanners': 'scanners',
        'url': 'url'
    }

    def __init__(self, allowed_pattern=None, blocked_pattern=None, cleanup_policy=None, config=None, created_at=None, description=None, identifier=None, is_public=None, labels=None, modified_at=None, package_type=None, policy_refs=None, scanners=None, url=None):  # noqa: E501
        """Registry - a model defined in Swagger"""  # noqa: E501
        self._allowed_pattern = None
        self._blocked_pattern = None
        self._cleanup_policy = None
        self._config = None
        self._created_at = None
        self._description = None
        self._identifier = None
        self._is_public = None
        self._labels = None
        self._modified_at = None
        self._package_type = None
        self._policy_refs = None
        self._scanners = None
        self._url = None
        self.discriminator = None
        if allowed_pattern is not None:
            self.allowed_pattern = allowed_pattern
        if blocked_pattern is not None:
            self.blocked_pattern = blocked_pattern
        if cleanup_policy is not None:
            self.cleanup_policy = cleanup_policy
        if config is not None:
            self.config = config
        if created_at is not None:
            self.created_at = created_at
        if description is not None:
            self.description = description
        self.identifier = identifier
        self.is_public = is_public
        if labels is not None:
            self.labels = labels
        if modified_at is not None:
            self.modified_at = modified_at
        self.package_type = package_type
        if policy_refs is not None:
            self.policy_refs = policy_refs
        if scanners is not None:
            self.scanners = scanners
        self.url = url

    @property
    def allowed_pattern(self):
        """Gets the allowed_pattern of this Registry.  # noqa: E501


        :return: The allowed_pattern of this Registry.  # noqa: E501
        :rtype: list[str]
        """
        return self._allowed_pattern

    @allowed_pattern.setter
    def allowed_pattern(self, allowed_pattern):
        """Sets the allowed_pattern of this Registry.


        :param allowed_pattern: The allowed_pattern of this Registry.  # noqa: E501
        :type: list[str]
        """

        self._allowed_pattern = allowed_pattern

    @property
    def blocked_pattern(self):
        """Gets the blocked_pattern of this Registry.  # noqa: E501


        :return: The blocked_pattern of this Registry.  # noqa: E501
        :rtype: list[str]
        """
        return self._blocked_pattern

    @blocked_pattern.setter
    def blocked_pattern(self, blocked_pattern):
        """Sets the blocked_pattern of this Registry.


        :param blocked_pattern: The blocked_pattern of this Registry.  # noqa: E501
        :type: list[str]
        """

        self._blocked_pattern = blocked_pattern

    @property
    def cleanup_policy(self):
        """Gets the cleanup_policy of this Registry.  # noqa: E501


        :return: The cleanup_policy of this Registry.  # noqa: E501
        :rtype: list[CleanupPolicy]
        """
        return self._cleanup_policy

    @cleanup_policy.setter
    def cleanup_policy(self, cleanup_policy):
        """Sets the cleanup_policy of this Registry.


        :param cleanup_policy: The cleanup_policy of this Registry.  # noqa: E501
        :type: list[CleanupPolicy]
        """

        self._cleanup_policy = cleanup_policy

    @property
    def config(self):
        """Gets the config of this Registry.  # noqa: E501


        :return: The config of this Registry.  # noqa: E501
        :rtype: RegistryConfig
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this Registry.


        :param config: The config of this Registry.  # noqa: E501
        :type: RegistryConfig
        """

        self._config = config

    @property
    def created_at(self):
        """Gets the created_at of this Registry.  # noqa: E501


        :return: The created_at of this Registry.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Registry.


        :param created_at: The created_at of this Registry.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def description(self):
        """Gets the description of this Registry.  # noqa: E501


        :return: The description of this Registry.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Registry.


        :param description: The description of this Registry.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def identifier(self):
        """Gets the identifier of this Registry.  # noqa: E501


        :return: The identifier of this Registry.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this Registry.


        :param identifier: The identifier of this Registry.  # noqa: E501
        :type: str
        """
        if identifier is None:
            raise ValueError("Invalid value for `identifier`, must not be `None`")  # noqa: E501

        self._identifier = identifier

    @property
    def is_public(self):
        """Gets the is_public of this Registry.  # noqa: E501


        :return: The is_public of this Registry.  # noqa: E501
        :rtype: bool
        """
        return self._is_public

    @is_public.setter
    def is_public(self, is_public):
        """Sets the is_public of this Registry.


        :param is_public: The is_public of this Registry.  # noqa: E501
        :type: bool
        """
        if is_public is None:
            raise ValueError("Invalid value for `is_public`, must not be `None`")  # noqa: E501

        self._is_public = is_public

    @property
    def labels(self):
        """Gets the labels of this Registry.  # noqa: E501


        :return: The labels of this Registry.  # noqa: E501
        :rtype: list[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this Registry.


        :param labels: The labels of this Registry.  # noqa: E501
        :type: list[str]
        """

        self._labels = labels

    @property
    def modified_at(self):
        """Gets the modified_at of this Registry.  # noqa: E501


        :return: The modified_at of this Registry.  # noqa: E501
        :rtype: str
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this Registry.


        :param modified_at: The modified_at of this Registry.  # noqa: E501
        :type: str
        """

        self._modified_at = modified_at

    @property
    def package_type(self):
        """Gets the package_type of this Registry.  # noqa: E501


        :return: The package_type of this Registry.  # noqa: E501
        :rtype: PackageType
        """
        return self._package_type

    @package_type.setter
    def package_type(self, package_type):
        """Sets the package_type of this Registry.


        :param package_type: The package_type of this Registry.  # noqa: E501
        :type: PackageType
        """
        if package_type is None:
            raise ValueError("Invalid value for `package_type`, must not be `None`")  # noqa: E501

        self._package_type = package_type

    @property
    def policy_refs(self):
        """Gets the policy_refs of this Registry.  # noqa: E501


        :return: The policy_refs of this Registry.  # noqa: E501
        :rtype: list[str]
        """
        return self._policy_refs

    @policy_refs.setter
    def policy_refs(self, policy_refs):
        """Sets the policy_refs of this Registry.


        :param policy_refs: The policy_refs of this Registry.  # noqa: E501
        :type: list[str]
        """

        self._policy_refs = policy_refs

    @property
    def scanners(self):
        """Gets the scanners of this Registry.  # noqa: E501


        :return: The scanners of this Registry.  # noqa: E501
        :rtype: list[Scanner]
        """
        return self._scanners

    @scanners.setter
    def scanners(self, scanners):
        """Sets the scanners of this Registry.


        :param scanners: The scanners of this Registry.  # noqa: E501
        :type: list[Scanner]
        """

        self._scanners = scanners

    @property
    def url(self):
        """Gets the url of this Registry.  # noqa: E501


        :return: The url of this Registry.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this Registry.


        :param url: The url of this Registry.  # noqa: E501
        :type: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

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
        if issubclass(Registry, dict):
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
        if not isinstance(other, Registry):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
