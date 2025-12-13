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

class ApplicationsApplicationSourceKustomize(object):
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
        'api_versions': 'list[str]',
        'common_annotations': 'dict(str, str)',
        'common_labels': 'dict(str, str)',
        'components': 'list[str]',
        'force_common_annotations': 'bool',
        'force_common_labels': 'bool',
        'images': 'list[str]',
        'kube_version': 'str',
        'label_without_selector': 'bool',
        'name_prefix': 'str',
        'name_suffix': 'str',
        'namespace': 'str',
        'patches': 'list[ApplicationsKustomizePatch]',
        'replicas': 'list[ApplicationsKustomizeReplicas]',
        'version': 'str'
    }

    attribute_map = {
        'api_versions': 'apiVersions',
        'common_annotations': 'commonAnnotations',
        'common_labels': 'commonLabels',
        'components': 'components',
        'force_common_annotations': 'forceCommonAnnotations',
        'force_common_labels': 'forceCommonLabels',
        'images': 'images',
        'kube_version': 'kubeVersion',
        'label_without_selector': 'labelWithoutSelector',
        'name_prefix': 'namePrefix',
        'name_suffix': 'nameSuffix',
        'namespace': 'namespace',
        'patches': 'patches',
        'replicas': 'replicas',
        'version': 'version'
    }

    def __init__(self, api_versions=None, common_annotations=None, common_labels=None, components=None, force_common_annotations=None, force_common_labels=None, images=None, kube_version=None, label_without_selector=None, name_prefix=None, name_suffix=None, namespace=None, patches=None, replicas=None, version=None):  # noqa: E501
        """ApplicationsApplicationSourceKustomize - a model defined in Swagger"""  # noqa: E501
        self._api_versions = None
        self._common_annotations = None
        self._common_labels = None
        self._components = None
        self._force_common_annotations = None
        self._force_common_labels = None
        self._images = None
        self._kube_version = None
        self._label_without_selector = None
        self._name_prefix = None
        self._name_suffix = None
        self._namespace = None
        self._patches = None
        self._replicas = None
        self._version = None
        self.discriminator = None
        if api_versions is not None:
            self.api_versions = api_versions
        if common_annotations is not None:
            self.common_annotations = common_annotations
        if common_labels is not None:
            self.common_labels = common_labels
        if components is not None:
            self.components = components
        if force_common_annotations is not None:
            self.force_common_annotations = force_common_annotations
        if force_common_labels is not None:
            self.force_common_labels = force_common_labels
        if images is not None:
            self.images = images
        if kube_version is not None:
            self.kube_version = kube_version
        if label_without_selector is not None:
            self.label_without_selector = label_without_selector
        if name_prefix is not None:
            self.name_prefix = name_prefix
        if name_suffix is not None:
            self.name_suffix = name_suffix
        if namespace is not None:
            self.namespace = namespace
        if patches is not None:
            self.patches = patches
        if replicas is not None:
            self.replicas = replicas
        if version is not None:
            self.version = version

    @property
    def api_versions(self):
        """Gets the api_versions of this ApplicationsApplicationSourceKustomize.  # noqa: E501

        APIVersions specifies the Kubernetes resource API versions to pass to Helm when templating manifests. By default, Argo CD uses the API versions of the target cluster. The format is [group/]version/kind.  # noqa: E501

        :return: The api_versions of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: list[str]
        """
        return self._api_versions

    @api_versions.setter
    def api_versions(self, api_versions):
        """Sets the api_versions of this ApplicationsApplicationSourceKustomize.

        APIVersions specifies the Kubernetes resource API versions to pass to Helm when templating manifests. By default, Argo CD uses the API versions of the target cluster. The format is [group/]version/kind.  # noqa: E501

        :param api_versions: The api_versions of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: list[str]
        """

        self._api_versions = api_versions

    @property
    def common_annotations(self):
        """Gets the common_annotations of this ApplicationsApplicationSourceKustomize.  # noqa: E501


        :return: The common_annotations of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._common_annotations

    @common_annotations.setter
    def common_annotations(self, common_annotations):
        """Sets the common_annotations of this ApplicationsApplicationSourceKustomize.


        :param common_annotations: The common_annotations of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: dict(str, str)
        """

        self._common_annotations = common_annotations

    @property
    def common_labels(self):
        """Gets the common_labels of this ApplicationsApplicationSourceKustomize.  # noqa: E501


        :return: The common_labels of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._common_labels

    @common_labels.setter
    def common_labels(self, common_labels):
        """Sets the common_labels of this ApplicationsApplicationSourceKustomize.


        :param common_labels: The common_labels of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: dict(str, str)
        """

        self._common_labels = common_labels

    @property
    def components(self):
        """Gets the components of this ApplicationsApplicationSourceKustomize.  # noqa: E501


        :return: The components of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: list[str]
        """
        return self._components

    @components.setter
    def components(self, components):
        """Sets the components of this ApplicationsApplicationSourceKustomize.


        :param components: The components of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: list[str]
        """

        self._components = components

    @property
    def force_common_annotations(self):
        """Gets the force_common_annotations of this ApplicationsApplicationSourceKustomize.  # noqa: E501


        :return: The force_common_annotations of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: bool
        """
        return self._force_common_annotations

    @force_common_annotations.setter
    def force_common_annotations(self, force_common_annotations):
        """Sets the force_common_annotations of this ApplicationsApplicationSourceKustomize.


        :param force_common_annotations: The force_common_annotations of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: bool
        """

        self._force_common_annotations = force_common_annotations

    @property
    def force_common_labels(self):
        """Gets the force_common_labels of this ApplicationsApplicationSourceKustomize.  # noqa: E501


        :return: The force_common_labels of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: bool
        """
        return self._force_common_labels

    @force_common_labels.setter
    def force_common_labels(self, force_common_labels):
        """Sets the force_common_labels of this ApplicationsApplicationSourceKustomize.


        :param force_common_labels: The force_common_labels of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: bool
        """

        self._force_common_labels = force_common_labels

    @property
    def images(self):
        """Gets the images of this ApplicationsApplicationSourceKustomize.  # noqa: E501


        :return: The images of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: list[str]
        """
        return self._images

    @images.setter
    def images(self, images):
        """Sets the images of this ApplicationsApplicationSourceKustomize.


        :param images: The images of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: list[str]
        """

        self._images = images

    @property
    def kube_version(self):
        """Gets the kube_version of this ApplicationsApplicationSourceKustomize.  # noqa: E501

        KubeVersion specifies the Kubernetes API version to pass to Helm when templating manifests. By default, Argo CD uses the Kubernetes version of the target cluster.  # noqa: E501

        :return: The kube_version of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: str
        """
        return self._kube_version

    @kube_version.setter
    def kube_version(self, kube_version):
        """Sets the kube_version of this ApplicationsApplicationSourceKustomize.

        KubeVersion specifies the Kubernetes API version to pass to Helm when templating manifests. By default, Argo CD uses the Kubernetes version of the target cluster.  # noqa: E501

        :param kube_version: The kube_version of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: str
        """

        self._kube_version = kube_version

    @property
    def label_without_selector(self):
        """Gets the label_without_selector of this ApplicationsApplicationSourceKustomize.  # noqa: E501


        :return: The label_without_selector of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: bool
        """
        return self._label_without_selector

    @label_without_selector.setter
    def label_without_selector(self, label_without_selector):
        """Sets the label_without_selector of this ApplicationsApplicationSourceKustomize.


        :param label_without_selector: The label_without_selector of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: bool
        """

        self._label_without_selector = label_without_selector

    @property
    def name_prefix(self):
        """Gets the name_prefix of this ApplicationsApplicationSourceKustomize.  # noqa: E501


        :return: The name_prefix of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: str
        """
        return self._name_prefix

    @name_prefix.setter
    def name_prefix(self, name_prefix):
        """Sets the name_prefix of this ApplicationsApplicationSourceKustomize.


        :param name_prefix: The name_prefix of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: str
        """

        self._name_prefix = name_prefix

    @property
    def name_suffix(self):
        """Gets the name_suffix of this ApplicationsApplicationSourceKustomize.  # noqa: E501


        :return: The name_suffix of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: str
        """
        return self._name_suffix

    @name_suffix.setter
    def name_suffix(self, name_suffix):
        """Sets the name_suffix of this ApplicationsApplicationSourceKustomize.


        :param name_suffix: The name_suffix of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: str
        """

        self._name_suffix = name_suffix

    @property
    def namespace(self):
        """Gets the namespace of this ApplicationsApplicationSourceKustomize.  # noqa: E501


        :return: The namespace of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this ApplicationsApplicationSourceKustomize.


        :param namespace: The namespace of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def patches(self):
        """Gets the patches of this ApplicationsApplicationSourceKustomize.  # noqa: E501


        :return: The patches of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: list[ApplicationsKustomizePatch]
        """
        return self._patches

    @patches.setter
    def patches(self, patches):
        """Sets the patches of this ApplicationsApplicationSourceKustomize.


        :param patches: The patches of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: list[ApplicationsKustomizePatch]
        """

        self._patches = patches

    @property
    def replicas(self):
        """Gets the replicas of this ApplicationsApplicationSourceKustomize.  # noqa: E501


        :return: The replicas of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: list[ApplicationsKustomizeReplicas]
        """
        return self._replicas

    @replicas.setter
    def replicas(self, replicas):
        """Sets the replicas of this ApplicationsApplicationSourceKustomize.


        :param replicas: The replicas of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: list[ApplicationsKustomizeReplicas]
        """

        self._replicas = replicas

    @property
    def version(self):
        """Gets the version of this ApplicationsApplicationSourceKustomize.  # noqa: E501


        :return: The version of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ApplicationsApplicationSourceKustomize.


        :param version: The version of this ApplicationsApplicationSourceKustomize.  # noqa: E501
        :type: str
        """

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
        if issubclass(ApplicationsApplicationSourceKustomize, dict):
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
        if not isinstance(other, ApplicationsApplicationSourceKustomize):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
