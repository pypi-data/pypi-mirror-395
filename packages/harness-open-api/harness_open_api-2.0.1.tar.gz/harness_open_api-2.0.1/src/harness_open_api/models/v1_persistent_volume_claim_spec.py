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

class V1PersistentVolumeClaimSpec(object):
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
        'access_modes': 'list[str]',
        'data_source': 'V1TypedLocalObjectReference',
        'data_source_ref': 'V1TypedObjectReference',
        'resources': 'V1VolumeResourceRequirements',
        'selector': 'V1LabelSelector',
        'storage_class_name': 'str',
        'volume_attributes_class_name': 'str',
        'volume_mode': 'str',
        'volume_name': 'str'
    }

    attribute_map = {
        'access_modes': 'accessModes',
        'data_source': 'dataSource',
        'data_source_ref': 'dataSourceRef',
        'resources': 'resources',
        'selector': 'selector',
        'storage_class_name': 'storageClassName',
        'volume_attributes_class_name': 'volumeAttributesClassName',
        'volume_mode': 'volumeMode',
        'volume_name': 'volumeName'
    }

    def __init__(self, access_modes=None, data_source=None, data_source_ref=None, resources=None, selector=None, storage_class_name=None, volume_attributes_class_name=None, volume_mode=None, volume_name=None):  # noqa: E501
        """V1PersistentVolumeClaimSpec - a model defined in Swagger"""  # noqa: E501
        self._access_modes = None
        self._data_source = None
        self._data_source_ref = None
        self._resources = None
        self._selector = None
        self._storage_class_name = None
        self._volume_attributes_class_name = None
        self._volume_mode = None
        self._volume_name = None
        self.discriminator = None
        if access_modes is not None:
            self.access_modes = access_modes
        if data_source is not None:
            self.data_source = data_source
        if data_source_ref is not None:
            self.data_source_ref = data_source_ref
        if resources is not None:
            self.resources = resources
        if selector is not None:
            self.selector = selector
        if storage_class_name is not None:
            self.storage_class_name = storage_class_name
        if volume_attributes_class_name is not None:
            self.volume_attributes_class_name = volume_attributes_class_name
        if volume_mode is not None:
            self.volume_mode = volume_mode
        if volume_name is not None:
            self.volume_name = volume_name

    @property
    def access_modes(self):
        """Gets the access_modes of this V1PersistentVolumeClaimSpec.  # noqa: E501


        :return: The access_modes of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :rtype: list[str]
        """
        return self._access_modes

    @access_modes.setter
    def access_modes(self, access_modes):
        """Sets the access_modes of this V1PersistentVolumeClaimSpec.


        :param access_modes: The access_modes of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :type: list[str]
        """

        self._access_modes = access_modes

    @property
    def data_source(self):
        """Gets the data_source of this V1PersistentVolumeClaimSpec.  # noqa: E501


        :return: The data_source of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :rtype: V1TypedLocalObjectReference
        """
        return self._data_source

    @data_source.setter
    def data_source(self, data_source):
        """Sets the data_source of this V1PersistentVolumeClaimSpec.


        :param data_source: The data_source of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :type: V1TypedLocalObjectReference
        """

        self._data_source = data_source

    @property
    def data_source_ref(self):
        """Gets the data_source_ref of this V1PersistentVolumeClaimSpec.  # noqa: E501


        :return: The data_source_ref of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :rtype: V1TypedObjectReference
        """
        return self._data_source_ref

    @data_source_ref.setter
    def data_source_ref(self, data_source_ref):
        """Sets the data_source_ref of this V1PersistentVolumeClaimSpec.


        :param data_source_ref: The data_source_ref of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :type: V1TypedObjectReference
        """

        self._data_source_ref = data_source_ref

    @property
    def resources(self):
        """Gets the resources of this V1PersistentVolumeClaimSpec.  # noqa: E501


        :return: The resources of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :rtype: V1VolumeResourceRequirements
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this V1PersistentVolumeClaimSpec.


        :param resources: The resources of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :type: V1VolumeResourceRequirements
        """

        self._resources = resources

    @property
    def selector(self):
        """Gets the selector of this V1PersistentVolumeClaimSpec.  # noqa: E501


        :return: The selector of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :rtype: V1LabelSelector
        """
        return self._selector

    @selector.setter
    def selector(self, selector):
        """Sets the selector of this V1PersistentVolumeClaimSpec.


        :param selector: The selector of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :type: V1LabelSelector
        """

        self._selector = selector

    @property
    def storage_class_name(self):
        """Gets the storage_class_name of this V1PersistentVolumeClaimSpec.  # noqa: E501


        :return: The storage_class_name of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :rtype: str
        """
        return self._storage_class_name

    @storage_class_name.setter
    def storage_class_name(self, storage_class_name):
        """Sets the storage_class_name of this V1PersistentVolumeClaimSpec.


        :param storage_class_name: The storage_class_name of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :type: str
        """

        self._storage_class_name = storage_class_name

    @property
    def volume_attributes_class_name(self):
        """Gets the volume_attributes_class_name of this V1PersistentVolumeClaimSpec.  # noqa: E501


        :return: The volume_attributes_class_name of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :rtype: str
        """
        return self._volume_attributes_class_name

    @volume_attributes_class_name.setter
    def volume_attributes_class_name(self, volume_attributes_class_name):
        """Sets the volume_attributes_class_name of this V1PersistentVolumeClaimSpec.


        :param volume_attributes_class_name: The volume_attributes_class_name of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :type: str
        """

        self._volume_attributes_class_name = volume_attributes_class_name

    @property
    def volume_mode(self):
        """Gets the volume_mode of this V1PersistentVolumeClaimSpec.  # noqa: E501


        :return: The volume_mode of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :rtype: str
        """
        return self._volume_mode

    @volume_mode.setter
    def volume_mode(self, volume_mode):
        """Sets the volume_mode of this V1PersistentVolumeClaimSpec.


        :param volume_mode: The volume_mode of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :type: str
        """

        self._volume_mode = volume_mode

    @property
    def volume_name(self):
        """Gets the volume_name of this V1PersistentVolumeClaimSpec.  # noqa: E501


        :return: The volume_name of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :rtype: str
        """
        return self._volume_name

    @volume_name.setter
    def volume_name(self, volume_name):
        """Sets the volume_name of this V1PersistentVolumeClaimSpec.


        :param volume_name: The volume_name of this V1PersistentVolumeClaimSpec.  # noqa: E501
        :type: str
        """

        self._volume_name = volume_name

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
        if issubclass(V1PersistentVolumeClaimSpec, dict):
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
        if not isinstance(other, V1PersistentVolumeClaimSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
