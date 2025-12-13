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

class VariableSetsCreateVariableSetAccountLevelResponseBody(object):
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
        'account': 'str',
        'connectors': 'list[VariableSetConnector]',
        'created': 'int',
        'description': 'str',
        'environment_variables': 'dict(str, VariableSetVar)',
        'identifier': 'str',
        'name': 'str',
        'org': 'str',
        'project': 'str',
        'terraform_variable_files': 'list[VariableSetVarFile]',
        'terraform_variables': 'dict(str, VariableSetVar)',
        'updated': 'int'
    }

    attribute_map = {
        'account': 'account',
        'connectors': 'connectors',
        'created': 'created',
        'description': 'description',
        'environment_variables': 'environment_variables',
        'identifier': 'identifier',
        'name': 'name',
        'org': 'org',
        'project': 'project',
        'terraform_variable_files': 'terraform_variable_files',
        'terraform_variables': 'terraform_variables',
        'updated': 'updated'
    }

    def __init__(self, account=None, connectors=None, created=None, description=None, environment_variables=None, identifier=None, name=None, org=None, project=None, terraform_variable_files=None, terraform_variables=None, updated=None):  # noqa: E501
        """VariableSetsCreateVariableSetAccountLevelResponseBody - a model defined in Swagger"""  # noqa: E501
        self._account = None
        self._connectors = None
        self._created = None
        self._description = None
        self._environment_variables = None
        self._identifier = None
        self._name = None
        self._org = None
        self._project = None
        self._terraform_variable_files = None
        self._terraform_variables = None
        self._updated = None
        self.discriminator = None
        self.account = account
        if connectors is not None:
            self.connectors = connectors
        if created is not None:
            self.created = created
        if description is not None:
            self.description = description
        if environment_variables is not None:
            self.environment_variables = environment_variables
        self.identifier = identifier
        self.name = name
        self.org = org
        self.project = project
        if terraform_variable_files is not None:
            self.terraform_variable_files = terraform_variable_files
        if terraform_variables is not None:
            self.terraform_variables = terraform_variables
        if updated is not None:
            self.updated = updated

    @property
    def account(self):
        """Gets the account of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501

        Account is the internal customer account ID.  # noqa: E501

        :return: The account of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this VariableSetsCreateVariableSetAccountLevelResponseBody.

        Account is the internal customer account ID.  # noqa: E501

        :param account: The account of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :type: str
        """
        if account is None:
            raise ValueError("Invalid value for `account`, must not be `None`")  # noqa: E501

        self._account = account

    @property
    def connectors(self):
        """Gets the connectors of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501

        define an array of connectors that belong to Variable Set  # noqa: E501

        :return: The connectors of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :rtype: list[VariableSetConnector]
        """
        return self._connectors

    @connectors.setter
    def connectors(self, connectors):
        """Sets the connectors of this VariableSetsCreateVariableSetAccountLevelResponseBody.

        define an array of connectors that belong to Variable Set  # noqa: E501

        :param connectors: The connectors of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :type: list[VariableSetConnector]
        """

        self._connectors = connectors

    @property
    def created(self):
        """Gets the created of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501

        Timestamp when the variable set was created.  # noqa: E501

        :return: The created of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this VariableSetsCreateVariableSetAccountLevelResponseBody.

        Timestamp when the variable set was created.  # noqa: E501

        :param created: The created of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :type: int
        """

        self._created = created

    @property
    def description(self):
        """Gets the description of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501

        Description provides long-form text about the resource.  # noqa: E501

        :return: The description of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this VariableSetsCreateVariableSetAccountLevelResponseBody.

        Description provides long-form text about the resource.  # noqa: E501

        :param description: The description of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def environment_variables(self):
        """Gets the environment_variables of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501

        map of environment variables configured on the Variable Set.  # noqa: E501

        :return: The environment_variables of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :rtype: dict(str, VariableSetVar)
        """
        return self._environment_variables

    @environment_variables.setter
    def environment_variables(self, environment_variables):
        """Sets the environment_variables of this VariableSetsCreateVariableSetAccountLevelResponseBody.

        map of environment variables configured on the Variable Set.  # noqa: E501

        :param environment_variables: The environment_variables of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :type: dict(str, VariableSetVar)
        """

        self._environment_variables = environment_variables

    @property
    def identifier(self):
        """Gets the identifier of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501

        Identifier is the VariableSet identifier.  # noqa: E501

        :return: The identifier of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this VariableSetsCreateVariableSetAccountLevelResponseBody.

        Identifier is the VariableSet identifier.  # noqa: E501

        :param identifier: The identifier of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :type: str
        """
        if identifier is None:
            raise ValueError("Invalid value for `identifier`, must not be `None`")  # noqa: E501

        self._identifier = identifier

    @property
    def name(self):
        """Gets the name of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501

        Name is the human readable name for the resource.  # noqa: E501

        :return: The name of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this VariableSetsCreateVariableSetAccountLevelResponseBody.

        Name is the human readable name for the resource.  # noqa: E501

        :param name: The name of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def org(self):
        """Gets the org of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501

        Org is the organisation identifier.  # noqa: E501

        :return: The org of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :rtype: str
        """
        return self._org

    @org.setter
    def org(self, org):
        """Sets the org of this VariableSetsCreateVariableSetAccountLevelResponseBody.

        Org is the organisation identifier.  # noqa: E501

        :param org: The org of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :type: str
        """
        if org is None:
            raise ValueError("Invalid value for `org`, must not be `None`")  # noqa: E501

        self._org = org

    @property
    def project(self):
        """Gets the project of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501

        Project is the project identifier.  # noqa: E501

        :return: The project of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this VariableSetsCreateVariableSetAccountLevelResponseBody.

        Project is the project identifier.  # noqa: E501

        :param project: The project of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :type: str
        """
        if project is None:
            raise ValueError("Invalid value for `project`, must not be `None`")  # noqa: E501

        self._project = project

    @property
    def terraform_variable_files(self):
        """Gets the terraform_variable_files of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501

        define an array of terraform variables files that belong to a different repository  # noqa: E501

        :return: The terraform_variable_files of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :rtype: list[VariableSetVarFile]
        """
        return self._terraform_variable_files

    @terraform_variable_files.setter
    def terraform_variable_files(self, terraform_variable_files):
        """Sets the terraform_variable_files of this VariableSetsCreateVariableSetAccountLevelResponseBody.

        define an array of terraform variables files that belong to a different repository  # noqa: E501

        :param terraform_variable_files: The terraform_variable_files of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :type: list[VariableSetVarFile]
        """

        self._terraform_variable_files = terraform_variable_files

    @property
    def terraform_variables(self):
        """Gets the terraform_variables of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501

        map of terraform variables configured on the Variable Set.  # noqa: E501

        :return: The terraform_variables of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :rtype: dict(str, VariableSetVar)
        """
        return self._terraform_variables

    @terraform_variables.setter
    def terraform_variables(self, terraform_variables):
        """Sets the terraform_variables of this VariableSetsCreateVariableSetAccountLevelResponseBody.

        map of terraform variables configured on the Variable Set.  # noqa: E501

        :param terraform_variables: The terraform_variables of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :type: dict(str, VariableSetVar)
        """

        self._terraform_variables = terraform_variables

    @property
    def updated(self):
        """Gets the updated of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501

        Timestamp when the variable set was last updated.  # noqa: E501

        :return: The updated of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
        :rtype: int
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this VariableSetsCreateVariableSetAccountLevelResponseBody.

        Timestamp when the variable set was last updated.  # noqa: E501

        :param updated: The updated of this VariableSetsCreateVariableSetAccountLevelResponseBody.  # noqa: E501
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
        if issubclass(VariableSetsCreateVariableSetAccountLevelResponseBody, dict):
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
        if not isinstance(other, VariableSetsCreateVariableSetAccountLevelResponseBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
