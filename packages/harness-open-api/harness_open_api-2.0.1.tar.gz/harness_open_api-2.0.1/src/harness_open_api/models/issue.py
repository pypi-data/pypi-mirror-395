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

class Issue(object):
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
        'base_image_name': 'str',
        'baseline_variant_id': 'str',
        'created': 'int',
        'current_status': 'str',
        'details': 'dict(str, object)',
        'epss_last_modified': 'str',
        'epss_percentile': 'float',
        'epss_score': 'float',
        'exemption_coverage': 'str',
        'exemption_id': 'str',
        'exemption_status_at_scan': 'str',
        'harness_augmentation': 'dict(str, object)',
        'id': 'str',
        'key': 'str',
        'num_occurrences': 'int',
        'occurrence_id': 'int',
        'occurrences': 'list[dict(str, object)]',
        'origin_status': 'str',
        'origins': 'list[str]',
        'product_id': 'str',
        'severity': 'float',
        'severity_code': 'str',
        'status': 'str',
        'subproduct': 'str',
        'target_id': 'str',
        'target_name': 'str',
        'target_type': 'str',
        'target_variant_id': 'str',
        'target_variant_name': 'str',
        'title': 'str',
        'type': 'str'
    }

    attribute_map = {
        'base_image_name': 'baseImageName',
        'baseline_variant_id': 'baselineVariantId',
        'created': 'created',
        'current_status': 'currentStatus',
        'details': 'details',
        'epss_last_modified': 'epssLastModified',
        'epss_percentile': 'epssPercentile',
        'epss_score': 'epssScore',
        'exemption_coverage': 'exemptionCoverage',
        'exemption_id': 'exemptionId',
        'exemption_status_at_scan': 'exemptionStatusAtScan',
        'harness_augmentation': 'harnessAugmentation',
        'id': 'id',
        'key': 'key',
        'num_occurrences': 'numOccurrences',
        'occurrence_id': 'occurrenceId',
        'occurrences': 'occurrences',
        'origin_status': 'originStatus',
        'origins': 'origins',
        'product_id': 'productId',
        'severity': 'severity',
        'severity_code': 'severityCode',
        'status': 'status',
        'subproduct': 'subproduct',
        'target_id': 'targetId',
        'target_name': 'targetName',
        'target_type': 'targetType',
        'target_variant_id': 'targetVariantId',
        'target_variant_name': 'targetVariantName',
        'title': 'title',
        'type': 'type'
    }

    def __init__(self, base_image_name=None, baseline_variant_id=None, created=None, current_status=None, details=None, epss_last_modified=None, epss_percentile=None, epss_score=None, exemption_coverage=None, exemption_id=None, exemption_status_at_scan=None, harness_augmentation=None, id=None, key=None, num_occurrences=None, occurrence_id=None, occurrences=None, origin_status=None, origins=None, product_id=None, severity=None, severity_code=None, status=None, subproduct=None, target_id=None, target_name=None, target_type=None, target_variant_id=None, target_variant_name=None, title=None, type=None):  # noqa: E501
        """Issue - a model defined in Swagger"""  # noqa: E501
        self._base_image_name = None
        self._baseline_variant_id = None
        self._created = None
        self._current_status = None
        self._details = None
        self._epss_last_modified = None
        self._epss_percentile = None
        self._epss_score = None
        self._exemption_coverage = None
        self._exemption_id = None
        self._exemption_status_at_scan = None
        self._harness_augmentation = None
        self._id = None
        self._key = None
        self._num_occurrences = None
        self._occurrence_id = None
        self._occurrences = None
        self._origin_status = None
        self._origins = None
        self._product_id = None
        self._severity = None
        self._severity_code = None
        self._status = None
        self._subproduct = None
        self._target_id = None
        self._target_name = None
        self._target_type = None
        self._target_variant_id = None
        self._target_variant_name = None
        self._title = None
        self._type = None
        self.discriminator = None
        if base_image_name is not None:
            self.base_image_name = base_image_name
        if baseline_variant_id is not None:
            self.baseline_variant_id = baseline_variant_id
        self.created = created
        if current_status is not None:
            self.current_status = current_status
        self.details = details
        if epss_last_modified is not None:
            self.epss_last_modified = epss_last_modified
        if epss_percentile is not None:
            self.epss_percentile = epss_percentile
        if epss_score is not None:
            self.epss_score = epss_score
        if exemption_coverage is not None:
            self.exemption_coverage = exemption_coverage
        if exemption_id is not None:
            self.exemption_id = exemption_id
        if exemption_status_at_scan is not None:
            self.exemption_status_at_scan = exemption_status_at_scan
        if harness_augmentation is not None:
            self.harness_augmentation = harness_augmentation
        self.id = id
        self.key = key
        if num_occurrences is not None:
            self.num_occurrences = num_occurrences
        if occurrence_id is not None:
            self.occurrence_id = occurrence_id
        if occurrences is not None:
            self.occurrences = occurrences
        if origin_status is not None:
            self.origin_status = origin_status
        if origins is not None:
            self.origins = origins
        self.product_id = product_id
        self.severity = severity
        self.severity_code = severity_code
        if status is not None:
            self.status = status
        if subproduct is not None:
            self.subproduct = subproduct
        if target_id is not None:
            self.target_id = target_id
        if target_name is not None:
            self.target_name = target_name
        if target_type is not None:
            self.target_type = target_type
        if target_variant_id is not None:
            self.target_variant_id = target_variant_id
        if target_variant_name is not None:
            self.target_variant_name = target_variant_name
        self.title = title
        if type is not None:
            self.type = type

    @property
    def base_image_name(self):
        """Gets the base_image_name of this Issue.  # noqa: E501

        base image name of the issue  # noqa: E501

        :return: The base_image_name of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._base_image_name

    @base_image_name.setter
    def base_image_name(self, base_image_name):
        """Sets the base_image_name of this Issue.

        base image name of the issue  # noqa: E501

        :param base_image_name: The base_image_name of this Issue.  # noqa: E501
        :type: str
        """

        self._base_image_name = base_image_name

    @property
    def baseline_variant_id(self):
        """Gets the baseline_variant_id of this Issue.  # noqa: E501

        The Baseline Target Variant related to this Security Issue  # noqa: E501

        :return: The baseline_variant_id of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._baseline_variant_id

    @baseline_variant_id.setter
    def baseline_variant_id(self, baseline_variant_id):
        """Sets the baseline_variant_id of this Issue.

        The Baseline Target Variant related to this Security Issue  # noqa: E501

        :param baseline_variant_id: The baseline_variant_id of this Issue.  # noqa: E501
        :type: str
        """

        self._baseline_variant_id = baseline_variant_id

    @property
    def created(self):
        """Gets the created of this Issue.  # noqa: E501

        Unix timestamp at which the resource was created  # noqa: E501

        :return: The created of this Issue.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this Issue.

        Unix timestamp at which the resource was created  # noqa: E501

        :param created: The created of this Issue.  # noqa: E501
        :type: int
        """
        if created is None:
            raise ValueError("Invalid value for `created`, must not be `None`")  # noqa: E501

        self._created = created

    @property
    def current_status(self):
        """Gets the current_status of this Issue.  # noqa: E501

        Current status of the Exemption  # noqa: E501

        :return: The current_status of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._current_status

    @current_status.setter
    def current_status(self, current_status):
        """Sets the current_status of this Issue.

        Current status of the Exemption  # noqa: E501

        :param current_status: The current_status of this Issue.  # noqa: E501
        :type: str
        """
        allowed_values = ["Pending", "Approved", "Rejected", "Expired"]  # noqa: E501
        if current_status not in allowed_values:
            raise ValueError(
                "Invalid value for `current_status` ({0}), must be one of {1}"  # noqa: E501
                .format(current_status, allowed_values)
            )

        self._current_status = current_status

    @property
    def details(self):
        """Gets the details of this Issue.  # noqa: E501

        Issue details common to all occurrences  # noqa: E501

        :return: The details of this Issue.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this Issue.

        Issue details common to all occurrences  # noqa: E501

        :param details: The details of this Issue.  # noqa: E501
        :type: dict(str, object)
        """
        if details is None:
            raise ValueError("Invalid value for `details`, must not be `None`")  # noqa: E501

        self._details = details

    @property
    def epss_last_modified(self):
        """Gets the epss_last_modified of this Issue.  # noqa: E501

        Last date the issue EPSS data was last modified  # noqa: E501

        :return: The epss_last_modified of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._epss_last_modified

    @epss_last_modified.setter
    def epss_last_modified(self, epss_last_modified):
        """Sets the epss_last_modified of this Issue.

        Last date the issue EPSS data was last modified  # noqa: E501

        :param epss_last_modified: The epss_last_modified of this Issue.  # noqa: E501
        :type: str
        """

        self._epss_last_modified = epss_last_modified

    @property
    def epss_percentile(self):
        """Gets the epss_percentile of this Issue.  # noqa: E501

        EPSS percentile of the issue CVE identifier  # noqa: E501

        :return: The epss_percentile of this Issue.  # noqa: E501
        :rtype: float
        """
        return self._epss_percentile

    @epss_percentile.setter
    def epss_percentile(self, epss_percentile):
        """Sets the epss_percentile of this Issue.

        EPSS percentile of the issue CVE identifier  # noqa: E501

        :param epss_percentile: The epss_percentile of this Issue.  # noqa: E501
        :type: float
        """

        self._epss_percentile = epss_percentile

    @property
    def epss_score(self):
        """Gets the epss_score of this Issue.  # noqa: E501

        EPSS score of the issue CVE identifier  # noqa: E501

        :return: The epss_score of this Issue.  # noqa: E501
        :rtype: float
        """
        return self._epss_score

    @epss_score.setter
    def epss_score(self, epss_score):
        """Sets the epss_score of this Issue.

        EPSS score of the issue CVE identifier  # noqa: E501

        :param epss_score: The epss_score of this Issue.  # noqa: E501
        :type: float
        """

        self._epss_score = epss_score

    @property
    def exemption_coverage(self):
        """Gets the exemption_coverage of this Issue.  # noqa: E501

        Indicates if the Security Issue was found to be Exempted, Partially Exempted.  # noqa: E501

        :return: The exemption_coverage of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._exemption_coverage

    @exemption_coverage.setter
    def exemption_coverage(self, exemption_coverage):
        """Sets the exemption_coverage of this Issue.

        Indicates if the Security Issue was found to be Exempted, Partially Exempted.  # noqa: E501

        :param exemption_coverage: The exemption_coverage of this Issue.  # noqa: E501
        :type: str
        """

        self._exemption_coverage = exemption_coverage

    @property
    def exemption_id(self):
        """Gets the exemption_id of this Issue.  # noqa: E501

        ID of Security Test Exemption  # noqa: E501

        :return: The exemption_id of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._exemption_id

    @exemption_id.setter
    def exemption_id(self, exemption_id):
        """Sets the exemption_id of this Issue.

        ID of Security Test Exemption  # noqa: E501

        :param exemption_id: The exemption_id of this Issue.  # noqa: E501
        :type: str
        """

        self._exemption_id = exemption_id

    @property
    def exemption_status_at_scan(self):
        """Gets the exemption_status_at_scan of this Issue.  # noqa: E501

        Exemption's status at the Security Scan created time  # noqa: E501

        :return: The exemption_status_at_scan of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._exemption_status_at_scan

    @exemption_status_at_scan.setter
    def exemption_status_at_scan(self, exemption_status_at_scan):
        """Sets the exemption_status_at_scan of this Issue.

        Exemption's status at the Security Scan created time  # noqa: E501

        :param exemption_status_at_scan: The exemption_status_at_scan of this Issue.  # noqa: E501
        :type: str
        """
        allowed_values = ["Pending", "Approved", "Rejected", "Expired"]  # noqa: E501
        if exemption_status_at_scan not in allowed_values:
            raise ValueError(
                "Invalid value for `exemption_status_at_scan` ({0}), must be one of {1}"  # noqa: E501
                .format(exemption_status_at_scan, allowed_values)
            )

        self._exemption_status_at_scan = exemption_status_at_scan

    @property
    def harness_augmentation(self):
        """Gets the harness_augmentation of this Issue.  # noqa: E501

        Harness Augmentation details  # noqa: E501

        :return: The harness_augmentation of this Issue.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._harness_augmentation

    @harness_augmentation.setter
    def harness_augmentation(self, harness_augmentation):
        """Sets the harness_augmentation of this Issue.

        Harness Augmentation details  # noqa: E501

        :param harness_augmentation: The harness_augmentation of this Issue.  # noqa: E501
        :type: dict(str, object)
        """

        self._harness_augmentation = harness_augmentation

    @property
    def id(self):
        """Gets the id of this Issue.  # noqa: E501

        Resource identifier  # noqa: E501

        :return: The id of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Issue.

        Resource identifier  # noqa: E501

        :param id: The id of this Issue.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def key(self):
        """Gets the key of this Issue.  # noqa: E501

        Compression/deduplication key  # noqa: E501

        :return: The key of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this Issue.

        Compression/deduplication key  # noqa: E501

        :param key: The key of this Issue.  # noqa: E501
        :type: str
        """
        if key is None:
            raise ValueError("Invalid value for `key`, must not be `None`")  # noqa: E501

        self._key = key

    @property
    def num_occurrences(self):
        """Gets the num_occurrences of this Issue.  # noqa: E501

        Indicates the number of Occurrences on the Issue  # noqa: E501

        :return: The num_occurrences of this Issue.  # noqa: E501
        :rtype: int
        """
        return self._num_occurrences

    @num_occurrences.setter
    def num_occurrences(self, num_occurrences):
        """Sets the num_occurrences of this Issue.

        Indicates the number of Occurrences on the Issue  # noqa: E501

        :param num_occurrences: The num_occurrences of this Issue.  # noqa: E501
        :type: int
        """

        self._num_occurrences = num_occurrences

    @property
    def occurrence_id(self):
        """Gets the occurrence_id of this Issue.  # noqa: E501


        :return: The occurrence_id of this Issue.  # noqa: E501
        :rtype: int
        """
        return self._occurrence_id

    @occurrence_id.setter
    def occurrence_id(self, occurrence_id):
        """Sets the occurrence_id of this Issue.


        :param occurrence_id: The occurrence_id of this Issue.  # noqa: E501
        :type: int
        """

        self._occurrence_id = occurrence_id

    @property
    def occurrences(self):
        """Gets the occurrences of this Issue.  # noqa: E501

        Array of details unique to each occurrence  # noqa: E501

        :return: The occurrences of this Issue.  # noqa: E501
        :rtype: list[dict(str, object)]
        """
        return self._occurrences

    @occurrences.setter
    def occurrences(self, occurrences):
        """Sets the occurrences of this Issue.

        Array of details unique to each occurrence  # noqa: E501

        :param occurrences: The occurrences of this Issue.  # noqa: E501
        :type: list[dict(str, object)]
        """

        self._occurrences = occurrences

    @property
    def origin_status(self):
        """Gets the origin_status of this Issue.  # noqa: E501

        The status of the origin, either 'approved' or 'unapproved'  # noqa: E501

        :return: The origin_status of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._origin_status

    @origin_status.setter
    def origin_status(self, origin_status):
        """Sets the origin_status of this Issue.

        The status of the origin, either 'approved' or 'unapproved'  # noqa: E501

        :param origin_status: The origin_status of this Issue.  # noqa: E501
        :type: str
        """

        self._origin_status = origin_status

    @property
    def origins(self):
        """Gets the origins of this Issue.  # noqa: E501

        The origins of the issue  # noqa: E501

        :return: The origins of this Issue.  # noqa: E501
        :rtype: list[str]
        """
        return self._origins

    @origins.setter
    def origins(self, origins):
        """Sets the origins of this Issue.

        The origins of the issue  # noqa: E501

        :param origins: The origins of this Issue.  # noqa: E501
        :type: list[str]
        """

        self._origins = origins

    @property
    def product_id(self):
        """Gets the product_id of this Issue.  # noqa: E501

        The scan tool that identified this Security Issue  # noqa: E501

        :return: The product_id of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        """Sets the product_id of this Issue.

        The scan tool that identified this Security Issue  # noqa: E501

        :param product_id: The product_id of this Issue.  # noqa: E501
        :type: str
        """
        if product_id is None:
            raise ValueError("Invalid value for `product_id`, must not be `None`")  # noqa: E501

        self._product_id = product_id

    @property
    def severity(self):
        """Gets the severity of this Issue.  # noqa: E501

        Numeric severity, from 0 (lowest) to 10 (highest)  # noqa: E501

        :return: The severity of this Issue.  # noqa: E501
        :rtype: float
        """
        return self._severity

    @severity.setter
    def severity(self, severity):
        """Sets the severity of this Issue.

        Numeric severity, from 0 (lowest) to 10 (highest)  # noqa: E501

        :param severity: The severity of this Issue.  # noqa: E501
        :type: float
        """
        if severity is None:
            raise ValueError("Invalid value for `severity`, must not be `None`")  # noqa: E501

        self._severity = severity

    @property
    def severity_code(self):
        """Gets the severity_code of this Issue.  # noqa: E501

        Severity code  # noqa: E501

        :return: The severity_code of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._severity_code

    @severity_code.setter
    def severity_code(self, severity_code):
        """Sets the severity_code of this Issue.

        Severity code  # noqa: E501

        :param severity_code: The severity_code of this Issue.  # noqa: E501
        :type: str
        """
        if severity_code is None:
            raise ValueError("Invalid value for `severity_code`, must not be `None`")  # noqa: E501
        allowed_values = ["Critical", "High", "Medium", "Low", "Info", "Unassigned"]  # noqa: E501
        if severity_code not in allowed_values:
            raise ValueError(
                "Invalid value for `severity_code` ({0}), must be one of {1}"  # noqa: E501
                .format(severity_code, allowed_values)
            )

        self._severity_code = severity_code

    @property
    def status(self):
        """Gets the status of this Issue.  # noqa: E501

        Indicates if the Security Issue was found to be remediated, ignored, etc.  # noqa: E501

        :return: The status of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Issue.

        Indicates if the Security Issue was found to be remediated, ignored, etc.  # noqa: E501

        :param status: The status of this Issue.  # noqa: E501
        :type: str
        """
        allowed_values = ["Remediated", "Compensating Controls", "Acceptable Use", "Acceptable Risk", "False Positive", "Fix Unavailable", "Exempted"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def subproduct(self):
        """Gets the subproduct of this Issue.  # noqa: E501

        The subproduct that identified this Security Issue  # noqa: E501

        :return: The subproduct of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._subproduct

    @subproduct.setter
    def subproduct(self, subproduct):
        """Sets the subproduct of this Issue.

        The subproduct that identified this Security Issue  # noqa: E501

        :param subproduct: The subproduct of this Issue.  # noqa: E501
        :type: str
        """

        self._subproduct = subproduct

    @property
    def target_id(self):
        """Gets the target_id of this Issue.  # noqa: E501

        The Target that this Security Issue affects  # noqa: E501

        :return: The target_id of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """Sets the target_id of this Issue.

        The Target that this Security Issue affects  # noqa: E501

        :param target_id: The target_id of this Issue.  # noqa: E501
        :type: str
        """

        self._target_id = target_id

    @property
    def target_name(self):
        """Gets the target_name of this Issue.  # noqa: E501

        The Name of the Target that this Security Issue affects  # noqa: E501

        :return: The target_name of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._target_name

    @target_name.setter
    def target_name(self, target_name):
        """Sets the target_name of this Issue.

        The Name of the Target that this Security Issue affects  # noqa: E501

        :param target_name: The target_name of this Issue.  # noqa: E501
        :type: str
        """

        self._target_name = target_name

    @property
    def target_type(self):
        """Gets the target_type of this Issue.  # noqa: E501

        The type of the Target that this Security Issue affects  # noqa: E501

        :return: The target_type of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._target_type

    @target_type.setter
    def target_type(self, target_type):
        """Sets the target_type of this Issue.

        The type of the Target that this Security Issue affects  # noqa: E501

        :param target_type: The target_type of this Issue.  # noqa: E501
        :type: str
        """
        allowed_values = ["container", "repository", "instance", "configuration"]  # noqa: E501
        if target_type not in allowed_values:
            raise ValueError(
                "Invalid value for `target_type` ({0}), must be one of {1}"  # noqa: E501
                .format(target_type, allowed_values)
            )

        self._target_type = target_type

    @property
    def target_variant_id(self):
        """Gets the target_variant_id of this Issue.  # noqa: E501

        The Target Variant that this Security Issue affects  # noqa: E501

        :return: The target_variant_id of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._target_variant_id

    @target_variant_id.setter
    def target_variant_id(self, target_variant_id):
        """Sets the target_variant_id of this Issue.

        The Target Variant that this Security Issue affects  # noqa: E501

        :param target_variant_id: The target_variant_id of this Issue.  # noqa: E501
        :type: str
        """

        self._target_variant_id = target_variant_id

    @property
    def target_variant_name(self):
        """Gets the target_variant_name of this Issue.  # noqa: E501

        Name of the associated Target and Variant  # noqa: E501

        :return: The target_variant_name of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._target_variant_name

    @target_variant_name.setter
    def target_variant_name(self, target_variant_name):
        """Sets the target_variant_name of this Issue.

        Name of the associated Target and Variant  # noqa: E501

        :param target_variant_name: The target_variant_name of this Issue.  # noqa: E501
        :type: str
        """

        self._target_variant_name = target_variant_name

    @property
    def title(self):
        """Gets the title of this Issue.  # noqa: E501

        Title of the Security Issue  # noqa: E501

        :return: The title of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Issue.

        Title of the Security Issue  # noqa: E501

        :param title: The title of this Issue.  # noqa: E501
        :type: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501

        self._title = title

    @property
    def type(self):
        """Gets the type of this Issue.  # noqa: E501

        The type of vulnerability or quality issue for this Issue  # noqa: E501

        :return: The type of this Issue.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Issue.

        The type of vulnerability or quality issue for this Issue  # noqa: E501

        :param type: The type of this Issue.  # noqa: E501
        :type: str
        """
        allowed_values = ["SAST", "DAST", "SCA", "IAC", "SECRET", "MISCONFIG", "BUG_SMELLS", "CODE_SMELLS", "CODE_COVERAGE", "EXTERNAL_POLICY"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

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
        if issubclass(Issue, dict):
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
        if not isinstance(other, Issue):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
