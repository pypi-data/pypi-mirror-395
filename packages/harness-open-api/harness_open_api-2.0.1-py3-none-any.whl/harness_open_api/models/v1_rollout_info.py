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

class V1RolloutInfo(object):
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
        'actual_weight': 'str',
        'analysis_runs': 'list[V1RolloutAnalysisRunInfo]',
        'available': 'int',
        'canary_images': 'list[str]',
        'canary_revision': 'int',
        'containers': 'list[V1RolloutContainerInfo]',
        'current': 'int',
        'desired': 'int',
        'experiments': 'list[V1RolloutExperimentInfo]',
        'generation': 'str',
        'icon': 'str',
        'message': 'str',
        'metadata': 'V1ObjectMeta',
        'preview_images': 'list[str]',
        'ready': 'int',
        'replica_sets': 'list[V1RolloutReplicaSetInfo]',
        'restarted_at': 'str',
        'set_weight': 'str',
        'stable_images': 'list[str]',
        'status': 'str',
        'step': 'str',
        'steps': 'list[V1CanaryStep]',
        'strategy': 'str',
        'updated': 'int'
    }

    attribute_map = {
        'actual_weight': 'actualWeight',
        'analysis_runs': 'analysisRuns',
        'available': 'available',
        'canary_images': 'canaryImages',
        'canary_revision': 'canaryRevision',
        'containers': 'containers',
        'current': 'current',
        'desired': 'desired',
        'experiments': 'experiments',
        'generation': 'generation',
        'icon': 'icon',
        'message': 'message',
        'metadata': 'metadata',
        'preview_images': 'previewImages',
        'ready': 'ready',
        'replica_sets': 'replicaSets',
        'restarted_at': 'restartedAt',
        'set_weight': 'setWeight',
        'stable_images': 'stableImages',
        'status': 'status',
        'step': 'step',
        'steps': 'steps',
        'strategy': 'strategy',
        'updated': 'updated'
    }

    def __init__(self, actual_weight=None, analysis_runs=None, available=None, canary_images=None, canary_revision=None, containers=None, current=None, desired=None, experiments=None, generation=None, icon=None, message=None, metadata=None, preview_images=None, ready=None, replica_sets=None, restarted_at=None, set_weight=None, stable_images=None, status=None, step=None, steps=None, strategy=None, updated=None):  # noqa: E501
        """V1RolloutInfo - a model defined in Swagger"""  # noqa: E501
        self._actual_weight = None
        self._analysis_runs = None
        self._available = None
        self._canary_images = None
        self._canary_revision = None
        self._containers = None
        self._current = None
        self._desired = None
        self._experiments = None
        self._generation = None
        self._icon = None
        self._message = None
        self._metadata = None
        self._preview_images = None
        self._ready = None
        self._replica_sets = None
        self._restarted_at = None
        self._set_weight = None
        self._stable_images = None
        self._status = None
        self._step = None
        self._steps = None
        self._strategy = None
        self._updated = None
        self.discriminator = None
        if actual_weight is not None:
            self.actual_weight = actual_weight
        if analysis_runs is not None:
            self.analysis_runs = analysis_runs
        if available is not None:
            self.available = available
        if canary_images is not None:
            self.canary_images = canary_images
        if canary_revision is not None:
            self.canary_revision = canary_revision
        if containers is not None:
            self.containers = containers
        if current is not None:
            self.current = current
        if desired is not None:
            self.desired = desired
        if experiments is not None:
            self.experiments = experiments
        if generation is not None:
            self.generation = generation
        if icon is not None:
            self.icon = icon
        if message is not None:
            self.message = message
        if metadata is not None:
            self.metadata = metadata
        if preview_images is not None:
            self.preview_images = preview_images
        if ready is not None:
            self.ready = ready
        if replica_sets is not None:
            self.replica_sets = replica_sets
        if restarted_at is not None:
            self.restarted_at = restarted_at
        if set_weight is not None:
            self.set_weight = set_weight
        if stable_images is not None:
            self.stable_images = stable_images
        if status is not None:
            self.status = status
        if step is not None:
            self.step = step
        if steps is not None:
            self.steps = steps
        if strategy is not None:
            self.strategy = strategy
        if updated is not None:
            self.updated = updated

    @property
    def actual_weight(self):
        """Gets the actual_weight of this V1RolloutInfo.  # noqa: E501


        :return: The actual_weight of this V1RolloutInfo.  # noqa: E501
        :rtype: str
        """
        return self._actual_weight

    @actual_weight.setter
    def actual_weight(self, actual_weight):
        """Sets the actual_weight of this V1RolloutInfo.


        :param actual_weight: The actual_weight of this V1RolloutInfo.  # noqa: E501
        :type: str
        """

        self._actual_weight = actual_weight

    @property
    def analysis_runs(self):
        """Gets the analysis_runs of this V1RolloutInfo.  # noqa: E501


        :return: The analysis_runs of this V1RolloutInfo.  # noqa: E501
        :rtype: list[V1RolloutAnalysisRunInfo]
        """
        return self._analysis_runs

    @analysis_runs.setter
    def analysis_runs(self, analysis_runs):
        """Sets the analysis_runs of this V1RolloutInfo.


        :param analysis_runs: The analysis_runs of this V1RolloutInfo.  # noqa: E501
        :type: list[V1RolloutAnalysisRunInfo]
        """

        self._analysis_runs = analysis_runs

    @property
    def available(self):
        """Gets the available of this V1RolloutInfo.  # noqa: E501


        :return: The available of this V1RolloutInfo.  # noqa: E501
        :rtype: int
        """
        return self._available

    @available.setter
    def available(self, available):
        """Sets the available of this V1RolloutInfo.


        :param available: The available of this V1RolloutInfo.  # noqa: E501
        :type: int
        """

        self._available = available

    @property
    def canary_images(self):
        """Gets the canary_images of this V1RolloutInfo.  # noqa: E501


        :return: The canary_images of this V1RolloutInfo.  # noqa: E501
        :rtype: list[str]
        """
        return self._canary_images

    @canary_images.setter
    def canary_images(self, canary_images):
        """Sets the canary_images of this V1RolloutInfo.


        :param canary_images: The canary_images of this V1RolloutInfo.  # noqa: E501
        :type: list[str]
        """

        self._canary_images = canary_images

    @property
    def canary_revision(self):
        """Gets the canary_revision of this V1RolloutInfo.  # noqa: E501


        :return: The canary_revision of this V1RolloutInfo.  # noqa: E501
        :rtype: int
        """
        return self._canary_revision

    @canary_revision.setter
    def canary_revision(self, canary_revision):
        """Sets the canary_revision of this V1RolloutInfo.


        :param canary_revision: The canary_revision of this V1RolloutInfo.  # noqa: E501
        :type: int
        """

        self._canary_revision = canary_revision

    @property
    def containers(self):
        """Gets the containers of this V1RolloutInfo.  # noqa: E501


        :return: The containers of this V1RolloutInfo.  # noqa: E501
        :rtype: list[V1RolloutContainerInfo]
        """
        return self._containers

    @containers.setter
    def containers(self, containers):
        """Sets the containers of this V1RolloutInfo.


        :param containers: The containers of this V1RolloutInfo.  # noqa: E501
        :type: list[V1RolloutContainerInfo]
        """

        self._containers = containers

    @property
    def current(self):
        """Gets the current of this V1RolloutInfo.  # noqa: E501


        :return: The current of this V1RolloutInfo.  # noqa: E501
        :rtype: int
        """
        return self._current

    @current.setter
    def current(self, current):
        """Sets the current of this V1RolloutInfo.


        :param current: The current of this V1RolloutInfo.  # noqa: E501
        :type: int
        """

        self._current = current

    @property
    def desired(self):
        """Gets the desired of this V1RolloutInfo.  # noqa: E501


        :return: The desired of this V1RolloutInfo.  # noqa: E501
        :rtype: int
        """
        return self._desired

    @desired.setter
    def desired(self, desired):
        """Sets the desired of this V1RolloutInfo.


        :param desired: The desired of this V1RolloutInfo.  # noqa: E501
        :type: int
        """

        self._desired = desired

    @property
    def experiments(self):
        """Gets the experiments of this V1RolloutInfo.  # noqa: E501


        :return: The experiments of this V1RolloutInfo.  # noqa: E501
        :rtype: list[V1RolloutExperimentInfo]
        """
        return self._experiments

    @experiments.setter
    def experiments(self, experiments):
        """Sets the experiments of this V1RolloutInfo.


        :param experiments: The experiments of this V1RolloutInfo.  # noqa: E501
        :type: list[V1RolloutExperimentInfo]
        """

        self._experiments = experiments

    @property
    def generation(self):
        """Gets the generation of this V1RolloutInfo.  # noqa: E501


        :return: The generation of this V1RolloutInfo.  # noqa: E501
        :rtype: str
        """
        return self._generation

    @generation.setter
    def generation(self, generation):
        """Sets the generation of this V1RolloutInfo.


        :param generation: The generation of this V1RolloutInfo.  # noqa: E501
        :type: str
        """

        self._generation = generation

    @property
    def icon(self):
        """Gets the icon of this V1RolloutInfo.  # noqa: E501


        :return: The icon of this V1RolloutInfo.  # noqa: E501
        :rtype: str
        """
        return self._icon

    @icon.setter
    def icon(self, icon):
        """Sets the icon of this V1RolloutInfo.


        :param icon: The icon of this V1RolloutInfo.  # noqa: E501
        :type: str
        """

        self._icon = icon

    @property
    def message(self):
        """Gets the message of this V1RolloutInfo.  # noqa: E501


        :return: The message of this V1RolloutInfo.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this V1RolloutInfo.


        :param message: The message of this V1RolloutInfo.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def metadata(self):
        """Gets the metadata of this V1RolloutInfo.  # noqa: E501


        :return: The metadata of this V1RolloutInfo.  # noqa: E501
        :rtype: V1ObjectMeta
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this V1RolloutInfo.


        :param metadata: The metadata of this V1RolloutInfo.  # noqa: E501
        :type: V1ObjectMeta
        """

        self._metadata = metadata

    @property
    def preview_images(self):
        """Gets the preview_images of this V1RolloutInfo.  # noqa: E501


        :return: The preview_images of this V1RolloutInfo.  # noqa: E501
        :rtype: list[str]
        """
        return self._preview_images

    @preview_images.setter
    def preview_images(self, preview_images):
        """Sets the preview_images of this V1RolloutInfo.


        :param preview_images: The preview_images of this V1RolloutInfo.  # noqa: E501
        :type: list[str]
        """

        self._preview_images = preview_images

    @property
    def ready(self):
        """Gets the ready of this V1RolloutInfo.  # noqa: E501


        :return: The ready of this V1RolloutInfo.  # noqa: E501
        :rtype: int
        """
        return self._ready

    @ready.setter
    def ready(self, ready):
        """Sets the ready of this V1RolloutInfo.


        :param ready: The ready of this V1RolloutInfo.  # noqa: E501
        :type: int
        """

        self._ready = ready

    @property
    def replica_sets(self):
        """Gets the replica_sets of this V1RolloutInfo.  # noqa: E501


        :return: The replica_sets of this V1RolloutInfo.  # noqa: E501
        :rtype: list[V1RolloutReplicaSetInfo]
        """
        return self._replica_sets

    @replica_sets.setter
    def replica_sets(self, replica_sets):
        """Sets the replica_sets of this V1RolloutInfo.


        :param replica_sets: The replica_sets of this V1RolloutInfo.  # noqa: E501
        :type: list[V1RolloutReplicaSetInfo]
        """

        self._replica_sets = replica_sets

    @property
    def restarted_at(self):
        """Gets the restarted_at of this V1RolloutInfo.  # noqa: E501


        :return: The restarted_at of this V1RolloutInfo.  # noqa: E501
        :rtype: str
        """
        return self._restarted_at

    @restarted_at.setter
    def restarted_at(self, restarted_at):
        """Sets the restarted_at of this V1RolloutInfo.


        :param restarted_at: The restarted_at of this V1RolloutInfo.  # noqa: E501
        :type: str
        """

        self._restarted_at = restarted_at

    @property
    def set_weight(self):
        """Gets the set_weight of this V1RolloutInfo.  # noqa: E501


        :return: The set_weight of this V1RolloutInfo.  # noqa: E501
        :rtype: str
        """
        return self._set_weight

    @set_weight.setter
    def set_weight(self, set_weight):
        """Sets the set_weight of this V1RolloutInfo.


        :param set_weight: The set_weight of this V1RolloutInfo.  # noqa: E501
        :type: str
        """

        self._set_weight = set_weight

    @property
    def stable_images(self):
        """Gets the stable_images of this V1RolloutInfo.  # noqa: E501


        :return: The stable_images of this V1RolloutInfo.  # noqa: E501
        :rtype: list[str]
        """
        return self._stable_images

    @stable_images.setter
    def stable_images(self, stable_images):
        """Sets the stable_images of this V1RolloutInfo.


        :param stable_images: The stable_images of this V1RolloutInfo.  # noqa: E501
        :type: list[str]
        """

        self._stable_images = stable_images

    @property
    def status(self):
        """Gets the status of this V1RolloutInfo.  # noqa: E501


        :return: The status of this V1RolloutInfo.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this V1RolloutInfo.


        :param status: The status of this V1RolloutInfo.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def step(self):
        """Gets the step of this V1RolloutInfo.  # noqa: E501


        :return: The step of this V1RolloutInfo.  # noqa: E501
        :rtype: str
        """
        return self._step

    @step.setter
    def step(self, step):
        """Sets the step of this V1RolloutInfo.


        :param step: The step of this V1RolloutInfo.  # noqa: E501
        :type: str
        """

        self._step = step

    @property
    def steps(self):
        """Gets the steps of this V1RolloutInfo.  # noqa: E501


        :return: The steps of this V1RolloutInfo.  # noqa: E501
        :rtype: list[V1CanaryStep]
        """
        return self._steps

    @steps.setter
    def steps(self, steps):
        """Sets the steps of this V1RolloutInfo.


        :param steps: The steps of this V1RolloutInfo.  # noqa: E501
        :type: list[V1CanaryStep]
        """

        self._steps = steps

    @property
    def strategy(self):
        """Gets the strategy of this V1RolloutInfo.  # noqa: E501


        :return: The strategy of this V1RolloutInfo.  # noqa: E501
        :rtype: str
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        """Sets the strategy of this V1RolloutInfo.


        :param strategy: The strategy of this V1RolloutInfo.  # noqa: E501
        :type: str
        """

        self._strategy = strategy

    @property
    def updated(self):
        """Gets the updated of this V1RolloutInfo.  # noqa: E501


        :return: The updated of this V1RolloutInfo.  # noqa: E501
        :rtype: int
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this V1RolloutInfo.


        :param updated: The updated of this V1RolloutInfo.  # noqa: E501
        :type: int
        """

        self._updated = updated

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
        if issubclass(V1RolloutInfo, dict):
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
        if not isinstance(other, V1RolloutInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
