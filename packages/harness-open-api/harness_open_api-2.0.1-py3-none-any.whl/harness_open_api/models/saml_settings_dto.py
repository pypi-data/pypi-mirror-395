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

class SamlSettingsDTO(object):
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
        'account_id': 'str',
        'authentication_enabled': 'bool',
        'authorization_enabled': 'bool',
        'client_id': 'str',
        'client_secret': 'list[str]',
        'configured_from_ng': 'bool',
        'display_name': 'str',
        'encrypted_client_secret': 'str',
        'entity_identifier': 'str',
        'friendly_saml_name': 'str',
        'group_membership_attr': 'str',
        'jit_enabled': 'bool',
        'jit_validation_key': 'str',
        'jit_validation_value': 'str',
        'logout_url': 'str',
        'meta_data_file': 'str',
        'next_iterations': 'list[int]',
        'origin': 'str',
        'provider_type': 'str',
        'saml_provider_type': 'str',
        'type': 'str',
        'url': 'str',
        'uuid': 'str'
    }

    attribute_map = {
        'account_id': 'accountId',
        'authentication_enabled': 'authenticationEnabled',
        'authorization_enabled': 'authorizationEnabled',
        'client_id': 'clientId',
        'client_secret': 'clientSecret',
        'configured_from_ng': 'configuredFromNG',
        'display_name': 'displayName',
        'encrypted_client_secret': 'encryptedClientSecret',
        'entity_identifier': 'entityIdentifier',
        'friendly_saml_name': 'friendlySamlName',
        'group_membership_attr': 'groupMembershipAttr',
        'jit_enabled': 'jitEnabled',
        'jit_validation_key': 'jitValidationKey',
        'jit_validation_value': 'jitValidationValue',
        'logout_url': 'logoutUrl',
        'meta_data_file': 'metaDataFile',
        'next_iterations': 'nextIterations',
        'origin': 'origin',
        'provider_type': 'providerType',
        'saml_provider_type': 'samlProviderType',
        'type': 'type',
        'url': 'url',
        'uuid': 'uuid'
    }

    def __init__(self, account_id=None, authentication_enabled=None, authorization_enabled=None, client_id=None, client_secret=None, configured_from_ng=None, display_name=None, encrypted_client_secret=None, entity_identifier=None, friendly_saml_name=None, group_membership_attr=None, jit_enabled=None, jit_validation_key=None, jit_validation_value=None, logout_url=None, meta_data_file=None, next_iterations=None, origin=None, provider_type=None, saml_provider_type=None, type=None, url=None, uuid=None):  # noqa: E501
        """SamlSettingsDTO - a model defined in Swagger"""  # noqa: E501
        self._account_id = None
        self._authentication_enabled = None
        self._authorization_enabled = None
        self._client_id = None
        self._client_secret = None
        self._configured_from_ng = None
        self._display_name = None
        self._encrypted_client_secret = None
        self._entity_identifier = None
        self._friendly_saml_name = None
        self._group_membership_attr = None
        self._jit_enabled = None
        self._jit_validation_key = None
        self._jit_validation_value = None
        self._logout_url = None
        self._meta_data_file = None
        self._next_iterations = None
        self._origin = None
        self._provider_type = None
        self._saml_provider_type = None
        self._type = None
        self._url = None
        self._uuid = None
        self.discriminator = None
        self.account_id = account_id
        if authentication_enabled is not None:
            self.authentication_enabled = authentication_enabled
        if authorization_enabled is not None:
            self.authorization_enabled = authorization_enabled
        if client_id is not None:
            self.client_id = client_id
        if client_secret is not None:
            self.client_secret = client_secret
        if configured_from_ng is not None:
            self.configured_from_ng = configured_from_ng
        self.display_name = display_name
        if encrypted_client_secret is not None:
            self.encrypted_client_secret = encrypted_client_secret
        if entity_identifier is not None:
            self.entity_identifier = entity_identifier
        if friendly_saml_name is not None:
            self.friendly_saml_name = friendly_saml_name
        if group_membership_attr is not None:
            self.group_membership_attr = group_membership_attr
        if jit_enabled is not None:
            self.jit_enabled = jit_enabled
        if jit_validation_key is not None:
            self.jit_validation_key = jit_validation_key
        if jit_validation_value is not None:
            self.jit_validation_value = jit_validation_value
        if logout_url is not None:
            self.logout_url = logout_url
        if meta_data_file is not None:
            self.meta_data_file = meta_data_file
        if next_iterations is not None:
            self.next_iterations = next_iterations
        self.origin = origin
        if provider_type is not None:
            self.provider_type = provider_type
        if saml_provider_type is not None:
            self.saml_provider_type = saml_provider_type
        self.type = type
        self.url = url
        if uuid is not None:
            self.uuid = uuid

    @property
    def account_id(self):
        """Gets the account_id of this SamlSettingsDTO.  # noqa: E501


        :return: The account_id of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this SamlSettingsDTO.


        :param account_id: The account_id of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """
        if account_id is None:
            raise ValueError("Invalid value for `account_id`, must not be `None`")  # noqa: E501

        self._account_id = account_id

    @property
    def authentication_enabled(self):
        """Gets the authentication_enabled of this SamlSettingsDTO.  # noqa: E501


        :return: The authentication_enabled of this SamlSettingsDTO.  # noqa: E501
        :rtype: bool
        """
        return self._authentication_enabled

    @authentication_enabled.setter
    def authentication_enabled(self, authentication_enabled):
        """Sets the authentication_enabled of this SamlSettingsDTO.


        :param authentication_enabled: The authentication_enabled of this SamlSettingsDTO.  # noqa: E501
        :type: bool
        """

        self._authentication_enabled = authentication_enabled

    @property
    def authorization_enabled(self):
        """Gets the authorization_enabled of this SamlSettingsDTO.  # noqa: E501


        :return: The authorization_enabled of this SamlSettingsDTO.  # noqa: E501
        :rtype: bool
        """
        return self._authorization_enabled

    @authorization_enabled.setter
    def authorization_enabled(self, authorization_enabled):
        """Sets the authorization_enabled of this SamlSettingsDTO.


        :param authorization_enabled: The authorization_enabled of this SamlSettingsDTO.  # noqa: E501
        :type: bool
        """

        self._authorization_enabled = authorization_enabled

    @property
    def client_id(self):
        """Gets the client_id of this SamlSettingsDTO.  # noqa: E501


        :return: The client_id of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this SamlSettingsDTO.


        :param client_id: The client_id of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """

        self._client_id = client_id

    @property
    def client_secret(self):
        """Gets the client_secret of this SamlSettingsDTO.  # noqa: E501


        :return: The client_secret of this SamlSettingsDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._client_secret

    @client_secret.setter
    def client_secret(self, client_secret):
        """Sets the client_secret of this SamlSettingsDTO.


        :param client_secret: The client_secret of this SamlSettingsDTO.  # noqa: E501
        :type: list[str]
        """

        self._client_secret = client_secret

    @property
    def configured_from_ng(self):
        """Gets the configured_from_ng of this SamlSettingsDTO.  # noqa: E501


        :return: The configured_from_ng of this SamlSettingsDTO.  # noqa: E501
        :rtype: bool
        """
        return self._configured_from_ng

    @configured_from_ng.setter
    def configured_from_ng(self, configured_from_ng):
        """Sets the configured_from_ng of this SamlSettingsDTO.


        :param configured_from_ng: The configured_from_ng of this SamlSettingsDTO.  # noqa: E501
        :type: bool
        """

        self._configured_from_ng = configured_from_ng

    @property
    def display_name(self):
        """Gets the display_name of this SamlSettingsDTO.  # noqa: E501


        :return: The display_name of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this SamlSettingsDTO.


        :param display_name: The display_name of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """
        if display_name is None:
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501

        self._display_name = display_name

    @property
    def encrypted_client_secret(self):
        """Gets the encrypted_client_secret of this SamlSettingsDTO.  # noqa: E501


        :return: The encrypted_client_secret of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._encrypted_client_secret

    @encrypted_client_secret.setter
    def encrypted_client_secret(self, encrypted_client_secret):
        """Sets the encrypted_client_secret of this SamlSettingsDTO.


        :param encrypted_client_secret: The encrypted_client_secret of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """

        self._encrypted_client_secret = encrypted_client_secret

    @property
    def entity_identifier(self):
        """Gets the entity_identifier of this SamlSettingsDTO.  # noqa: E501


        :return: The entity_identifier of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._entity_identifier

    @entity_identifier.setter
    def entity_identifier(self, entity_identifier):
        """Sets the entity_identifier of this SamlSettingsDTO.


        :param entity_identifier: The entity_identifier of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """

        self._entity_identifier = entity_identifier

    @property
    def friendly_saml_name(self):
        """Gets the friendly_saml_name of this SamlSettingsDTO.  # noqa: E501


        :return: The friendly_saml_name of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._friendly_saml_name

    @friendly_saml_name.setter
    def friendly_saml_name(self, friendly_saml_name):
        """Sets the friendly_saml_name of this SamlSettingsDTO.


        :param friendly_saml_name: The friendly_saml_name of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """

        self._friendly_saml_name = friendly_saml_name

    @property
    def group_membership_attr(self):
        """Gets the group_membership_attr of this SamlSettingsDTO.  # noqa: E501


        :return: The group_membership_attr of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._group_membership_attr

    @group_membership_attr.setter
    def group_membership_attr(self, group_membership_attr):
        """Sets the group_membership_attr of this SamlSettingsDTO.


        :param group_membership_attr: The group_membership_attr of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """

        self._group_membership_attr = group_membership_attr

    @property
    def jit_enabled(self):
        """Gets the jit_enabled of this SamlSettingsDTO.  # noqa: E501


        :return: The jit_enabled of this SamlSettingsDTO.  # noqa: E501
        :rtype: bool
        """
        return self._jit_enabled

    @jit_enabled.setter
    def jit_enabled(self, jit_enabled):
        """Sets the jit_enabled of this SamlSettingsDTO.


        :param jit_enabled: The jit_enabled of this SamlSettingsDTO.  # noqa: E501
        :type: bool
        """

        self._jit_enabled = jit_enabled

    @property
    def jit_validation_key(self):
        """Gets the jit_validation_key of this SamlSettingsDTO.  # noqa: E501


        :return: The jit_validation_key of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._jit_validation_key

    @jit_validation_key.setter
    def jit_validation_key(self, jit_validation_key):
        """Sets the jit_validation_key of this SamlSettingsDTO.


        :param jit_validation_key: The jit_validation_key of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """

        self._jit_validation_key = jit_validation_key

    @property
    def jit_validation_value(self):
        """Gets the jit_validation_value of this SamlSettingsDTO.  # noqa: E501


        :return: The jit_validation_value of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._jit_validation_value

    @jit_validation_value.setter
    def jit_validation_value(self, jit_validation_value):
        """Sets the jit_validation_value of this SamlSettingsDTO.


        :param jit_validation_value: The jit_validation_value of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """

        self._jit_validation_value = jit_validation_value

    @property
    def logout_url(self):
        """Gets the logout_url of this SamlSettingsDTO.  # noqa: E501


        :return: The logout_url of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._logout_url

    @logout_url.setter
    def logout_url(self, logout_url):
        """Sets the logout_url of this SamlSettingsDTO.


        :param logout_url: The logout_url of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """

        self._logout_url = logout_url

    @property
    def meta_data_file(self):
        """Gets the meta_data_file of this SamlSettingsDTO.  # noqa: E501


        :return: The meta_data_file of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._meta_data_file

    @meta_data_file.setter
    def meta_data_file(self, meta_data_file):
        """Sets the meta_data_file of this SamlSettingsDTO.


        :param meta_data_file: The meta_data_file of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """

        self._meta_data_file = meta_data_file

    @property
    def next_iterations(self):
        """Gets the next_iterations of this SamlSettingsDTO.  # noqa: E501


        :return: The next_iterations of this SamlSettingsDTO.  # noqa: E501
        :rtype: list[int]
        """
        return self._next_iterations

    @next_iterations.setter
    def next_iterations(self, next_iterations):
        """Sets the next_iterations of this SamlSettingsDTO.


        :param next_iterations: The next_iterations of this SamlSettingsDTO.  # noqa: E501
        :type: list[int]
        """

        self._next_iterations = next_iterations

    @property
    def origin(self):
        """Gets the origin of this SamlSettingsDTO.  # noqa: E501


        :return: The origin of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._origin

    @origin.setter
    def origin(self, origin):
        """Sets the origin of this SamlSettingsDTO.


        :param origin: The origin of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """
        if origin is None:
            raise ValueError("Invalid value for `origin`, must not be `None`")  # noqa: E501

        self._origin = origin

    @property
    def provider_type(self):
        """Gets the provider_type of this SamlSettingsDTO.  # noqa: E501


        :return: The provider_type of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._provider_type

    @provider_type.setter
    def provider_type(self, provider_type):
        """Sets the provider_type of this SamlSettingsDTO.


        :param provider_type: The provider_type of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """
        allowed_values = ["AZURE", "OKTA", "ONELOGIN", "OTHER"]  # noqa: E501
        if provider_type not in allowed_values:
            raise ValueError(
                "Invalid value for `provider_type` ({0}), must be one of {1}"  # noqa: E501
                .format(provider_type, allowed_values)
            )

        self._provider_type = provider_type

    @property
    def saml_provider_type(self):
        """Gets the saml_provider_type of this SamlSettingsDTO.  # noqa: E501


        :return: The saml_provider_type of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._saml_provider_type

    @saml_provider_type.setter
    def saml_provider_type(self, saml_provider_type):
        """Sets the saml_provider_type of this SamlSettingsDTO.


        :param saml_provider_type: The saml_provider_type of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """
        allowed_values = ["AZURE", "OKTA", "ONELOGIN", "OTHER"]  # noqa: E501
        if saml_provider_type not in allowed_values:
            raise ValueError(
                "Invalid value for `saml_provider_type` ({0}), must be one of {1}"  # noqa: E501
                .format(saml_provider_type, allowed_values)
            )

        self._saml_provider_type = saml_provider_type

    @property
    def type(self):
        """Gets the type of this SamlSettingsDTO.  # noqa: E501


        :return: The type of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this SamlSettingsDTO.


        :param type: The type of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["SAML", "LDAP", "OAUTH", "OIDC"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def url(self):
        """Gets the url of this SamlSettingsDTO.  # noqa: E501


        :return: The url of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this SamlSettingsDTO.


        :param url: The url of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def uuid(self):
        """Gets the uuid of this SamlSettingsDTO.  # noqa: E501


        :return: The uuid of this SamlSettingsDTO.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this SamlSettingsDTO.


        :param uuid: The uuid of this SamlSettingsDTO.  # noqa: E501
        :type: str
        """

        self._uuid = uuid

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
        if issubclass(SamlSettingsDTO, dict):
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
        if not isinstance(other, SamlSettingsDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
