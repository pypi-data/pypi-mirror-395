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

class V1RolloutReplicaSetInfo(object):
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
        'active': 'bool',
        'available': 'int',
        'canary': 'bool',
        'icon': 'str',
        'images': 'list[str]',
        'metadata': 'V1ObjectMeta',
        'ping': 'bool',
        'pods': 'list[V1RolloutPodInfo]',
        'pong': 'bool',
        'preview': 'bool',
        'replicas': 'int',
        'revision': 'str',
        'scale_down_deadline': 'str',
        'stable': 'bool',
        'status': 'str',
        'template': 'str'
    }

    attribute_map = {
        'active': 'active',
        'available': 'available',
        'canary': 'canary',
        'icon': 'icon',
        'images': 'images',
        'metadata': 'metadata',
        'ping': 'ping',
        'pods': 'pods',
        'pong': 'pong',
        'preview': 'preview',
        'replicas': 'replicas',
        'revision': 'revision',
        'scale_down_deadline': 'scaleDownDeadline',
        'stable': 'stable',
        'status': 'status',
        'template': 'template'
    }

    def __init__(self, active=None, available=None, canary=None, icon=None, images=None, metadata=None, ping=None, pods=None, pong=None, preview=None, replicas=None, revision=None, scale_down_deadline=None, stable=None, status=None, template=None):  # noqa: E501
        """V1RolloutReplicaSetInfo - a model defined in Swagger"""  # noqa: E501
        self._active = None
        self._available = None
        self._canary = None
        self._icon = None
        self._images = None
        self._metadata = None
        self._ping = None
        self._pods = None
        self._pong = None
        self._preview = None
        self._replicas = None
        self._revision = None
        self._scale_down_deadline = None
        self._stable = None
        self._status = None
        self._template = None
        self.discriminator = None
        if active is not None:
            self.active = active
        if available is not None:
            self.available = available
        if canary is not None:
            self.canary = canary
        if icon is not None:
            self.icon = icon
        if images is not None:
            self.images = images
        if metadata is not None:
            self.metadata = metadata
        if ping is not None:
            self.ping = ping
        if pods is not None:
            self.pods = pods
        if pong is not None:
            self.pong = pong
        if preview is not None:
            self.preview = preview
        if replicas is not None:
            self.replicas = replicas
        if revision is not None:
            self.revision = revision
        if scale_down_deadline is not None:
            self.scale_down_deadline = scale_down_deadline
        if stable is not None:
            self.stable = stable
        if status is not None:
            self.status = status
        if template is not None:
            self.template = template

    @property
    def active(self):
        """Gets the active of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The active of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """Sets the active of this V1RolloutReplicaSetInfo.


        :param active: The active of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: bool
        """

        self._active = active

    @property
    def available(self):
        """Gets the available of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The available of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: int
        """
        return self._available

    @available.setter
    def available(self, available):
        """Sets the available of this V1RolloutReplicaSetInfo.


        :param available: The available of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: int
        """

        self._available = available

    @property
    def canary(self):
        """Gets the canary of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The canary of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: bool
        """
        return self._canary

    @canary.setter
    def canary(self, canary):
        """Sets the canary of this V1RolloutReplicaSetInfo.


        :param canary: The canary of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: bool
        """

        self._canary = canary

    @property
    def icon(self):
        """Gets the icon of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The icon of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: str
        """
        return self._icon

    @icon.setter
    def icon(self, icon):
        """Sets the icon of this V1RolloutReplicaSetInfo.


        :param icon: The icon of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: str
        """

        self._icon = icon

    @property
    def images(self):
        """Gets the images of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The images of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: list[str]
        """
        return self._images

    @images.setter
    def images(self, images):
        """Sets the images of this V1RolloutReplicaSetInfo.


        :param images: The images of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: list[str]
        """

        self._images = images

    @property
    def metadata(self):
        """Gets the metadata of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The metadata of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: V1ObjectMeta
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this V1RolloutReplicaSetInfo.


        :param metadata: The metadata of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: V1ObjectMeta
        """

        self._metadata = metadata

    @property
    def ping(self):
        """Gets the ping of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The ping of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: bool
        """
        return self._ping

    @ping.setter
    def ping(self, ping):
        """Sets the ping of this V1RolloutReplicaSetInfo.


        :param ping: The ping of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: bool
        """

        self._ping = ping

    @property
    def pods(self):
        """Gets the pods of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The pods of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: list[V1RolloutPodInfo]
        """
        return self._pods

    @pods.setter
    def pods(self, pods):
        """Sets the pods of this V1RolloutReplicaSetInfo.


        :param pods: The pods of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: list[V1RolloutPodInfo]
        """

        self._pods = pods

    @property
    def pong(self):
        """Gets the pong of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The pong of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: bool
        """
        return self._pong

    @pong.setter
    def pong(self, pong):
        """Sets the pong of this V1RolloutReplicaSetInfo.


        :param pong: The pong of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: bool
        """

        self._pong = pong

    @property
    def preview(self):
        """Gets the preview of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The preview of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: bool
        """
        return self._preview

    @preview.setter
    def preview(self, preview):
        """Sets the preview of this V1RolloutReplicaSetInfo.


        :param preview: The preview of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: bool
        """

        self._preview = preview

    @property
    def replicas(self):
        """Gets the replicas of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The replicas of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: int
        """
        return self._replicas

    @replicas.setter
    def replicas(self, replicas):
        """Sets the replicas of this V1RolloutReplicaSetInfo.


        :param replicas: The replicas of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: int
        """

        self._replicas = replicas

    @property
    def revision(self):
        """Gets the revision of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The revision of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: str
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """Sets the revision of this V1RolloutReplicaSetInfo.


        :param revision: The revision of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: str
        """

        self._revision = revision

    @property
    def scale_down_deadline(self):
        """Gets the scale_down_deadline of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The scale_down_deadline of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: str
        """
        return self._scale_down_deadline

    @scale_down_deadline.setter
    def scale_down_deadline(self, scale_down_deadline):
        """Sets the scale_down_deadline of this V1RolloutReplicaSetInfo.


        :param scale_down_deadline: The scale_down_deadline of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: str
        """

        self._scale_down_deadline = scale_down_deadline

    @property
    def stable(self):
        """Gets the stable of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The stable of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: bool
        """
        return self._stable

    @stable.setter
    def stable(self, stable):
        """Sets the stable of this V1RolloutReplicaSetInfo.


        :param stable: The stable of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: bool
        """

        self._stable = stable

    @property
    def status(self):
        """Gets the status of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The status of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this V1RolloutReplicaSetInfo.


        :param status: The status of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def template(self):
        """Gets the template of this V1RolloutReplicaSetInfo.  # noqa: E501


        :return: The template of this V1RolloutReplicaSetInfo.  # noqa: E501
        :rtype: str
        """
        return self._template

    @template.setter
    def template(self, template):
        """Sets the template of this V1RolloutReplicaSetInfo.


        :param template: The template of this V1RolloutReplicaSetInfo.  # noqa: E501
        :type: str
        """

        self._template = template

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
        if issubclass(V1RolloutReplicaSetInfo, dict):
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
        if not isinstance(other, V1RolloutReplicaSetInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
