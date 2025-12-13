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

class V1Container(object):
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
        'args': 'list[str]',
        'command': 'list[str]',
        'env': 'list[V1EnvVar]',
        'env_from': 'list[V1EnvFromSource]',
        'image': 'str',
        'image_pull_policy': 'str',
        'lifecycle': 'V1Lifecycle',
        'liveness_probe': 'V1Probe',
        'name': 'str',
        'ports': 'list[V1ContainerPort]',
        'readiness_probe': 'V1Probe',
        'resize_policy': 'list[V1ContainerResizePolicy]',
        'resources': 'V1ResourceRequirements',
        'restart_policy': 'str',
        'security_context': 'V1SecurityContext',
        'startup_probe': 'V1Probe',
        'stdin': 'bool',
        'stdin_once': 'bool',
        'termination_message_path': 'str',
        'termination_message_policy': 'str',
        'tty': 'bool',
        'volume_devices': 'list[V1VolumeDevice]',
        'volume_mounts': 'list[V1VolumeMount]',
        'working_dir': 'str'
    }

    attribute_map = {
        'args': 'args',
        'command': 'command',
        'env': 'env',
        'env_from': 'envFrom',
        'image': 'image',
        'image_pull_policy': 'imagePullPolicy',
        'lifecycle': 'lifecycle',
        'liveness_probe': 'livenessProbe',
        'name': 'name',
        'ports': 'ports',
        'readiness_probe': 'readinessProbe',
        'resize_policy': 'resizePolicy',
        'resources': 'resources',
        'restart_policy': 'restartPolicy',
        'security_context': 'securityContext',
        'startup_probe': 'startupProbe',
        'stdin': 'stdin',
        'stdin_once': 'stdinOnce',
        'termination_message_path': 'terminationMessagePath',
        'termination_message_policy': 'terminationMessagePolicy',
        'tty': 'tty',
        'volume_devices': 'volumeDevices',
        'volume_mounts': 'volumeMounts',
        'working_dir': 'workingDir'
    }

    def __init__(self, args=None, command=None, env=None, env_from=None, image=None, image_pull_policy=None, lifecycle=None, liveness_probe=None, name=None, ports=None, readiness_probe=None, resize_policy=None, resources=None, restart_policy=None, security_context=None, startup_probe=None, stdin=None, stdin_once=None, termination_message_path=None, termination_message_policy=None, tty=None, volume_devices=None, volume_mounts=None, working_dir=None):  # noqa: E501
        """V1Container - a model defined in Swagger"""  # noqa: E501
        self._args = None
        self._command = None
        self._env = None
        self._env_from = None
        self._image = None
        self._image_pull_policy = None
        self._lifecycle = None
        self._liveness_probe = None
        self._name = None
        self._ports = None
        self._readiness_probe = None
        self._resize_policy = None
        self._resources = None
        self._restart_policy = None
        self._security_context = None
        self._startup_probe = None
        self._stdin = None
        self._stdin_once = None
        self._termination_message_path = None
        self._termination_message_policy = None
        self._tty = None
        self._volume_devices = None
        self._volume_mounts = None
        self._working_dir = None
        self.discriminator = None
        if args is not None:
            self.args = args
        if command is not None:
            self.command = command
        if env is not None:
            self.env = env
        if env_from is not None:
            self.env_from = env_from
        if image is not None:
            self.image = image
        if image_pull_policy is not None:
            self.image_pull_policy = image_pull_policy
        if lifecycle is not None:
            self.lifecycle = lifecycle
        if liveness_probe is not None:
            self.liveness_probe = liveness_probe
        if name is not None:
            self.name = name
        if ports is not None:
            self.ports = ports
        if readiness_probe is not None:
            self.readiness_probe = readiness_probe
        if resize_policy is not None:
            self.resize_policy = resize_policy
        if resources is not None:
            self.resources = resources
        if restart_policy is not None:
            self.restart_policy = restart_policy
        if security_context is not None:
            self.security_context = security_context
        if startup_probe is not None:
            self.startup_probe = startup_probe
        if stdin is not None:
            self.stdin = stdin
        if stdin_once is not None:
            self.stdin_once = stdin_once
        if termination_message_path is not None:
            self.termination_message_path = termination_message_path
        if termination_message_policy is not None:
            self.termination_message_policy = termination_message_policy
        if tty is not None:
            self.tty = tty
        if volume_devices is not None:
            self.volume_devices = volume_devices
        if volume_mounts is not None:
            self.volume_mounts = volume_mounts
        if working_dir is not None:
            self.working_dir = working_dir

    @property
    def args(self):
        """Gets the args of this V1Container.  # noqa: E501


        :return: The args of this V1Container.  # noqa: E501
        :rtype: list[str]
        """
        return self._args

    @args.setter
    def args(self, args):
        """Sets the args of this V1Container.


        :param args: The args of this V1Container.  # noqa: E501
        :type: list[str]
        """

        self._args = args

    @property
    def command(self):
        """Gets the command of this V1Container.  # noqa: E501


        :return: The command of this V1Container.  # noqa: E501
        :rtype: list[str]
        """
        return self._command

    @command.setter
    def command(self, command):
        """Sets the command of this V1Container.


        :param command: The command of this V1Container.  # noqa: E501
        :type: list[str]
        """

        self._command = command

    @property
    def env(self):
        """Gets the env of this V1Container.  # noqa: E501


        :return: The env of this V1Container.  # noqa: E501
        :rtype: list[V1EnvVar]
        """
        return self._env

    @env.setter
    def env(self, env):
        """Sets the env of this V1Container.


        :param env: The env of this V1Container.  # noqa: E501
        :type: list[V1EnvVar]
        """

        self._env = env

    @property
    def env_from(self):
        """Gets the env_from of this V1Container.  # noqa: E501


        :return: The env_from of this V1Container.  # noqa: E501
        :rtype: list[V1EnvFromSource]
        """
        return self._env_from

    @env_from.setter
    def env_from(self, env_from):
        """Sets the env_from of this V1Container.


        :param env_from: The env_from of this V1Container.  # noqa: E501
        :type: list[V1EnvFromSource]
        """

        self._env_from = env_from

    @property
    def image(self):
        """Gets the image of this V1Container.  # noqa: E501


        :return: The image of this V1Container.  # noqa: E501
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this V1Container.


        :param image: The image of this V1Container.  # noqa: E501
        :type: str
        """

        self._image = image

    @property
    def image_pull_policy(self):
        """Gets the image_pull_policy of this V1Container.  # noqa: E501


        :return: The image_pull_policy of this V1Container.  # noqa: E501
        :rtype: str
        """
        return self._image_pull_policy

    @image_pull_policy.setter
    def image_pull_policy(self, image_pull_policy):
        """Sets the image_pull_policy of this V1Container.


        :param image_pull_policy: The image_pull_policy of this V1Container.  # noqa: E501
        :type: str
        """

        self._image_pull_policy = image_pull_policy

    @property
    def lifecycle(self):
        """Gets the lifecycle of this V1Container.  # noqa: E501


        :return: The lifecycle of this V1Container.  # noqa: E501
        :rtype: V1Lifecycle
        """
        return self._lifecycle

    @lifecycle.setter
    def lifecycle(self, lifecycle):
        """Sets the lifecycle of this V1Container.


        :param lifecycle: The lifecycle of this V1Container.  # noqa: E501
        :type: V1Lifecycle
        """

        self._lifecycle = lifecycle

    @property
    def liveness_probe(self):
        """Gets the liveness_probe of this V1Container.  # noqa: E501


        :return: The liveness_probe of this V1Container.  # noqa: E501
        :rtype: V1Probe
        """
        return self._liveness_probe

    @liveness_probe.setter
    def liveness_probe(self, liveness_probe):
        """Sets the liveness_probe of this V1Container.


        :param liveness_probe: The liveness_probe of this V1Container.  # noqa: E501
        :type: V1Probe
        """

        self._liveness_probe = liveness_probe

    @property
    def name(self):
        """Gets the name of this V1Container.  # noqa: E501

        Name of the container specified as a DNS_LABEL. Each container in a pod must have a unique name (DNS_LABEL). Cannot be updated.  # noqa: E501

        :return: The name of this V1Container.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V1Container.

        Name of the container specified as a DNS_LABEL. Each container in a pod must have a unique name (DNS_LABEL). Cannot be updated.  # noqa: E501

        :param name: The name of this V1Container.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def ports(self):
        """Gets the ports of this V1Container.  # noqa: E501


        :return: The ports of this V1Container.  # noqa: E501
        :rtype: list[V1ContainerPort]
        """
        return self._ports

    @ports.setter
    def ports(self, ports):
        """Sets the ports of this V1Container.


        :param ports: The ports of this V1Container.  # noqa: E501
        :type: list[V1ContainerPort]
        """

        self._ports = ports

    @property
    def readiness_probe(self):
        """Gets the readiness_probe of this V1Container.  # noqa: E501


        :return: The readiness_probe of this V1Container.  # noqa: E501
        :rtype: V1Probe
        """
        return self._readiness_probe

    @readiness_probe.setter
    def readiness_probe(self, readiness_probe):
        """Sets the readiness_probe of this V1Container.


        :param readiness_probe: The readiness_probe of this V1Container.  # noqa: E501
        :type: V1Probe
        """

        self._readiness_probe = readiness_probe

    @property
    def resize_policy(self):
        """Gets the resize_policy of this V1Container.  # noqa: E501


        :return: The resize_policy of this V1Container.  # noqa: E501
        :rtype: list[V1ContainerResizePolicy]
        """
        return self._resize_policy

    @resize_policy.setter
    def resize_policy(self, resize_policy):
        """Sets the resize_policy of this V1Container.


        :param resize_policy: The resize_policy of this V1Container.  # noqa: E501
        :type: list[V1ContainerResizePolicy]
        """

        self._resize_policy = resize_policy

    @property
    def resources(self):
        """Gets the resources of this V1Container.  # noqa: E501


        :return: The resources of this V1Container.  # noqa: E501
        :rtype: V1ResourceRequirements
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this V1Container.


        :param resources: The resources of this V1Container.  # noqa: E501
        :type: V1ResourceRequirements
        """

        self._resources = resources

    @property
    def restart_policy(self):
        """Gets the restart_policy of this V1Container.  # noqa: E501


        :return: The restart_policy of this V1Container.  # noqa: E501
        :rtype: str
        """
        return self._restart_policy

    @restart_policy.setter
    def restart_policy(self, restart_policy):
        """Sets the restart_policy of this V1Container.


        :param restart_policy: The restart_policy of this V1Container.  # noqa: E501
        :type: str
        """

        self._restart_policy = restart_policy

    @property
    def security_context(self):
        """Gets the security_context of this V1Container.  # noqa: E501


        :return: The security_context of this V1Container.  # noqa: E501
        :rtype: V1SecurityContext
        """
        return self._security_context

    @security_context.setter
    def security_context(self, security_context):
        """Sets the security_context of this V1Container.


        :param security_context: The security_context of this V1Container.  # noqa: E501
        :type: V1SecurityContext
        """

        self._security_context = security_context

    @property
    def startup_probe(self):
        """Gets the startup_probe of this V1Container.  # noqa: E501


        :return: The startup_probe of this V1Container.  # noqa: E501
        :rtype: V1Probe
        """
        return self._startup_probe

    @startup_probe.setter
    def startup_probe(self, startup_probe):
        """Sets the startup_probe of this V1Container.


        :param startup_probe: The startup_probe of this V1Container.  # noqa: E501
        :type: V1Probe
        """

        self._startup_probe = startup_probe

    @property
    def stdin(self):
        """Gets the stdin of this V1Container.  # noqa: E501


        :return: The stdin of this V1Container.  # noqa: E501
        :rtype: bool
        """
        return self._stdin

    @stdin.setter
    def stdin(self, stdin):
        """Sets the stdin of this V1Container.


        :param stdin: The stdin of this V1Container.  # noqa: E501
        :type: bool
        """

        self._stdin = stdin

    @property
    def stdin_once(self):
        """Gets the stdin_once of this V1Container.  # noqa: E501


        :return: The stdin_once of this V1Container.  # noqa: E501
        :rtype: bool
        """
        return self._stdin_once

    @stdin_once.setter
    def stdin_once(self, stdin_once):
        """Sets the stdin_once of this V1Container.


        :param stdin_once: The stdin_once of this V1Container.  # noqa: E501
        :type: bool
        """

        self._stdin_once = stdin_once

    @property
    def termination_message_path(self):
        """Gets the termination_message_path of this V1Container.  # noqa: E501


        :return: The termination_message_path of this V1Container.  # noqa: E501
        :rtype: str
        """
        return self._termination_message_path

    @termination_message_path.setter
    def termination_message_path(self, termination_message_path):
        """Sets the termination_message_path of this V1Container.


        :param termination_message_path: The termination_message_path of this V1Container.  # noqa: E501
        :type: str
        """

        self._termination_message_path = termination_message_path

    @property
    def termination_message_policy(self):
        """Gets the termination_message_policy of this V1Container.  # noqa: E501


        :return: The termination_message_policy of this V1Container.  # noqa: E501
        :rtype: str
        """
        return self._termination_message_policy

    @termination_message_policy.setter
    def termination_message_policy(self, termination_message_policy):
        """Sets the termination_message_policy of this V1Container.


        :param termination_message_policy: The termination_message_policy of this V1Container.  # noqa: E501
        :type: str
        """

        self._termination_message_policy = termination_message_policy

    @property
    def tty(self):
        """Gets the tty of this V1Container.  # noqa: E501


        :return: The tty of this V1Container.  # noqa: E501
        :rtype: bool
        """
        return self._tty

    @tty.setter
    def tty(self, tty):
        """Sets the tty of this V1Container.


        :param tty: The tty of this V1Container.  # noqa: E501
        :type: bool
        """

        self._tty = tty

    @property
    def volume_devices(self):
        """Gets the volume_devices of this V1Container.  # noqa: E501


        :return: The volume_devices of this V1Container.  # noqa: E501
        :rtype: list[V1VolumeDevice]
        """
        return self._volume_devices

    @volume_devices.setter
    def volume_devices(self, volume_devices):
        """Sets the volume_devices of this V1Container.


        :param volume_devices: The volume_devices of this V1Container.  # noqa: E501
        :type: list[V1VolumeDevice]
        """

        self._volume_devices = volume_devices

    @property
    def volume_mounts(self):
        """Gets the volume_mounts of this V1Container.  # noqa: E501


        :return: The volume_mounts of this V1Container.  # noqa: E501
        :rtype: list[V1VolumeMount]
        """
        return self._volume_mounts

    @volume_mounts.setter
    def volume_mounts(self, volume_mounts):
        """Sets the volume_mounts of this V1Container.


        :param volume_mounts: The volume_mounts of this V1Container.  # noqa: E501
        :type: list[V1VolumeMount]
        """

        self._volume_mounts = volume_mounts

    @property
    def working_dir(self):
        """Gets the working_dir of this V1Container.  # noqa: E501


        :return: The working_dir of this V1Container.  # noqa: E501
        :rtype: str
        """
        return self._working_dir

    @working_dir.setter
    def working_dir(self, working_dir):
        """Sets the working_dir of this V1Container.


        :param working_dir: The working_dir of this V1Container.  # noqa: E501
        :type: str
        """

        self._working_dir = working_dir

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
        if issubclass(V1Container, dict):
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
        if not isinstance(other, V1Container):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
