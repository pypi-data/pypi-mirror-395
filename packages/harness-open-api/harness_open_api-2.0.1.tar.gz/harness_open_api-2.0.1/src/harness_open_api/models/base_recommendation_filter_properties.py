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

class BaseRecommendationFilterProperties(object):
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
        'applied_at_end_time': 'int',
        'applied_at_start_time': 'int',
        'cloud_account_id': 'list[str]',
        'cloud_account_name': 'list[str]',
        'cloud_provider': 'list[str]',
        'id': 'list[str]',
        'recommendation_state': 'list[str]',
        'region': 'list[str]',
        'resource_id': 'list[str]',
        'resource_name': 'list[str]',
        'resource_type': 'list[str]'
    }

    attribute_map = {
        'applied_at_end_time': 'appliedAtEndTime',
        'applied_at_start_time': 'appliedAtStartTime',
        'cloud_account_id': 'cloudAccountId',
        'cloud_account_name': 'cloudAccountName',
        'cloud_provider': 'cloudProvider',
        'id': 'id',
        'recommendation_state': 'recommendationState',
        'region': 'region',
        'resource_id': 'resourceId',
        'resource_name': 'resourceName',
        'resource_type': 'resourceType'
    }

    def __init__(self, applied_at_end_time=None, applied_at_start_time=None, cloud_account_id=None, cloud_account_name=None, cloud_provider=None, id=None, recommendation_state=None, region=None, resource_id=None, resource_name=None, resource_type=None):  # noqa: E501
        """BaseRecommendationFilterProperties - a model defined in Swagger"""  # noqa: E501
        self._applied_at_end_time = None
        self._applied_at_start_time = None
        self._cloud_account_id = None
        self._cloud_account_name = None
        self._cloud_provider = None
        self._id = None
        self._recommendation_state = None
        self._region = None
        self._resource_id = None
        self._resource_name = None
        self._resource_type = None
        self.discriminator = None
        if applied_at_end_time is not None:
            self.applied_at_end_time = applied_at_end_time
        if applied_at_start_time is not None:
            self.applied_at_start_time = applied_at_start_time
        if cloud_account_id is not None:
            self.cloud_account_id = cloud_account_id
        if cloud_account_name is not None:
            self.cloud_account_name = cloud_account_name
        if cloud_provider is not None:
            self.cloud_provider = cloud_provider
        if id is not None:
            self.id = id
        if recommendation_state is not None:
            self.recommendation_state = recommendation_state
        if region is not None:
            self.region = region
        if resource_id is not None:
            self.resource_id = resource_id
        if resource_name is not None:
            self.resource_name = resource_name
        if resource_type is not None:
            self.resource_type = resource_type

    @property
    def applied_at_end_time(self):
        """Gets the applied_at_end_time of this BaseRecommendationFilterProperties.  # noqa: E501

        Filter for recommendations applied before this timestamp (Unix time in milliseconds)  # noqa: E501

        :return: The applied_at_end_time of this BaseRecommendationFilterProperties.  # noqa: E501
        :rtype: int
        """
        return self._applied_at_end_time

    @applied_at_end_time.setter
    def applied_at_end_time(self, applied_at_end_time):
        """Sets the applied_at_end_time of this BaseRecommendationFilterProperties.

        Filter for recommendations applied before this timestamp (Unix time in milliseconds)  # noqa: E501

        :param applied_at_end_time: The applied_at_end_time of this BaseRecommendationFilterProperties.  # noqa: E501
        :type: int
        """

        self._applied_at_end_time = applied_at_end_time

    @property
    def applied_at_start_time(self):
        """Gets the applied_at_start_time of this BaseRecommendationFilterProperties.  # noqa: E501

        Filter for recommendations applied after this timestamp (Unix time in milliseconds)  # noqa: E501

        :return: The applied_at_start_time of this BaseRecommendationFilterProperties.  # noqa: E501
        :rtype: int
        """
        return self._applied_at_start_time

    @applied_at_start_time.setter
    def applied_at_start_time(self, applied_at_start_time):
        """Sets the applied_at_start_time of this BaseRecommendationFilterProperties.

        Filter for recommendations applied after this timestamp (Unix time in milliseconds)  # noqa: E501

        :param applied_at_start_time: The applied_at_start_time of this BaseRecommendationFilterProperties.  # noqa: E501
        :type: int
        """

        self._applied_at_start_time = applied_at_start_time

    @property
    def cloud_account_id(self):
        """Gets the cloud_account_id of this BaseRecommendationFilterProperties.  # noqa: E501

        List of cloud account IDs to filter recommendations  # noqa: E501

        :return: The cloud_account_id of this BaseRecommendationFilterProperties.  # noqa: E501
        :rtype: list[str]
        """
        return self._cloud_account_id

    @cloud_account_id.setter
    def cloud_account_id(self, cloud_account_id):
        """Sets the cloud_account_id of this BaseRecommendationFilterProperties.

        List of cloud account IDs to filter recommendations  # noqa: E501

        :param cloud_account_id: The cloud_account_id of this BaseRecommendationFilterProperties.  # noqa: E501
        :type: list[str]
        """

        self._cloud_account_id = cloud_account_id

    @property
    def cloud_account_name(self):
        """Gets the cloud_account_name of this BaseRecommendationFilterProperties.  # noqa: E501

        List of cloud account names to filter recommendations  # noqa: E501

        :return: The cloud_account_name of this BaseRecommendationFilterProperties.  # noqa: E501
        :rtype: list[str]
        """
        return self._cloud_account_name

    @cloud_account_name.setter
    def cloud_account_name(self, cloud_account_name):
        """Sets the cloud_account_name of this BaseRecommendationFilterProperties.

        List of cloud account names to filter recommendations  # noqa: E501

        :param cloud_account_name: The cloud_account_name of this BaseRecommendationFilterProperties.  # noqa: E501
        :type: list[str]
        """

        self._cloud_account_name = cloud_account_name

    @property
    def cloud_provider(self):
        """Gets the cloud_provider of this BaseRecommendationFilterProperties.  # noqa: E501

        List of cloud providers which will be applied as filter for Recommendations  # noqa: E501

        :return: The cloud_provider of this BaseRecommendationFilterProperties.  # noqa: E501
        :rtype: list[str]
        """
        return self._cloud_provider

    @cloud_provider.setter
    def cloud_provider(self, cloud_provider):
        """Sets the cloud_provider of this BaseRecommendationFilterProperties.

        List of cloud providers which will be applied as filter for Recommendations  # noqa: E501

        :param cloud_provider: The cloud_provider of this BaseRecommendationFilterProperties.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["AWS", "AZURE", "GCP", "CLUSTER", "EXTERNAL_DATA", "IBM", "ON_PREM", "UNKNOWN"]  # noqa: E501
        if not set(cloud_provider).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `cloud_provider` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(cloud_provider) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._cloud_provider = cloud_provider

    @property
    def id(self):
        """Gets the id of this BaseRecommendationFilterProperties.  # noqa: E501

        List of ids which will be applied as filter for Recommendations  # noqa: E501

        :return: The id of this BaseRecommendationFilterProperties.  # noqa: E501
        :rtype: list[str]
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BaseRecommendationFilterProperties.

        List of ids which will be applied as filter for Recommendations  # noqa: E501

        :param id: The id of this BaseRecommendationFilterProperties.  # noqa: E501
        :type: list[str]
        """

        self._id = id

    @property
    def recommendation_state(self):
        """Gets the recommendation_state of this BaseRecommendationFilterProperties.  # noqa: E501

        List of recommendationStates which will be applied as filter for Recommendations  # noqa: E501

        :return: The recommendation_state of this BaseRecommendationFilterProperties.  # noqa: E501
        :rtype: list[str]
        """
        return self._recommendation_state

    @recommendation_state.setter
    def recommendation_state(self, recommendation_state):
        """Sets the recommendation_state of this BaseRecommendationFilterProperties.

        List of recommendationStates which will be applied as filter for Recommendations  # noqa: E501

        :param recommendation_state: The recommendation_state of this BaseRecommendationFilterProperties.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["OPEN", "APPLIED", "IGNORED"]  # noqa: E501
        if not set(recommendation_state).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `recommendation_state` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(recommendation_state) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._recommendation_state = recommendation_state

    @property
    def region(self):
        """Gets the region of this BaseRecommendationFilterProperties.  # noqa: E501

        List of regions to filter recommendations  # noqa: E501

        :return: The region of this BaseRecommendationFilterProperties.  # noqa: E501
        :rtype: list[str]
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this BaseRecommendationFilterProperties.

        List of regions to filter recommendations  # noqa: E501

        :param region: The region of this BaseRecommendationFilterProperties.  # noqa: E501
        :type: list[str]
        """

        self._region = region

    @property
    def resource_id(self):
        """Gets the resource_id of this BaseRecommendationFilterProperties.  # noqa: E501

        List of resource IDs to filter recommendations  # noqa: E501

        :return: The resource_id of this BaseRecommendationFilterProperties.  # noqa: E501
        :rtype: list[str]
        """
        return self._resource_id

    @resource_id.setter
    def resource_id(self, resource_id):
        """Sets the resource_id of this BaseRecommendationFilterProperties.

        List of resource IDs to filter recommendations  # noqa: E501

        :param resource_id: The resource_id of this BaseRecommendationFilterProperties.  # noqa: E501
        :type: list[str]
        """

        self._resource_id = resource_id

    @property
    def resource_name(self):
        """Gets the resource_name of this BaseRecommendationFilterProperties.  # noqa: E501

        List of resource names to filter recommendations  # noqa: E501

        :return: The resource_name of this BaseRecommendationFilterProperties.  # noqa: E501
        :rtype: list[str]
        """
        return self._resource_name

    @resource_name.setter
    def resource_name(self, resource_name):
        """Sets the resource_name of this BaseRecommendationFilterProperties.

        List of resource names to filter recommendations  # noqa: E501

        :param resource_name: The resource_name of this BaseRecommendationFilterProperties.  # noqa: E501
        :type: list[str]
        """

        self._resource_name = resource_name

    @property
    def resource_type(self):
        """Gets the resource_type of this BaseRecommendationFilterProperties.  # noqa: E501

        List of resourceTypes which will be applied as filter for Recommendations  # noqa: E501

        :return: The resource_type of this BaseRecommendationFilterProperties.  # noqa: E501
        :rtype: list[str]
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """Sets the resource_type of this BaseRecommendationFilterProperties.

        List of resourceTypes which will be applied as filter for Recommendations  # noqa: E501

        :param resource_type: The resource_type of this BaseRecommendationFilterProperties.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["WORKLOAD", "NODE_POOL", "ECS_SERVICE", "EC2_INSTANCE", "GOVERNANCE", "AZURE_INSTANCE"]  # noqa: E501
        if not set(resource_type).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `resource_type` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(resource_type) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._resource_type = resource_type

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
        if issubclass(BaseRecommendationFilterProperties, dict):
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
        if not isinstance(other, BaseRecommendationFilterProperties):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
