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

class ImpactedTarget(object):
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
        'execution_id': 'str',
        'exemption_id': 'str',
        'exemption_status': 'str',
        'id': 'str',
        'last_detected': 'int',
        'name': 'str',
        'num_occurrences': 'int',
        'pipeline_id': 'str',
        'user_email': 'str',
        'user_id': 'str',
        'user_name': 'str',
        'variant_name': 'str'
    }

    attribute_map = {
        'execution_id': 'executionId',
        'exemption_id': 'exemptionId',
        'exemption_status': 'exemptionStatus',
        'id': 'id',
        'last_detected': 'lastDetected',
        'name': 'name',
        'num_occurrences': 'numOccurrences',
        'pipeline_id': 'pipelineId',
        'user_email': 'userEmail',
        'user_id': 'userId',
        'user_name': 'userName',
        'variant_name': 'variantName'
    }

    def __init__(self, execution_id=None, exemption_id=None, exemption_status=None, id=None, last_detected=None, name=None, num_occurrences=None, pipeline_id=None, user_email=None, user_id=None, user_name=None, variant_name=None):  # noqa: E501
        """ImpactedTarget - a model defined in Swagger"""  # noqa: E501
        self._execution_id = None
        self._exemption_id = None
        self._exemption_status = None
        self._id = None
        self._last_detected = None
        self._name = None
        self._num_occurrences = None
        self._pipeline_id = None
        self._user_email = None
        self._user_id = None
        self._user_name = None
        self._variant_name = None
        self.discriminator = None
        self.execution_id = execution_id
        if exemption_id is not None:
            self.exemption_id = exemption_id
        if exemption_status is not None:
            self.exemption_status = exemption_status
        self.id = id
        self.last_detected = last_detected
        self.name = name
        self.num_occurrences = num_occurrences
        self.pipeline_id = pipeline_id
        if user_email is not None:
            self.user_email = user_email
        if user_id is not None:
            self.user_id = user_id
        if user_name is not None:
            self.user_name = user_name
        self.variant_name = variant_name

    @property
    def execution_id(self):
        """Gets the execution_id of this ImpactedTarget.  # noqa: E501

        Harness Execution ID  # noqa: E501

        :return: The execution_id of this ImpactedTarget.  # noqa: E501
        :rtype: str
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id):
        """Sets the execution_id of this ImpactedTarget.

        Harness Execution ID  # noqa: E501

        :param execution_id: The execution_id of this ImpactedTarget.  # noqa: E501
        :type: str
        """
        if execution_id is None:
            raise ValueError("Invalid value for `execution_id`, must not be `None`")  # noqa: E501

        self._execution_id = execution_id

    @property
    def exemption_id(self):
        """Gets the exemption_id of this ImpactedTarget.  # noqa: E501

        ID of Security Test Exemption  # noqa: E501

        :return: The exemption_id of this ImpactedTarget.  # noqa: E501
        :rtype: str
        """
        return self._exemption_id

    @exemption_id.setter
    def exemption_id(self, exemption_id):
        """Sets the exemption_id of this ImpactedTarget.

        ID of Security Test Exemption  # noqa: E501

        :param exemption_id: The exemption_id of this ImpactedTarget.  # noqa: E501
        :type: str
        """

        self._exemption_id = exemption_id

    @property
    def exemption_status(self):
        """Gets the exemption_status of this ImpactedTarget.  # noqa: E501

        Status of project scoped exemption for this issue  # noqa: E501

        :return: The exemption_status of this ImpactedTarget.  # noqa: E501
        :rtype: str
        """
        return self._exemption_status

    @exemption_status.setter
    def exemption_status(self, exemption_status):
        """Sets the exemption_status of this ImpactedTarget.

        Status of project scoped exemption for this issue  # noqa: E501

        :param exemption_status: The exemption_status of this ImpactedTarget.  # noqa: E501
        :type: str
        """

        self._exemption_status = exemption_status

    @property
    def id(self):
        """Gets the id of this ImpactedTarget.  # noqa: E501

        The ID of the impacted target  # noqa: E501

        :return: The id of this ImpactedTarget.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ImpactedTarget.

        The ID of the impacted target  # noqa: E501

        :param id: The id of this ImpactedTarget.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def last_detected(self):
        """Gets the last_detected of this ImpactedTarget.  # noqa: E501

        Timestamp of the last detection of this issue  # noqa: E501

        :return: The last_detected of this ImpactedTarget.  # noqa: E501
        :rtype: int
        """
        return self._last_detected

    @last_detected.setter
    def last_detected(self, last_detected):
        """Sets the last_detected of this ImpactedTarget.

        Timestamp of the last detection of this issue  # noqa: E501

        :param last_detected: The last_detected of this ImpactedTarget.  # noqa: E501
        :type: int
        """
        if last_detected is None:
            raise ValueError("Invalid value for `last_detected`, must not be `None`")  # noqa: E501

        self._last_detected = last_detected

    @property
    def name(self):
        """Gets the name of this ImpactedTarget.  # noqa: E501

        The name of the impacted target  # noqa: E501

        :return: The name of this ImpactedTarget.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ImpactedTarget.

        The name of the impacted target  # noqa: E501

        :param name: The name of this ImpactedTarget.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def num_occurrences(self):
        """Gets the num_occurrences of this ImpactedTarget.  # noqa: E501

        Indicates the number of Occurrences on the Issue  # noqa: E501

        :return: The num_occurrences of this ImpactedTarget.  # noqa: E501
        :rtype: int
        """
        return self._num_occurrences

    @num_occurrences.setter
    def num_occurrences(self, num_occurrences):
        """Sets the num_occurrences of this ImpactedTarget.

        Indicates the number of Occurrences on the Issue  # noqa: E501

        :param num_occurrences: The num_occurrences of this ImpactedTarget.  # noqa: E501
        :type: int
        """
        if num_occurrences is None:
            raise ValueError("Invalid value for `num_occurrences`, must not be `None`")  # noqa: E501

        self._num_occurrences = num_occurrences

    @property
    def pipeline_id(self):
        """Gets the pipeline_id of this ImpactedTarget.  # noqa: E501

        Harness Pipeline ID  # noqa: E501

        :return: The pipeline_id of this ImpactedTarget.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_id

    @pipeline_id.setter
    def pipeline_id(self, pipeline_id):
        """Sets the pipeline_id of this ImpactedTarget.

        Harness Pipeline ID  # noqa: E501

        :param pipeline_id: The pipeline_id of this ImpactedTarget.  # noqa: E501
        :type: str
        """
        if pipeline_id is None:
            raise ValueError("Invalid value for `pipeline_id`, must not be `None`")  # noqa: E501

        self._pipeline_id = pipeline_id

    @property
    def user_email(self):
        """Gets the user_email of this ImpactedTarget.  # noqa: E501

        The email associated with the user id  # noqa: E501

        :return: The user_email of this ImpactedTarget.  # noqa: E501
        :rtype: str
        """
        return self._user_email

    @user_email.setter
    def user_email(self, user_email):
        """Sets the user_email of this ImpactedTarget.

        The email associated with the user id  # noqa: E501

        :param user_email: The user_email of this ImpactedTarget.  # noqa: E501
        :type: str
        """

        self._user_email = user_email

    @property
    def user_id(self):
        """Gets the user_id of this ImpactedTarget.  # noqa: E501

        The user id associated with the last scan run  # noqa: E501

        :return: The user_id of this ImpactedTarget.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this ImpactedTarget.

        The user id associated with the last scan run  # noqa: E501

        :param user_id: The user_id of this ImpactedTarget.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

    @property
    def user_name(self):
        """Gets the user_name of this ImpactedTarget.  # noqa: E501

        The user name associated with the user id  # noqa: E501

        :return: The user_name of this ImpactedTarget.  # noqa: E501
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """Sets the user_name of this ImpactedTarget.

        The user name associated with the user id  # noqa: E501

        :param user_name: The user_name of this ImpactedTarget.  # noqa: E501
        :type: str
        """

        self._user_name = user_name

    @property
    def variant_name(self):
        """Gets the variant_name of this ImpactedTarget.  # noqa: E501

        Variant name  # noqa: E501

        :return: The variant_name of this ImpactedTarget.  # noqa: E501
        :rtype: str
        """
        return self._variant_name

    @variant_name.setter
    def variant_name(self, variant_name):
        """Sets the variant_name of this ImpactedTarget.

        Variant name  # noqa: E501

        :param variant_name: The variant_name of this ImpactedTarget.  # noqa: E501
        :type: str
        """
        if variant_name is None:
            raise ValueError("Invalid value for `variant_name`, must not be `None`")  # noqa: E501

        self._variant_name = variant_name

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
        if issubclass(ImpactedTarget, dict):
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
        if not isinstance(other, ImpactedTarget):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
