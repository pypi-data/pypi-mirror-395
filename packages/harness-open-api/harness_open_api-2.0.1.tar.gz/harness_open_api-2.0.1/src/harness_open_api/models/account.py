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

class Account(object):
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
        'absolute_session_timeout_in_minutes': 'int',
        'account_status': 'str',
        'account_type': 'str',
        'authentication_mechanism': 'str',
        'canny_username_abbreviation_enabled': 'bool',
        'cluster': 'str',
        'company_name': 'str',
        'created_at': 'int',
        'cross_generation_access_enabled': 'bool',
        'default_experience': 'str',
        'expiry_time': 'int',
        'harness_support_access_allowed': 'bool',
        'identifier': 'str',
        'name': 'str',
        'next_gen_enabled': 'bool',
        'oauth_enabled': 'bool',
        'product_led': 'bool',
        'public_access_enabled': 'bool',
        'ring_name': 'str',
        'service_account_config': 'ServiceAccountConfig',
        'session_timeout_in_minutes': 'int',
        'subdomain_url': 'str',
        'two_factor_admin_enforced': 'bool'
    }

    attribute_map = {
        'absolute_session_timeout_in_minutes': 'absoluteSessionTimeoutInMinutes',
        'account_status': 'accountStatus',
        'account_type': 'accountType',
        'authentication_mechanism': 'authenticationMechanism',
        'canny_username_abbreviation_enabled': 'cannyUsernameAbbreviationEnabled',
        'cluster': 'cluster',
        'company_name': 'companyName',
        'created_at': 'createdAt',
        'cross_generation_access_enabled': 'crossGenerationAccessEnabled',
        'default_experience': 'defaultExperience',
        'expiry_time': 'expiryTime',
        'harness_support_access_allowed': 'harnessSupportAccessAllowed',
        'identifier': 'identifier',
        'name': 'name',
        'next_gen_enabled': 'nextGenEnabled',
        'oauth_enabled': 'oauthEnabled',
        'product_led': 'productLed',
        'public_access_enabled': 'publicAccessEnabled',
        'ring_name': 'ringName',
        'service_account_config': 'serviceAccountConfig',
        'session_timeout_in_minutes': 'sessionTimeoutInMinutes',
        'subdomain_url': 'subdomainURL',
        'two_factor_admin_enforced': 'twoFactorAdminEnforced'
    }

    def __init__(self, absolute_session_timeout_in_minutes=None, account_status=None, account_type=None, authentication_mechanism=None, canny_username_abbreviation_enabled=None, cluster=None, company_name=None, created_at=None, cross_generation_access_enabled=None, default_experience=None, expiry_time=None, harness_support_access_allowed=None, identifier=None, name=None, next_gen_enabled=None, oauth_enabled=None, product_led=None, public_access_enabled=None, ring_name=None, service_account_config=None, session_timeout_in_minutes=None, subdomain_url=None, two_factor_admin_enforced=None):  # noqa: E501
        """Account - a model defined in Swagger"""  # noqa: E501
        self._absolute_session_timeout_in_minutes = None
        self._account_status = None
        self._account_type = None
        self._authentication_mechanism = None
        self._canny_username_abbreviation_enabled = None
        self._cluster = None
        self._company_name = None
        self._created_at = None
        self._cross_generation_access_enabled = None
        self._default_experience = None
        self._expiry_time = None
        self._harness_support_access_allowed = None
        self._identifier = None
        self._name = None
        self._next_gen_enabled = None
        self._oauth_enabled = None
        self._product_led = None
        self._public_access_enabled = None
        self._ring_name = None
        self._service_account_config = None
        self._session_timeout_in_minutes = None
        self._subdomain_url = None
        self._two_factor_admin_enforced = None
        self.discriminator = None
        if absolute_session_timeout_in_minutes is not None:
            self.absolute_session_timeout_in_minutes = absolute_session_timeout_in_minutes
        if account_status is not None:
            self.account_status = account_status
        if account_type is not None:
            self.account_type = account_type
        if authentication_mechanism is not None:
            self.authentication_mechanism = authentication_mechanism
        if canny_username_abbreviation_enabled is not None:
            self.canny_username_abbreviation_enabled = canny_username_abbreviation_enabled
        if cluster is not None:
            self.cluster = cluster
        if company_name is not None:
            self.company_name = company_name
        if created_at is not None:
            self.created_at = created_at
        if cross_generation_access_enabled is not None:
            self.cross_generation_access_enabled = cross_generation_access_enabled
        if default_experience is not None:
            self.default_experience = default_experience
        if expiry_time is not None:
            self.expiry_time = expiry_time
        if harness_support_access_allowed is not None:
            self.harness_support_access_allowed = harness_support_access_allowed
        if identifier is not None:
            self.identifier = identifier
        if name is not None:
            self.name = name
        if next_gen_enabled is not None:
            self.next_gen_enabled = next_gen_enabled
        if oauth_enabled is not None:
            self.oauth_enabled = oauth_enabled
        if product_led is not None:
            self.product_led = product_led
        if public_access_enabled is not None:
            self.public_access_enabled = public_access_enabled
        if ring_name is not None:
            self.ring_name = ring_name
        if service_account_config is not None:
            self.service_account_config = service_account_config
        if session_timeout_in_minutes is not None:
            self.session_timeout_in_minutes = session_timeout_in_minutes
        if subdomain_url is not None:
            self.subdomain_url = subdomain_url
        if two_factor_admin_enforced is not None:
            self.two_factor_admin_enforced = two_factor_admin_enforced

    @property
    def absolute_session_timeout_in_minutes(self):
        """Gets the absolute_session_timeout_in_minutes of this Account.  # noqa: E501

        Absolute SessionTimeout in minutes  # noqa: E501

        :return: The absolute_session_timeout_in_minutes of this Account.  # noqa: E501
        :rtype: int
        """
        return self._absolute_session_timeout_in_minutes

    @absolute_session_timeout_in_minutes.setter
    def absolute_session_timeout_in_minutes(self, absolute_session_timeout_in_minutes):
        """Sets the absolute_session_timeout_in_minutes of this Account.

        Absolute SessionTimeout in minutes  # noqa: E501

        :param absolute_session_timeout_in_minutes: The absolute_session_timeout_in_minutes of this Account.  # noqa: E501
        :type: int
        """

        self._absolute_session_timeout_in_minutes = absolute_session_timeout_in_minutes

    @property
    def account_status(self):
        """Gets the account_status of this Account.  # noqa: E501

        Status of the Account  # noqa: E501

        :return: The account_status of this Account.  # noqa: E501
        :rtype: str
        """
        return self._account_status

    @account_status.setter
    def account_status(self, account_status):
        """Sets the account_status of this Account.

        Status of the Account  # noqa: E501

        :param account_status: The account_status of this Account.  # noqa: E501
        :type: str
        """

        self._account_status = account_status

    @property
    def account_type(self):
        """Gets the account_type of this Account.  # noqa: E501

        Type of the Account  # noqa: E501

        :return: The account_type of this Account.  # noqa: E501
        :rtype: str
        """
        return self._account_type

    @account_type.setter
    def account_type(self, account_type):
        """Sets the account_type of this Account.

        Type of the Account  # noqa: E501

        :param account_type: The account_type of this Account.  # noqa: E501
        :type: str
        """

        self._account_type = account_type

    @property
    def authentication_mechanism(self):
        """Gets the authentication_mechanism of this Account.  # noqa: E501

        Authentication mechanism associated with the account.  # noqa: E501

        :return: The authentication_mechanism of this Account.  # noqa: E501
        :rtype: str
        """
        return self._authentication_mechanism

    @authentication_mechanism.setter
    def authentication_mechanism(self, authentication_mechanism):
        """Sets the authentication_mechanism of this Account.

        Authentication mechanism associated with the account.  # noqa: E501

        :param authentication_mechanism: The authentication_mechanism of this Account.  # noqa: E501
        :type: str
        """
        allowed_values = ["USER_PASSWORD", "SAML", "LDAP", "OAUTH", "OIDC"]  # noqa: E501
        if authentication_mechanism not in allowed_values:
            raise ValueError(
                "Invalid value for `authentication_mechanism` ({0}), must be one of {1}"  # noqa: E501
                .format(authentication_mechanism, allowed_values)
            )

        self._authentication_mechanism = authentication_mechanism

    @property
    def canny_username_abbreviation_enabled(self):
        """Gets the canny_username_abbreviation_enabled of this Account.  # noqa: E501


        :return: The canny_username_abbreviation_enabled of this Account.  # noqa: E501
        :rtype: bool
        """
        return self._canny_username_abbreviation_enabled

    @canny_username_abbreviation_enabled.setter
    def canny_username_abbreviation_enabled(self, canny_username_abbreviation_enabled):
        """Sets the canny_username_abbreviation_enabled of this Account.


        :param canny_username_abbreviation_enabled: The canny_username_abbreviation_enabled of this Account.  # noqa: E501
        :type: bool
        """

        self._canny_username_abbreviation_enabled = canny_username_abbreviation_enabled

    @property
    def cluster(self):
        """Gets the cluster of this Account.  # noqa: E501

        Name of the cluster associated with this Account.  # noqa: E501

        :return: The cluster of this Account.  # noqa: E501
        :rtype: str
        """
        return self._cluster

    @cluster.setter
    def cluster(self, cluster):
        """Sets the cluster of this Account.

        Name of the cluster associated with this Account.  # noqa: E501

        :param cluster: The cluster of this Account.  # noqa: E501
        :type: str
        """

        self._cluster = cluster

    @property
    def company_name(self):
        """Gets the company_name of this Account.  # noqa: E501

        Name of the Company.  # noqa: E501

        :return: The company_name of this Account.  # noqa: E501
        :rtype: str
        """
        return self._company_name

    @company_name.setter
    def company_name(self, company_name):
        """Sets the company_name of this Account.

        Name of the Company.  # noqa: E501

        :param company_name: The company_name of this Account.  # noqa: E501
        :type: str
        """

        self._company_name = company_name

    @property
    def created_at(self):
        """Gets the created_at of this Account.  # noqa: E501

        Account creation time in epoch  # noqa: E501

        :return: The created_at of this Account.  # noqa: E501
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Account.

        Account creation time in epoch  # noqa: E501

        :param created_at: The created_at of this Account.  # noqa: E501
        :type: int
        """

        self._created_at = created_at

    @property
    def cross_generation_access_enabled(self):
        """Gets the cross_generation_access_enabled of this Account.  # noqa: E501


        :return: The cross_generation_access_enabled of this Account.  # noqa: E501
        :rtype: bool
        """
        return self._cross_generation_access_enabled

    @cross_generation_access_enabled.setter
    def cross_generation_access_enabled(self, cross_generation_access_enabled):
        """Sets the cross_generation_access_enabled of this Account.


        :param cross_generation_access_enabled: The cross_generation_access_enabled of this Account.  # noqa: E501
        :type: bool
        """

        self._cross_generation_access_enabled = cross_generation_access_enabled

    @property
    def default_experience(self):
        """Gets the default_experience of this Account.  # noqa: E501

        Default experience of the Account.  # noqa: E501

        :return: The default_experience of this Account.  # noqa: E501
        :rtype: str
        """
        return self._default_experience

    @default_experience.setter
    def default_experience(self, default_experience):
        """Sets the default_experience of this Account.

        Default experience of the Account.  # noqa: E501

        :param default_experience: The default_experience of this Account.  # noqa: E501
        :type: str
        """
        allowed_values = ["NG", "CG"]  # noqa: E501
        if default_experience not in allowed_values:
            raise ValueError(
                "Invalid value for `default_experience` ({0}), must be one of {1}"  # noqa: E501
                .format(default_experience, allowed_values)
            )

        self._default_experience = default_experience

    @property
    def expiry_time(self):
        """Gets the expiry_time of this Account.  # noqa: E501

        Account's license expiry time in epoch  # noqa: E501

        :return: The expiry_time of this Account.  # noqa: E501
        :rtype: int
        """
        return self._expiry_time

    @expiry_time.setter
    def expiry_time(self, expiry_time):
        """Sets the expiry_time of this Account.

        Account's license expiry time in epoch  # noqa: E501

        :param expiry_time: The expiry_time of this Account.  # noqa: E501
        :type: int
        """

        self._expiry_time = expiry_time

    @property
    def harness_support_access_allowed(self):
        """Gets the harness_support_access_allowed of this Account.  # noqa: E501


        :return: The harness_support_access_allowed of this Account.  # noqa: E501
        :rtype: bool
        """
        return self._harness_support_access_allowed

    @harness_support_access_allowed.setter
    def harness_support_access_allowed(self, harness_support_access_allowed):
        """Sets the harness_support_access_allowed of this Account.


        :param harness_support_access_allowed: The harness_support_access_allowed of this Account.  # noqa: E501
        :type: bool
        """

        self._harness_support_access_allowed = harness_support_access_allowed

    @property
    def identifier(self):
        """Gets the identifier of this Account.  # noqa: E501

        Account Identifier.  # noqa: E501

        :return: The identifier of this Account.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this Account.

        Account Identifier.  # noqa: E501

        :param identifier: The identifier of this Account.  # noqa: E501
        :type: str
        """

        self._identifier = identifier

    @property
    def name(self):
        """Gets the name of this Account.  # noqa: E501

        Name of the Account.  # noqa: E501

        :return: The name of this Account.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Account.

        Name of the Account.  # noqa: E501

        :param name: The name of this Account.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def next_gen_enabled(self):
        """Gets the next_gen_enabled of this Account.  # noqa: E501


        :return: The next_gen_enabled of this Account.  # noqa: E501
        :rtype: bool
        """
        return self._next_gen_enabled

    @next_gen_enabled.setter
    def next_gen_enabled(self, next_gen_enabled):
        """Sets the next_gen_enabled of this Account.


        :param next_gen_enabled: The next_gen_enabled of this Account.  # noqa: E501
        :type: bool
        """

        self._next_gen_enabled = next_gen_enabled

    @property
    def oauth_enabled(self):
        """Gets the oauth_enabled of this Account.  # noqa: E501


        :return: The oauth_enabled of this Account.  # noqa: E501
        :rtype: bool
        """
        return self._oauth_enabled

    @oauth_enabled.setter
    def oauth_enabled(self, oauth_enabled):
        """Sets the oauth_enabled of this Account.


        :param oauth_enabled: The oauth_enabled of this Account.  # noqa: E501
        :type: bool
        """

        self._oauth_enabled = oauth_enabled

    @property
    def product_led(self):
        """Gets the product_led of this Account.  # noqa: E501


        :return: The product_led of this Account.  # noqa: E501
        :rtype: bool
        """
        return self._product_led

    @product_led.setter
    def product_led(self, product_led):
        """Sets the product_led of this Account.


        :param product_led: The product_led of this Account.  # noqa: E501
        :type: bool
        """

        self._product_led = product_led

    @property
    def public_access_enabled(self):
        """Gets the public_access_enabled of this Account.  # noqa: E501

        Specifies if Account has public access enabled.  # noqa: E501

        :return: The public_access_enabled of this Account.  # noqa: E501
        :rtype: bool
        """
        return self._public_access_enabled

    @public_access_enabled.setter
    def public_access_enabled(self, public_access_enabled):
        """Sets the public_access_enabled of this Account.

        Specifies if Account has public access enabled.  # noqa: E501

        :param public_access_enabled: The public_access_enabled of this Account.  # noqa: E501
        :type: bool
        """

        self._public_access_enabled = public_access_enabled

    @property
    def ring_name(self):
        """Gets the ring_name of this Account.  # noqa: E501

        Specifies delegate ring version for account  # noqa: E501

        :return: The ring_name of this Account.  # noqa: E501
        :rtype: str
        """
        return self._ring_name

    @ring_name.setter
    def ring_name(self, ring_name):
        """Sets the ring_name of this Account.

        Specifies delegate ring version for account  # noqa: E501

        :param ring_name: The ring_name of this Account.  # noqa: E501
        :type: str
        """

        self._ring_name = ring_name

    @property
    def service_account_config(self):
        """Gets the service_account_config of this Account.  # noqa: E501


        :return: The service_account_config of this Account.  # noqa: E501
        :rtype: ServiceAccountConfig
        """
        return self._service_account_config

    @service_account_config.setter
    def service_account_config(self, service_account_config):
        """Sets the service_account_config of this Account.


        :param service_account_config: The service_account_config of this Account.  # noqa: E501
        :type: ServiceAccountConfig
        """

        self._service_account_config = service_account_config

    @property
    def session_timeout_in_minutes(self):
        """Gets the session_timeout_in_minutes of this Account.  # noqa: E501

        SessionTimeout in minutes  # noqa: E501

        :return: The session_timeout_in_minutes of this Account.  # noqa: E501
        :rtype: int
        """
        return self._session_timeout_in_minutes

    @session_timeout_in_minutes.setter
    def session_timeout_in_minutes(self, session_timeout_in_minutes):
        """Sets the session_timeout_in_minutes of this Account.

        SessionTimeout in minutes  # noqa: E501

        :param session_timeout_in_minutes: The session_timeout_in_minutes of this Account.  # noqa: E501
        :type: int
        """

        self._session_timeout_in_minutes = session_timeout_in_minutes

    @property
    def subdomain_url(self):
        """Gets the subdomain_url of this Account.  # noqa: E501

        Specifies subdomain url for account  # noqa: E501

        :return: The subdomain_url of this Account.  # noqa: E501
        :rtype: str
        """
        return self._subdomain_url

    @subdomain_url.setter
    def subdomain_url(self, subdomain_url):
        """Sets the subdomain_url of this Account.

        Specifies subdomain url for account  # noqa: E501

        :param subdomain_url: The subdomain_url of this Account.  # noqa: E501
        :type: str
        """

        self._subdomain_url = subdomain_url

    @property
    def two_factor_admin_enforced(self):
        """Gets the two_factor_admin_enforced of this Account.  # noqa: E501


        :return: The two_factor_admin_enforced of this Account.  # noqa: E501
        :rtype: bool
        """
        return self._two_factor_admin_enforced

    @two_factor_admin_enforced.setter
    def two_factor_admin_enforced(self, two_factor_admin_enforced):
        """Sets the two_factor_admin_enforced of this Account.


        :param two_factor_admin_enforced: The two_factor_admin_enforced of this Account.  # noqa: E501
        :type: bool
        """

        self._two_factor_admin_enforced = two_factor_admin_enforced

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
        if issubclass(Account, dict):
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
        if not isinstance(other, Account):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
