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

class ArtifactV2Overview(object):
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
        'deployments': 'Deployments',
        'digest': 'str',
        'id': 'str',
        'metadata': 'object',
        'name': 'str',
        'pipeline_details': 'PipelineDetails',
        'sbom_details': 'SBOMInfo',
        'scorecard': 'Scorecard1',
        'signing': 'IntegrityVerification',
        'slsa_details': 'SLSADetails1',
        'source_id': 'str',
        'sto_issue_count': 'StoIssueCount',
        'tags': 'list[str]',
        'updated': 'str',
        'url': 'str',
        'violations': 'Violations'
    }

    attribute_map = {
        'deployments': 'deployments',
        'digest': 'digest',
        'id': 'id',
        'metadata': 'metadata',
        'name': 'name',
        'pipeline_details': 'pipeline_details',
        'sbom_details': 'sbom_details',
        'scorecard': 'scorecard',
        'signing': 'signing',
        'slsa_details': 'slsa_details',
        'source_id': 'source_id',
        'sto_issue_count': 'sto_issue_count',
        'tags': 'tags',
        'updated': 'updated',
        'url': 'url',
        'violations': 'violations'
    }

    def __init__(self, deployments=None, digest=None, id=None, metadata=None, name=None, pipeline_details=None, sbom_details=None, scorecard=None, signing=None, slsa_details=None, source_id=None, sto_issue_count=None, tags=None, updated=None, url=None, violations=None):  # noqa: E501
        """ArtifactV2Overview - a model defined in Swagger"""  # noqa: E501
        self._deployments = None
        self._digest = None
        self._id = None
        self._metadata = None
        self._name = None
        self._pipeline_details = None
        self._sbom_details = None
        self._scorecard = None
        self._signing = None
        self._slsa_details = None
        self._source_id = None
        self._sto_issue_count = None
        self._tags = None
        self._updated = None
        self._url = None
        self._violations = None
        self.discriminator = None
        if deployments is not None:
            self.deployments = deployments
        if digest is not None:
            self.digest = digest
        if id is not None:
            self.id = id
        if metadata is not None:
            self.metadata = metadata
        self.name = name
        if pipeline_details is not None:
            self.pipeline_details = pipeline_details
        if sbom_details is not None:
            self.sbom_details = sbom_details
        if scorecard is not None:
            self.scorecard = scorecard
        if signing is not None:
            self.signing = signing
        if slsa_details is not None:
            self.slsa_details = slsa_details
        if source_id is not None:
            self.source_id = source_id
        if sto_issue_count is not None:
            self.sto_issue_count = sto_issue_count
        if tags is not None:
            self.tags = tags
        if updated is not None:
            self.updated = updated
        self.url = url
        if violations is not None:
            self.violations = violations

    @property
    def deployments(self):
        """Gets the deployments of this ArtifactV2Overview.  # noqa: E501


        :return: The deployments of this ArtifactV2Overview.  # noqa: E501
        :rtype: Deployments
        """
        return self._deployments

    @deployments.setter
    def deployments(self, deployments):
        """Sets the deployments of this ArtifactV2Overview.


        :param deployments: The deployments of this ArtifactV2Overview.  # noqa: E501
        :type: Deployments
        """

        self._deployments = deployments

    @property
    def digest(self):
        """Gets the digest of this ArtifactV2Overview.  # noqa: E501

        digest of the artifact  # noqa: E501

        :return: The digest of this ArtifactV2Overview.  # noqa: E501
        :rtype: str
        """
        return self._digest

    @digest.setter
    def digest(self, digest):
        """Sets the digest of this ArtifactV2Overview.

        digest of the artifact  # noqa: E501

        :param digest: The digest of this ArtifactV2Overview.  # noqa: E501
        :type: str
        """

        self._digest = digest

    @property
    def id(self):
        """Gets the id of this ArtifactV2Overview.  # noqa: E501

        Artifact Identifier  # noqa: E501

        :return: The id of this ArtifactV2Overview.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ArtifactV2Overview.

        Artifact Identifier  # noqa: E501

        :param id: The id of this ArtifactV2Overview.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def metadata(self):
        """Gets the metadata of this ArtifactV2Overview.  # noqa: E501


        :return: The metadata of this ArtifactV2Overview.  # noqa: E501
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this ArtifactV2Overview.


        :param metadata: The metadata of this ArtifactV2Overview.  # noqa: E501
        :type: object
        """

        self._metadata = metadata

    @property
    def name(self):
        """Gets the name of this ArtifactV2Overview.  # noqa: E501

        Artifact Name  # noqa: E501

        :return: The name of this ArtifactV2Overview.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ArtifactV2Overview.

        Artifact Name  # noqa: E501

        :param name: The name of this ArtifactV2Overview.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def pipeline_details(self):
        """Gets the pipeline_details of this ArtifactV2Overview.  # noqa: E501


        :return: The pipeline_details of this ArtifactV2Overview.  # noqa: E501
        :rtype: PipelineDetails
        """
        return self._pipeline_details

    @pipeline_details.setter
    def pipeline_details(self, pipeline_details):
        """Sets the pipeline_details of this ArtifactV2Overview.


        :param pipeline_details: The pipeline_details of this ArtifactV2Overview.  # noqa: E501
        :type: PipelineDetails
        """

        self._pipeline_details = pipeline_details

    @property
    def sbom_details(self):
        """Gets the sbom_details of this ArtifactV2Overview.  # noqa: E501


        :return: The sbom_details of this ArtifactV2Overview.  # noqa: E501
        :rtype: SBOMInfo
        """
        return self._sbom_details

    @sbom_details.setter
    def sbom_details(self, sbom_details):
        """Sets the sbom_details of this ArtifactV2Overview.


        :param sbom_details: The sbom_details of this ArtifactV2Overview.  # noqa: E501
        :type: SBOMInfo
        """

        self._sbom_details = sbom_details

    @property
    def scorecard(self):
        """Gets the scorecard of this ArtifactV2Overview.  # noqa: E501


        :return: The scorecard of this ArtifactV2Overview.  # noqa: E501
        :rtype: Scorecard1
        """
        return self._scorecard

    @scorecard.setter
    def scorecard(self, scorecard):
        """Sets the scorecard of this ArtifactV2Overview.


        :param scorecard: The scorecard of this ArtifactV2Overview.  # noqa: E501
        :type: Scorecard1
        """

        self._scorecard = scorecard

    @property
    def signing(self):
        """Gets the signing of this ArtifactV2Overview.  # noqa: E501


        :return: The signing of this ArtifactV2Overview.  # noqa: E501
        :rtype: IntegrityVerification
        """
        return self._signing

    @signing.setter
    def signing(self, signing):
        """Sets the signing of this ArtifactV2Overview.


        :param signing: The signing of this ArtifactV2Overview.  # noqa: E501
        :type: IntegrityVerification
        """

        self._signing = signing

    @property
    def slsa_details(self):
        """Gets the slsa_details of this ArtifactV2Overview.  # noqa: E501


        :return: The slsa_details of this ArtifactV2Overview.  # noqa: E501
        :rtype: SLSADetails1
        """
        return self._slsa_details

    @slsa_details.setter
    def slsa_details(self, slsa_details):
        """Sets the slsa_details of this ArtifactV2Overview.


        :param slsa_details: The slsa_details of this ArtifactV2Overview.  # noqa: E501
        :type: SLSADetails1
        """

        self._slsa_details = slsa_details

    @property
    def source_id(self):
        """Gets the source_id of this ArtifactV2Overview.  # noqa: E501


        :return: The source_id of this ArtifactV2Overview.  # noqa: E501
        :rtype: str
        """
        return self._source_id

    @source_id.setter
    def source_id(self, source_id):
        """Sets the source_id of this ArtifactV2Overview.


        :param source_id: The source_id of this ArtifactV2Overview.  # noqa: E501
        :type: str
        """

        self._source_id = source_id

    @property
    def sto_issue_count(self):
        """Gets the sto_issue_count of this ArtifactV2Overview.  # noqa: E501


        :return: The sto_issue_count of this ArtifactV2Overview.  # noqa: E501
        :rtype: StoIssueCount
        """
        return self._sto_issue_count

    @sto_issue_count.setter
    def sto_issue_count(self, sto_issue_count):
        """Sets the sto_issue_count of this ArtifactV2Overview.


        :param sto_issue_count: The sto_issue_count of this ArtifactV2Overview.  # noqa: E501
        :type: StoIssueCount
        """

        self._sto_issue_count = sto_issue_count

    @property
    def tags(self):
        """Gets the tags of this ArtifactV2Overview.  # noqa: E501


        :return: The tags of this ArtifactV2Overview.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this ArtifactV2Overview.


        :param tags: The tags of this ArtifactV2Overview.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def updated(self):
        """Gets the updated of this ArtifactV2Overview.  # noqa: E501

        Last Updated time of artifact  # noqa: E501

        :return: The updated of this ArtifactV2Overview.  # noqa: E501
        :rtype: str
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this ArtifactV2Overview.

        Last Updated time of artifact  # noqa: E501

        :param updated: The updated of this ArtifactV2Overview.  # noqa: E501
        :type: str
        """

        self._updated = updated

    @property
    def url(self):
        """Gets the url of this ArtifactV2Overview.  # noqa: E501

        Artifact URL  # noqa: E501

        :return: The url of this ArtifactV2Overview.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this ArtifactV2Overview.

        Artifact URL  # noqa: E501

        :param url: The url of this ArtifactV2Overview.  # noqa: E501
        :type: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def violations(self):
        """Gets the violations of this ArtifactV2Overview.  # noqa: E501


        :return: The violations of this ArtifactV2Overview.  # noqa: E501
        :rtype: Violations
        """
        return self._violations

    @violations.setter
    def violations(self, violations):
        """Sets the violations of this ArtifactV2Overview.


        :param violations: The violations of this ArtifactV2Overview.  # noqa: E501
        :type: Violations
        """

        self._violations = violations

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
        if issubclass(ArtifactV2Overview, dict):
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
        if not isinstance(other, ArtifactV2Overview):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
