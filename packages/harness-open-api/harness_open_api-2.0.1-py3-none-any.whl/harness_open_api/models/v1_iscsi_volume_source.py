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

class V1ISCSIVolumeSource(object):
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
        'chap_auth_discovery': 'bool',
        'chap_auth_session': 'bool',
        'fs_type': 'str',
        'initiator_name': 'str',
        'iqn': 'str',
        'iscsi_interface': 'str',
        'lun': 'int',
        'portals': 'list[str]',
        'read_only': 'bool',
        'secret_ref': 'V1LocalObjectReference',
        'target_portal': 'str'
    }

    attribute_map = {
        'chap_auth_discovery': 'chapAuthDiscovery',
        'chap_auth_session': 'chapAuthSession',
        'fs_type': 'fsType',
        'initiator_name': 'initiatorName',
        'iqn': 'iqn',
        'iscsi_interface': 'iscsiInterface',
        'lun': 'lun',
        'portals': 'portals',
        'read_only': 'readOnly',
        'secret_ref': 'secretRef',
        'target_portal': 'targetPortal'
    }

    def __init__(self, chap_auth_discovery=None, chap_auth_session=None, fs_type=None, initiator_name=None, iqn=None, iscsi_interface=None, lun=None, portals=None, read_only=None, secret_ref=None, target_portal=None):  # noqa: E501
        """V1ISCSIVolumeSource - a model defined in Swagger"""  # noqa: E501
        self._chap_auth_discovery = None
        self._chap_auth_session = None
        self._fs_type = None
        self._initiator_name = None
        self._iqn = None
        self._iscsi_interface = None
        self._lun = None
        self._portals = None
        self._read_only = None
        self._secret_ref = None
        self._target_portal = None
        self.discriminator = None
        if chap_auth_discovery is not None:
            self.chap_auth_discovery = chap_auth_discovery
        if chap_auth_session is not None:
            self.chap_auth_session = chap_auth_session
        if fs_type is not None:
            self.fs_type = fs_type
        if initiator_name is not None:
            self.initiator_name = initiator_name
        if iqn is not None:
            self.iqn = iqn
        if iscsi_interface is not None:
            self.iscsi_interface = iscsi_interface
        if lun is not None:
            self.lun = lun
        if portals is not None:
            self.portals = portals
        if read_only is not None:
            self.read_only = read_only
        if secret_ref is not None:
            self.secret_ref = secret_ref
        if target_portal is not None:
            self.target_portal = target_portal

    @property
    def chap_auth_discovery(self):
        """Gets the chap_auth_discovery of this V1ISCSIVolumeSource.  # noqa: E501


        :return: The chap_auth_discovery of this V1ISCSIVolumeSource.  # noqa: E501
        :rtype: bool
        """
        return self._chap_auth_discovery

    @chap_auth_discovery.setter
    def chap_auth_discovery(self, chap_auth_discovery):
        """Sets the chap_auth_discovery of this V1ISCSIVolumeSource.


        :param chap_auth_discovery: The chap_auth_discovery of this V1ISCSIVolumeSource.  # noqa: E501
        :type: bool
        """

        self._chap_auth_discovery = chap_auth_discovery

    @property
    def chap_auth_session(self):
        """Gets the chap_auth_session of this V1ISCSIVolumeSource.  # noqa: E501


        :return: The chap_auth_session of this V1ISCSIVolumeSource.  # noqa: E501
        :rtype: bool
        """
        return self._chap_auth_session

    @chap_auth_session.setter
    def chap_auth_session(self, chap_auth_session):
        """Sets the chap_auth_session of this V1ISCSIVolumeSource.


        :param chap_auth_session: The chap_auth_session of this V1ISCSIVolumeSource.  # noqa: E501
        :type: bool
        """

        self._chap_auth_session = chap_auth_session

    @property
    def fs_type(self):
        """Gets the fs_type of this V1ISCSIVolumeSource.  # noqa: E501


        :return: The fs_type of this V1ISCSIVolumeSource.  # noqa: E501
        :rtype: str
        """
        return self._fs_type

    @fs_type.setter
    def fs_type(self, fs_type):
        """Sets the fs_type of this V1ISCSIVolumeSource.


        :param fs_type: The fs_type of this V1ISCSIVolumeSource.  # noqa: E501
        :type: str
        """

        self._fs_type = fs_type

    @property
    def initiator_name(self):
        """Gets the initiator_name of this V1ISCSIVolumeSource.  # noqa: E501


        :return: The initiator_name of this V1ISCSIVolumeSource.  # noqa: E501
        :rtype: str
        """
        return self._initiator_name

    @initiator_name.setter
    def initiator_name(self, initiator_name):
        """Sets the initiator_name of this V1ISCSIVolumeSource.


        :param initiator_name: The initiator_name of this V1ISCSIVolumeSource.  # noqa: E501
        :type: str
        """

        self._initiator_name = initiator_name

    @property
    def iqn(self):
        """Gets the iqn of this V1ISCSIVolumeSource.  # noqa: E501

        iqn is the target iSCSI Qualified Name.  # noqa: E501

        :return: The iqn of this V1ISCSIVolumeSource.  # noqa: E501
        :rtype: str
        """
        return self._iqn

    @iqn.setter
    def iqn(self, iqn):
        """Sets the iqn of this V1ISCSIVolumeSource.

        iqn is the target iSCSI Qualified Name.  # noqa: E501

        :param iqn: The iqn of this V1ISCSIVolumeSource.  # noqa: E501
        :type: str
        """

        self._iqn = iqn

    @property
    def iscsi_interface(self):
        """Gets the iscsi_interface of this V1ISCSIVolumeSource.  # noqa: E501


        :return: The iscsi_interface of this V1ISCSIVolumeSource.  # noqa: E501
        :rtype: str
        """
        return self._iscsi_interface

    @iscsi_interface.setter
    def iscsi_interface(self, iscsi_interface):
        """Sets the iscsi_interface of this V1ISCSIVolumeSource.


        :param iscsi_interface: The iscsi_interface of this V1ISCSIVolumeSource.  # noqa: E501
        :type: str
        """

        self._iscsi_interface = iscsi_interface

    @property
    def lun(self):
        """Gets the lun of this V1ISCSIVolumeSource.  # noqa: E501

        lun represents iSCSI Target Lun number.  # noqa: E501

        :return: The lun of this V1ISCSIVolumeSource.  # noqa: E501
        :rtype: int
        """
        return self._lun

    @lun.setter
    def lun(self, lun):
        """Sets the lun of this V1ISCSIVolumeSource.

        lun represents iSCSI Target Lun number.  # noqa: E501

        :param lun: The lun of this V1ISCSIVolumeSource.  # noqa: E501
        :type: int
        """

        self._lun = lun

    @property
    def portals(self):
        """Gets the portals of this V1ISCSIVolumeSource.  # noqa: E501


        :return: The portals of this V1ISCSIVolumeSource.  # noqa: E501
        :rtype: list[str]
        """
        return self._portals

    @portals.setter
    def portals(self, portals):
        """Sets the portals of this V1ISCSIVolumeSource.


        :param portals: The portals of this V1ISCSIVolumeSource.  # noqa: E501
        :type: list[str]
        """

        self._portals = portals

    @property
    def read_only(self):
        """Gets the read_only of this V1ISCSIVolumeSource.  # noqa: E501


        :return: The read_only of this V1ISCSIVolumeSource.  # noqa: E501
        :rtype: bool
        """
        return self._read_only

    @read_only.setter
    def read_only(self, read_only):
        """Sets the read_only of this V1ISCSIVolumeSource.


        :param read_only: The read_only of this V1ISCSIVolumeSource.  # noqa: E501
        :type: bool
        """

        self._read_only = read_only

    @property
    def secret_ref(self):
        """Gets the secret_ref of this V1ISCSIVolumeSource.  # noqa: E501


        :return: The secret_ref of this V1ISCSIVolumeSource.  # noqa: E501
        :rtype: V1LocalObjectReference
        """
        return self._secret_ref

    @secret_ref.setter
    def secret_ref(self, secret_ref):
        """Sets the secret_ref of this V1ISCSIVolumeSource.


        :param secret_ref: The secret_ref of this V1ISCSIVolumeSource.  # noqa: E501
        :type: V1LocalObjectReference
        """

        self._secret_ref = secret_ref

    @property
    def target_portal(self):
        """Gets the target_portal of this V1ISCSIVolumeSource.  # noqa: E501

        targetPortal is iSCSI Target Portal. The Portal is either an IP or ip_addr:port if the port is other than default (typically TCP ports 860 and 3260).  # noqa: E501

        :return: The target_portal of this V1ISCSIVolumeSource.  # noqa: E501
        :rtype: str
        """
        return self._target_portal

    @target_portal.setter
    def target_portal(self, target_portal):
        """Sets the target_portal of this V1ISCSIVolumeSource.

        targetPortal is iSCSI Target Portal. The Portal is either an IP or ip_addr:port if the port is other than default (typically TCP ports 860 and 3260).  # noqa: E501

        :param target_portal: The target_portal of this V1ISCSIVolumeSource.  # noqa: E501
        :type: str
        """

        self._target_portal = target_portal

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
        if issubclass(V1ISCSIVolumeSource, dict):
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
        if not isinstance(other, V1ISCSIVolumeSource):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
