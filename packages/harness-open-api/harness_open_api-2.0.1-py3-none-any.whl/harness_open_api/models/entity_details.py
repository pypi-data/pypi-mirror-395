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

class EntityDetails(object):
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
        'branch': 'str',
        'entity_metadata': 'EntityMetadata',
        'entity_type': 'str',
        'entity_url': 'str',
        'error_metadata': 'ErrorMetadata1',
        'identifier': 'str',
        'is_valid': 'bool',
        'org': 'str',
        'project': 'str'
    }

    attribute_map = {
        'branch': 'branch',
        'entity_metadata': 'entity_metadata',
        'entity_type': 'entity_type',
        'entity_url': 'entity_url',
        'error_metadata': 'error_metadata',
        'identifier': 'identifier',
        'is_valid': 'is_valid',
        'org': 'org',
        'project': 'project'
    }

    def __init__(self, branch=None, entity_metadata=None, entity_type=None, entity_url=None, error_metadata=None, identifier=None, is_valid=None, org=None, project=None):  # noqa: E501
        """EntityDetails - a model defined in Swagger"""  # noqa: E501
        self._branch = None
        self._entity_metadata = None
        self._entity_type = None
        self._entity_url = None
        self._error_metadata = None
        self._identifier = None
        self._is_valid = None
        self._org = None
        self._project = None
        self.discriminator = None
        if branch is not None:
            self.branch = branch
        if entity_metadata is not None:
            self.entity_metadata = entity_metadata
        if entity_type is not None:
            self.entity_type = entity_type
        if entity_url is not None:
            self.entity_url = entity_url
        if error_metadata is not None:
            self.error_metadata = error_metadata
        if identifier is not None:
            self.identifier = identifier
        if is_valid is not None:
            self.is_valid = is_valid
        if org is not None:
            self.org = org
        if project is not None:
            self.project = project

    @property
    def branch(self):
        """Gets the branch of this EntityDetails.  # noqa: E501


        :return: The branch of this EntityDetails.  # noqa: E501
        :rtype: str
        """
        return self._branch

    @branch.setter
    def branch(self, branch):
        """Sets the branch of this EntityDetails.


        :param branch: The branch of this EntityDetails.  # noqa: E501
        :type: str
        """

        self._branch = branch

    @property
    def entity_metadata(self):
        """Gets the entity_metadata of this EntityDetails.  # noqa: E501


        :return: The entity_metadata of this EntityDetails.  # noqa: E501
        :rtype: EntityMetadata
        """
        return self._entity_metadata

    @entity_metadata.setter
    def entity_metadata(self, entity_metadata):
        """Sets the entity_metadata of this EntityDetails.


        :param entity_metadata: The entity_metadata of this EntityDetails.  # noqa: E501
        :type: EntityMetadata
        """

        self._entity_metadata = entity_metadata

    @property
    def entity_type(self):
        """Gets the entity_type of this EntityDetails.  # noqa: E501


        :return: The entity_type of this EntityDetails.  # noqa: E501
        :rtype: str
        """
        return self._entity_type

    @entity_type.setter
    def entity_type(self, entity_type):
        """Sets the entity_type of this EntityDetails.


        :param entity_type: The entity_type of this EntityDetails.  # noqa: E501
        :type: str
        """
        allowed_values = ["Pipelines", "Template", "InputSets", "Service", "Environment", "Infrastructure", "Overrides", "Unknown"]  # noqa: E501
        if entity_type not in allowed_values:
            raise ValueError(
                "Invalid value for `entity_type` ({0}), must be one of {1}"  # noqa: E501
                .format(entity_type, allowed_values)
            )

        self._entity_type = entity_type

    @property
    def entity_url(self):
        """Gets the entity_url of this EntityDetails.  # noqa: E501


        :return: The entity_url of this EntityDetails.  # noqa: E501
        :rtype: str
        """
        return self._entity_url

    @entity_url.setter
    def entity_url(self, entity_url):
        """Sets the entity_url of this EntityDetails.


        :param entity_url: The entity_url of this EntityDetails.  # noqa: E501
        :type: str
        """

        self._entity_url = entity_url

    @property
    def error_metadata(self):
        """Gets the error_metadata of this EntityDetails.  # noqa: E501


        :return: The error_metadata of this EntityDetails.  # noqa: E501
        :rtype: ErrorMetadata1
        """
        return self._error_metadata

    @error_metadata.setter
    def error_metadata(self, error_metadata):
        """Sets the error_metadata of this EntityDetails.


        :param error_metadata: The error_metadata of this EntityDetails.  # noqa: E501
        :type: ErrorMetadata1
        """

        self._error_metadata = error_metadata

    @property
    def identifier(self):
        """Gets the identifier of this EntityDetails.  # noqa: E501


        :return: The identifier of this EntityDetails.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this EntityDetails.


        :param identifier: The identifier of this EntityDetails.  # noqa: E501
        :type: str
        """

        self._identifier = identifier

    @property
    def is_valid(self):
        """Gets the is_valid of this EntityDetails.  # noqa: E501


        :return: The is_valid of this EntityDetails.  # noqa: E501
        :rtype: bool
        """
        return self._is_valid

    @is_valid.setter
    def is_valid(self, is_valid):
        """Sets the is_valid of this EntityDetails.


        :param is_valid: The is_valid of this EntityDetails.  # noqa: E501
        :type: bool
        """

        self._is_valid = is_valid

    @property
    def org(self):
        """Gets the org of this EntityDetails.  # noqa: E501


        :return: The org of this EntityDetails.  # noqa: E501
        :rtype: str
        """
        return self._org

    @org.setter
    def org(self, org):
        """Sets the org of this EntityDetails.


        :param org: The org of this EntityDetails.  # noqa: E501
        :type: str
        """

        self._org = org

    @property
    def project(self):
        """Gets the project of this EntityDetails.  # noqa: E501


        :return: The project of this EntityDetails.  # noqa: E501
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this EntityDetails.


        :param project: The project of this EntityDetails.  # noqa: E501
        :type: str
        """

        self._project = project

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
        if issubclass(EntityDetails, dict):
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
        if not isinstance(other, EntityDetails):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
