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

class CreateComplianceResultV2(object):
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
        'default_branch': 'str',
        'full_fqn': 'str',
        'name': 'str',
        'org': 'str',
        'pipeline_execution_identifier': 'str',
        'pipeline_identifier': 'str',
        'plugins': 'list[PluginDTO]',
        'results': 'list[ComplianceResult]',
        'scan_type': 'ComplianceScanType',
        'source_platform': 'str',
        'stage_execution_identifier': 'str',
        'stage_type': 'str',
        'step_execution_identifier': 'str',
        'url': 'str'
    }

    attribute_map = {
        'default_branch': 'default_branch',
        'full_fqn': 'full_fqn',
        'name': 'name',
        'org': 'org',
        'pipeline_execution_identifier': 'pipeline_execution_identifier',
        'pipeline_identifier': 'pipeline_identifier',
        'plugins': 'plugins',
        'results': 'results',
        'scan_type': 'scan_type',
        'source_platform': 'source_platform',
        'stage_execution_identifier': 'stage_execution_identifier',
        'stage_type': 'stage_type',
        'step_execution_identifier': 'step_execution_identifier',
        'url': 'url'
    }

    def __init__(self, default_branch=None, full_fqn=None, name=None, org=None, pipeline_execution_identifier=None, pipeline_identifier=None, plugins=None, results=None, scan_type=None, source_platform=None, stage_execution_identifier=None, stage_type=None, step_execution_identifier=None, url=None):  # noqa: E501
        """CreateComplianceResultV2 - a model defined in Swagger"""  # noqa: E501
        self._default_branch = None
        self._full_fqn = None
        self._name = None
        self._org = None
        self._pipeline_execution_identifier = None
        self._pipeline_identifier = None
        self._plugins = None
        self._results = None
        self._scan_type = None
        self._source_platform = None
        self._stage_execution_identifier = None
        self._stage_type = None
        self._step_execution_identifier = None
        self._url = None
        self.discriminator = None
        if default_branch is not None:
            self.default_branch = default_branch
        if full_fqn is not None:
            self.full_fqn = full_fqn
        self.name = name
        if org is not None:
            self.org = org
        if pipeline_execution_identifier is not None:
            self.pipeline_execution_identifier = pipeline_execution_identifier
        if pipeline_identifier is not None:
            self.pipeline_identifier = pipeline_identifier
        if plugins is not None:
            self.plugins = plugins
        self.results = results
        self.scan_type = scan_type
        self.source_platform = source_platform
        if stage_execution_identifier is not None:
            self.stage_execution_identifier = stage_execution_identifier
        if stage_type is not None:
            self.stage_type = stage_type
        if step_execution_identifier is not None:
            self.step_execution_identifier = step_execution_identifier
        self.url = url

    @property
    def default_branch(self):
        """Gets the default_branch of this CreateComplianceResultV2.  # noqa: E501

        Branch for scan.  # noqa: E501

        :return: The default_branch of this CreateComplianceResultV2.  # noqa: E501
        :rtype: str
        """
        return self._default_branch

    @default_branch.setter
    def default_branch(self, default_branch):
        """Sets the default_branch of this CreateComplianceResultV2.

        Branch for scan.  # noqa: E501

        :param default_branch: The default_branch of this CreateComplianceResultV2.  # noqa: E501
        :type: str
        """

        self._default_branch = default_branch

    @property
    def full_fqn(self):
        """Gets the full_fqn of this CreateComplianceResultV2.  # noqa: E501

        Fully qualified name of entity.  Uses entire URL and name to depict same.  # noqa: E501

        :return: The full_fqn of this CreateComplianceResultV2.  # noqa: E501
        :rtype: str
        """
        return self._full_fqn

    @full_fqn.setter
    def full_fqn(self, full_fqn):
        """Sets the full_fqn of this CreateComplianceResultV2.

        Fully qualified name of entity.  Uses entire URL and name to depict same.  # noqa: E501

        :param full_fqn: The full_fqn of this CreateComplianceResultV2.  # noqa: E501
        :type: str
        """

        self._full_fqn = full_fqn

    @property
    def name(self):
        """Gets the name of this CreateComplianceResultV2.  # noqa: E501

        Name of entity for compliance results.  # noqa: E501

        :return: The name of this CreateComplianceResultV2.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateComplianceResultV2.

        Name of entity for compliance results.  # noqa: E501

        :param name: The name of this CreateComplianceResultV2.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def org(self):
        """Gets the org of this CreateComplianceResultV2.  # noqa: E501

        Represents organization.  # noqa: E501

        :return: The org of this CreateComplianceResultV2.  # noqa: E501
        :rtype: str
        """
        return self._org

    @org.setter
    def org(self, org):
        """Sets the org of this CreateComplianceResultV2.

        Represents organization.  # noqa: E501

        :param org: The org of this CreateComplianceResultV2.  # noqa: E501
        :type: str
        """

        self._org = org

    @property
    def pipeline_execution_identifier(self):
        """Gets the pipeline_execution_identifier of this CreateComplianceResultV2.  # noqa: E501


        :return: The pipeline_execution_identifier of this CreateComplianceResultV2.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_execution_identifier

    @pipeline_execution_identifier.setter
    def pipeline_execution_identifier(self, pipeline_execution_identifier):
        """Sets the pipeline_execution_identifier of this CreateComplianceResultV2.


        :param pipeline_execution_identifier: The pipeline_execution_identifier of this CreateComplianceResultV2.  # noqa: E501
        :type: str
        """

        self._pipeline_execution_identifier = pipeline_execution_identifier

    @property
    def pipeline_identifier(self):
        """Gets the pipeline_identifier of this CreateComplianceResultV2.  # noqa: E501


        :return: The pipeline_identifier of this CreateComplianceResultV2.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_identifier

    @pipeline_identifier.setter
    def pipeline_identifier(self, pipeline_identifier):
        """Sets the pipeline_identifier of this CreateComplianceResultV2.


        :param pipeline_identifier: The pipeline_identifier of this CreateComplianceResultV2.  # noqa: E501
        :type: str
        """

        self._pipeline_identifier = pipeline_identifier

    @property
    def plugins(self):
        """Gets the plugins of this CreateComplianceResultV2.  # noqa: E501


        :return: The plugins of this CreateComplianceResultV2.  # noqa: E501
        :rtype: list[PluginDTO]
        """
        return self._plugins

    @plugins.setter
    def plugins(self, plugins):
        """Sets the plugins of this CreateComplianceResultV2.


        :param plugins: The plugins of this CreateComplianceResultV2.  # noqa: E501
        :type: list[PluginDTO]
        """

        self._plugins = plugins

    @property
    def results(self):
        """Gets the results of this CreateComplianceResultV2.  # noqa: E501


        :return: The results of this CreateComplianceResultV2.  # noqa: E501
        :rtype: list[ComplianceResult]
        """
        return self._results

    @results.setter
    def results(self, results):
        """Sets the results of this CreateComplianceResultV2.


        :param results: The results of this CreateComplianceResultV2.  # noqa: E501
        :type: list[ComplianceResult]
        """
        if results is None:
            raise ValueError("Invalid value for `results`, must not be `None`")  # noqa: E501

        self._results = results

    @property
    def scan_type(self):
        """Gets the scan_type of this CreateComplianceResultV2.  # noqa: E501


        :return: The scan_type of this CreateComplianceResultV2.  # noqa: E501
        :rtype: ComplianceScanType
        """
        return self._scan_type

    @scan_type.setter
    def scan_type(self, scan_type):
        """Sets the scan_type of this CreateComplianceResultV2.


        :param scan_type: The scan_type of this CreateComplianceResultV2.  # noqa: E501
        :type: ComplianceScanType
        """
        if scan_type is None:
            raise ValueError("Invalid value for `scan_type`, must not be `None`")  # noqa: E501

        self._scan_type = scan_type

    @property
    def source_platform(self):
        """Gets the source_platform of this CreateComplianceResultV2.  # noqa: E501

        Source platform enum.  Example: GITHUB, HARNESS  # noqa: E501

        :return: The source_platform of this CreateComplianceResultV2.  # noqa: E501
        :rtype: str
        """
        return self._source_platform

    @source_platform.setter
    def source_platform(self, source_platform):
        """Sets the source_platform of this CreateComplianceResultV2.

        Source platform enum.  Example: GITHUB, HARNESS  # noqa: E501

        :param source_platform: The source_platform of this CreateComplianceResultV2.  # noqa: E501
        :type: str
        """
        if source_platform is None:
            raise ValueError("Invalid value for `source_platform`, must not be `None`")  # noqa: E501
        allowed_values = ["GITHUB", "HARNESS"]  # noqa: E501
        if source_platform not in allowed_values:
            raise ValueError(
                "Invalid value for `source_platform` ({0}), must be one of {1}"  # noqa: E501
                .format(source_platform, allowed_values)
            )

        self._source_platform = source_platform

    @property
    def stage_execution_identifier(self):
        """Gets the stage_execution_identifier of this CreateComplianceResultV2.  # noqa: E501


        :return: The stage_execution_identifier of this CreateComplianceResultV2.  # noqa: E501
        :rtype: str
        """
        return self._stage_execution_identifier

    @stage_execution_identifier.setter
    def stage_execution_identifier(self, stage_execution_identifier):
        """Sets the stage_execution_identifier of this CreateComplianceResultV2.


        :param stage_execution_identifier: The stage_execution_identifier of this CreateComplianceResultV2.  # noqa: E501
        :type: str
        """

        self._stage_execution_identifier = stage_execution_identifier

    @property
    def stage_type(self):
        """Gets the stage_type of this CreateComplianceResultV2.  # noqa: E501


        :return: The stage_type of this CreateComplianceResultV2.  # noqa: E501
        :rtype: str
        """
        return self._stage_type

    @stage_type.setter
    def stage_type(self, stage_type):
        """Sets the stage_type of this CreateComplianceResultV2.


        :param stage_type: The stage_type of this CreateComplianceResultV2.  # noqa: E501
        :type: str
        """

        self._stage_type = stage_type

    @property
    def step_execution_identifier(self):
        """Gets the step_execution_identifier of this CreateComplianceResultV2.  # noqa: E501


        :return: The step_execution_identifier of this CreateComplianceResultV2.  # noqa: E501
        :rtype: str
        """
        return self._step_execution_identifier

    @step_execution_identifier.setter
    def step_execution_identifier(self, step_execution_identifier):
        """Sets the step_execution_identifier of this CreateComplianceResultV2.


        :param step_execution_identifier: The step_execution_identifier of this CreateComplianceResultV2.  # noqa: E501
        :type: str
        """

        self._step_execution_identifier = step_execution_identifier

    @property
    def url(self):
        """Gets the url of this CreateComplianceResultV2.  # noqa: E501

        Represents Source URL.  # noqa: E501

        :return: The url of this CreateComplianceResultV2.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this CreateComplianceResultV2.

        Represents Source URL.  # noqa: E501

        :param url: The url of this CreateComplianceResultV2.  # noqa: E501
        :type: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

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
        if issubclass(CreateComplianceResultV2, dict):
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
        if not isinstance(other, CreateComplianceResultV2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
