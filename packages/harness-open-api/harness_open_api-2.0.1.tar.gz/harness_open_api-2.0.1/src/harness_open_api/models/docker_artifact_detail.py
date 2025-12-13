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

class DockerArtifactDetail(object):
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
        'created_at': 'str',
        'downloads_count': 'int',
        'image_name': 'str',
        'is_quarantined': 'bool',
        'metadata': 'ArtifactEntityMetadata',
        'modified_at': 'str',
        'package_type': 'PackageType',
        'pull_command': 'str',
        'pull_command_by_digest': 'str',
        'quarantine_reason': 'str',
        'registry_path': 'str',
        'size': 'str',
        'url': 'str',
        'version': 'str'
    }

    attribute_map = {
        'created_at': 'createdAt',
        'downloads_count': 'downloadsCount',
        'image_name': 'imageName',
        'is_quarantined': 'isQuarantined',
        'metadata': 'metadata',
        'modified_at': 'modifiedAt',
        'package_type': 'packageType',
        'pull_command': 'pullCommand',
        'pull_command_by_digest': 'pullCommandByDigest',
        'quarantine_reason': 'quarantineReason',
        'registry_path': 'registryPath',
        'size': 'size',
        'url': 'url',
        'version': 'version'
    }

    def __init__(self, created_at=None, downloads_count=None, image_name=None, is_quarantined=None, metadata=None, modified_at=None, package_type=None, pull_command=None, pull_command_by_digest=None, quarantine_reason=None, registry_path=None, size=None, url=None, version=None):  # noqa: E501
        """DockerArtifactDetail - a model defined in Swagger"""  # noqa: E501
        self._created_at = None
        self._downloads_count = None
        self._image_name = None
        self._is_quarantined = None
        self._metadata = None
        self._modified_at = None
        self._package_type = None
        self._pull_command = None
        self._pull_command_by_digest = None
        self._quarantine_reason = None
        self._registry_path = None
        self._size = None
        self._url = None
        self._version = None
        self.discriminator = None
        if created_at is not None:
            self.created_at = created_at
        if downloads_count is not None:
            self.downloads_count = downloads_count
        self.image_name = image_name
        if is_quarantined is not None:
            self.is_quarantined = is_quarantined
        if metadata is not None:
            self.metadata = metadata
        if modified_at is not None:
            self.modified_at = modified_at
        self.package_type = package_type
        if pull_command is not None:
            self.pull_command = pull_command
        if pull_command_by_digest is not None:
            self.pull_command_by_digest = pull_command_by_digest
        if quarantine_reason is not None:
            self.quarantine_reason = quarantine_reason
        self.registry_path = registry_path
        if size is not None:
            self.size = size
        self.url = url
        self.version = version

    @property
    def created_at(self):
        """Gets the created_at of this DockerArtifactDetail.  # noqa: E501


        :return: The created_at of this DockerArtifactDetail.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this DockerArtifactDetail.


        :param created_at: The created_at of this DockerArtifactDetail.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def downloads_count(self):
        """Gets the downloads_count of this DockerArtifactDetail.  # noqa: E501


        :return: The downloads_count of this DockerArtifactDetail.  # noqa: E501
        :rtype: int
        """
        return self._downloads_count

    @downloads_count.setter
    def downloads_count(self, downloads_count):
        """Sets the downloads_count of this DockerArtifactDetail.


        :param downloads_count: The downloads_count of this DockerArtifactDetail.  # noqa: E501
        :type: int
        """

        self._downloads_count = downloads_count

    @property
    def image_name(self):
        """Gets the image_name of this DockerArtifactDetail.  # noqa: E501


        :return: The image_name of this DockerArtifactDetail.  # noqa: E501
        :rtype: str
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name):
        """Sets the image_name of this DockerArtifactDetail.


        :param image_name: The image_name of this DockerArtifactDetail.  # noqa: E501
        :type: str
        """
        if image_name is None:
            raise ValueError("Invalid value for `image_name`, must not be `None`")  # noqa: E501

        self._image_name = image_name

    @property
    def is_quarantined(self):
        """Gets the is_quarantined of this DockerArtifactDetail.  # noqa: E501


        :return: The is_quarantined of this DockerArtifactDetail.  # noqa: E501
        :rtype: bool
        """
        return self._is_quarantined

    @is_quarantined.setter
    def is_quarantined(self, is_quarantined):
        """Sets the is_quarantined of this DockerArtifactDetail.


        :param is_quarantined: The is_quarantined of this DockerArtifactDetail.  # noqa: E501
        :type: bool
        """

        self._is_quarantined = is_quarantined

    @property
    def metadata(self):
        """Gets the metadata of this DockerArtifactDetail.  # noqa: E501


        :return: The metadata of this DockerArtifactDetail.  # noqa: E501
        :rtype: ArtifactEntityMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this DockerArtifactDetail.


        :param metadata: The metadata of this DockerArtifactDetail.  # noqa: E501
        :type: ArtifactEntityMetadata
        """

        self._metadata = metadata

    @property
    def modified_at(self):
        """Gets the modified_at of this DockerArtifactDetail.  # noqa: E501


        :return: The modified_at of this DockerArtifactDetail.  # noqa: E501
        :rtype: str
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this DockerArtifactDetail.


        :param modified_at: The modified_at of this DockerArtifactDetail.  # noqa: E501
        :type: str
        """

        self._modified_at = modified_at

    @property
    def package_type(self):
        """Gets the package_type of this DockerArtifactDetail.  # noqa: E501


        :return: The package_type of this DockerArtifactDetail.  # noqa: E501
        :rtype: PackageType
        """
        return self._package_type

    @package_type.setter
    def package_type(self, package_type):
        """Sets the package_type of this DockerArtifactDetail.


        :param package_type: The package_type of this DockerArtifactDetail.  # noqa: E501
        :type: PackageType
        """
        if package_type is None:
            raise ValueError("Invalid value for `package_type`, must not be `None`")  # noqa: E501

        self._package_type = package_type

    @property
    def pull_command(self):
        """Gets the pull_command of this DockerArtifactDetail.  # noqa: E501


        :return: The pull_command of this DockerArtifactDetail.  # noqa: E501
        :rtype: str
        """
        return self._pull_command

    @pull_command.setter
    def pull_command(self, pull_command):
        """Sets the pull_command of this DockerArtifactDetail.


        :param pull_command: The pull_command of this DockerArtifactDetail.  # noqa: E501
        :type: str
        """

        self._pull_command = pull_command

    @property
    def pull_command_by_digest(self):
        """Gets the pull_command_by_digest of this DockerArtifactDetail.  # noqa: E501


        :return: The pull_command_by_digest of this DockerArtifactDetail.  # noqa: E501
        :rtype: str
        """
        return self._pull_command_by_digest

    @pull_command_by_digest.setter
    def pull_command_by_digest(self, pull_command_by_digest):
        """Sets the pull_command_by_digest of this DockerArtifactDetail.


        :param pull_command_by_digest: The pull_command_by_digest of this DockerArtifactDetail.  # noqa: E501
        :type: str
        """

        self._pull_command_by_digest = pull_command_by_digest

    @property
    def quarantine_reason(self):
        """Gets the quarantine_reason of this DockerArtifactDetail.  # noqa: E501


        :return: The quarantine_reason of this DockerArtifactDetail.  # noqa: E501
        :rtype: str
        """
        return self._quarantine_reason

    @quarantine_reason.setter
    def quarantine_reason(self, quarantine_reason):
        """Sets the quarantine_reason of this DockerArtifactDetail.


        :param quarantine_reason: The quarantine_reason of this DockerArtifactDetail.  # noqa: E501
        :type: str
        """

        self._quarantine_reason = quarantine_reason

    @property
    def registry_path(self):
        """Gets the registry_path of this DockerArtifactDetail.  # noqa: E501


        :return: The registry_path of this DockerArtifactDetail.  # noqa: E501
        :rtype: str
        """
        return self._registry_path

    @registry_path.setter
    def registry_path(self, registry_path):
        """Sets the registry_path of this DockerArtifactDetail.


        :param registry_path: The registry_path of this DockerArtifactDetail.  # noqa: E501
        :type: str
        """
        if registry_path is None:
            raise ValueError("Invalid value for `registry_path`, must not be `None`")  # noqa: E501

        self._registry_path = registry_path

    @property
    def size(self):
        """Gets the size of this DockerArtifactDetail.  # noqa: E501


        :return: The size of this DockerArtifactDetail.  # noqa: E501
        :rtype: str
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this DockerArtifactDetail.


        :param size: The size of this DockerArtifactDetail.  # noqa: E501
        :type: str
        """

        self._size = size

    @property
    def url(self):
        """Gets the url of this DockerArtifactDetail.  # noqa: E501


        :return: The url of this DockerArtifactDetail.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this DockerArtifactDetail.


        :param url: The url of this DockerArtifactDetail.  # noqa: E501
        :type: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def version(self):
        """Gets the version of this DockerArtifactDetail.  # noqa: E501


        :return: The version of this DockerArtifactDetail.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this DockerArtifactDetail.


        :param version: The version of this DockerArtifactDetail.  # noqa: E501
        :type: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

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
        if issubclass(DockerArtifactDetail, dict):
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
        if not isinstance(other, DockerArtifactDetail):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
