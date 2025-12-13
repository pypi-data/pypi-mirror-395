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

class PolicyViolation(object):
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
        'account': 'str',
        'artifact_id': 'str',
        'enforcement_id': 'str',
        'exemption_id': 'str',
        'filter_tags': 'list[LayerType]',
        'image_name': 'str',
        'is_exempted': 'bool',
        'language': 'str',
        'license': 'list[str]',
        'name': 'str',
        'orchestration_id': 'str',
        'org': 'str',
        'package_manager': 'str',
        'project': 'str',
        'purl': 'str',
        'supplier': 'str',
        'supplier_type': 'str',
        'tag': 'str',
        'version': 'str',
        'violation_details': 'str',
        'violation_type': 'str'
    }

    attribute_map = {
        'account': 'account',
        'artifact_id': 'artifact_id',
        'enforcement_id': 'enforcement_id',
        'exemption_id': 'exemption_id',
        'filter_tags': 'filter_tags',
        'image_name': 'image_name',
        'is_exempted': 'is_exempted',
        'language': 'language',
        'license': 'license',
        'name': 'name',
        'orchestration_id': 'orchestration_id',
        'org': 'org',
        'package_manager': 'package_manager',
        'project': 'project',
        'purl': 'purl',
        'supplier': 'supplier',
        'supplier_type': 'supplier_type',
        'tag': 'tag',
        'version': 'version',
        'violation_details': 'violation_details',
        'violation_type': 'violation_type'
    }

    def __init__(self, account=None, artifact_id=None, enforcement_id=None, exemption_id=None, filter_tags=None, image_name=None, is_exempted=None, language=None, license=None, name=None, orchestration_id=None, org=None, package_manager=None, project=None, purl=None, supplier=None, supplier_type=None, tag=None, version=None, violation_details=None, violation_type=None):  # noqa: E501
        """PolicyViolation - a model defined in Swagger"""  # noqa: E501
        self._account = None
        self._artifact_id = None
        self._enforcement_id = None
        self._exemption_id = None
        self._filter_tags = None
        self._image_name = None
        self._is_exempted = None
        self._language = None
        self._license = None
        self._name = None
        self._orchestration_id = None
        self._org = None
        self._package_manager = None
        self._project = None
        self._purl = None
        self._supplier = None
        self._supplier_type = None
        self._tag = None
        self._version = None
        self._violation_details = None
        self._violation_type = None
        self.discriminator = None
        if account is not None:
            self.account = account
        if artifact_id is not None:
            self.artifact_id = artifact_id
        if enforcement_id is not None:
            self.enforcement_id = enforcement_id
        if exemption_id is not None:
            self.exemption_id = exemption_id
        if filter_tags is not None:
            self.filter_tags = filter_tags
        if image_name is not None:
            self.image_name = image_name
        if is_exempted is not None:
            self.is_exempted = is_exempted
        if language is not None:
            self.language = language
        if license is not None:
            self.license = license
        if name is not None:
            self.name = name
        if orchestration_id is not None:
            self.orchestration_id = orchestration_id
        if org is not None:
            self.org = org
        if package_manager is not None:
            self.package_manager = package_manager
        if project is not None:
            self.project = project
        if purl is not None:
            self.purl = purl
        if supplier is not None:
            self.supplier = supplier
        if supplier_type is not None:
            self.supplier_type = supplier_type
        if tag is not None:
            self.tag = tag
        if version is not None:
            self.version = version
        if violation_details is not None:
            self.violation_details = violation_details
        if violation_type is not None:
            self.violation_type = violation_type

    @property
    def account(self):
        """Gets the account of this PolicyViolation.  # noqa: E501


        :return: The account of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this PolicyViolation.


        :param account: The account of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._account = account

    @property
    def artifact_id(self):
        """Gets the artifact_id of this PolicyViolation.  # noqa: E501


        :return: The artifact_id of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._artifact_id

    @artifact_id.setter
    def artifact_id(self, artifact_id):
        """Sets the artifact_id of this PolicyViolation.


        :param artifact_id: The artifact_id of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._artifact_id = artifact_id

    @property
    def enforcement_id(self):
        """Gets the enforcement_id of this PolicyViolation.  # noqa: E501


        :return: The enforcement_id of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._enforcement_id

    @enforcement_id.setter
    def enforcement_id(self, enforcement_id):
        """Sets the enforcement_id of this PolicyViolation.


        :param enforcement_id: The enforcement_id of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._enforcement_id = enforcement_id

    @property
    def exemption_id(self):
        """Gets the exemption_id of this PolicyViolation.  # noqa: E501


        :return: The exemption_id of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._exemption_id

    @exemption_id.setter
    def exemption_id(self, exemption_id):
        """Sets the exemption_id of this PolicyViolation.


        :param exemption_id: The exemption_id of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._exemption_id = exemption_id

    @property
    def filter_tags(self):
        """Gets the filter_tags of this PolicyViolation.  # noqa: E501


        :return: The filter_tags of this PolicyViolation.  # noqa: E501
        :rtype: list[LayerType]
        """
        return self._filter_tags

    @filter_tags.setter
    def filter_tags(self, filter_tags):
        """Sets the filter_tags of this PolicyViolation.


        :param filter_tags: The filter_tags of this PolicyViolation.  # noqa: E501
        :type: list[LayerType]
        """

        self._filter_tags = filter_tags

    @property
    def image_name(self):
        """Gets the image_name of this PolicyViolation.  # noqa: E501


        :return: The image_name of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name):
        """Sets the image_name of this PolicyViolation.


        :param image_name: The image_name of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._image_name = image_name

    @property
    def is_exempted(self):
        """Gets the is_exempted of this PolicyViolation.  # noqa: E501


        :return: The is_exempted of this PolicyViolation.  # noqa: E501
        :rtype: bool
        """
        return self._is_exempted

    @is_exempted.setter
    def is_exempted(self, is_exempted):
        """Sets the is_exempted of this PolicyViolation.


        :param is_exempted: The is_exempted of this PolicyViolation.  # noqa: E501
        :type: bool
        """

        self._is_exempted = is_exempted

    @property
    def language(self):
        """Gets the language of this PolicyViolation.  # noqa: E501


        :return: The language of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this PolicyViolation.


        :param language: The language of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._language = language

    @property
    def license(self):
        """Gets the license of this PolicyViolation.  # noqa: E501


        :return: The license of this PolicyViolation.  # noqa: E501
        :rtype: list[str]
        """
        return self._license

    @license.setter
    def license(self, license):
        """Sets the license of this PolicyViolation.


        :param license: The license of this PolicyViolation.  # noqa: E501
        :type: list[str]
        """

        self._license = license

    @property
    def name(self):
        """Gets the name of this PolicyViolation.  # noqa: E501


        :return: The name of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PolicyViolation.


        :param name: The name of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def orchestration_id(self):
        """Gets the orchestration_id of this PolicyViolation.  # noqa: E501


        :return: The orchestration_id of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._orchestration_id

    @orchestration_id.setter
    def orchestration_id(self, orchestration_id):
        """Sets the orchestration_id of this PolicyViolation.


        :param orchestration_id: The orchestration_id of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._orchestration_id = orchestration_id

    @property
    def org(self):
        """Gets the org of this PolicyViolation.  # noqa: E501


        :return: The org of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._org

    @org.setter
    def org(self, org):
        """Sets the org of this PolicyViolation.


        :param org: The org of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._org = org

    @property
    def package_manager(self):
        """Gets the package_manager of this PolicyViolation.  # noqa: E501


        :return: The package_manager of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._package_manager

    @package_manager.setter
    def package_manager(self, package_manager):
        """Sets the package_manager of this PolicyViolation.


        :param package_manager: The package_manager of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._package_manager = package_manager

    @property
    def project(self):
        """Gets the project of this PolicyViolation.  # noqa: E501


        :return: The project of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this PolicyViolation.


        :param project: The project of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._project = project

    @property
    def purl(self):
        """Gets the purl of this PolicyViolation.  # noqa: E501


        :return: The purl of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._purl

    @purl.setter
    def purl(self, purl):
        """Sets the purl of this PolicyViolation.


        :param purl: The purl of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._purl = purl

    @property
    def supplier(self):
        """Gets the supplier of this PolicyViolation.  # noqa: E501


        :return: The supplier of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._supplier

    @supplier.setter
    def supplier(self, supplier):
        """Sets the supplier of this PolicyViolation.


        :param supplier: The supplier of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._supplier = supplier

    @property
    def supplier_type(self):
        """Gets the supplier_type of this PolicyViolation.  # noqa: E501


        :return: The supplier_type of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._supplier_type

    @supplier_type.setter
    def supplier_type(self, supplier_type):
        """Sets the supplier_type of this PolicyViolation.


        :param supplier_type: The supplier_type of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._supplier_type = supplier_type

    @property
    def tag(self):
        """Gets the tag of this PolicyViolation.  # noqa: E501


        :return: The tag of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """Sets the tag of this PolicyViolation.


        :param tag: The tag of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._tag = tag

    @property
    def version(self):
        """Gets the version of this PolicyViolation.  # noqa: E501


        :return: The version of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this PolicyViolation.


        :param version: The version of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def violation_details(self):
        """Gets the violation_details of this PolicyViolation.  # noqa: E501


        :return: The violation_details of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._violation_details

    @violation_details.setter
    def violation_details(self, violation_details):
        """Sets the violation_details of this PolicyViolation.


        :param violation_details: The violation_details of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._violation_details = violation_details

    @property
    def violation_type(self):
        """Gets the violation_type of this PolicyViolation.  # noqa: E501


        :return: The violation_type of this PolicyViolation.  # noqa: E501
        :rtype: str
        """
        return self._violation_type

    @violation_type.setter
    def violation_type(self, violation_type):
        """Sets the violation_type of this PolicyViolation.


        :param violation_type: The violation_type of this PolicyViolation.  # noqa: E501
        :type: str
        """

        self._violation_type = violation_type

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
        if issubclass(PolicyViolation, dict):
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
        if not isinstance(other, PolicyViolation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
