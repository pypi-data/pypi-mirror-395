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

class SbomComponentRequestDTO(object):
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
        'filter_tags': 'list[LayerType]',
        'language': 'str',
        'major_version': 'float',
        'minor_version': 'float',
        'originator_type': 'str',
        'package_cpe': 'str',
        'package_description': 'str',
        'package_id': 'str',
        'package_license': 'list[str]',
        'package_manager': 'str',
        'package_name': 'str',
        'package_namespace': 'str',
        'package_originator_name': 'str',
        'package_properties': 'str',
        'package_source_info': 'str',
        'package_type': 'str',
        'package_version': 'str',
        'patch_version': 'float',
        'purl': 'str',
        'tags': 'list[str]'
    }

    attribute_map = {
        'filter_tags': 'filter_tags',
        'language': 'language',
        'major_version': 'major_version',
        'minor_version': 'minor_version',
        'originator_type': 'originator_type',
        'package_cpe': 'package_cpe',
        'package_description': 'package_description',
        'package_id': 'package_id',
        'package_license': 'package_license',
        'package_manager': 'package_manager',
        'package_name': 'package_name',
        'package_namespace': 'package_namespace',
        'package_originator_name': 'package_originator_name',
        'package_properties': 'package_properties',
        'package_source_info': 'package_source_info',
        'package_type': 'package_type',
        'package_version': 'package_version',
        'patch_version': 'patch_version',
        'purl': 'purl',
        'tags': 'tags'
    }

    def __init__(self, filter_tags=None, language=None, major_version=None, minor_version=None, originator_type=None, package_cpe=None, package_description=None, package_id=None, package_license=None, package_manager=None, package_name=None, package_namespace=None, package_originator_name=None, package_properties=None, package_source_info=None, package_type=None, package_version=None, patch_version=None, purl=None, tags=None):  # noqa: E501
        """SbomComponentRequestDTO - a model defined in Swagger"""  # noqa: E501
        self._filter_tags = None
        self._language = None
        self._major_version = None
        self._minor_version = None
        self._originator_type = None
        self._package_cpe = None
        self._package_description = None
        self._package_id = None
        self._package_license = None
        self._package_manager = None
        self._package_name = None
        self._package_namespace = None
        self._package_originator_name = None
        self._package_properties = None
        self._package_source_info = None
        self._package_type = None
        self._package_version = None
        self._patch_version = None
        self._purl = None
        self._tags = None
        self.discriminator = None
        if filter_tags is not None:
            self.filter_tags = filter_tags
        if language is not None:
            self.language = language
        if major_version is not None:
            self.major_version = major_version
        if minor_version is not None:
            self.minor_version = minor_version
        if originator_type is not None:
            self.originator_type = originator_type
        if package_cpe is not None:
            self.package_cpe = package_cpe
        if package_description is not None:
            self.package_description = package_description
        if package_id is not None:
            self.package_id = package_id
        if package_license is not None:
            self.package_license = package_license
        if package_manager is not None:
            self.package_manager = package_manager
        if package_name is not None:
            self.package_name = package_name
        if package_namespace is not None:
            self.package_namespace = package_namespace
        if package_originator_name is not None:
            self.package_originator_name = package_originator_name
        if package_properties is not None:
            self.package_properties = package_properties
        if package_source_info is not None:
            self.package_source_info = package_source_info
        if package_type is not None:
            self.package_type = package_type
        if package_version is not None:
            self.package_version = package_version
        if patch_version is not None:
            self.patch_version = patch_version
        if purl is not None:
            self.purl = purl
        if tags is not None:
            self.tags = tags

    @property
    def filter_tags(self):
        """Gets the filter_tags of this SbomComponentRequestDTO.  # noqa: E501


        :return: The filter_tags of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: list[LayerType]
        """
        return self._filter_tags

    @filter_tags.setter
    def filter_tags(self, filter_tags):
        """Sets the filter_tags of this SbomComponentRequestDTO.


        :param filter_tags: The filter_tags of this SbomComponentRequestDTO.  # noqa: E501
        :type: list[LayerType]
        """

        self._filter_tags = filter_tags

    @property
    def language(self):
        """Gets the language of this SbomComponentRequestDTO.  # noqa: E501


        :return: The language of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this SbomComponentRequestDTO.


        :param language: The language of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._language = language

    @property
    def major_version(self):
        """Gets the major_version of this SbomComponentRequestDTO.  # noqa: E501


        :return: The major_version of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: float
        """
        return self._major_version

    @major_version.setter
    def major_version(self, major_version):
        """Sets the major_version of this SbomComponentRequestDTO.


        :param major_version: The major_version of this SbomComponentRequestDTO.  # noqa: E501
        :type: float
        """

        self._major_version = major_version

    @property
    def minor_version(self):
        """Gets the minor_version of this SbomComponentRequestDTO.  # noqa: E501


        :return: The minor_version of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: float
        """
        return self._minor_version

    @minor_version.setter
    def minor_version(self, minor_version):
        """Sets the minor_version of this SbomComponentRequestDTO.


        :param minor_version: The minor_version of this SbomComponentRequestDTO.  # noqa: E501
        :type: float
        """

        self._minor_version = minor_version

    @property
    def originator_type(self):
        """Gets the originator_type of this SbomComponentRequestDTO.  # noqa: E501


        :return: The originator_type of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._originator_type

    @originator_type.setter
    def originator_type(self, originator_type):
        """Sets the originator_type of this SbomComponentRequestDTO.


        :param originator_type: The originator_type of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._originator_type = originator_type

    @property
    def package_cpe(self):
        """Gets the package_cpe of this SbomComponentRequestDTO.  # noqa: E501


        :return: The package_cpe of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._package_cpe

    @package_cpe.setter
    def package_cpe(self, package_cpe):
        """Sets the package_cpe of this SbomComponentRequestDTO.


        :param package_cpe: The package_cpe of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._package_cpe = package_cpe

    @property
    def package_description(self):
        """Gets the package_description of this SbomComponentRequestDTO.  # noqa: E501


        :return: The package_description of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._package_description

    @package_description.setter
    def package_description(self, package_description):
        """Sets the package_description of this SbomComponentRequestDTO.


        :param package_description: The package_description of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._package_description = package_description

    @property
    def package_id(self):
        """Gets the package_id of this SbomComponentRequestDTO.  # noqa: E501


        :return: The package_id of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._package_id

    @package_id.setter
    def package_id(self, package_id):
        """Sets the package_id of this SbomComponentRequestDTO.


        :param package_id: The package_id of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._package_id = package_id

    @property
    def package_license(self):
        """Gets the package_license of this SbomComponentRequestDTO.  # noqa: E501


        :return: The package_license of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._package_license

    @package_license.setter
    def package_license(self, package_license):
        """Sets the package_license of this SbomComponentRequestDTO.


        :param package_license: The package_license of this SbomComponentRequestDTO.  # noqa: E501
        :type: list[str]
        """

        self._package_license = package_license

    @property
    def package_manager(self):
        """Gets the package_manager of this SbomComponentRequestDTO.  # noqa: E501


        :return: The package_manager of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._package_manager

    @package_manager.setter
    def package_manager(self, package_manager):
        """Sets the package_manager of this SbomComponentRequestDTO.


        :param package_manager: The package_manager of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._package_manager = package_manager

    @property
    def package_name(self):
        """Gets the package_name of this SbomComponentRequestDTO.  # noqa: E501


        :return: The package_name of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._package_name

    @package_name.setter
    def package_name(self, package_name):
        """Sets the package_name of this SbomComponentRequestDTO.


        :param package_name: The package_name of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._package_name = package_name

    @property
    def package_namespace(self):
        """Gets the package_namespace of this SbomComponentRequestDTO.  # noqa: E501


        :return: The package_namespace of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._package_namespace

    @package_namespace.setter
    def package_namespace(self, package_namespace):
        """Sets the package_namespace of this SbomComponentRequestDTO.


        :param package_namespace: The package_namespace of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._package_namespace = package_namespace

    @property
    def package_originator_name(self):
        """Gets the package_originator_name of this SbomComponentRequestDTO.  # noqa: E501


        :return: The package_originator_name of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._package_originator_name

    @package_originator_name.setter
    def package_originator_name(self, package_originator_name):
        """Sets the package_originator_name of this SbomComponentRequestDTO.


        :param package_originator_name: The package_originator_name of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._package_originator_name = package_originator_name

    @property
    def package_properties(self):
        """Gets the package_properties of this SbomComponentRequestDTO.  # noqa: E501


        :return: The package_properties of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._package_properties

    @package_properties.setter
    def package_properties(self, package_properties):
        """Sets the package_properties of this SbomComponentRequestDTO.


        :param package_properties: The package_properties of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._package_properties = package_properties

    @property
    def package_source_info(self):
        """Gets the package_source_info of this SbomComponentRequestDTO.  # noqa: E501


        :return: The package_source_info of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._package_source_info

    @package_source_info.setter
    def package_source_info(self, package_source_info):
        """Sets the package_source_info of this SbomComponentRequestDTO.


        :param package_source_info: The package_source_info of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._package_source_info = package_source_info

    @property
    def package_type(self):
        """Gets the package_type of this SbomComponentRequestDTO.  # noqa: E501


        :return: The package_type of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._package_type

    @package_type.setter
    def package_type(self, package_type):
        """Sets the package_type of this SbomComponentRequestDTO.


        :param package_type: The package_type of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._package_type = package_type

    @property
    def package_version(self):
        """Gets the package_version of this SbomComponentRequestDTO.  # noqa: E501


        :return: The package_version of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._package_version

    @package_version.setter
    def package_version(self, package_version):
        """Sets the package_version of this SbomComponentRequestDTO.


        :param package_version: The package_version of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._package_version = package_version

    @property
    def patch_version(self):
        """Gets the patch_version of this SbomComponentRequestDTO.  # noqa: E501


        :return: The patch_version of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: float
        """
        return self._patch_version

    @patch_version.setter
    def patch_version(self, patch_version):
        """Sets the patch_version of this SbomComponentRequestDTO.


        :param patch_version: The patch_version of this SbomComponentRequestDTO.  # noqa: E501
        :type: float
        """

        self._patch_version = patch_version

    @property
    def purl(self):
        """Gets the purl of this SbomComponentRequestDTO.  # noqa: E501


        :return: The purl of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: str
        """
        return self._purl

    @purl.setter
    def purl(self, purl):
        """Sets the purl of this SbomComponentRequestDTO.


        :param purl: The purl of this SbomComponentRequestDTO.  # noqa: E501
        :type: str
        """

        self._purl = purl

    @property
    def tags(self):
        """Gets the tags of this SbomComponentRequestDTO.  # noqa: E501


        :return: The tags of this SbomComponentRequestDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this SbomComponentRequestDTO.


        :param tags: The tags of this SbomComponentRequestDTO.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

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
        if issubclass(SbomComponentRequestDTO, dict):
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
        if not isinstance(other, SbomComponentRequestDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
