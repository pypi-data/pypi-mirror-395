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

class Webhook(object):
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
        'created_by': 'int',
        'description': 'str',
        'enabled': 'bool',
        'extra_headers': 'list[ExtraHeader]',
        'identifier': 'str',
        'insecure': 'bool',
        'internal': 'bool',
        'latest_execution_result': 'WebhookExecResult',
        'modified_at': 'str',
        'name': 'str',
        'secret_identifier': 'str',
        'secret_space_id': 'int',
        'secret_space_path': 'str',
        'triggers': 'list[Trigger]',
        'url': 'str',
        'version': 'int'
    }

    attribute_map = {
        'created_at': 'createdAt',
        'created_by': 'createdBy',
        'description': 'description',
        'enabled': 'enabled',
        'extra_headers': 'extraHeaders',
        'identifier': 'identifier',
        'insecure': 'insecure',
        'internal': 'internal',
        'latest_execution_result': 'latestExecutionResult',
        'modified_at': 'modifiedAt',
        'name': 'name',
        'secret_identifier': 'secretIdentifier',
        'secret_space_id': 'secretSpaceId',
        'secret_space_path': 'secretSpacePath',
        'triggers': 'triggers',
        'url': 'url',
        'version': 'version'
    }

    def __init__(self, created_at=None, created_by=None, description=None, enabled=None, extra_headers=None, identifier=None, insecure=None, internal=None, latest_execution_result=None, modified_at=None, name=None, secret_identifier=None, secret_space_id=None, secret_space_path=None, triggers=None, url=None, version=None):  # noqa: E501
        """Webhook - a model defined in Swagger"""  # noqa: E501
        self._created_at = None
        self._created_by = None
        self._description = None
        self._enabled = None
        self._extra_headers = None
        self._identifier = None
        self._insecure = None
        self._internal = None
        self._latest_execution_result = None
        self._modified_at = None
        self._name = None
        self._secret_identifier = None
        self._secret_space_id = None
        self._secret_space_path = None
        self._triggers = None
        self._url = None
        self._version = None
        self.discriminator = None
        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if description is not None:
            self.description = description
        self.enabled = enabled
        if extra_headers is not None:
            self.extra_headers = extra_headers
        self.identifier = identifier
        self.insecure = insecure
        if internal is not None:
            self.internal = internal
        if latest_execution_result is not None:
            self.latest_execution_result = latest_execution_result
        if modified_at is not None:
            self.modified_at = modified_at
        self.name = name
        if secret_identifier is not None:
            self.secret_identifier = secret_identifier
        if secret_space_id is not None:
            self.secret_space_id = secret_space_id
        if secret_space_path is not None:
            self.secret_space_path = secret_space_path
        if triggers is not None:
            self.triggers = triggers
        self.url = url
        if version is not None:
            self.version = version

    @property
    def created_at(self):
        """Gets the created_at of this Webhook.  # noqa: E501


        :return: The created_at of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Webhook.


        :param created_at: The created_at of this Webhook.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this Webhook.  # noqa: E501


        :return: The created_by of this Webhook.  # noqa: E501
        :rtype: int
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this Webhook.


        :param created_by: The created_by of this Webhook.  # noqa: E501
        :type: int
        """

        self._created_by = created_by

    @property
    def description(self):
        """Gets the description of this Webhook.  # noqa: E501


        :return: The description of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Webhook.


        :param description: The description of this Webhook.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def enabled(self):
        """Gets the enabled of this Webhook.  # noqa: E501


        :return: The enabled of this Webhook.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this Webhook.


        :param enabled: The enabled of this Webhook.  # noqa: E501
        :type: bool
        """
        if enabled is None:
            raise ValueError("Invalid value for `enabled`, must not be `None`")  # noqa: E501

        self._enabled = enabled

    @property
    def extra_headers(self):
        """Gets the extra_headers of this Webhook.  # noqa: E501


        :return: The extra_headers of this Webhook.  # noqa: E501
        :rtype: list[ExtraHeader]
        """
        return self._extra_headers

    @extra_headers.setter
    def extra_headers(self, extra_headers):
        """Sets the extra_headers of this Webhook.


        :param extra_headers: The extra_headers of this Webhook.  # noqa: E501
        :type: list[ExtraHeader]
        """

        self._extra_headers = extra_headers

    @property
    def identifier(self):
        """Gets the identifier of this Webhook.  # noqa: E501


        :return: The identifier of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this Webhook.


        :param identifier: The identifier of this Webhook.  # noqa: E501
        :type: str
        """
        if identifier is None:
            raise ValueError("Invalid value for `identifier`, must not be `None`")  # noqa: E501

        self._identifier = identifier

    @property
    def insecure(self):
        """Gets the insecure of this Webhook.  # noqa: E501


        :return: The insecure of this Webhook.  # noqa: E501
        :rtype: bool
        """
        return self._insecure

    @insecure.setter
    def insecure(self, insecure):
        """Sets the insecure of this Webhook.


        :param insecure: The insecure of this Webhook.  # noqa: E501
        :type: bool
        """
        if insecure is None:
            raise ValueError("Invalid value for `insecure`, must not be `None`")  # noqa: E501

        self._insecure = insecure

    @property
    def internal(self):
        """Gets the internal of this Webhook.  # noqa: E501


        :return: The internal of this Webhook.  # noqa: E501
        :rtype: bool
        """
        return self._internal

    @internal.setter
    def internal(self, internal):
        """Sets the internal of this Webhook.


        :param internal: The internal of this Webhook.  # noqa: E501
        :type: bool
        """

        self._internal = internal

    @property
    def latest_execution_result(self):
        """Gets the latest_execution_result of this Webhook.  # noqa: E501


        :return: The latest_execution_result of this Webhook.  # noqa: E501
        :rtype: WebhookExecResult
        """
        return self._latest_execution_result

    @latest_execution_result.setter
    def latest_execution_result(self, latest_execution_result):
        """Sets the latest_execution_result of this Webhook.


        :param latest_execution_result: The latest_execution_result of this Webhook.  # noqa: E501
        :type: WebhookExecResult
        """

        self._latest_execution_result = latest_execution_result

    @property
    def modified_at(self):
        """Gets the modified_at of this Webhook.  # noqa: E501


        :return: The modified_at of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this Webhook.


        :param modified_at: The modified_at of this Webhook.  # noqa: E501
        :type: str
        """

        self._modified_at = modified_at

    @property
    def name(self):
        """Gets the name of this Webhook.  # noqa: E501


        :return: The name of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Webhook.


        :param name: The name of this Webhook.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def secret_identifier(self):
        """Gets the secret_identifier of this Webhook.  # noqa: E501


        :return: The secret_identifier of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._secret_identifier

    @secret_identifier.setter
    def secret_identifier(self, secret_identifier):
        """Sets the secret_identifier of this Webhook.


        :param secret_identifier: The secret_identifier of this Webhook.  # noqa: E501
        :type: str
        """

        self._secret_identifier = secret_identifier

    @property
    def secret_space_id(self):
        """Gets the secret_space_id of this Webhook.  # noqa: E501


        :return: The secret_space_id of this Webhook.  # noqa: E501
        :rtype: int
        """
        return self._secret_space_id

    @secret_space_id.setter
    def secret_space_id(self, secret_space_id):
        """Sets the secret_space_id of this Webhook.


        :param secret_space_id: The secret_space_id of this Webhook.  # noqa: E501
        :type: int
        """

        self._secret_space_id = secret_space_id

    @property
    def secret_space_path(self):
        """Gets the secret_space_path of this Webhook.  # noqa: E501


        :return: The secret_space_path of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._secret_space_path

    @secret_space_path.setter
    def secret_space_path(self, secret_space_path):
        """Sets the secret_space_path of this Webhook.


        :param secret_space_path: The secret_space_path of this Webhook.  # noqa: E501
        :type: str
        """

        self._secret_space_path = secret_space_path

    @property
    def triggers(self):
        """Gets the triggers of this Webhook.  # noqa: E501


        :return: The triggers of this Webhook.  # noqa: E501
        :rtype: list[Trigger]
        """
        return self._triggers

    @triggers.setter
    def triggers(self, triggers):
        """Sets the triggers of this Webhook.


        :param triggers: The triggers of this Webhook.  # noqa: E501
        :type: list[Trigger]
        """

        self._triggers = triggers

    @property
    def url(self):
        """Gets the url of this Webhook.  # noqa: E501


        :return: The url of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this Webhook.


        :param url: The url of this Webhook.  # noqa: E501
        :type: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def version(self):
        """Gets the version of this Webhook.  # noqa: E501


        :return: The version of this Webhook.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Webhook.


        :param version: The version of this Webhook.  # noqa: E501
        :type: int
        """

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
        if issubclass(Webhook, dict):
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
        if not isinstance(other, Webhook):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
