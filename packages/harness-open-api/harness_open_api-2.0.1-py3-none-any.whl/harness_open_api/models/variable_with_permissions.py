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

class VariableWithPermissions(object):
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
        'associated_template': 'str',
        'associated_variable_set': 'str',
        'created': 'int',
        'in_use': 'bool',
        'include_in_workspace': 'bool',
        'is_locked': 'bool',
        'key': 'str',
        'kind': 'str',
        'permissions': 'VariablePermissions',
        'source': 'str',
        'updated': 'int',
        'uuid': 'str',
        'value': 'str',
        'value_type': 'str'
    }

    attribute_map = {
        'associated_template': 'associatedTemplate',
        'associated_variable_set': 'associatedVariableSet',
        'created': 'created',
        'in_use': 'inUse',
        'include_in_workspace': 'includeInWorkspace',
        'is_locked': 'isLocked',
        'key': 'key',
        'kind': 'kind',
        'permissions': 'permissions',
        'source': 'source',
        'updated': 'updated',
        'uuid': 'uuid',
        'value': 'value',
        'value_type': 'value_type'
    }

    def __init__(self, associated_template=None, associated_variable_set=None, created=None, in_use=None, include_in_workspace=None, is_locked=None, key=None, kind=None, permissions=None, source=None, updated=None, uuid=None, value=None, value_type=None):  # noqa: E501
        """VariableWithPermissions - a model defined in Swagger"""  # noqa: E501
        self._associated_template = None
        self._associated_variable_set = None
        self._created = None
        self._in_use = None
        self._include_in_workspace = None
        self._is_locked = None
        self._key = None
        self._kind = None
        self._permissions = None
        self._source = None
        self._updated = None
        self._uuid = None
        self._value = None
        self._value_type = None
        self.discriminator = None
        if associated_template is not None:
            self.associated_template = associated_template
        if associated_variable_set is not None:
            self.associated_variable_set = associated_variable_set
        self.created = created
        self.in_use = in_use
        self.include_in_workspace = include_in_workspace
        self.is_locked = is_locked
        self.key = key
        self.kind = kind
        self.permissions = permissions
        self.source = source
        self.updated = updated
        self.uuid = uuid
        self.value = value
        self.value_type = value_type

    @property
    def associated_template(self):
        """Gets the associated_template of this VariableWithPermissions.  # noqa: E501


        :return: The associated_template of this VariableWithPermissions.  # noqa: E501
        :rtype: str
        """
        return self._associated_template

    @associated_template.setter
    def associated_template(self, associated_template):
        """Sets the associated_template of this VariableWithPermissions.


        :param associated_template: The associated_template of this VariableWithPermissions.  # noqa: E501
        :type: str
        """

        self._associated_template = associated_template

    @property
    def associated_variable_set(self):
        """Gets the associated_variable_set of this VariableWithPermissions.  # noqa: E501


        :return: The associated_variable_set of this VariableWithPermissions.  # noqa: E501
        :rtype: str
        """
        return self._associated_variable_set

    @associated_variable_set.setter
    def associated_variable_set(self, associated_variable_set):
        """Sets the associated_variable_set of this VariableWithPermissions.


        :param associated_variable_set: The associated_variable_set of this VariableWithPermissions.  # noqa: E501
        :type: str
        """

        self._associated_variable_set = associated_variable_set

    @property
    def created(self):
        """Gets the created of this VariableWithPermissions.  # noqa: E501


        :return: The created of this VariableWithPermissions.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this VariableWithPermissions.


        :param created: The created of this VariableWithPermissions.  # noqa: E501
        :type: int
        """
        if created is None:
            raise ValueError("Invalid value for `created`, must not be `None`")  # noqa: E501

        self._created = created

    @property
    def in_use(self):
        """Gets the in_use of this VariableWithPermissions.  # noqa: E501

        Indicates if this variable is the one actively used in the workspace  # noqa: E501

        :return: The in_use of this VariableWithPermissions.  # noqa: E501
        :rtype: bool
        """
        return self._in_use

    @in_use.setter
    def in_use(self, in_use):
        """Sets the in_use of this VariableWithPermissions.

        Indicates if this variable is the one actively used in the workspace  # noqa: E501

        :param in_use: The in_use of this VariableWithPermissions.  # noqa: E501
        :type: bool
        """
        if in_use is None:
            raise ValueError("Invalid value for `in_use`, must not be `None`")  # noqa: E501

        self._in_use = in_use

    @property
    def include_in_workspace(self):
        """Gets the include_in_workspace of this VariableWithPermissions.  # noqa: E501


        :return: The include_in_workspace of this VariableWithPermissions.  # noqa: E501
        :rtype: bool
        """
        return self._include_in_workspace

    @include_in_workspace.setter
    def include_in_workspace(self, include_in_workspace):
        """Sets the include_in_workspace of this VariableWithPermissions.


        :param include_in_workspace: The include_in_workspace of this VariableWithPermissions.  # noqa: E501
        :type: bool
        """
        if include_in_workspace is None:
            raise ValueError("Invalid value for `include_in_workspace`, must not be `None`")  # noqa: E501

        self._include_in_workspace = include_in_workspace

    @property
    def is_locked(self):
        """Gets the is_locked of this VariableWithPermissions.  # noqa: E501


        :return: The is_locked of this VariableWithPermissions.  # noqa: E501
        :rtype: bool
        """
        return self._is_locked

    @is_locked.setter
    def is_locked(self, is_locked):
        """Sets the is_locked of this VariableWithPermissions.


        :param is_locked: The is_locked of this VariableWithPermissions.  # noqa: E501
        :type: bool
        """
        if is_locked is None:
            raise ValueError("Invalid value for `is_locked`, must not be `None`")  # noqa: E501

        self._is_locked = is_locked

    @property
    def key(self):
        """Gets the key of this VariableWithPermissions.  # noqa: E501


        :return: The key of this VariableWithPermissions.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this VariableWithPermissions.


        :param key: The key of this VariableWithPermissions.  # noqa: E501
        :type: str
        """
        if key is None:
            raise ValueError("Invalid value for `key`, must not be `None`")  # noqa: E501

        self._key = key

    @property
    def kind(self):
        """Gets the kind of this VariableWithPermissions.  # noqa: E501


        :return: The kind of this VariableWithPermissions.  # noqa: E501
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this VariableWithPermissions.


        :param kind: The kind of this VariableWithPermissions.  # noqa: E501
        :type: str
        """
        if kind is None:
            raise ValueError("Invalid value for `kind`, must not be `None`")  # noqa: E501

        self._kind = kind

    @property
    def permissions(self):
        """Gets the permissions of this VariableWithPermissions.  # noqa: E501


        :return: The permissions of this VariableWithPermissions.  # noqa: E501
        :rtype: VariablePermissions
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """Sets the permissions of this VariableWithPermissions.


        :param permissions: The permissions of this VariableWithPermissions.  # noqa: E501
        :type: VariablePermissions
        """
        if permissions is None:
            raise ValueError("Invalid value for `permissions`, must not be `None`")  # noqa: E501

        self._permissions = permissions

    @property
    def source(self):
        """Gets the source of this VariableWithPermissions.  # noqa: E501


        :return: The source of this VariableWithPermissions.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this VariableWithPermissions.


        :param source: The source of this VariableWithPermissions.  # noqa: E501
        :type: str
        """
        if source is None:
            raise ValueError("Invalid value for `source`, must not be `None`")  # noqa: E501
        allowed_values = ["workspace", "template", "variableSet"]  # noqa: E501
        if source not in allowed_values:
            raise ValueError(
                "Invalid value for `source` ({0}), must be one of {1}"  # noqa: E501
                .format(source, allowed_values)
            )

        self._source = source

    @property
    def updated(self):
        """Gets the updated of this VariableWithPermissions.  # noqa: E501


        :return: The updated of this VariableWithPermissions.  # noqa: E501
        :rtype: int
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this VariableWithPermissions.


        :param updated: The updated of this VariableWithPermissions.  # noqa: E501
        :type: int
        """
        if updated is None:
            raise ValueError("Invalid value for `updated`, must not be `None`")  # noqa: E501

        self._updated = updated

    @property
    def uuid(self):
        """Gets the uuid of this VariableWithPermissions.  # noqa: E501

        Unique identifier for this variable  # noqa: E501

        :return: The uuid of this VariableWithPermissions.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this VariableWithPermissions.

        Unique identifier for this variable  # noqa: E501

        :param uuid: The uuid of this VariableWithPermissions.  # noqa: E501
        :type: str
        """
        if uuid is None:
            raise ValueError("Invalid value for `uuid`, must not be `None`")  # noqa: E501

        self._uuid = uuid

    @property
    def value(self):
        """Gets the value of this VariableWithPermissions.  # noqa: E501


        :return: The value of this VariableWithPermissions.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this VariableWithPermissions.


        :param value: The value of this VariableWithPermissions.  # noqa: E501
        :type: str
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501

        self._value = value

    @property
    def value_type(self):
        """Gets the value_type of this VariableWithPermissions.  # noqa: E501


        :return: The value_type of this VariableWithPermissions.  # noqa: E501
        :rtype: str
        """
        return self._value_type

    @value_type.setter
    def value_type(self, value_type):
        """Sets the value_type of this VariableWithPermissions.


        :param value_type: The value_type of this VariableWithPermissions.  # noqa: E501
        :type: str
        """
        if value_type is None:
            raise ValueError("Invalid value for `value_type`, must not be `None`")  # noqa: E501

        self._value_type = value_type

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
        if issubclass(VariableWithPermissions, dict):
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
        if not isinstance(other, VariableWithPermissions):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
