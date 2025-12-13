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

class HarnessIacmWorkspaceCreateresult(object):
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
        'associated_template': 'AssociatedTemplate',
        'backend_locked': 'bool',
        'budget': 'float',
        'cost_breakdown_json': 'str',
        'cost_diff_json': 'str',
        'cost_estimation_enabled': 'bool',
        'created': 'int',
        'default_pipelines': 'dict(str, DefaultPipelineOverride)',
        'description': 'str',
        'environment_variables': 'dict(str, VariableResource)',
        'id': 'int',
        'identifier': 'str',
        'modules_json': 'str',
        'name': 'str',
        'org': 'str',
        'policy_evaluation': 'IaCMEvaluation',
        'project': 'str',
        'provider_connector': 'str',
        'provider_connectors': 'list[WorkspaceProviderConnector]',
        'providers_json': 'str',
        'provisioner': 'str',
        'provisioner_data': 'str',
        'provisioner_version': 'str',
        'prune_sensitive_data': 'bool',
        'repository': 'str',
        'repository_branch': 'str',
        'repository_commit': 'str',
        'repository_connector': 'str',
        'repository_path': 'str',
        'repository_sha': 'str',
        'repository_submodules': 'str',
        'run_all': 'bool',
        'sparse_checkout': 'str',
        'state_checksum': 'str',
        'status': 'str',
        'tags': 'str',
        'terraform_plan_json': 'str',
        'terraform_state': 'str',
        'terraform_state_json': 'str',
        'terraform_variable_files': 'list[WorkspaceTerraformVariableFiles]',
        'terraform_variables': 'dict(str, VariableResource)',
        'terragrunt_provider': 'bool',
        'terragrunt_version': 'str',
        'updated': 'int',
        'variable_sets': 'list[str]'
    }

    attribute_map = {
        'account': 'account',
        'associated_template': 'associated_template',
        'backend_locked': 'backend_locked',
        'budget': 'budget',
        'cost_breakdown_json': 'cost_breakdown_json',
        'cost_diff_json': 'cost_diff_json',
        'cost_estimation_enabled': 'cost_estimation_enabled',
        'created': 'created',
        'default_pipelines': 'default_pipelines',
        'description': 'description',
        'environment_variables': 'environment_variables',
        'id': 'id',
        'identifier': 'identifier',
        'modules_json': 'modules_json',
        'name': 'name',
        'org': 'org',
        'policy_evaluation': 'policy_evaluation',
        'project': 'project',
        'provider_connector': 'provider_connector',
        'provider_connectors': 'provider_connectors',
        'providers_json': 'providers_json',
        'provisioner': 'provisioner',
        'provisioner_data': 'provisioner_data',
        'provisioner_version': 'provisioner_version',
        'prune_sensitive_data': 'prune_sensitive_data',
        'repository': 'repository',
        'repository_branch': 'repository_branch',
        'repository_commit': 'repository_commit',
        'repository_connector': 'repository_connector',
        'repository_path': 'repository_path',
        'repository_sha': 'repository_sha',
        'repository_submodules': 'repository_submodules',
        'run_all': 'run_all',
        'sparse_checkout': 'sparse_checkout',
        'state_checksum': 'state_checksum',
        'status': 'status',
        'tags': 'tags',
        'terraform_plan_json': 'terraform_plan_json',
        'terraform_state': 'terraform_state',
        'terraform_state_json': 'terraform_state_json',
        'terraform_variable_files': 'terraform_variable_files',
        'terraform_variables': 'terraform_variables',
        'terragrunt_provider': 'terragrunt_provider',
        'terragrunt_version': 'terragrunt_version',
        'updated': 'updated',
        'variable_sets': 'variable_sets'
    }

    def __init__(self, account=None, associated_template=None, backend_locked=False, budget=None, cost_breakdown_json=None, cost_diff_json=None, cost_estimation_enabled=False, created=None, default_pipelines=None, description=None, environment_variables=None, id=None, identifier=None, modules_json=None, name=None, org=None, policy_evaluation=None, project=None, provider_connector=None, provider_connectors=None, providers_json=None, provisioner=None, provisioner_data=None, provisioner_version='latest', prune_sensitive_data=False, repository=None, repository_branch=None, repository_commit=None, repository_connector=None, repository_path='', repository_sha=None, repository_submodules='false', run_all=None, sparse_checkout=None, state_checksum=None, status=None, tags=None, terraform_plan_json=None, terraform_state=None, terraform_state_json=None, terraform_variable_files=None, terraform_variables=None, terragrunt_provider=False, terragrunt_version=None, updated=None, variable_sets=None):  # noqa: E501
        """HarnessIacmWorkspaceCreateresult - a model defined in Swagger"""  # noqa: E501
        self._account = None
        self._associated_template = None
        self._backend_locked = None
        self._budget = None
        self._cost_breakdown_json = None
        self._cost_diff_json = None
        self._cost_estimation_enabled = None
        self._created = None
        self._default_pipelines = None
        self._description = None
        self._environment_variables = None
        self._id = None
        self._identifier = None
        self._modules_json = None
        self._name = None
        self._org = None
        self._policy_evaluation = None
        self._project = None
        self._provider_connector = None
        self._provider_connectors = None
        self._providers_json = None
        self._provisioner = None
        self._provisioner_data = None
        self._provisioner_version = None
        self._prune_sensitive_data = None
        self._repository = None
        self._repository_branch = None
        self._repository_commit = None
        self._repository_connector = None
        self._repository_path = None
        self._repository_sha = None
        self._repository_submodules = None
        self._run_all = None
        self._sparse_checkout = None
        self._state_checksum = None
        self._status = None
        self._tags = None
        self._terraform_plan_json = None
        self._terraform_state = None
        self._terraform_state_json = None
        self._terraform_variable_files = None
        self._terraform_variables = None
        self._terragrunt_provider = None
        self._terragrunt_version = None
        self._updated = None
        self._variable_sets = None
        self.discriminator = None
        self.account = account
        if associated_template is not None:
            self.associated_template = associated_template
        if backend_locked is not None:
            self.backend_locked = backend_locked
        if budget is not None:
            self.budget = budget
        if cost_breakdown_json is not None:
            self.cost_breakdown_json = cost_breakdown_json
        if cost_diff_json is not None:
            self.cost_diff_json = cost_diff_json
        if cost_estimation_enabled is not None:
            self.cost_estimation_enabled = cost_estimation_enabled
        self.created = created
        if default_pipelines is not None:
            self.default_pipelines = default_pipelines
        if description is not None:
            self.description = description
        self.environment_variables = environment_variables
        if id is not None:
            self.id = id
        self.identifier = identifier
        if modules_json is not None:
            self.modules_json = modules_json
        self.name = name
        self.org = org
        if policy_evaluation is not None:
            self.policy_evaluation = policy_evaluation
        self.project = project
        self.provider_connector = provider_connector
        if provider_connectors is not None:
            self.provider_connectors = provider_connectors
        if providers_json is not None:
            self.providers_json = providers_json
        self.provisioner = provisioner
        self.provisioner_data = provisioner_data
        if provisioner_version is not None:
            self.provisioner_version = provisioner_version
        if prune_sensitive_data is not None:
            self.prune_sensitive_data = prune_sensitive_data
        if repository is not None:
            self.repository = repository
        if repository_branch is not None:
            self.repository_branch = repository_branch
        if repository_commit is not None:
            self.repository_commit = repository_commit
        self.repository_connector = repository_connector
        if repository_path is not None:
            self.repository_path = repository_path
        if repository_sha is not None:
            self.repository_sha = repository_sha
        if repository_submodules is not None:
            self.repository_submodules = repository_submodules
        if run_all is not None:
            self.run_all = run_all
        if sparse_checkout is not None:
            self.sparse_checkout = sparse_checkout
        if state_checksum is not None:
            self.state_checksum = state_checksum
        self.status = status
        self.tags = tags
        if terraform_plan_json is not None:
            self.terraform_plan_json = terraform_plan_json
        if terraform_state is not None:
            self.terraform_state = terraform_state
        if terraform_state_json is not None:
            self.terraform_state_json = terraform_state_json
        if terraform_variable_files is not None:
            self.terraform_variable_files = terraform_variable_files
        self.terraform_variables = terraform_variables
        if terragrunt_provider is not None:
            self.terragrunt_provider = terragrunt_provider
        if terragrunt_version is not None:
            self.terragrunt_version = terragrunt_version
        self.updated = updated
        if variable_sets is not None:
            self.variable_sets = variable_sets

    @property
    def account(self):
        """Gets the account of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Account is the internal customer account ID.  # noqa: E501

        :return: The account of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this HarnessIacmWorkspaceCreateresult.

        Account is the internal customer account ID.  # noqa: E501

        :param account: The account of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """
        if account is None:
            raise ValueError("Invalid value for `account`, must not be `None`")  # noqa: E501

        self._account = account

    @property
    def associated_template(self):
        """Gets the associated_template of this HarnessIacmWorkspaceCreateresult.  # noqa: E501


        :return: The associated_template of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: AssociatedTemplate
        """
        return self._associated_template

    @associated_template.setter
    def associated_template(self, associated_template):
        """Sets the associated_template of this HarnessIacmWorkspaceCreateresult.


        :param associated_template: The associated_template of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: AssociatedTemplate
        """

        self._associated_template = associated_template

    @property
    def backend_locked(self):
        """Gets the backend_locked of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Defines if the remote backend is locked or not  # noqa: E501

        :return: The backend_locked of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: bool
        """
        return self._backend_locked

    @backend_locked.setter
    def backend_locked(self, backend_locked):
        """Sets the backend_locked of this HarnessIacmWorkspaceCreateresult.

        Defines if the remote backend is locked or not  # noqa: E501

        :param backend_locked: The backend_locked of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: bool
        """

        self._backend_locked = backend_locked

    @property
    def budget(self):
        """Gets the budget of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        define the budget for a specific workspace  # noqa: E501

        :return: The budget of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: float
        """
        return self._budget

    @budget.setter
    def budget(self, budget):
        """Sets the budget of this HarnessIacmWorkspaceCreateresult.

        define the budget for a specific workspace  # noqa: E501

        :param budget: The budget of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: float
        """

        self._budget = budget

    @property
    def cost_breakdown_json(self):
        """Gets the cost_breakdown_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        cost_breakdown_json is the identifier to the breakdown cost file from the current execution that was applied successfully  # noqa: E501

        :return: The cost_breakdown_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._cost_breakdown_json

    @cost_breakdown_json.setter
    def cost_breakdown_json(self, cost_breakdown_json):
        """Sets the cost_breakdown_json of this HarnessIacmWorkspaceCreateresult.

        cost_breakdown_json is the identifier to the breakdown cost file from the current execution that was applied successfully  # noqa: E501

        :param cost_breakdown_json: The cost_breakdown_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._cost_breakdown_json = cost_breakdown_json

    @property
    def cost_diff_json(self):
        """Gets the cost_diff_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        cost_diff_json is the identifier to the diff cost file between the previous and current successful executions  # noqa: E501

        :return: The cost_diff_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._cost_diff_json

    @cost_diff_json.setter
    def cost_diff_json(self, cost_diff_json):
        """Sets the cost_diff_json of this HarnessIacmWorkspaceCreateresult.

        cost_diff_json is the identifier to the diff cost file between the previous and current successful executions  # noqa: E501

        :param cost_diff_json: The cost_diff_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._cost_diff_json = cost_diff_json

    @property
    def cost_estimation_enabled(self):
        """Gets the cost_estimation_enabled of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        define if cost estimation operations will be performed in this workspace  # noqa: E501

        :return: The cost_estimation_enabled of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: bool
        """
        return self._cost_estimation_enabled

    @cost_estimation_enabled.setter
    def cost_estimation_enabled(self, cost_estimation_enabled):
        """Sets the cost_estimation_enabled of this HarnessIacmWorkspaceCreateresult.

        define if cost estimation operations will be performed in this workspace  # noqa: E501

        :param cost_estimation_enabled: The cost_estimation_enabled of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: bool
        """

        self._cost_estimation_enabled = cost_estimation_enabled

    @property
    def created(self):
        """Gets the created of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Created is the unix timestamp at which the resource was originally created in milliseconds.  # noqa: E501

        :return: The created of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this HarnessIacmWorkspaceCreateresult.

        Created is the unix timestamp at which the resource was originally created in milliseconds.  # noqa: E501

        :param created: The created of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: int
        """
        if created is None:
            raise ValueError("Invalid value for `created`, must not be `None`")  # noqa: E501

        self._created = created

    @property
    def default_pipelines(self):
        """Gets the default_pipelines of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        List of default pipelines associated with this workspace and any per-workspace overrides.  # noqa: E501

        :return: The default_pipelines of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: dict(str, DefaultPipelineOverride)
        """
        return self._default_pipelines

    @default_pipelines.setter
    def default_pipelines(self, default_pipelines):
        """Sets the default_pipelines of this HarnessIacmWorkspaceCreateresult.

        List of default pipelines associated with this workspace and any per-workspace overrides.  # noqa: E501

        :param default_pipelines: The default_pipelines of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: dict(str, DefaultPipelineOverride)
        """

        self._default_pipelines = default_pipelines

    @property
    def description(self):
        """Gets the description of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Description provides long-form text about the resource.  # noqa: E501

        :return: The description of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this HarnessIacmWorkspaceCreateresult.

        Description provides long-form text about the resource.  # noqa: E501

        :param description: The description of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def environment_variables(self):
        """Gets the environment_variables of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        list of environment variables configured on the workspace.  # noqa: E501

        :return: The environment_variables of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: dict(str, VariableResource)
        """
        return self._environment_variables

    @environment_variables.setter
    def environment_variables(self, environment_variables):
        """Sets the environment_variables of this HarnessIacmWorkspaceCreateresult.

        list of environment variables configured on the workspace.  # noqa: E501

        :param environment_variables: The environment_variables of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: dict(str, VariableResource)
        """
        if environment_variables is None:
            raise ValueError("Invalid value for `environment_variables`, must not be `None`")  # noqa: E501

        self._environment_variables = environment_variables

    @property
    def id(self):
        """Gets the id of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        ID PK for internal uses  # noqa: E501

        :return: The id of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this HarnessIacmWorkspaceCreateresult.

        ID PK for internal uses  # noqa: E501

        :param id: The id of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def identifier(self):
        """Gets the identifier of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Workspace identifier.  # noqa: E501

        :return: The identifier of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this HarnessIacmWorkspaceCreateresult.

        Workspace identifier.  # noqa: E501

        :param identifier: The identifier of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """
        if identifier is None:
            raise ValueError("Invalid value for `identifier`, must not be `None`")  # noqa: E501

        self._identifier = identifier

    @property
    def modules_json(self):
        """Gets the modules_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        modules_json is the identifier of any modules metadata associated with this workspace  # noqa: E501

        :return: The modules_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._modules_json

    @modules_json.setter
    def modules_json(self, modules_json):
        """Sets the modules_json of this HarnessIacmWorkspaceCreateresult.

        modules_json is the identifier of any modules metadata associated with this workspace  # noqa: E501

        :param modules_json: The modules_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._modules_json = modules_json

    @property
    def name(self):
        """Gets the name of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Name is the human readable name for the resource.  # noqa: E501

        :return: The name of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this HarnessIacmWorkspaceCreateresult.

        Name is the human readable name for the resource.  # noqa: E501

        :param name: The name of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def org(self):
        """Gets the org of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Org is the organisation identifier.  # noqa: E501

        :return: The org of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._org

    @org.setter
    def org(self, org):
        """Sets the org of this HarnessIacmWorkspaceCreateresult.

        Org is the organisation identifier.  # noqa: E501

        :param org: The org of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """
        if org is None:
            raise ValueError("Invalid value for `org`, must not be `None`")  # noqa: E501

        self._org = org

    @property
    def policy_evaluation(self):
        """Gets the policy_evaluation of this HarnessIacmWorkspaceCreateresult.  # noqa: E501


        :return: The policy_evaluation of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: IaCMEvaluation
        """
        return self._policy_evaluation

    @policy_evaluation.setter
    def policy_evaluation(self, policy_evaluation):
        """Sets the policy_evaluation of this HarnessIacmWorkspaceCreateresult.


        :param policy_evaluation: The policy_evaluation of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: IaCMEvaluation
        """

        self._policy_evaluation = policy_evaluation

    @property
    def project(self):
        """Gets the project of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Project is the project identifier.  # noqa: E501

        :return: The project of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this HarnessIacmWorkspaceCreateresult.

        Project is the project identifier.  # noqa: E501

        :param project: The project of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """
        if project is None:
            raise ValueError("Invalid value for `project`, must not be `None`")  # noqa: E501

        self._project = project

    @property
    def provider_connector(self):
        """Gets the provider_connector of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Provider Connector is the reference to the connector for the infrastructure provider.  # noqa: E501

        :return: The provider_connector of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._provider_connector

    @provider_connector.setter
    def provider_connector(self, provider_connector):
        """Sets the provider_connector of this HarnessIacmWorkspaceCreateresult.

        Provider Connector is the reference to the connector for the infrastructure provider.  # noqa: E501

        :param provider_connector: The provider_connector of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """
        if provider_connector is None:
            raise ValueError("Invalid value for `provider_connector`, must not be `None`")  # noqa: E501

        self._provider_connector = provider_connector

    @property
    def provider_connectors(self):
        """Gets the provider_connectors of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        define an array of provider connectors that belong to Workspace  # noqa: E501

        :return: The provider_connectors of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: list[WorkspaceProviderConnector]
        """
        return self._provider_connectors

    @provider_connectors.setter
    def provider_connectors(self, provider_connectors):
        """Sets the provider_connectors of this HarnessIacmWorkspaceCreateresult.

        define an array of provider connectors that belong to Workspace  # noqa: E501

        :param provider_connectors: The provider_connectors of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: list[WorkspaceProviderConnector]
        """

        self._provider_connectors = provider_connectors

    @property
    def providers_json(self):
        """Gets the providers_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        providers_json is the identifier of any modules metadata associated with this workspace  # noqa: E501

        :return: The providers_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._providers_json

    @providers_json.setter
    def providers_json(self, providers_json):
        """Sets the providers_json of this HarnessIacmWorkspaceCreateresult.

        providers_json is the identifier of any modules metadata associated with this workspace  # noqa: E501

        :param providers_json: The providers_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._providers_json = providers_json

    @property
    def provisioner(self):
        """Gets the provisioner of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Provisioner defines the provisioning tool to use.  # noqa: E501

        :return: The provisioner of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._provisioner

    @provisioner.setter
    def provisioner(self, provisioner):
        """Sets the provisioner of this HarnessIacmWorkspaceCreateresult.

        Provisioner defines the provisioning tool to use.  # noqa: E501

        :param provisioner: The provisioner of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """
        if provisioner is None:
            raise ValueError("Invalid value for `provisioner`, must not be `None`")  # noqa: E501

        self._provisioner = provisioner

    @property
    def provisioner_data(self):
        """Gets the provisioner_data of this HarnessIacmWorkspaceCreateresult.  # noqa: E501


        :return: The provisioner_data of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._provisioner_data

    @provisioner_data.setter
    def provisioner_data(self, provisioner_data):
        """Sets the provisioner_data of this HarnessIacmWorkspaceCreateresult.


        :param provisioner_data: The provisioner_data of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """
        if provisioner_data is None:
            raise ValueError("Invalid value for `provisioner_data`, must not be `None`")  # noqa: E501

        self._provisioner_data = provisioner_data

    @property
    def provisioner_version(self):
        """Gets the provisioner_version of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Provisioner Version defines the tool version to use.  # noqa: E501

        :return: The provisioner_version of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._provisioner_version

    @provisioner_version.setter
    def provisioner_version(self, provisioner_version):
        """Sets the provisioner_version of this HarnessIacmWorkspaceCreateresult.

        Provisioner Version defines the tool version to use.  # noqa: E501

        :param provisioner_version: The provisioner_version of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._provisioner_version = provisioner_version

    @property
    def prune_sensitive_data(self):
        """Gets the prune_sensitive_data of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        prune_sensitive_data is a flag to enable or disable pruning of sensitive data  # noqa: E501

        :return: The prune_sensitive_data of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: bool
        """
        return self._prune_sensitive_data

    @prune_sensitive_data.setter
    def prune_sensitive_data(self, prune_sensitive_data):
        """Sets the prune_sensitive_data of this HarnessIacmWorkspaceCreateresult.

        prune_sensitive_data is a flag to enable or disable pruning of sensitive data  # noqa: E501

        :param prune_sensitive_data: The prune_sensitive_data of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: bool
        """

        self._prune_sensitive_data = prune_sensitive_data

    @property
    def repository(self):
        """Gets the repository of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Repository is the name of the repository to use.  # noqa: E501

        :return: The repository of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._repository

    @repository.setter
    def repository(self, repository):
        """Sets the repository of this HarnessIacmWorkspaceCreateresult.

        Repository is the name of the repository to use.  # noqa: E501

        :param repository: The repository of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._repository = repository

    @property
    def repository_branch(self):
        """Gets the repository_branch of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Repository Branch in which the code should be accessed.  # noqa: E501

        :return: The repository_branch of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._repository_branch

    @repository_branch.setter
    def repository_branch(self, repository_branch):
        """Sets the repository_branch of this HarnessIacmWorkspaceCreateresult.

        Repository Branch in which the code should be accessed.  # noqa: E501

        :param repository_branch: The repository_branch of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._repository_branch = repository_branch

    @property
    def repository_commit(self):
        """Gets the repository_commit of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Repository Commit/Tag in which the code should be accessed.  # noqa: E501

        :return: The repository_commit of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._repository_commit

    @repository_commit.setter
    def repository_commit(self, repository_commit):
        """Sets the repository_commit of this HarnessIacmWorkspaceCreateresult.

        Repository Commit/Tag in which the code should be accessed.  # noqa: E501

        :param repository_commit: The repository_commit of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._repository_commit = repository_commit

    @property
    def repository_connector(self):
        """Gets the repository_connector of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Repository Connector is the reference to the connector to use for this code.  # noqa: E501

        :return: The repository_connector of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._repository_connector

    @repository_connector.setter
    def repository_connector(self, repository_connector):
        """Sets the repository_connector of this HarnessIacmWorkspaceCreateresult.

        Repository Connector is the reference to the connector to use for this code.  # noqa: E501

        :param repository_connector: The repository_connector of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """
        if repository_connector is None:
            raise ValueError("Invalid value for `repository_connector`, must not be `None`")  # noqa: E501

        self._repository_connector = repository_connector

    @property
    def repository_path(self):
        """Gets the repository_path of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Repository Path is the path in which the infra code resides.  # noqa: E501

        :return: The repository_path of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._repository_path

    @repository_path.setter
    def repository_path(self, repository_path):
        """Sets the repository_path of this HarnessIacmWorkspaceCreateresult.

        Repository Path is the path in which the infra code resides.  # noqa: E501

        :param repository_path: The repository_path of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._repository_path = repository_path

    @property
    def repository_sha(self):
        """Gets the repository_sha of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Repository SHA in which the code should be accessed.  # noqa: E501

        :return: The repository_sha of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._repository_sha

    @repository_sha.setter
    def repository_sha(self, repository_sha):
        """Sets the repository_sha of this HarnessIacmWorkspaceCreateresult.

        Repository SHA in which the code should be accessed.  # noqa: E501

        :param repository_sha: The repository_sha of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._repository_sha = repository_sha

    @property
    def repository_submodules(self):
        """Gets the repository_submodules of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        repository_submodules is the instruction about whether to clone submodules in the pipeline step  # noqa: E501

        :return: The repository_submodules of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._repository_submodules

    @repository_submodules.setter
    def repository_submodules(self, repository_submodules):
        """Sets the repository_submodules of this HarnessIacmWorkspaceCreateresult.

        repository_submodules is the instruction about whether to clone submodules in the pipeline step  # noqa: E501

        :param repository_submodules: The repository_submodules of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """
        allowed_values = ["false", "true", "recursive"]  # noqa: E501
        if repository_submodules not in allowed_values:
            raise ValueError(
                "Invalid value for `repository_submodules` ({0}), must be one of {1}"  # noqa: E501
                .format(repository_submodules, allowed_values)
            )

        self._repository_submodules = repository_submodules

    @property
    def run_all(self):
        """Gets the run_all of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Run-All terragrunt modules.  # noqa: E501

        :return: The run_all of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: bool
        """
        return self._run_all

    @run_all.setter
    def run_all(self, run_all):
        """Sets the run_all of this HarnessIacmWorkspaceCreateresult.

        Run-All terragrunt modules.  # noqa: E501

        :param run_all: The run_all of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: bool
        """

        self._run_all = run_all

    @property
    def sparse_checkout(self):
        """Gets the sparse_checkout of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        List of patterens that will be used for sparse checkout option of git clone  # noqa: E501

        :return: The sparse_checkout of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._sparse_checkout

    @sparse_checkout.setter
    def sparse_checkout(self, sparse_checkout):
        """Sets the sparse_checkout of this HarnessIacmWorkspaceCreateresult.

        List of patterens that will be used for sparse checkout option of git clone  # noqa: E501

        :param sparse_checkout: The sparse_checkout of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._sparse_checkout = sparse_checkout

    @property
    def state_checksum(self):
        """Gets the state_checksum of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        state_checksum is the sha-256 checksum of terraform state file  # noqa: E501

        :return: The state_checksum of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._state_checksum

    @state_checksum.setter
    def state_checksum(self, state_checksum):
        """Sets the state_checksum of this HarnessIacmWorkspaceCreateresult.

        state_checksum is the sha-256 checksum of terraform state file  # noqa: E501

        :param state_checksum: The state_checksum of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._state_checksum = state_checksum

    @property
    def status(self):
        """Gets the status of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        The status of the workspace  # noqa: E501

        :return: The status of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this HarnessIacmWorkspaceCreateresult.

        The status of the workspace  # noqa: E501

        :param status: The status of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501
        allowed_values = ["active", "inactive", "provisioning", "destroying", "failed", "unknown"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def tags(self):
        """Gets the tags of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Tags associated with the workspace.  # noqa: E501

        :return: The tags of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this HarnessIacmWorkspaceCreateresult.

        Tags associated with the workspace.  # noqa: E501

        :param tags: The tags of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """
        if tags is None:
            raise ValueError("Invalid value for `tags`, must not be `None`")  # noqa: E501

        self._tags = tags

    @property
    def terraform_plan_json(self):
        """Gets the terraform_plan_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        terraform_plan_json is the identifier to the current state file only in JSON format.  # noqa: E501

        :return: The terraform_plan_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._terraform_plan_json

    @terraform_plan_json.setter
    def terraform_plan_json(self, terraform_plan_json):
        """Sets the terraform_plan_json of this HarnessIacmWorkspaceCreateresult.

        terraform_plan_json is the identifier to the current state file only in JSON format.  # noqa: E501

        :param terraform_plan_json: The terraform_plan_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._terraform_plan_json = terraform_plan_json

    @property
    def terraform_state(self):
        """Gets the terraform_state of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        terraform_state is the identifier to the plan file used to create the latest state.  # noqa: E501

        :return: The terraform_state of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._terraform_state

    @terraform_state.setter
    def terraform_state(self, terraform_state):
        """Sets the terraform_state of this HarnessIacmWorkspaceCreateresult.

        terraform_state is the identifier to the plan file used to create the latest state.  # noqa: E501

        :param terraform_state: The terraform_state of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._terraform_state = terraform_state

    @property
    def terraform_state_json(self):
        """Gets the terraform_state_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        terraform_state_json is the identifier to the plan file used to create the latest state only in JSON format.  # noqa: E501

        :return: The terraform_state_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._terraform_state_json

    @terraform_state_json.setter
    def terraform_state_json(self, terraform_state_json):
        """Sets the terraform_state_json of this HarnessIacmWorkspaceCreateresult.

        terraform_state_json is the identifier to the plan file used to create the latest state only in JSON format.  # noqa: E501

        :param terraform_state_json: The terraform_state_json of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._terraform_state_json = terraform_state_json

    @property
    def terraform_variable_files(self):
        """Gets the terraform_variable_files of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        define an array of terraform variables files that belong to a different repository  # noqa: E501

        :return: The terraform_variable_files of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: list[WorkspaceTerraformVariableFiles]
        """
        return self._terraform_variable_files

    @terraform_variable_files.setter
    def terraform_variable_files(self, terraform_variable_files):
        """Sets the terraform_variable_files of this HarnessIacmWorkspaceCreateresult.

        define an array of terraform variables files that belong to a different repository  # noqa: E501

        :param terraform_variable_files: The terraform_variable_files of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: list[WorkspaceTerraformVariableFiles]
        """

        self._terraform_variable_files = terraform_variable_files

    @property
    def terraform_variables(self):
        """Gets the terraform_variables of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        list of terraform variables configured on the workspace.  # noqa: E501

        :return: The terraform_variables of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: dict(str, VariableResource)
        """
        return self._terraform_variables

    @terraform_variables.setter
    def terraform_variables(self, terraform_variables):
        """Sets the terraform_variables of this HarnessIacmWorkspaceCreateresult.

        list of terraform variables configured on the workspace.  # noqa: E501

        :param terraform_variables: The terraform_variables of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: dict(str, VariableResource)
        """
        if terraform_variables is None:
            raise ValueError("Invalid value for `terraform_variables`, must not be `None`")  # noqa: E501

        self._terraform_variables = terraform_variables

    @property
    def terragrunt_provider(self):
        """Gets the terragrunt_provider of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Whether this workspace uses terragrunt to provision infrastructure  # noqa: E501

        :return: The terragrunt_provider of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: bool
        """
        return self._terragrunt_provider

    @terragrunt_provider.setter
    def terragrunt_provider(self, terragrunt_provider):
        """Sets the terragrunt_provider of this HarnessIacmWorkspaceCreateresult.

        Whether this workspace uses terragrunt to provision infrastructure  # noqa: E501

        :param terragrunt_provider: The terragrunt_provider of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: bool
        """

        self._terragrunt_provider = terragrunt_provider

    @property
    def terragrunt_version(self):
        """Gets the terragrunt_version of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Terragrunt Version to use when provisioner is terragrunt.  # noqa: E501

        :return: The terragrunt_version of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: str
        """
        return self._terragrunt_version

    @terragrunt_version.setter
    def terragrunt_version(self, terragrunt_version):
        """Sets the terragrunt_version of this HarnessIacmWorkspaceCreateresult.

        Terragrunt Version to use when provisioner is terragrunt.  # noqa: E501

        :param terragrunt_version: The terragrunt_version of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: str
        """

        self._terragrunt_version = terragrunt_version

    @property
    def updated(self):
        """Gets the updated of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Modified is the unix timestamp at which the resource was last modified in milliseconds.  # noqa: E501

        :return: The updated of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: int
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this HarnessIacmWorkspaceCreateresult.

        Modified is the unix timestamp at which the resource was last modified in milliseconds.  # noqa: E501

        :param updated: The updated of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: int
        """
        if updated is None:
            raise ValueError("Invalid value for `updated`, must not be `None`")  # noqa: E501

        self._updated = updated

    @property
    def variable_sets(self):
        """Gets the variable_sets of this HarnessIacmWorkspaceCreateresult.  # noqa: E501

        Attached Variable Sets references  # noqa: E501

        :return: The variable_sets of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :rtype: list[str]
        """
        return self._variable_sets

    @variable_sets.setter
    def variable_sets(self, variable_sets):
        """Sets the variable_sets of this HarnessIacmWorkspaceCreateresult.

        Attached Variable Sets references  # noqa: E501

        :param variable_sets: The variable_sets of this HarnessIacmWorkspaceCreateresult.  # noqa: E501
        :type: list[str]
        """

        self._variable_sets = variable_sets

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
        if issubclass(HarnessIacmWorkspaceCreateresult, dict):
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
        if not isinstance(other, HarnessIacmWorkspaceCreateresult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
