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

class ArtifactChainOfCustody(object):
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
        'activity_type': 'str',
        'artifact_details': 'ArtifactV2Details',
        'compliance': 'RiskAndCompliance',
        'created_at': 'int',
        'deployment': 'Deployments',
        'enforcement': 'Violations',
        'orchestration': 'SBOMInfo',
        'provenance': 'SLSADetails1',
        'verification': 'SLSADetails1',
        'vulnerability': 'StoIssueCount'
    }

    attribute_map = {
        'activity_type': 'ActivityType',
        'artifact_details': 'artifact_details',
        'compliance': 'compliance',
        'created_at': 'created_at',
        'deployment': 'deployment',
        'enforcement': 'enforcement',
        'orchestration': 'orchestration',
        'provenance': 'provenance',
        'verification': 'verification',
        'vulnerability': 'vulnerability'
    }

    def __init__(self, activity_type=None, artifact_details=None, compliance=None, created_at=None, deployment=None, enforcement=None, orchestration=None, provenance=None, verification=None, vulnerability=None):  # noqa: E501
        """ArtifactChainOfCustody - a model defined in Swagger"""  # noqa: E501
        self._activity_type = None
        self._artifact_details = None
        self._compliance = None
        self._created_at = None
        self._deployment = None
        self._enforcement = None
        self._orchestration = None
        self._provenance = None
        self._verification = None
        self._vulnerability = None
        self.discriminator = None
        if activity_type is not None:
            self.activity_type = activity_type
        if artifact_details is not None:
            self.artifact_details = artifact_details
        if compliance is not None:
            self.compliance = compliance
        if created_at is not None:
            self.created_at = created_at
        if deployment is not None:
            self.deployment = deployment
        if enforcement is not None:
            self.enforcement = enforcement
        if orchestration is not None:
            self.orchestration = orchestration
        if provenance is not None:
            self.provenance = provenance
        if verification is not None:
            self.verification = verification
        if vulnerability is not None:
            self.vulnerability = vulnerability

    @property
    def activity_type(self):
        """Gets the activity_type of this ArtifactChainOfCustody.  # noqa: E501


        :return: The activity_type of this ArtifactChainOfCustody.  # noqa: E501
        :rtype: str
        """
        return self._activity_type

    @activity_type.setter
    def activity_type(self, activity_type):
        """Sets the activity_type of this ArtifactChainOfCustody.


        :param activity_type: The activity_type of this ArtifactChainOfCustody.  # noqa: E501
        :type: str
        """
        allowed_values = ["ORCHESTRATION", "ENFORCEMENT", "PROVENANCE", "VERIFICATION", "COMPLIANCE", "VULNERABILITY", "DEPLOYMENT"]  # noqa: E501
        if activity_type not in allowed_values:
            raise ValueError(
                "Invalid value for `activity_type` ({0}), must be one of {1}"  # noqa: E501
                .format(activity_type, allowed_values)
            )

        self._activity_type = activity_type

    @property
    def artifact_details(self):
        """Gets the artifact_details of this ArtifactChainOfCustody.  # noqa: E501


        :return: The artifact_details of this ArtifactChainOfCustody.  # noqa: E501
        :rtype: ArtifactV2Details
        """
        return self._artifact_details

    @artifact_details.setter
    def artifact_details(self, artifact_details):
        """Sets the artifact_details of this ArtifactChainOfCustody.


        :param artifact_details: The artifact_details of this ArtifactChainOfCustody.  # noqa: E501
        :type: ArtifactV2Details
        """

        self._artifact_details = artifact_details

    @property
    def compliance(self):
        """Gets the compliance of this ArtifactChainOfCustody.  # noqa: E501


        :return: The compliance of this ArtifactChainOfCustody.  # noqa: E501
        :rtype: RiskAndCompliance
        """
        return self._compliance

    @compliance.setter
    def compliance(self, compliance):
        """Sets the compliance of this ArtifactChainOfCustody.


        :param compliance: The compliance of this ArtifactChainOfCustody.  # noqa: E501
        :type: RiskAndCompliance
        """

        self._compliance = compliance

    @property
    def created_at(self):
        """Gets the created_at of this ArtifactChainOfCustody.  # noqa: E501


        :return: The created_at of this ArtifactChainOfCustody.  # noqa: E501
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ArtifactChainOfCustody.


        :param created_at: The created_at of this ArtifactChainOfCustody.  # noqa: E501
        :type: int
        """

        self._created_at = created_at

    @property
    def deployment(self):
        """Gets the deployment of this ArtifactChainOfCustody.  # noqa: E501


        :return: The deployment of this ArtifactChainOfCustody.  # noqa: E501
        :rtype: Deployments
        """
        return self._deployment

    @deployment.setter
    def deployment(self, deployment):
        """Sets the deployment of this ArtifactChainOfCustody.


        :param deployment: The deployment of this ArtifactChainOfCustody.  # noqa: E501
        :type: Deployments
        """

        self._deployment = deployment

    @property
    def enforcement(self):
        """Gets the enforcement of this ArtifactChainOfCustody.  # noqa: E501


        :return: The enforcement of this ArtifactChainOfCustody.  # noqa: E501
        :rtype: Violations
        """
        return self._enforcement

    @enforcement.setter
    def enforcement(self, enforcement):
        """Sets the enforcement of this ArtifactChainOfCustody.


        :param enforcement: The enforcement of this ArtifactChainOfCustody.  # noqa: E501
        :type: Violations
        """

        self._enforcement = enforcement

    @property
    def orchestration(self):
        """Gets the orchestration of this ArtifactChainOfCustody.  # noqa: E501


        :return: The orchestration of this ArtifactChainOfCustody.  # noqa: E501
        :rtype: SBOMInfo
        """
        return self._orchestration

    @orchestration.setter
    def orchestration(self, orchestration):
        """Sets the orchestration of this ArtifactChainOfCustody.


        :param orchestration: The orchestration of this ArtifactChainOfCustody.  # noqa: E501
        :type: SBOMInfo
        """

        self._orchestration = orchestration

    @property
    def provenance(self):
        """Gets the provenance of this ArtifactChainOfCustody.  # noqa: E501


        :return: The provenance of this ArtifactChainOfCustody.  # noqa: E501
        :rtype: SLSADetails1
        """
        return self._provenance

    @provenance.setter
    def provenance(self, provenance):
        """Sets the provenance of this ArtifactChainOfCustody.


        :param provenance: The provenance of this ArtifactChainOfCustody.  # noqa: E501
        :type: SLSADetails1
        """

        self._provenance = provenance

    @property
    def verification(self):
        """Gets the verification of this ArtifactChainOfCustody.  # noqa: E501


        :return: The verification of this ArtifactChainOfCustody.  # noqa: E501
        :rtype: SLSADetails1
        """
        return self._verification

    @verification.setter
    def verification(self, verification):
        """Sets the verification of this ArtifactChainOfCustody.


        :param verification: The verification of this ArtifactChainOfCustody.  # noqa: E501
        :type: SLSADetails1
        """

        self._verification = verification

    @property
    def vulnerability(self):
        """Gets the vulnerability of this ArtifactChainOfCustody.  # noqa: E501


        :return: The vulnerability of this ArtifactChainOfCustody.  # noqa: E501
        :rtype: StoIssueCount
        """
        return self._vulnerability

    @vulnerability.setter
    def vulnerability(self, vulnerability):
        """Sets the vulnerability of this ArtifactChainOfCustody.


        :param vulnerability: The vulnerability of this ArtifactChainOfCustody.  # noqa: E501
        :type: StoIssueCount
        """

        self._vulnerability = vulnerability

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
        if issubclass(ArtifactChainOfCustody, dict):
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
        if not isinstance(other, ArtifactChainOfCustody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
