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

class UpdateScanRequestBody(object):
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
        'artifact_fingerprint': 'str',
        'code_coverage': 'float',
        'execution_id': 'str',
        'git_metadata': 'GitMetadata',
        'metadata': 'ScanMetadata',
        'org_id': 'str',
        'pipeline_id': 'str',
        'product_id': 'str',
        'project_id': 'str',
        'refinement_version': 'str',
        'stage_id': 'str',
        'status': 'str',
        'step_id': 'str',
        'subproduct': 'str',
        'target_variant_id': 'str'
    }

    attribute_map = {
        'artifact_fingerprint': 'artifactFingerprint',
        'code_coverage': 'codeCoverage',
        'execution_id': 'executionId',
        'git_metadata': 'gitMetadata',
        'metadata': 'metadata',
        'org_id': 'orgId',
        'pipeline_id': 'pipelineId',
        'product_id': 'productId',
        'project_id': 'projectId',
        'refinement_version': 'refinementVersion',
        'stage_id': 'stageId',
        'status': 'status',
        'step_id': 'stepId',
        'subproduct': 'subproduct',
        'target_variant_id': 'targetVariantId'
    }

    def __init__(self, artifact_fingerprint=None, code_coverage=None, execution_id=None, git_metadata=None, metadata=None, org_id=None, pipeline_id=None, product_id=None, project_id=None, refinement_version=None, stage_id=None, status=None, step_id=None, subproduct=None, target_variant_id=None):  # noqa: E501
        """UpdateScanRequestBody - a model defined in Swagger"""  # noqa: E501
        self._artifact_fingerprint = None
        self._code_coverage = None
        self._execution_id = None
        self._git_metadata = None
        self._metadata = None
        self._org_id = None
        self._pipeline_id = None
        self._product_id = None
        self._project_id = None
        self._refinement_version = None
        self._stage_id = None
        self._status = None
        self._step_id = None
        self._subproduct = None
        self._target_variant_id = None
        self.discriminator = None
        if artifact_fingerprint is not None:
            self.artifact_fingerprint = artifact_fingerprint
        if code_coverage is not None:
            self.code_coverage = code_coverage
        self.execution_id = execution_id
        if git_metadata is not None:
            self.git_metadata = git_metadata
        if metadata is not None:
            self.metadata = metadata
        self.org_id = org_id
        self.pipeline_id = pipeline_id
        self.product_id = product_id
        self.project_id = project_id
        self.refinement_version = refinement_version
        self.stage_id = stage_id
        self.status = status
        self.step_id = step_id
        if subproduct is not None:
            self.subproduct = subproduct
        self.target_variant_id = target_variant_id

    @property
    def artifact_fingerprint(self):
        """Gets the artifact_fingerprint of this UpdateScanRequestBody.  # noqa: E501

        The Artifact Fingerprint used use to identify the target  # noqa: E501

        :return: The artifact_fingerprint of this UpdateScanRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._artifact_fingerprint

    @artifact_fingerprint.setter
    def artifact_fingerprint(self, artifact_fingerprint):
        """Sets the artifact_fingerprint of this UpdateScanRequestBody.

        The Artifact Fingerprint used use to identify the target  # noqa: E501

        :param artifact_fingerprint: The artifact_fingerprint of this UpdateScanRequestBody.  # noqa: E501
        :type: str
        """

        self._artifact_fingerprint = artifact_fingerprint

    @property
    def code_coverage(self):
        """Gets the code_coverage of this UpdateScanRequestBody.  # noqa: E501

        The Code Coverage value for the Scan  # noqa: E501

        :return: The code_coverage of this UpdateScanRequestBody.  # noqa: E501
        :rtype: float
        """
        return self._code_coverage

    @code_coverage.setter
    def code_coverage(self, code_coverage):
        """Sets the code_coverage of this UpdateScanRequestBody.

        The Code Coverage value for the Scan  # noqa: E501

        :param code_coverage: The code_coverage of this UpdateScanRequestBody.  # noqa: E501
        :type: float
        """

        self._code_coverage = code_coverage

    @property
    def execution_id(self):
        """Gets the execution_id of this UpdateScanRequestBody.  # noqa: E501

        Pipeline Execution ID associated with the Scan  # noqa: E501

        :return: The execution_id of this UpdateScanRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id):
        """Sets the execution_id of this UpdateScanRequestBody.

        Pipeline Execution ID associated with the Scan  # noqa: E501

        :param execution_id: The execution_id of this UpdateScanRequestBody.  # noqa: E501
        :type: str
        """
        if execution_id is None:
            raise ValueError("Invalid value for `execution_id`, must not be `None`")  # noqa: E501

        self._execution_id = execution_id

    @property
    def git_metadata(self):
        """Gets the git_metadata of this UpdateScanRequestBody.  # noqa: E501


        :return: The git_metadata of this UpdateScanRequestBody.  # noqa: E501
        :rtype: GitMetadata
        """
        return self._git_metadata

    @git_metadata.setter
    def git_metadata(self, git_metadata):
        """Sets the git_metadata of this UpdateScanRequestBody.


        :param git_metadata: The git_metadata of this UpdateScanRequestBody.  # noqa: E501
        :type: GitMetadata
        """

        self._git_metadata = git_metadata

    @property
    def metadata(self):
        """Gets the metadata of this UpdateScanRequestBody.  # noqa: E501


        :return: The metadata of this UpdateScanRequestBody.  # noqa: E501
        :rtype: ScanMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this UpdateScanRequestBody.


        :param metadata: The metadata of this UpdateScanRequestBody.  # noqa: E501
        :type: ScanMetadata
        """

        self._metadata = metadata

    @property
    def org_id(self):
        """Gets the org_id of this UpdateScanRequestBody.  # noqa: E501

        Harness Organization ID  # noqa: E501

        :return: The org_id of this UpdateScanRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Sets the org_id of this UpdateScanRequestBody.

        Harness Organization ID  # noqa: E501

        :param org_id: The org_id of this UpdateScanRequestBody.  # noqa: E501
        :type: str
        """
        if org_id is None:
            raise ValueError("Invalid value for `org_id`, must not be `None`")  # noqa: E501

        self._org_id = org_id

    @property
    def pipeline_id(self):
        """Gets the pipeline_id of this UpdateScanRequestBody.  # noqa: E501

        Harness Organization ID  # noqa: E501

        :return: The pipeline_id of this UpdateScanRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_id

    @pipeline_id.setter
    def pipeline_id(self, pipeline_id):
        """Sets the pipeline_id of this UpdateScanRequestBody.

        Harness Organization ID  # noqa: E501

        :param pipeline_id: The pipeline_id of this UpdateScanRequestBody.  # noqa: E501
        :type: str
        """
        if pipeline_id is None:
            raise ValueError("Invalid value for `pipeline_id`, must not be `None`")  # noqa: E501

        self._pipeline_id = pipeline_id

    @property
    def product_id(self):
        """Gets the product_id of this UpdateScanRequestBody.  # noqa: E501

        The Scan Product used for the Scan  # noqa: E501

        :return: The product_id of this UpdateScanRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        """Sets the product_id of this UpdateScanRequestBody.

        The Scan Product used for the Scan  # noqa: E501

        :param product_id: The product_id of this UpdateScanRequestBody.  # noqa: E501
        :type: str
        """
        if product_id is None:
            raise ValueError("Invalid value for `product_id`, must not be `None`")  # noqa: E501

        self._product_id = product_id

    @property
    def project_id(self):
        """Gets the project_id of this UpdateScanRequestBody.  # noqa: E501

        Harness Project ID  # noqa: E501

        :return: The project_id of this UpdateScanRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this UpdateScanRequestBody.

        Harness Project ID  # noqa: E501

        :param project_id: The project_id of this UpdateScanRequestBody.  # noqa: E501
        :type: str
        """
        if project_id is None:
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def refinement_version(self):
        """Gets the refinement_version of this UpdateScanRequestBody.  # noqa: E501

        The Issue refinement version used for this Scan  # noqa: E501

        :return: The refinement_version of this UpdateScanRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._refinement_version

    @refinement_version.setter
    def refinement_version(self, refinement_version):
        """Sets the refinement_version of this UpdateScanRequestBody.

        The Issue refinement version used for this Scan  # noqa: E501

        :param refinement_version: The refinement_version of this UpdateScanRequestBody.  # noqa: E501
        :type: str
        """
        if refinement_version is None:
            raise ValueError("Invalid value for `refinement_version`, must not be `None`")  # noqa: E501

        self._refinement_version = refinement_version

    @property
    def stage_id(self):
        """Gets the stage_id of this UpdateScanRequestBody.  # noqa: E501

        Pipeline Stage ID associated with the Scan  # noqa: E501

        :return: The stage_id of this UpdateScanRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._stage_id

    @stage_id.setter
    def stage_id(self, stage_id):
        """Sets the stage_id of this UpdateScanRequestBody.

        Pipeline Stage ID associated with the Scan  # noqa: E501

        :param stage_id: The stage_id of this UpdateScanRequestBody.  # noqa: E501
        :type: str
        """
        if stage_id is None:
            raise ValueError("Invalid value for `stage_id`, must not be `None`")  # noqa: E501

        self._stage_id = stage_id

    @property
    def status(self):
        """Gets the status of this UpdateScanRequestBody.  # noqa: E501

        Current status of the Scan  # noqa: E501

        :return: The status of this UpdateScanRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this UpdateScanRequestBody.

        Current status of the Scan  # noqa: E501

        :param status: The status of this UpdateScanRequestBody.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501
        allowed_values = ["Pending", "Running", "Succeeded", "Failed"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def step_id(self):
        """Gets the step_id of this UpdateScanRequestBody.  # noqa: E501

        Pipeline Step ID associated with the Scan  # noqa: E501

        :return: The step_id of this UpdateScanRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._step_id

    @step_id.setter
    def step_id(self, step_id):
        """Sets the step_id of this UpdateScanRequestBody.

        Pipeline Step ID associated with the Scan  # noqa: E501

        :param step_id: The step_id of this UpdateScanRequestBody.  # noqa: E501
        :type: str
        """
        if step_id is None:
            raise ValueError("Invalid value for `step_id`, must not be `None`")  # noqa: E501

        self._step_id = step_id

    @property
    def subproduct(self):
        """Gets the subproduct of this UpdateScanRequestBody.  # noqa: E501

        The Scan Subproduct used for the Scan  # noqa: E501

        :return: The subproduct of this UpdateScanRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._subproduct

    @subproduct.setter
    def subproduct(self, subproduct):
        """Sets the subproduct of this UpdateScanRequestBody.

        The Scan Subproduct used for the Scan  # noqa: E501

        :param subproduct: The subproduct of this UpdateScanRequestBody.  # noqa: E501
        :type: str
        """

        self._subproduct = subproduct

    @property
    def target_variant_id(self):
        """Gets the target_variant_id of this UpdateScanRequestBody.  # noqa: E501

        The Target Variant associated with the Scan  # noqa: E501

        :return: The target_variant_id of this UpdateScanRequestBody.  # noqa: E501
        :rtype: str
        """
        return self._target_variant_id

    @target_variant_id.setter
    def target_variant_id(self, target_variant_id):
        """Sets the target_variant_id of this UpdateScanRequestBody.

        The Target Variant associated with the Scan  # noqa: E501

        :param target_variant_id: The target_variant_id of this UpdateScanRequestBody.  # noqa: E501
        :type: str
        """
        if target_variant_id is None:
            raise ValueError("Invalid value for `target_variant_id`, must not be `None`")  # noqa: E501

        self._target_variant_id = target_variant_id

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
        if issubclass(UpdateScanRequestBody, dict):
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
        if not isinstance(other, UpdateScanRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
