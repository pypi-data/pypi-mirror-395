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
from harness_open_api.models.execution_context_v2 import ExecutionContextV2  # noqa: F401,E501

class GithubExecutionContext(ExecutionContextV2):
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
        'action_path': 'str',
        'github_action': 'str',
        'job_id': 'str',
        'repository': 'str',
        'run_id': 'str',
        'runner_detail': 'RunnerDetail',
        'type': 'str',
        'workflow_ref': 'str'
    }
    if hasattr(ExecutionContextV2, "swagger_types"):
        swagger_types.update(ExecutionContextV2.swagger_types)

    attribute_map = {
        'action_path': 'action_path',
        'github_action': 'github_action',
        'job_id': 'job_id',
        'repository': 'repository',
        'run_id': 'run_id',
        'runner_detail': 'runner_detail',
        'type': 'type',
        'workflow_ref': 'workflow_ref'
    }
    if hasattr(ExecutionContextV2, "attribute_map"):
        attribute_map.update(ExecutionContextV2.attribute_map)

    def __init__(self, action_path=None, github_action=None, job_id=None, repository=None, run_id=None, runner_detail=None, type=None, workflow_ref=None, *args, **kwargs):  # noqa: E501
        """GithubExecutionContext - a model defined in Swagger"""  # noqa: E501
        self._action_path = None
        self._github_action = None
        self._job_id = None
        self._repository = None
        self._run_id = None
        self._runner_detail = None
        self._type = None
        self._workflow_ref = None
        self.discriminator = None
        if action_path is not None:
            self.action_path = action_path
        if github_action is not None:
            self.github_action = github_action
        if job_id is not None:
            self.job_id = job_id
        if repository is not None:
            self.repository = repository
        if run_id is not None:
            self.run_id = run_id
        if runner_detail is not None:
            self.runner_detail = runner_detail
        self.type = type
        if workflow_ref is not None:
            self.workflow_ref = workflow_ref
        ExecutionContextV2.__init__(self, *args, **kwargs)

    @property
    def action_path(self):
        """Gets the action_path of this GithubExecutionContext.  # noqa: E501


        :return: The action_path of this GithubExecutionContext.  # noqa: E501
        :rtype: str
        """
        return self._action_path

    @action_path.setter
    def action_path(self, action_path):
        """Sets the action_path of this GithubExecutionContext.


        :param action_path: The action_path of this GithubExecutionContext.  # noqa: E501
        :type: str
        """

        self._action_path = action_path

    @property
    def github_action(self):
        """Gets the github_action of this GithubExecutionContext.  # noqa: E501


        :return: The github_action of this GithubExecutionContext.  # noqa: E501
        :rtype: str
        """
        return self._github_action

    @github_action.setter
    def github_action(self, github_action):
        """Sets the github_action of this GithubExecutionContext.


        :param github_action: The github_action of this GithubExecutionContext.  # noqa: E501
        :type: str
        """

        self._github_action = github_action

    @property
    def job_id(self):
        """Gets the job_id of this GithubExecutionContext.  # noqa: E501


        :return: The job_id of this GithubExecutionContext.  # noqa: E501
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this GithubExecutionContext.


        :param job_id: The job_id of this GithubExecutionContext.  # noqa: E501
        :type: str
        """

        self._job_id = job_id

    @property
    def repository(self):
        """Gets the repository of this GithubExecutionContext.  # noqa: E501


        :return: The repository of this GithubExecutionContext.  # noqa: E501
        :rtype: str
        """
        return self._repository

    @repository.setter
    def repository(self, repository):
        """Sets the repository of this GithubExecutionContext.


        :param repository: The repository of this GithubExecutionContext.  # noqa: E501
        :type: str
        """

        self._repository = repository

    @property
    def run_id(self):
        """Gets the run_id of this GithubExecutionContext.  # noqa: E501


        :return: The run_id of this GithubExecutionContext.  # noqa: E501
        :rtype: str
        """
        return self._run_id

    @run_id.setter
    def run_id(self, run_id):
        """Sets the run_id of this GithubExecutionContext.


        :param run_id: The run_id of this GithubExecutionContext.  # noqa: E501
        :type: str
        """

        self._run_id = run_id

    @property
    def runner_detail(self):
        """Gets the runner_detail of this GithubExecutionContext.  # noqa: E501


        :return: The runner_detail of this GithubExecutionContext.  # noqa: E501
        :rtype: RunnerDetail
        """
        return self._runner_detail

    @runner_detail.setter
    def runner_detail(self, runner_detail):
        """Sets the runner_detail of this GithubExecutionContext.


        :param runner_detail: The runner_detail of this GithubExecutionContext.  # noqa: E501
        :type: RunnerDetail
        """

        self._runner_detail = runner_detail

    @property
    def type(self):
        """Gets the type of this GithubExecutionContext.  # noqa: E501

        This specifies the type of context  # noqa: E501

        :return: The type of this GithubExecutionContext.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this GithubExecutionContext.

        This specifies the type of context  # noqa: E501

        :param type: The type of this GithubExecutionContext.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["github"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def workflow_ref(self):
        """Gets the workflow_ref of this GithubExecutionContext.  # noqa: E501


        :return: The workflow_ref of this GithubExecutionContext.  # noqa: E501
        :rtype: str
        """
        return self._workflow_ref

    @workflow_ref.setter
    def workflow_ref(self, workflow_ref):
        """Sets the workflow_ref of this GithubExecutionContext.


        :param workflow_ref: The workflow_ref of this GithubExecutionContext.  # noqa: E501
        :type: str
        """

        self._workflow_ref = workflow_ref

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
        if issubclass(GithubExecutionContext, dict):
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
        if not isinstance(other, GithubExecutionContext):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
