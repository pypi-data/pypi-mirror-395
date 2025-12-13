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

class OrgUsersBody(object):
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
        'additional_fields': 'object',
        'created_at': 'int',
        'dynamic_column_aggs_region': 'str',
        'email': 'str',
        'full_name': 'str',
        'id': 'str',
        'integration_user_ids': 'list[object]',
        'org_uuid': 'str',
        'updated_at': 'int',
        'version': 'str'
    }

    attribute_map = {
        'additional_fields': 'additional_fields',
        'created_at': 'created_at',
        'dynamic_column_aggs_region': 'dynamic_column_aggs_region',
        'email': 'email',
        'full_name': 'full_name',
        'id': 'id',
        'integration_user_ids': 'integration_user_ids',
        'org_uuid': 'org_uuid',
        'updated_at': 'updated_at',
        'version': 'version'
    }

    def __init__(self, additional_fields=None, created_at=None, dynamic_column_aggs_region=None, email=None, full_name=None, id=None, integration_user_ids=None, org_uuid=None, updated_at=None, version=None):  # noqa: E501
        """OrgUsersBody - a model defined in Swagger"""  # noqa: E501
        self._additional_fields = None
        self._created_at = None
        self._dynamic_column_aggs_region = None
        self._email = None
        self._full_name = None
        self._id = None
        self._integration_user_ids = None
        self._org_uuid = None
        self._updated_at = None
        self._version = None
        self.discriminator = None
        if additional_fields is not None:
            self.additional_fields = additional_fields
        if created_at is not None:
            self.created_at = created_at
        if dynamic_column_aggs_region is not None:
            self.dynamic_column_aggs_region = dynamic_column_aggs_region
        if email is not None:
            self.email = email
        if full_name is not None:
            self.full_name = full_name
        if id is not None:
            self.id = id
        if integration_user_ids is not None:
            self.integration_user_ids = integration_user_ids
        if org_uuid is not None:
            self.org_uuid = org_uuid
        if updated_at is not None:
            self.updated_at = updated_at
        if version is not None:
            self.version = version

    @property
    def additional_fields(self):
        """Gets the additional_fields of this OrgUsersBody.  # noqa: E501

        An object containing additional fields for the contributor (based on the schema).  # noqa: E501

        :return: The additional_fields of this OrgUsersBody.  # noqa: E501
        :rtype: object
        """
        return self._additional_fields

    @additional_fields.setter
    def additional_fields(self, additional_fields):
        """Sets the additional_fields of this OrgUsersBody.

        An object containing additional fields for the contributor (based on the schema).  # noqa: E501

        :param additional_fields: The additional_fields of this OrgUsersBody.  # noqa: E501
        :type: object
        """

        self._additional_fields = additional_fields

    @property
    def created_at(self):
        """Gets the created_at of this OrgUsersBody.  # noqa: E501

        The timestamp when the contributor record was created (in milliseconds).  # noqa: E501

        :return: The created_at of this OrgUsersBody.  # noqa: E501
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this OrgUsersBody.

        The timestamp when the contributor record was created (in milliseconds).  # noqa: E501

        :param created_at: The created_at of this OrgUsersBody.  # noqa: E501
        :type: int
        """

        self._created_at = created_at

    @property
    def dynamic_column_aggs_region(self):
        """Gets the dynamic_column_aggs_region of this OrgUsersBody.  # noqa: E501

        A dynamic field for region aggregation.  # noqa: E501

        :return: The dynamic_column_aggs_region of this OrgUsersBody.  # noqa: E501
        :rtype: str
        """
        return self._dynamic_column_aggs_region

    @dynamic_column_aggs_region.setter
    def dynamic_column_aggs_region(self, dynamic_column_aggs_region):
        """Sets the dynamic_column_aggs_region of this OrgUsersBody.

        A dynamic field for region aggregation.  # noqa: E501

        :param dynamic_column_aggs_region: The dynamic_column_aggs_region of this OrgUsersBody.  # noqa: E501
        :type: str
        """

        self._dynamic_column_aggs_region = dynamic_column_aggs_region

    @property
    def email(self):
        """Gets the email of this OrgUsersBody.  # noqa: E501

        The updated email address of the contributor.  # noqa: E501

        :return: The email of this OrgUsersBody.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this OrgUsersBody.

        The updated email address of the contributor.  # noqa: E501

        :param email: The email of this OrgUsersBody.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def full_name(self):
        """Gets the full_name of this OrgUsersBody.  # noqa: E501

        The updated full name of the contributor.  # noqa: E501

        :return: The full_name of this OrgUsersBody.  # noqa: E501
        :rtype: str
        """
        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        """Sets the full_name of this OrgUsersBody.

        The updated full name of the contributor.  # noqa: E501

        :param full_name: The full_name of this OrgUsersBody.  # noqa: E501
        :type: str
        """

        self._full_name = full_name

    @property
    def id(self):
        """Gets the id of this OrgUsersBody.  # noqa: E501

        The unique identifier of the contributor.  # noqa: E501

        :return: The id of this OrgUsersBody.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OrgUsersBody.

        The unique identifier of the contributor.  # noqa: E501

        :param id: The id of this OrgUsersBody.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def integration_user_ids(self):
        """Gets the integration_user_ids of this OrgUsersBody.  # noqa: E501

        An array of objects representing the integration user IDs associated with the contributor.  # noqa: E501

        :return: The integration_user_ids of this OrgUsersBody.  # noqa: E501
        :rtype: list[object]
        """
        return self._integration_user_ids

    @integration_user_ids.setter
    def integration_user_ids(self, integration_user_ids):
        """Sets the integration_user_ids of this OrgUsersBody.

        An array of objects representing the integration user IDs associated with the contributor.  # noqa: E501

        :param integration_user_ids: The integration_user_ids of this OrgUsersBody.  # noqa: E501
        :type: list[object]
        """

        self._integration_user_ids = integration_user_ids

    @property
    def org_uuid(self):
        """Gets the org_uuid of this OrgUsersBody.  # noqa: E501

        The UUID of the Collection the contributor belongs to.  # noqa: E501

        :return: The org_uuid of this OrgUsersBody.  # noqa: E501
        :rtype: str
        """
        return self._org_uuid

    @org_uuid.setter
    def org_uuid(self, org_uuid):
        """Sets the org_uuid of this OrgUsersBody.

        The UUID of the Collection the contributor belongs to.  # noqa: E501

        :param org_uuid: The org_uuid of this OrgUsersBody.  # noqa: E501
        :type: str
        """

        self._org_uuid = org_uuid

    @property
    def updated_at(self):
        """Gets the updated_at of this OrgUsersBody.  # noqa: E501

        The timestamp when the contributor record was last updated (in milliseconds).  # noqa: E501

        :return: The updated_at of this OrgUsersBody.  # noqa: E501
        :rtype: int
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this OrgUsersBody.

        The timestamp when the contributor record was last updated (in milliseconds).  # noqa: E501

        :param updated_at: The updated_at of this OrgUsersBody.  # noqa: E501
        :type: int
        """

        self._updated_at = updated_at

    @property
    def version(self):
        """Gets the version of this OrgUsersBody.  # noqa: E501

        The version of the contributor record.  # noqa: E501

        :return: The version of this OrgUsersBody.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this OrgUsersBody.

        The version of the contributor record.  # noqa: E501

        :param version: The version of this OrgUsersBody.  # noqa: E501
        :type: str
        """

        self._version = version

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
        if issubclass(OrgUsersBody, dict):
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
        if not isinstance(other, OrgUsersBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
