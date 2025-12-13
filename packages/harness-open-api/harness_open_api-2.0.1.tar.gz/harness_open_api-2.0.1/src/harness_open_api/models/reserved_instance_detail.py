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

class ReservedInstanceDetail(object):
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
        'approval_info': 'ApprovalInfo',
        'availability_zone': 'str',
        'expiry_date': 'datetime',
        'hourly_cost': 'float',
        'id': 'str',
        'instance_count': 'int',
        'instance_type': 'str',
        'is_harness_managed': 'bool',
        'payment_option': 'str',
        'platform': 'str',
        'previously_was': 'PreviousStateInfo',
        'purchase_date': 'datetime',
        'purchase_term_years': 'str',
        'scope': 'str',
        'start_date': 'datetime',
        'status': 'str',
        'tenancy': 'str',
        'type': 'str',
        'upfront_fee': 'float',
        'usage_price': 'float',
        'utilization': 'float'
    }

    attribute_map = {
        'approval_info': 'approval_info',
        'availability_zone': 'availability_zone',
        'expiry_date': 'expiry_date',
        'hourly_cost': 'hourly_cost',
        'id': 'id',
        'instance_count': 'instance_count',
        'instance_type': 'instance_type',
        'is_harness_managed': 'is_harness_managed',
        'payment_option': 'payment_option',
        'platform': 'platform',
        'previously_was': 'previously_was',
        'purchase_date': 'purchase_date',
        'purchase_term_years': 'purchase_term_years',
        'scope': 'scope',
        'start_date': 'start_date',
        'status': 'status',
        'tenancy': 'tenancy',
        'type': 'type',
        'upfront_fee': 'upfront_fee',
        'usage_price': 'usage_price',
        'utilization': 'utilization'
    }

    def __init__(self, approval_info=None, availability_zone=None, expiry_date=None, hourly_cost=None, id=None, instance_count=None, instance_type=None, is_harness_managed=None, payment_option=None, platform=None, previously_was=None, purchase_date=None, purchase_term_years=None, scope=None, start_date=None, status=None, tenancy=None, type=None, upfront_fee=None, usage_price=None, utilization=None):  # noqa: E501
        """ReservedInstanceDetail - a model defined in Swagger"""  # noqa: E501
        self._approval_info = None
        self._availability_zone = None
        self._expiry_date = None
        self._hourly_cost = None
        self._id = None
        self._instance_count = None
        self._instance_type = None
        self._is_harness_managed = None
        self._payment_option = None
        self._platform = None
        self._previously_was = None
        self._purchase_date = None
        self._purchase_term_years = None
        self._scope = None
        self._start_date = None
        self._status = None
        self._tenancy = None
        self._type = None
        self._upfront_fee = None
        self._usage_price = None
        self._utilization = None
        self.discriminator = None
        if approval_info is not None:
            self.approval_info = approval_info
        if availability_zone is not None:
            self.availability_zone = availability_zone
        if expiry_date is not None:
            self.expiry_date = expiry_date
        if hourly_cost is not None:
            self.hourly_cost = hourly_cost
        if id is not None:
            self.id = id
        if instance_count is not None:
            self.instance_count = instance_count
        if instance_type is not None:
            self.instance_type = instance_type
        if is_harness_managed is not None:
            self.is_harness_managed = is_harness_managed
        if payment_option is not None:
            self.payment_option = payment_option
        if platform is not None:
            self.platform = platform
        if previously_was is not None:
            self.previously_was = previously_was
        if purchase_date is not None:
            self.purchase_date = purchase_date
        if purchase_term_years is not None:
            self.purchase_term_years = purchase_term_years
        if scope is not None:
            self.scope = scope
        if start_date is not None:
            self.start_date = start_date
        if status is not None:
            self.status = status
        if tenancy is not None:
            self.tenancy = tenancy
        if type is not None:
            self.type = type
        if upfront_fee is not None:
            self.upfront_fee = upfront_fee
        if usage_price is not None:
            self.usage_price = usage_price
        if utilization is not None:
            self.utilization = utilization

    @property
    def approval_info(self):
        """Gets the approval_info of this ReservedInstanceDetail.  # noqa: E501


        :return: The approval_info of this ReservedInstanceDetail.  # noqa: E501
        :rtype: ApprovalInfo
        """
        return self._approval_info

    @approval_info.setter
    def approval_info(self, approval_info):
        """Sets the approval_info of this ReservedInstanceDetail.


        :param approval_info: The approval_info of this ReservedInstanceDetail.  # noqa: E501
        :type: ApprovalInfo
        """

        self._approval_info = approval_info

    @property
    def availability_zone(self):
        """Gets the availability_zone of this ReservedInstanceDetail.  # noqa: E501

        Availability zone if applicable  # noqa: E501

        :return: The availability_zone of this ReservedInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._availability_zone

    @availability_zone.setter
    def availability_zone(self, availability_zone):
        """Sets the availability_zone of this ReservedInstanceDetail.

        Availability zone if applicable  # noqa: E501

        :param availability_zone: The availability_zone of this ReservedInstanceDetail.  # noqa: E501
        :type: str
        """

        self._availability_zone = availability_zone

    @property
    def expiry_date(self):
        """Gets the expiry_date of this ReservedInstanceDetail.  # noqa: E501

        Expiration date of the reservation  # noqa: E501

        :return: The expiry_date of this ReservedInstanceDetail.  # noqa: E501
        :rtype: datetime
        """
        return self._expiry_date

    @expiry_date.setter
    def expiry_date(self, expiry_date):
        """Sets the expiry_date of this ReservedInstanceDetail.

        Expiration date of the reservation  # noqa: E501

        :param expiry_date: The expiry_date of this ReservedInstanceDetail.  # noqa: E501
        :type: datetime
        """

        self._expiry_date = expiry_date

    @property
    def hourly_cost(self):
        """Gets the hourly_cost of this ReservedInstanceDetail.  # noqa: E501

        Total hourly cost  # noqa: E501

        :return: The hourly_cost of this ReservedInstanceDetail.  # noqa: E501
        :rtype: float
        """
        return self._hourly_cost

    @hourly_cost.setter
    def hourly_cost(self, hourly_cost):
        """Sets the hourly_cost of this ReservedInstanceDetail.

        Total hourly cost  # noqa: E501

        :param hourly_cost: The hourly_cost of this ReservedInstanceDetail.  # noqa: E501
        :type: float
        """

        self._hourly_cost = hourly_cost

    @property
    def id(self):
        """Gets the id of this ReservedInstanceDetail.  # noqa: E501

        Unique identifier for the Reserved Instance  # noqa: E501

        :return: The id of this ReservedInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ReservedInstanceDetail.

        Unique identifier for the Reserved Instance  # noqa: E501

        :param id: The id of this ReservedInstanceDetail.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def instance_count(self):
        """Gets the instance_count of this ReservedInstanceDetail.  # noqa: E501

        Number of instances in this reservation  # noqa: E501

        :return: The instance_count of this ReservedInstanceDetail.  # noqa: E501
        :rtype: int
        """
        return self._instance_count

    @instance_count.setter
    def instance_count(self, instance_count):
        """Sets the instance_count of this ReservedInstanceDetail.

        Number of instances in this reservation  # noqa: E501

        :param instance_count: The instance_count of this ReservedInstanceDetail.  # noqa: E501
        :type: int
        """

        self._instance_count = instance_count

    @property
    def instance_type(self):
        """Gets the instance_type of this ReservedInstanceDetail.  # noqa: E501

        Type of EC2 instance  # noqa: E501

        :return: The instance_type of this ReservedInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._instance_type

    @instance_type.setter
    def instance_type(self, instance_type):
        """Sets the instance_type of this ReservedInstanceDetail.

        Type of EC2 instance  # noqa: E501

        :param instance_type: The instance_type of this ReservedInstanceDetail.  # noqa: E501
        :type: str
        """

        self._instance_type = instance_type

    @property
    def is_harness_managed(self):
        """Gets the is_harness_managed of this ReservedInstanceDetail.  # noqa: E501

        Indicates if the reservation is managed by Harness  # noqa: E501

        :return: The is_harness_managed of this ReservedInstanceDetail.  # noqa: E501
        :rtype: bool
        """
        return self._is_harness_managed

    @is_harness_managed.setter
    def is_harness_managed(self, is_harness_managed):
        """Sets the is_harness_managed of this ReservedInstanceDetail.

        Indicates if the reservation is managed by Harness  # noqa: E501

        :param is_harness_managed: The is_harness_managed of this ReservedInstanceDetail.  # noqa: E501
        :type: bool
        """

        self._is_harness_managed = is_harness_managed

    @property
    def payment_option(self):
        """Gets the payment_option of this ReservedInstanceDetail.  # noqa: E501

        Payment option selected  # noqa: E501

        :return: The payment_option of this ReservedInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._payment_option

    @payment_option.setter
    def payment_option(self, payment_option):
        """Sets the payment_option of this ReservedInstanceDetail.

        Payment option selected  # noqa: E501

        :param payment_option: The payment_option of this ReservedInstanceDetail.  # noqa: E501
        :type: str
        """

        self._payment_option = payment_option

    @property
    def platform(self):
        """Gets the platform of this ReservedInstanceDetail.  # noqa: E501

        Operating system platform  # noqa: E501

        :return: The platform of this ReservedInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """Sets the platform of this ReservedInstanceDetail.

        Operating system platform  # noqa: E501

        :param platform: The platform of this ReservedInstanceDetail.  # noqa: E501
        :type: str
        """

        self._platform = platform

    @property
    def previously_was(self):
        """Gets the previously_was of this ReservedInstanceDetail.  # noqa: E501


        :return: The previously_was of this ReservedInstanceDetail.  # noqa: E501
        :rtype: PreviousStateInfo
        """
        return self._previously_was

    @previously_was.setter
    def previously_was(self, previously_was):
        """Sets the previously_was of this ReservedInstanceDetail.


        :param previously_was: The previously_was of this ReservedInstanceDetail.  # noqa: E501
        :type: PreviousStateInfo
        """

        self._previously_was = previously_was

    @property
    def purchase_date(self):
        """Gets the purchase_date of this ReservedInstanceDetail.  # noqa: E501

        Date when the reservation was purchased  # noqa: E501

        :return: The purchase_date of this ReservedInstanceDetail.  # noqa: E501
        :rtype: datetime
        """
        return self._purchase_date

    @purchase_date.setter
    def purchase_date(self, purchase_date):
        """Sets the purchase_date of this ReservedInstanceDetail.

        Date when the reservation was purchased  # noqa: E501

        :param purchase_date: The purchase_date of this ReservedInstanceDetail.  # noqa: E501
        :type: datetime
        """

        self._purchase_date = purchase_date

    @property
    def purchase_term_years(self):
        """Gets the purchase_term_years of this ReservedInstanceDetail.  # noqa: E501

        Term length of the reservation  # noqa: E501

        :return: The purchase_term_years of this ReservedInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._purchase_term_years

    @purchase_term_years.setter
    def purchase_term_years(self, purchase_term_years):
        """Sets the purchase_term_years of this ReservedInstanceDetail.

        Term length of the reservation  # noqa: E501

        :param purchase_term_years: The purchase_term_years of this ReservedInstanceDetail.  # noqa: E501
        :type: str
        """

        self._purchase_term_years = purchase_term_years

    @property
    def scope(self):
        """Gets the scope of this ReservedInstanceDetail.  # noqa: E501

        Scope of the reservation (e.g., region)  # noqa: E501

        :return: The scope of this ReservedInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this ReservedInstanceDetail.

        Scope of the reservation (e.g., region)  # noqa: E501

        :param scope: The scope of this ReservedInstanceDetail.  # noqa: E501
        :type: str
        """

        self._scope = scope

    @property
    def start_date(self):
        """Gets the start_date of this ReservedInstanceDetail.  # noqa: E501

        Start date of the reservation  # noqa: E501

        :return: The start_date of this ReservedInstanceDetail.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this ReservedInstanceDetail.

        Start date of the reservation  # noqa: E501

        :param start_date: The start_date of this ReservedInstanceDetail.  # noqa: E501
        :type: datetime
        """

        self._start_date = start_date

    @property
    def status(self):
        """Gets the status of this ReservedInstanceDetail.  # noqa: E501

        Current status of the reservation  # noqa: E501

        :return: The status of this ReservedInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ReservedInstanceDetail.

        Current status of the reservation  # noqa: E501

        :param status: The status of this ReservedInstanceDetail.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def tenancy(self):
        """Gets the tenancy of this ReservedInstanceDetail.  # noqa: E501

        Instance tenancy (e.g., Shared, Dedicated)  # noqa: E501

        :return: The tenancy of this ReservedInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._tenancy

    @tenancy.setter
    def tenancy(self, tenancy):
        """Sets the tenancy of this ReservedInstanceDetail.

        Instance tenancy (e.g., Shared, Dedicated)  # noqa: E501

        :param tenancy: The tenancy of this ReservedInstanceDetail.  # noqa: E501
        :type: str
        """

        self._tenancy = tenancy

    @property
    def type(self):
        """Gets the type of this ReservedInstanceDetail.  # noqa: E501

        Type of Reserved Instance (e.g., Convertible)  # noqa: E501

        :return: The type of this ReservedInstanceDetail.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ReservedInstanceDetail.

        Type of Reserved Instance (e.g., Convertible)  # noqa: E501

        :param type: The type of this ReservedInstanceDetail.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def upfront_fee(self):
        """Gets the upfront_fee of this ReservedInstanceDetail.  # noqa: E501

        Upfront payment amount  # noqa: E501

        :return: The upfront_fee of this ReservedInstanceDetail.  # noqa: E501
        :rtype: float
        """
        return self._upfront_fee

    @upfront_fee.setter
    def upfront_fee(self, upfront_fee):
        """Sets the upfront_fee of this ReservedInstanceDetail.

        Upfront payment amount  # noqa: E501

        :param upfront_fee: The upfront_fee of this ReservedInstanceDetail.  # noqa: E501
        :type: float
        """

        self._upfront_fee = upfront_fee

    @property
    def usage_price(self):
        """Gets the usage_price of this ReservedInstanceDetail.  # noqa: E501

        Usage price per hour  # noqa: E501

        :return: The usage_price of this ReservedInstanceDetail.  # noqa: E501
        :rtype: float
        """
        return self._usage_price

    @usage_price.setter
    def usage_price(self, usage_price):
        """Sets the usage_price of this ReservedInstanceDetail.

        Usage price per hour  # noqa: E501

        :param usage_price: The usage_price of this ReservedInstanceDetail.  # noqa: E501
        :type: float
        """

        self._usage_price = usage_price

    @property
    def utilization(self):
        """Gets the utilization of this ReservedInstanceDetail.  # noqa: E501

        Current utilization percentage  # noqa: E501

        :return: The utilization of this ReservedInstanceDetail.  # noqa: E501
        :rtype: float
        """
        return self._utilization

    @utilization.setter
    def utilization(self, utilization):
        """Sets the utilization of this ReservedInstanceDetail.

        Current utilization percentage  # noqa: E501

        :param utilization: The utilization of this ReservedInstanceDetail.  # noqa: E501
        :type: float
        """

        self._utilization = utilization

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
        if issubclass(ReservedInstanceDetail, dict):
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
        if not isinstance(other, ReservedInstanceDetail):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
