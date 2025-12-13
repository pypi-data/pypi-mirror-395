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

class ScanMetadata(object):
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
        'base_image_digest': 'str',
        'base_image_name': 'str',
        'base_image_tag': 'str',
        'deduplicated_count': 'int',
        'image_domain': 'str',
        'image_name': 'str',
        'image_tag': 'str',
        'normalized_count': 'int'
    }

    attribute_map = {
        'base_image_digest': 'baseImageDigest',
        'base_image_name': 'baseImageName',
        'base_image_tag': 'baseImageTag',
        'deduplicated_count': 'deduplicatedCount',
        'image_domain': 'imageDomain',
        'image_name': 'imageName',
        'image_tag': 'imageTag',
        'normalized_count': 'normalizedCount'
    }

    def __init__(self, base_image_digest=None, base_image_name=None, base_image_tag=None, deduplicated_count=None, image_domain=None, image_name=None, image_tag=None, normalized_count=None):  # noqa: E501
        """ScanMetadata - a model defined in Swagger"""  # noqa: E501
        self._base_image_digest = None
        self._base_image_name = None
        self._base_image_tag = None
        self._deduplicated_count = None
        self._image_domain = None
        self._image_name = None
        self._image_tag = None
        self._normalized_count = None
        self.discriminator = None
        if base_image_digest is not None:
            self.base_image_digest = base_image_digest
        if base_image_name is not None:
            self.base_image_name = base_image_name
        if base_image_tag is not None:
            self.base_image_tag = base_image_tag
        if deduplicated_count is not None:
            self.deduplicated_count = deduplicated_count
        if image_domain is not None:
            self.image_domain = image_domain
        if image_name is not None:
            self.image_name = image_name
        if image_tag is not None:
            self.image_tag = image_tag
        if normalized_count is not None:
            self.normalized_count = normalized_count

    @property
    def base_image_digest(self):
        """Gets the base_image_digest of this ScanMetadata.  # noqa: E501

        Digest of the base image  # noqa: E501

        :return: The base_image_digest of this ScanMetadata.  # noqa: E501
        :rtype: str
        """
        return self._base_image_digest

    @base_image_digest.setter
    def base_image_digest(self, base_image_digest):
        """Sets the base_image_digest of this ScanMetadata.

        Digest of the base image  # noqa: E501

        :param base_image_digest: The base_image_digest of this ScanMetadata.  # noqa: E501
        :type: str
        """

        self._base_image_digest = base_image_digest

    @property
    def base_image_name(self):
        """Gets the base_image_name of this ScanMetadata.  # noqa: E501

        Name of the base image  # noqa: E501

        :return: The base_image_name of this ScanMetadata.  # noqa: E501
        :rtype: str
        """
        return self._base_image_name

    @base_image_name.setter
    def base_image_name(self, base_image_name):
        """Sets the base_image_name of this ScanMetadata.

        Name of the base image  # noqa: E501

        :param base_image_name: The base_image_name of this ScanMetadata.  # noqa: E501
        :type: str
        """

        self._base_image_name = base_image_name

    @property
    def base_image_tag(self):
        """Gets the base_image_tag of this ScanMetadata.  # noqa: E501

        Tag of the base image  # noqa: E501

        :return: The base_image_tag of this ScanMetadata.  # noqa: E501
        :rtype: str
        """
        return self._base_image_tag

    @base_image_tag.setter
    def base_image_tag(self, base_image_tag):
        """Sets the base_image_tag of this ScanMetadata.

        Tag of the base image  # noqa: E501

        :param base_image_tag: The base_image_tag of this ScanMetadata.  # noqa: E501
        :type: str
        """

        self._base_image_tag = base_image_tag

    @property
    def deduplicated_count(self):
        """Gets the deduplicated_count of this ScanMetadata.  # noqa: E501

        Total number of deduplicated issues found in the scan  # noqa: E501

        :return: The deduplicated_count of this ScanMetadata.  # noqa: E501
        :rtype: int
        """
        return self._deduplicated_count

    @deduplicated_count.setter
    def deduplicated_count(self, deduplicated_count):
        """Sets the deduplicated_count of this ScanMetadata.

        Total number of deduplicated issues found in the scan  # noqa: E501

        :param deduplicated_count: The deduplicated_count of this ScanMetadata.  # noqa: E501
        :type: int
        """

        self._deduplicated_count = deduplicated_count

    @property
    def image_domain(self):
        """Gets the image_domain of this ScanMetadata.  # noqa: E501

        Domain of the container image registry  # noqa: E501

        :return: The image_domain of this ScanMetadata.  # noqa: E501
        :rtype: str
        """
        return self._image_domain

    @image_domain.setter
    def image_domain(self, image_domain):
        """Sets the image_domain of this ScanMetadata.

        Domain of the container image registry  # noqa: E501

        :param image_domain: The image_domain of this ScanMetadata.  # noqa: E501
        :type: str
        """

        self._image_domain = image_domain

    @property
    def image_name(self):
        """Gets the image_name of this ScanMetadata.  # noqa: E501

        Name of the container image  # noqa: E501

        :return: The image_name of this ScanMetadata.  # noqa: E501
        :rtype: str
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name):
        """Sets the image_name of this ScanMetadata.

        Name of the container image  # noqa: E501

        :param image_name: The image_name of this ScanMetadata.  # noqa: E501
        :type: str
        """

        self._image_name = image_name

    @property
    def image_tag(self):
        """Gets the image_tag of this ScanMetadata.  # noqa: E501

        Tag of the container image  # noqa: E501

        :return: The image_tag of this ScanMetadata.  # noqa: E501
        :rtype: str
        """
        return self._image_tag

    @image_tag.setter
    def image_tag(self, image_tag):
        """Sets the image_tag of this ScanMetadata.

        Tag of the container image  # noqa: E501

        :param image_tag: The image_tag of this ScanMetadata.  # noqa: E501
        :type: str
        """

        self._image_tag = image_tag

    @property
    def normalized_count(self):
        """Gets the normalized_count of this ScanMetadata.  # noqa: E501

        Total number of normalized issues found in the scan  # noqa: E501

        :return: The normalized_count of this ScanMetadata.  # noqa: E501
        :rtype: int
        """
        return self._normalized_count

    @normalized_count.setter
    def normalized_count(self, normalized_count):
        """Sets the normalized_count of this ScanMetadata.

        Total number of normalized issues found in the scan  # noqa: E501

        :param normalized_count: The normalized_count of this ScanMetadata.  # noqa: E501
        :type: int
        """

        self._normalized_count = normalized_count

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
        if issubclass(ScanMetadata, dict):
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
        if not isinstance(other, ScanMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
