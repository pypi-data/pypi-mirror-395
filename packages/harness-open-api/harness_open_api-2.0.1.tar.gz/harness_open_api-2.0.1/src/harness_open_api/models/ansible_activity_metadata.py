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

class AnsibleActivityMetadata(object):
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
        'activity_status': 'str',
        'git_branch': 'str',
        'git_commit_message': 'str',
        'git_commit_sha': 'str',
        'git_repo': 'str',
        'pipeline': 'str',
        'pipeline_execution_id': 'str',
        'pipeline_execution_number': 'str',
        'pipeline_name': 'str',
        'pipeline_stage_id': 'str',
        'results_uuid': 'str',
        'trigger': 'dict(str, object)'
    }

    attribute_map = {
        'activity_status': 'activity_status',
        'git_branch': 'git_branch',
        'git_commit_message': 'git_commit_message',
        'git_commit_sha': 'git_commit_sha',
        'git_repo': 'git_repo',
        'pipeline': 'pipeline',
        'pipeline_execution_id': 'pipeline_execution_id',
        'pipeline_execution_number': 'pipeline_execution_number',
        'pipeline_name': 'pipeline_name',
        'pipeline_stage_id': 'pipeline_stage_id',
        'results_uuid': 'results_uuid',
        'trigger': 'trigger'
    }

    def __init__(self, activity_status=None, git_branch=None, git_commit_message=None, git_commit_sha=None, git_repo=None, pipeline=None, pipeline_execution_id=None, pipeline_execution_number=None, pipeline_name=None, pipeline_stage_id=None, results_uuid=None, trigger=None):  # noqa: E501
        """AnsibleActivityMetadata - a model defined in Swagger"""  # noqa: E501
        self._activity_status = None
        self._git_branch = None
        self._git_commit_message = None
        self._git_commit_sha = None
        self._git_repo = None
        self._pipeline = None
        self._pipeline_execution_id = None
        self._pipeline_execution_number = None
        self._pipeline_name = None
        self._pipeline_stage_id = None
        self._results_uuid = None
        self._trigger = None
        self.discriminator = None
        if activity_status is not None:
            self.activity_status = activity_status
        if git_branch is not None:
            self.git_branch = git_branch
        if git_commit_message is not None:
            self.git_commit_message = git_commit_message
        if git_commit_sha is not None:
            self.git_commit_sha = git_commit_sha
        if git_repo is not None:
            self.git_repo = git_repo
        if pipeline is not None:
            self.pipeline = pipeline
        if pipeline_execution_id is not None:
            self.pipeline_execution_id = pipeline_execution_id
        if pipeline_execution_number is not None:
            self.pipeline_execution_number = pipeline_execution_number
        if pipeline_name is not None:
            self.pipeline_name = pipeline_name
        if pipeline_stage_id is not None:
            self.pipeline_stage_id = pipeline_stage_id
        if results_uuid is not None:
            self.results_uuid = results_uuid
        if trigger is not None:
            self.trigger = trigger

    @property
    def activity_status(self):
        """Gets the activity_status of this AnsibleActivityMetadata.  # noqa: E501

        The status of this activity  # noqa: E501

        :return: The activity_status of this AnsibleActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._activity_status

    @activity_status.setter
    def activity_status(self, activity_status):
        """Sets the activity_status of this AnsibleActivityMetadata.

        The status of this activity  # noqa: E501

        :param activity_status: The activity_status of this AnsibleActivityMetadata.  # noqa: E501
        :type: str
        """

        self._activity_status = activity_status

    @property
    def git_branch(self):
        """Gets the git_branch of this AnsibleActivityMetadata.  # noqa: E501

        Git branch associated with this execution  # noqa: E501

        :return: The git_branch of this AnsibleActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._git_branch

    @git_branch.setter
    def git_branch(self, git_branch):
        """Sets the git_branch of this AnsibleActivityMetadata.

        Git branch associated with this execution  # noqa: E501

        :param git_branch: The git_branch of this AnsibleActivityMetadata.  # noqa: E501
        :type: str
        """

        self._git_branch = git_branch

    @property
    def git_commit_message(self):
        """Gets the git_commit_message of this AnsibleActivityMetadata.  # noqa: E501

        Git commit message associated with this execution  # noqa: E501

        :return: The git_commit_message of this AnsibleActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._git_commit_message

    @git_commit_message.setter
    def git_commit_message(self, git_commit_message):
        """Sets the git_commit_message of this AnsibleActivityMetadata.

        Git commit message associated with this execution  # noqa: E501

        :param git_commit_message: The git_commit_message of this AnsibleActivityMetadata.  # noqa: E501
        :type: str
        """

        self._git_commit_message = git_commit_message

    @property
    def git_commit_sha(self):
        """Gets the git_commit_sha of this AnsibleActivityMetadata.  # noqa: E501

        Git commit SHA associated with this execution  # noqa: E501

        :return: The git_commit_sha of this AnsibleActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._git_commit_sha

    @git_commit_sha.setter
    def git_commit_sha(self, git_commit_sha):
        """Sets the git_commit_sha of this AnsibleActivityMetadata.

        Git commit SHA associated with this execution  # noqa: E501

        :param git_commit_sha: The git_commit_sha of this AnsibleActivityMetadata.  # noqa: E501
        :type: str
        """

        self._git_commit_sha = git_commit_sha

    @property
    def git_repo(self):
        """Gets the git_repo of this AnsibleActivityMetadata.  # noqa: E501

        Git repo associated with this execution  # noqa: E501

        :return: The git_repo of this AnsibleActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._git_repo

    @git_repo.setter
    def git_repo(self, git_repo):
        """Sets the git_repo of this AnsibleActivityMetadata.

        Git repo associated with this execution  # noqa: E501

        :param git_repo: The git_repo of this AnsibleActivityMetadata.  # noqa: E501
        :type: str
        """

        self._git_repo = git_repo

    @property
    def pipeline(self):
        """Gets the pipeline of this AnsibleActivityMetadata.  # noqa: E501

        The unique identifier of any associated pipeline  # noqa: E501

        :return: The pipeline of this AnsibleActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._pipeline

    @pipeline.setter
    def pipeline(self, pipeline):
        """Sets the pipeline of this AnsibleActivityMetadata.

        The unique identifier of any associated pipeline  # noqa: E501

        :param pipeline: The pipeline of this AnsibleActivityMetadata.  # noqa: E501
        :type: str
        """

        self._pipeline = pipeline

    @property
    def pipeline_execution_id(self):
        """Gets the pipeline_execution_id of this AnsibleActivityMetadata.  # noqa: E501

        The unique identifier for any associated pipeline execution  # noqa: E501

        :return: The pipeline_execution_id of this AnsibleActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_execution_id

    @pipeline_execution_id.setter
    def pipeline_execution_id(self, pipeline_execution_id):
        """Sets the pipeline_execution_id of this AnsibleActivityMetadata.

        The unique identifier for any associated pipeline execution  # noqa: E501

        :param pipeline_execution_id: The pipeline_execution_id of this AnsibleActivityMetadata.  # noqa: E501
        :type: str
        """

        self._pipeline_execution_id = pipeline_execution_id

    @property
    def pipeline_execution_number(self):
        """Gets the pipeline_execution_number of this AnsibleActivityMetadata.  # noqa: E501

        The unique number for any associated pipeline execution  # noqa: E501

        :return: The pipeline_execution_number of this AnsibleActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_execution_number

    @pipeline_execution_number.setter
    def pipeline_execution_number(self, pipeline_execution_number):
        """Sets the pipeline_execution_number of this AnsibleActivityMetadata.

        The unique number for any associated pipeline execution  # noqa: E501

        :param pipeline_execution_number: The pipeline_execution_number of this AnsibleActivityMetadata.  # noqa: E501
        :type: str
        """

        self._pipeline_execution_number = pipeline_execution_number

    @property
    def pipeline_name(self):
        """Gets the pipeline_name of this AnsibleActivityMetadata.  # noqa: E501

        The name of any associated pipeline  # noqa: E501

        :return: The pipeline_name of this AnsibleActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_name

    @pipeline_name.setter
    def pipeline_name(self, pipeline_name):
        """Sets the pipeline_name of this AnsibleActivityMetadata.

        The name of any associated pipeline  # noqa: E501

        :param pipeline_name: The pipeline_name of this AnsibleActivityMetadata.  # noqa: E501
        :type: str
        """

        self._pipeline_name = pipeline_name

    @property
    def pipeline_stage_id(self):
        """Gets the pipeline_stage_id of this AnsibleActivityMetadata.  # noqa: E501

        The unique identifier for the associated pipeline stage  # noqa: E501

        :return: The pipeline_stage_id of this AnsibleActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_stage_id

    @pipeline_stage_id.setter
    def pipeline_stage_id(self, pipeline_stage_id):
        """Sets the pipeline_stage_id of this AnsibleActivityMetadata.

        The unique identifier for the associated pipeline stage  # noqa: E501

        :param pipeline_stage_id: The pipeline_stage_id of this AnsibleActivityMetadata.  # noqa: E501
        :type: str
        """

        self._pipeline_stage_id = pipeline_stage_id

    @property
    def results_uuid(self):
        """Gets the results_uuid of this AnsibleActivityMetadata.  # noqa: E501

        The ID of any associated results  # noqa: E501

        :return: The results_uuid of this AnsibleActivityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._results_uuid

    @results_uuid.setter
    def results_uuid(self, results_uuid):
        """Sets the results_uuid of this AnsibleActivityMetadata.

        The ID of any associated results  # noqa: E501

        :param results_uuid: The results_uuid of this AnsibleActivityMetadata.  # noqa: E501
        :type: str
        """

        self._results_uuid = results_uuid

    @property
    def trigger(self):
        """Gets the trigger of this AnsibleActivityMetadata.  # noqa: E501

        Trigger info for any associated pipeline execution  # noqa: E501

        :return: The trigger of this AnsibleActivityMetadata.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._trigger

    @trigger.setter
    def trigger(self, trigger):
        """Sets the trigger of this AnsibleActivityMetadata.

        Trigger info for any associated pipeline execution  # noqa: E501

        :param trigger: The trigger of this AnsibleActivityMetadata.  # noqa: E501
        :type: dict(str, object)
        """

        self._trigger = trigger

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
        if issubclass(AnsibleActivityMetadata, dict):
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
        if not isinstance(other, AnsibleActivityMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
