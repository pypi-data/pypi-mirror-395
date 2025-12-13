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

class TypesPullReq(object):
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
        'author': 'TypesPrincipalInfo',
        'check_summary': 'TypesCheckCountSummary',
        'closed': 'int',
        'created': 'int',
        'description': 'str',
        'edited': 'int',
        'is_draft': 'bool',
        'labels': 'list[TypesLabelPullReqAssignmentInfo]',
        'merge_base_sha': 'str',
        'merge_check_status': 'EnumMergeCheckStatus',
        'merge_conflicts': 'list[str]',
        'merge_method': 'EnumMergeMethod',
        'merge_target_sha': 'str',
        'merge_violations_bypassed': 'bool',
        'merged': 'int',
        'merger': 'TypesPrincipalInfo',
        'number': 'int',
        'rebase_check_status': 'EnumMergeCheckStatus',
        'rebase_conflicts': 'list[str]',
        'rules': 'list[TypesRuleInfo]',
        'source_branch': 'str',
        'source_repo_id': 'int',
        'source_sha': 'str',
        'state': 'EnumPullReqState',
        'stats': 'TypesPullReqStats',
        'target_branch': 'str',
        'target_repo_id': 'int',
        'title': 'str',
        'updated': 'int'
    }

    attribute_map = {
        'author': 'author',
        'check_summary': 'check_summary',
        'closed': 'closed',
        'created': 'created',
        'description': 'description',
        'edited': 'edited',
        'is_draft': 'is_draft',
        'labels': 'labels',
        'merge_base_sha': 'merge_base_sha',
        'merge_check_status': 'merge_check_status',
        'merge_conflicts': 'merge_conflicts',
        'merge_method': 'merge_method',
        'merge_target_sha': 'merge_target_sha',
        'merge_violations_bypassed': 'merge_violations_bypassed',
        'merged': 'merged',
        'merger': 'merger',
        'number': 'number',
        'rebase_check_status': 'rebase_check_status',
        'rebase_conflicts': 'rebase_conflicts',
        'rules': 'rules',
        'source_branch': 'source_branch',
        'source_repo_id': 'source_repo_id',
        'source_sha': 'source_sha',
        'state': 'state',
        'stats': 'stats',
        'target_branch': 'target_branch',
        'target_repo_id': 'target_repo_id',
        'title': 'title',
        'updated': 'updated'
    }

    def __init__(self, author=None, check_summary=None, closed=None, created=None, description=None, edited=None, is_draft=None, labels=None, merge_base_sha=None, merge_check_status=None, merge_conflicts=None, merge_method=None, merge_target_sha=None, merge_violations_bypassed=None, merged=None, merger=None, number=None, rebase_check_status=None, rebase_conflicts=None, rules=None, source_branch=None, source_repo_id=None, source_sha=None, state=None, stats=None, target_branch=None, target_repo_id=None, title=None, updated=None):  # noqa: E501
        """TypesPullReq - a model defined in Swagger"""  # noqa: E501
        self._author = None
        self._check_summary = None
        self._closed = None
        self._created = None
        self._description = None
        self._edited = None
        self._is_draft = None
        self._labels = None
        self._merge_base_sha = None
        self._merge_check_status = None
        self._merge_conflicts = None
        self._merge_method = None
        self._merge_target_sha = None
        self._merge_violations_bypassed = None
        self._merged = None
        self._merger = None
        self._number = None
        self._rebase_check_status = None
        self._rebase_conflicts = None
        self._rules = None
        self._source_branch = None
        self._source_repo_id = None
        self._source_sha = None
        self._state = None
        self._stats = None
        self._target_branch = None
        self._target_repo_id = None
        self._title = None
        self._updated = None
        self.discriminator = None
        if author is not None:
            self.author = author
        if check_summary is not None:
            self.check_summary = check_summary
        if closed is not None:
            self.closed = closed
        if created is not None:
            self.created = created
        if description is not None:
            self.description = description
        if edited is not None:
            self.edited = edited
        if is_draft is not None:
            self.is_draft = is_draft
        if labels is not None:
            self.labels = labels
        if merge_base_sha is not None:
            self.merge_base_sha = merge_base_sha
        if merge_check_status is not None:
            self.merge_check_status = merge_check_status
        if merge_conflicts is not None:
            self.merge_conflicts = merge_conflicts
        if merge_method is not None:
            self.merge_method = merge_method
        if merge_target_sha is not None:
            self.merge_target_sha = merge_target_sha
        if merge_violations_bypassed is not None:
            self.merge_violations_bypassed = merge_violations_bypassed
        if merged is not None:
            self.merged = merged
        if merger is not None:
            self.merger = merger
        if number is not None:
            self.number = number
        if rebase_check_status is not None:
            self.rebase_check_status = rebase_check_status
        if rebase_conflicts is not None:
            self.rebase_conflicts = rebase_conflicts
        if rules is not None:
            self.rules = rules
        if source_branch is not None:
            self.source_branch = source_branch
        if source_repo_id is not None:
            self.source_repo_id = source_repo_id
        if source_sha is not None:
            self.source_sha = source_sha
        if state is not None:
            self.state = state
        if stats is not None:
            self.stats = stats
        if target_branch is not None:
            self.target_branch = target_branch
        if target_repo_id is not None:
            self.target_repo_id = target_repo_id
        if title is not None:
            self.title = title
        if updated is not None:
            self.updated = updated

    @property
    def author(self):
        """Gets the author of this TypesPullReq.  # noqa: E501


        :return: The author of this TypesPullReq.  # noqa: E501
        :rtype: TypesPrincipalInfo
        """
        return self._author

    @author.setter
    def author(self, author):
        """Sets the author of this TypesPullReq.


        :param author: The author of this TypesPullReq.  # noqa: E501
        :type: TypesPrincipalInfo
        """

        self._author = author

    @property
    def check_summary(self):
        """Gets the check_summary of this TypesPullReq.  # noqa: E501


        :return: The check_summary of this TypesPullReq.  # noqa: E501
        :rtype: TypesCheckCountSummary
        """
        return self._check_summary

    @check_summary.setter
    def check_summary(self, check_summary):
        """Sets the check_summary of this TypesPullReq.


        :param check_summary: The check_summary of this TypesPullReq.  # noqa: E501
        :type: TypesCheckCountSummary
        """

        self._check_summary = check_summary

    @property
    def closed(self):
        """Gets the closed of this TypesPullReq.  # noqa: E501


        :return: The closed of this TypesPullReq.  # noqa: E501
        :rtype: int
        """
        return self._closed

    @closed.setter
    def closed(self, closed):
        """Sets the closed of this TypesPullReq.


        :param closed: The closed of this TypesPullReq.  # noqa: E501
        :type: int
        """

        self._closed = closed

    @property
    def created(self):
        """Gets the created of this TypesPullReq.  # noqa: E501


        :return: The created of this TypesPullReq.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this TypesPullReq.


        :param created: The created of this TypesPullReq.  # noqa: E501
        :type: int
        """

        self._created = created

    @property
    def description(self):
        """Gets the description of this TypesPullReq.  # noqa: E501


        :return: The description of this TypesPullReq.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this TypesPullReq.


        :param description: The description of this TypesPullReq.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def edited(self):
        """Gets the edited of this TypesPullReq.  # noqa: E501


        :return: The edited of this TypesPullReq.  # noqa: E501
        :rtype: int
        """
        return self._edited

    @edited.setter
    def edited(self, edited):
        """Sets the edited of this TypesPullReq.


        :param edited: The edited of this TypesPullReq.  # noqa: E501
        :type: int
        """

        self._edited = edited

    @property
    def is_draft(self):
        """Gets the is_draft of this TypesPullReq.  # noqa: E501


        :return: The is_draft of this TypesPullReq.  # noqa: E501
        :rtype: bool
        """
        return self._is_draft

    @is_draft.setter
    def is_draft(self, is_draft):
        """Sets the is_draft of this TypesPullReq.


        :param is_draft: The is_draft of this TypesPullReq.  # noqa: E501
        :type: bool
        """

        self._is_draft = is_draft

    @property
    def labels(self):
        """Gets the labels of this TypesPullReq.  # noqa: E501


        :return: The labels of this TypesPullReq.  # noqa: E501
        :rtype: list[TypesLabelPullReqAssignmentInfo]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this TypesPullReq.


        :param labels: The labels of this TypesPullReq.  # noqa: E501
        :type: list[TypesLabelPullReqAssignmentInfo]
        """

        self._labels = labels

    @property
    def merge_base_sha(self):
        """Gets the merge_base_sha of this TypesPullReq.  # noqa: E501


        :return: The merge_base_sha of this TypesPullReq.  # noqa: E501
        :rtype: str
        """
        return self._merge_base_sha

    @merge_base_sha.setter
    def merge_base_sha(self, merge_base_sha):
        """Sets the merge_base_sha of this TypesPullReq.


        :param merge_base_sha: The merge_base_sha of this TypesPullReq.  # noqa: E501
        :type: str
        """

        self._merge_base_sha = merge_base_sha

    @property
    def merge_check_status(self):
        """Gets the merge_check_status of this TypesPullReq.  # noqa: E501


        :return: The merge_check_status of this TypesPullReq.  # noqa: E501
        :rtype: EnumMergeCheckStatus
        """
        return self._merge_check_status

    @merge_check_status.setter
    def merge_check_status(self, merge_check_status):
        """Sets the merge_check_status of this TypesPullReq.


        :param merge_check_status: The merge_check_status of this TypesPullReq.  # noqa: E501
        :type: EnumMergeCheckStatus
        """

        self._merge_check_status = merge_check_status

    @property
    def merge_conflicts(self):
        """Gets the merge_conflicts of this TypesPullReq.  # noqa: E501


        :return: The merge_conflicts of this TypesPullReq.  # noqa: E501
        :rtype: list[str]
        """
        return self._merge_conflicts

    @merge_conflicts.setter
    def merge_conflicts(self, merge_conflicts):
        """Sets the merge_conflicts of this TypesPullReq.


        :param merge_conflicts: The merge_conflicts of this TypesPullReq.  # noqa: E501
        :type: list[str]
        """

        self._merge_conflicts = merge_conflicts

    @property
    def merge_method(self):
        """Gets the merge_method of this TypesPullReq.  # noqa: E501


        :return: The merge_method of this TypesPullReq.  # noqa: E501
        :rtype: EnumMergeMethod
        """
        return self._merge_method

    @merge_method.setter
    def merge_method(self, merge_method):
        """Sets the merge_method of this TypesPullReq.


        :param merge_method: The merge_method of this TypesPullReq.  # noqa: E501
        :type: EnumMergeMethod
        """

        self._merge_method = merge_method

    @property
    def merge_target_sha(self):
        """Gets the merge_target_sha of this TypesPullReq.  # noqa: E501


        :return: The merge_target_sha of this TypesPullReq.  # noqa: E501
        :rtype: str
        """
        return self._merge_target_sha

    @merge_target_sha.setter
    def merge_target_sha(self, merge_target_sha):
        """Sets the merge_target_sha of this TypesPullReq.


        :param merge_target_sha: The merge_target_sha of this TypesPullReq.  # noqa: E501
        :type: str
        """

        self._merge_target_sha = merge_target_sha

    @property
    def merge_violations_bypassed(self):
        """Gets the merge_violations_bypassed of this TypesPullReq.  # noqa: E501


        :return: The merge_violations_bypassed of this TypesPullReq.  # noqa: E501
        :rtype: bool
        """
        return self._merge_violations_bypassed

    @merge_violations_bypassed.setter
    def merge_violations_bypassed(self, merge_violations_bypassed):
        """Sets the merge_violations_bypassed of this TypesPullReq.


        :param merge_violations_bypassed: The merge_violations_bypassed of this TypesPullReq.  # noqa: E501
        :type: bool
        """

        self._merge_violations_bypassed = merge_violations_bypassed

    @property
    def merged(self):
        """Gets the merged of this TypesPullReq.  # noqa: E501


        :return: The merged of this TypesPullReq.  # noqa: E501
        :rtype: int
        """
        return self._merged

    @merged.setter
    def merged(self, merged):
        """Sets the merged of this TypesPullReq.


        :param merged: The merged of this TypesPullReq.  # noqa: E501
        :type: int
        """

        self._merged = merged

    @property
    def merger(self):
        """Gets the merger of this TypesPullReq.  # noqa: E501


        :return: The merger of this TypesPullReq.  # noqa: E501
        :rtype: TypesPrincipalInfo
        """
        return self._merger

    @merger.setter
    def merger(self, merger):
        """Sets the merger of this TypesPullReq.


        :param merger: The merger of this TypesPullReq.  # noqa: E501
        :type: TypesPrincipalInfo
        """

        self._merger = merger

    @property
    def number(self):
        """Gets the number of this TypesPullReq.  # noqa: E501


        :return: The number of this TypesPullReq.  # noqa: E501
        :rtype: int
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this TypesPullReq.


        :param number: The number of this TypesPullReq.  # noqa: E501
        :type: int
        """

        self._number = number

    @property
    def rebase_check_status(self):
        """Gets the rebase_check_status of this TypesPullReq.  # noqa: E501


        :return: The rebase_check_status of this TypesPullReq.  # noqa: E501
        :rtype: EnumMergeCheckStatus
        """
        return self._rebase_check_status

    @rebase_check_status.setter
    def rebase_check_status(self, rebase_check_status):
        """Sets the rebase_check_status of this TypesPullReq.


        :param rebase_check_status: The rebase_check_status of this TypesPullReq.  # noqa: E501
        :type: EnumMergeCheckStatus
        """

        self._rebase_check_status = rebase_check_status

    @property
    def rebase_conflicts(self):
        """Gets the rebase_conflicts of this TypesPullReq.  # noqa: E501


        :return: The rebase_conflicts of this TypesPullReq.  # noqa: E501
        :rtype: list[str]
        """
        return self._rebase_conflicts

    @rebase_conflicts.setter
    def rebase_conflicts(self, rebase_conflicts):
        """Sets the rebase_conflicts of this TypesPullReq.


        :param rebase_conflicts: The rebase_conflicts of this TypesPullReq.  # noqa: E501
        :type: list[str]
        """

        self._rebase_conflicts = rebase_conflicts

    @property
    def rules(self):
        """Gets the rules of this TypesPullReq.  # noqa: E501


        :return: The rules of this TypesPullReq.  # noqa: E501
        :rtype: list[TypesRuleInfo]
        """
        return self._rules

    @rules.setter
    def rules(self, rules):
        """Sets the rules of this TypesPullReq.


        :param rules: The rules of this TypesPullReq.  # noqa: E501
        :type: list[TypesRuleInfo]
        """

        self._rules = rules

    @property
    def source_branch(self):
        """Gets the source_branch of this TypesPullReq.  # noqa: E501


        :return: The source_branch of this TypesPullReq.  # noqa: E501
        :rtype: str
        """
        return self._source_branch

    @source_branch.setter
    def source_branch(self, source_branch):
        """Sets the source_branch of this TypesPullReq.


        :param source_branch: The source_branch of this TypesPullReq.  # noqa: E501
        :type: str
        """

        self._source_branch = source_branch

    @property
    def source_repo_id(self):
        """Gets the source_repo_id of this TypesPullReq.  # noqa: E501


        :return: The source_repo_id of this TypesPullReq.  # noqa: E501
        :rtype: int
        """
        return self._source_repo_id

    @source_repo_id.setter
    def source_repo_id(self, source_repo_id):
        """Sets the source_repo_id of this TypesPullReq.


        :param source_repo_id: The source_repo_id of this TypesPullReq.  # noqa: E501
        :type: int
        """

        self._source_repo_id = source_repo_id

    @property
    def source_sha(self):
        """Gets the source_sha of this TypesPullReq.  # noqa: E501


        :return: The source_sha of this TypesPullReq.  # noqa: E501
        :rtype: str
        """
        return self._source_sha

    @source_sha.setter
    def source_sha(self, source_sha):
        """Sets the source_sha of this TypesPullReq.


        :param source_sha: The source_sha of this TypesPullReq.  # noqa: E501
        :type: str
        """

        self._source_sha = source_sha

    @property
    def state(self):
        """Gets the state of this TypesPullReq.  # noqa: E501


        :return: The state of this TypesPullReq.  # noqa: E501
        :rtype: EnumPullReqState
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this TypesPullReq.


        :param state: The state of this TypesPullReq.  # noqa: E501
        :type: EnumPullReqState
        """

        self._state = state

    @property
    def stats(self):
        """Gets the stats of this TypesPullReq.  # noqa: E501


        :return: The stats of this TypesPullReq.  # noqa: E501
        :rtype: TypesPullReqStats
        """
        return self._stats

    @stats.setter
    def stats(self, stats):
        """Sets the stats of this TypesPullReq.


        :param stats: The stats of this TypesPullReq.  # noqa: E501
        :type: TypesPullReqStats
        """

        self._stats = stats

    @property
    def target_branch(self):
        """Gets the target_branch of this TypesPullReq.  # noqa: E501


        :return: The target_branch of this TypesPullReq.  # noqa: E501
        :rtype: str
        """
        return self._target_branch

    @target_branch.setter
    def target_branch(self, target_branch):
        """Sets the target_branch of this TypesPullReq.


        :param target_branch: The target_branch of this TypesPullReq.  # noqa: E501
        :type: str
        """

        self._target_branch = target_branch

    @property
    def target_repo_id(self):
        """Gets the target_repo_id of this TypesPullReq.  # noqa: E501


        :return: The target_repo_id of this TypesPullReq.  # noqa: E501
        :rtype: int
        """
        return self._target_repo_id

    @target_repo_id.setter
    def target_repo_id(self, target_repo_id):
        """Sets the target_repo_id of this TypesPullReq.


        :param target_repo_id: The target_repo_id of this TypesPullReq.  # noqa: E501
        :type: int
        """

        self._target_repo_id = target_repo_id

    @property
    def title(self):
        """Gets the title of this TypesPullReq.  # noqa: E501


        :return: The title of this TypesPullReq.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this TypesPullReq.


        :param title: The title of this TypesPullReq.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def updated(self):
        """Gets the updated of this TypesPullReq.  # noqa: E501


        :return: The updated of this TypesPullReq.  # noqa: E501
        :rtype: int
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this TypesPullReq.


        :param updated: The updated of this TypesPullReq.  # noqa: E501
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
        if issubclass(TypesPullReq, dict):
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
        if not isinstance(other, TypesPullReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
