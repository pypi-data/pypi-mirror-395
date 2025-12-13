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

class FullIssueCounts(object):
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
        'app_critical': 'int',
        'app_high': 'int',
        'app_info': 'int',
        'app_low': 'int',
        'app_medium': 'int',
        'base_critical': 'int',
        'base_high': 'int',
        'base_image_approved': 'bool',
        'base_image_detected': 'bool',
        'base_info': 'int',
        'base_low': 'int',
        'base_medium': 'int',
        'code_coverage': 'float',
        'critical': 'int',
        'external_policy_failures': 'int',
        'high': 'int',
        'ignored': 'int',
        'ignored_critical': 'int',
        'ignored_high': 'int',
        'ignored_info': 'int',
        'ignored_low': 'int',
        'ignored_medium': 'int',
        'ignored_unassigned': 'int',
        'info': 'int',
        'low': 'int',
        'medium': 'int',
        'new_app_critical': 'int',
        'new_app_high': 'int',
        'new_app_info': 'int',
        'new_app_low': 'int',
        'new_app_medium': 'int',
        'new_base_critical': 'int',
        'new_base_high': 'int',
        'new_base_info': 'int',
        'new_base_low': 'int',
        'new_base_medium': 'int',
        'new_critical': 'int',
        'new_high': 'int',
        'new_ignored_critical': 'int',
        'new_ignored_high': 'int',
        'new_ignored_info': 'int',
        'new_ignored_low': 'int',
        'new_ignored_medium': 'int',
        'new_ignored_occurrences_critical': 'int',
        'new_ignored_occurrences_high': 'int',
        'new_ignored_occurrences_info': 'int',
        'new_ignored_occurrences_low': 'int',
        'new_ignored_occurrences_medium': 'int',
        'new_ignored_occurrences_unassigned': 'int',
        'new_ignored_unassigned': 'int',
        'new_info': 'int',
        'new_low': 'int',
        'new_medium': 'int',
        'new_occurrences_critical': 'int',
        'new_occurrences_high': 'int',
        'new_occurrences_info': 'int',
        'new_occurrences_low': 'int',
        'new_occurrences_medium': 'int',
        'new_occurrences_unassigned': 'int',
        'new_total': 'int',
        'new_total_base': 'int',
        'new_unassigned': 'int',
        'total': 'int',
        'total_base': 'int',
        'unassigned': 'int'
    }

    attribute_map = {
        'app_critical': 'appCritical',
        'app_high': 'appHigh',
        'app_info': 'appInfo',
        'app_low': 'appLow',
        'app_medium': 'appMedium',
        'base_critical': 'baseCritical',
        'base_high': 'baseHigh',
        'base_image_approved': 'baseImageApproved',
        'base_image_detected': 'baseImageDetected',
        'base_info': 'baseInfo',
        'base_low': 'baseLow',
        'base_medium': 'baseMedium',
        'code_coverage': 'codeCoverage',
        'critical': 'critical',
        'external_policy_failures': 'externalPolicyFailures',
        'high': 'high',
        'ignored': 'ignored',
        'ignored_critical': 'ignoredCritical',
        'ignored_high': 'ignoredHigh',
        'ignored_info': 'ignoredInfo',
        'ignored_low': 'ignoredLow',
        'ignored_medium': 'ignoredMedium',
        'ignored_unassigned': 'ignoredUnassigned',
        'info': 'info',
        'low': 'low',
        'medium': 'medium',
        'new_app_critical': 'newAppCritical',
        'new_app_high': 'newAppHigh',
        'new_app_info': 'newAppInfo',
        'new_app_low': 'newAppLow',
        'new_app_medium': 'newAppMedium',
        'new_base_critical': 'newBaseCritical',
        'new_base_high': 'newBaseHigh',
        'new_base_info': 'newBaseInfo',
        'new_base_low': 'newBaseLow',
        'new_base_medium': 'newBaseMedium',
        'new_critical': 'newCritical',
        'new_high': 'newHigh',
        'new_ignored_critical': 'newIgnoredCritical',
        'new_ignored_high': 'newIgnoredHigh',
        'new_ignored_info': 'newIgnoredInfo',
        'new_ignored_low': 'newIgnoredLow',
        'new_ignored_medium': 'newIgnoredMedium',
        'new_ignored_occurrences_critical': 'newIgnoredOccurrencesCritical',
        'new_ignored_occurrences_high': 'newIgnoredOccurrencesHigh',
        'new_ignored_occurrences_info': 'newIgnoredOccurrencesInfo',
        'new_ignored_occurrences_low': 'newIgnoredOccurrencesLow',
        'new_ignored_occurrences_medium': 'newIgnoredOccurrencesMedium',
        'new_ignored_occurrences_unassigned': 'newIgnoredOccurrencesUnassigned',
        'new_ignored_unassigned': 'newIgnoredUnassigned',
        'new_info': 'newInfo',
        'new_low': 'newLow',
        'new_medium': 'newMedium',
        'new_occurrences_critical': 'newOccurrencesCritical',
        'new_occurrences_high': 'newOccurrencesHigh',
        'new_occurrences_info': 'newOccurrencesInfo',
        'new_occurrences_low': 'newOccurrencesLow',
        'new_occurrences_medium': 'newOccurrencesMedium',
        'new_occurrences_unassigned': 'newOccurrencesUnassigned',
        'new_total': 'newTotal',
        'new_total_base': 'newTotalBase',
        'new_unassigned': 'newUnassigned',
        'total': 'total',
        'total_base': 'totalBase',
        'unassigned': 'unassigned'
    }

    def __init__(self, app_critical=None, app_high=None, app_info=None, app_low=None, app_medium=None, base_critical=None, base_high=None, base_image_approved=None, base_image_detected=None, base_info=None, base_low=None, base_medium=None, code_coverage=None, critical=None, external_policy_failures=None, high=None, ignored=None, ignored_critical=None, ignored_high=None, ignored_info=None, ignored_low=None, ignored_medium=None, ignored_unassigned=None, info=None, low=None, medium=None, new_app_critical=None, new_app_high=None, new_app_info=None, new_app_low=None, new_app_medium=None, new_base_critical=None, new_base_high=None, new_base_info=None, new_base_low=None, new_base_medium=None, new_critical=None, new_high=None, new_ignored_critical=None, new_ignored_high=None, new_ignored_info=None, new_ignored_low=None, new_ignored_medium=None, new_ignored_occurrences_critical=None, new_ignored_occurrences_high=None, new_ignored_occurrences_info=None, new_ignored_occurrences_low=None, new_ignored_occurrences_medium=None, new_ignored_occurrences_unassigned=None, new_ignored_unassigned=None, new_info=None, new_low=None, new_medium=None, new_occurrences_critical=None, new_occurrences_high=None, new_occurrences_info=None, new_occurrences_low=None, new_occurrences_medium=None, new_occurrences_unassigned=None, new_total=None, new_total_base=None, new_unassigned=None, total=None, total_base=None, unassigned=None):  # noqa: E501
        """FullIssueCounts - a model defined in Swagger"""  # noqa: E501
        self._app_critical = None
        self._app_high = None
        self._app_info = None
        self._app_low = None
        self._app_medium = None
        self._base_critical = None
        self._base_high = None
        self._base_image_approved = None
        self._base_image_detected = None
        self._base_info = None
        self._base_low = None
        self._base_medium = None
        self._code_coverage = None
        self._critical = None
        self._external_policy_failures = None
        self._high = None
        self._ignored = None
        self._ignored_critical = None
        self._ignored_high = None
        self._ignored_info = None
        self._ignored_low = None
        self._ignored_medium = None
        self._ignored_unassigned = None
        self._info = None
        self._low = None
        self._medium = None
        self._new_app_critical = None
        self._new_app_high = None
        self._new_app_info = None
        self._new_app_low = None
        self._new_app_medium = None
        self._new_base_critical = None
        self._new_base_high = None
        self._new_base_info = None
        self._new_base_low = None
        self._new_base_medium = None
        self._new_critical = None
        self._new_high = None
        self._new_ignored_critical = None
        self._new_ignored_high = None
        self._new_ignored_info = None
        self._new_ignored_low = None
        self._new_ignored_medium = None
        self._new_ignored_occurrences_critical = None
        self._new_ignored_occurrences_high = None
        self._new_ignored_occurrences_info = None
        self._new_ignored_occurrences_low = None
        self._new_ignored_occurrences_medium = None
        self._new_ignored_occurrences_unassigned = None
        self._new_ignored_unassigned = None
        self._new_info = None
        self._new_low = None
        self._new_medium = None
        self._new_occurrences_critical = None
        self._new_occurrences_high = None
        self._new_occurrences_info = None
        self._new_occurrences_low = None
        self._new_occurrences_medium = None
        self._new_occurrences_unassigned = None
        self._new_total = None
        self._new_total_base = None
        self._new_unassigned = None
        self._total = None
        self._total_base = None
        self._unassigned = None
        self.discriminator = None
        if app_critical is not None:
            self.app_critical = app_critical
        if app_high is not None:
            self.app_high = app_high
        if app_info is not None:
            self.app_info = app_info
        if app_low is not None:
            self.app_low = app_low
        if app_medium is not None:
            self.app_medium = app_medium
        if base_critical is not None:
            self.base_critical = base_critical
        if base_high is not None:
            self.base_high = base_high
        if base_image_approved is not None:
            self.base_image_approved = base_image_approved
        if base_image_detected is not None:
            self.base_image_detected = base_image_detected
        if base_info is not None:
            self.base_info = base_info
        if base_low is not None:
            self.base_low = base_low
        if base_medium is not None:
            self.base_medium = base_medium
        if code_coverage is not None:
            self.code_coverage = code_coverage
        self.critical = critical
        self.external_policy_failures = external_policy_failures
        self.high = high
        self.ignored = ignored
        self.ignored_critical = ignored_critical
        self.ignored_high = ignored_high
        self.ignored_info = ignored_info
        self.ignored_low = ignored_low
        self.ignored_medium = ignored_medium
        self.ignored_unassigned = ignored_unassigned
        self.info = info
        self.low = low
        self.medium = medium
        if new_app_critical is not None:
            self.new_app_critical = new_app_critical
        if new_app_high is not None:
            self.new_app_high = new_app_high
        if new_app_info is not None:
            self.new_app_info = new_app_info
        if new_app_low is not None:
            self.new_app_low = new_app_low
        if new_app_medium is not None:
            self.new_app_medium = new_app_medium
        if new_base_critical is not None:
            self.new_base_critical = new_base_critical
        if new_base_high is not None:
            self.new_base_high = new_base_high
        if new_base_info is not None:
            self.new_base_info = new_base_info
        if new_base_low is not None:
            self.new_base_low = new_base_low
        if new_base_medium is not None:
            self.new_base_medium = new_base_medium
        self.new_critical = new_critical
        self.new_high = new_high
        self.new_ignored_critical = new_ignored_critical
        self.new_ignored_high = new_ignored_high
        self.new_ignored_info = new_ignored_info
        self.new_ignored_low = new_ignored_low
        self.new_ignored_medium = new_ignored_medium
        self.new_ignored_occurrences_critical = new_ignored_occurrences_critical
        self.new_ignored_occurrences_high = new_ignored_occurrences_high
        self.new_ignored_occurrences_info = new_ignored_occurrences_info
        self.new_ignored_occurrences_low = new_ignored_occurrences_low
        self.new_ignored_occurrences_medium = new_ignored_occurrences_medium
        self.new_ignored_occurrences_unassigned = new_ignored_occurrences_unassigned
        self.new_ignored_unassigned = new_ignored_unassigned
        self.new_info = new_info
        self.new_low = new_low
        self.new_medium = new_medium
        self.new_occurrences_critical = new_occurrences_critical
        self.new_occurrences_high = new_occurrences_high
        self.new_occurrences_info = new_occurrences_info
        self.new_occurrences_low = new_occurrences_low
        self.new_occurrences_medium = new_occurrences_medium
        self.new_occurrences_unassigned = new_occurrences_unassigned
        self.new_total = new_total
        if new_total_base is not None:
            self.new_total_base = new_total_base
        self.new_unassigned = new_unassigned
        self.total = total
        if total_base is not None:
            self.total_base = total_base
        self.unassigned = unassigned

    @property
    def app_critical(self):
        """Gets the app_critical of this FullIssueCounts.  # noqa: E501

        The number of Critical-severity Issues in the App Image  # noqa: E501

        :return: The app_critical of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._app_critical

    @app_critical.setter
    def app_critical(self, app_critical):
        """Sets the app_critical of this FullIssueCounts.

        The number of Critical-severity Issues in the App Image  # noqa: E501

        :param app_critical: The app_critical of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._app_critical = app_critical

    @property
    def app_high(self):
        """Gets the app_high of this FullIssueCounts.  # noqa: E501

        The number of High-severity Issues in the App Image  # noqa: E501

        :return: The app_high of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._app_high

    @app_high.setter
    def app_high(self, app_high):
        """Sets the app_high of this FullIssueCounts.

        The number of High-severity Issues in the App Image  # noqa: E501

        :param app_high: The app_high of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._app_high = app_high

    @property
    def app_info(self):
        """Gets the app_info of this FullIssueCounts.  # noqa: E501

        The number of Informational Issues in the App Image  # noqa: E501

        :return: The app_info of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._app_info

    @app_info.setter
    def app_info(self, app_info):
        """Sets the app_info of this FullIssueCounts.

        The number of Informational Issues in the App Image  # noqa: E501

        :param app_info: The app_info of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._app_info = app_info

    @property
    def app_low(self):
        """Gets the app_low of this FullIssueCounts.  # noqa: E501

        The number of Low-severity Issues in the App Image  # noqa: E501

        :return: The app_low of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._app_low

    @app_low.setter
    def app_low(self, app_low):
        """Sets the app_low of this FullIssueCounts.

        The number of Low-severity Issues in the App Image  # noqa: E501

        :param app_low: The app_low of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._app_low = app_low

    @property
    def app_medium(self):
        """Gets the app_medium of this FullIssueCounts.  # noqa: E501

        The number of Medium-severity Issues in the App Image  # noqa: E501

        :return: The app_medium of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._app_medium

    @app_medium.setter
    def app_medium(self, app_medium):
        """Sets the app_medium of this FullIssueCounts.

        The number of Medium-severity Issues in the App Image  # noqa: E501

        :param app_medium: The app_medium of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._app_medium = app_medium

    @property
    def base_critical(self):
        """Gets the base_critical of this FullIssueCounts.  # noqa: E501

        The number of Critical-severity Issues in the Base Image  # noqa: E501

        :return: The base_critical of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._base_critical

    @base_critical.setter
    def base_critical(self, base_critical):
        """Sets the base_critical of this FullIssueCounts.

        The number of Critical-severity Issues in the Base Image  # noqa: E501

        :param base_critical: The base_critical of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._base_critical = base_critical

    @property
    def base_high(self):
        """Gets the base_high of this FullIssueCounts.  # noqa: E501

        The number of High-severity Issues in the Base Image  # noqa: E501

        :return: The base_high of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._base_high

    @base_high.setter
    def base_high(self, base_high):
        """Sets the base_high of this FullIssueCounts.

        The number of High-severity Issues in the Base Image  # noqa: E501

        :param base_high: The base_high of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._base_high = base_high

    @property
    def base_image_approved(self):
        """Gets the base_image_approved of this FullIssueCounts.  # noqa: E501

        The approval status of the Base Image for the Scan  # noqa: E501

        :return: The base_image_approved of this FullIssueCounts.  # noqa: E501
        :rtype: bool
        """
        return self._base_image_approved

    @base_image_approved.setter
    def base_image_approved(self, base_image_approved):
        """Sets the base_image_approved of this FullIssueCounts.

        The approval status of the Base Image for the Scan  # noqa: E501

        :param base_image_approved: The base_image_approved of this FullIssueCounts.  # noqa: E501
        :type: bool
        """

        self._base_image_approved = base_image_approved

    @property
    def base_image_detected(self):
        """Gets the base_image_detected of this FullIssueCounts.  # noqa: E501

        The status of the Base Image for the Scan  # noqa: E501

        :return: The base_image_detected of this FullIssueCounts.  # noqa: E501
        :rtype: bool
        """
        return self._base_image_detected

    @base_image_detected.setter
    def base_image_detected(self, base_image_detected):
        """Sets the base_image_detected of this FullIssueCounts.

        The status of the Base Image for the Scan  # noqa: E501

        :param base_image_detected: The base_image_detected of this FullIssueCounts.  # noqa: E501
        :type: bool
        """

        self._base_image_detected = base_image_detected

    @property
    def base_info(self):
        """Gets the base_info of this FullIssueCounts.  # noqa: E501

        The number of Informational Issues in the Base Image  # noqa: E501

        :return: The base_info of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._base_info

    @base_info.setter
    def base_info(self, base_info):
        """Sets the base_info of this FullIssueCounts.

        The number of Informational Issues in the Base Image  # noqa: E501

        :param base_info: The base_info of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._base_info = base_info

    @property
    def base_low(self):
        """Gets the base_low of this FullIssueCounts.  # noqa: E501

        The number of Low-severity Issues in the Base Image  # noqa: E501

        :return: The base_low of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._base_low

    @base_low.setter
    def base_low(self, base_low):
        """Sets the base_low of this FullIssueCounts.

        The number of Low-severity Issues in the Base Image  # noqa: E501

        :param base_low: The base_low of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._base_low = base_low

    @property
    def base_medium(self):
        """Gets the base_medium of this FullIssueCounts.  # noqa: E501

        The number of Medium-severity Issues in the Base Image  # noqa: E501

        :return: The base_medium of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._base_medium

    @base_medium.setter
    def base_medium(self, base_medium):
        """Sets the base_medium of this FullIssueCounts.

        The number of Medium-severity Issues in the Base Image  # noqa: E501

        :param base_medium: The base_medium of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._base_medium = base_medium

    @property
    def code_coverage(self):
        """Gets the code_coverage of this FullIssueCounts.  # noqa: E501

        The Code Coverage value for the Scan  # noqa: E501

        :return: The code_coverage of this FullIssueCounts.  # noqa: E501
        :rtype: float
        """
        return self._code_coverage

    @code_coverage.setter
    def code_coverage(self, code_coverage):
        """Sets the code_coverage of this FullIssueCounts.

        The Code Coverage value for the Scan  # noqa: E501

        :param code_coverage: The code_coverage of this FullIssueCounts.  # noqa: E501
        :type: float
        """

        self._code_coverage = code_coverage

    @property
    def critical(self):
        """Gets the critical of this FullIssueCounts.  # noqa: E501

        The number of Critical-severity Issues  # noqa: E501

        :return: The critical of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._critical

    @critical.setter
    def critical(self, critical):
        """Sets the critical of this FullIssueCounts.

        The number of Critical-severity Issues  # noqa: E501

        :param critical: The critical of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if critical is None:
            raise ValueError("Invalid value for `critical`, must not be `None`")  # noqa: E501

        self._critical = critical

    @property
    def external_policy_failures(self):
        """Gets the external_policy_failures of this FullIssueCounts.  # noqa: E501

        The number of EXTERNAL_POLICY Issues  # noqa: E501

        :return: The external_policy_failures of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._external_policy_failures

    @external_policy_failures.setter
    def external_policy_failures(self, external_policy_failures):
        """Sets the external_policy_failures of this FullIssueCounts.

        The number of EXTERNAL_POLICY Issues  # noqa: E501

        :param external_policy_failures: The external_policy_failures of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if external_policy_failures is None:
            raise ValueError("Invalid value for `external_policy_failures`, must not be `None`")  # noqa: E501

        self._external_policy_failures = external_policy_failures

    @property
    def high(self):
        """Gets the high of this FullIssueCounts.  # noqa: E501

        The number of High-severity Issues  # noqa: E501

        :return: The high of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._high

    @high.setter
    def high(self, high):
        """Sets the high of this FullIssueCounts.

        The number of High-severity Issues  # noqa: E501

        :param high: The high of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if high is None:
            raise ValueError("Invalid value for `high`, must not be `None`")  # noqa: E501

        self._high = high

    @property
    def ignored(self):
        """Gets the ignored of this FullIssueCounts.  # noqa: E501

        The number of Issues ignored due to Exemptions, and therefore not included in other counts  # noqa: E501

        :return: The ignored of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._ignored

    @ignored.setter
    def ignored(self, ignored):
        """Sets the ignored of this FullIssueCounts.

        The number of Issues ignored due to Exemptions, and therefore not included in other counts  # noqa: E501

        :param ignored: The ignored of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if ignored is None:
            raise ValueError("Invalid value for `ignored`, must not be `None`")  # noqa: E501

        self._ignored = ignored

    @property
    def ignored_critical(self):
        """Gets the ignored_critical of this FullIssueCounts.  # noqa: E501

        The number of ignored Critical-severity Issues  # noqa: E501

        :return: The ignored_critical of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._ignored_critical

    @ignored_critical.setter
    def ignored_critical(self, ignored_critical):
        """Sets the ignored_critical of this FullIssueCounts.

        The number of ignored Critical-severity Issues  # noqa: E501

        :param ignored_critical: The ignored_critical of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if ignored_critical is None:
            raise ValueError("Invalid value for `ignored_critical`, must not be `None`")  # noqa: E501

        self._ignored_critical = ignored_critical

    @property
    def ignored_high(self):
        """Gets the ignored_high of this FullIssueCounts.  # noqa: E501

        The number of ignored High-severity Issues  # noqa: E501

        :return: The ignored_high of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._ignored_high

    @ignored_high.setter
    def ignored_high(self, ignored_high):
        """Sets the ignored_high of this FullIssueCounts.

        The number of ignored High-severity Issues  # noqa: E501

        :param ignored_high: The ignored_high of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if ignored_high is None:
            raise ValueError("Invalid value for `ignored_high`, must not be `None`")  # noqa: E501

        self._ignored_high = ignored_high

    @property
    def ignored_info(self):
        """Gets the ignored_info of this FullIssueCounts.  # noqa: E501

        The number of ignored Informational Issues  # noqa: E501

        :return: The ignored_info of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._ignored_info

    @ignored_info.setter
    def ignored_info(self, ignored_info):
        """Sets the ignored_info of this FullIssueCounts.

        The number of ignored Informational Issues  # noqa: E501

        :param ignored_info: The ignored_info of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if ignored_info is None:
            raise ValueError("Invalid value for `ignored_info`, must not be `None`")  # noqa: E501

        self._ignored_info = ignored_info

    @property
    def ignored_low(self):
        """Gets the ignored_low of this FullIssueCounts.  # noqa: E501

        The number of ignored Low-severity Issues  # noqa: E501

        :return: The ignored_low of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._ignored_low

    @ignored_low.setter
    def ignored_low(self, ignored_low):
        """Sets the ignored_low of this FullIssueCounts.

        The number of ignored Low-severity Issues  # noqa: E501

        :param ignored_low: The ignored_low of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if ignored_low is None:
            raise ValueError("Invalid value for `ignored_low`, must not be `None`")  # noqa: E501

        self._ignored_low = ignored_low

    @property
    def ignored_medium(self):
        """Gets the ignored_medium of this FullIssueCounts.  # noqa: E501

        The number of ignored Medium-severity Issues  # noqa: E501

        :return: The ignored_medium of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._ignored_medium

    @ignored_medium.setter
    def ignored_medium(self, ignored_medium):
        """Sets the ignored_medium of this FullIssueCounts.

        The number of ignored Medium-severity Issues  # noqa: E501

        :param ignored_medium: The ignored_medium of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if ignored_medium is None:
            raise ValueError("Invalid value for `ignored_medium`, must not be `None`")  # noqa: E501

        self._ignored_medium = ignored_medium

    @property
    def ignored_unassigned(self):
        """Gets the ignored_unassigned of this FullIssueCounts.  # noqa: E501

        The number of Issues with no associated severity code  # noqa: E501

        :return: The ignored_unassigned of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._ignored_unassigned

    @ignored_unassigned.setter
    def ignored_unassigned(self, ignored_unassigned):
        """Sets the ignored_unassigned of this FullIssueCounts.

        The number of Issues with no associated severity code  # noqa: E501

        :param ignored_unassigned: The ignored_unassigned of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if ignored_unassigned is None:
            raise ValueError("Invalid value for `ignored_unassigned`, must not be `None`")  # noqa: E501

        self._ignored_unassigned = ignored_unassigned

    @property
    def info(self):
        """Gets the info of this FullIssueCounts.  # noqa: E501

        The number of Informational Issues  # noqa: E501

        :return: The info of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this FullIssueCounts.

        The number of Informational Issues  # noqa: E501

        :param info: The info of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if info is None:
            raise ValueError("Invalid value for `info`, must not be `None`")  # noqa: E501

        self._info = info

    @property
    def low(self):
        """Gets the low of this FullIssueCounts.  # noqa: E501

        The number of Low-severity Issues  # noqa: E501

        :return: The low of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._low

    @low.setter
    def low(self, low):
        """Sets the low of this FullIssueCounts.

        The number of Low-severity Issues  # noqa: E501

        :param low: The low of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if low is None:
            raise ValueError("Invalid value for `low`, must not be `None`")  # noqa: E501

        self._low = low

    @property
    def medium(self):
        """Gets the medium of this FullIssueCounts.  # noqa: E501

        The number of Medium-severity Issues  # noqa: E501

        :return: The medium of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._medium

    @medium.setter
    def medium(self, medium):
        """Sets the medium of this FullIssueCounts.

        The number of Medium-severity Issues  # noqa: E501

        :param medium: The medium of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if medium is None:
            raise ValueError("Invalid value for `medium`, must not be `None`")  # noqa: E501

        self._medium = medium

    @property
    def new_app_critical(self):
        """Gets the new_app_critical of this FullIssueCounts.  # noqa: E501

        The number of new Critical-severity Issues in the App Image  # noqa: E501

        :return: The new_app_critical of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_app_critical

    @new_app_critical.setter
    def new_app_critical(self, new_app_critical):
        """Sets the new_app_critical of this FullIssueCounts.

        The number of new Critical-severity Issues in the App Image  # noqa: E501

        :param new_app_critical: The new_app_critical of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._new_app_critical = new_app_critical

    @property
    def new_app_high(self):
        """Gets the new_app_high of this FullIssueCounts.  # noqa: E501

        The number of new High-severity Issues in the App Image  # noqa: E501

        :return: The new_app_high of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_app_high

    @new_app_high.setter
    def new_app_high(self, new_app_high):
        """Sets the new_app_high of this FullIssueCounts.

        The number of new High-severity Issues in the App Image  # noqa: E501

        :param new_app_high: The new_app_high of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._new_app_high = new_app_high

    @property
    def new_app_info(self):
        """Gets the new_app_info of this FullIssueCounts.  # noqa: E501

        The number of new Informational Issues in the App Image  # noqa: E501

        :return: The new_app_info of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_app_info

    @new_app_info.setter
    def new_app_info(self, new_app_info):
        """Sets the new_app_info of this FullIssueCounts.

        The number of new Informational Issues in the App Image  # noqa: E501

        :param new_app_info: The new_app_info of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._new_app_info = new_app_info

    @property
    def new_app_low(self):
        """Gets the new_app_low of this FullIssueCounts.  # noqa: E501

        The number of new Low-severity Issues in the App Image  # noqa: E501

        :return: The new_app_low of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_app_low

    @new_app_low.setter
    def new_app_low(self, new_app_low):
        """Sets the new_app_low of this FullIssueCounts.

        The number of new Low-severity Issues in the App Image  # noqa: E501

        :param new_app_low: The new_app_low of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._new_app_low = new_app_low

    @property
    def new_app_medium(self):
        """Gets the new_app_medium of this FullIssueCounts.  # noqa: E501

        The number of new Medium-severity Issues in the App Image  # noqa: E501

        :return: The new_app_medium of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_app_medium

    @new_app_medium.setter
    def new_app_medium(self, new_app_medium):
        """Sets the new_app_medium of this FullIssueCounts.

        The number of new Medium-severity Issues in the App Image  # noqa: E501

        :param new_app_medium: The new_app_medium of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._new_app_medium = new_app_medium

    @property
    def new_base_critical(self):
        """Gets the new_base_critical of this FullIssueCounts.  # noqa: E501

        The number of new Critical-severity Issues in the Base Image  # noqa: E501

        :return: The new_base_critical of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_base_critical

    @new_base_critical.setter
    def new_base_critical(self, new_base_critical):
        """Sets the new_base_critical of this FullIssueCounts.

        The number of new Critical-severity Issues in the Base Image  # noqa: E501

        :param new_base_critical: The new_base_critical of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._new_base_critical = new_base_critical

    @property
    def new_base_high(self):
        """Gets the new_base_high of this FullIssueCounts.  # noqa: E501

        The number of new High-severity Issues in the Base Image  # noqa: E501

        :return: The new_base_high of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_base_high

    @new_base_high.setter
    def new_base_high(self, new_base_high):
        """Sets the new_base_high of this FullIssueCounts.

        The number of new High-severity Issues in the Base Image  # noqa: E501

        :param new_base_high: The new_base_high of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._new_base_high = new_base_high

    @property
    def new_base_info(self):
        """Gets the new_base_info of this FullIssueCounts.  # noqa: E501

        The number of new Informational Issues in the Base Image  # noqa: E501

        :return: The new_base_info of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_base_info

    @new_base_info.setter
    def new_base_info(self, new_base_info):
        """Sets the new_base_info of this FullIssueCounts.

        The number of new Informational Issues in the Base Image  # noqa: E501

        :param new_base_info: The new_base_info of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._new_base_info = new_base_info

    @property
    def new_base_low(self):
        """Gets the new_base_low of this FullIssueCounts.  # noqa: E501

        The number of new Low-severity Issues in the Base Image  # noqa: E501

        :return: The new_base_low of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_base_low

    @new_base_low.setter
    def new_base_low(self, new_base_low):
        """Sets the new_base_low of this FullIssueCounts.

        The number of new Low-severity Issues in the Base Image  # noqa: E501

        :param new_base_low: The new_base_low of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._new_base_low = new_base_low

    @property
    def new_base_medium(self):
        """Gets the new_base_medium of this FullIssueCounts.  # noqa: E501

        The number of new Medium-severity Issues in the Base Image  # noqa: E501

        :return: The new_base_medium of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_base_medium

    @new_base_medium.setter
    def new_base_medium(self, new_base_medium):
        """Sets the new_base_medium of this FullIssueCounts.

        The number of new Medium-severity Issues in the Base Image  # noqa: E501

        :param new_base_medium: The new_base_medium of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._new_base_medium = new_base_medium

    @property
    def new_critical(self):
        """Gets the new_critical of this FullIssueCounts.  # noqa: E501

        The number of new Critical-severity Issues  # noqa: E501

        :return: The new_critical of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_critical

    @new_critical.setter
    def new_critical(self, new_critical):
        """Sets the new_critical of this FullIssueCounts.

        The number of new Critical-severity Issues  # noqa: E501

        :param new_critical: The new_critical of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_critical is None:
            raise ValueError("Invalid value for `new_critical`, must not be `None`")  # noqa: E501

        self._new_critical = new_critical

    @property
    def new_high(self):
        """Gets the new_high of this FullIssueCounts.  # noqa: E501

        The number of new High-severity Issues  # noqa: E501

        :return: The new_high of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_high

    @new_high.setter
    def new_high(self, new_high):
        """Sets the new_high of this FullIssueCounts.

        The number of new High-severity Issues  # noqa: E501

        :param new_high: The new_high of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_high is None:
            raise ValueError("Invalid value for `new_high`, must not be `None`")  # noqa: E501

        self._new_high = new_high

    @property
    def new_ignored_critical(self):
        """Gets the new_ignored_critical of this FullIssueCounts.  # noqa: E501

        The number of ignored Critical-severity Issues  # noqa: E501

        :return: The new_ignored_critical of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_ignored_critical

    @new_ignored_critical.setter
    def new_ignored_critical(self, new_ignored_critical):
        """Sets the new_ignored_critical of this FullIssueCounts.

        The number of ignored Critical-severity Issues  # noqa: E501

        :param new_ignored_critical: The new_ignored_critical of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_ignored_critical is None:
            raise ValueError("Invalid value for `new_ignored_critical`, must not be `None`")  # noqa: E501

        self._new_ignored_critical = new_ignored_critical

    @property
    def new_ignored_high(self):
        """Gets the new_ignored_high of this FullIssueCounts.  # noqa: E501

        The number of ignored High-severity Issues  # noqa: E501

        :return: The new_ignored_high of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_ignored_high

    @new_ignored_high.setter
    def new_ignored_high(self, new_ignored_high):
        """Sets the new_ignored_high of this FullIssueCounts.

        The number of ignored High-severity Issues  # noqa: E501

        :param new_ignored_high: The new_ignored_high of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_ignored_high is None:
            raise ValueError("Invalid value for `new_ignored_high`, must not be `None`")  # noqa: E501

        self._new_ignored_high = new_ignored_high

    @property
    def new_ignored_info(self):
        """Gets the new_ignored_info of this FullIssueCounts.  # noqa: E501

        The number of ignored Informational Issues  # noqa: E501

        :return: The new_ignored_info of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_ignored_info

    @new_ignored_info.setter
    def new_ignored_info(self, new_ignored_info):
        """Sets the new_ignored_info of this FullIssueCounts.

        The number of ignored Informational Issues  # noqa: E501

        :param new_ignored_info: The new_ignored_info of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_ignored_info is None:
            raise ValueError("Invalid value for `new_ignored_info`, must not be `None`")  # noqa: E501

        self._new_ignored_info = new_ignored_info

    @property
    def new_ignored_low(self):
        """Gets the new_ignored_low of this FullIssueCounts.  # noqa: E501

        The number of ignored Low-severity Issues  # noqa: E501

        :return: The new_ignored_low of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_ignored_low

    @new_ignored_low.setter
    def new_ignored_low(self, new_ignored_low):
        """Sets the new_ignored_low of this FullIssueCounts.

        The number of ignored Low-severity Issues  # noqa: E501

        :param new_ignored_low: The new_ignored_low of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_ignored_low is None:
            raise ValueError("Invalid value for `new_ignored_low`, must not be `None`")  # noqa: E501

        self._new_ignored_low = new_ignored_low

    @property
    def new_ignored_medium(self):
        """Gets the new_ignored_medium of this FullIssueCounts.  # noqa: E501

        The number of ignored Medium-severity Issues  # noqa: E501

        :return: The new_ignored_medium of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_ignored_medium

    @new_ignored_medium.setter
    def new_ignored_medium(self, new_ignored_medium):
        """Sets the new_ignored_medium of this FullIssueCounts.

        The number of ignored Medium-severity Issues  # noqa: E501

        :param new_ignored_medium: The new_ignored_medium of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_ignored_medium is None:
            raise ValueError("Invalid value for `new_ignored_medium`, must not be `None`")  # noqa: E501

        self._new_ignored_medium = new_ignored_medium

    @property
    def new_ignored_occurrences_critical(self):
        """Gets the new_ignored_occurrences_critical of this FullIssueCounts.  # noqa: E501

        The number of ignored Critical-severity Occurrences  # noqa: E501

        :return: The new_ignored_occurrences_critical of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_ignored_occurrences_critical

    @new_ignored_occurrences_critical.setter
    def new_ignored_occurrences_critical(self, new_ignored_occurrences_critical):
        """Sets the new_ignored_occurrences_critical of this FullIssueCounts.

        The number of ignored Critical-severity Occurrences  # noqa: E501

        :param new_ignored_occurrences_critical: The new_ignored_occurrences_critical of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_ignored_occurrences_critical is None:
            raise ValueError("Invalid value for `new_ignored_occurrences_critical`, must not be `None`")  # noqa: E501

        self._new_ignored_occurrences_critical = new_ignored_occurrences_critical

    @property
    def new_ignored_occurrences_high(self):
        """Gets the new_ignored_occurrences_high of this FullIssueCounts.  # noqa: E501

        The number of ignored High-severity Occurrences  # noqa: E501

        :return: The new_ignored_occurrences_high of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_ignored_occurrences_high

    @new_ignored_occurrences_high.setter
    def new_ignored_occurrences_high(self, new_ignored_occurrences_high):
        """Sets the new_ignored_occurrences_high of this FullIssueCounts.

        The number of ignored High-severity Occurrences  # noqa: E501

        :param new_ignored_occurrences_high: The new_ignored_occurrences_high of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_ignored_occurrences_high is None:
            raise ValueError("Invalid value for `new_ignored_occurrences_high`, must not be `None`")  # noqa: E501

        self._new_ignored_occurrences_high = new_ignored_occurrences_high

    @property
    def new_ignored_occurrences_info(self):
        """Gets the new_ignored_occurrences_info of this FullIssueCounts.  # noqa: E501

        The number of ignored Informational Occurrences  # noqa: E501

        :return: The new_ignored_occurrences_info of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_ignored_occurrences_info

    @new_ignored_occurrences_info.setter
    def new_ignored_occurrences_info(self, new_ignored_occurrences_info):
        """Sets the new_ignored_occurrences_info of this FullIssueCounts.

        The number of ignored Informational Occurrences  # noqa: E501

        :param new_ignored_occurrences_info: The new_ignored_occurrences_info of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_ignored_occurrences_info is None:
            raise ValueError("Invalid value for `new_ignored_occurrences_info`, must not be `None`")  # noqa: E501

        self._new_ignored_occurrences_info = new_ignored_occurrences_info

    @property
    def new_ignored_occurrences_low(self):
        """Gets the new_ignored_occurrences_low of this FullIssueCounts.  # noqa: E501

        The number of ignored Low-severity Occurrences  # noqa: E501

        :return: The new_ignored_occurrences_low of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_ignored_occurrences_low

    @new_ignored_occurrences_low.setter
    def new_ignored_occurrences_low(self, new_ignored_occurrences_low):
        """Sets the new_ignored_occurrences_low of this FullIssueCounts.

        The number of ignored Low-severity Occurrences  # noqa: E501

        :param new_ignored_occurrences_low: The new_ignored_occurrences_low of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_ignored_occurrences_low is None:
            raise ValueError("Invalid value for `new_ignored_occurrences_low`, must not be `None`")  # noqa: E501

        self._new_ignored_occurrences_low = new_ignored_occurrences_low

    @property
    def new_ignored_occurrences_medium(self):
        """Gets the new_ignored_occurrences_medium of this FullIssueCounts.  # noqa: E501

        The number of ignored Medium-severity Occurrences  # noqa: E501

        :return: The new_ignored_occurrences_medium of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_ignored_occurrences_medium

    @new_ignored_occurrences_medium.setter
    def new_ignored_occurrences_medium(self, new_ignored_occurrences_medium):
        """Sets the new_ignored_occurrences_medium of this FullIssueCounts.

        The number of ignored Medium-severity Occurrences  # noqa: E501

        :param new_ignored_occurrences_medium: The new_ignored_occurrences_medium of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_ignored_occurrences_medium is None:
            raise ValueError("Invalid value for `new_ignored_occurrences_medium`, must not be `None`")  # noqa: E501

        self._new_ignored_occurrences_medium = new_ignored_occurrences_medium

    @property
    def new_ignored_occurrences_unassigned(self):
        """Gets the new_ignored_occurrences_unassigned of this FullIssueCounts.  # noqa: E501

        The number of ignored Occurrences with no associated severity code  # noqa: E501

        :return: The new_ignored_occurrences_unassigned of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_ignored_occurrences_unassigned

    @new_ignored_occurrences_unassigned.setter
    def new_ignored_occurrences_unassigned(self, new_ignored_occurrences_unassigned):
        """Sets the new_ignored_occurrences_unassigned of this FullIssueCounts.

        The number of ignored Occurrences with no associated severity code  # noqa: E501

        :param new_ignored_occurrences_unassigned: The new_ignored_occurrences_unassigned of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_ignored_occurrences_unassigned is None:
            raise ValueError("Invalid value for `new_ignored_occurrences_unassigned`, must not be `None`")  # noqa: E501

        self._new_ignored_occurrences_unassigned = new_ignored_occurrences_unassigned

    @property
    def new_ignored_unassigned(self):
        """Gets the new_ignored_unassigned of this FullIssueCounts.  # noqa: E501

        The number of Issues with no associated severity code  # noqa: E501

        :return: The new_ignored_unassigned of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_ignored_unassigned

    @new_ignored_unassigned.setter
    def new_ignored_unassigned(self, new_ignored_unassigned):
        """Sets the new_ignored_unassigned of this FullIssueCounts.

        The number of Issues with no associated severity code  # noqa: E501

        :param new_ignored_unassigned: The new_ignored_unassigned of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_ignored_unassigned is None:
            raise ValueError("Invalid value for `new_ignored_unassigned`, must not be `None`")  # noqa: E501

        self._new_ignored_unassigned = new_ignored_unassigned

    @property
    def new_info(self):
        """Gets the new_info of this FullIssueCounts.  # noqa: E501

        The number of new Informational Issues  # noqa: E501

        :return: The new_info of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_info

    @new_info.setter
    def new_info(self, new_info):
        """Sets the new_info of this FullIssueCounts.

        The number of new Informational Issues  # noqa: E501

        :param new_info: The new_info of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_info is None:
            raise ValueError("Invalid value for `new_info`, must not be `None`")  # noqa: E501

        self._new_info = new_info

    @property
    def new_low(self):
        """Gets the new_low of this FullIssueCounts.  # noqa: E501

        The number of new Low-severity Issues  # noqa: E501

        :return: The new_low of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_low

    @new_low.setter
    def new_low(self, new_low):
        """Sets the new_low of this FullIssueCounts.

        The number of new Low-severity Issues  # noqa: E501

        :param new_low: The new_low of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_low is None:
            raise ValueError("Invalid value for `new_low`, must not be `None`")  # noqa: E501

        self._new_low = new_low

    @property
    def new_medium(self):
        """Gets the new_medium of this FullIssueCounts.  # noqa: E501

        The number of new Medium-severity Issues  # noqa: E501

        :return: The new_medium of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_medium

    @new_medium.setter
    def new_medium(self, new_medium):
        """Sets the new_medium of this FullIssueCounts.

        The number of new Medium-severity Issues  # noqa: E501

        :param new_medium: The new_medium of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_medium is None:
            raise ValueError("Invalid value for `new_medium`, must not be `None`")  # noqa: E501

        self._new_medium = new_medium

    @property
    def new_occurrences_critical(self):
        """Gets the new_occurrences_critical of this FullIssueCounts.  # noqa: E501

        The number of new Critical-severity Occurrences  # noqa: E501

        :return: The new_occurrences_critical of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_occurrences_critical

    @new_occurrences_critical.setter
    def new_occurrences_critical(self, new_occurrences_critical):
        """Sets the new_occurrences_critical of this FullIssueCounts.

        The number of new Critical-severity Occurrences  # noqa: E501

        :param new_occurrences_critical: The new_occurrences_critical of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_occurrences_critical is None:
            raise ValueError("Invalid value for `new_occurrences_critical`, must not be `None`")  # noqa: E501

        self._new_occurrences_critical = new_occurrences_critical

    @property
    def new_occurrences_high(self):
        """Gets the new_occurrences_high of this FullIssueCounts.  # noqa: E501

        The number of new High-severity Occurrences  # noqa: E501

        :return: The new_occurrences_high of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_occurrences_high

    @new_occurrences_high.setter
    def new_occurrences_high(self, new_occurrences_high):
        """Sets the new_occurrences_high of this FullIssueCounts.

        The number of new High-severity Occurrences  # noqa: E501

        :param new_occurrences_high: The new_occurrences_high of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_occurrences_high is None:
            raise ValueError("Invalid value for `new_occurrences_high`, must not be `None`")  # noqa: E501

        self._new_occurrences_high = new_occurrences_high

    @property
    def new_occurrences_info(self):
        """Gets the new_occurrences_info of this FullIssueCounts.  # noqa: E501

        The number of new Informational Occurrences  # noqa: E501

        :return: The new_occurrences_info of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_occurrences_info

    @new_occurrences_info.setter
    def new_occurrences_info(self, new_occurrences_info):
        """Sets the new_occurrences_info of this FullIssueCounts.

        The number of new Informational Occurrences  # noqa: E501

        :param new_occurrences_info: The new_occurrences_info of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_occurrences_info is None:
            raise ValueError("Invalid value for `new_occurrences_info`, must not be `None`")  # noqa: E501

        self._new_occurrences_info = new_occurrences_info

    @property
    def new_occurrences_low(self):
        """Gets the new_occurrences_low of this FullIssueCounts.  # noqa: E501

        The number of new Low-severity Occurrences  # noqa: E501

        :return: The new_occurrences_low of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_occurrences_low

    @new_occurrences_low.setter
    def new_occurrences_low(self, new_occurrences_low):
        """Sets the new_occurrences_low of this FullIssueCounts.

        The number of new Low-severity Occurrences  # noqa: E501

        :param new_occurrences_low: The new_occurrences_low of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_occurrences_low is None:
            raise ValueError("Invalid value for `new_occurrences_low`, must not be `None`")  # noqa: E501

        self._new_occurrences_low = new_occurrences_low

    @property
    def new_occurrences_medium(self):
        """Gets the new_occurrences_medium of this FullIssueCounts.  # noqa: E501

        The number of new Medium-severity Occurrences  # noqa: E501

        :return: The new_occurrences_medium of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_occurrences_medium

    @new_occurrences_medium.setter
    def new_occurrences_medium(self, new_occurrences_medium):
        """Sets the new_occurrences_medium of this FullIssueCounts.

        The number of new Medium-severity Occurrences  # noqa: E501

        :param new_occurrences_medium: The new_occurrences_medium of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_occurrences_medium is None:
            raise ValueError("Invalid value for `new_occurrences_medium`, must not be `None`")  # noqa: E501

        self._new_occurrences_medium = new_occurrences_medium

    @property
    def new_occurrences_unassigned(self):
        """Gets the new_occurrences_unassigned of this FullIssueCounts.  # noqa: E501

        The number of new Occurrences with no associated severity code  # noqa: E501

        :return: The new_occurrences_unassigned of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_occurrences_unassigned

    @new_occurrences_unassigned.setter
    def new_occurrences_unassigned(self, new_occurrences_unassigned):
        """Sets the new_occurrences_unassigned of this FullIssueCounts.

        The number of new Occurrences with no associated severity code  # noqa: E501

        :param new_occurrences_unassigned: The new_occurrences_unassigned of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_occurrences_unassigned is None:
            raise ValueError("Invalid value for `new_occurrences_unassigned`, must not be `None`")  # noqa: E501

        self._new_occurrences_unassigned = new_occurrences_unassigned

    @property
    def new_total(self):
        """Gets the new_total of this FullIssueCounts.  # noqa: E501

        The total number new Issues  # noqa: E501

        :return: The new_total of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_total

    @new_total.setter
    def new_total(self, new_total):
        """Sets the new_total of this FullIssueCounts.

        The total number new Issues  # noqa: E501

        :param new_total: The new_total of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_total is None:
            raise ValueError("Invalid value for `new_total`, must not be `None`")  # noqa: E501

        self._new_total = new_total

    @property
    def new_total_base(self):
        """Gets the new_total_base of this FullIssueCounts.  # noqa: E501

        The total number new Issues in the Base Image  # noqa: E501

        :return: The new_total_base of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_total_base

    @new_total_base.setter
    def new_total_base(self, new_total_base):
        """Sets the new_total_base of this FullIssueCounts.

        The total number new Issues in the Base Image  # noqa: E501

        :param new_total_base: The new_total_base of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._new_total_base = new_total_base

    @property
    def new_unassigned(self):
        """Gets the new_unassigned of this FullIssueCounts.  # noqa: E501

        The number of new Issues with no associated severity code  # noqa: E501

        :return: The new_unassigned of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._new_unassigned

    @new_unassigned.setter
    def new_unassigned(self, new_unassigned):
        """Sets the new_unassigned of this FullIssueCounts.

        The number of new Issues with no associated severity code  # noqa: E501

        :param new_unassigned: The new_unassigned of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if new_unassigned is None:
            raise ValueError("Invalid value for `new_unassigned`, must not be `None`")  # noqa: E501

        self._new_unassigned = new_unassigned

    @property
    def total(self):
        """Gets the total of this FullIssueCounts.  # noqa: E501

        The total number of Issues  # noqa: E501

        :return: The total of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this FullIssueCounts.

        The total number of Issues  # noqa: E501

        :param total: The total of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if total is None:
            raise ValueError("Invalid value for `total`, must not be `None`")  # noqa: E501

        self._total = total

    @property
    def total_base(self):
        """Gets the total_base of this FullIssueCounts.  # noqa: E501

        The total number of Issues in the Base Image  # noqa: E501

        :return: The total_base of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._total_base

    @total_base.setter
    def total_base(self, total_base):
        """Sets the total_base of this FullIssueCounts.

        The total number of Issues in the Base Image  # noqa: E501

        :param total_base: The total_base of this FullIssueCounts.  # noqa: E501
        :type: int
        """

        self._total_base = total_base

    @property
    def unassigned(self):
        """Gets the unassigned of this FullIssueCounts.  # noqa: E501

        The number of Issues with no associated severity code  # noqa: E501

        :return: The unassigned of this FullIssueCounts.  # noqa: E501
        :rtype: int
        """
        return self._unassigned

    @unassigned.setter
    def unassigned(self, unassigned):
        """Sets the unassigned of this FullIssueCounts.

        The number of Issues with no associated severity code  # noqa: E501

        :param unassigned: The unassigned of this FullIssueCounts.  # noqa: E501
        :type: int
        """
        if unassigned is None:
            raise ValueError("Invalid value for `unassigned`, must not be `None`")  # noqa: E501

        self._unassigned = unassigned

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
        if issubclass(FullIssueCounts, dict):
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
        if not isinstance(other, FullIssueCounts):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
