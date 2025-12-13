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

class TypesBranchExtended(object):
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
        'check_summary': 'TypesCheckCountSummary',
        'commit': 'TypesCommit',
        'commit_divergence': 'TypesCommitDivergence',
        'is_default': 'bool',
        'name': 'str',
        'pull_requests': 'list[TypesPullReq]',
        'rules': 'list[TypesRuleInfo]',
        'sha': 'ShaSHA'
    }

    attribute_map = {
        'check_summary': 'check_summary',
        'commit': 'commit',
        'commit_divergence': 'commit_divergence',
        'is_default': 'is_default',
        'name': 'name',
        'pull_requests': 'pull_requests',
        'rules': 'rules',
        'sha': 'sha'
    }

    def __init__(self, check_summary=None, commit=None, commit_divergence=None, is_default=None, name=None, pull_requests=None, rules=None, sha=None):  # noqa: E501
        """TypesBranchExtended - a model defined in Swagger"""  # noqa: E501
        self._check_summary = None
        self._commit = None
        self._commit_divergence = None
        self._is_default = None
        self._name = None
        self._pull_requests = None
        self._rules = None
        self._sha = None
        self.discriminator = None
        if check_summary is not None:
            self.check_summary = check_summary
        if commit is not None:
            self.commit = commit
        if commit_divergence is not None:
            self.commit_divergence = commit_divergence
        if is_default is not None:
            self.is_default = is_default
        if name is not None:
            self.name = name
        if pull_requests is not None:
            self.pull_requests = pull_requests
        if rules is not None:
            self.rules = rules
        if sha is not None:
            self.sha = sha

    @property
    def check_summary(self):
        """Gets the check_summary of this TypesBranchExtended.  # noqa: E501


        :return: The check_summary of this TypesBranchExtended.  # noqa: E501
        :rtype: TypesCheckCountSummary
        """
        return self._check_summary

    @check_summary.setter
    def check_summary(self, check_summary):
        """Sets the check_summary of this TypesBranchExtended.


        :param check_summary: The check_summary of this TypesBranchExtended.  # noqa: E501
        :type: TypesCheckCountSummary
        """

        self._check_summary = check_summary

    @property
    def commit(self):
        """Gets the commit of this TypesBranchExtended.  # noqa: E501


        :return: The commit of this TypesBranchExtended.  # noqa: E501
        :rtype: TypesCommit
        """
        return self._commit

    @commit.setter
    def commit(self, commit):
        """Sets the commit of this TypesBranchExtended.


        :param commit: The commit of this TypesBranchExtended.  # noqa: E501
        :type: TypesCommit
        """

        self._commit = commit

    @property
    def commit_divergence(self):
        """Gets the commit_divergence of this TypesBranchExtended.  # noqa: E501


        :return: The commit_divergence of this TypesBranchExtended.  # noqa: E501
        :rtype: TypesCommitDivergence
        """
        return self._commit_divergence

    @commit_divergence.setter
    def commit_divergence(self, commit_divergence):
        """Sets the commit_divergence of this TypesBranchExtended.


        :param commit_divergence: The commit_divergence of this TypesBranchExtended.  # noqa: E501
        :type: TypesCommitDivergence
        """

        self._commit_divergence = commit_divergence

    @property
    def is_default(self):
        """Gets the is_default of this TypesBranchExtended.  # noqa: E501


        :return: The is_default of this TypesBranchExtended.  # noqa: E501
        :rtype: bool
        """
        return self._is_default

    @is_default.setter
    def is_default(self, is_default):
        """Sets the is_default of this TypesBranchExtended.


        :param is_default: The is_default of this TypesBranchExtended.  # noqa: E501
        :type: bool
        """

        self._is_default = is_default

    @property
    def name(self):
        """Gets the name of this TypesBranchExtended.  # noqa: E501


        :return: The name of this TypesBranchExtended.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TypesBranchExtended.


        :param name: The name of this TypesBranchExtended.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def pull_requests(self):
        """Gets the pull_requests of this TypesBranchExtended.  # noqa: E501


        :return: The pull_requests of this TypesBranchExtended.  # noqa: E501
        :rtype: list[TypesPullReq]
        """
        return self._pull_requests

    @pull_requests.setter
    def pull_requests(self, pull_requests):
        """Sets the pull_requests of this TypesBranchExtended.


        :param pull_requests: The pull_requests of this TypesBranchExtended.  # noqa: E501
        :type: list[TypesPullReq]
        """

        self._pull_requests = pull_requests

    @property
    def rules(self):
        """Gets the rules of this TypesBranchExtended.  # noqa: E501


        :return: The rules of this TypesBranchExtended.  # noqa: E501
        :rtype: list[TypesRuleInfo]
        """
        return self._rules

    @rules.setter
    def rules(self, rules):
        """Sets the rules of this TypesBranchExtended.


        :param rules: The rules of this TypesBranchExtended.  # noqa: E501
        :type: list[TypesRuleInfo]
        """

        self._rules = rules

    @property
    def sha(self):
        """Gets the sha of this TypesBranchExtended.  # noqa: E501


        :return: The sha of this TypesBranchExtended.  # noqa: E501
        :rtype: ShaSHA
        """
        return self._sha

    @sha.setter
    def sha(self, sha):
        """Sets the sha of this TypesBranchExtended.


        :param sha: The sha of this TypesBranchExtended.  # noqa: E501
        :type: ShaSHA
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
        if issubclass(TypesBranchExtended, dict):
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
        if not isinstance(other, TypesBranchExtended):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
