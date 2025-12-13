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

class InventoryRIAPIFilter(object):
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
        'account_ids': 'list[str]',
        'cloud_account_ids': 'list[str]',
        'instance_families': 'list[str]',
        'instance_types': 'list[str]',
        'is_harness_managed': 'bool',
        'payment_options': 'list[str]',
        'plan_types': 'list[str]',
        'platforms': 'list[str]',
        'regions': 'list[str]',
        'service': 'str',
        'status': 'list[str]',
        'tenancy': 'list[str]',
        'terms': 'list[float]'
    }

    attribute_map = {
        'account_ids': 'account_ids',
        'cloud_account_ids': 'cloud_account_ids',
        'instance_families': 'instance_families',
        'instance_types': 'instance_types',
        'is_harness_managed': 'is_harness_managed',
        'payment_options': 'payment_options',
        'plan_types': 'plan_types',
        'platforms': 'platforms',
        'regions': 'regions',
        'service': 'service',
        'status': 'status',
        'tenancy': 'tenancy',
        'terms': 'terms'
    }

    def __init__(self, account_ids=None, cloud_account_ids=None, instance_families=None, instance_types=None, is_harness_managed=None, payment_options=None, plan_types=None, platforms=None, regions=None, service=None, status=None, tenancy=None, terms=None):  # noqa: E501
        """InventoryRIAPIFilter - a model defined in Swagger"""  # noqa: E501
        self._account_ids = None
        self._cloud_account_ids = None
        self._instance_families = None
        self._instance_types = None
        self._is_harness_managed = None
        self._payment_options = None
        self._plan_types = None
        self._platforms = None
        self._regions = None
        self._service = None
        self._status = None
        self._tenancy = None
        self._terms = None
        self.discriminator = None
        if account_ids is not None:
            self.account_ids = account_ids
        if cloud_account_ids is not None:
            self.cloud_account_ids = cloud_account_ids
        if instance_families is not None:
            self.instance_families = instance_families
        if instance_types is not None:
            self.instance_types = instance_types
        if is_harness_managed is not None:
            self.is_harness_managed = is_harness_managed
        if payment_options is not None:
            self.payment_options = payment_options
        if plan_types is not None:
            self.plan_types = plan_types
        if platforms is not None:
            self.platforms = platforms
        if regions is not None:
            self.regions = regions
        if service is not None:
            self.service = service
        if status is not None:
            self.status = status
        if tenancy is not None:
            self.tenancy = tenancy
        if terms is not None:
            self.terms = terms

    @property
    def account_ids(self):
        """Gets the account_ids of this InventoryRIAPIFilter.  # noqa: E501

        List of provider account IDs  # noqa: E501

        :return: The account_ids of this InventoryRIAPIFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._account_ids

    @account_ids.setter
    def account_ids(self, account_ids):
        """Sets the account_ids of this InventoryRIAPIFilter.

        List of provider account IDs  # noqa: E501

        :param account_ids: The account_ids of this InventoryRIAPIFilter.  # noqa: E501
        :type: list[str]
        """

        self._account_ids = account_ids

    @property
    def cloud_account_ids(self):
        """Gets the cloud_account_ids of this InventoryRIAPIFilter.  # noqa: E501

        List of cloud account IDs  # noqa: E501

        :return: The cloud_account_ids of this InventoryRIAPIFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._cloud_account_ids

    @cloud_account_ids.setter
    def cloud_account_ids(self, cloud_account_ids):
        """Sets the cloud_account_ids of this InventoryRIAPIFilter.

        List of cloud account IDs  # noqa: E501

        :param cloud_account_ids: The cloud_account_ids of this InventoryRIAPIFilter.  # noqa: E501
        :type: list[str]
        """

        self._cloud_account_ids = cloud_account_ids

    @property
    def instance_families(self):
        """Gets the instance_families of this InventoryRIAPIFilter.  # noqa: E501

        List of instance families  # noqa: E501

        :return: The instance_families of this InventoryRIAPIFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._instance_families

    @instance_families.setter
    def instance_families(self, instance_families):
        """Sets the instance_families of this InventoryRIAPIFilter.

        List of instance families  # noqa: E501

        :param instance_families: The instance_families of this InventoryRIAPIFilter.  # noqa: E501
        :type: list[str]
        """

        self._instance_families = instance_families

    @property
    def instance_types(self):
        """Gets the instance_types of this InventoryRIAPIFilter.  # noqa: E501

        List of instance types  # noqa: E501

        :return: The instance_types of this InventoryRIAPIFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._instance_types

    @instance_types.setter
    def instance_types(self, instance_types):
        """Sets the instance_types of this InventoryRIAPIFilter.

        List of instance types  # noqa: E501

        :param instance_types: The instance_types of this InventoryRIAPIFilter.  # noqa: E501
        :type: list[str]
        """

        self._instance_types = instance_types

    @property
    def is_harness_managed(self):
        """Gets the is_harness_managed of this InventoryRIAPIFilter.  # noqa: E501

        Filter by Harness managed status  # noqa: E501

        :return: The is_harness_managed of this InventoryRIAPIFilter.  # noqa: E501
        :rtype: bool
        """
        return self._is_harness_managed

    @is_harness_managed.setter
    def is_harness_managed(self, is_harness_managed):
        """Sets the is_harness_managed of this InventoryRIAPIFilter.

        Filter by Harness managed status  # noqa: E501

        :param is_harness_managed: The is_harness_managed of this InventoryRIAPIFilter.  # noqa: E501
        :type: bool
        """

        self._is_harness_managed = is_harness_managed

    @property
    def payment_options(self):
        """Gets the payment_options of this InventoryRIAPIFilter.  # noqa: E501

        List of payment options  # noqa: E501

        :return: The payment_options of this InventoryRIAPIFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._payment_options

    @payment_options.setter
    def payment_options(self, payment_options):
        """Sets the payment_options of this InventoryRIAPIFilter.

        List of payment options  # noqa: E501

        :param payment_options: The payment_options of this InventoryRIAPIFilter.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["No Upfront", "Partial Upfront", "All Upfront"]  # noqa: E501
        if not set(payment_options).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `payment_options` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(payment_options) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._payment_options = payment_options

    @property
    def plan_types(self):
        """Gets the plan_types of this InventoryRIAPIFilter.  # noqa: E501

        List of RI types  # noqa: E501

        :return: The plan_types of this InventoryRIAPIFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._plan_types

    @plan_types.setter
    def plan_types(self, plan_types):
        """Sets the plan_types of this InventoryRIAPIFilter.

        List of RI types  # noqa: E501

        :param plan_types: The plan_types of this InventoryRIAPIFilter.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["Standard", "Convertible"]  # noqa: E501
        if not set(plan_types).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `plan_types` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(plan_types) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._plan_types = plan_types

    @property
    def platforms(self):
        """Gets the platforms of this InventoryRIAPIFilter.  # noqa: E501

        List of platforms  # noqa: E501

        :return: The platforms of this InventoryRIAPIFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._platforms

    @platforms.setter
    def platforms(self, platforms):
        """Sets the platforms of this InventoryRIAPIFilter.

        List of platforms  # noqa: E501

        :param platforms: The platforms of this InventoryRIAPIFilter.  # noqa: E501
        :type: list[str]
        """

        self._platforms = platforms

    @property
    def regions(self):
        """Gets the regions of this InventoryRIAPIFilter.  # noqa: E501

        List of regions  # noqa: E501

        :return: The regions of this InventoryRIAPIFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._regions

    @regions.setter
    def regions(self, regions):
        """Sets the regions of this InventoryRIAPIFilter.

        List of regions  # noqa: E501

        :param regions: The regions of this InventoryRIAPIFilter.  # noqa: E501
        :type: list[str]
        """

        self._regions = regions

    @property
    def service(self):
        """Gets the service of this InventoryRIAPIFilter.  # noqa: E501

        Service to filter by  # noqa: E501

        :return: The service of this InventoryRIAPIFilter.  # noqa: E501
        :rtype: str
        """
        return self._service

    @service.setter
    def service(self, service):
        """Sets the service of this InventoryRIAPIFilter.

        Service to filter by  # noqa: E501

        :param service: The service of this InventoryRIAPIFilter.  # noqa: E501
        :type: str
        """

        self._service = service

    @property
    def status(self):
        """Gets the status of this InventoryRIAPIFilter.  # noqa: E501

        List of statuses  # noqa: E501

        :return: The status of this InventoryRIAPIFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InventoryRIAPIFilter.

        List of statuses  # noqa: E501

        :param status: The status of this InventoryRIAPIFilter.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["active", "expired", "pending", "retired"]  # noqa: E501
        if not set(status).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `status` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(status) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._status = status

    @property
    def tenancy(self):
        """Gets the tenancy of this InventoryRIAPIFilter.  # noqa: E501

        List of tenancy options  # noqa: E501

        :return: The tenancy of this InventoryRIAPIFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._tenancy

    @tenancy.setter
    def tenancy(self, tenancy):
        """Sets the tenancy of this InventoryRIAPIFilter.

        List of tenancy options  # noqa: E501

        :param tenancy: The tenancy of this InventoryRIAPIFilter.  # noqa: E501
        :type: list[str]
        """

        self._tenancy = tenancy

    @property
    def terms(self):
        """Gets the terms of this InventoryRIAPIFilter.  # noqa: E501

        List of term lengths in years  # noqa: E501

        :return: The terms of this InventoryRIAPIFilter.  # noqa: E501
        :rtype: list[float]
        """
        return self._terms

    @terms.setter
    def terms(self, terms):
        """Sets the terms of this InventoryRIAPIFilter.

        List of term lengths in years  # noqa: E501

        :param terms: The terms of this InventoryRIAPIFilter.  # noqa: E501
        :type: list[float]
        """

        self._terms = terms

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
        if issubclass(InventoryRIAPIFilter, dict):
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
        if not isinstance(other, InventoryRIAPIFilter):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
