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

class ConnectedKubernetesClusterConfig(object):
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
        'base_on_demand_capacity': 'int',
        'consolidation': 'ConnectedKubernetesClusterConfigConsolidation',
        'distribution_strategy': 'str',
        'node_deletion_delay': 'int',
        'on_demand_split': 'int',
        'reverse_fallback': 'str',
        'spot_distribution': 'str',
        'spot_split': 'int'
    }

    attribute_map = {
        'base_on_demand_capacity': 'base_on_demand_capacity',
        'consolidation': 'consolidation',
        'distribution_strategy': 'distribution_strategy',
        'node_deletion_delay': 'node_deletion_delay',
        'on_demand_split': 'on_demand_split',
        'reverse_fallback': 'reverse_fallback',
        'spot_distribution': 'spot_distribution',
        'spot_split': 'spot_split'
    }

    def __init__(self, base_on_demand_capacity=None, consolidation=None, distribution_strategy=None, node_deletion_delay=None, on_demand_split=None, reverse_fallback=None, spot_distribution=None, spot_split=None):  # noqa: E501
        """ConnectedKubernetesClusterConfig - a model defined in Swagger"""  # noqa: E501
        self._base_on_demand_capacity = None
        self._consolidation = None
        self._distribution_strategy = None
        self._node_deletion_delay = None
        self._on_demand_split = None
        self._reverse_fallback = None
        self._spot_distribution = None
        self._spot_split = None
        self.discriminator = None
        if base_on_demand_capacity is not None:
            self.base_on_demand_capacity = base_on_demand_capacity
        if consolidation is not None:
            self.consolidation = consolidation
        if distribution_strategy is not None:
            self.distribution_strategy = distribution_strategy
        if node_deletion_delay is not None:
            self.node_deletion_delay = node_deletion_delay
        if on_demand_split is not None:
            self.on_demand_split = on_demand_split
        if reverse_fallback is not None:
            self.reverse_fallback = reverse_fallback
        if spot_distribution is not None:
            self.spot_distribution = spot_distribution
        if spot_split is not None:
            self.spot_split = spot_split

    @property
    def base_on_demand_capacity(self):
        """Gets the base_on_demand_capacity of this ConnectedKubernetesClusterConfig.  # noqa: E501


        :return: The base_on_demand_capacity of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :rtype: int
        """
        return self._base_on_demand_capacity

    @base_on_demand_capacity.setter
    def base_on_demand_capacity(self, base_on_demand_capacity):
        """Sets the base_on_demand_capacity of this ConnectedKubernetesClusterConfig.


        :param base_on_demand_capacity: The base_on_demand_capacity of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :type: int
        """

        self._base_on_demand_capacity = base_on_demand_capacity

    @property
    def consolidation(self):
        """Gets the consolidation of this ConnectedKubernetesClusterConfig.  # noqa: E501


        :return: The consolidation of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :rtype: ConnectedKubernetesClusterConfigConsolidation
        """
        return self._consolidation

    @consolidation.setter
    def consolidation(self, consolidation):
        """Sets the consolidation of this ConnectedKubernetesClusterConfig.


        :param consolidation: The consolidation of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :type: ConnectedKubernetesClusterConfigConsolidation
        """

        self._consolidation = consolidation

    @property
    def distribution_strategy(self):
        """Gets the distribution_strategy of this ConnectedKubernetesClusterConfig.  # noqa: E501


        :return: The distribution_strategy of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :rtype: str
        """
        return self._distribution_strategy

    @distribution_strategy.setter
    def distribution_strategy(self, distribution_strategy):
        """Sets the distribution_strategy of this ConnectedKubernetesClusterConfig.


        :param distribution_strategy: The distribution_strategy of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :type: str
        """
        allowed_values = ["CostOptimized", "LeastInterrupted"]  # noqa: E501
        if distribution_strategy not in allowed_values:
            raise ValueError(
                "Invalid value for `distribution_strategy` ({0}), must be one of {1}"  # noqa: E501
                .format(distribution_strategy, allowed_values)
            )

        self._distribution_strategy = distribution_strategy

    @property
    def node_deletion_delay(self):
        """Gets the node_deletion_delay of this ConnectedKubernetesClusterConfig.  # noqa: E501


        :return: The node_deletion_delay of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :rtype: int
        """
        return self._node_deletion_delay

    @node_deletion_delay.setter
    def node_deletion_delay(self, node_deletion_delay):
        """Sets the node_deletion_delay of this ConnectedKubernetesClusterConfig.


        :param node_deletion_delay: The node_deletion_delay of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :type: int
        """

        self._node_deletion_delay = node_deletion_delay

    @property
    def on_demand_split(self):
        """Gets the on_demand_split of this ConnectedKubernetesClusterConfig.  # noqa: E501


        :return: The on_demand_split of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :rtype: int
        """
        return self._on_demand_split

    @on_demand_split.setter
    def on_demand_split(self, on_demand_split):
        """Sets the on_demand_split of this ConnectedKubernetesClusterConfig.


        :param on_demand_split: The on_demand_split of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :type: int
        """

        self._on_demand_split = on_demand_split

    @property
    def reverse_fallback(self):
        """Gets the reverse_fallback of this ConnectedKubernetesClusterConfig.  # noqa: E501

        The nodes which were replaced by a fallback ondemand node will be retried for spot after this window  # noqa: E501

        :return: The reverse_fallback of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :rtype: str
        """
        return self._reverse_fallback

    @reverse_fallback.setter
    def reverse_fallback(self, reverse_fallback):
        """Sets the reverse_fallback of this ConnectedKubernetesClusterConfig.

        The nodes which were replaced by a fallback ondemand node will be retried for spot after this window  # noqa: E501

        :param reverse_fallback: The reverse_fallback of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :type: str
        """

        self._reverse_fallback = reverse_fallback

    @property
    def spot_distribution(self):
        """Gets the spot_distribution of this ConnectedKubernetesClusterConfig.  # noqa: E501


        :return: The spot_distribution of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :rtype: str
        """
        return self._spot_distribution

    @spot_distribution.setter
    def spot_distribution(self, spot_distribution):
        """Sets the spot_distribution of this ConnectedKubernetesClusterConfig.


        :param spot_distribution: The spot_distribution of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :type: str
        """
        allowed_values = ["ALL", "SpotReady", "None"]  # noqa: E501
        if spot_distribution not in allowed_values:
            raise ValueError(
                "Invalid value for `spot_distribution` ({0}), must be one of {1}"  # noqa: E501
                .format(spot_distribution, allowed_values)
            )

        self._spot_distribution = spot_distribution

    @property
    def spot_split(self):
        """Gets the spot_split of this ConnectedKubernetesClusterConfig.  # noqa: E501


        :return: The spot_split of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :rtype: int
        """
        return self._spot_split

    @spot_split.setter
    def spot_split(self, spot_split):
        """Sets the spot_split of this ConnectedKubernetesClusterConfig.


        :param spot_split: The spot_split of this ConnectedKubernetesClusterConfig.  # noqa: E501
        :type: int
        """

        self._spot_split = spot_split

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
        if issubclass(ConnectedKubernetesClusterConfig, dict):
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
        if not isinstance(other, ConnectedKubernetesClusterConfig):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
