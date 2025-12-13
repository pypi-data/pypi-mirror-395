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

class ReplicationRule(object):
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
        'allowed_patterns': 'list[str]',
        'blocked_patterns': 'list[str]',
        'created_at': 'str',
        'destination': 'ReplicationRegistry',
        'destination_type': 'str',
        'identifier': 'str',
        'modified_at': 'str',
        'parent_ref': 'str',
        'source': 'ReplicationRegistry',
        'source_type': 'str'
    }

    attribute_map = {
        'allowed_patterns': 'allowedPatterns',
        'blocked_patterns': 'blockedPatterns',
        'created_at': 'createdAt',
        'destination': 'destination',
        'destination_type': 'destinationType',
        'identifier': 'identifier',
        'modified_at': 'modifiedAt',
        'parent_ref': 'parentRef',
        'source': 'source',
        'source_type': 'sourceType'
    }

    def __init__(self, allowed_patterns=None, blocked_patterns=None, created_at=None, destination=None, destination_type=None, identifier=None, modified_at=None, parent_ref=None, source=None, source_type=None):  # noqa: E501
        """ReplicationRule - a model defined in Swagger"""  # noqa: E501
        self._allowed_patterns = None
        self._blocked_patterns = None
        self._created_at = None
        self._destination = None
        self._destination_type = None
        self._identifier = None
        self._modified_at = None
        self._parent_ref = None
        self._source = None
        self._source_type = None
        self.discriminator = None
        self.allowed_patterns = allowed_patterns
        self.blocked_patterns = blocked_patterns
        self.created_at = created_at
        self.destination = destination
        self.destination_type = destination_type
        self.identifier = identifier
        self.modified_at = modified_at
        self.parent_ref = parent_ref
        self.source = source
        self.source_type = source_type

    @property
    def allowed_patterns(self):
        """Gets the allowed_patterns of this ReplicationRule.  # noqa: E501


        :return: The allowed_patterns of this ReplicationRule.  # noqa: E501
        :rtype: list[str]
        """
        return self._allowed_patterns

    @allowed_patterns.setter
    def allowed_patterns(self, allowed_patterns):
        """Sets the allowed_patterns of this ReplicationRule.


        :param allowed_patterns: The allowed_patterns of this ReplicationRule.  # noqa: E501
        :type: list[str]
        """
        if allowed_patterns is None:
            raise ValueError("Invalid value for `allowed_patterns`, must not be `None`")  # noqa: E501

        self._allowed_patterns = allowed_patterns

    @property
    def blocked_patterns(self):
        """Gets the blocked_patterns of this ReplicationRule.  # noqa: E501


        :return: The blocked_patterns of this ReplicationRule.  # noqa: E501
        :rtype: list[str]
        """
        return self._blocked_patterns

    @blocked_patterns.setter
    def blocked_patterns(self, blocked_patterns):
        """Sets the blocked_patterns of this ReplicationRule.


        :param blocked_patterns: The blocked_patterns of this ReplicationRule.  # noqa: E501
        :type: list[str]
        """
        if blocked_patterns is None:
            raise ValueError("Invalid value for `blocked_patterns`, must not be `None`")  # noqa: E501

        self._blocked_patterns = blocked_patterns

    @property
    def created_at(self):
        """Gets the created_at of this ReplicationRule.  # noqa: E501


        :return: The created_at of this ReplicationRule.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ReplicationRule.


        :param created_at: The created_at of this ReplicationRule.  # noqa: E501
        :type: str
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def destination(self):
        """Gets the destination of this ReplicationRule.  # noqa: E501


        :return: The destination of this ReplicationRule.  # noqa: E501
        :rtype: ReplicationRegistry
        """
        return self._destination

    @destination.setter
    def destination(self, destination):
        """Sets the destination of this ReplicationRule.


        :param destination: The destination of this ReplicationRule.  # noqa: E501
        :type: ReplicationRegistry
        """
        if destination is None:
            raise ValueError("Invalid value for `destination`, must not be `None`")  # noqa: E501

        self._destination = destination

    @property
    def destination_type(self):
        """Gets the destination_type of this ReplicationRule.  # noqa: E501


        :return: The destination_type of this ReplicationRule.  # noqa: E501
        :rtype: str
        """
        return self._destination_type

    @destination_type.setter
    def destination_type(self, destination_type):
        """Sets the destination_type of this ReplicationRule.


        :param destination_type: The destination_type of this ReplicationRule.  # noqa: E501
        :type: str
        """
        if destination_type is None:
            raise ValueError("Invalid value for `destination_type`, must not be `None`")  # noqa: E501
        allowed_values = ["Local", "Jfrog", "GCP"]  # noqa: E501
        if destination_type not in allowed_values:
            raise ValueError(
                "Invalid value for `destination_type` ({0}), must be one of {1}"  # noqa: E501
                .format(destination_type, allowed_values)
            )

        self._destination_type = destination_type

    @property
    def identifier(self):
        """Gets the identifier of this ReplicationRule.  # noqa: E501


        :return: The identifier of this ReplicationRule.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this ReplicationRule.


        :param identifier: The identifier of this ReplicationRule.  # noqa: E501
        :type: str
        """
        if identifier is None:
            raise ValueError("Invalid value for `identifier`, must not be `None`")  # noqa: E501

        self._identifier = identifier

    @property
    def modified_at(self):
        """Gets the modified_at of this ReplicationRule.  # noqa: E501


        :return: The modified_at of this ReplicationRule.  # noqa: E501
        :rtype: str
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this ReplicationRule.


        :param modified_at: The modified_at of this ReplicationRule.  # noqa: E501
        :type: str
        """
        if modified_at is None:
            raise ValueError("Invalid value for `modified_at`, must not be `None`")  # noqa: E501

        self._modified_at = modified_at

    @property
    def parent_ref(self):
        """Gets the parent_ref of this ReplicationRule.  # noqa: E501


        :return: The parent_ref of this ReplicationRule.  # noqa: E501
        :rtype: str
        """
        return self._parent_ref

    @parent_ref.setter
    def parent_ref(self, parent_ref):
        """Sets the parent_ref of this ReplicationRule.


        :param parent_ref: The parent_ref of this ReplicationRule.  # noqa: E501
        :type: str
        """
        if parent_ref is None:
            raise ValueError("Invalid value for `parent_ref`, must not be `None`")  # noqa: E501

        self._parent_ref = parent_ref

    @property
    def source(self):
        """Gets the source of this ReplicationRule.  # noqa: E501


        :return: The source of this ReplicationRule.  # noqa: E501
        :rtype: ReplicationRegistry
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this ReplicationRule.


        :param source: The source of this ReplicationRule.  # noqa: E501
        :type: ReplicationRegistry
        """
        if source is None:
            raise ValueError("Invalid value for `source`, must not be `None`")  # noqa: E501

        self._source = source

    @property
    def source_type(self):
        """Gets the source_type of this ReplicationRule.  # noqa: E501


        :return: The source_type of this ReplicationRule.  # noqa: E501
        :rtype: str
        """
        return self._source_type

    @source_type.setter
    def source_type(self, source_type):
        """Sets the source_type of this ReplicationRule.


        :param source_type: The source_type of this ReplicationRule.  # noqa: E501
        :type: str
        """
        if source_type is None:
            raise ValueError("Invalid value for `source_type`, must not be `None`")  # noqa: E501
        allowed_values = ["Local", "Jfrog", "GCP"]  # noqa: E501
        if source_type not in allowed_values:
            raise ValueError(
                "Invalid value for `source_type` ({0}), must be one of {1}"  # noqa: E501
                .format(source_type, allowed_values)
            )

        self._source_type = source_type

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
        if issubclass(ReplicationRule, dict):
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
        if not isinstance(other, ReplicationRule):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
