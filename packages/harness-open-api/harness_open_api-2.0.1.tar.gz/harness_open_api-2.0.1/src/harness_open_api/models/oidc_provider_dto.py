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

class OidcProviderDTO(object):
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
        'authorization_config': 'OidcAuthorizationConfigDTO',
        'client_config': 'OidcClientConfigDTO',
        'discovery': 'bool',
        'identifier': 'str',
        'issuer': 'str',
        'jit_config': 'OidcJitConfigDTO',
        'name': 'str',
        'pkce': 'bool',
        'response_type': 'str',
        'scope': 'list[str]',
        'send_scope_to_token_endpoint': 'bool',
        'uid_field': 'str'
    }

    attribute_map = {
        'authorization_config': 'authorizationConfig',
        'client_config': 'clientConfig',
        'discovery': 'discovery',
        'identifier': 'identifier',
        'issuer': 'issuer',
        'jit_config': 'jitConfig',
        'name': 'name',
        'pkce': 'pkce',
        'response_type': 'response_type',
        'scope': 'scope',
        'send_scope_to_token_endpoint': 'send_scope_to_token_endpoint',
        'uid_field': 'uid_field'
    }

    def __init__(self, authorization_config=None, client_config=None, discovery=None, identifier=None, issuer=None, jit_config=None, name=None, pkce=None, response_type=None, scope=None, send_scope_to_token_endpoint=None, uid_field=None):  # noqa: E501
        """OidcProviderDTO - a model defined in Swagger"""  # noqa: E501
        self._authorization_config = None
        self._client_config = None
        self._discovery = None
        self._identifier = None
        self._issuer = None
        self._jit_config = None
        self._name = None
        self._pkce = None
        self._response_type = None
        self._scope = None
        self._send_scope_to_token_endpoint = None
        self._uid_field = None
        self.discriminator = None
        if authorization_config is not None:
            self.authorization_config = authorization_config
        if client_config is not None:
            self.client_config = client_config
        if discovery is not None:
            self.discovery = discovery
        if identifier is not None:
            self.identifier = identifier
        if issuer is not None:
            self.issuer = issuer
        if jit_config is not None:
            self.jit_config = jit_config
        if name is not None:
            self.name = name
        if pkce is not None:
            self.pkce = pkce
        if response_type is not None:
            self.response_type = response_type
        if scope is not None:
            self.scope = scope
        if send_scope_to_token_endpoint is not None:
            self.send_scope_to_token_endpoint = send_scope_to_token_endpoint
        if uid_field is not None:
            self.uid_field = uid_field

    @property
    def authorization_config(self):
        """Gets the authorization_config of this OidcProviderDTO.  # noqa: E501


        :return: The authorization_config of this OidcProviderDTO.  # noqa: E501
        :rtype: OidcAuthorizationConfigDTO
        """
        return self._authorization_config

    @authorization_config.setter
    def authorization_config(self, authorization_config):
        """Sets the authorization_config of this OidcProviderDTO.


        :param authorization_config: The authorization_config of this OidcProviderDTO.  # noqa: E501
        :type: OidcAuthorizationConfigDTO
        """

        self._authorization_config = authorization_config

    @property
    def client_config(self):
        """Gets the client_config of this OidcProviderDTO.  # noqa: E501


        :return: The client_config of this OidcProviderDTO.  # noqa: E501
        :rtype: OidcClientConfigDTO
        """
        return self._client_config

    @client_config.setter
    def client_config(self, client_config):
        """Sets the client_config of this OidcProviderDTO.


        :param client_config: The client_config of this OidcProviderDTO.  # noqa: E501
        :type: OidcClientConfigDTO
        """

        self._client_config = client_config

    @property
    def discovery(self):
        """Gets the discovery of this OidcProviderDTO.  # noqa: E501


        :return: The discovery of this OidcProviderDTO.  # noqa: E501
        :rtype: bool
        """
        return self._discovery

    @discovery.setter
    def discovery(self, discovery):
        """Sets the discovery of this OidcProviderDTO.


        :param discovery: The discovery of this OidcProviderDTO.  # noqa: E501
        :type: bool
        """

        self._discovery = discovery

    @property
    def identifier(self):
        """Gets the identifier of this OidcProviderDTO.  # noqa: E501


        :return: The identifier of this OidcProviderDTO.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this OidcProviderDTO.


        :param identifier: The identifier of this OidcProviderDTO.  # noqa: E501
        :type: str
        """

        self._identifier = identifier

    @property
    def issuer(self):
        """Gets the issuer of this OidcProviderDTO.  # noqa: E501


        :return: The issuer of this OidcProviderDTO.  # noqa: E501
        :rtype: str
        """
        return self._issuer

    @issuer.setter
    def issuer(self, issuer):
        """Sets the issuer of this OidcProviderDTO.


        :param issuer: The issuer of this OidcProviderDTO.  # noqa: E501
        :type: str
        """

        self._issuer = issuer

    @property
    def jit_config(self):
        """Gets the jit_config of this OidcProviderDTO.  # noqa: E501


        :return: The jit_config of this OidcProviderDTO.  # noqa: E501
        :rtype: OidcJitConfigDTO
        """
        return self._jit_config

    @jit_config.setter
    def jit_config(self, jit_config):
        """Sets the jit_config of this OidcProviderDTO.


        :param jit_config: The jit_config of this OidcProviderDTO.  # noqa: E501
        :type: OidcJitConfigDTO
        """

        self._jit_config = jit_config

    @property
    def name(self):
        """Gets the name of this OidcProviderDTO.  # noqa: E501


        :return: The name of this OidcProviderDTO.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this OidcProviderDTO.


        :param name: The name of this OidcProviderDTO.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def pkce(self):
        """Gets the pkce of this OidcProviderDTO.  # noqa: E501


        :return: The pkce of this OidcProviderDTO.  # noqa: E501
        :rtype: bool
        """
        return self._pkce

    @pkce.setter
    def pkce(self, pkce):
        """Sets the pkce of this OidcProviderDTO.


        :param pkce: The pkce of this OidcProviderDTO.  # noqa: E501
        :type: bool
        """

        self._pkce = pkce

    @property
    def response_type(self):
        """Gets the response_type of this OidcProviderDTO.  # noqa: E501


        :return: The response_type of this OidcProviderDTO.  # noqa: E501
        :rtype: str
        """
        return self._response_type

    @response_type.setter
    def response_type(self, response_type):
        """Sets the response_type of this OidcProviderDTO.


        :param response_type: The response_type of this OidcProviderDTO.  # noqa: E501
        :type: str
        """
        allowed_values = ["code"]  # noqa: E501
        if response_type not in allowed_values:
            raise ValueError(
                "Invalid value for `response_type` ({0}), must be one of {1}"  # noqa: E501
                .format(response_type, allowed_values)
            )

        self._response_type = response_type

    @property
    def scope(self):
        """Gets the scope of this OidcProviderDTO.  # noqa: E501


        :return: The scope of this OidcProviderDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this OidcProviderDTO.


        :param scope: The scope of this OidcProviderDTO.  # noqa: E501
        :type: list[str]
        """

        self._scope = scope

    @property
    def send_scope_to_token_endpoint(self):
        """Gets the send_scope_to_token_endpoint of this OidcProviderDTO.  # noqa: E501


        :return: The send_scope_to_token_endpoint of this OidcProviderDTO.  # noqa: E501
        :rtype: bool
        """
        return self._send_scope_to_token_endpoint

    @send_scope_to_token_endpoint.setter
    def send_scope_to_token_endpoint(self, send_scope_to_token_endpoint):
        """Sets the send_scope_to_token_endpoint of this OidcProviderDTO.


        :param send_scope_to_token_endpoint: The send_scope_to_token_endpoint of this OidcProviderDTO.  # noqa: E501
        :type: bool
        """

        self._send_scope_to_token_endpoint = send_scope_to_token_endpoint

    @property
    def uid_field(self):
        """Gets the uid_field of this OidcProviderDTO.  # noqa: E501


        :return: The uid_field of this OidcProviderDTO.  # noqa: E501
        :rtype: str
        """
        return self._uid_field

    @uid_field.setter
    def uid_field(self, uid_field):
        """Sets the uid_field of this OidcProviderDTO.


        :param uid_field: The uid_field of this OidcProviderDTO.  # noqa: E501
        :type: str
        """

        self._uid_field = uid_field

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
        if issubclass(OidcProviderDTO, dict):
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
        if not isinstance(other, OidcProviderDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
