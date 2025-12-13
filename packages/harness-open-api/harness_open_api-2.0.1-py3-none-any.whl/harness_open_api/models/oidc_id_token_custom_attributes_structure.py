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

class OidcIdTokenCustomAttributesStructure(object):
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
        'account_id': 'str',
        'connector_id': 'str',
        'connector_name': 'str',
        'context': 'str',
        'environment_id': 'str',
        'environment_type': 'str',
        'organization_id': 'str',
        'pipeline_id': 'str',
        'project_id': 'str',
        'service_id': 'str',
        'service_name': 'str',
        'stage_type': 'str',
        'step_type': 'str',
        'trigger_by_email': 'str',
        'triggered_by_name': 'str'
    }

    attribute_map = {
        'account_id': 'account_id',
        'connector_id': 'connector_id',
        'connector_name': 'connector_name',
        'context': 'context',
        'environment_id': 'environment_id',
        'environment_type': 'environment_type',
        'organization_id': 'organization_id',
        'pipeline_id': 'pipeline_id',
        'project_id': 'project_id',
        'service_id': 'service_id',
        'service_name': 'service_name',
        'stage_type': 'stage_type',
        'step_type': 'step_type',
        'trigger_by_email': 'trigger_by_email',
        'triggered_by_name': 'triggered_by_name'
    }

    def __init__(self, account_id=None, connector_id=None, connector_name=None, context=None, environment_id=None, environment_type=None, organization_id=None, pipeline_id=None, project_id=None, service_id=None, service_name=None, stage_type=None, step_type=None, trigger_by_email=None, triggered_by_name=None):  # noqa: E501
        """OidcIdTokenCustomAttributesStructure - a model defined in Swagger"""  # noqa: E501
        self._account_id = None
        self._connector_id = None
        self._connector_name = None
        self._context = None
        self._environment_id = None
        self._environment_type = None
        self._organization_id = None
        self._pipeline_id = None
        self._project_id = None
        self._service_id = None
        self._service_name = None
        self._stage_type = None
        self._step_type = None
        self._trigger_by_email = None
        self._triggered_by_name = None
        self.discriminator = None
        self.account_id = account_id
        if connector_id is not None:
            self.connector_id = connector_id
        if connector_name is not None:
            self.connector_name = connector_name
        if context is not None:
            self.context = context
        if environment_id is not None:
            self.environment_id = environment_id
        if environment_type is not None:
            self.environment_type = environment_type
        if organization_id is not None:
            self.organization_id = organization_id
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if project_id is not None:
            self.project_id = project_id
        if service_id is not None:
            self.service_id = service_id
        if service_name is not None:
            self.service_name = service_name
        if stage_type is not None:
            self.stage_type = stage_type
        if step_type is not None:
            self.step_type = step_type
        if trigger_by_email is not None:
            self.trigger_by_email = trigger_by_email
        if triggered_by_name is not None:
            self.triggered_by_name = triggered_by_name

    @property
    def account_id(self):
        """Gets the account_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The account_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this OidcIdTokenCustomAttributesStructure.


        :param account_id: The account_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """
        if account_id is None:
            raise ValueError("Invalid value for `account_id`, must not be `None`")  # noqa: E501

        self._account_id = account_id

    @property
    def connector_id(self):
        """Gets the connector_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The connector_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._connector_id

    @connector_id.setter
    def connector_id(self, connector_id):
        """Sets the connector_id of this OidcIdTokenCustomAttributesStructure.


        :param connector_id: The connector_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._connector_id = connector_id

    @property
    def connector_name(self):
        """Gets the connector_name of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The connector_name of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._connector_name

    @connector_name.setter
    def connector_name(self, connector_name):
        """Sets the connector_name of this OidcIdTokenCustomAttributesStructure.


        :param connector_name: The connector_name of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._connector_name = connector_name

    @property
    def context(self):
        """Gets the context of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The context of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context):
        """Sets the context of this OidcIdTokenCustomAttributesStructure.


        :param context: The context of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._context = context

    @property
    def environment_id(self):
        """Gets the environment_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The environment_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._environment_id

    @environment_id.setter
    def environment_id(self, environment_id):
        """Sets the environment_id of this OidcIdTokenCustomAttributesStructure.


        :param environment_id: The environment_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._environment_id = environment_id

    @property
    def environment_type(self):
        """Gets the environment_type of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The environment_type of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._environment_type

    @environment_type.setter
    def environment_type(self, environment_type):
        """Sets the environment_type of this OidcIdTokenCustomAttributesStructure.


        :param environment_type: The environment_type of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._environment_type = environment_type

    @property
    def organization_id(self):
        """Gets the organization_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The organization_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this OidcIdTokenCustomAttributesStructure.


        :param organization_id: The organization_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._organization_id = organization_id

    @property
    def pipeline_id(self):
        """Gets the pipeline_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The pipeline_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_id

    @pipeline_id.setter
    def pipeline_id(self, pipeline_id):
        """Sets the pipeline_id of this OidcIdTokenCustomAttributesStructure.


        :param pipeline_id: The pipeline_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._pipeline_id = pipeline_id

    @property
    def project_id(self):
        """Gets the project_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The project_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this OidcIdTokenCustomAttributesStructure.


        :param project_id: The project_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def service_id(self):
        """Gets the service_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The service_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._service_id

    @service_id.setter
    def service_id(self, service_id):
        """Sets the service_id of this OidcIdTokenCustomAttributesStructure.


        :param service_id: The service_id of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._service_id = service_id

    @property
    def service_name(self):
        """Gets the service_name of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The service_name of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        """Sets the service_name of this OidcIdTokenCustomAttributesStructure.


        :param service_name: The service_name of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._service_name = service_name

    @property
    def stage_type(self):
        """Gets the stage_type of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The stage_type of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._stage_type

    @stage_type.setter
    def stage_type(self, stage_type):
        """Sets the stage_type of this OidcIdTokenCustomAttributesStructure.


        :param stage_type: The stage_type of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._stage_type = stage_type

    @property
    def step_type(self):
        """Gets the step_type of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The step_type of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._step_type

    @step_type.setter
    def step_type(self, step_type):
        """Sets the step_type of this OidcIdTokenCustomAttributesStructure.


        :param step_type: The step_type of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._step_type = step_type

    @property
    def trigger_by_email(self):
        """Gets the trigger_by_email of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The trigger_by_email of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._trigger_by_email

    @trigger_by_email.setter
    def trigger_by_email(self, trigger_by_email):
        """Sets the trigger_by_email of this OidcIdTokenCustomAttributesStructure.


        :param trigger_by_email: The trigger_by_email of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._trigger_by_email = trigger_by_email

    @property
    def triggered_by_name(self):
        """Gets the triggered_by_name of this OidcIdTokenCustomAttributesStructure.  # noqa: E501


        :return: The triggered_by_name of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :rtype: str
        """
        return self._triggered_by_name

    @triggered_by_name.setter
    def triggered_by_name(self, triggered_by_name):
        """Sets the triggered_by_name of this OidcIdTokenCustomAttributesStructure.


        :param triggered_by_name: The triggered_by_name of this OidcIdTokenCustomAttributesStructure.  # noqa: E501
        :type: str
        """

        self._triggered_by_name = triggered_by_name

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
        if issubclass(OidcIdTokenCustomAttributesStructure, dict):
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
        if not isinstance(other, OidcIdTokenCustomAttributesStructure):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
