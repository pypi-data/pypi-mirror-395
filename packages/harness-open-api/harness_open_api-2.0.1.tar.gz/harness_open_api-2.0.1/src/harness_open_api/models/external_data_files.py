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

class ExternalDataFiles(object):
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
        'cloud_storage_path': 'str',
        'created_at': 'int',
        'created_by': 'EmbeddedUser',
        'description': 'str',
        'file_extension': 'str',
        'ingestion_status': 'str',
        'invoice_month': 'str',
        'last_updated_at': 'int',
        'last_updated_by': 'EmbeddedUser',
        'md5': 'str',
        'name': 'str',
        'org_identifier': 'str',
        'project_identifier': 'str',
        'provider_id': 'str',
        'provider_name': 'str',
        'signed_url_used': 'bool',
        'upload_status': 'str',
        'uuid': 'str'
    }

    attribute_map = {
        'account_id': 'accountId',
        'cloud_storage_path': 'cloudStoragePath',
        'created_at': 'createdAt',
        'created_by': 'createdBy',
        'description': 'description',
        'file_extension': 'fileExtension',
        'ingestion_status': 'ingestionStatus',
        'invoice_month': 'invoiceMonth',
        'last_updated_at': 'lastUpdatedAt',
        'last_updated_by': 'lastUpdatedBy',
        'md5': 'md5',
        'name': 'name',
        'org_identifier': 'orgIdentifier',
        'project_identifier': 'projectIdentifier',
        'provider_id': 'providerId',
        'provider_name': 'providerName',
        'signed_url_used': 'signedUrlUsed',
        'upload_status': 'uploadStatus',
        'uuid': 'uuid'
    }

    def __init__(self, account_id=None, cloud_storage_path=None, created_at=None, created_by=None, description=None, file_extension=None, ingestion_status=None, invoice_month=None, last_updated_at=None, last_updated_by=None, md5=None, name=None, org_identifier=None, project_identifier=None, provider_id=None, provider_name=None, signed_url_used=None, upload_status=None, uuid=None):  # noqa: E501
        """ExternalDataFiles - a model defined in Swagger"""  # noqa: E501
        self._account_id = None
        self._cloud_storage_path = None
        self._created_at = None
        self._created_by = None
        self._description = None
        self._file_extension = None
        self._ingestion_status = None
        self._invoice_month = None
        self._last_updated_at = None
        self._last_updated_by = None
        self._md5 = None
        self._name = None
        self._org_identifier = None
        self._project_identifier = None
        self._provider_id = None
        self._provider_name = None
        self._signed_url_used = None
        self._upload_status = None
        self._uuid = None
        self.discriminator = None
        if account_id is not None:
            self.account_id = account_id
        if cloud_storage_path is not None:
            self.cloud_storage_path = cloud_storage_path
        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if description is not None:
            self.description = description
        if file_extension is not None:
            self.file_extension = file_extension
        if ingestion_status is not None:
            self.ingestion_status = ingestion_status
        if invoice_month is not None:
            self.invoice_month = invoice_month
        if last_updated_at is not None:
            self.last_updated_at = last_updated_at
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if md5 is not None:
            self.md5 = md5
        if name is not None:
            self.name = name
        if org_identifier is not None:
            self.org_identifier = org_identifier
        if project_identifier is not None:
            self.project_identifier = project_identifier
        if provider_id is not None:
            self.provider_id = provider_id
        if provider_name is not None:
            self.provider_name = provider_name
        if signed_url_used is not None:
            self.signed_url_used = signed_url_used
        if upload_status is not None:
            self.upload_status = upload_status
        if uuid is not None:
            self.uuid = uuid

    @property
    def account_id(self):
        """Gets the account_id of this ExternalDataFiles.  # noqa: E501

        account id  # noqa: E501

        :return: The account_id of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this ExternalDataFiles.

        account id  # noqa: E501

        :param account_id: The account_id of this ExternalDataFiles.  # noqa: E501
        :type: str
        """

        self._account_id = account_id

    @property
    def cloud_storage_path(self):
        """Gets the cloud_storage_path of this ExternalDataFiles.  # noqa: E501

        cloudStoragePath  # noqa: E501

        :return: The cloud_storage_path of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._cloud_storage_path

    @cloud_storage_path.setter
    def cloud_storage_path(self, cloud_storage_path):
        """Sets the cloud_storage_path of this ExternalDataFiles.

        cloudStoragePath  # noqa: E501

        :param cloud_storage_path: The cloud_storage_path of this ExternalDataFiles.  # noqa: E501
        :type: str
        """

        self._cloud_storage_path = cloud_storage_path

    @property
    def created_at(self):
        """Gets the created_at of this ExternalDataFiles.  # noqa: E501

        Time at which the entity was created  # noqa: E501

        :return: The created_at of this ExternalDataFiles.  # noqa: E501
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ExternalDataFiles.

        Time at which the entity was created  # noqa: E501

        :param created_at: The created_at of this ExternalDataFiles.  # noqa: E501
        :type: int
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this ExternalDataFiles.  # noqa: E501


        :return: The created_by of this ExternalDataFiles.  # noqa: E501
        :rtype: EmbeddedUser
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ExternalDataFiles.


        :param created_by: The created_by of this ExternalDataFiles.  # noqa: E501
        :type: EmbeddedUser
        """

        self._created_by = created_by

    @property
    def description(self):
        """Gets the description of this ExternalDataFiles.  # noqa: E501

        description  # noqa: E501

        :return: The description of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ExternalDataFiles.

        description  # noqa: E501

        :param description: The description of this ExternalDataFiles.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def file_extension(self):
        """Gets the file_extension of this ExternalDataFiles.  # noqa: E501

        externalDataFileExtension  # noqa: E501

        :return: The file_extension of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._file_extension

    @file_extension.setter
    def file_extension(self, file_extension):
        """Sets the file_extension of this ExternalDataFiles.

        externalDataFileExtension  # noqa: E501

        :param file_extension: The file_extension of this ExternalDataFiles.  # noqa: E501
        :type: str
        """
        allowed_values = ["CSV"]  # noqa: E501
        if file_extension not in allowed_values:
            raise ValueError(
                "Invalid value for `file_extension` ({0}), must be one of {1}"  # noqa: E501
                .format(file_extension, allowed_values)
            )

        self._file_extension = file_extension

    @property
    def ingestion_status(self):
        """Gets the ingestion_status of this ExternalDataFiles.  # noqa: E501

        status of file ingestion  # noqa: E501

        :return: The ingestion_status of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._ingestion_status

    @ingestion_status.setter
    def ingestion_status(self, ingestion_status):
        """Sets the ingestion_status of this ExternalDataFiles.

        status of file ingestion  # noqa: E501

        :param ingestion_status: The ingestion_status of this ExternalDataFiles.  # noqa: E501
        :type: str
        """

        self._ingestion_status = ingestion_status

    @property
    def invoice_month(self):
        """Gets the invoice_month of this ExternalDataFiles.  # noqa: E501

        invoice_month  # noqa: E501

        :return: The invoice_month of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._invoice_month

    @invoice_month.setter
    def invoice_month(self, invoice_month):
        """Sets the invoice_month of this ExternalDataFiles.

        invoice_month  # noqa: E501

        :param invoice_month: The invoice_month of this ExternalDataFiles.  # noqa: E501
        :type: str
        """

        self._invoice_month = invoice_month

    @property
    def last_updated_at(self):
        """Gets the last_updated_at of this ExternalDataFiles.  # noqa: E501

        Time at which the entity was last updated  # noqa: E501

        :return: The last_updated_at of this ExternalDataFiles.  # noqa: E501
        :rtype: int
        """
        return self._last_updated_at

    @last_updated_at.setter
    def last_updated_at(self, last_updated_at):
        """Sets the last_updated_at of this ExternalDataFiles.

        Time at which the entity was last updated  # noqa: E501

        :param last_updated_at: The last_updated_at of this ExternalDataFiles.  # noqa: E501
        :type: int
        """

        self._last_updated_at = last_updated_at

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this ExternalDataFiles.  # noqa: E501


        :return: The last_updated_by of this ExternalDataFiles.  # noqa: E501
        :rtype: EmbeddedUser
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this ExternalDataFiles.


        :param last_updated_by: The last_updated_by of this ExternalDataFiles.  # noqa: E501
        :type: EmbeddedUser
        """

        self._last_updated_by = last_updated_by

    @property
    def md5(self):
        """Gets the md5 of this ExternalDataFiles.  # noqa: E501

        md5 of the file  # noqa: E501

        :return: The md5 of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._md5

    @md5.setter
    def md5(self, md5):
        """Sets the md5 of this ExternalDataFiles.

        md5 of the file  # noqa: E501

        :param md5: The md5 of this ExternalDataFiles.  # noqa: E501
        :type: str
        """

        self._md5 = md5

    @property
    def name(self):
        """Gets the name of this ExternalDataFiles.  # noqa: E501

        filename  # noqa: E501

        :return: The name of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ExternalDataFiles.

        filename  # noqa: E501

        :param name: The name of this ExternalDataFiles.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def org_identifier(self):
        """Gets the org_identifier of this ExternalDataFiles.  # noqa: E501

        Organization Identifier for the Entity.  # noqa: E501

        :return: The org_identifier of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._org_identifier

    @org_identifier.setter
    def org_identifier(self, org_identifier):
        """Sets the org_identifier of this ExternalDataFiles.

        Organization Identifier for the Entity.  # noqa: E501

        :param org_identifier: The org_identifier of this ExternalDataFiles.  # noqa: E501
        :type: str
        """

        self._org_identifier = org_identifier

    @property
    def project_identifier(self):
        """Gets the project_identifier of this ExternalDataFiles.  # noqa: E501

        Project Identifier for the Entity.  # noqa: E501

        :return: The project_identifier of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._project_identifier

    @project_identifier.setter
    def project_identifier(self, project_identifier):
        """Sets the project_identifier of this ExternalDataFiles.

        Project Identifier for the Entity.  # noqa: E501

        :param project_identifier: The project_identifier of this ExternalDataFiles.  # noqa: E501
        :type: str
        """

        self._project_identifier = project_identifier

    @property
    def provider_id(self):
        """Gets the provider_id of this ExternalDataFiles.  # noqa: E501

        Identifier of the external data provider  # noqa: E501

        :return: The provider_id of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._provider_id

    @provider_id.setter
    def provider_id(self, provider_id):
        """Sets the provider_id of this ExternalDataFiles.

        Identifier of the external data provider  # noqa: E501

        :param provider_id: The provider_id of this ExternalDataFiles.  # noqa: E501
        :type: str
        """

        self._provider_id = provider_id

    @property
    def provider_name(self):
        """Gets the provider_name of this ExternalDataFiles.  # noqa: E501

        providerName  # noqa: E501

        :return: The provider_name of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._provider_name

    @provider_name.setter
    def provider_name(self, provider_name):
        """Sets the provider_name of this ExternalDataFiles.

        providerName  # noqa: E501

        :param provider_name: The provider_name of this ExternalDataFiles.  # noqa: E501
        :type: str
        """

        self._provider_name = provider_name

    @property
    def signed_url_used(self):
        """Gets the signed_url_used of this ExternalDataFiles.  # noqa: E501

        signedUrlUsed - truncated  # noqa: E501

        :return: The signed_url_used of this ExternalDataFiles.  # noqa: E501
        :rtype: bool
        """
        return self._signed_url_used

    @signed_url_used.setter
    def signed_url_used(self, signed_url_used):
        """Sets the signed_url_used of this ExternalDataFiles.

        signedUrlUsed - truncated  # noqa: E501

        :param signed_url_used: The signed_url_used of this ExternalDataFiles.  # noqa: E501
        :type: bool
        """

        self._signed_url_used = signed_url_used

    @property
    def upload_status(self):
        """Gets the upload_status of this ExternalDataFiles.  # noqa: E501

        status of upload  # noqa: E501

        :return: The upload_status of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._upload_status

    @upload_status.setter
    def upload_status(self, upload_status):
        """Sets the upload_status of this ExternalDataFiles.

        status of upload  # noqa: E501

        :param upload_status: The upload_status of this ExternalDataFiles.  # noqa: E501
        :type: str
        """
        allowed_values = ["INPROGRESS", "COMPLETE", "FAILED", "UNKNOWN"]  # noqa: E501
        if upload_status not in allowed_values:
            raise ValueError(
                "Invalid value for `upload_status` ({0}), must be one of {1}"  # noqa: E501
                .format(upload_status, allowed_values)
            )

        self._upload_status = upload_status

    @property
    def uuid(self):
        """Gets the uuid of this ExternalDataFiles.  # noqa: E501

        unique id  # noqa: E501

        :return: The uuid of this ExternalDataFiles.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this ExternalDataFiles.

        unique id  # noqa: E501

        :param uuid: The uuid of this ExternalDataFiles.  # noqa: E501
        :type: str
        """

        self._uuid = uuid

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
        if issubclass(ExternalDataFiles, dict):
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
        if not isinstance(other, ExternalDataFiles):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
