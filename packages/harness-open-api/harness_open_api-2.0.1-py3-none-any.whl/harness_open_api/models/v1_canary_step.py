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

class V1CanaryStep(object):
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
        'analysis': 'V1RolloutAnalysis',
        'experiment': 'V1RolloutExperimentStep',
        'pause': 'V1RolloutPause',
        'set_canary_scale': 'V1SetCanaryScale',
        'set_header_route': 'V1SetHeaderRoute',
        'set_mirror_route': 'V1SetMirrorRoute',
        'set_weight': 'int'
    }

    attribute_map = {
        'analysis': 'analysis',
        'experiment': 'experiment',
        'pause': 'pause',
        'set_canary_scale': 'setCanaryScale',
        'set_header_route': 'setHeaderRoute',
        'set_mirror_route': 'setMirrorRoute',
        'set_weight': 'setWeight'
    }

    def __init__(self, analysis=None, experiment=None, pause=None, set_canary_scale=None, set_header_route=None, set_mirror_route=None, set_weight=None):  # noqa: E501
        """V1CanaryStep - a model defined in Swagger"""  # noqa: E501
        self._analysis = None
        self._experiment = None
        self._pause = None
        self._set_canary_scale = None
        self._set_header_route = None
        self._set_mirror_route = None
        self._set_weight = None
        self.discriminator = None
        if analysis is not None:
            self.analysis = analysis
        if experiment is not None:
            self.experiment = experiment
        if pause is not None:
            self.pause = pause
        if set_canary_scale is not None:
            self.set_canary_scale = set_canary_scale
        if set_header_route is not None:
            self.set_header_route = set_header_route
        if set_mirror_route is not None:
            self.set_mirror_route = set_mirror_route
        if set_weight is not None:
            self.set_weight = set_weight

    @property
    def analysis(self):
        """Gets the analysis of this V1CanaryStep.  # noqa: E501


        :return: The analysis of this V1CanaryStep.  # noqa: E501
        :rtype: V1RolloutAnalysis
        """
        return self._analysis

    @analysis.setter
    def analysis(self, analysis):
        """Sets the analysis of this V1CanaryStep.


        :param analysis: The analysis of this V1CanaryStep.  # noqa: E501
        :type: V1RolloutAnalysis
        """

        self._analysis = analysis

    @property
    def experiment(self):
        """Gets the experiment of this V1CanaryStep.  # noqa: E501


        :return: The experiment of this V1CanaryStep.  # noqa: E501
        :rtype: V1RolloutExperimentStep
        """
        return self._experiment

    @experiment.setter
    def experiment(self, experiment):
        """Sets the experiment of this V1CanaryStep.


        :param experiment: The experiment of this V1CanaryStep.  # noqa: E501
        :type: V1RolloutExperimentStep
        """

        self._experiment = experiment

    @property
    def pause(self):
        """Gets the pause of this V1CanaryStep.  # noqa: E501


        :return: The pause of this V1CanaryStep.  # noqa: E501
        :rtype: V1RolloutPause
        """
        return self._pause

    @pause.setter
    def pause(self, pause):
        """Sets the pause of this V1CanaryStep.


        :param pause: The pause of this V1CanaryStep.  # noqa: E501
        :type: V1RolloutPause
        """

        self._pause = pause

    @property
    def set_canary_scale(self):
        """Gets the set_canary_scale of this V1CanaryStep.  # noqa: E501


        :return: The set_canary_scale of this V1CanaryStep.  # noqa: E501
        :rtype: V1SetCanaryScale
        """
        return self._set_canary_scale

    @set_canary_scale.setter
    def set_canary_scale(self, set_canary_scale):
        """Sets the set_canary_scale of this V1CanaryStep.


        :param set_canary_scale: The set_canary_scale of this V1CanaryStep.  # noqa: E501
        :type: V1SetCanaryScale
        """

        self._set_canary_scale = set_canary_scale

    @property
    def set_header_route(self):
        """Gets the set_header_route of this V1CanaryStep.  # noqa: E501


        :return: The set_header_route of this V1CanaryStep.  # noqa: E501
        :rtype: V1SetHeaderRoute
        """
        return self._set_header_route

    @set_header_route.setter
    def set_header_route(self, set_header_route):
        """Sets the set_header_route of this V1CanaryStep.


        :param set_header_route: The set_header_route of this V1CanaryStep.  # noqa: E501
        :type: V1SetHeaderRoute
        """

        self._set_header_route = set_header_route

    @property
    def set_mirror_route(self):
        """Gets the set_mirror_route of this V1CanaryStep.  # noqa: E501


        :return: The set_mirror_route of this V1CanaryStep.  # noqa: E501
        :rtype: V1SetMirrorRoute
        """
        return self._set_mirror_route

    @set_mirror_route.setter
    def set_mirror_route(self, set_mirror_route):
        """Sets the set_mirror_route of this V1CanaryStep.


        :param set_mirror_route: The set_mirror_route of this V1CanaryStep.  # noqa: E501
        :type: V1SetMirrorRoute
        """

        self._set_mirror_route = set_mirror_route

    @property
    def set_weight(self):
        """Gets the set_weight of this V1CanaryStep.  # noqa: E501


        :return: The set_weight of this V1CanaryStep.  # noqa: E501
        :rtype: int
        """
        return self._set_weight

    @set_weight.setter
    def set_weight(self, set_weight):
        """Sets the set_weight of this V1CanaryStep.


        :param set_weight: The set_weight of this V1CanaryStep.  # noqa: E501
        :type: int
        """

        self._set_weight = set_weight

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
        if issubclass(V1CanaryStep, dict):
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
        if not isinstance(other, V1CanaryStep):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
