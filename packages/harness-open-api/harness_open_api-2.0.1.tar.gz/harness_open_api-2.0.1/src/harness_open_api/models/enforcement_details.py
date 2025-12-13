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

class EnforcementDetails(object):
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
        'account_id_and_names': 'dict(str, str)',
        'accounts': 'list[str]',
        'cloud_provider': 'str',
        'created_at': 'int',
        'created_by': 'EmbeddedUser',
        'description': 'str',
        'enforcement_name': 'str',
        'execution_timezone': 'str',
        'is_dry_run': 'bool',
        'is_enabled': 'bool',
        'last_updated_at': 'int',
        'last_updated_by': 'EmbeddedUser',
        'regions': 'list[str]',
        'rule_ids': 'dict(str, str)',
        'rule_set_ids': 'dict(str, str)',
        'schedule': 'str'
    }

    attribute_map = {
        'account_id_and_names': 'accountIdAndNames',
        'accounts': 'accounts',
        'cloud_provider': 'cloudProvider',
        'created_at': 'createdAt',
        'created_by': 'createdBy',
        'description': 'description',
        'enforcement_name': 'enforcementName',
        'execution_timezone': 'executionTimezone',
        'is_dry_run': 'isDryRun',
        'is_enabled': 'isEnabled',
        'last_updated_at': 'lastUpdatedAt',
        'last_updated_by': 'lastUpdatedBy',
        'regions': 'regions',
        'rule_ids': 'ruleIds',
        'rule_set_ids': 'ruleSetIds',
        'schedule': 'schedule'
    }

    def __init__(self, account_id_and_names=None, accounts=None, cloud_provider=None, created_at=None, created_by=None, description=None, enforcement_name=None, execution_timezone=None, is_dry_run=None, is_enabled=None, last_updated_at=None, last_updated_by=None, regions=None, rule_ids=None, rule_set_ids=None, schedule=None):  # noqa: E501
        """EnforcementDetails - a model defined in Swagger"""  # noqa: E501
        self._account_id_and_names = None
        self._accounts = None
        self._cloud_provider = None
        self._created_at = None
        self._created_by = None
        self._description = None
        self._enforcement_name = None
        self._execution_timezone = None
        self._is_dry_run = None
        self._is_enabled = None
        self._last_updated_at = None
        self._last_updated_by = None
        self._regions = None
        self._rule_ids = None
        self._rule_set_ids = None
        self._schedule = None
        self.discriminator = None
        if account_id_and_names is not None:
            self.account_id_and_names = account_id_and_names
        if accounts is not None:
            self.accounts = accounts
        if cloud_provider is not None:
            self.cloud_provider = cloud_provider
        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if description is not None:
            self.description = description
        if enforcement_name is not None:
            self.enforcement_name = enforcement_name
        if execution_timezone is not None:
            self.execution_timezone = execution_timezone
        if is_dry_run is not None:
            self.is_dry_run = is_dry_run
        if is_enabled is not None:
            self.is_enabled = is_enabled
        if last_updated_at is not None:
            self.last_updated_at = last_updated_at
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if regions is not None:
            self.regions = regions
        if rule_ids is not None:
            self.rule_ids = rule_ids
        if rule_set_ids is not None:
            self.rule_set_ids = rule_set_ids
        if schedule is not None:
            self.schedule = schedule

    @property
    def account_id_and_names(self):
        """Gets the account_id_and_names of this EnforcementDetails.  # noqa: E501

        Target Account/Subscription/Project Id and Names  # noqa: E501

        :return: The account_id_and_names of this EnforcementDetails.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._account_id_and_names

    @account_id_and_names.setter
    def account_id_and_names(self, account_id_and_names):
        """Sets the account_id_and_names of this EnforcementDetails.

        Target Account/Subscription/Project Id and Names  # noqa: E501

        :param account_id_and_names: The account_id_and_names of this EnforcementDetails.  # noqa: E501
        :type: dict(str, str)
        """

        self._account_id_and_names = account_id_and_names

    @property
    def accounts(self):
        """Gets the accounts of this EnforcementDetails.  # noqa: E501

        Target Account/Subscription/Project Ids  # noqa: E501

        :return: The accounts of this EnforcementDetails.  # noqa: E501
        :rtype: list[str]
        """
        return self._accounts

    @accounts.setter
    def accounts(self, accounts):
        """Sets the accounts of this EnforcementDetails.

        Target Account/Subscription/Project Ids  # noqa: E501

        :param accounts: The accounts of this EnforcementDetails.  # noqa: E501
        :type: list[str]
        """

        self._accounts = accounts

    @property
    def cloud_provider(self):
        """Gets the cloud_provider of this EnforcementDetails.  # noqa: E501

        cloudProvider  # noqa: E501

        :return: The cloud_provider of this EnforcementDetails.  # noqa: E501
        :rtype: str
        """
        return self._cloud_provider

    @cloud_provider.setter
    def cloud_provider(self, cloud_provider):
        """Sets the cloud_provider of this EnforcementDetails.

        cloudProvider  # noqa: E501

        :param cloud_provider: The cloud_provider of this EnforcementDetails.  # noqa: E501
        :type: str
        """
        allowed_values = ["AWS", "AZURE", "GCP"]  # noqa: E501
        if cloud_provider not in allowed_values:
            raise ValueError(
                "Invalid value for `cloud_provider` ({0}), must be one of {1}"  # noqa: E501
                .format(cloud_provider, allowed_values)
            )

        self._cloud_provider = cloud_provider

    @property
    def created_at(self):
        """Gets the created_at of this EnforcementDetails.  # noqa: E501

        Time at which the entity was created  # noqa: E501

        :return: The created_at of this EnforcementDetails.  # noqa: E501
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this EnforcementDetails.

        Time at which the entity was created  # noqa: E501

        :param created_at: The created_at of this EnforcementDetails.  # noqa: E501
        :type: int
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this EnforcementDetails.  # noqa: E501


        :return: The created_by of this EnforcementDetails.  # noqa: E501
        :rtype: EmbeddedUser
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this EnforcementDetails.


        :param created_by: The created_by of this EnforcementDetails.  # noqa: E501
        :type: EmbeddedUser
        """

        self._created_by = created_by

    @property
    def description(self):
        """Gets the description of this EnforcementDetails.  # noqa: E501

        description  # noqa: E501

        :return: The description of this EnforcementDetails.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this EnforcementDetails.

        description  # noqa: E501

        :param description: The description of this EnforcementDetails.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def enforcement_name(self):
        """Gets the enforcement_name of this EnforcementDetails.  # noqa: E501

        Enforcement Name  # noqa: E501

        :return: The enforcement_name of this EnforcementDetails.  # noqa: E501
        :rtype: str
        """
        return self._enforcement_name

    @enforcement_name.setter
    def enforcement_name(self, enforcement_name):
        """Sets the enforcement_name of this EnforcementDetails.

        Enforcement Name  # noqa: E501

        :param enforcement_name: The enforcement_name of this EnforcementDetails.  # noqa: E501
        :type: str
        """

        self._enforcement_name = enforcement_name

    @property
    def execution_timezone(self):
        """Gets the execution_timezone of this EnforcementDetails.  # noqa: E501

        executionTimezone  # noqa: E501

        :return: The execution_timezone of this EnforcementDetails.  # noqa: E501
        :rtype: str
        """
        return self._execution_timezone

    @execution_timezone.setter
    def execution_timezone(self, execution_timezone):
        """Sets the execution_timezone of this EnforcementDetails.

        executionTimezone  # noqa: E501

        :param execution_timezone: The execution_timezone of this EnforcementDetails.  # noqa: E501
        :type: str
        """

        self._execution_timezone = execution_timezone

    @property
    def is_dry_run(self):
        """Gets the is_dry_run of this EnforcementDetails.  # noqa: E501

        isDryRun  # noqa: E501

        :return: The is_dry_run of this EnforcementDetails.  # noqa: E501
        :rtype: bool
        """
        return self._is_dry_run

    @is_dry_run.setter
    def is_dry_run(self, is_dry_run):
        """Sets the is_dry_run of this EnforcementDetails.

        isDryRun  # noqa: E501

        :param is_dry_run: The is_dry_run of this EnforcementDetails.  # noqa: E501
        :type: bool
        """

        self._is_dry_run = is_dry_run

    @property
    def is_enabled(self):
        """Gets the is_enabled of this EnforcementDetails.  # noqa: E501

        isEnabled  # noqa: E501

        :return: The is_enabled of this EnforcementDetails.  # noqa: E501
        :rtype: bool
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        """Sets the is_enabled of this EnforcementDetails.

        isEnabled  # noqa: E501

        :param is_enabled: The is_enabled of this EnforcementDetails.  # noqa: E501
        :type: bool
        """

        self._is_enabled = is_enabled

    @property
    def last_updated_at(self):
        """Gets the last_updated_at of this EnforcementDetails.  # noqa: E501

        Time at which the entity was last updated  # noqa: E501

        :return: The last_updated_at of this EnforcementDetails.  # noqa: E501
        :rtype: int
        """
        return self._last_updated_at

    @last_updated_at.setter
    def last_updated_at(self, last_updated_at):
        """Sets the last_updated_at of this EnforcementDetails.

        Time at which the entity was last updated  # noqa: E501

        :param last_updated_at: The last_updated_at of this EnforcementDetails.  # noqa: E501
        :type: int
        """

        self._last_updated_at = last_updated_at

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this EnforcementDetails.  # noqa: E501


        :return: The last_updated_by of this EnforcementDetails.  # noqa: E501
        :rtype: EmbeddedUser
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this EnforcementDetails.


        :param last_updated_by: The last_updated_by of this EnforcementDetails.  # noqa: E501
        :type: EmbeddedUser
        """

        self._last_updated_by = last_updated_by

    @property
    def regions(self):
        """Gets the regions of this EnforcementDetails.  # noqa: E501

        Target Region  # noqa: E501

        :return: The regions of this EnforcementDetails.  # noqa: E501
        :rtype: list[str]
        """
        return self._regions

    @regions.setter
    def regions(self, regions):
        """Sets the regions of this EnforcementDetails.

        Target Region  # noqa: E501

        :param regions: The regions of this EnforcementDetails.  # noqa: E501
        :type: list[str]
        """

        self._regions = regions

    @property
    def rule_ids(self):
        """Gets the rule_ids of this EnforcementDetails.  # noqa: E501

        rules ids and list of enforcement  # noqa: E501

        :return: The rule_ids of this EnforcementDetails.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._rule_ids

    @rule_ids.setter
    def rule_ids(self, rule_ids):
        """Sets the rule_ids of this EnforcementDetails.

        rules ids and list of enforcement  # noqa: E501

        :param rule_ids: The rule_ids of this EnforcementDetails.  # noqa: E501
        :type: dict(str, str)
        """

        self._rule_ids = rule_ids

    @property
    def rule_set_ids(self):
        """Gets the rule_set_ids of this EnforcementDetails.  # noqa: E501

        rules pack ids and list of enforcement  # noqa: E501

        :return: The rule_set_ids of this EnforcementDetails.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._rule_set_ids

    @rule_set_ids.setter
    def rule_set_ids(self, rule_set_ids):
        """Sets the rule_set_ids of this EnforcementDetails.

        rules pack ids and list of enforcement  # noqa: E501

        :param rule_set_ids: The rule_set_ids of this EnforcementDetails.  # noqa: E501
        :type: dict(str, str)
        """

        self._rule_set_ids = rule_set_ids

    @property
    def schedule(self):
        """Gets the schedule of this EnforcementDetails.  # noqa: E501

        schedule  # noqa: E501

        :return: The schedule of this EnforcementDetails.  # noqa: E501
        :rtype: str
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """Sets the schedule of this EnforcementDetails.

        schedule  # noqa: E501

        :param schedule: The schedule of this EnforcementDetails.  # noqa: E501
        :type: str
        """

        self._schedule = schedule

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
        if issubclass(EnforcementDetails, dict):
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
        if not isinstance(other, EnforcementDetails):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
