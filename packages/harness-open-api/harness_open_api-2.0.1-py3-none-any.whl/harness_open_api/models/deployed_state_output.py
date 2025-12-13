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

class DeployedStateOutput(object):
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
        'author': 'str',
        'change_set_fqn': 'str',
        'change_set_id': 'str',
        'command': 'Command',
        'comment': 'str',
        'deployed_at': 'int',
        'deployed_in_current_execution': 'bool',
        'file_name': 'str',
        'label': 'str',
        'metadata': 'DbOpsExecutionMetadata',
        'status': 'CommandExecutionStatus',
        'tag': 'str'
    }

    attribute_map = {
        'author': 'author',
        'change_set_fqn': 'changeSetFQN',
        'change_set_id': 'changeSetId',
        'command': 'command',
        'comment': 'comment',
        'deployed_at': 'deployedAt',
        'deployed_in_current_execution': 'deployedInCurrentExecution',
        'file_name': 'fileName',
        'label': 'label',
        'metadata': 'metadata',
        'status': 'status',
        'tag': 'tag'
    }

    def __init__(self, author=None, change_set_fqn=None, change_set_id=None, command=None, comment=None, deployed_at=None, deployed_in_current_execution=None, file_name=None, label=None, metadata=None, status=None, tag=None):  # noqa: E501
        """DeployedStateOutput - a model defined in Swagger"""  # noqa: E501
        self._author = None
        self._change_set_fqn = None
        self._change_set_id = None
        self._command = None
        self._comment = None
        self._deployed_at = None
        self._deployed_in_current_execution = None
        self._file_name = None
        self._label = None
        self._metadata = None
        self._status = None
        self._tag = None
        self.discriminator = None
        self.author = author
        self.change_set_fqn = change_set_fqn
        self.change_set_id = change_set_id
        self.command = command
        if comment is not None:
            self.comment = comment
        if deployed_at is not None:
            self.deployed_at = deployed_at
        self.deployed_in_current_execution = deployed_in_current_execution
        self.file_name = file_name
        if label is not None:
            self.label = label
        self.metadata = metadata
        self.status = status
        if tag is not None:
            self.tag = tag

    @property
    def author(self):
        """Gets the author of this DeployedStateOutput.  # noqa: E501


        :return: The author of this DeployedStateOutput.  # noqa: E501
        :rtype: str
        """
        return self._author

    @author.setter
    def author(self, author):
        """Sets the author of this DeployedStateOutput.


        :param author: The author of this DeployedStateOutput.  # noqa: E501
        :type: str
        """
        if author is None:
            raise ValueError("Invalid value for `author`, must not be `None`")  # noqa: E501

        self._author = author

    @property
    def change_set_fqn(self):
        """Gets the change_set_fqn of this DeployedStateOutput.  # noqa: E501

        changesetFQN is a unique identifier for database changesets in the format filename::changesetId::author  # noqa: E501

        :return: The change_set_fqn of this DeployedStateOutput.  # noqa: E501
        :rtype: str
        """
        return self._change_set_fqn

    @change_set_fqn.setter
    def change_set_fqn(self, change_set_fqn):
        """Sets the change_set_fqn of this DeployedStateOutput.

        changesetFQN is a unique identifier for database changesets in the format filename::changesetId::author  # noqa: E501

        :param change_set_fqn: The change_set_fqn of this DeployedStateOutput.  # noqa: E501
        :type: str
        """
        if change_set_fqn is None:
            raise ValueError("Invalid value for `change_set_fqn`, must not be `None`")  # noqa: E501

        self._change_set_fqn = change_set_fqn

    @property
    def change_set_id(self):
        """Gets the change_set_id of this DeployedStateOutput.  # noqa: E501


        :return: The change_set_id of this DeployedStateOutput.  # noqa: E501
        :rtype: str
        """
        return self._change_set_id

    @change_set_id.setter
    def change_set_id(self, change_set_id):
        """Sets the change_set_id of this DeployedStateOutput.


        :param change_set_id: The change_set_id of this DeployedStateOutput.  # noqa: E501
        :type: str
        """
        if change_set_id is None:
            raise ValueError("Invalid value for `change_set_id`, must not be `None`")  # noqa: E501

        self._change_set_id = change_set_id

    @property
    def command(self):
        """Gets the command of this DeployedStateOutput.  # noqa: E501


        :return: The command of this DeployedStateOutput.  # noqa: E501
        :rtype: Command
        """
        return self._command

    @command.setter
    def command(self, command):
        """Sets the command of this DeployedStateOutput.


        :param command: The command of this DeployedStateOutput.  # noqa: E501
        :type: Command
        """
        if command is None:
            raise ValueError("Invalid value for `command`, must not be `None`")  # noqa: E501

        self._command = command

    @property
    def comment(self):
        """Gets the comment of this DeployedStateOutput.  # noqa: E501

        comment in changeset definition  # noqa: E501

        :return: The comment of this DeployedStateOutput.  # noqa: E501
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this DeployedStateOutput.

        comment in changeset definition  # noqa: E501

        :param comment: The comment of this DeployedStateOutput.  # noqa: E501
        :type: str
        """

        self._comment = comment

    @property
    def deployed_at(self):
        """Gets the deployed_at of this DeployedStateOutput.  # noqa: E501


        :return: The deployed_at of this DeployedStateOutput.  # noqa: E501
        :rtype: int
        """
        return self._deployed_at

    @deployed_at.setter
    def deployed_at(self, deployed_at):
        """Sets the deployed_at of this DeployedStateOutput.


        :param deployed_at: The deployed_at of this DeployedStateOutput.  # noqa: E501
        :type: int
        """

        self._deployed_at = deployed_at

    @property
    def deployed_in_current_execution(self):
        """Gets the deployed_in_current_execution of this DeployedStateOutput.  # noqa: E501

        if changeset run as part of current step execution  # noqa: E501

        :return: The deployed_in_current_execution of this DeployedStateOutput.  # noqa: E501
        :rtype: bool
        """
        return self._deployed_in_current_execution

    @deployed_in_current_execution.setter
    def deployed_in_current_execution(self, deployed_in_current_execution):
        """Sets the deployed_in_current_execution of this DeployedStateOutput.

        if changeset run as part of current step execution  # noqa: E501

        :param deployed_in_current_execution: The deployed_in_current_execution of this DeployedStateOutput.  # noqa: E501
        :type: bool
        """
        if deployed_in_current_execution is None:
            raise ValueError("Invalid value for `deployed_in_current_execution`, must not be `None`")  # noqa: E501

        self._deployed_in_current_execution = deployed_in_current_execution

    @property
    def file_name(self):
        """Gets the file_name of this DeployedStateOutput.  # noqa: E501


        :return: The file_name of this DeployedStateOutput.  # noqa: E501
        :rtype: str
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        """Sets the file_name of this DeployedStateOutput.


        :param file_name: The file_name of this DeployedStateOutput.  # noqa: E501
        :type: str
        """
        if file_name is None:
            raise ValueError("Invalid value for `file_name`, must not be `None`")  # noqa: E501

        self._file_name = file_name

    @property
    def label(self):
        """Gets the label of this DeployedStateOutput.  # noqa: E501

        label in changeset definition  # noqa: E501

        :return: The label of this DeployedStateOutput.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this DeployedStateOutput.

        label in changeset definition  # noqa: E501

        :param label: The label of this DeployedStateOutput.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def metadata(self):
        """Gets the metadata of this DeployedStateOutput.  # noqa: E501


        :return: The metadata of this DeployedStateOutput.  # noqa: E501
        :rtype: DbOpsExecutionMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this DeployedStateOutput.


        :param metadata: The metadata of this DeployedStateOutput.  # noqa: E501
        :type: DbOpsExecutionMetadata
        """
        if metadata is None:
            raise ValueError("Invalid value for `metadata`, must not be `None`")  # noqa: E501

        self._metadata = metadata

    @property
    def status(self):
        """Gets the status of this DeployedStateOutput.  # noqa: E501


        :return: The status of this DeployedStateOutput.  # noqa: E501
        :rtype: CommandExecutionStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DeployedStateOutput.


        :param status: The status of this DeployedStateOutput.  # noqa: E501
        :type: CommandExecutionStatus
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def tag(self):
        """Gets the tag of this DeployedStateOutput.  # noqa: E501


        :return: The tag of this DeployedStateOutput.  # noqa: E501
        :rtype: str
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """Sets the tag of this DeployedStateOutput.


        :param tag: The tag of this DeployedStateOutput.  # noqa: E501
        :type: str
        """

        self._tag = tag

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
        if issubclass(DeployedStateOutput, dict):
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
        if not isinstance(other, DeployedStateOutput):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
