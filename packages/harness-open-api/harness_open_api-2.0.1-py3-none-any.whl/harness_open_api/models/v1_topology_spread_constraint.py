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

class V1TopologySpreadConstraint(object):
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
        'label_selector': 'V1LabelSelector',
        'match_label_keys': 'list[str]',
        'max_skew': 'int',
        'min_domains': 'int',
        'node_affinity_policy': 'str',
        'node_taints_policy': 'str',
        'topology_key': 'str',
        'when_unsatisfiable': 'str'
    }

    attribute_map = {
        'label_selector': 'labelSelector',
        'match_label_keys': 'matchLabelKeys',
        'max_skew': 'maxSkew',
        'min_domains': 'minDomains',
        'node_affinity_policy': 'nodeAffinityPolicy',
        'node_taints_policy': 'nodeTaintsPolicy',
        'topology_key': 'topologyKey',
        'when_unsatisfiable': 'whenUnsatisfiable'
    }

    def __init__(self, label_selector=None, match_label_keys=None, max_skew=None, min_domains=None, node_affinity_policy=None, node_taints_policy=None, topology_key=None, when_unsatisfiable=None):  # noqa: E501
        """V1TopologySpreadConstraint - a model defined in Swagger"""  # noqa: E501
        self._label_selector = None
        self._match_label_keys = None
        self._max_skew = None
        self._min_domains = None
        self._node_affinity_policy = None
        self._node_taints_policy = None
        self._topology_key = None
        self._when_unsatisfiable = None
        self.discriminator = None
        if label_selector is not None:
            self.label_selector = label_selector
        if match_label_keys is not None:
            self.match_label_keys = match_label_keys
        if max_skew is not None:
            self.max_skew = max_skew
        if min_domains is not None:
            self.min_domains = min_domains
        if node_affinity_policy is not None:
            self.node_affinity_policy = node_affinity_policy
        if node_taints_policy is not None:
            self.node_taints_policy = node_taints_policy
        if topology_key is not None:
            self.topology_key = topology_key
        if when_unsatisfiable is not None:
            self.when_unsatisfiable = when_unsatisfiable

    @property
    def label_selector(self):
        """Gets the label_selector of this V1TopologySpreadConstraint.  # noqa: E501


        :return: The label_selector of this V1TopologySpreadConstraint.  # noqa: E501
        :rtype: V1LabelSelector
        """
        return self._label_selector

    @label_selector.setter
    def label_selector(self, label_selector):
        """Sets the label_selector of this V1TopologySpreadConstraint.


        :param label_selector: The label_selector of this V1TopologySpreadConstraint.  # noqa: E501
        :type: V1LabelSelector
        """

        self._label_selector = label_selector

    @property
    def match_label_keys(self):
        """Gets the match_label_keys of this V1TopologySpreadConstraint.  # noqa: E501

        MatchLabelKeys is a set of pod label keys to select the pods over which spreading will be calculated. The keys are used to lookup values from the incoming pod labels, those key-value labels are ANDed with labelSelector to select the group of existing pods over which spreading will be calculated for the incoming pod. The same key is forbidden to exist in both MatchLabelKeys and LabelSelector. MatchLabelKeys cannot be set when LabelSelector isn't set. Keys that don't exist in the incoming pod labels will be ignored. A null or empty list means only match against labelSelector.  This is a beta field and requires the MatchLabelKeysInPodTopologySpread feature gate to be enabled (enabled by default). +listType=atomic +optional  # noqa: E501

        :return: The match_label_keys of this V1TopologySpreadConstraint.  # noqa: E501
        :rtype: list[str]
        """
        return self._match_label_keys

    @match_label_keys.setter
    def match_label_keys(self, match_label_keys):
        """Sets the match_label_keys of this V1TopologySpreadConstraint.

        MatchLabelKeys is a set of pod label keys to select the pods over which spreading will be calculated. The keys are used to lookup values from the incoming pod labels, those key-value labels are ANDed with labelSelector to select the group of existing pods over which spreading will be calculated for the incoming pod. The same key is forbidden to exist in both MatchLabelKeys and LabelSelector. MatchLabelKeys cannot be set when LabelSelector isn't set. Keys that don't exist in the incoming pod labels will be ignored. A null or empty list means only match against labelSelector.  This is a beta field and requires the MatchLabelKeysInPodTopologySpread feature gate to be enabled (enabled by default). +listType=atomic +optional  # noqa: E501

        :param match_label_keys: The match_label_keys of this V1TopologySpreadConstraint.  # noqa: E501
        :type: list[str]
        """

        self._match_label_keys = match_label_keys

    @property
    def max_skew(self):
        """Gets the max_skew of this V1TopologySpreadConstraint.  # noqa: E501

        MaxSkew describes the degree to which pods may be unevenly distributed. When `whenUnsatisfiable=DoNotSchedule`, it is the maximum permitted difference between the number of matching pods in the target topology and the global minimum. The global minimum is the minimum number of matching pods in an eligible domain or zero if the number of eligible domains is less than MinDomains. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same labelSelector spread as 2/2/1: In this case, the global minimum is 1. +-------+-------+-------+ | zone1 | zone2 | zone3 | +-------+-------+-------+ |  P P  |  P P  |   P   | +-------+-------+-------+ - if MaxSkew is 1, incoming pod can only be scheduled to zone3 to become 2/2/2; scheduling it onto zone1(zone2) would make the ActualSkew(3-1) on zone1(zone2) violate MaxSkew(1). - if MaxSkew is 2, incoming pod can be scheduled onto any zone. When `whenUnsatisfiable=ScheduleAnyway`, it is used to give higher precedence to topologies that satisfy it. It's a required field. Default value is 1 and 0 is not allowed.  # noqa: E501

        :return: The max_skew of this V1TopologySpreadConstraint.  # noqa: E501
        :rtype: int
        """
        return self._max_skew

    @max_skew.setter
    def max_skew(self, max_skew):
        """Sets the max_skew of this V1TopologySpreadConstraint.

        MaxSkew describes the degree to which pods may be unevenly distributed. When `whenUnsatisfiable=DoNotSchedule`, it is the maximum permitted difference between the number of matching pods in the target topology and the global minimum. The global minimum is the minimum number of matching pods in an eligible domain or zero if the number of eligible domains is less than MinDomains. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same labelSelector spread as 2/2/1: In this case, the global minimum is 1. +-------+-------+-------+ | zone1 | zone2 | zone3 | +-------+-------+-------+ |  P P  |  P P  |   P   | +-------+-------+-------+ - if MaxSkew is 1, incoming pod can only be scheduled to zone3 to become 2/2/2; scheduling it onto zone1(zone2) would make the ActualSkew(3-1) on zone1(zone2) violate MaxSkew(1). - if MaxSkew is 2, incoming pod can be scheduled onto any zone. When `whenUnsatisfiable=ScheduleAnyway`, it is used to give higher precedence to topologies that satisfy it. It's a required field. Default value is 1 and 0 is not allowed.  # noqa: E501

        :param max_skew: The max_skew of this V1TopologySpreadConstraint.  # noqa: E501
        :type: int
        """

        self._max_skew = max_skew

    @property
    def min_domains(self):
        """Gets the min_domains of this V1TopologySpreadConstraint.  # noqa: E501

        MinDomains indicates a minimum number of eligible domains. When the number of eligible domains with matching topology keys is less than minDomains, Pod Topology Spread treats \"global minimum\" as 0, and then the calculation of Skew is performed. And when the number of eligible domains with matching topology keys equals or greater than minDomains, this value has no effect on scheduling. As a result, when the number of eligible domains is less than minDomains, scheduler won't schedule more than maxSkew Pods to those domains. If value is nil, the constraint behaves as if MinDomains is equal to 1. Valid values are integers greater than 0. When value is not nil, WhenUnsatisfiable must be DoNotSchedule.  For example, in a 3-zone cluster, MaxSkew is set to 2, MinDomains is set to 5 and pods with the same labelSelector spread as 2/2/2: +-------+-------+-------+ | zone1 | zone2 | zone3 | +-------+-------+-------+ |  P P  |  P P  |  P P  | +-------+-------+-------+ The number of domains is less than 5(MinDomains), so \"global minimum\" is treated as 0. In this situation, new pod with the same labelSelector cannot be scheduled, because computed skew will be 3(3 - 0) if new Pod is scheduled to any of the three zones, it will violate MaxSkew. +optional  # noqa: E501

        :return: The min_domains of this V1TopologySpreadConstraint.  # noqa: E501
        :rtype: int
        """
        return self._min_domains

    @min_domains.setter
    def min_domains(self, min_domains):
        """Sets the min_domains of this V1TopologySpreadConstraint.

        MinDomains indicates a minimum number of eligible domains. When the number of eligible domains with matching topology keys is less than minDomains, Pod Topology Spread treats \"global minimum\" as 0, and then the calculation of Skew is performed. And when the number of eligible domains with matching topology keys equals or greater than minDomains, this value has no effect on scheduling. As a result, when the number of eligible domains is less than minDomains, scheduler won't schedule more than maxSkew Pods to those domains. If value is nil, the constraint behaves as if MinDomains is equal to 1. Valid values are integers greater than 0. When value is not nil, WhenUnsatisfiable must be DoNotSchedule.  For example, in a 3-zone cluster, MaxSkew is set to 2, MinDomains is set to 5 and pods with the same labelSelector spread as 2/2/2: +-------+-------+-------+ | zone1 | zone2 | zone3 | +-------+-------+-------+ |  P P  |  P P  |  P P  | +-------+-------+-------+ The number of domains is less than 5(MinDomains), so \"global minimum\" is treated as 0. In this situation, new pod with the same labelSelector cannot be scheduled, because computed skew will be 3(3 - 0) if new Pod is scheduled to any of the three zones, it will violate MaxSkew. +optional  # noqa: E501

        :param min_domains: The min_domains of this V1TopologySpreadConstraint.  # noqa: E501
        :type: int
        """

        self._min_domains = min_domains

    @property
    def node_affinity_policy(self):
        """Gets the node_affinity_policy of this V1TopologySpreadConstraint.  # noqa: E501

        NodeAffinityPolicy indicates how we will treat Pod's nodeAffinity/nodeSelector when calculating pod topology spread skew. Options are: - Honor: only nodes matching nodeAffinity/nodeSelector are included in the calculations. - Ignore: nodeAffinity/nodeSelector are ignored. All nodes are included in the calculations.  If this value is nil, the behavior is equivalent to the Honor policy. This is a beta-level feature default enabled by the NodeInclusionPolicyInPodTopologySpread feature flag. +optional  # noqa: E501

        :return: The node_affinity_policy of this V1TopologySpreadConstraint.  # noqa: E501
        :rtype: str
        """
        return self._node_affinity_policy

    @node_affinity_policy.setter
    def node_affinity_policy(self, node_affinity_policy):
        """Sets the node_affinity_policy of this V1TopologySpreadConstraint.

        NodeAffinityPolicy indicates how we will treat Pod's nodeAffinity/nodeSelector when calculating pod topology spread skew. Options are: - Honor: only nodes matching nodeAffinity/nodeSelector are included in the calculations. - Ignore: nodeAffinity/nodeSelector are ignored. All nodes are included in the calculations.  If this value is nil, the behavior is equivalent to the Honor policy. This is a beta-level feature default enabled by the NodeInclusionPolicyInPodTopologySpread feature flag. +optional  # noqa: E501

        :param node_affinity_policy: The node_affinity_policy of this V1TopologySpreadConstraint.  # noqa: E501
        :type: str
        """

        self._node_affinity_policy = node_affinity_policy

    @property
    def node_taints_policy(self):
        """Gets the node_taints_policy of this V1TopologySpreadConstraint.  # noqa: E501

        NodeTaintsPolicy indicates how we will treat node taints when calculating pod topology spread skew. Options are: - Honor: nodes without taints, along with tainted nodes for which the incoming pod has a toleration, are included. - Ignore: node taints are ignored. All nodes are included.  If this value is nil, the behavior is equivalent to the Ignore policy. This is a beta-level feature default enabled by the NodeInclusionPolicyInPodTopologySpread feature flag. +optional  # noqa: E501

        :return: The node_taints_policy of this V1TopologySpreadConstraint.  # noqa: E501
        :rtype: str
        """
        return self._node_taints_policy

    @node_taints_policy.setter
    def node_taints_policy(self, node_taints_policy):
        """Sets the node_taints_policy of this V1TopologySpreadConstraint.

        NodeTaintsPolicy indicates how we will treat node taints when calculating pod topology spread skew. Options are: - Honor: nodes without taints, along with tainted nodes for which the incoming pod has a toleration, are included. - Ignore: node taints are ignored. All nodes are included.  If this value is nil, the behavior is equivalent to the Ignore policy. This is a beta-level feature default enabled by the NodeInclusionPolicyInPodTopologySpread feature flag. +optional  # noqa: E501

        :param node_taints_policy: The node_taints_policy of this V1TopologySpreadConstraint.  # noqa: E501
        :type: str
        """

        self._node_taints_policy = node_taints_policy

    @property
    def topology_key(self):
        """Gets the topology_key of this V1TopologySpreadConstraint.  # noqa: E501

        TopologyKey is the key of node labels. Nodes that have a label with this key and identical values are considered to be in the same topology. We consider each <key, value> as a \"bucket\", and try to put balanced number of pods into each bucket. We define a domain as a particular instance of a topology. Also, we define an eligible domain as a domain whose nodes meet the requirements of nodeAffinityPolicy and nodeTaintsPolicy. e.g. If TopologyKey is \"kubernetes.io/hostname\", each Node is a domain of that topology. And, if TopologyKey is \"topology.kubernetes.io/zone\", each zone is a domain of that topology. It's a required field.  # noqa: E501

        :return: The topology_key of this V1TopologySpreadConstraint.  # noqa: E501
        :rtype: str
        """
        return self._topology_key

    @topology_key.setter
    def topology_key(self, topology_key):
        """Sets the topology_key of this V1TopologySpreadConstraint.

        TopologyKey is the key of node labels. Nodes that have a label with this key and identical values are considered to be in the same topology. We consider each <key, value> as a \"bucket\", and try to put balanced number of pods into each bucket. We define a domain as a particular instance of a topology. Also, we define an eligible domain as a domain whose nodes meet the requirements of nodeAffinityPolicy and nodeTaintsPolicy. e.g. If TopologyKey is \"kubernetes.io/hostname\", each Node is a domain of that topology. And, if TopologyKey is \"topology.kubernetes.io/zone\", each zone is a domain of that topology. It's a required field.  # noqa: E501

        :param topology_key: The topology_key of this V1TopologySpreadConstraint.  # noqa: E501
        :type: str
        """

        self._topology_key = topology_key

    @property
    def when_unsatisfiable(self):
        """Gets the when_unsatisfiable of this V1TopologySpreadConstraint.  # noqa: E501

        WhenUnsatisfiable indicates how to deal with a pod if it doesn't satisfy the spread constraint. - DoNotSchedule (default) tells the scheduler not to schedule it. - ScheduleAnyway tells the scheduler to schedule the pod in any location,   but giving higher precedence to topologies that would help reduce the   skew. A constraint is considered \"Unsatisfiable\" for an incoming pod if and only if every possible node assignment for that pod would violate \"MaxSkew\" on some topology. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same labelSelector spread as 3/1/1: +-------+-------+-------+ | zone1 | zone2 | zone3 | +-------+-------+-------+ | P P P |   P   |   P   | +-------+-------+-------+ If WhenUnsatisfiable is set to DoNotSchedule, incoming pod can only be scheduled to zone2(zone3) to become 3/2/1(3/1/2) as ActualSkew(2-1) on zone2(zone3) satisfies MaxSkew(1). In other words, the cluster can still be imbalanced, but scheduler won't make it *more* imbalanced. It's a required field.  # noqa: E501

        :return: The when_unsatisfiable of this V1TopologySpreadConstraint.  # noqa: E501
        :rtype: str
        """
        return self._when_unsatisfiable

    @when_unsatisfiable.setter
    def when_unsatisfiable(self, when_unsatisfiable):
        """Sets the when_unsatisfiable of this V1TopologySpreadConstraint.

        WhenUnsatisfiable indicates how to deal with a pod if it doesn't satisfy the spread constraint. - DoNotSchedule (default) tells the scheduler not to schedule it. - ScheduleAnyway tells the scheduler to schedule the pod in any location,   but giving higher precedence to topologies that would help reduce the   skew. A constraint is considered \"Unsatisfiable\" for an incoming pod if and only if every possible node assignment for that pod would violate \"MaxSkew\" on some topology. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same labelSelector spread as 3/1/1: +-------+-------+-------+ | zone1 | zone2 | zone3 | +-------+-------+-------+ | P P P |   P   |   P   | +-------+-------+-------+ If WhenUnsatisfiable is set to DoNotSchedule, incoming pod can only be scheduled to zone2(zone3) to become 3/2/1(3/1/2) as ActualSkew(2-1) on zone2(zone3) satisfies MaxSkew(1). In other words, the cluster can still be imbalanced, but scheduler won't make it *more* imbalanced. It's a required field.  # noqa: E501

        :param when_unsatisfiable: The when_unsatisfiable of this V1TopologySpreadConstraint.  # noqa: E501
        :type: str
        """

        self._when_unsatisfiable = when_unsatisfiable

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
        if issubclass(V1TopologySpreadConstraint, dict):
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
        if not isinstance(other, V1TopologySpreadConstraint):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
