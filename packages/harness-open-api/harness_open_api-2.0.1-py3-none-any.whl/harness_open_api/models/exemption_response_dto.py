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

class ExemptionResponseDTO(object):
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
        'account_id': 'str',
        'artifact_id': 'str',
        'component_name': 'str',
        'component_version': 'str',
        'created_at': 'int',
        'created_by_name': 'str',
        'created_by_user_id': 'str',
        'exemption_duration': 'ExemptionDurationDTO',
        'exemption_initiator': 'ExemptionInitiatorDTO',
        'exemption_status': 'ExemptionStatusDTO',
        'org_identifier': 'str',
        'project_identifier': 'str',
        'reason': 'str',
        'review_comment': 'str',
        'reviewed_at': 'int',
        'reviewed_by_name': 'str',
        'reviewed_by_user_id': 'str',
        'updated_at': 'int',
        'updated_by': 'str',
        'uuid': 'str',
        'valid_until': 'int',
        'version_operator': 'Operator'
    }

    attribute_map = {
        'account_id': 'account_id',
        'artifact_id': 'artifact_id',
        'component_name': 'component_name',
        'component_version': 'component_version',
        'created_at': 'created_at',
        'created_by_name': 'created_by_name',
        'created_by_user_id': 'created_by_user_id',
        'exemption_duration': 'exemption_duration',
        'exemption_initiator': 'exemption_initiator',
        'exemption_status': 'exemption_status',
        'org_identifier': 'org_identifier',
        'project_identifier': 'project_identifier',
        'reason': 'reason',
        'review_comment': 'review_comment',
        'reviewed_at': 'reviewed_at',
        'reviewed_by_name': 'reviewed_by_name',
        'reviewed_by_user_id': 'reviewed_by_user_id',
        'updated_at': 'updated_at',
        'updated_by': 'updated_by',
        'uuid': 'uuid',
        'valid_until': 'valid_until',
        'version_operator': 'version_operator'
    }

    def __init__(self, account_id=None, artifact_id=None, component_name=None, component_version=None, created_at=None, created_by_name=None, created_by_user_id=None, exemption_duration=None, exemption_initiator=None, exemption_status=None, org_identifier=None, project_identifier=None, reason=None, review_comment=None, reviewed_at=None, reviewed_by_name=None, reviewed_by_user_id=None, updated_at=None, updated_by=None, uuid=None, valid_until=None, version_operator=None):  # noqa: E501
        """ExemptionResponseDTO - a model defined in Swagger"""  # noqa: E501
        self._account_id = None
        self._artifact_id = None
        self._component_name = None
        self._component_version = None
        self._created_at = None
        self._created_by_name = None
        self._created_by_user_id = None
        self._exemption_duration = None
        self._exemption_initiator = None
        self._exemption_status = None
        self._org_identifier = None
        self._project_identifier = None
        self._reason = None
        self._review_comment = None
        self._reviewed_at = None
        self._reviewed_by_name = None
        self._reviewed_by_user_id = None
        self._updated_at = None
        self._updated_by = None
        self._uuid = None
        self._valid_until = None
        self._version_operator = None
        self.discriminator = None
        if account_id is not None:
            self.account_id = account_id
        if artifact_id is not None:
            self.artifact_id = artifact_id
        if component_name is not None:
            self.component_name = component_name
        if component_version is not None:
            self.component_version = component_version
        if created_at is not None:
            self.created_at = created_at
        if created_by_name is not None:
            self.created_by_name = created_by_name
        if created_by_user_id is not None:
            self.created_by_user_id = created_by_user_id
        if exemption_duration is not None:
            self.exemption_duration = exemption_duration
        if exemption_initiator is not None:
            self.exemption_initiator = exemption_initiator
        if exemption_status is not None:
            self.exemption_status = exemption_status
        if org_identifier is not None:
            self.org_identifier = org_identifier
        if project_identifier is not None:
            self.project_identifier = project_identifier
        if reason is not None:
            self.reason = reason
        if review_comment is not None:
            self.review_comment = review_comment
        if reviewed_at is not None:
            self.reviewed_at = reviewed_at
        if reviewed_by_name is not None:
            self.reviewed_by_name = reviewed_by_name
        if reviewed_by_user_id is not None:
            self.reviewed_by_user_id = reviewed_by_user_id
        if updated_at is not None:
            self.updated_at = updated_at
        if updated_by is not None:
            self.updated_by = updated_by
        if uuid is not None:
            self.uuid = uuid
        if valid_until is not None:
            self.valid_until = valid_until
        if version_operator is not None:
            self.version_operator = version_operator

    @property
    def account_id(self):
        """Gets the account_id of this ExemptionResponseDTO.  # noqa: E501


        :return: The account_id of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this ExemptionResponseDTO.


        :param account_id: The account_id of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._account_id = account_id

    @property
    def artifact_id(self):
        """Gets the artifact_id of this ExemptionResponseDTO.  # noqa: E501


        :return: The artifact_id of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._artifact_id

    @artifact_id.setter
    def artifact_id(self, artifact_id):
        """Sets the artifact_id of this ExemptionResponseDTO.


        :param artifact_id: The artifact_id of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._artifact_id = artifact_id

    @property
    def component_name(self):
        """Gets the component_name of this ExemptionResponseDTO.  # noqa: E501


        :return: The component_name of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._component_name

    @component_name.setter
    def component_name(self, component_name):
        """Sets the component_name of this ExemptionResponseDTO.


        :param component_name: The component_name of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._component_name = component_name

    @property
    def component_version(self):
        """Gets the component_version of this ExemptionResponseDTO.  # noqa: E501


        :return: The component_version of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._component_version

    @component_version.setter
    def component_version(self, component_version):
        """Sets the component_version of this ExemptionResponseDTO.


        :param component_version: The component_version of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._component_version = component_version

    @property
    def created_at(self):
        """Gets the created_at of this ExemptionResponseDTO.  # noqa: E501


        :return: The created_at of this ExemptionResponseDTO.  # noqa: E501
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ExemptionResponseDTO.


        :param created_at: The created_at of this ExemptionResponseDTO.  # noqa: E501
        :type: int
        """

        self._created_at = created_at

    @property
    def created_by_name(self):
        """Gets the created_by_name of this ExemptionResponseDTO.  # noqa: E501


        :return: The created_by_name of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._created_by_name

    @created_by_name.setter
    def created_by_name(self, created_by_name):
        """Sets the created_by_name of this ExemptionResponseDTO.


        :param created_by_name: The created_by_name of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._created_by_name = created_by_name

    @property
    def created_by_user_id(self):
        """Gets the created_by_user_id of this ExemptionResponseDTO.  # noqa: E501


        :return: The created_by_user_id of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._created_by_user_id

    @created_by_user_id.setter
    def created_by_user_id(self, created_by_user_id):
        """Sets the created_by_user_id of this ExemptionResponseDTO.


        :param created_by_user_id: The created_by_user_id of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._created_by_user_id = created_by_user_id

    @property
    def exemption_duration(self):
        """Gets the exemption_duration of this ExemptionResponseDTO.  # noqa: E501


        :return: The exemption_duration of this ExemptionResponseDTO.  # noqa: E501
        :rtype: ExemptionDurationDTO
        """
        return self._exemption_duration

    @exemption_duration.setter
    def exemption_duration(self, exemption_duration):
        """Sets the exemption_duration of this ExemptionResponseDTO.


        :param exemption_duration: The exemption_duration of this ExemptionResponseDTO.  # noqa: E501
        :type: ExemptionDurationDTO
        """

        self._exemption_duration = exemption_duration

    @property
    def exemption_initiator(self):
        """Gets the exemption_initiator of this ExemptionResponseDTO.  # noqa: E501


        :return: The exemption_initiator of this ExemptionResponseDTO.  # noqa: E501
        :rtype: ExemptionInitiatorDTO
        """
        return self._exemption_initiator

    @exemption_initiator.setter
    def exemption_initiator(self, exemption_initiator):
        """Sets the exemption_initiator of this ExemptionResponseDTO.


        :param exemption_initiator: The exemption_initiator of this ExemptionResponseDTO.  # noqa: E501
        :type: ExemptionInitiatorDTO
        """

        self._exemption_initiator = exemption_initiator

    @property
    def exemption_status(self):
        """Gets the exemption_status of this ExemptionResponseDTO.  # noqa: E501


        :return: The exemption_status of this ExemptionResponseDTO.  # noqa: E501
        :rtype: ExemptionStatusDTO
        """
        return self._exemption_status

    @exemption_status.setter
    def exemption_status(self, exemption_status):
        """Sets the exemption_status of this ExemptionResponseDTO.


        :param exemption_status: The exemption_status of this ExemptionResponseDTO.  # noqa: E501
        :type: ExemptionStatusDTO
        """

        self._exemption_status = exemption_status

    @property
    def org_identifier(self):
        """Gets the org_identifier of this ExemptionResponseDTO.  # noqa: E501


        :return: The org_identifier of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._org_identifier

    @org_identifier.setter
    def org_identifier(self, org_identifier):
        """Sets the org_identifier of this ExemptionResponseDTO.


        :param org_identifier: The org_identifier of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._org_identifier = org_identifier

    @property
    def project_identifier(self):
        """Gets the project_identifier of this ExemptionResponseDTO.  # noqa: E501


        :return: The project_identifier of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._project_identifier

    @project_identifier.setter
    def project_identifier(self, project_identifier):
        """Sets the project_identifier of this ExemptionResponseDTO.


        :param project_identifier: The project_identifier of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._project_identifier = project_identifier

    @property
    def reason(self):
        """Gets the reason of this ExemptionResponseDTO.  # noqa: E501


        :return: The reason of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this ExemptionResponseDTO.


        :param reason: The reason of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._reason = reason

    @property
    def review_comment(self):
        """Gets the review_comment of this ExemptionResponseDTO.  # noqa: E501


        :return: The review_comment of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._review_comment

    @review_comment.setter
    def review_comment(self, review_comment):
        """Sets the review_comment of this ExemptionResponseDTO.


        :param review_comment: The review_comment of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._review_comment = review_comment

    @property
    def reviewed_at(self):
        """Gets the reviewed_at of this ExemptionResponseDTO.  # noqa: E501


        :return: The reviewed_at of this ExemptionResponseDTO.  # noqa: E501
        :rtype: int
        """
        return self._reviewed_at

    @reviewed_at.setter
    def reviewed_at(self, reviewed_at):
        """Sets the reviewed_at of this ExemptionResponseDTO.


        :param reviewed_at: The reviewed_at of this ExemptionResponseDTO.  # noqa: E501
        :type: int
        """

        self._reviewed_at = reviewed_at

    @property
    def reviewed_by_name(self):
        """Gets the reviewed_by_name of this ExemptionResponseDTO.  # noqa: E501


        :return: The reviewed_by_name of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._reviewed_by_name

    @reviewed_by_name.setter
    def reviewed_by_name(self, reviewed_by_name):
        """Sets the reviewed_by_name of this ExemptionResponseDTO.


        :param reviewed_by_name: The reviewed_by_name of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._reviewed_by_name = reviewed_by_name

    @property
    def reviewed_by_user_id(self):
        """Gets the reviewed_by_user_id of this ExemptionResponseDTO.  # noqa: E501


        :return: The reviewed_by_user_id of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._reviewed_by_user_id

    @reviewed_by_user_id.setter
    def reviewed_by_user_id(self, reviewed_by_user_id):
        """Sets the reviewed_by_user_id of this ExemptionResponseDTO.


        :param reviewed_by_user_id: The reviewed_by_user_id of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._reviewed_by_user_id = reviewed_by_user_id

    @property
    def updated_at(self):
        """Gets the updated_at of this ExemptionResponseDTO.  # noqa: E501


        :return: The updated_at of this ExemptionResponseDTO.  # noqa: E501
        :rtype: int
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ExemptionResponseDTO.


        :param updated_at: The updated_at of this ExemptionResponseDTO.  # noqa: E501
        :type: int
        """

        self._updated_at = updated_at

    @property
    def updated_by(self):
        """Gets the updated_by of this ExemptionResponseDTO.  # noqa: E501


        :return: The updated_by of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """Sets the updated_by of this ExemptionResponseDTO.


        :param updated_by: The updated_by of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._updated_by = updated_by

    @property
    def uuid(self):
        """Gets the uuid of this ExemptionResponseDTO.  # noqa: E501


        :return: The uuid of this ExemptionResponseDTO.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this ExemptionResponseDTO.


        :param uuid: The uuid of this ExemptionResponseDTO.  # noqa: E501
        :type: str
        """

        self._uuid = uuid

    @property
    def valid_until(self):
        """Gets the valid_until of this ExemptionResponseDTO.  # noqa: E501


        :return: The valid_until of this ExemptionResponseDTO.  # noqa: E501
        :rtype: int
        """
        return self._valid_until

    @valid_until.setter
    def valid_until(self, valid_until):
        """Sets the valid_until of this ExemptionResponseDTO.


        :param valid_until: The valid_until of this ExemptionResponseDTO.  # noqa: E501
        :type: int
        """

        self._valid_until = valid_until

    @property
    def version_operator(self):
        """Gets the version_operator of this ExemptionResponseDTO.  # noqa: E501


        :return: The version_operator of this ExemptionResponseDTO.  # noqa: E501
        :rtype: Operator
        """
        return self._version_operator

    @version_operator.setter
    def version_operator(self, version_operator):
        """Sets the version_operator of this ExemptionResponseDTO.


        :param version_operator: The version_operator of this ExemptionResponseDTO.  # noqa: E501
        :type: Operator
        """

        self._version_operator = version_operator

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
        if issubclass(ExemptionResponseDTO, dict):
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
        if not isinstance(other, ExemptionResponseDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
