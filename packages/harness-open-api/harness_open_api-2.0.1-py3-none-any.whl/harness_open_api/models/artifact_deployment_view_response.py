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

class ArtifactDeploymentViewResponse(object):
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
        'allow_list_violation_count': 'str',
        'deny_list_violation_count': 'str',
        'enforcement_id': 'str',
        'env_id': 'str',
        'env_name': 'str',
        'env_type': 'str',
        'pipeline_execution_id': 'str',
        'pipeline_id': 'str',
        'pipeline_name': 'str',
        'pipeline_sequence_id': 'str',
        'slsa_verification': 'Slsa',
        'triggered_at': 'str',
        'triggered_by': 'str',
        'triggered_by_id': 'str',
        'triggered_type': 'str'
    }

    attribute_map = {
        'allow_list_violation_count': 'allow_list_violation_count',
        'deny_list_violation_count': 'deny_list_violation_count',
        'enforcement_id': 'enforcement_id',
        'env_id': 'env_id',
        'env_name': 'env_name',
        'env_type': 'env_type',
        'pipeline_execution_id': 'pipeline_execution_id',
        'pipeline_id': 'pipeline_id',
        'pipeline_name': 'pipeline_name',
        'pipeline_sequence_id': 'pipeline_sequence_id',
        'slsa_verification': 'slsa_verification',
        'triggered_at': 'triggered_at',
        'triggered_by': 'triggered_by',
        'triggered_by_id': 'triggered_by_id',
        'triggered_type': 'triggered_type'
    }

    def __init__(self, allow_list_violation_count=None, deny_list_violation_count=None, enforcement_id=None, env_id=None, env_name=None, env_type=None, pipeline_execution_id=None, pipeline_id=None, pipeline_name=None, pipeline_sequence_id=None, slsa_verification=None, triggered_at=None, triggered_by=None, triggered_by_id=None, triggered_type=None):  # noqa: E501
        """ArtifactDeploymentViewResponse - a model defined in Swagger"""  # noqa: E501
        self._allow_list_violation_count = None
        self._deny_list_violation_count = None
        self._enforcement_id = None
        self._env_id = None
        self._env_name = None
        self._env_type = None
        self._pipeline_execution_id = None
        self._pipeline_id = None
        self._pipeline_name = None
        self._pipeline_sequence_id = None
        self._slsa_verification = None
        self._triggered_at = None
        self._triggered_by = None
        self._triggered_by_id = None
        self._triggered_type = None
        self.discriminator = None
        if allow_list_violation_count is not None:
            self.allow_list_violation_count = allow_list_violation_count
        if deny_list_violation_count is not None:
            self.deny_list_violation_count = deny_list_violation_count
        if enforcement_id is not None:
            self.enforcement_id = enforcement_id
        if env_id is not None:
            self.env_id = env_id
        if env_name is not None:
            self.env_name = env_name
        if env_type is not None:
            self.env_type = env_type
        if pipeline_execution_id is not None:
            self.pipeline_execution_id = pipeline_execution_id
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if pipeline_name is not None:
            self.pipeline_name = pipeline_name
        if pipeline_sequence_id is not None:
            self.pipeline_sequence_id = pipeline_sequence_id
        if slsa_verification is not None:
            self.slsa_verification = slsa_verification
        if triggered_at is not None:
            self.triggered_at = triggered_at
        if triggered_by is not None:
            self.triggered_by = triggered_by
        if triggered_by_id is not None:
            self.triggered_by_id = triggered_by_id
        if triggered_type is not None:
            self.triggered_type = triggered_type

    @property
    def allow_list_violation_count(self):
        """Gets the allow_list_violation_count of this ArtifactDeploymentViewResponse.  # noqa: E501

        Allow list type policy violation count  # noqa: E501

        :return: The allow_list_violation_count of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._allow_list_violation_count

    @allow_list_violation_count.setter
    def allow_list_violation_count(self, allow_list_violation_count):
        """Sets the allow_list_violation_count of this ArtifactDeploymentViewResponse.

        Allow list type policy violation count  # noqa: E501

        :param allow_list_violation_count: The allow_list_violation_count of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """

        self._allow_list_violation_count = allow_list_violation_count

    @property
    def deny_list_violation_count(self):
        """Gets the deny_list_violation_count of this ArtifactDeploymentViewResponse.  # noqa: E501

        Deny list type policy violation count  # noqa: E501

        :return: The deny_list_violation_count of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._deny_list_violation_count

    @deny_list_violation_count.setter
    def deny_list_violation_count(self, deny_list_violation_count):
        """Sets the deny_list_violation_count of this ArtifactDeploymentViewResponse.

        Deny list type policy violation count  # noqa: E501

        :param deny_list_violation_count: The deny_list_violation_count of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """

        self._deny_list_violation_count = deny_list_violation_count

    @property
    def enforcement_id(self):
        """Gets the enforcement_id of this ArtifactDeploymentViewResponse.  # noqa: E501

        Enforcement step identifier  # noqa: E501

        :return: The enforcement_id of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._enforcement_id

    @enforcement_id.setter
    def enforcement_id(self, enforcement_id):
        """Sets the enforcement_id of this ArtifactDeploymentViewResponse.

        Enforcement step identifier  # noqa: E501

        :param enforcement_id: The enforcement_id of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """

        self._enforcement_id = enforcement_id

    @property
    def env_id(self):
        """Gets the env_id of this ArtifactDeploymentViewResponse.  # noqa: E501

        Harness environment id  # noqa: E501

        :return: The env_id of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._env_id

    @env_id.setter
    def env_id(self, env_id):
        """Sets the env_id of this ArtifactDeploymentViewResponse.

        Harness environment id  # noqa: E501

        :param env_id: The env_id of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """

        self._env_id = env_id

    @property
    def env_name(self):
        """Gets the env_name of this ArtifactDeploymentViewResponse.  # noqa: E501

        Environment name  # noqa: E501

        :return: The env_name of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._env_name

    @env_name.setter
    def env_name(self, env_name):
        """Sets the env_name of this ArtifactDeploymentViewResponse.

        Environment name  # noqa: E501

        :param env_name: The env_name of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """

        self._env_name = env_name

    @property
    def env_type(self):
        """Gets the env_type of this ArtifactDeploymentViewResponse.  # noqa: E501

        Environment type  # noqa: E501

        :return: The env_type of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._env_type

    @env_type.setter
    def env_type(self, env_type):
        """Sets the env_type of this ArtifactDeploymentViewResponse.

        Environment type  # noqa: E501

        :param env_type: The env_type of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """
        allowed_values = ["PROD", "NONPROD"]  # noqa: E501
        if env_type not in allowed_values:
            raise ValueError(
                "Invalid value for `env_type` ({0}), must be one of {1}"  # noqa: E501
                .format(env_type, allowed_values)
            )

        self._env_type = env_type

    @property
    def pipeline_execution_id(self):
        """Gets the pipeline_execution_id of this ArtifactDeploymentViewResponse.  # noqa: E501

        Pipeline execution identifier of deployment pipeline  # noqa: E501

        :return: The pipeline_execution_id of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_execution_id

    @pipeline_execution_id.setter
    def pipeline_execution_id(self, pipeline_execution_id):
        """Sets the pipeline_execution_id of this ArtifactDeploymentViewResponse.

        Pipeline execution identifier of deployment pipeline  # noqa: E501

        :param pipeline_execution_id: The pipeline_execution_id of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """

        self._pipeline_execution_id = pipeline_execution_id

    @property
    def pipeline_id(self):
        """Gets the pipeline_id of this ArtifactDeploymentViewResponse.  # noqa: E501

        Pipeline identifier of deployment pipeline  # noqa: E501

        :return: The pipeline_id of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_id

    @pipeline_id.setter
    def pipeline_id(self, pipeline_id):
        """Sets the pipeline_id of this ArtifactDeploymentViewResponse.

        Pipeline identifier of deployment pipeline  # noqa: E501

        :param pipeline_id: The pipeline_id of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """

        self._pipeline_id = pipeline_id

    @property
    def pipeline_name(self):
        """Gets the pipeline_name of this ArtifactDeploymentViewResponse.  # noqa: E501

        Pipeline name of deployment pipeline  # noqa: E501

        :return: The pipeline_name of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_name

    @pipeline_name.setter
    def pipeline_name(self, pipeline_name):
        """Sets the pipeline_name of this ArtifactDeploymentViewResponse.

        Pipeline name of deployment pipeline  # noqa: E501

        :param pipeline_name: The pipeline_name of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """

        self._pipeline_name = pipeline_name

    @property
    def pipeline_sequence_id(self):
        """Gets the pipeline_sequence_id of this ArtifactDeploymentViewResponse.  # noqa: E501

        Pipeline Sequence id of deployment pipeline  # noqa: E501

        :return: The pipeline_sequence_id of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_sequence_id

    @pipeline_sequence_id.setter
    def pipeline_sequence_id(self, pipeline_sequence_id):
        """Sets the pipeline_sequence_id of this ArtifactDeploymentViewResponse.

        Pipeline Sequence id of deployment pipeline  # noqa: E501

        :param pipeline_sequence_id: The pipeline_sequence_id of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """

        self._pipeline_sequence_id = pipeline_sequence_id

    @property
    def slsa_verification(self):
        """Gets the slsa_verification of this ArtifactDeploymentViewResponse.  # noqa: E501


        :return: The slsa_verification of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: Slsa
        """
        return self._slsa_verification

    @slsa_verification.setter
    def slsa_verification(self, slsa_verification):
        """Sets the slsa_verification of this ArtifactDeploymentViewResponse.


        :param slsa_verification: The slsa_verification of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: Slsa
        """

        self._slsa_verification = slsa_verification

    @property
    def triggered_at(self):
        """Gets the triggered_at of this ArtifactDeploymentViewResponse.  # noqa: E501

        Time of trigger of the deployment pipeline  # noqa: E501

        :return: The triggered_at of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._triggered_at

    @triggered_at.setter
    def triggered_at(self, triggered_at):
        """Sets the triggered_at of this ArtifactDeploymentViewResponse.

        Time of trigger of the deployment pipeline  # noqa: E501

        :param triggered_at: The triggered_at of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """

        self._triggered_at = triggered_at

    @property
    def triggered_by(self):
        """Gets the triggered_by of this ArtifactDeploymentViewResponse.  # noqa: E501

        Name of who trigger the deployment pipeline  # noqa: E501

        :return: The triggered_by of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._triggered_by

    @triggered_by.setter
    def triggered_by(self, triggered_by):
        """Sets the triggered_by of this ArtifactDeploymentViewResponse.

        Name of who trigger the deployment pipeline  # noqa: E501

        :param triggered_by: The triggered_by of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """

        self._triggered_by = triggered_by

    @property
    def triggered_by_id(self):
        """Gets the triggered_by_id of this ArtifactDeploymentViewResponse.  # noqa: E501

        Id of who trigger the deployment pipeline  # noqa: E501

        :return: The triggered_by_id of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._triggered_by_id

    @triggered_by_id.setter
    def triggered_by_id(self, triggered_by_id):
        """Sets the triggered_by_id of this ArtifactDeploymentViewResponse.

        Id of who trigger the deployment pipeline  # noqa: E501

        :param triggered_by_id: The triggered_by_id of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """

        self._triggered_by_id = triggered_by_id

    @property
    def triggered_type(self):
        """Gets the triggered_type of this ArtifactDeploymentViewResponse.  # noqa: E501

        Trigger type of the deployment pipeline  # noqa: E501

        :return: The triggered_type of this ArtifactDeploymentViewResponse.  # noqa: E501
        :rtype: str
        """
        return self._triggered_type

    @triggered_type.setter
    def triggered_type(self, triggered_type):
        """Sets the triggered_type of this ArtifactDeploymentViewResponse.

        Trigger type of the deployment pipeline  # noqa: E501

        :param triggered_type: The triggered_type of this ArtifactDeploymentViewResponse.  # noqa: E501
        :type: str
        """

        self._triggered_type = triggered_type

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
        if issubclass(ArtifactDeploymentViewResponse, dict):
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
        if not isinstance(other, ArtifactDeploymentViewResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
