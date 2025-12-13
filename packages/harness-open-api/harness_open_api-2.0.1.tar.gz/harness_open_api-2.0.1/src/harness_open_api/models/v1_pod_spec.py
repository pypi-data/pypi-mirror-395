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

class V1PodSpec(object):
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
        'active_deadline_seconds': 'str',
        'affinity': 'V1Affinity',
        'automount_service_account_token': 'bool',
        'containers': 'list[V1Container]',
        'dns_config': 'V1PodDNSConfig',
        'dns_policy': 'str',
        'enable_service_links': 'bool',
        'ephemeral_containers': 'list[V1EphemeralContainer]',
        'host_aliases': 'list[V1HostAlias]',
        'host_ipc': 'bool',
        'host_network': 'bool',
        'host_pid': 'bool',
        'host_users': 'bool',
        'hostname': 'str',
        'image_pull_secrets': 'list[V1LocalObjectReference]',
        'init_containers': 'list[V1Container]',
        'node_name': 'str',
        'node_selector': 'dict(str, str)',
        'os': 'V1PodOS',
        'overhead': 'dict(str, ResourceQuantity)',
        'preemption_policy': 'str',
        'priority': 'int',
        'priority_class_name': 'str',
        'readiness_gates': 'list[V1PodReadinessGate]',
        'resource_claims': 'list[V1PodResourceClaim]',
        'resources': 'V1ResourceRequirements',
        'restart_policy': 'str',
        'runtime_class_name': 'str',
        'scheduler_name': 'str',
        'scheduling_gates': 'list[V1PodSchedulingGate]',
        'security_context': 'V1PodSecurityContext',
        'service_account': 'str',
        'service_account_name': 'str',
        'set_hostname_as_fqdn': 'bool',
        'share_process_namespace': 'bool',
        'subdomain': 'str',
        'termination_grace_period_seconds': 'str',
        'tolerations': 'list[V1Toleration]',
        'topology_spread_constraints': 'list[V1TopologySpreadConstraint]',
        'volumes': 'list[V1Volume]'
    }

    attribute_map = {
        'active_deadline_seconds': 'activeDeadlineSeconds',
        'affinity': 'affinity',
        'automount_service_account_token': 'automountServiceAccountToken',
        'containers': 'containers',
        'dns_config': 'dnsConfig',
        'dns_policy': 'dnsPolicy',
        'enable_service_links': 'enableServiceLinks',
        'ephemeral_containers': 'ephemeralContainers',
        'host_aliases': 'hostAliases',
        'host_ipc': 'hostIPC',
        'host_network': 'hostNetwork',
        'host_pid': 'hostPID',
        'host_users': 'hostUsers',
        'hostname': 'hostname',
        'image_pull_secrets': 'imagePullSecrets',
        'init_containers': 'initContainers',
        'node_name': 'nodeName',
        'node_selector': 'nodeSelector',
        'os': 'os',
        'overhead': 'overhead',
        'preemption_policy': 'preemptionPolicy',
        'priority': 'priority',
        'priority_class_name': 'priorityClassName',
        'readiness_gates': 'readinessGates',
        'resource_claims': 'resourceClaims',
        'resources': 'resources',
        'restart_policy': 'restartPolicy',
        'runtime_class_name': 'runtimeClassName',
        'scheduler_name': 'schedulerName',
        'scheduling_gates': 'schedulingGates',
        'security_context': 'securityContext',
        'service_account': 'serviceAccount',
        'service_account_name': 'serviceAccountName',
        'set_hostname_as_fqdn': 'setHostnameAsFQDN',
        'share_process_namespace': 'shareProcessNamespace',
        'subdomain': 'subdomain',
        'termination_grace_period_seconds': 'terminationGracePeriodSeconds',
        'tolerations': 'tolerations',
        'topology_spread_constraints': 'topologySpreadConstraints',
        'volumes': 'volumes'
    }

    def __init__(self, active_deadline_seconds=None, affinity=None, automount_service_account_token=None, containers=None, dns_config=None, dns_policy=None, enable_service_links=None, ephemeral_containers=None, host_aliases=None, host_ipc=None, host_network=None, host_pid=None, host_users=None, hostname=None, image_pull_secrets=None, init_containers=None, node_name=None, node_selector=None, os=None, overhead=None, preemption_policy=None, priority=None, priority_class_name=None, readiness_gates=None, resource_claims=None, resources=None, restart_policy=None, runtime_class_name=None, scheduler_name=None, scheduling_gates=None, security_context=None, service_account=None, service_account_name=None, set_hostname_as_fqdn=None, share_process_namespace=None, subdomain=None, termination_grace_period_seconds=None, tolerations=None, topology_spread_constraints=None, volumes=None):  # noqa: E501
        """V1PodSpec - a model defined in Swagger"""  # noqa: E501
        self._active_deadline_seconds = None
        self._affinity = None
        self._automount_service_account_token = None
        self._containers = None
        self._dns_config = None
        self._dns_policy = None
        self._enable_service_links = None
        self._ephemeral_containers = None
        self._host_aliases = None
        self._host_ipc = None
        self._host_network = None
        self._host_pid = None
        self._host_users = None
        self._hostname = None
        self._image_pull_secrets = None
        self._init_containers = None
        self._node_name = None
        self._node_selector = None
        self._os = None
        self._overhead = None
        self._preemption_policy = None
        self._priority = None
        self._priority_class_name = None
        self._readiness_gates = None
        self._resource_claims = None
        self._resources = None
        self._restart_policy = None
        self._runtime_class_name = None
        self._scheduler_name = None
        self._scheduling_gates = None
        self._security_context = None
        self._service_account = None
        self._service_account_name = None
        self._set_hostname_as_fqdn = None
        self._share_process_namespace = None
        self._subdomain = None
        self._termination_grace_period_seconds = None
        self._tolerations = None
        self._topology_spread_constraints = None
        self._volumes = None
        self.discriminator = None
        if active_deadline_seconds is not None:
            self.active_deadline_seconds = active_deadline_seconds
        if affinity is not None:
            self.affinity = affinity
        if automount_service_account_token is not None:
            self.automount_service_account_token = automount_service_account_token
        if containers is not None:
            self.containers = containers
        if dns_config is not None:
            self.dns_config = dns_config
        if dns_policy is not None:
            self.dns_policy = dns_policy
        if enable_service_links is not None:
            self.enable_service_links = enable_service_links
        if ephemeral_containers is not None:
            self.ephemeral_containers = ephemeral_containers
        if host_aliases is not None:
            self.host_aliases = host_aliases
        if host_ipc is not None:
            self.host_ipc = host_ipc
        if host_network is not None:
            self.host_network = host_network
        if host_pid is not None:
            self.host_pid = host_pid
        if host_users is not None:
            self.host_users = host_users
        if hostname is not None:
            self.hostname = hostname
        if image_pull_secrets is not None:
            self.image_pull_secrets = image_pull_secrets
        if init_containers is not None:
            self.init_containers = init_containers
        if node_name is not None:
            self.node_name = node_name
        if node_selector is not None:
            self.node_selector = node_selector
        if os is not None:
            self.os = os
        if overhead is not None:
            self.overhead = overhead
        if preemption_policy is not None:
            self.preemption_policy = preemption_policy
        if priority is not None:
            self.priority = priority
        if priority_class_name is not None:
            self.priority_class_name = priority_class_name
        if readiness_gates is not None:
            self.readiness_gates = readiness_gates
        if resource_claims is not None:
            self.resource_claims = resource_claims
        if resources is not None:
            self.resources = resources
        if restart_policy is not None:
            self.restart_policy = restart_policy
        if runtime_class_name is not None:
            self.runtime_class_name = runtime_class_name
        if scheduler_name is not None:
            self.scheduler_name = scheduler_name
        if scheduling_gates is not None:
            self.scheduling_gates = scheduling_gates
        if security_context is not None:
            self.security_context = security_context
        if service_account is not None:
            self.service_account = service_account
        if service_account_name is not None:
            self.service_account_name = service_account_name
        if set_hostname_as_fqdn is not None:
            self.set_hostname_as_fqdn = set_hostname_as_fqdn
        if share_process_namespace is not None:
            self.share_process_namespace = share_process_namespace
        if subdomain is not None:
            self.subdomain = subdomain
        if termination_grace_period_seconds is not None:
            self.termination_grace_period_seconds = termination_grace_period_seconds
        if tolerations is not None:
            self.tolerations = tolerations
        if topology_spread_constraints is not None:
            self.topology_spread_constraints = topology_spread_constraints
        if volumes is not None:
            self.volumes = volumes

    @property
    def active_deadline_seconds(self):
        """Gets the active_deadline_seconds of this V1PodSpec.  # noqa: E501


        :return: The active_deadline_seconds of this V1PodSpec.  # noqa: E501
        :rtype: str
        """
        return self._active_deadline_seconds

    @active_deadline_seconds.setter
    def active_deadline_seconds(self, active_deadline_seconds):
        """Sets the active_deadline_seconds of this V1PodSpec.


        :param active_deadline_seconds: The active_deadline_seconds of this V1PodSpec.  # noqa: E501
        :type: str
        """

        self._active_deadline_seconds = active_deadline_seconds

    @property
    def affinity(self):
        """Gets the affinity of this V1PodSpec.  # noqa: E501


        :return: The affinity of this V1PodSpec.  # noqa: E501
        :rtype: V1Affinity
        """
        return self._affinity

    @affinity.setter
    def affinity(self, affinity):
        """Sets the affinity of this V1PodSpec.


        :param affinity: The affinity of this V1PodSpec.  # noqa: E501
        :type: V1Affinity
        """

        self._affinity = affinity

    @property
    def automount_service_account_token(self):
        """Gets the automount_service_account_token of this V1PodSpec.  # noqa: E501


        :return: The automount_service_account_token of this V1PodSpec.  # noqa: E501
        :rtype: bool
        """
        return self._automount_service_account_token

    @automount_service_account_token.setter
    def automount_service_account_token(self, automount_service_account_token):
        """Sets the automount_service_account_token of this V1PodSpec.


        :param automount_service_account_token: The automount_service_account_token of this V1PodSpec.  # noqa: E501
        :type: bool
        """

        self._automount_service_account_token = automount_service_account_token

    @property
    def containers(self):
        """Gets the containers of this V1PodSpec.  # noqa: E501


        :return: The containers of this V1PodSpec.  # noqa: E501
        :rtype: list[V1Container]
        """
        return self._containers

    @containers.setter
    def containers(self, containers):
        """Sets the containers of this V1PodSpec.


        :param containers: The containers of this V1PodSpec.  # noqa: E501
        :type: list[V1Container]
        """

        self._containers = containers

    @property
    def dns_config(self):
        """Gets the dns_config of this V1PodSpec.  # noqa: E501


        :return: The dns_config of this V1PodSpec.  # noqa: E501
        :rtype: V1PodDNSConfig
        """
        return self._dns_config

    @dns_config.setter
    def dns_config(self, dns_config):
        """Sets the dns_config of this V1PodSpec.


        :param dns_config: The dns_config of this V1PodSpec.  # noqa: E501
        :type: V1PodDNSConfig
        """

        self._dns_config = dns_config

    @property
    def dns_policy(self):
        """Gets the dns_policy of this V1PodSpec.  # noqa: E501


        :return: The dns_policy of this V1PodSpec.  # noqa: E501
        :rtype: str
        """
        return self._dns_policy

    @dns_policy.setter
    def dns_policy(self, dns_policy):
        """Sets the dns_policy of this V1PodSpec.


        :param dns_policy: The dns_policy of this V1PodSpec.  # noqa: E501
        :type: str
        """

        self._dns_policy = dns_policy

    @property
    def enable_service_links(self):
        """Gets the enable_service_links of this V1PodSpec.  # noqa: E501


        :return: The enable_service_links of this V1PodSpec.  # noqa: E501
        :rtype: bool
        """
        return self._enable_service_links

    @enable_service_links.setter
    def enable_service_links(self, enable_service_links):
        """Sets the enable_service_links of this V1PodSpec.


        :param enable_service_links: The enable_service_links of this V1PodSpec.  # noqa: E501
        :type: bool
        """

        self._enable_service_links = enable_service_links

    @property
    def ephemeral_containers(self):
        """Gets the ephemeral_containers of this V1PodSpec.  # noqa: E501


        :return: The ephemeral_containers of this V1PodSpec.  # noqa: E501
        :rtype: list[V1EphemeralContainer]
        """
        return self._ephemeral_containers

    @ephemeral_containers.setter
    def ephemeral_containers(self, ephemeral_containers):
        """Sets the ephemeral_containers of this V1PodSpec.


        :param ephemeral_containers: The ephemeral_containers of this V1PodSpec.  # noqa: E501
        :type: list[V1EphemeralContainer]
        """

        self._ephemeral_containers = ephemeral_containers

    @property
    def host_aliases(self):
        """Gets the host_aliases of this V1PodSpec.  # noqa: E501


        :return: The host_aliases of this V1PodSpec.  # noqa: E501
        :rtype: list[V1HostAlias]
        """
        return self._host_aliases

    @host_aliases.setter
    def host_aliases(self, host_aliases):
        """Sets the host_aliases of this V1PodSpec.


        :param host_aliases: The host_aliases of this V1PodSpec.  # noqa: E501
        :type: list[V1HostAlias]
        """

        self._host_aliases = host_aliases

    @property
    def host_ipc(self):
        """Gets the host_ipc of this V1PodSpec.  # noqa: E501


        :return: The host_ipc of this V1PodSpec.  # noqa: E501
        :rtype: bool
        """
        return self._host_ipc

    @host_ipc.setter
    def host_ipc(self, host_ipc):
        """Sets the host_ipc of this V1PodSpec.


        :param host_ipc: The host_ipc of this V1PodSpec.  # noqa: E501
        :type: bool
        """

        self._host_ipc = host_ipc

    @property
    def host_network(self):
        """Gets the host_network of this V1PodSpec.  # noqa: E501


        :return: The host_network of this V1PodSpec.  # noqa: E501
        :rtype: bool
        """
        return self._host_network

    @host_network.setter
    def host_network(self, host_network):
        """Sets the host_network of this V1PodSpec.


        :param host_network: The host_network of this V1PodSpec.  # noqa: E501
        :type: bool
        """

        self._host_network = host_network

    @property
    def host_pid(self):
        """Gets the host_pid of this V1PodSpec.  # noqa: E501


        :return: The host_pid of this V1PodSpec.  # noqa: E501
        :rtype: bool
        """
        return self._host_pid

    @host_pid.setter
    def host_pid(self, host_pid):
        """Sets the host_pid of this V1PodSpec.


        :param host_pid: The host_pid of this V1PodSpec.  # noqa: E501
        :type: bool
        """

        self._host_pid = host_pid

    @property
    def host_users(self):
        """Gets the host_users of this V1PodSpec.  # noqa: E501


        :return: The host_users of this V1PodSpec.  # noqa: E501
        :rtype: bool
        """
        return self._host_users

    @host_users.setter
    def host_users(self, host_users):
        """Sets the host_users of this V1PodSpec.


        :param host_users: The host_users of this V1PodSpec.  # noqa: E501
        :type: bool
        """

        self._host_users = host_users

    @property
    def hostname(self):
        """Gets the hostname of this V1PodSpec.  # noqa: E501


        :return: The hostname of this V1PodSpec.  # noqa: E501
        :rtype: str
        """
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        """Sets the hostname of this V1PodSpec.


        :param hostname: The hostname of this V1PodSpec.  # noqa: E501
        :type: str
        """

        self._hostname = hostname

    @property
    def image_pull_secrets(self):
        """Gets the image_pull_secrets of this V1PodSpec.  # noqa: E501


        :return: The image_pull_secrets of this V1PodSpec.  # noqa: E501
        :rtype: list[V1LocalObjectReference]
        """
        return self._image_pull_secrets

    @image_pull_secrets.setter
    def image_pull_secrets(self, image_pull_secrets):
        """Sets the image_pull_secrets of this V1PodSpec.


        :param image_pull_secrets: The image_pull_secrets of this V1PodSpec.  # noqa: E501
        :type: list[V1LocalObjectReference]
        """

        self._image_pull_secrets = image_pull_secrets

    @property
    def init_containers(self):
        """Gets the init_containers of this V1PodSpec.  # noqa: E501


        :return: The init_containers of this V1PodSpec.  # noqa: E501
        :rtype: list[V1Container]
        """
        return self._init_containers

    @init_containers.setter
    def init_containers(self, init_containers):
        """Sets the init_containers of this V1PodSpec.


        :param init_containers: The init_containers of this V1PodSpec.  # noqa: E501
        :type: list[V1Container]
        """

        self._init_containers = init_containers

    @property
    def node_name(self):
        """Gets the node_name of this V1PodSpec.  # noqa: E501


        :return: The node_name of this V1PodSpec.  # noqa: E501
        :rtype: str
        """
        return self._node_name

    @node_name.setter
    def node_name(self, node_name):
        """Sets the node_name of this V1PodSpec.


        :param node_name: The node_name of this V1PodSpec.  # noqa: E501
        :type: str
        """

        self._node_name = node_name

    @property
    def node_selector(self):
        """Gets the node_selector of this V1PodSpec.  # noqa: E501


        :return: The node_selector of this V1PodSpec.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._node_selector

    @node_selector.setter
    def node_selector(self, node_selector):
        """Sets the node_selector of this V1PodSpec.


        :param node_selector: The node_selector of this V1PodSpec.  # noqa: E501
        :type: dict(str, str)
        """

        self._node_selector = node_selector

    @property
    def os(self):
        """Gets the os of this V1PodSpec.  # noqa: E501


        :return: The os of this V1PodSpec.  # noqa: E501
        :rtype: V1PodOS
        """
        return self._os

    @os.setter
    def os(self, os):
        """Sets the os of this V1PodSpec.


        :param os: The os of this V1PodSpec.  # noqa: E501
        :type: V1PodOS
        """

        self._os = os

    @property
    def overhead(self):
        """Gets the overhead of this V1PodSpec.  # noqa: E501


        :return: The overhead of this V1PodSpec.  # noqa: E501
        :rtype: dict(str, ResourceQuantity)
        """
        return self._overhead

    @overhead.setter
    def overhead(self, overhead):
        """Sets the overhead of this V1PodSpec.


        :param overhead: The overhead of this V1PodSpec.  # noqa: E501
        :type: dict(str, ResourceQuantity)
        """

        self._overhead = overhead

    @property
    def preemption_policy(self):
        """Gets the preemption_policy of this V1PodSpec.  # noqa: E501


        :return: The preemption_policy of this V1PodSpec.  # noqa: E501
        :rtype: str
        """
        return self._preemption_policy

    @preemption_policy.setter
    def preemption_policy(self, preemption_policy):
        """Sets the preemption_policy of this V1PodSpec.


        :param preemption_policy: The preemption_policy of this V1PodSpec.  # noqa: E501
        :type: str
        """

        self._preemption_policy = preemption_policy

    @property
    def priority(self):
        """Gets the priority of this V1PodSpec.  # noqa: E501


        :return: The priority of this V1PodSpec.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this V1PodSpec.


        :param priority: The priority of this V1PodSpec.  # noqa: E501
        :type: int
        """

        self._priority = priority

    @property
    def priority_class_name(self):
        """Gets the priority_class_name of this V1PodSpec.  # noqa: E501


        :return: The priority_class_name of this V1PodSpec.  # noqa: E501
        :rtype: str
        """
        return self._priority_class_name

    @priority_class_name.setter
    def priority_class_name(self, priority_class_name):
        """Sets the priority_class_name of this V1PodSpec.


        :param priority_class_name: The priority_class_name of this V1PodSpec.  # noqa: E501
        :type: str
        """

        self._priority_class_name = priority_class_name

    @property
    def readiness_gates(self):
        """Gets the readiness_gates of this V1PodSpec.  # noqa: E501


        :return: The readiness_gates of this V1PodSpec.  # noqa: E501
        :rtype: list[V1PodReadinessGate]
        """
        return self._readiness_gates

    @readiness_gates.setter
    def readiness_gates(self, readiness_gates):
        """Sets the readiness_gates of this V1PodSpec.


        :param readiness_gates: The readiness_gates of this V1PodSpec.  # noqa: E501
        :type: list[V1PodReadinessGate]
        """

        self._readiness_gates = readiness_gates

    @property
    def resource_claims(self):
        """Gets the resource_claims of this V1PodSpec.  # noqa: E501

        ResourceClaims defines which ResourceClaims must be allocated and reserved before the Pod is allowed to start. The resources will be made available to those containers which consume them by name.  This is an alpha field and requires enabling the DynamicResourceAllocation feature gate.  This field is immutable.  +patchMergeKey=name +patchStrategy=merge,retainKeys +listType=map +listMapKey=name +featureGate=DynamicResourceAllocation +optional  # noqa: E501

        :return: The resource_claims of this V1PodSpec.  # noqa: E501
        :rtype: list[V1PodResourceClaim]
        """
        return self._resource_claims

    @resource_claims.setter
    def resource_claims(self, resource_claims):
        """Sets the resource_claims of this V1PodSpec.

        ResourceClaims defines which ResourceClaims must be allocated and reserved before the Pod is allowed to start. The resources will be made available to those containers which consume them by name.  This is an alpha field and requires enabling the DynamicResourceAllocation feature gate.  This field is immutable.  +patchMergeKey=name +patchStrategy=merge,retainKeys +listType=map +listMapKey=name +featureGate=DynamicResourceAllocation +optional  # noqa: E501

        :param resource_claims: The resource_claims of this V1PodSpec.  # noqa: E501
        :type: list[V1PodResourceClaim]
        """

        self._resource_claims = resource_claims

    @property
    def resources(self):
        """Gets the resources of this V1PodSpec.  # noqa: E501


        :return: The resources of this V1PodSpec.  # noqa: E501
        :rtype: V1ResourceRequirements
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this V1PodSpec.


        :param resources: The resources of this V1PodSpec.  # noqa: E501
        :type: V1ResourceRequirements
        """

        self._resources = resources

    @property
    def restart_policy(self):
        """Gets the restart_policy of this V1PodSpec.  # noqa: E501


        :return: The restart_policy of this V1PodSpec.  # noqa: E501
        :rtype: str
        """
        return self._restart_policy

    @restart_policy.setter
    def restart_policy(self, restart_policy):
        """Sets the restart_policy of this V1PodSpec.


        :param restart_policy: The restart_policy of this V1PodSpec.  # noqa: E501
        :type: str
        """

        self._restart_policy = restart_policy

    @property
    def runtime_class_name(self):
        """Gets the runtime_class_name of this V1PodSpec.  # noqa: E501


        :return: The runtime_class_name of this V1PodSpec.  # noqa: E501
        :rtype: str
        """
        return self._runtime_class_name

    @runtime_class_name.setter
    def runtime_class_name(self, runtime_class_name):
        """Sets the runtime_class_name of this V1PodSpec.


        :param runtime_class_name: The runtime_class_name of this V1PodSpec.  # noqa: E501
        :type: str
        """

        self._runtime_class_name = runtime_class_name

    @property
    def scheduler_name(self):
        """Gets the scheduler_name of this V1PodSpec.  # noqa: E501


        :return: The scheduler_name of this V1PodSpec.  # noqa: E501
        :rtype: str
        """
        return self._scheduler_name

    @scheduler_name.setter
    def scheduler_name(self, scheduler_name):
        """Sets the scheduler_name of this V1PodSpec.


        :param scheduler_name: The scheduler_name of this V1PodSpec.  # noqa: E501
        :type: str
        """

        self._scheduler_name = scheduler_name

    @property
    def scheduling_gates(self):
        """Gets the scheduling_gates of this V1PodSpec.  # noqa: E501

        SchedulingGates is an opaque list of values that if specified will block scheduling the pod. If schedulingGates is not empty, the pod will stay in the SchedulingGated state and the scheduler will not attempt to schedule the pod.  SchedulingGates can only be set at pod creation time, and be removed only afterwards.  +patchMergeKey=name +patchStrategy=merge +listType=map +listMapKey=name +optional  # noqa: E501

        :return: The scheduling_gates of this V1PodSpec.  # noqa: E501
        :rtype: list[V1PodSchedulingGate]
        """
        return self._scheduling_gates

    @scheduling_gates.setter
    def scheduling_gates(self, scheduling_gates):
        """Sets the scheduling_gates of this V1PodSpec.

        SchedulingGates is an opaque list of values that if specified will block scheduling the pod. If schedulingGates is not empty, the pod will stay in the SchedulingGated state and the scheduler will not attempt to schedule the pod.  SchedulingGates can only be set at pod creation time, and be removed only afterwards.  +patchMergeKey=name +patchStrategy=merge +listType=map +listMapKey=name +optional  # noqa: E501

        :param scheduling_gates: The scheduling_gates of this V1PodSpec.  # noqa: E501
        :type: list[V1PodSchedulingGate]
        """

        self._scheduling_gates = scheduling_gates

    @property
    def security_context(self):
        """Gets the security_context of this V1PodSpec.  # noqa: E501


        :return: The security_context of this V1PodSpec.  # noqa: E501
        :rtype: V1PodSecurityContext
        """
        return self._security_context

    @security_context.setter
    def security_context(self, security_context):
        """Sets the security_context of this V1PodSpec.


        :param security_context: The security_context of this V1PodSpec.  # noqa: E501
        :type: V1PodSecurityContext
        """

        self._security_context = security_context

    @property
    def service_account(self):
        """Gets the service_account of this V1PodSpec.  # noqa: E501


        :return: The service_account of this V1PodSpec.  # noqa: E501
        :rtype: str
        """
        return self._service_account

    @service_account.setter
    def service_account(self, service_account):
        """Sets the service_account of this V1PodSpec.


        :param service_account: The service_account of this V1PodSpec.  # noqa: E501
        :type: str
        """

        self._service_account = service_account

    @property
    def service_account_name(self):
        """Gets the service_account_name of this V1PodSpec.  # noqa: E501


        :return: The service_account_name of this V1PodSpec.  # noqa: E501
        :rtype: str
        """
        return self._service_account_name

    @service_account_name.setter
    def service_account_name(self, service_account_name):
        """Sets the service_account_name of this V1PodSpec.


        :param service_account_name: The service_account_name of this V1PodSpec.  # noqa: E501
        :type: str
        """

        self._service_account_name = service_account_name

    @property
    def set_hostname_as_fqdn(self):
        """Gets the set_hostname_as_fqdn of this V1PodSpec.  # noqa: E501


        :return: The set_hostname_as_fqdn of this V1PodSpec.  # noqa: E501
        :rtype: bool
        """
        return self._set_hostname_as_fqdn

    @set_hostname_as_fqdn.setter
    def set_hostname_as_fqdn(self, set_hostname_as_fqdn):
        """Sets the set_hostname_as_fqdn of this V1PodSpec.


        :param set_hostname_as_fqdn: The set_hostname_as_fqdn of this V1PodSpec.  # noqa: E501
        :type: bool
        """

        self._set_hostname_as_fqdn = set_hostname_as_fqdn

    @property
    def share_process_namespace(self):
        """Gets the share_process_namespace of this V1PodSpec.  # noqa: E501


        :return: The share_process_namespace of this V1PodSpec.  # noqa: E501
        :rtype: bool
        """
        return self._share_process_namespace

    @share_process_namespace.setter
    def share_process_namespace(self, share_process_namespace):
        """Sets the share_process_namespace of this V1PodSpec.


        :param share_process_namespace: The share_process_namespace of this V1PodSpec.  # noqa: E501
        :type: bool
        """

        self._share_process_namespace = share_process_namespace

    @property
    def subdomain(self):
        """Gets the subdomain of this V1PodSpec.  # noqa: E501


        :return: The subdomain of this V1PodSpec.  # noqa: E501
        :rtype: str
        """
        return self._subdomain

    @subdomain.setter
    def subdomain(self, subdomain):
        """Sets the subdomain of this V1PodSpec.


        :param subdomain: The subdomain of this V1PodSpec.  # noqa: E501
        :type: str
        """

        self._subdomain = subdomain

    @property
    def termination_grace_period_seconds(self):
        """Gets the termination_grace_period_seconds of this V1PodSpec.  # noqa: E501


        :return: The termination_grace_period_seconds of this V1PodSpec.  # noqa: E501
        :rtype: str
        """
        return self._termination_grace_period_seconds

    @termination_grace_period_seconds.setter
    def termination_grace_period_seconds(self, termination_grace_period_seconds):
        """Sets the termination_grace_period_seconds of this V1PodSpec.


        :param termination_grace_period_seconds: The termination_grace_period_seconds of this V1PodSpec.  # noqa: E501
        :type: str
        """

        self._termination_grace_period_seconds = termination_grace_period_seconds

    @property
    def tolerations(self):
        """Gets the tolerations of this V1PodSpec.  # noqa: E501


        :return: The tolerations of this V1PodSpec.  # noqa: E501
        :rtype: list[V1Toleration]
        """
        return self._tolerations

    @tolerations.setter
    def tolerations(self, tolerations):
        """Sets the tolerations of this V1PodSpec.


        :param tolerations: The tolerations of this V1PodSpec.  # noqa: E501
        :type: list[V1Toleration]
        """

        self._tolerations = tolerations

    @property
    def topology_spread_constraints(self):
        """Gets the topology_spread_constraints of this V1PodSpec.  # noqa: E501


        :return: The topology_spread_constraints of this V1PodSpec.  # noqa: E501
        :rtype: list[V1TopologySpreadConstraint]
        """
        return self._topology_spread_constraints

    @topology_spread_constraints.setter
    def topology_spread_constraints(self, topology_spread_constraints):
        """Sets the topology_spread_constraints of this V1PodSpec.


        :param topology_spread_constraints: The topology_spread_constraints of this V1PodSpec.  # noqa: E501
        :type: list[V1TopologySpreadConstraint]
        """

        self._topology_spread_constraints = topology_spread_constraints

    @property
    def volumes(self):
        """Gets the volumes of this V1PodSpec.  # noqa: E501


        :return: The volumes of this V1PodSpec.  # noqa: E501
        :rtype: list[V1Volume]
        """
        return self._volumes

    @volumes.setter
    def volumes(self, volumes):
        """Sets the volumes of this V1PodSpec.


        :param volumes: The volumes of this V1PodSpec.  # noqa: E501
        :type: list[V1Volume]
        """

        self._volumes = volumes

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
        if issubclass(V1PodSpec, dict):
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
        if not isinstance(other, V1PodSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
