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

class EncryptedRecordData(object):
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
        'additional_metadata': 'AdditionalMetadata',
        'backup_encrypted_value': 'list[str]',
        'backup_encryption_key': 'str',
        'backup_encryption_type': 'str',
        'backup_kms_id': 'str',
        'base64_encoded': 'bool',
        'encrypted_value': 'list[str]',
        'encryption_key': 'str',
        'encryption_type': 'str',
        'kms_id': 'str',
        'name': 'str',
        'parameters': 'list[EncryptedDataParams]',
        'path': 'str',
        'uuid': 'str'
    }

    attribute_map = {
        'additional_metadata': 'additionalMetadata',
        'backup_encrypted_value': 'backupEncryptedValue',
        'backup_encryption_key': 'backupEncryptionKey',
        'backup_encryption_type': 'backupEncryptionType',
        'backup_kms_id': 'backupKmsId',
        'base64_encoded': 'base64Encoded',
        'encrypted_value': 'encryptedValue',
        'encryption_key': 'encryptionKey',
        'encryption_type': 'encryptionType',
        'kms_id': 'kmsId',
        'name': 'name',
        'parameters': 'parameters',
        'path': 'path',
        'uuid': 'uuid'
    }

    def __init__(self, additional_metadata=None, backup_encrypted_value=None, backup_encryption_key=None, backup_encryption_type=None, backup_kms_id=None, base64_encoded=None, encrypted_value=None, encryption_key=None, encryption_type=None, kms_id=None, name=None, parameters=None, path=None, uuid=None):  # noqa: E501
        """EncryptedRecordData - a model defined in Swagger"""  # noqa: E501
        self._additional_metadata = None
        self._backup_encrypted_value = None
        self._backup_encryption_key = None
        self._backup_encryption_type = None
        self._backup_kms_id = None
        self._base64_encoded = None
        self._encrypted_value = None
        self._encryption_key = None
        self._encryption_type = None
        self._kms_id = None
        self._name = None
        self._parameters = None
        self._path = None
        self._uuid = None
        self.discriminator = None
        if additional_metadata is not None:
            self.additional_metadata = additional_metadata
        if backup_encrypted_value is not None:
            self.backup_encrypted_value = backup_encrypted_value
        if backup_encryption_key is not None:
            self.backup_encryption_key = backup_encryption_key
        if backup_encryption_type is not None:
            self.backup_encryption_type = backup_encryption_type
        if backup_kms_id is not None:
            self.backup_kms_id = backup_kms_id
        if base64_encoded is not None:
            self.base64_encoded = base64_encoded
        if encrypted_value is not None:
            self.encrypted_value = encrypted_value
        if encryption_key is not None:
            self.encryption_key = encryption_key
        if encryption_type is not None:
            self.encryption_type = encryption_type
        if kms_id is not None:
            self.kms_id = kms_id
        if name is not None:
            self.name = name
        if parameters is not None:
            self.parameters = parameters
        if path is not None:
            self.path = path
        if uuid is not None:
            self.uuid = uuid

    @property
    def additional_metadata(self):
        """Gets the additional_metadata of this EncryptedRecordData.  # noqa: E501


        :return: The additional_metadata of this EncryptedRecordData.  # noqa: E501
        :rtype: AdditionalMetadata
        """
        return self._additional_metadata

    @additional_metadata.setter
    def additional_metadata(self, additional_metadata):
        """Sets the additional_metadata of this EncryptedRecordData.


        :param additional_metadata: The additional_metadata of this EncryptedRecordData.  # noqa: E501
        :type: AdditionalMetadata
        """

        self._additional_metadata = additional_metadata

    @property
    def backup_encrypted_value(self):
        """Gets the backup_encrypted_value of this EncryptedRecordData.  # noqa: E501


        :return: The backup_encrypted_value of this EncryptedRecordData.  # noqa: E501
        :rtype: list[str]
        """
        return self._backup_encrypted_value

    @backup_encrypted_value.setter
    def backup_encrypted_value(self, backup_encrypted_value):
        """Sets the backup_encrypted_value of this EncryptedRecordData.


        :param backup_encrypted_value: The backup_encrypted_value of this EncryptedRecordData.  # noqa: E501
        :type: list[str]
        """

        self._backup_encrypted_value = backup_encrypted_value

    @property
    def backup_encryption_key(self):
        """Gets the backup_encryption_key of this EncryptedRecordData.  # noqa: E501


        :return: The backup_encryption_key of this EncryptedRecordData.  # noqa: E501
        :rtype: str
        """
        return self._backup_encryption_key

    @backup_encryption_key.setter
    def backup_encryption_key(self, backup_encryption_key):
        """Sets the backup_encryption_key of this EncryptedRecordData.


        :param backup_encryption_key: The backup_encryption_key of this EncryptedRecordData.  # noqa: E501
        :type: str
        """

        self._backup_encryption_key = backup_encryption_key

    @property
    def backup_encryption_type(self):
        """Gets the backup_encryption_type of this EncryptedRecordData.  # noqa: E501


        :return: The backup_encryption_type of this EncryptedRecordData.  # noqa: E501
        :rtype: str
        """
        return self._backup_encryption_type

    @backup_encryption_type.setter
    def backup_encryption_type(self, backup_encryption_type):
        """Sets the backup_encryption_type of this EncryptedRecordData.


        :param backup_encryption_type: The backup_encryption_type of this EncryptedRecordData.  # noqa: E501
        :type: str
        """
        allowed_values = ["LOCAL", "KMS", "GCP_KMS", "AWS_SECRETS_MANAGER", "AZURE_VAULT", "VAULT", "GCP_SECRETS_MANAGER", "CUSTOM", "VAULT_SSH", "CUSTOM_NG"]  # noqa: E501
        if backup_encryption_type not in allowed_values:
            raise ValueError(
                "Invalid value for `backup_encryption_type` ({0}), must be one of {1}"  # noqa: E501
                .format(backup_encryption_type, allowed_values)
            )

        self._backup_encryption_type = backup_encryption_type

    @property
    def backup_kms_id(self):
        """Gets the backup_kms_id of this EncryptedRecordData.  # noqa: E501


        :return: The backup_kms_id of this EncryptedRecordData.  # noqa: E501
        :rtype: str
        """
        return self._backup_kms_id

    @backup_kms_id.setter
    def backup_kms_id(self, backup_kms_id):
        """Sets the backup_kms_id of this EncryptedRecordData.


        :param backup_kms_id: The backup_kms_id of this EncryptedRecordData.  # noqa: E501
        :type: str
        """

        self._backup_kms_id = backup_kms_id

    @property
    def base64_encoded(self):
        """Gets the base64_encoded of this EncryptedRecordData.  # noqa: E501


        :return: The base64_encoded of this EncryptedRecordData.  # noqa: E501
        :rtype: bool
        """
        return self._base64_encoded

    @base64_encoded.setter
    def base64_encoded(self, base64_encoded):
        """Sets the base64_encoded of this EncryptedRecordData.


        :param base64_encoded: The base64_encoded of this EncryptedRecordData.  # noqa: E501
        :type: bool
        """

        self._base64_encoded = base64_encoded

    @property
    def encrypted_value(self):
        """Gets the encrypted_value of this EncryptedRecordData.  # noqa: E501


        :return: The encrypted_value of this EncryptedRecordData.  # noqa: E501
        :rtype: list[str]
        """
        return self._encrypted_value

    @encrypted_value.setter
    def encrypted_value(self, encrypted_value):
        """Sets the encrypted_value of this EncryptedRecordData.


        :param encrypted_value: The encrypted_value of this EncryptedRecordData.  # noqa: E501
        :type: list[str]
        """

        self._encrypted_value = encrypted_value

    @property
    def encryption_key(self):
        """Gets the encryption_key of this EncryptedRecordData.  # noqa: E501


        :return: The encryption_key of this EncryptedRecordData.  # noqa: E501
        :rtype: str
        """
        return self._encryption_key

    @encryption_key.setter
    def encryption_key(self, encryption_key):
        """Sets the encryption_key of this EncryptedRecordData.


        :param encryption_key: The encryption_key of this EncryptedRecordData.  # noqa: E501
        :type: str
        """

        self._encryption_key = encryption_key

    @property
    def encryption_type(self):
        """Gets the encryption_type of this EncryptedRecordData.  # noqa: E501


        :return: The encryption_type of this EncryptedRecordData.  # noqa: E501
        :rtype: str
        """
        return self._encryption_type

    @encryption_type.setter
    def encryption_type(self, encryption_type):
        """Sets the encryption_type of this EncryptedRecordData.


        :param encryption_type: The encryption_type of this EncryptedRecordData.  # noqa: E501
        :type: str
        """
        allowed_values = ["LOCAL", "KMS", "GCP_KMS", "AWS_SECRETS_MANAGER", "AZURE_VAULT", "VAULT", "GCP_SECRETS_MANAGER", "CUSTOM", "VAULT_SSH", "CUSTOM_NG"]  # noqa: E501
        if encryption_type not in allowed_values:
            raise ValueError(
                "Invalid value for `encryption_type` ({0}), must be one of {1}"  # noqa: E501
                .format(encryption_type, allowed_values)
            )

        self._encryption_type = encryption_type

    @property
    def kms_id(self):
        """Gets the kms_id of this EncryptedRecordData.  # noqa: E501


        :return: The kms_id of this EncryptedRecordData.  # noqa: E501
        :rtype: str
        """
        return self._kms_id

    @kms_id.setter
    def kms_id(self, kms_id):
        """Sets the kms_id of this EncryptedRecordData.


        :param kms_id: The kms_id of this EncryptedRecordData.  # noqa: E501
        :type: str
        """

        self._kms_id = kms_id

    @property
    def name(self):
        """Gets the name of this EncryptedRecordData.  # noqa: E501


        :return: The name of this EncryptedRecordData.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this EncryptedRecordData.


        :param name: The name of this EncryptedRecordData.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def parameters(self):
        """Gets the parameters of this EncryptedRecordData.  # noqa: E501


        :return: The parameters of this EncryptedRecordData.  # noqa: E501
        :rtype: list[EncryptedDataParams]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this EncryptedRecordData.


        :param parameters: The parameters of this EncryptedRecordData.  # noqa: E501
        :type: list[EncryptedDataParams]
        """

        self._parameters = parameters

    @property
    def path(self):
        """Gets the path of this EncryptedRecordData.  # noqa: E501


        :return: The path of this EncryptedRecordData.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this EncryptedRecordData.


        :param path: The path of this EncryptedRecordData.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def uuid(self):
        """Gets the uuid of this EncryptedRecordData.  # noqa: E501


        :return: The uuid of this EncryptedRecordData.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this EncryptedRecordData.


        :param uuid: The uuid of this EncryptedRecordData.  # noqa: E501
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
        if issubclass(EncryptedRecordData, dict):
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
        if not isinstance(other, EncryptedRecordData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
