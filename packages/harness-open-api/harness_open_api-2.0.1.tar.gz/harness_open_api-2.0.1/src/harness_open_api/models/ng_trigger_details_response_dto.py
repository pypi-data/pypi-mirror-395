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

class NGTriggerDetailsResponseDTO(object):
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
        'build_details': 'BuildDetails',
        'description': 'str',
        'enabled': 'bool',
        'executions': 'list[int]',
        'identifier': 'str',
        'is_pipeline_input_outdated': 'bool',
        'last_trigger_execution_details': 'LastTriggerExecutionDetails',
        'name': 'str',
        'pipeline_input_outdated': 'bool',
        'registration_status': 'str',
        'tags': 'dict(str, str)',
        'trigger_status': 'TriggerStatus',
        'type': 'str',
        'webhook_curl_command': 'str',
        'webhook_details': 'WebhookDetails',
        'webhook_url': 'str',
        'yaml': 'str',
        'yaml_version': 'str'
    }

    attribute_map = {
        'build_details': 'buildDetails',
        'description': 'description',
        'enabled': 'enabled',
        'executions': 'executions',
        'identifier': 'identifier',
        'is_pipeline_input_outdated': 'isPipelineInputOutdated',
        'last_trigger_execution_details': 'lastTriggerExecutionDetails',
        'name': 'name',
        'pipeline_input_outdated': 'pipelineInputOutdated',
        'registration_status': 'registrationStatus',
        'tags': 'tags',
        'trigger_status': 'triggerStatus',
        'type': 'type',
        'webhook_curl_command': 'webhookCurlCommand',
        'webhook_details': 'webhookDetails',
        'webhook_url': 'webhookUrl',
        'yaml': 'yaml',
        'yaml_version': 'yamlVersion'
    }

    def __init__(self, build_details=None, description=None, enabled=None, executions=None, identifier=None, is_pipeline_input_outdated=None, last_trigger_execution_details=None, name=None, pipeline_input_outdated=None, registration_status=None, tags=None, trigger_status=None, type=None, webhook_curl_command=None, webhook_details=None, webhook_url=None, yaml=None, yaml_version=None):  # noqa: E501
        """NGTriggerDetailsResponseDTO - a model defined in Swagger"""  # noqa: E501
        self._build_details = None
        self._description = None
        self._enabled = None
        self._executions = None
        self._identifier = None
        self._is_pipeline_input_outdated = None
        self._last_trigger_execution_details = None
        self._name = None
        self._pipeline_input_outdated = None
        self._registration_status = None
        self._tags = None
        self._trigger_status = None
        self._type = None
        self._webhook_curl_command = None
        self._webhook_details = None
        self._webhook_url = None
        self._yaml = None
        self._yaml_version = None
        self.discriminator = None
        if build_details is not None:
            self.build_details = build_details
        if description is not None:
            self.description = description
        if enabled is not None:
            self.enabled = enabled
        if executions is not None:
            self.executions = executions
        if identifier is not None:
            self.identifier = identifier
        if is_pipeline_input_outdated is not None:
            self.is_pipeline_input_outdated = is_pipeline_input_outdated
        if last_trigger_execution_details is not None:
            self.last_trigger_execution_details = last_trigger_execution_details
        if name is not None:
            self.name = name
        if pipeline_input_outdated is not None:
            self.pipeline_input_outdated = pipeline_input_outdated
        if registration_status is not None:
            self.registration_status = registration_status
        if tags is not None:
            self.tags = tags
        if trigger_status is not None:
            self.trigger_status = trigger_status
        if type is not None:
            self.type = type
        if webhook_curl_command is not None:
            self.webhook_curl_command = webhook_curl_command
        if webhook_details is not None:
            self.webhook_details = webhook_details
        if webhook_url is not None:
            self.webhook_url = webhook_url
        if yaml is not None:
            self.yaml = yaml
        if yaml_version is not None:
            self.yaml_version = yaml_version

    @property
    def build_details(self):
        """Gets the build_details of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The build_details of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: BuildDetails
        """
        return self._build_details

    @build_details.setter
    def build_details(self, build_details):
        """Sets the build_details of this NGTriggerDetailsResponseDTO.


        :param build_details: The build_details of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: BuildDetails
        """

        self._build_details = build_details

    @property
    def description(self):
        """Gets the description of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The description of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this NGTriggerDetailsResponseDTO.


        :param description: The description of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def enabled(self):
        """Gets the enabled of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The enabled of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this NGTriggerDetailsResponseDTO.


        :param enabled: The enabled of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def executions(self):
        """Gets the executions of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The executions of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: list[int]
        """
        return self._executions

    @executions.setter
    def executions(self, executions):
        """Sets the executions of this NGTriggerDetailsResponseDTO.


        :param executions: The executions of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: list[int]
        """

        self._executions = executions

    @property
    def identifier(self):
        """Gets the identifier of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The identifier of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this NGTriggerDetailsResponseDTO.


        :param identifier: The identifier of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: str
        """

        self._identifier = identifier

    @property
    def is_pipeline_input_outdated(self):
        """Gets the is_pipeline_input_outdated of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The is_pipeline_input_outdated of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: bool
        """
        return self._is_pipeline_input_outdated

    @is_pipeline_input_outdated.setter
    def is_pipeline_input_outdated(self, is_pipeline_input_outdated):
        """Sets the is_pipeline_input_outdated of this NGTriggerDetailsResponseDTO.


        :param is_pipeline_input_outdated: The is_pipeline_input_outdated of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: bool
        """

        self._is_pipeline_input_outdated = is_pipeline_input_outdated

    @property
    def last_trigger_execution_details(self):
        """Gets the last_trigger_execution_details of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The last_trigger_execution_details of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: LastTriggerExecutionDetails
        """
        return self._last_trigger_execution_details

    @last_trigger_execution_details.setter
    def last_trigger_execution_details(self, last_trigger_execution_details):
        """Sets the last_trigger_execution_details of this NGTriggerDetailsResponseDTO.


        :param last_trigger_execution_details: The last_trigger_execution_details of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: LastTriggerExecutionDetails
        """

        self._last_trigger_execution_details = last_trigger_execution_details

    @property
    def name(self):
        """Gets the name of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The name of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this NGTriggerDetailsResponseDTO.


        :param name: The name of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def pipeline_input_outdated(self):
        """Gets the pipeline_input_outdated of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The pipeline_input_outdated of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: bool
        """
        return self._pipeline_input_outdated

    @pipeline_input_outdated.setter
    def pipeline_input_outdated(self, pipeline_input_outdated):
        """Sets the pipeline_input_outdated of this NGTriggerDetailsResponseDTO.


        :param pipeline_input_outdated: The pipeline_input_outdated of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: bool
        """

        self._pipeline_input_outdated = pipeline_input_outdated

    @property
    def registration_status(self):
        """Gets the registration_status of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The registration_status of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._registration_status

    @registration_status.setter
    def registration_status(self, registration_status):
        """Sets the registration_status of this NGTriggerDetailsResponseDTO.


        :param registration_status: The registration_status of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: str
        """
        allowed_values = ["SUCCESS", "FAILED", "ERROR", "TIMEOUT", "UNAVAILABLE"]  # noqa: E501
        if registration_status not in allowed_values:
            raise ValueError(
                "Invalid value for `registration_status` ({0}), must be one of {1}"  # noqa: E501
                .format(registration_status, allowed_values)
            )

        self._registration_status = registration_status

    @property
    def tags(self):
        """Gets the tags of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The tags of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this NGTriggerDetailsResponseDTO.


        :param tags: The tags of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: dict(str, str)
        """

        self._tags = tags

    @property
    def trigger_status(self):
        """Gets the trigger_status of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The trigger_status of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: TriggerStatus
        """
        return self._trigger_status

    @trigger_status.setter
    def trigger_status(self, trigger_status):
        """Sets the trigger_status of this NGTriggerDetailsResponseDTO.


        :param trigger_status: The trigger_status of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: TriggerStatus
        """

        self._trigger_status = trigger_status

    @property
    def type(self):
        """Gets the type of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The type of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this NGTriggerDetailsResponseDTO.


        :param type: The type of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: str
        """
        allowed_values = ["Webhook", "Artifact", "Manifest", "Scheduled", "MultiRegionArtifact"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def webhook_curl_command(self):
        """Gets the webhook_curl_command of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The webhook_curl_command of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._webhook_curl_command

    @webhook_curl_command.setter
    def webhook_curl_command(self, webhook_curl_command):
        """Sets the webhook_curl_command of this NGTriggerDetailsResponseDTO.


        :param webhook_curl_command: The webhook_curl_command of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: str
        """

        self._webhook_curl_command = webhook_curl_command

    @property
    def webhook_details(self):
        """Gets the webhook_details of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The webhook_details of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: WebhookDetails
        """
        return self._webhook_details

    @webhook_details.setter
    def webhook_details(self, webhook_details):
        """Sets the webhook_details of this NGTriggerDetailsResponseDTO.


        :param webhook_details: The webhook_details of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: WebhookDetails
        """

        self._webhook_details = webhook_details

    @property
    def webhook_url(self):
        """Gets the webhook_url of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The webhook_url of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._webhook_url

    @webhook_url.setter
    def webhook_url(self, webhook_url):
        """Sets the webhook_url of this NGTriggerDetailsResponseDTO.


        :param webhook_url: The webhook_url of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: str
        """

        self._webhook_url = webhook_url

    @property
    def yaml(self):
        """Gets the yaml of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The yaml of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._yaml

    @yaml.setter
    def yaml(self, yaml):
        """Sets the yaml of this NGTriggerDetailsResponseDTO.


        :param yaml: The yaml of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: str
        """

        self._yaml = yaml

    @property
    def yaml_version(self):
        """Gets the yaml_version of this NGTriggerDetailsResponseDTO.  # noqa: E501


        :return: The yaml_version of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._yaml_version

    @yaml_version.setter
    def yaml_version(self, yaml_version):
        """Sets the yaml_version of this NGTriggerDetailsResponseDTO.


        :param yaml_version: The yaml_version of this NGTriggerDetailsResponseDTO.  # noqa: E501
        :type: str
        """

        self._yaml_version = yaml_version

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
        if issubclass(NGTriggerDetailsResponseDTO, dict):
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
        if not isinstance(other, NGTriggerDetailsResponseDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
