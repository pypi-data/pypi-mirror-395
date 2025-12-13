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

class V1PodSecurityContext(object):
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
        'app_armor_profile': 'V1AppArmorProfile',
        'fs_group': 'str',
        'fs_group_change_policy': 'str',
        'run_as_group': 'str',
        'run_as_non_root': 'bool',
        'run_as_user': 'str',
        'se_linux_change_policy': 'str',
        'se_linux_options': 'V1SELinuxOptions',
        'seccomp_profile': 'V1SeccompProfile',
        'supplemental_groups': 'list[str]',
        'supplemental_groups_policy': 'str',
        'sysctls': 'list[V1Sysctl]',
        'windows_options': 'V1WindowsSecurityContextOptions'
    }

    attribute_map = {
        'app_armor_profile': 'appArmorProfile',
        'fs_group': 'fsGroup',
        'fs_group_change_policy': 'fsGroupChangePolicy',
        'run_as_group': 'runAsGroup',
        'run_as_non_root': 'runAsNonRoot',
        'run_as_user': 'runAsUser',
        'se_linux_change_policy': 'seLinuxChangePolicy',
        'se_linux_options': 'seLinuxOptions',
        'seccomp_profile': 'seccompProfile',
        'supplemental_groups': 'supplementalGroups',
        'supplemental_groups_policy': 'supplementalGroupsPolicy',
        'sysctls': 'sysctls',
        'windows_options': 'windowsOptions'
    }

    def __init__(self, app_armor_profile=None, fs_group=None, fs_group_change_policy=None, run_as_group=None, run_as_non_root=None, run_as_user=None, se_linux_change_policy=None, se_linux_options=None, seccomp_profile=None, supplemental_groups=None, supplemental_groups_policy=None, sysctls=None, windows_options=None):  # noqa: E501
        """V1PodSecurityContext - a model defined in Swagger"""  # noqa: E501
        self._app_armor_profile = None
        self._fs_group = None
        self._fs_group_change_policy = None
        self._run_as_group = None
        self._run_as_non_root = None
        self._run_as_user = None
        self._se_linux_change_policy = None
        self._se_linux_options = None
        self._seccomp_profile = None
        self._supplemental_groups = None
        self._supplemental_groups_policy = None
        self._sysctls = None
        self._windows_options = None
        self.discriminator = None
        if app_armor_profile is not None:
            self.app_armor_profile = app_armor_profile
        if fs_group is not None:
            self.fs_group = fs_group
        if fs_group_change_policy is not None:
            self.fs_group_change_policy = fs_group_change_policy
        if run_as_group is not None:
            self.run_as_group = run_as_group
        if run_as_non_root is not None:
            self.run_as_non_root = run_as_non_root
        if run_as_user is not None:
            self.run_as_user = run_as_user
        if se_linux_change_policy is not None:
            self.se_linux_change_policy = se_linux_change_policy
        if se_linux_options is not None:
            self.se_linux_options = se_linux_options
        if seccomp_profile is not None:
            self.seccomp_profile = seccomp_profile
        if supplemental_groups is not None:
            self.supplemental_groups = supplemental_groups
        if supplemental_groups_policy is not None:
            self.supplemental_groups_policy = supplemental_groups_policy
        if sysctls is not None:
            self.sysctls = sysctls
        if windows_options is not None:
            self.windows_options = windows_options

    @property
    def app_armor_profile(self):
        """Gets the app_armor_profile of this V1PodSecurityContext.  # noqa: E501


        :return: The app_armor_profile of this V1PodSecurityContext.  # noqa: E501
        :rtype: V1AppArmorProfile
        """
        return self._app_armor_profile

    @app_armor_profile.setter
    def app_armor_profile(self, app_armor_profile):
        """Sets the app_armor_profile of this V1PodSecurityContext.


        :param app_armor_profile: The app_armor_profile of this V1PodSecurityContext.  # noqa: E501
        :type: V1AppArmorProfile
        """

        self._app_armor_profile = app_armor_profile

    @property
    def fs_group(self):
        """Gets the fs_group of this V1PodSecurityContext.  # noqa: E501

        1. The owning GID will be the FSGroup 2. The setgid bit is set (new files created in the volume will be owned by FSGroup) 3. The permission bits are OR'd with rw-rw----  If unset, the Kubelet will not modify the ownership and permissions of any volume. Note that this field cannot be set when spec.os.name is windows. +optional  # noqa: E501

        :return: The fs_group of this V1PodSecurityContext.  # noqa: E501
        :rtype: str
        """
        return self._fs_group

    @fs_group.setter
    def fs_group(self, fs_group):
        """Sets the fs_group of this V1PodSecurityContext.

        1. The owning GID will be the FSGroup 2. The setgid bit is set (new files created in the volume will be owned by FSGroup) 3. The permission bits are OR'd with rw-rw----  If unset, the Kubelet will not modify the ownership and permissions of any volume. Note that this field cannot be set when spec.os.name is windows. +optional  # noqa: E501

        :param fs_group: The fs_group of this V1PodSecurityContext.  # noqa: E501
        :type: str
        """

        self._fs_group = fs_group

    @property
    def fs_group_change_policy(self):
        """Gets the fs_group_change_policy of this V1PodSecurityContext.  # noqa: E501


        :return: The fs_group_change_policy of this V1PodSecurityContext.  # noqa: E501
        :rtype: str
        """
        return self._fs_group_change_policy

    @fs_group_change_policy.setter
    def fs_group_change_policy(self, fs_group_change_policy):
        """Sets the fs_group_change_policy of this V1PodSecurityContext.


        :param fs_group_change_policy: The fs_group_change_policy of this V1PodSecurityContext.  # noqa: E501
        :type: str
        """

        self._fs_group_change_policy = fs_group_change_policy

    @property
    def run_as_group(self):
        """Gets the run_as_group of this V1PodSecurityContext.  # noqa: E501


        :return: The run_as_group of this V1PodSecurityContext.  # noqa: E501
        :rtype: str
        """
        return self._run_as_group

    @run_as_group.setter
    def run_as_group(self, run_as_group):
        """Sets the run_as_group of this V1PodSecurityContext.


        :param run_as_group: The run_as_group of this V1PodSecurityContext.  # noqa: E501
        :type: str
        """

        self._run_as_group = run_as_group

    @property
    def run_as_non_root(self):
        """Gets the run_as_non_root of this V1PodSecurityContext.  # noqa: E501


        :return: The run_as_non_root of this V1PodSecurityContext.  # noqa: E501
        :rtype: bool
        """
        return self._run_as_non_root

    @run_as_non_root.setter
    def run_as_non_root(self, run_as_non_root):
        """Sets the run_as_non_root of this V1PodSecurityContext.


        :param run_as_non_root: The run_as_non_root of this V1PodSecurityContext.  # noqa: E501
        :type: bool
        """

        self._run_as_non_root = run_as_non_root

    @property
    def run_as_user(self):
        """Gets the run_as_user of this V1PodSecurityContext.  # noqa: E501


        :return: The run_as_user of this V1PodSecurityContext.  # noqa: E501
        :rtype: str
        """
        return self._run_as_user

    @run_as_user.setter
    def run_as_user(self, run_as_user):
        """Sets the run_as_user of this V1PodSecurityContext.


        :param run_as_user: The run_as_user of this V1PodSecurityContext.  # noqa: E501
        :type: str
        """

        self._run_as_user = run_as_user

    @property
    def se_linux_change_policy(self):
        """Gets the se_linux_change_policy of this V1PodSecurityContext.  # noqa: E501

        seLinuxChangePolicy defines how the container's SELinux label is applied to all volumes used by the Pod. It has no effect on nodes that do not support SELinux or to volumes does not support SELinux. Valid values are \"MountOption\" and \"Recursive\".  \"Recursive\" means relabeling of all files on all Pod volumes by the container runtime. This may be slow for large volumes, but allows mixing privileged and unprivileged Pods sharing the same volume on the same node.  \"MountOption\" mounts all eligible Pod volumes with `-o context` mount option. This requires all Pods that share the same volume to use the same SELinux label. It is not possible to share the same volume among privileged and unprivileged Pods. Eligible volumes are in-tree FibreChannel and iSCSI volumes, and all CSI volumes whose CSI driver announces SELinux support by setting spec.seLinuxMount: true in their CSIDriver instance. Other volumes are always re-labelled recursively. \"MountOption\" value is allowed only when SELinuxMount feature gate is enabled.  If not specified and SELinuxMount feature gate is enabled, \"MountOption\" is used. If not specified and SELinuxMount feature gate is disabled, \"MountOption\" is used for ReadWriteOncePod volumes and \"Recursive\" for all other volumes.  This field affects only Pods that have SELinux label set, either in PodSecurityContext or in SecurityContext of all containers.  All Pods that use the same volume should use the same seLinuxChangePolicy, otherwise some pods can get stuck in ContainerCreating state. Note that this field cannot be set when spec.os.name is windows. +featureGate=SELinuxChangePolicy +optional  # noqa: E501

        :return: The se_linux_change_policy of this V1PodSecurityContext.  # noqa: E501
        :rtype: str
        """
        return self._se_linux_change_policy

    @se_linux_change_policy.setter
    def se_linux_change_policy(self, se_linux_change_policy):
        """Sets the se_linux_change_policy of this V1PodSecurityContext.

        seLinuxChangePolicy defines how the container's SELinux label is applied to all volumes used by the Pod. It has no effect on nodes that do not support SELinux or to volumes does not support SELinux. Valid values are \"MountOption\" and \"Recursive\".  \"Recursive\" means relabeling of all files on all Pod volumes by the container runtime. This may be slow for large volumes, but allows mixing privileged and unprivileged Pods sharing the same volume on the same node.  \"MountOption\" mounts all eligible Pod volumes with `-o context` mount option. This requires all Pods that share the same volume to use the same SELinux label. It is not possible to share the same volume among privileged and unprivileged Pods. Eligible volumes are in-tree FibreChannel and iSCSI volumes, and all CSI volumes whose CSI driver announces SELinux support by setting spec.seLinuxMount: true in their CSIDriver instance. Other volumes are always re-labelled recursively. \"MountOption\" value is allowed only when SELinuxMount feature gate is enabled.  If not specified and SELinuxMount feature gate is enabled, \"MountOption\" is used. If not specified and SELinuxMount feature gate is disabled, \"MountOption\" is used for ReadWriteOncePod volumes and \"Recursive\" for all other volumes.  This field affects only Pods that have SELinux label set, either in PodSecurityContext or in SecurityContext of all containers.  All Pods that use the same volume should use the same seLinuxChangePolicy, otherwise some pods can get stuck in ContainerCreating state. Note that this field cannot be set when spec.os.name is windows. +featureGate=SELinuxChangePolicy +optional  # noqa: E501

        :param se_linux_change_policy: The se_linux_change_policy of this V1PodSecurityContext.  # noqa: E501
        :type: str
        """

        self._se_linux_change_policy = se_linux_change_policy

    @property
    def se_linux_options(self):
        """Gets the se_linux_options of this V1PodSecurityContext.  # noqa: E501


        :return: The se_linux_options of this V1PodSecurityContext.  # noqa: E501
        :rtype: V1SELinuxOptions
        """
        return self._se_linux_options

    @se_linux_options.setter
    def se_linux_options(self, se_linux_options):
        """Sets the se_linux_options of this V1PodSecurityContext.


        :param se_linux_options: The se_linux_options of this V1PodSecurityContext.  # noqa: E501
        :type: V1SELinuxOptions
        """

        self._se_linux_options = se_linux_options

    @property
    def seccomp_profile(self):
        """Gets the seccomp_profile of this V1PodSecurityContext.  # noqa: E501


        :return: The seccomp_profile of this V1PodSecurityContext.  # noqa: E501
        :rtype: V1SeccompProfile
        """
        return self._seccomp_profile

    @seccomp_profile.setter
    def seccomp_profile(self, seccomp_profile):
        """Sets the seccomp_profile of this V1PodSecurityContext.


        :param seccomp_profile: The seccomp_profile of this V1PodSecurityContext.  # noqa: E501
        :type: V1SeccompProfile
        """

        self._seccomp_profile = seccomp_profile

    @property
    def supplemental_groups(self):
        """Gets the supplemental_groups of this V1PodSecurityContext.  # noqa: E501


        :return: The supplemental_groups of this V1PodSecurityContext.  # noqa: E501
        :rtype: list[str]
        """
        return self._supplemental_groups

    @supplemental_groups.setter
    def supplemental_groups(self, supplemental_groups):
        """Sets the supplemental_groups of this V1PodSecurityContext.


        :param supplemental_groups: The supplemental_groups of this V1PodSecurityContext.  # noqa: E501
        :type: list[str]
        """

        self._supplemental_groups = supplemental_groups

    @property
    def supplemental_groups_policy(self):
        """Gets the supplemental_groups_policy of this V1PodSecurityContext.  # noqa: E501


        :return: The supplemental_groups_policy of this V1PodSecurityContext.  # noqa: E501
        :rtype: str
        """
        return self._supplemental_groups_policy

    @supplemental_groups_policy.setter
    def supplemental_groups_policy(self, supplemental_groups_policy):
        """Sets the supplemental_groups_policy of this V1PodSecurityContext.


        :param supplemental_groups_policy: The supplemental_groups_policy of this V1PodSecurityContext.  # noqa: E501
        :type: str
        """

        self._supplemental_groups_policy = supplemental_groups_policy

    @property
    def sysctls(self):
        """Gets the sysctls of this V1PodSecurityContext.  # noqa: E501


        :return: The sysctls of this V1PodSecurityContext.  # noqa: E501
        :rtype: list[V1Sysctl]
        """
        return self._sysctls

    @sysctls.setter
    def sysctls(self, sysctls):
        """Sets the sysctls of this V1PodSecurityContext.


        :param sysctls: The sysctls of this V1PodSecurityContext.  # noqa: E501
        :type: list[V1Sysctl]
        """

        self._sysctls = sysctls

    @property
    def windows_options(self):
        """Gets the windows_options of this V1PodSecurityContext.  # noqa: E501


        :return: The windows_options of this V1PodSecurityContext.  # noqa: E501
        :rtype: V1WindowsSecurityContextOptions
        """
        return self._windows_options

    @windows_options.setter
    def windows_options(self, windows_options):
        """Sets the windows_options of this V1PodSecurityContext.


        :param windows_options: The windows_options of this V1PodSecurityContext.  # noqa: E501
        :type: V1WindowsSecurityContextOptions
        """

        self._windows_options = windows_options

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
        if issubclass(V1PodSecurityContext, dict):
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
        if not isinstance(other, V1PodSecurityContext):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
