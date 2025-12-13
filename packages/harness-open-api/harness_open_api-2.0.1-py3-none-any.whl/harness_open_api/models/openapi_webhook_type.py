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

class OpenapiWebhookType(object):
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
        'created': 'int',
        'created_by': 'int',
        'description': 'str',
        'display_name': 'str',
        'enabled': 'bool',
        'has_secret': 'bool',
        'id': 'int',
        'identifier': 'str',
        'insecure': 'bool',
        'latest_execution_result': 'EnumWebhookExecutionResult',
        'parent_id': 'int',
        'parent_type': 'EnumWebhookParent',
        'scope': 'int',
        'triggers': 'list[EnumWebhookTrigger]',
        'updated': 'int',
        'url': 'str',
        'version': 'int'
    }

    attribute_map = {
        'created': 'created',
        'created_by': 'created_by',
        'description': 'description',
        'display_name': 'display_name',
        'enabled': 'enabled',
        'has_secret': 'has_secret',
        'id': 'id',
        'identifier': 'identifier',
        'insecure': 'insecure',
        'latest_execution_result': 'latest_execution_result',
        'parent_id': 'parent_id',
        'parent_type': 'parent_type',
        'scope': 'scope',
        'triggers': 'triggers',
        'updated': 'updated',
        'url': 'url',
        'version': 'version'
    }

    def __init__(self, created=None, created_by=None, description=None, display_name=None, enabled=None, has_secret=None, id=None, identifier=None, insecure=None, latest_execution_result=None, parent_id=None, parent_type=None, scope=None, triggers=None, updated=None, url=None, version=None):  # noqa: E501
        """OpenapiWebhookType - a model defined in Swagger"""  # noqa: E501
        self._created = None
        self._created_by = None
        self._description = None
        self._display_name = None
        self._enabled = None
        self._has_secret = None
        self._id = None
        self._identifier = None
        self._insecure = None
        self._latest_execution_result = None
        self._parent_id = None
        self._parent_type = None
        self._scope = None
        self._triggers = None
        self._updated = None
        self._url = None
        self._version = None
        self.discriminator = None
        if created is not None:
            self.created = created
        if created_by is not None:
            self.created_by = created_by
        if description is not None:
            self.description = description
        if display_name is not None:
            self.display_name = display_name
        if enabled is not None:
            self.enabled = enabled
        if has_secret is not None:
            self.has_secret = has_secret
        if id is not None:
            self.id = id
        if identifier is not None:
            self.identifier = identifier
        if insecure is not None:
            self.insecure = insecure
        if latest_execution_result is not None:
            self.latest_execution_result = latest_execution_result
        if parent_id is not None:
            self.parent_id = parent_id
        if parent_type is not None:
            self.parent_type = parent_type
        if scope is not None:
            self.scope = scope
        if triggers is not None:
            self.triggers = triggers
        if updated is not None:
            self.updated = updated
        if url is not None:
            self.url = url
        if version is not None:
            self.version = version

    @property
    def created(self):
        """Gets the created of this OpenapiWebhookType.  # noqa: E501


        :return: The created of this OpenapiWebhookType.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this OpenapiWebhookType.


        :param created: The created of this OpenapiWebhookType.  # noqa: E501
        :type: int
        """

        self._created = created

    @property
    def created_by(self):
        """Gets the created_by of this OpenapiWebhookType.  # noqa: E501


        :return: The created_by of this OpenapiWebhookType.  # noqa: E501
        :rtype: int
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this OpenapiWebhookType.


        :param created_by: The created_by of this OpenapiWebhookType.  # noqa: E501
        :type: int
        """

        self._created_by = created_by

    @property
    def description(self):
        """Gets the description of this OpenapiWebhookType.  # noqa: E501


        :return: The description of this OpenapiWebhookType.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this OpenapiWebhookType.


        :param description: The description of this OpenapiWebhookType.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def display_name(self):
        """Gets the display_name of this OpenapiWebhookType.  # noqa: E501


        :return: The display_name of this OpenapiWebhookType.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this OpenapiWebhookType.


        :param display_name: The display_name of this OpenapiWebhookType.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def enabled(self):
        """Gets the enabled of this OpenapiWebhookType.  # noqa: E501


        :return: The enabled of this OpenapiWebhookType.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this OpenapiWebhookType.


        :param enabled: The enabled of this OpenapiWebhookType.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def has_secret(self):
        """Gets the has_secret of this OpenapiWebhookType.  # noqa: E501


        :return: The has_secret of this OpenapiWebhookType.  # noqa: E501
        :rtype: bool
        """
        return self._has_secret

    @has_secret.setter
    def has_secret(self, has_secret):
        """Sets the has_secret of this OpenapiWebhookType.


        :param has_secret: The has_secret of this OpenapiWebhookType.  # noqa: E501
        :type: bool
        """

        self._has_secret = has_secret

    @property
    def id(self):
        """Gets the id of this OpenapiWebhookType.  # noqa: E501


        :return: The id of this OpenapiWebhookType.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OpenapiWebhookType.


        :param id: The id of this OpenapiWebhookType.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def identifier(self):
        """Gets the identifier of this OpenapiWebhookType.  # noqa: E501


        :return: The identifier of this OpenapiWebhookType.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this OpenapiWebhookType.


        :param identifier: The identifier of this OpenapiWebhookType.  # noqa: E501
        :type: str
        """

        self._identifier = identifier

    @property
    def insecure(self):
        """Gets the insecure of this OpenapiWebhookType.  # noqa: E501


        :return: The insecure of this OpenapiWebhookType.  # noqa: E501
        :rtype: bool
        """
        return self._insecure

    @insecure.setter
    def insecure(self, insecure):
        """Sets the insecure of this OpenapiWebhookType.


        :param insecure: The insecure of this OpenapiWebhookType.  # noqa: E501
        :type: bool
        """

        self._insecure = insecure

    @property
    def latest_execution_result(self):
        """Gets the latest_execution_result of this OpenapiWebhookType.  # noqa: E501


        :return: The latest_execution_result of this OpenapiWebhookType.  # noqa: E501
        :rtype: EnumWebhookExecutionResult
        """
        return self._latest_execution_result

    @latest_execution_result.setter
    def latest_execution_result(self, latest_execution_result):
        """Sets the latest_execution_result of this OpenapiWebhookType.


        :param latest_execution_result: The latest_execution_result of this OpenapiWebhookType.  # noqa: E501
        :type: EnumWebhookExecutionResult
        """

        self._latest_execution_result = latest_execution_result

    @property
    def parent_id(self):
        """Gets the parent_id of this OpenapiWebhookType.  # noqa: E501


        :return: The parent_id of this OpenapiWebhookType.  # noqa: E501
        :rtype: int
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """Sets the parent_id of this OpenapiWebhookType.


        :param parent_id: The parent_id of this OpenapiWebhookType.  # noqa: E501
        :type: int
        """

        self._parent_id = parent_id

    @property
    def parent_type(self):
        """Gets the parent_type of this OpenapiWebhookType.  # noqa: E501


        :return: The parent_type of this OpenapiWebhookType.  # noqa: E501
        :rtype: EnumWebhookParent
        """
        return self._parent_type

    @parent_type.setter
    def parent_type(self, parent_type):
        """Sets the parent_type of this OpenapiWebhookType.


        :param parent_type: The parent_type of this OpenapiWebhookType.  # noqa: E501
        :type: EnumWebhookParent
        """

        self._parent_type = parent_type

    @property
    def scope(self):
        """Gets the scope of this OpenapiWebhookType.  # noqa: E501


        :return: The scope of this OpenapiWebhookType.  # noqa: E501
        :rtype: int
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this OpenapiWebhookType.


        :param scope: The scope of this OpenapiWebhookType.  # noqa: E501
        :type: int
        """

        self._scope = scope

    @property
    def triggers(self):
        """Gets the triggers of this OpenapiWebhookType.  # noqa: E501


        :return: The triggers of this OpenapiWebhookType.  # noqa: E501
        :rtype: list[EnumWebhookTrigger]
        """
        return self._triggers

    @triggers.setter
    def triggers(self, triggers):
        """Sets the triggers of this OpenapiWebhookType.


        :param triggers: The triggers of this OpenapiWebhookType.  # noqa: E501
        :type: list[EnumWebhookTrigger]
        """

        self._triggers = triggers

    @property
    def updated(self):
        """Gets the updated of this OpenapiWebhookType.  # noqa: E501


        :return: The updated of this OpenapiWebhookType.  # noqa: E501
        :rtype: int
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this OpenapiWebhookType.


        :param updated: The updated of this OpenapiWebhookType.  # noqa: E501
        :type: int
        """

        self._updated = updated

    @property
    def url(self):
        """Gets the url of this OpenapiWebhookType.  # noqa: E501


        :return: The url of this OpenapiWebhookType.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this OpenapiWebhookType.


        :param url: The url of this OpenapiWebhookType.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def version(self):
        """Gets the version of this OpenapiWebhookType.  # noqa: E501


        :return: The version of this OpenapiWebhookType.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this OpenapiWebhookType.


        :param version: The version of this OpenapiWebhookType.  # noqa: E501
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
        if issubclass(OpenapiWebhookType, dict):
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
        if not isinstance(other, OpenapiWebhookType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
