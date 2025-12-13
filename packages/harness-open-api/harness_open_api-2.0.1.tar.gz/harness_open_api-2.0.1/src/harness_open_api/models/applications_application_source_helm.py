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

class ApplicationsApplicationSourceHelm(object):
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
        'file_parameters': 'list[ApplicationsHelmFileParameter]',
        'ignore_missing_value_files': 'bool',
        'kube_version': 'str',
        'namespace': 'str',
        'parameters': 'list[ApplicationsHelmParameter]',
        'pass_credentials': 'bool',
        'release_name': 'str',
        'skip_crds': 'bool',
        'skip_schema_validation': 'bool',
        'skip_tests': 'bool',
        'value_files': 'list[str]',
        'values': 'str',
        'values_object': 'object',
        'version': 'str'
    }

    attribute_map = {
        'api_versions': 'apiVersions',
        'file_parameters': 'fileParameters',
        'ignore_missing_value_files': 'ignoreMissingValueFiles',
        'kube_version': 'kubeVersion',
        'namespace': 'namespace',
        'parameters': 'parameters',
        'pass_credentials': 'passCredentials',
        'release_name': 'releaseName',
        'skip_crds': 'skipCrds',
        'skip_schema_validation': 'skipSchemaValidation',
        'skip_tests': 'skipTests',
        'value_files': 'valueFiles',
        'values': 'values',
        'values_object': 'valuesObject',
        'version': 'version'
    }

    def __init__(self, api_versions=None, file_parameters=None, ignore_missing_value_files=None, kube_version=None, namespace=None, parameters=None, pass_credentials=None, release_name=None, skip_crds=None, skip_schema_validation=None, skip_tests=None, value_files=None, values=None, values_object=None, version=None):  # noqa: E501
        """ApplicationsApplicationSourceHelm - a model defined in Swagger"""  # noqa: E501
        self._api_versions = None
        self._file_parameters = None
        self._ignore_missing_value_files = None
        self._kube_version = None
        self._namespace = None
        self._parameters = None
        self._pass_credentials = None
        self._release_name = None
        self._skip_crds = None
        self._skip_schema_validation = None
        self._skip_tests = None
        self._value_files = None
        self._values = None
        self._values_object = None
        self._version = None
        self.discriminator = None
        if api_versions is not None:
            self.api_versions = api_versions
        if file_parameters is not None:
            self.file_parameters = file_parameters
        if ignore_missing_value_files is not None:
            self.ignore_missing_value_files = ignore_missing_value_files
        if kube_version is not None:
            self.kube_version = kube_version
        if namespace is not None:
            self.namespace = namespace
        if parameters is not None:
            self.parameters = parameters
        if pass_credentials is not None:
            self.pass_credentials = pass_credentials
        if release_name is not None:
            self.release_name = release_name
        if skip_crds is not None:
            self.skip_crds = skip_crds
        if skip_schema_validation is not None:
            self.skip_schema_validation = skip_schema_validation
        if skip_tests is not None:
            self.skip_tests = skip_tests
        if value_files is not None:
            self.value_files = value_files
        if values is not None:
            self.values = values
        if values_object is not None:
            self.values_object = values_object
        if version is not None:
            self.version = version

    @property
    def api_versions(self):
        """Gets the api_versions of this ApplicationsApplicationSourceHelm.  # noqa: E501

        APIVersions specifies the Kubernetes resource API versions to pass to Helm when templating manifests. By default, Argo CD uses the API versions of the target cluster. The format is [group/]version/kind.  # noqa: E501

        :return: The api_versions of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: list[str]
        """
        return self._api_versions

    @api_versions.setter
    def api_versions(self, api_versions):
        """Sets the api_versions of this ApplicationsApplicationSourceHelm.

        APIVersions specifies the Kubernetes resource API versions to pass to Helm when templating manifests. By default, Argo CD uses the API versions of the target cluster. The format is [group/]version/kind.  # noqa: E501

        :param api_versions: The api_versions of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: list[str]
        """

        self._api_versions = api_versions

    @property
    def file_parameters(self):
        """Gets the file_parameters of this ApplicationsApplicationSourceHelm.  # noqa: E501


        :return: The file_parameters of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: list[ApplicationsHelmFileParameter]
        """
        return self._file_parameters

    @file_parameters.setter
    def file_parameters(self, file_parameters):
        """Sets the file_parameters of this ApplicationsApplicationSourceHelm.


        :param file_parameters: The file_parameters of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: list[ApplicationsHelmFileParameter]
        """

        self._file_parameters = file_parameters

    @property
    def ignore_missing_value_files(self):
        """Gets the ignore_missing_value_files of this ApplicationsApplicationSourceHelm.  # noqa: E501


        :return: The ignore_missing_value_files of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: bool
        """
        return self._ignore_missing_value_files

    @ignore_missing_value_files.setter
    def ignore_missing_value_files(self, ignore_missing_value_files):
        """Sets the ignore_missing_value_files of this ApplicationsApplicationSourceHelm.


        :param ignore_missing_value_files: The ignore_missing_value_files of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: bool
        """

        self._ignore_missing_value_files = ignore_missing_value_files

    @property
    def kube_version(self):
        """Gets the kube_version of this ApplicationsApplicationSourceHelm.  # noqa: E501

        KubeVersion specifies the Kubernetes API version to pass to Helm when templating manifests. By default, Argo CD uses the Kubernetes version of the target cluster.  # noqa: E501

        :return: The kube_version of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: str
        """
        return self._kube_version

    @kube_version.setter
    def kube_version(self, kube_version):
        """Sets the kube_version of this ApplicationsApplicationSourceHelm.

        KubeVersion specifies the Kubernetes API version to pass to Helm when templating manifests. By default, Argo CD uses the Kubernetes version of the target cluster.  # noqa: E501

        :param kube_version: The kube_version of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: str
        """

        self._kube_version = kube_version

    @property
    def namespace(self):
        """Gets the namespace of this ApplicationsApplicationSourceHelm.  # noqa: E501

        Namespace is an optional namespace to template with. If left empty, defaults to the app's destination namespace.  # noqa: E501

        :return: The namespace of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this ApplicationsApplicationSourceHelm.

        Namespace is an optional namespace to template with. If left empty, defaults to the app's destination namespace.  # noqa: E501

        :param namespace: The namespace of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def parameters(self):
        """Gets the parameters of this ApplicationsApplicationSourceHelm.  # noqa: E501


        :return: The parameters of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: list[ApplicationsHelmParameter]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this ApplicationsApplicationSourceHelm.


        :param parameters: The parameters of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: list[ApplicationsHelmParameter]
        """

        self._parameters = parameters

    @property
    def pass_credentials(self):
        """Gets the pass_credentials of this ApplicationsApplicationSourceHelm.  # noqa: E501


        :return: The pass_credentials of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: bool
        """
        return self._pass_credentials

    @pass_credentials.setter
    def pass_credentials(self, pass_credentials):
        """Sets the pass_credentials of this ApplicationsApplicationSourceHelm.


        :param pass_credentials: The pass_credentials of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: bool
        """

        self._pass_credentials = pass_credentials

    @property
    def release_name(self):
        """Gets the release_name of this ApplicationsApplicationSourceHelm.  # noqa: E501


        :return: The release_name of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: str
        """
        return self._release_name

    @release_name.setter
    def release_name(self, release_name):
        """Sets the release_name of this ApplicationsApplicationSourceHelm.


        :param release_name: The release_name of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: str
        """

        self._release_name = release_name

    @property
    def skip_crds(self):
        """Gets the skip_crds of this ApplicationsApplicationSourceHelm.  # noqa: E501


        :return: The skip_crds of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: bool
        """
        return self._skip_crds

    @skip_crds.setter
    def skip_crds(self, skip_crds):
        """Sets the skip_crds of this ApplicationsApplicationSourceHelm.


        :param skip_crds: The skip_crds of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: bool
        """

        self._skip_crds = skip_crds

    @property
    def skip_schema_validation(self):
        """Gets the skip_schema_validation of this ApplicationsApplicationSourceHelm.  # noqa: E501


        :return: The skip_schema_validation of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: bool
        """
        return self._skip_schema_validation

    @skip_schema_validation.setter
    def skip_schema_validation(self, skip_schema_validation):
        """Sets the skip_schema_validation of this ApplicationsApplicationSourceHelm.


        :param skip_schema_validation: The skip_schema_validation of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: bool
        """

        self._skip_schema_validation = skip_schema_validation

    @property
    def skip_tests(self):
        """Gets the skip_tests of this ApplicationsApplicationSourceHelm.  # noqa: E501

        SkipTests skips test manifest installation step (Helm's --skip-tests).  # noqa: E501

        :return: The skip_tests of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: bool
        """
        return self._skip_tests

    @skip_tests.setter
    def skip_tests(self, skip_tests):
        """Sets the skip_tests of this ApplicationsApplicationSourceHelm.

        SkipTests skips test manifest installation step (Helm's --skip-tests).  # noqa: E501

        :param skip_tests: The skip_tests of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: bool
        """

        self._skip_tests = skip_tests

    @property
    def value_files(self):
        """Gets the value_files of this ApplicationsApplicationSourceHelm.  # noqa: E501


        :return: The value_files of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: list[str]
        """
        return self._value_files

    @value_files.setter
    def value_files(self, value_files):
        """Sets the value_files of this ApplicationsApplicationSourceHelm.


        :param value_files: The value_files of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: list[str]
        """

        self._value_files = value_files

    @property
    def values(self):
        """Gets the values of this ApplicationsApplicationSourceHelm.  # noqa: E501


        :return: The values of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: str
        """
        return self._values

    @values.setter
    def values(self, values):
        """Sets the values of this ApplicationsApplicationSourceHelm.


        :param values: The values of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: str
        """

        self._values = values

    @property
    def values_object(self):
        """Gets the values_object of this ApplicationsApplicationSourceHelm.  # noqa: E501


        :return: The values_object of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: object
        """
        return self._values_object

    @values_object.setter
    def values_object(self, values_object):
        """Sets the values_object of this ApplicationsApplicationSourceHelm.


        :param values_object: The values_object of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :type: object
        """

        self._values_object = values_object

    @property
    def version(self):
        """Gets the version of this ApplicationsApplicationSourceHelm.  # noqa: E501


        :return: The version of this ApplicationsApplicationSourceHelm.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ApplicationsApplicationSourceHelm.


        :param version: The version of this ApplicationsApplicationSourceHelm.  # noqa: E501
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
        if issubclass(ApplicationsApplicationSourceHelm, dict):
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
        if not isinstance(other, ApplicationsApplicationSourceHelm):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
