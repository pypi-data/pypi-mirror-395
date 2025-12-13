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

class HarnessIacmApproval(object):
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
        'actioned_by': 'str',
        'actioned_by_email': 'str',
        'created': 'int',
        'id': 'str',
        'org': 'str',
        'pipeline_execution_id': 'str',
        'pipeline_stage_id': 'str',
        'project': 'str',
        'status': 'str',
        'updated': 'int',
        'workspace_id': 'str'
    }

    attribute_map = {
        'account': 'account',
        'actioned_by': 'actioned_by',
        'actioned_by_email': 'actioned_by_email',
        'created': 'created',
        'id': 'id',
        'org': 'org',
        'pipeline_execution_id': 'pipeline_execution_id',
        'pipeline_stage_id': 'pipeline_stage_id',
        'project': 'project',
        'status': 'status',
        'updated': 'updated',
        'workspace_id': 'workspace_id'
    }

    def __init__(self, account=None, actioned_by=None, actioned_by_email=None, created=None, id=None, org=None, pipeline_execution_id=None, pipeline_stage_id=None, project=None, status='pending', updated=None, workspace_id=None):  # noqa: E501
        """HarnessIacmApproval - a model defined in Swagger"""  # noqa: E501
        self._account = None
        self._actioned_by = None
        self._actioned_by_email = None
        self._created = None
        self._id = None
        self._org = None
        self._pipeline_execution_id = None
        self._pipeline_stage_id = None
        self._project = None
        self._status = None
        self._updated = None
        self._workspace_id = None
        self.discriminator = None
        self.account = account
        if actioned_by is not None:
            self.actioned_by = actioned_by
        if actioned_by_email is not None:
            self.actioned_by_email = actioned_by_email
        self.created = created
        self.id = id
        self.org = org
        self.pipeline_execution_id = pipeline_execution_id
        self.pipeline_stage_id = pipeline_stage_id
        self.project = project
        self.status = status
        self.updated = updated
        self.workspace_id = workspace_id

    @property
    def account(self):
        """Gets the account of this HarnessIacmApproval.  # noqa: E501

        Account is the internal customer account ID.  # noqa: E501

        :return: The account of this HarnessIacmApproval.  # noqa: E501
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this HarnessIacmApproval.

        Account is the internal customer account ID.  # noqa: E501

        :param account: The account of this HarnessIacmApproval.  # noqa: E501
        :type: str
        """
        if account is None:
            raise ValueError("Invalid value for `account`, must not be `None`")  # noqa: E501

        self._account = account

    @property
    def actioned_by(self):
        """Gets the actioned_by of this HarnessIacmApproval.  # noqa: E501

        User that approved/rejected the step  # noqa: E501

        :return: The actioned_by of this HarnessIacmApproval.  # noqa: E501
        :rtype: str
        """
        return self._actioned_by

    @actioned_by.setter
    def actioned_by(self, actioned_by):
        """Sets the actioned_by of this HarnessIacmApproval.

        User that approved/rejected the step  # noqa: E501

        :param actioned_by: The actioned_by of this HarnessIacmApproval.  # noqa: E501
        :type: str
        """

        self._actioned_by = actioned_by

    @property
    def actioned_by_email(self):
        """Gets the actioned_by_email of this HarnessIacmApproval.  # noqa: E501

        Email of the user that approved/rejected the step  # noqa: E501

        :return: The actioned_by_email of this HarnessIacmApproval.  # noqa: E501
        :rtype: str
        """
        return self._actioned_by_email

    @actioned_by_email.setter
    def actioned_by_email(self, actioned_by_email):
        """Sets the actioned_by_email of this HarnessIacmApproval.

        Email of the user that approved/rejected the step  # noqa: E501

        :param actioned_by_email: The actioned_by_email of this HarnessIacmApproval.  # noqa: E501
        :type: str
        """

        self._actioned_by_email = actioned_by_email

    @property
    def created(self):
        """Gets the created of this HarnessIacmApproval.  # noqa: E501

        Created is the unix timestamp at which the resource was originally created in milliseconds.  # noqa: E501

        :return: The created of this HarnessIacmApproval.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this HarnessIacmApproval.

        Created is the unix timestamp at which the resource was originally created in milliseconds.  # noqa: E501

        :param created: The created of this HarnessIacmApproval.  # noqa: E501
        :type: int
        """
        if created is None:
            raise ValueError("Invalid value for `created`, must not be `None`")  # noqa: E501

        self._created = created

    @property
    def id(self):
        """Gets the id of this HarnessIacmApproval.  # noqa: E501


        :return: The id of this HarnessIacmApproval.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this HarnessIacmApproval.


        :param id: The id of this HarnessIacmApproval.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def org(self):
        """Gets the org of this HarnessIacmApproval.  # noqa: E501

        Org is the organisation identifier.  # noqa: E501

        :return: The org of this HarnessIacmApproval.  # noqa: E501
        :rtype: str
        """
        return self._org

    @org.setter
    def org(self, org):
        """Sets the org of this HarnessIacmApproval.

        Org is the organisation identifier.  # noqa: E501

        :param org: The org of this HarnessIacmApproval.  # noqa: E501
        :type: str
        """
        if org is None:
            raise ValueError("Invalid value for `org`, must not be `None`")  # noqa: E501

        self._org = org

    @property
    def pipeline_execution_id(self):
        """Gets the pipeline_execution_id of this HarnessIacmApproval.  # noqa: E501

        The unique identifier for the associated pipeline execution  # noqa: E501

        :return: The pipeline_execution_id of this HarnessIacmApproval.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_execution_id

    @pipeline_execution_id.setter
    def pipeline_execution_id(self, pipeline_execution_id):
        """Sets the pipeline_execution_id of this HarnessIacmApproval.

        The unique identifier for the associated pipeline execution  # noqa: E501

        :param pipeline_execution_id: The pipeline_execution_id of this HarnessIacmApproval.  # noqa: E501
        :type: str
        """
        if pipeline_execution_id is None:
            raise ValueError("Invalid value for `pipeline_execution_id`, must not be `None`")  # noqa: E501

        self._pipeline_execution_id = pipeline_execution_id

    @property
    def pipeline_stage_id(self):
        """Gets the pipeline_stage_id of this HarnessIacmApproval.  # noqa: E501

        The unique identifier for the associated pipeline execution stage  # noqa: E501

        :return: The pipeline_stage_id of this HarnessIacmApproval.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_stage_id

    @pipeline_stage_id.setter
    def pipeline_stage_id(self, pipeline_stage_id):
        """Sets the pipeline_stage_id of this HarnessIacmApproval.

        The unique identifier for the associated pipeline execution stage  # noqa: E501

        :param pipeline_stage_id: The pipeline_stage_id of this HarnessIacmApproval.  # noqa: E501
        :type: str
        """
        if pipeline_stage_id is None:
            raise ValueError("Invalid value for `pipeline_stage_id`, must not be `None`")  # noqa: E501

        self._pipeline_stage_id = pipeline_stage_id

    @property
    def project(self):
        """Gets the project of this HarnessIacmApproval.  # noqa: E501

        Project is the project identifier.  # noqa: E501

        :return: The project of this HarnessIacmApproval.  # noqa: E501
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this HarnessIacmApproval.

        Project is the project identifier.  # noqa: E501

        :param project: The project of this HarnessIacmApproval.  # noqa: E501
        :type: str
        """
        if project is None:
            raise ValueError("Invalid value for `project`, must not be `None`")  # noqa: E501

        self._project = project

    @property
    def status(self):
        """Gets the status of this HarnessIacmApproval.  # noqa: E501

        Status of the approval resource  # noqa: E501

        :return: The status of this HarnessIacmApproval.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this HarnessIacmApproval.

        Status of the approval resource  # noqa: E501

        :param status: The status of this HarnessIacmApproval.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def updated(self):
        """Gets the updated of this HarnessIacmApproval.  # noqa: E501

        Modified is the unix timestamp at which the resource was last modified in milliseconds.  # noqa: E501

        :return: The updated of this HarnessIacmApproval.  # noqa: E501
        :rtype: int
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this HarnessIacmApproval.

        Modified is the unix timestamp at which the resource was last modified in milliseconds.  # noqa: E501

        :param updated: The updated of this HarnessIacmApproval.  # noqa: E501
        :type: int
        """
        if updated is None:
            raise ValueError("Invalid value for `updated`, must not be `None`")  # noqa: E501

        self._updated = updated

    @property
    def workspace_id(self):
        """Gets the workspace_id of this HarnessIacmApproval.  # noqa: E501

        The unique identifier for the workspace_id  # noqa: E501

        :return: The workspace_id of this HarnessIacmApproval.  # noqa: E501
        :rtype: str
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id):
        """Sets the workspace_id of this HarnessIacmApproval.

        The unique identifier for the workspace_id  # noqa: E501

        :param workspace_id: The workspace_id of this HarnessIacmApproval.  # noqa: E501
        :type: str
        """
        if workspace_id is None:
            raise ValueError("Invalid value for `workspace_id`, must not be `None`")  # noqa: E501

        self._workspace_id = workspace_id

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
        if issubclass(HarnessIacmApproval, dict):
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
        if not isinstance(other, HarnessIacmApproval):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
