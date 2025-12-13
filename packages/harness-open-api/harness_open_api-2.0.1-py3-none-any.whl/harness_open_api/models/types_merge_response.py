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

class TypesMergeResponse(object):
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
        'allowed_methods': 'list[EnumMergeMethod]',
        'branch_deleted': 'bool',
        'conflict_files': 'list[str]',
        'default_reviewer_aprovals': 'list[TypesDefaultReviewerApprovalsResponse]',
        'dry_run': 'bool',
        'dry_run_rules': 'bool',
        'mergeable': 'bool',
        'minimum_required_approvals_count': 'int',
        'minimum_required_approvals_count_latest': 'int',
        'requires_code_owners_approval': 'bool',
        'requires_code_owners_approval_latest': 'bool',
        'requires_comment_resolution': 'bool',
        'requires_no_change_requests': 'bool',
        'rule_violations': 'list[TypesRuleViolations]',
        'sha': 'str'
    }

    attribute_map = {
        'allowed_methods': 'allowed_methods',
        'branch_deleted': 'branch_deleted',
        'conflict_files': 'conflict_files',
        'default_reviewer_aprovals': 'default_reviewer_aprovals',
        'dry_run': 'dry_run',
        'dry_run_rules': 'dry_run_rules',
        'mergeable': 'mergeable',
        'minimum_required_approvals_count': 'minimum_required_approvals_count',
        'minimum_required_approvals_count_latest': 'minimum_required_approvals_count_latest',
        'requires_code_owners_approval': 'requires_code_owners_approval',
        'requires_code_owners_approval_latest': 'requires_code_owners_approval_latest',
        'requires_comment_resolution': 'requires_comment_resolution',
        'requires_no_change_requests': 'requires_no_change_requests',
        'rule_violations': 'rule_violations',
        'sha': 'sha'
    }

    def __init__(self, allowed_methods=None, branch_deleted=None, conflict_files=None, default_reviewer_aprovals=None, dry_run=None, dry_run_rules=None, mergeable=None, minimum_required_approvals_count=None, minimum_required_approvals_count_latest=None, requires_code_owners_approval=None, requires_code_owners_approval_latest=None, requires_comment_resolution=None, requires_no_change_requests=None, rule_violations=None, sha=None):  # noqa: E501
        """TypesMergeResponse - a model defined in Swagger"""  # noqa: E501
        self._allowed_methods = None
        self._branch_deleted = None
        self._conflict_files = None
        self._default_reviewer_aprovals = None
        self._dry_run = None
        self._dry_run_rules = None
        self._mergeable = None
        self._minimum_required_approvals_count = None
        self._minimum_required_approvals_count_latest = None
        self._requires_code_owners_approval = None
        self._requires_code_owners_approval_latest = None
        self._requires_comment_resolution = None
        self._requires_no_change_requests = None
        self._rule_violations = None
        self._sha = None
        self.discriminator = None
        if allowed_methods is not None:
            self.allowed_methods = allowed_methods
        if branch_deleted is not None:
            self.branch_deleted = branch_deleted
        if conflict_files is not None:
            self.conflict_files = conflict_files
        if default_reviewer_aprovals is not None:
            self.default_reviewer_aprovals = default_reviewer_aprovals
        if dry_run is not None:
            self.dry_run = dry_run
        if dry_run_rules is not None:
            self.dry_run_rules = dry_run_rules
        if mergeable is not None:
            self.mergeable = mergeable
        if minimum_required_approvals_count is not None:
            self.minimum_required_approvals_count = minimum_required_approvals_count
        if minimum_required_approvals_count_latest is not None:
            self.minimum_required_approvals_count_latest = minimum_required_approvals_count_latest
        if requires_code_owners_approval is not None:
            self.requires_code_owners_approval = requires_code_owners_approval
        if requires_code_owners_approval_latest is not None:
            self.requires_code_owners_approval_latest = requires_code_owners_approval_latest
        if requires_comment_resolution is not None:
            self.requires_comment_resolution = requires_comment_resolution
        if requires_no_change_requests is not None:
            self.requires_no_change_requests = requires_no_change_requests
        if rule_violations is not None:
            self.rule_violations = rule_violations
        if sha is not None:
            self.sha = sha

    @property
    def allowed_methods(self):
        """Gets the allowed_methods of this TypesMergeResponse.  # noqa: E501


        :return: The allowed_methods of this TypesMergeResponse.  # noqa: E501
        :rtype: list[EnumMergeMethod]
        """
        return self._allowed_methods

    @allowed_methods.setter
    def allowed_methods(self, allowed_methods):
        """Sets the allowed_methods of this TypesMergeResponse.


        :param allowed_methods: The allowed_methods of this TypesMergeResponse.  # noqa: E501
        :type: list[EnumMergeMethod]
        """

        self._allowed_methods = allowed_methods

    @property
    def branch_deleted(self):
        """Gets the branch_deleted of this TypesMergeResponse.  # noqa: E501


        :return: The branch_deleted of this TypesMergeResponse.  # noqa: E501
        :rtype: bool
        """
        return self._branch_deleted

    @branch_deleted.setter
    def branch_deleted(self, branch_deleted):
        """Sets the branch_deleted of this TypesMergeResponse.


        :param branch_deleted: The branch_deleted of this TypesMergeResponse.  # noqa: E501
        :type: bool
        """

        self._branch_deleted = branch_deleted

    @property
    def conflict_files(self):
        """Gets the conflict_files of this TypesMergeResponse.  # noqa: E501


        :return: The conflict_files of this TypesMergeResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._conflict_files

    @conflict_files.setter
    def conflict_files(self, conflict_files):
        """Sets the conflict_files of this TypesMergeResponse.


        :param conflict_files: The conflict_files of this TypesMergeResponse.  # noqa: E501
        :type: list[str]
        """

        self._conflict_files = conflict_files

    @property
    def default_reviewer_aprovals(self):
        """Gets the default_reviewer_aprovals of this TypesMergeResponse.  # noqa: E501


        :return: The default_reviewer_aprovals of this TypesMergeResponse.  # noqa: E501
        :rtype: list[TypesDefaultReviewerApprovalsResponse]
        """
        return self._default_reviewer_aprovals

    @default_reviewer_aprovals.setter
    def default_reviewer_aprovals(self, default_reviewer_aprovals):
        """Sets the default_reviewer_aprovals of this TypesMergeResponse.


        :param default_reviewer_aprovals: The default_reviewer_aprovals of this TypesMergeResponse.  # noqa: E501
        :type: list[TypesDefaultReviewerApprovalsResponse]
        """

        self._default_reviewer_aprovals = default_reviewer_aprovals

    @property
    def dry_run(self):
        """Gets the dry_run of this TypesMergeResponse.  # noqa: E501


        :return: The dry_run of this TypesMergeResponse.  # noqa: E501
        :rtype: bool
        """
        return self._dry_run

    @dry_run.setter
    def dry_run(self, dry_run):
        """Sets the dry_run of this TypesMergeResponse.


        :param dry_run: The dry_run of this TypesMergeResponse.  # noqa: E501
        :type: bool
        """

        self._dry_run = dry_run

    @property
    def dry_run_rules(self):
        """Gets the dry_run_rules of this TypesMergeResponse.  # noqa: E501


        :return: The dry_run_rules of this TypesMergeResponse.  # noqa: E501
        :rtype: bool
        """
        return self._dry_run_rules

    @dry_run_rules.setter
    def dry_run_rules(self, dry_run_rules):
        """Sets the dry_run_rules of this TypesMergeResponse.


        :param dry_run_rules: The dry_run_rules of this TypesMergeResponse.  # noqa: E501
        :type: bool
        """

        self._dry_run_rules = dry_run_rules

    @property
    def mergeable(self):
        """Gets the mergeable of this TypesMergeResponse.  # noqa: E501


        :return: The mergeable of this TypesMergeResponse.  # noqa: E501
        :rtype: bool
        """
        return self._mergeable

    @mergeable.setter
    def mergeable(self, mergeable):
        """Sets the mergeable of this TypesMergeResponse.


        :param mergeable: The mergeable of this TypesMergeResponse.  # noqa: E501
        :type: bool
        """

        self._mergeable = mergeable

    @property
    def minimum_required_approvals_count(self):
        """Gets the minimum_required_approvals_count of this TypesMergeResponse.  # noqa: E501


        :return: The minimum_required_approvals_count of this TypesMergeResponse.  # noqa: E501
        :rtype: int
        """
        return self._minimum_required_approvals_count

    @minimum_required_approvals_count.setter
    def minimum_required_approvals_count(self, minimum_required_approvals_count):
        """Sets the minimum_required_approvals_count of this TypesMergeResponse.


        :param minimum_required_approvals_count: The minimum_required_approvals_count of this TypesMergeResponse.  # noqa: E501
        :type: int
        """

        self._minimum_required_approvals_count = minimum_required_approvals_count

    @property
    def minimum_required_approvals_count_latest(self):
        """Gets the minimum_required_approvals_count_latest of this TypesMergeResponse.  # noqa: E501


        :return: The minimum_required_approvals_count_latest of this TypesMergeResponse.  # noqa: E501
        :rtype: int
        """
        return self._minimum_required_approvals_count_latest

    @minimum_required_approvals_count_latest.setter
    def minimum_required_approvals_count_latest(self, minimum_required_approvals_count_latest):
        """Sets the minimum_required_approvals_count_latest of this TypesMergeResponse.


        :param minimum_required_approvals_count_latest: The minimum_required_approvals_count_latest of this TypesMergeResponse.  # noqa: E501
        :type: int
        """

        self._minimum_required_approvals_count_latest = minimum_required_approvals_count_latest

    @property
    def requires_code_owners_approval(self):
        """Gets the requires_code_owners_approval of this TypesMergeResponse.  # noqa: E501


        :return: The requires_code_owners_approval of this TypesMergeResponse.  # noqa: E501
        :rtype: bool
        """
        return self._requires_code_owners_approval

    @requires_code_owners_approval.setter
    def requires_code_owners_approval(self, requires_code_owners_approval):
        """Sets the requires_code_owners_approval of this TypesMergeResponse.


        :param requires_code_owners_approval: The requires_code_owners_approval of this TypesMergeResponse.  # noqa: E501
        :type: bool
        """

        self._requires_code_owners_approval = requires_code_owners_approval

    @property
    def requires_code_owners_approval_latest(self):
        """Gets the requires_code_owners_approval_latest of this TypesMergeResponse.  # noqa: E501


        :return: The requires_code_owners_approval_latest of this TypesMergeResponse.  # noqa: E501
        :rtype: bool
        """
        return self._requires_code_owners_approval_latest

    @requires_code_owners_approval_latest.setter
    def requires_code_owners_approval_latest(self, requires_code_owners_approval_latest):
        """Sets the requires_code_owners_approval_latest of this TypesMergeResponse.


        :param requires_code_owners_approval_latest: The requires_code_owners_approval_latest of this TypesMergeResponse.  # noqa: E501
        :type: bool
        """

        self._requires_code_owners_approval_latest = requires_code_owners_approval_latest

    @property
    def requires_comment_resolution(self):
        """Gets the requires_comment_resolution of this TypesMergeResponse.  # noqa: E501


        :return: The requires_comment_resolution of this TypesMergeResponse.  # noqa: E501
        :rtype: bool
        """
        return self._requires_comment_resolution

    @requires_comment_resolution.setter
    def requires_comment_resolution(self, requires_comment_resolution):
        """Sets the requires_comment_resolution of this TypesMergeResponse.


        :param requires_comment_resolution: The requires_comment_resolution of this TypesMergeResponse.  # noqa: E501
        :type: bool
        """

        self._requires_comment_resolution = requires_comment_resolution

    @property
    def requires_no_change_requests(self):
        """Gets the requires_no_change_requests of this TypesMergeResponse.  # noqa: E501


        :return: The requires_no_change_requests of this TypesMergeResponse.  # noqa: E501
        :rtype: bool
        """
        return self._requires_no_change_requests

    @requires_no_change_requests.setter
    def requires_no_change_requests(self, requires_no_change_requests):
        """Sets the requires_no_change_requests of this TypesMergeResponse.


        :param requires_no_change_requests: The requires_no_change_requests of this TypesMergeResponse.  # noqa: E501
        :type: bool
        """

        self._requires_no_change_requests = requires_no_change_requests

    @property
    def rule_violations(self):
        """Gets the rule_violations of this TypesMergeResponse.  # noqa: E501


        :return: The rule_violations of this TypesMergeResponse.  # noqa: E501
        :rtype: list[TypesRuleViolations]
        """
        return self._rule_violations

    @rule_violations.setter
    def rule_violations(self, rule_violations):
        """Sets the rule_violations of this TypesMergeResponse.


        :param rule_violations: The rule_violations of this TypesMergeResponse.  # noqa: E501
        :type: list[TypesRuleViolations]
        """

        self._rule_violations = rule_violations

    @property
    def sha(self):
        """Gets the sha of this TypesMergeResponse.  # noqa: E501


        :return: The sha of this TypesMergeResponse.  # noqa: E501
        :rtype: str
        """
        return self._sha

    @sha.setter
    def sha(self, sha):
        """Sets the sha of this TypesMergeResponse.


        :param sha: The sha of this TypesMergeResponse.  # noqa: E501
        :type: str
        """

        self._sha = sha

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
        if issubclass(TypesMergeResponse, dict):
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
        if not isinstance(other, TypesMergeResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
