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

class DBSchemaOut(object):
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
        'change_log_script': 'ChangeLogScript',
        'changelog': 'Changelog',
        'created': 'int',
        'identifier': 'str',
        'instance_count': 'int',
        'migration_type': 'MigrationType',
        'name': 'str',
        'parent_id': 'str',
        'primary_db_instance_id': 'str',
        'schema_source_type': 'str',
        'service': 'str',
        'tags': 'dict(str, str)',
        'type': 'DBSchemaType',
        'updated': 'int'
    }

    attribute_map = {
        'change_log_script': 'changeLogScript',
        'changelog': 'changelog',
        'created': 'created',
        'identifier': 'identifier',
        'instance_count': 'instanceCount',
        'migration_type': 'migrationType',
        'name': 'name',
        'parent_id': 'parentId',
        'primary_db_instance_id': 'primaryDbInstanceId',
        'schema_source_type': 'schemaSourceType',
        'service': 'service',
        'tags': 'tags',
        'type': 'type',
        'updated': 'updated'
    }

    def __init__(self, change_log_script=None, changelog=None, created=None, identifier=None, instance_count=None, migration_type=None, name=None, parent_id=None, primary_db_instance_id=None, schema_source_type=None, service=None, tags=None, type=None, updated=None):  # noqa: E501
        """DBSchemaOut - a model defined in Swagger"""  # noqa: E501
        self._change_log_script = None
        self._changelog = None
        self._created = None
        self._identifier = None
        self._instance_count = None
        self._migration_type = None
        self._name = None
        self._parent_id = None
        self._primary_db_instance_id = None
        self._schema_source_type = None
        self._service = None
        self._tags = None
        self._type = None
        self._updated = None
        self.discriminator = None
        if change_log_script is not None:
            self.change_log_script = change_log_script
        if changelog is not None:
            self.changelog = changelog
        self.created = created
        self.identifier = identifier
        self.instance_count = instance_count
        self.migration_type = migration_type
        self.name = name
        self.parent_id = parent_id
        if primary_db_instance_id is not None:
            self.primary_db_instance_id = primary_db_instance_id
        if schema_source_type is not None:
            self.schema_source_type = schema_source_type
        if service is not None:
            self.service = service
        if tags is not None:
            self.tags = tags
        self.type = type
        if updated is not None:
            self.updated = updated

    @property
    def change_log_script(self):
        """Gets the change_log_script of this DBSchemaOut.  # noqa: E501


        :return: The change_log_script of this DBSchemaOut.  # noqa: E501
        :rtype: ChangeLogScript
        """
        return self._change_log_script

    @change_log_script.setter
    def change_log_script(self, change_log_script):
        """Sets the change_log_script of this DBSchemaOut.


        :param change_log_script: The change_log_script of this DBSchemaOut.  # noqa: E501
        :type: ChangeLogScript
        """

        self._change_log_script = change_log_script

    @property
    def changelog(self):
        """Gets the changelog of this DBSchemaOut.  # noqa: E501


        :return: The changelog of this DBSchemaOut.  # noqa: E501
        :rtype: Changelog
        """
        return self._changelog

    @changelog.setter
    def changelog(self, changelog):
        """Sets the changelog of this DBSchemaOut.


        :param changelog: The changelog of this DBSchemaOut.  # noqa: E501
        :type: Changelog
        """

        self._changelog = changelog

    @property
    def created(self):
        """Gets the created of this DBSchemaOut.  # noqa: E501

        epoch seconds when the database schema was created  # noqa: E501

        :return: The created of this DBSchemaOut.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this DBSchemaOut.

        epoch seconds when the database schema was created  # noqa: E501

        :param created: The created of this DBSchemaOut.  # noqa: E501
        :type: int
        """
        if created is None:
            raise ValueError("Invalid value for `created`, must not be `None`")  # noqa: E501

        self._created = created

    @property
    def identifier(self):
        """Gets the identifier of this DBSchemaOut.  # noqa: E501

        identifier of the database schema  # noqa: E501

        :return: The identifier of this DBSchemaOut.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this DBSchemaOut.

        identifier of the database schema  # noqa: E501

        :param identifier: The identifier of this DBSchemaOut.  # noqa: E501
        :type: str
        """
        if identifier is None:
            raise ValueError("Invalid value for `identifier`, must not be `None`")  # noqa: E501

        self._identifier = identifier

    @property
    def instance_count(self):
        """Gets the instance_count of this DBSchemaOut.  # noqa: E501

        number of database instances corresponding to database schema  # noqa: E501

        :return: The instance_count of this DBSchemaOut.  # noqa: E501
        :rtype: int
        """
        return self._instance_count

    @instance_count.setter
    def instance_count(self, instance_count):
        """Sets the instance_count of this DBSchemaOut.

        number of database instances corresponding to database schema  # noqa: E501

        :param instance_count: The instance_count of this DBSchemaOut.  # noqa: E501
        :type: int
        """
        if instance_count is None:
            raise ValueError("Invalid value for `instance_count`, must not be `None`")  # noqa: E501

        self._instance_count = instance_count

    @property
    def migration_type(self):
        """Gets the migration_type of this DBSchemaOut.  # noqa: E501


        :return: The migration_type of this DBSchemaOut.  # noqa: E501
        :rtype: MigrationType
        """
        return self._migration_type

    @migration_type.setter
    def migration_type(self, migration_type):
        """Sets the migration_type of this DBSchemaOut.


        :param migration_type: The migration_type of this DBSchemaOut.  # noqa: E501
        :type: MigrationType
        """
        if migration_type is None:
            raise ValueError("Invalid value for `migration_type`, must not be `None`")  # noqa: E501

        self._migration_type = migration_type

    @property
    def name(self):
        """Gets the name of this DBSchemaOut.  # noqa: E501

        name of the database schema  # noqa: E501

        :return: The name of this DBSchemaOut.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DBSchemaOut.

        name of the database schema  # noqa: E501

        :param name: The name of this DBSchemaOut.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def parent_id(self):
        """Gets the parent_id of this DBSchemaOut.  # noqa: E501

        parentUniqueId for scope schema belongs to  # noqa: E501

        :return: The parent_id of this DBSchemaOut.  # noqa: E501
        :rtype: str
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """Sets the parent_id of this DBSchemaOut.

        parentUniqueId for scope schema belongs to  # noqa: E501

        :param parent_id: The parent_id of this DBSchemaOut.  # noqa: E501
        :type: str
        """
        if parent_id is None:
            raise ValueError("Invalid value for `parent_id`, must not be `None`")  # noqa: E501

        self._parent_id = parent_id

    @property
    def primary_db_instance_id(self):
        """Gets the primary_db_instance_id of this DBSchemaOut.  # noqa: E501

        Identifier for the primary dbInstance used for advanced feature like LLM Authoring etc.  # noqa: E501

        :return: The primary_db_instance_id of this DBSchemaOut.  # noqa: E501
        :rtype: str
        """
        return self._primary_db_instance_id

    @primary_db_instance_id.setter
    def primary_db_instance_id(self, primary_db_instance_id):
        """Sets the primary_db_instance_id of this DBSchemaOut.

        Identifier for the primary dbInstance used for advanced feature like LLM Authoring etc.  # noqa: E501

        :param primary_db_instance_id: The primary_db_instance_id of this DBSchemaOut.  # noqa: E501
        :type: str
        """

        self._primary_db_instance_id = primary_db_instance_id

    @property
    def schema_source_type(self):
        """Gets the schema_source_type of this DBSchemaOut.  # noqa: E501


        :return: The schema_source_type of this DBSchemaOut.  # noqa: E501
        :rtype: str
        """
        return self._schema_source_type

    @schema_source_type.setter
    def schema_source_type(self, schema_source_type):
        """Sets the schema_source_type of this DBSchemaOut.


        :param schema_source_type: The schema_source_type of this DBSchemaOut.  # noqa: E501
        :type: str
        """
        allowed_values = ["Git", "Artifactory", "Custom"]  # noqa: E501
        if schema_source_type not in allowed_values:
            raise ValueError(
                "Invalid value for `schema_source_type` ({0}), must be one of {1}"  # noqa: E501
                .format(schema_source_type, allowed_values)
            )

        self._schema_source_type = schema_source_type

    @property
    def service(self):
        """Gets the service of this DBSchemaOut.  # noqa: E501

        harness service corresponding to database schema  # noqa: E501

        :return: The service of this DBSchemaOut.  # noqa: E501
        :rtype: str
        """
        return self._service

    @service.setter
    def service(self, service):
        """Sets the service of this DBSchemaOut.

        harness service corresponding to database schema  # noqa: E501

        :param service: The service of this DBSchemaOut.  # noqa: E501
        :type: str
        """

        self._service = service

    @property
    def tags(self):
        """Gets the tags of this DBSchemaOut.  # noqa: E501

        tags attached to the database schema  # noqa: E501

        :return: The tags of this DBSchemaOut.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this DBSchemaOut.

        tags attached to the database schema  # noqa: E501

        :param tags: The tags of this DBSchemaOut.  # noqa: E501
        :type: dict(str, str)
        """

        self._tags = tags

    @property
    def type(self):
        """Gets the type of this DBSchemaOut.  # noqa: E501


        :return: The type of this DBSchemaOut.  # noqa: E501
        :rtype: DBSchemaType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this DBSchemaOut.


        :param type: The type of this DBSchemaOut.  # noqa: E501
        :type: DBSchemaType
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def updated(self):
        """Gets the updated of this DBSchemaOut.  # noqa: E501

        epoch seconds when the database schema was last updated  # noqa: E501

        :return: The updated of this DBSchemaOut.  # noqa: E501
        :rtype: int
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this DBSchemaOut.

        epoch seconds when the database schema was last updated  # noqa: E501

        :param updated: The updated of this DBSchemaOut.  # noqa: E501
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
        if issubclass(DBSchemaOut, dict):
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
        if not isinstance(other, DBSchemaOut):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
