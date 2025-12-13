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

class StoTarget(object):
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
        'baseline_reg_ex': 'str',
        'baseline_variant_id': 'str',
        'created': 'int',
        'directory': 'str',
        'id': 'str',
        'last_modified': 'int',
        'name': 'str',
        'org_id': 'str',
        'project_id': 'str',
        'type': 'str',
        'url': 'str'
    }

    attribute_map = {
        'baseline_reg_ex': 'baselineRegEx',
        'baseline_variant_id': 'baselineVariantId',
        'created': 'created',
        'directory': 'directory',
        'id': 'id',
        'last_modified': 'lastModified',
        'name': 'name',
        'org_id': 'orgId',
        'project_id': 'projectId',
        'type': 'type',
        'url': 'url'
    }

    def __init__(self, baseline_reg_ex=None, baseline_variant_id=None, created=None, directory=None, id=None, last_modified=None, name=None, org_id=None, project_id=None, type=None, url=None):  # noqa: E501
        """StoTarget - a model defined in Swagger"""  # noqa: E501
        self._baseline_reg_ex = None
        self._baseline_variant_id = None
        self._created = None
        self._directory = None
        self._id = None
        self._last_modified = None
        self._name = None
        self._org_id = None
        self._project_id = None
        self._type = None
        self._url = None
        self.discriminator = None
        if baseline_reg_ex is not None:
            self.baseline_reg_ex = baseline_reg_ex
        if baseline_variant_id is not None:
            self.baseline_variant_id = baseline_variant_id
        self.created = created
        if directory is not None:
            self.directory = directory
        self.id = id
        self.last_modified = last_modified
        self.name = name
        self.org_id = org_id
        self.project_id = project_id
        self.type = type
        if url is not None:
            self.url = url

    @property
    def baseline_reg_ex(self):
        """Gets the baseline_reg_ex of this StoTarget.  # noqa: E501

        RegEx to match for dynamically selecting the Baseline for this Scan Target. Must be compatible with the RE2 standard.  # noqa: E501

        :return: The baseline_reg_ex of this StoTarget.  # noqa: E501
        :rtype: str
        """
        return self._baseline_reg_ex

    @baseline_reg_ex.setter
    def baseline_reg_ex(self, baseline_reg_ex):
        """Sets the baseline_reg_ex of this StoTarget.

        RegEx to match for dynamically selecting the Baseline for this Scan Target. Must be compatible with the RE2 standard.  # noqa: E501

        :param baseline_reg_ex: The baseline_reg_ex of this StoTarget.  # noqa: E501
        :type: str
        """

        self._baseline_reg_ex = baseline_reg_ex

    @property
    def baseline_variant_id(self):
        """Gets the baseline_variant_id of this StoTarget.  # noqa: E501

        ID of baseline Target Variant for Issue comparison  # noqa: E501

        :return: The baseline_variant_id of this StoTarget.  # noqa: E501
        :rtype: str
        """
        return self._baseline_variant_id

    @baseline_variant_id.setter
    def baseline_variant_id(self, baseline_variant_id):
        """Sets the baseline_variant_id of this StoTarget.

        ID of baseline Target Variant for Issue comparison  # noqa: E501

        :param baseline_variant_id: The baseline_variant_id of this StoTarget.  # noqa: E501
        :type: str
        """

        self._baseline_variant_id = baseline_variant_id

    @property
    def created(self):
        """Gets the created of this StoTarget.  # noqa: E501

        Unix timestamp at which the resource was created  # noqa: E501

        :return: The created of this StoTarget.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this StoTarget.

        Unix timestamp at which the resource was created  # noqa: E501

        :param created: The created of this StoTarget.  # noqa: E501
        :type: int
        """
        if created is None:
            raise ValueError("Invalid value for `created`, must not be `None`")  # noqa: E501

        self._created = created

    @property
    def directory(self):
        """Gets the directory of this StoTarget.  # noqa: E501

        Directory within the Test Target to be scanned  # noqa: E501

        :return: The directory of this StoTarget.  # noqa: E501
        :rtype: str
        """
        return self._directory

    @directory.setter
    def directory(self, directory):
        """Sets the directory of this StoTarget.

        Directory within the Test Target to be scanned  # noqa: E501

        :param directory: The directory of this StoTarget.  # noqa: E501
        :type: str
        """

        self._directory = directory

    @property
    def id(self):
        """Gets the id of this StoTarget.  # noqa: E501

        Resource identifier  # noqa: E501

        :return: The id of this StoTarget.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this StoTarget.

        Resource identifier  # noqa: E501

        :param id: The id of this StoTarget.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def last_modified(self):
        """Gets the last_modified of this StoTarget.  # noqa: E501

        Unix timestamp at which the resource was most recently modified  # noqa: E501

        :return: The last_modified of this StoTarget.  # noqa: E501
        :rtype: int
        """
        return self._last_modified

    @last_modified.setter
    def last_modified(self, last_modified):
        """Sets the last_modified of this StoTarget.

        Unix timestamp at which the resource was most recently modified  # noqa: E501

        :param last_modified: The last_modified of this StoTarget.  # noqa: E501
        :type: int
        """
        if last_modified is None:
            raise ValueError("Invalid value for `last_modified`, must not be `None`")  # noqa: E501

        self._last_modified = last_modified

    @property
    def name(self):
        """Gets the name of this StoTarget.  # noqa: E501

        Name of the Test Target  # noqa: E501

        :return: The name of this StoTarget.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this StoTarget.

        Name of the Test Target  # noqa: E501

        :param name: The name of this StoTarget.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def org_id(self):
        """Gets the org_id of this StoTarget.  # noqa: E501

        Harness Organization ID  # noqa: E501

        :return: The org_id of this StoTarget.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Sets the org_id of this StoTarget.

        Harness Organization ID  # noqa: E501

        :param org_id: The org_id of this StoTarget.  # noqa: E501
        :type: str
        """
        if org_id is None:
            raise ValueError("Invalid value for `org_id`, must not be `None`")  # noqa: E501

        self._org_id = org_id

    @property
    def project_id(self):
        """Gets the project_id of this StoTarget.  # noqa: E501

        Harness Project ID  # noqa: E501

        :return: The project_id of this StoTarget.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this StoTarget.

        Harness Project ID  # noqa: E501

        :param project_id: The project_id of this StoTarget.  # noqa: E501
        :type: str
        """
        if project_id is None:
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def type(self):
        """Gets the type of this StoTarget.  # noqa: E501

        Test Target's type  # noqa: E501

        :return: The type of this StoTarget.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this StoTarget.

        Test Target's type  # noqa: E501

        :param type: The type of this StoTarget.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["container", "repository", "instance", "configuration"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def url(self):
        """Gets the url of this StoTarget.  # noqa: E501

        URL used to access the Test Target  # noqa: E501

        :return: The url of this StoTarget.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this StoTarget.

        URL used to access the Test Target  # noqa: E501

        :param url: The url of this StoTarget.  # noqa: E501
        :type: str
        """

        self._url = url

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
        if issubclass(StoTarget, dict):
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
        if not isinstance(other, StoTarget):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
