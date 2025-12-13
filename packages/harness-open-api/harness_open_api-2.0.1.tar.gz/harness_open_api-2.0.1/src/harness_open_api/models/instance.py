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

class Instance(object):
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
        'applied_revision': 'int',
        'backend': 'str',
        'created_at': 'str',
        'current_state': 'State',
        'id': 'str',
        'infrastructure_id': 'str',
        'message': 'str',
        'outputs': 'dict(str, str)',
        'progress': 'InstanceProgress',
        'step': 'InstanceStep',
        'target_revision': 'int',
        'target_state': 'State',
        'updated_at': 'str',
        'url': 'str'
    }

    attribute_map = {
        'applied_revision': 'appliedRevision',
        'backend': 'backend',
        'created_at': 'createdAt',
        'current_state': 'currentState',
        'id': 'id',
        'infrastructure_id': 'infrastructureId',
        'message': 'message',
        'outputs': 'outputs',
        'progress': 'progress',
        'step': 'step',
        'target_revision': 'targetRevision',
        'target_state': 'targetState',
        'updated_at': 'updatedAt',
        'url': 'url'
    }

    def __init__(self, applied_revision=None, backend=None, created_at=None, current_state=None, id=None, infrastructure_id=None, message=None, outputs=None, progress=None, step=None, target_revision=None, target_state=None, updated_at=None, url=None):  # noqa: E501
        """Instance - a model defined in Swagger"""  # noqa: E501
        self._applied_revision = None
        self._backend = None
        self._created_at = None
        self._current_state = None
        self._id = None
        self._infrastructure_id = None
        self._message = None
        self._outputs = None
        self._progress = None
        self._step = None
        self._target_revision = None
        self._target_state = None
        self._updated_at = None
        self._url = None
        self.discriminator = None
        if applied_revision is not None:
            self.applied_revision = applied_revision
        if backend is not None:
            self.backend = backend
        if created_at is not None:
            self.created_at = created_at
        if current_state is not None:
            self.current_state = current_state
        if id is not None:
            self.id = id
        if infrastructure_id is not None:
            self.infrastructure_id = infrastructure_id
        if message is not None:
            self.message = message
        if outputs is not None:
            self.outputs = outputs
        if progress is not None:
            self.progress = progress
        if step is not None:
            self.step = step
        if target_revision is not None:
            self.target_revision = target_revision
        if target_state is not None:
            self.target_state = target_state
        if updated_at is not None:
            self.updated_at = updated_at
        if url is not None:
            self.url = url

    @property
    def applied_revision(self):
        """Gets the applied_revision of this Instance.  # noqa: E501

        Revision of the instance that is currently active  # noqa: E501

        :return: The applied_revision of this Instance.  # noqa: E501
        :rtype: int
        """
        return self._applied_revision

    @applied_revision.setter
    def applied_revision(self, applied_revision):
        """Sets the applied_revision of this Instance.

        Revision of the instance that is currently active  # noqa: E501

        :param applied_revision: The applied_revision of this Instance.  # noqa: E501
        :type: int
        """

        self._applied_revision = applied_revision

    @property
    def backend(self):
        """Gets the backend of this Instance.  # noqa: E501


        :return: The backend of this Instance.  # noqa: E501
        :rtype: str
        """
        return self._backend

    @backend.setter
    def backend(self, backend):
        """Sets the backend of this Instance.


        :param backend: The backend of this Instance.  # noqa: E501
        :type: str
        """

        self._backend = backend

    @property
    def created_at(self):
        """Gets the created_at of this Instance.  # noqa: E501


        :return: The created_at of this Instance.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Instance.


        :param created_at: The created_at of this Instance.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def current_state(self):
        """Gets the current_state of this Instance.  # noqa: E501


        :return: The current_state of this Instance.  # noqa: E501
        :rtype: State
        """
        return self._current_state

    @current_state.setter
    def current_state(self, current_state):
        """Sets the current_state of this Instance.


        :param current_state: The current_state of this Instance.  # noqa: E501
        :type: State
        """

        self._current_state = current_state

    @property
    def id(self):
        """Gets the id of this Instance.  # noqa: E501


        :return: The id of this Instance.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Instance.


        :param id: The id of this Instance.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def infrastructure_id(self):
        """Gets the infrastructure_id of this Instance.  # noqa: E501


        :return: The infrastructure_id of this Instance.  # noqa: E501
        :rtype: str
        """
        return self._infrastructure_id

    @infrastructure_id.setter
    def infrastructure_id(self, infrastructure_id):
        """Sets the infrastructure_id of this Instance.


        :param infrastructure_id: The infrastructure_id of this Instance.  # noqa: E501
        :type: str
        """

        self._infrastructure_id = infrastructure_id

    @property
    def message(self):
        """Gets the message of this Instance.  # noqa: E501


        :return: The message of this Instance.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this Instance.


        :param message: The message of this Instance.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def outputs(self):
        """Gets the outputs of this Instance.  # noqa: E501


        :return: The outputs of this Instance.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        """Sets the outputs of this Instance.


        :param outputs: The outputs of this Instance.  # noqa: E501
        :type: dict(str, str)
        """

        self._outputs = outputs

    @property
    def progress(self):
        """Gets the progress of this Instance.  # noqa: E501


        :return: The progress of this Instance.  # noqa: E501
        :rtype: InstanceProgress
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """Sets the progress of this Instance.


        :param progress: The progress of this Instance.  # noqa: E501
        :type: InstanceProgress
        """

        self._progress = progress

    @property
    def step(self):
        """Gets the step of this Instance.  # noqa: E501


        :return: The step of this Instance.  # noqa: E501
        :rtype: InstanceStep
        """
        return self._step

    @step.setter
    def step(self, step):
        """Sets the step of this Instance.


        :param step: The step of this Instance.  # noqa: E501
        :type: InstanceStep
        """

        self._step = step

    @property
    def target_revision(self):
        """Gets the target_revision of this Instance.  # noqa: E501

        Target revision of the instance  # noqa: E501

        :return: The target_revision of this Instance.  # noqa: E501
        :rtype: int
        """
        return self._target_revision

    @target_revision.setter
    def target_revision(self, target_revision):
        """Sets the target_revision of this Instance.

        Target revision of the instance  # noqa: E501

        :param target_revision: The target_revision of this Instance.  # noqa: E501
        :type: int
        """

        self._target_revision = target_revision

    @property
    def target_state(self):
        """Gets the target_state of this Instance.  # noqa: E501


        :return: The target_state of this Instance.  # noqa: E501
        :rtype: State
        """
        return self._target_state

    @target_state.setter
    def target_state(self, target_state):
        """Sets the target_state of this Instance.


        :param target_state: The target_state of this Instance.  # noqa: E501
        :type: State
        """

        self._target_state = target_state

    @property
    def updated_at(self):
        """Gets the updated_at of this Instance.  # noqa: E501


        :return: The updated_at of this Instance.  # noqa: E501
        :rtype: str
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Instance.


        :param updated_at: The updated_at of this Instance.  # noqa: E501
        :type: str
        """

        self._updated_at = updated_at

    @property
    def url(self):
        """Gets the url of this Instance.  # noqa: E501


        :return: The url of this Instance.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this Instance.


        :param url: The url of this Instance.  # noqa: E501
        :type: str
        """

        self._url = url

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
        if issubclass(Instance, dict):
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
        if not isinstance(other, Instance):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
