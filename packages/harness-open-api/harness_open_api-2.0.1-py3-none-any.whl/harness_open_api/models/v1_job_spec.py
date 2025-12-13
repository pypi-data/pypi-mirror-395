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

class V1JobSpec(object):
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
        'active_deadline_seconds': 'str',
        'backoff_limit': 'int',
        'backoff_limit_per_index': 'int',
        'completion_mode': 'str',
        'completions': 'int',
        'managed_by': 'str',
        'manual_selector': 'bool',
        'max_failed_indexes': 'int',
        'parallelism': 'int',
        'pod_failure_policy': 'V1PodFailurePolicy',
        'pod_replacement_policy': 'str',
        'selector': 'V1LabelSelector',
        'success_policy': 'V1SuccessPolicy',
        'suspend': 'bool',
        'template': 'V1PodTemplateSpec',
        'ttl_seconds_after_finished': 'int'
    }

    attribute_map = {
        'active_deadline_seconds': 'activeDeadlineSeconds',
        'backoff_limit': 'backoffLimit',
        'backoff_limit_per_index': 'backoffLimitPerIndex',
        'completion_mode': 'completionMode',
        'completions': 'completions',
        'managed_by': 'managedBy',
        'manual_selector': 'manualSelector',
        'max_failed_indexes': 'maxFailedIndexes',
        'parallelism': 'parallelism',
        'pod_failure_policy': 'podFailurePolicy',
        'pod_replacement_policy': 'podReplacementPolicy',
        'selector': 'selector',
        'success_policy': 'successPolicy',
        'suspend': 'suspend',
        'template': 'template',
        'ttl_seconds_after_finished': 'ttlSecondsAfterFinished'
    }

    def __init__(self, active_deadline_seconds=None, backoff_limit=None, backoff_limit_per_index=None, completion_mode=None, completions=None, managed_by=None, manual_selector=None, max_failed_indexes=None, parallelism=None, pod_failure_policy=None, pod_replacement_policy=None, selector=None, success_policy=None, suspend=None, template=None, ttl_seconds_after_finished=None):  # noqa: E501
        """V1JobSpec - a model defined in Swagger"""  # noqa: E501
        self._active_deadline_seconds = None
        self._backoff_limit = None
        self._backoff_limit_per_index = None
        self._completion_mode = None
        self._completions = None
        self._managed_by = None
        self._manual_selector = None
        self._max_failed_indexes = None
        self._parallelism = None
        self._pod_failure_policy = None
        self._pod_replacement_policy = None
        self._selector = None
        self._success_policy = None
        self._suspend = None
        self._template = None
        self._ttl_seconds_after_finished = None
        self.discriminator = None
        if active_deadline_seconds is not None:
            self.active_deadline_seconds = active_deadline_seconds
        if backoff_limit is not None:
            self.backoff_limit = backoff_limit
        if backoff_limit_per_index is not None:
            self.backoff_limit_per_index = backoff_limit_per_index
        if completion_mode is not None:
            self.completion_mode = completion_mode
        if completions is not None:
            self.completions = completions
        if managed_by is not None:
            self.managed_by = managed_by
        if manual_selector is not None:
            self.manual_selector = manual_selector
        if max_failed_indexes is not None:
            self.max_failed_indexes = max_failed_indexes
        if parallelism is not None:
            self.parallelism = parallelism
        if pod_failure_policy is not None:
            self.pod_failure_policy = pod_failure_policy
        if pod_replacement_policy is not None:
            self.pod_replacement_policy = pod_replacement_policy
        if selector is not None:
            self.selector = selector
        if success_policy is not None:
            self.success_policy = success_policy
        if suspend is not None:
            self.suspend = suspend
        if template is not None:
            self.template = template
        if ttl_seconds_after_finished is not None:
            self.ttl_seconds_after_finished = ttl_seconds_after_finished

    @property
    def active_deadline_seconds(self):
        """Gets the active_deadline_seconds of this V1JobSpec.  # noqa: E501


        :return: The active_deadline_seconds of this V1JobSpec.  # noqa: E501
        :rtype: str
        """
        return self._active_deadline_seconds

    @active_deadline_seconds.setter
    def active_deadline_seconds(self, active_deadline_seconds):
        """Sets the active_deadline_seconds of this V1JobSpec.


        :param active_deadline_seconds: The active_deadline_seconds of this V1JobSpec.  # noqa: E501
        :type: str
        """

        self._active_deadline_seconds = active_deadline_seconds

    @property
    def backoff_limit(self):
        """Gets the backoff_limit of this V1JobSpec.  # noqa: E501


        :return: The backoff_limit of this V1JobSpec.  # noqa: E501
        :rtype: int
        """
        return self._backoff_limit

    @backoff_limit.setter
    def backoff_limit(self, backoff_limit):
        """Sets the backoff_limit of this V1JobSpec.


        :param backoff_limit: The backoff_limit of this V1JobSpec.  # noqa: E501
        :type: int
        """

        self._backoff_limit = backoff_limit

    @property
    def backoff_limit_per_index(self):
        """Gets the backoff_limit_per_index of this V1JobSpec.  # noqa: E501


        :return: The backoff_limit_per_index of this V1JobSpec.  # noqa: E501
        :rtype: int
        """
        return self._backoff_limit_per_index

    @backoff_limit_per_index.setter
    def backoff_limit_per_index(self, backoff_limit_per_index):
        """Sets the backoff_limit_per_index of this V1JobSpec.


        :param backoff_limit_per_index: The backoff_limit_per_index of this V1JobSpec.  # noqa: E501
        :type: int
        """

        self._backoff_limit_per_index = backoff_limit_per_index

    @property
    def completion_mode(self):
        """Gets the completion_mode of this V1JobSpec.  # noqa: E501

        completionMode specifies how Pod completions are tracked. It can be `NonIndexed` (default) or `Indexed`.  `NonIndexed` means that the Job is considered complete when there have been .spec.completions successfully completed Pods. Each Pod completion is homologous to each other.  `Indexed` means that the Pods of a Job get an associated completion index from 0 to (.spec.completions - 1), available in the annotation batch.kubernetes.io/job-completion-index. The Job is considered complete when there is one successfully completed Pod for each index. When value is `Indexed`, .spec.completions must be specified and `.spec.parallelism` must be less than or equal to 10^5. In addition, The Pod name takes the form `$(job-name)-$(index)-$(random-string)`, the Pod hostname takes the form `$(job-name)-$(index)`.  More completion modes can be added in the future. If the Job controller observes a mode that it doesn't recognize, which is possible during upgrades due to version skew, the controller skips updates for the Job. +optional  # noqa: E501

        :return: The completion_mode of this V1JobSpec.  # noqa: E501
        :rtype: str
        """
        return self._completion_mode

    @completion_mode.setter
    def completion_mode(self, completion_mode):
        """Sets the completion_mode of this V1JobSpec.

        completionMode specifies how Pod completions are tracked. It can be `NonIndexed` (default) or `Indexed`.  `NonIndexed` means that the Job is considered complete when there have been .spec.completions successfully completed Pods. Each Pod completion is homologous to each other.  `Indexed` means that the Pods of a Job get an associated completion index from 0 to (.spec.completions - 1), available in the annotation batch.kubernetes.io/job-completion-index. The Job is considered complete when there is one successfully completed Pod for each index. When value is `Indexed`, .spec.completions must be specified and `.spec.parallelism` must be less than or equal to 10^5. In addition, The Pod name takes the form `$(job-name)-$(index)-$(random-string)`, the Pod hostname takes the form `$(job-name)-$(index)`.  More completion modes can be added in the future. If the Job controller observes a mode that it doesn't recognize, which is possible during upgrades due to version skew, the controller skips updates for the Job. +optional  # noqa: E501

        :param completion_mode: The completion_mode of this V1JobSpec.  # noqa: E501
        :type: str
        """

        self._completion_mode = completion_mode

    @property
    def completions(self):
        """Gets the completions of this V1JobSpec.  # noqa: E501


        :return: The completions of this V1JobSpec.  # noqa: E501
        :rtype: int
        """
        return self._completions

    @completions.setter
    def completions(self, completions):
        """Sets the completions of this V1JobSpec.


        :param completions: The completions of this V1JobSpec.  # noqa: E501
        :type: int
        """

        self._completions = completions

    @property
    def managed_by(self):
        """Gets the managed_by of this V1JobSpec.  # noqa: E501

        ManagedBy field indicates the controller that manages a Job. The k8s Job controller reconciles jobs which don't have this field at all or the field value is the reserved string `kubernetes.io/job-controller`, but skips reconciling Jobs with a custom value for this field. The value must be a valid domain-prefixed path (e.g. acme.io/foo) - all characters before the first \"/\" must be a valid subdomain as defined by RFC 1123. All characters trailing the first \"/\" must be valid HTTP Path characters as defined by RFC 3986. The value cannot exceed 63 characters. This field is immutable.  This field is beta-level. The job controller accepts setting the field when the feature gate JobManagedBy is enabled (enabled by default). +optional  # noqa: E501

        :return: The managed_by of this V1JobSpec.  # noqa: E501
        :rtype: str
        """
        return self._managed_by

    @managed_by.setter
    def managed_by(self, managed_by):
        """Sets the managed_by of this V1JobSpec.

        ManagedBy field indicates the controller that manages a Job. The k8s Job controller reconciles jobs which don't have this field at all or the field value is the reserved string `kubernetes.io/job-controller`, but skips reconciling Jobs with a custom value for this field. The value must be a valid domain-prefixed path (e.g. acme.io/foo) - all characters before the first \"/\" must be a valid subdomain as defined by RFC 1123. All characters trailing the first \"/\" must be valid HTTP Path characters as defined by RFC 3986. The value cannot exceed 63 characters. This field is immutable.  This field is beta-level. The job controller accepts setting the field when the feature gate JobManagedBy is enabled (enabled by default). +optional  # noqa: E501

        :param managed_by: The managed_by of this V1JobSpec.  # noqa: E501
        :type: str
        """

        self._managed_by = managed_by

    @property
    def manual_selector(self):
        """Gets the manual_selector of this V1JobSpec.  # noqa: E501


        :return: The manual_selector of this V1JobSpec.  # noqa: E501
        :rtype: bool
        """
        return self._manual_selector

    @manual_selector.setter
    def manual_selector(self, manual_selector):
        """Sets the manual_selector of this V1JobSpec.


        :param manual_selector: The manual_selector of this V1JobSpec.  # noqa: E501
        :type: bool
        """

        self._manual_selector = manual_selector

    @property
    def max_failed_indexes(self):
        """Gets the max_failed_indexes of this V1JobSpec.  # noqa: E501


        :return: The max_failed_indexes of this V1JobSpec.  # noqa: E501
        :rtype: int
        """
        return self._max_failed_indexes

    @max_failed_indexes.setter
    def max_failed_indexes(self, max_failed_indexes):
        """Sets the max_failed_indexes of this V1JobSpec.


        :param max_failed_indexes: The max_failed_indexes of this V1JobSpec.  # noqa: E501
        :type: int
        """

        self._max_failed_indexes = max_failed_indexes

    @property
    def parallelism(self):
        """Gets the parallelism of this V1JobSpec.  # noqa: E501


        :return: The parallelism of this V1JobSpec.  # noqa: E501
        :rtype: int
        """
        return self._parallelism

    @parallelism.setter
    def parallelism(self, parallelism):
        """Sets the parallelism of this V1JobSpec.


        :param parallelism: The parallelism of this V1JobSpec.  # noqa: E501
        :type: int
        """

        self._parallelism = parallelism

    @property
    def pod_failure_policy(self):
        """Gets the pod_failure_policy of this V1JobSpec.  # noqa: E501


        :return: The pod_failure_policy of this V1JobSpec.  # noqa: E501
        :rtype: V1PodFailurePolicy
        """
        return self._pod_failure_policy

    @pod_failure_policy.setter
    def pod_failure_policy(self, pod_failure_policy):
        """Sets the pod_failure_policy of this V1JobSpec.


        :param pod_failure_policy: The pod_failure_policy of this V1JobSpec.  # noqa: E501
        :type: V1PodFailurePolicy
        """

        self._pod_failure_policy = pod_failure_policy

    @property
    def pod_replacement_policy(self):
        """Gets the pod_replacement_policy of this V1JobSpec.  # noqa: E501

        podReplacementPolicy specifies when to create replacement Pods. Possible values are: - TerminatingOrFailed means that we recreate pods   when they are terminating (has a metadata.deletionTimestamp) or failed. - Failed means to wait until a previously created Pod is fully terminated (has phase   Failed or Succeeded) before creating a replacement Pod.  When using podFailurePolicy, Failed is the the only allowed value. TerminatingOrFailed and Failed are allowed values when podFailurePolicy is not in use. This is an beta field. To use this, enable the JobPodReplacementPolicy feature toggle. This is on by default. +optional  # noqa: E501

        :return: The pod_replacement_policy of this V1JobSpec.  # noqa: E501
        :rtype: str
        """
        return self._pod_replacement_policy

    @pod_replacement_policy.setter
    def pod_replacement_policy(self, pod_replacement_policy):
        """Sets the pod_replacement_policy of this V1JobSpec.

        podReplacementPolicy specifies when to create replacement Pods. Possible values are: - TerminatingOrFailed means that we recreate pods   when they are terminating (has a metadata.deletionTimestamp) or failed. - Failed means to wait until a previously created Pod is fully terminated (has phase   Failed or Succeeded) before creating a replacement Pod.  When using podFailurePolicy, Failed is the the only allowed value. TerminatingOrFailed and Failed are allowed values when podFailurePolicy is not in use. This is an beta field. To use this, enable the JobPodReplacementPolicy feature toggle. This is on by default. +optional  # noqa: E501

        :param pod_replacement_policy: The pod_replacement_policy of this V1JobSpec.  # noqa: E501
        :type: str
        """

        self._pod_replacement_policy = pod_replacement_policy

    @property
    def selector(self):
        """Gets the selector of this V1JobSpec.  # noqa: E501


        :return: The selector of this V1JobSpec.  # noqa: E501
        :rtype: V1LabelSelector
        """
        return self._selector

    @selector.setter
    def selector(self, selector):
        """Sets the selector of this V1JobSpec.


        :param selector: The selector of this V1JobSpec.  # noqa: E501
        :type: V1LabelSelector
        """

        self._selector = selector

    @property
    def success_policy(self):
        """Gets the success_policy of this V1JobSpec.  # noqa: E501


        :return: The success_policy of this V1JobSpec.  # noqa: E501
        :rtype: V1SuccessPolicy
        """
        return self._success_policy

    @success_policy.setter
    def success_policy(self, success_policy):
        """Sets the success_policy of this V1JobSpec.


        :param success_policy: The success_policy of this V1JobSpec.  # noqa: E501
        :type: V1SuccessPolicy
        """

        self._success_policy = success_policy

    @property
    def suspend(self):
        """Gets the suspend of this V1JobSpec.  # noqa: E501

        suspend specifies whether the Job controller should create Pods or not. If a Job is created with suspend set to true, no Pods are created by the Job controller. If a Job is suspended after creation (i.e. the flag goes from false to true), the Job controller will delete all active Pods associated with this Job. Users must design their workload to gracefully handle this. Suspending a Job will reset the StartTime field of the Job, effectively resetting the ActiveDeadlineSeconds timer too. Defaults to false.  +optional  # noqa: E501

        :return: The suspend of this V1JobSpec.  # noqa: E501
        :rtype: bool
        """
        return self._suspend

    @suspend.setter
    def suspend(self, suspend):
        """Sets the suspend of this V1JobSpec.

        suspend specifies whether the Job controller should create Pods or not. If a Job is created with suspend set to true, no Pods are created by the Job controller. If a Job is suspended after creation (i.e. the flag goes from false to true), the Job controller will delete all active Pods associated with this Job. Users must design their workload to gracefully handle this. Suspending a Job will reset the StartTime field of the Job, effectively resetting the ActiveDeadlineSeconds timer too. Defaults to false.  +optional  # noqa: E501

        :param suspend: The suspend of this V1JobSpec.  # noqa: E501
        :type: bool
        """

        self._suspend = suspend

    @property
    def template(self):
        """Gets the template of this V1JobSpec.  # noqa: E501


        :return: The template of this V1JobSpec.  # noqa: E501
        :rtype: V1PodTemplateSpec
        """
        return self._template

    @template.setter
    def template(self, template):
        """Sets the template of this V1JobSpec.


        :param template: The template of this V1JobSpec.  # noqa: E501
        :type: V1PodTemplateSpec
        """

        self._template = template

    @property
    def ttl_seconds_after_finished(self):
        """Gets the ttl_seconds_after_finished of this V1JobSpec.  # noqa: E501


        :return: The ttl_seconds_after_finished of this V1JobSpec.  # noqa: E501
        :rtype: int
        """
        return self._ttl_seconds_after_finished

    @ttl_seconds_after_finished.setter
    def ttl_seconds_after_finished(self, ttl_seconds_after_finished):
        """Sets the ttl_seconds_after_finished of this V1JobSpec.


        :param ttl_seconds_after_finished: The ttl_seconds_after_finished of this V1JobSpec.  # noqa: E501
        :type: int
        """

        self._ttl_seconds_after_finished = ttl_seconds_after_finished

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
        if issubclass(V1JobSpec, dict):
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
        if not isinstance(other, V1JobSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
