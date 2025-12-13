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

class TypesPullReqActivity(object):
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
        'author': 'TypesPrincipalInfo',
        'code_comment': 'TypesCodeCommentFields',
        'created': 'int',
        'deleted': 'int',
        'edited': 'int',
        'id': 'int',
        'kind': 'EnumPullReqActivityKind',
        'mentions': 'dict(str, TypesPrincipalInfo)',
        'metadata': 'TypesPullReqActivityMetadata',
        'order': 'int',
        'parent_id': 'int',
        'payload': 'object',
        'pullreq_id': 'int',
        'repo_id': 'int',
        'resolved': 'int',
        'resolver': 'TypesPrincipalInfo',
        'sub_order': 'int',
        'text': 'str',
        'type': 'EnumPullReqActivityType',
        'updated': 'int',
        'user_group_mentions': 'dict(str, TypesUserGroupInfo)'
    }

    attribute_map = {
        'author': 'author',
        'code_comment': 'code_comment',
        'created': 'created',
        'deleted': 'deleted',
        'edited': 'edited',
        'id': 'id',
        'kind': 'kind',
        'mentions': 'mentions',
        'metadata': 'metadata',
        'order': 'order',
        'parent_id': 'parent_id',
        'payload': 'payload',
        'pullreq_id': 'pullreq_id',
        'repo_id': 'repo_id',
        'resolved': 'resolved',
        'resolver': 'resolver',
        'sub_order': 'sub_order',
        'text': 'text',
        'type': 'type',
        'updated': 'updated',
        'user_group_mentions': 'user_group_mentions'
    }

    def __init__(self, author=None, code_comment=None, created=None, deleted=None, edited=None, id=None, kind=None, mentions=None, metadata=None, order=None, parent_id=None, payload=None, pullreq_id=None, repo_id=None, resolved=None, resolver=None, sub_order=None, text=None, type=None, updated=None, user_group_mentions=None):  # noqa: E501
        """TypesPullReqActivity - a model defined in Swagger"""  # noqa: E501
        self._author = None
        self._code_comment = None
        self._created = None
        self._deleted = None
        self._edited = None
        self._id = None
        self._kind = None
        self._mentions = None
        self._metadata = None
        self._order = None
        self._parent_id = None
        self._payload = None
        self._pullreq_id = None
        self._repo_id = None
        self._resolved = None
        self._resolver = None
        self._sub_order = None
        self._text = None
        self._type = None
        self._updated = None
        self._user_group_mentions = None
        self.discriminator = None
        if author is not None:
            self.author = author
        if code_comment is not None:
            self.code_comment = code_comment
        if created is not None:
            self.created = created
        if deleted is not None:
            self.deleted = deleted
        if edited is not None:
            self.edited = edited
        if id is not None:
            self.id = id
        if kind is not None:
            self.kind = kind
        if mentions is not None:
            self.mentions = mentions
        if metadata is not None:
            self.metadata = metadata
        if order is not None:
            self.order = order
        if parent_id is not None:
            self.parent_id = parent_id
        if payload is not None:
            self.payload = payload
        if pullreq_id is not None:
            self.pullreq_id = pullreq_id
        if repo_id is not None:
            self.repo_id = repo_id
        if resolved is not None:
            self.resolved = resolved
        if resolver is not None:
            self.resolver = resolver
        if sub_order is not None:
            self.sub_order = sub_order
        if text is not None:
            self.text = text
        if type is not None:
            self.type = type
        if updated is not None:
            self.updated = updated
        if user_group_mentions is not None:
            self.user_group_mentions = user_group_mentions

    @property
    def author(self):
        """Gets the author of this TypesPullReqActivity.  # noqa: E501


        :return: The author of this TypesPullReqActivity.  # noqa: E501
        :rtype: TypesPrincipalInfo
        """
        return self._author

    @author.setter
    def author(self, author):
        """Sets the author of this TypesPullReqActivity.


        :param author: The author of this TypesPullReqActivity.  # noqa: E501
        :type: TypesPrincipalInfo
        """

        self._author = author

    @property
    def code_comment(self):
        """Gets the code_comment of this TypesPullReqActivity.  # noqa: E501


        :return: The code_comment of this TypesPullReqActivity.  # noqa: E501
        :rtype: TypesCodeCommentFields
        """
        return self._code_comment

    @code_comment.setter
    def code_comment(self, code_comment):
        """Sets the code_comment of this TypesPullReqActivity.


        :param code_comment: The code_comment of this TypesPullReqActivity.  # noqa: E501
        :type: TypesCodeCommentFields
        """

        self._code_comment = code_comment

    @property
    def created(self):
        """Gets the created of this TypesPullReqActivity.  # noqa: E501


        :return: The created of this TypesPullReqActivity.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this TypesPullReqActivity.


        :param created: The created of this TypesPullReqActivity.  # noqa: E501
        :type: int
        """

        self._created = created

    @property
    def deleted(self):
        """Gets the deleted of this TypesPullReqActivity.  # noqa: E501


        :return: The deleted of this TypesPullReqActivity.  # noqa: E501
        :rtype: int
        """
        return self._deleted

    @deleted.setter
    def deleted(self, deleted):
        """Sets the deleted of this TypesPullReqActivity.


        :param deleted: The deleted of this TypesPullReqActivity.  # noqa: E501
        :type: int
        """

        self._deleted = deleted

    @property
    def edited(self):
        """Gets the edited of this TypesPullReqActivity.  # noqa: E501


        :return: The edited of this TypesPullReqActivity.  # noqa: E501
        :rtype: int
        """
        return self._edited

    @edited.setter
    def edited(self, edited):
        """Sets the edited of this TypesPullReqActivity.


        :param edited: The edited of this TypesPullReqActivity.  # noqa: E501
        :type: int
        """

        self._edited = edited

    @property
    def id(self):
        """Gets the id of this TypesPullReqActivity.  # noqa: E501


        :return: The id of this TypesPullReqActivity.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this TypesPullReqActivity.


        :param id: The id of this TypesPullReqActivity.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def kind(self):
        """Gets the kind of this TypesPullReqActivity.  # noqa: E501


        :return: The kind of this TypesPullReqActivity.  # noqa: E501
        :rtype: EnumPullReqActivityKind
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this TypesPullReqActivity.


        :param kind: The kind of this TypesPullReqActivity.  # noqa: E501
        :type: EnumPullReqActivityKind
        """

        self._kind = kind

    @property
    def mentions(self):
        """Gets the mentions of this TypesPullReqActivity.  # noqa: E501


        :return: The mentions of this TypesPullReqActivity.  # noqa: E501
        :rtype: dict(str, TypesPrincipalInfo)
        """
        return self._mentions

    @mentions.setter
    def mentions(self, mentions):
        """Sets the mentions of this TypesPullReqActivity.


        :param mentions: The mentions of this TypesPullReqActivity.  # noqa: E501
        :type: dict(str, TypesPrincipalInfo)
        """

        self._mentions = mentions

    @property
    def metadata(self):
        """Gets the metadata of this TypesPullReqActivity.  # noqa: E501


        :return: The metadata of this TypesPullReqActivity.  # noqa: E501
        :rtype: TypesPullReqActivityMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this TypesPullReqActivity.


        :param metadata: The metadata of this TypesPullReqActivity.  # noqa: E501
        :type: TypesPullReqActivityMetadata
        """

        self._metadata = metadata

    @property
    def order(self):
        """Gets the order of this TypesPullReqActivity.  # noqa: E501


        :return: The order of this TypesPullReqActivity.  # noqa: E501
        :rtype: int
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this TypesPullReqActivity.


        :param order: The order of this TypesPullReqActivity.  # noqa: E501
        :type: int
        """

        self._order = order

    @property
    def parent_id(self):
        """Gets the parent_id of this TypesPullReqActivity.  # noqa: E501


        :return: The parent_id of this TypesPullReqActivity.  # noqa: E501
        :rtype: int
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """Sets the parent_id of this TypesPullReqActivity.


        :param parent_id: The parent_id of this TypesPullReqActivity.  # noqa: E501
        :type: int
        """

        self._parent_id = parent_id

    @property
    def payload(self):
        """Gets the payload of this TypesPullReqActivity.  # noqa: E501


        :return: The payload of this TypesPullReqActivity.  # noqa: E501
        :rtype: object
        """
        return self._payload

    @payload.setter
    def payload(self, payload):
        """Sets the payload of this TypesPullReqActivity.


        :param payload: The payload of this TypesPullReqActivity.  # noqa: E501
        :type: object
        """

        self._payload = payload

    @property
    def pullreq_id(self):
        """Gets the pullreq_id of this TypesPullReqActivity.  # noqa: E501


        :return: The pullreq_id of this TypesPullReqActivity.  # noqa: E501
        :rtype: int
        """
        return self._pullreq_id

    @pullreq_id.setter
    def pullreq_id(self, pullreq_id):
        """Sets the pullreq_id of this TypesPullReqActivity.


        :param pullreq_id: The pullreq_id of this TypesPullReqActivity.  # noqa: E501
        :type: int
        """

        self._pullreq_id = pullreq_id

    @property
    def repo_id(self):
        """Gets the repo_id of this TypesPullReqActivity.  # noqa: E501


        :return: The repo_id of this TypesPullReqActivity.  # noqa: E501
        :rtype: int
        """
        return self._repo_id

    @repo_id.setter
    def repo_id(self, repo_id):
        """Sets the repo_id of this TypesPullReqActivity.


        :param repo_id: The repo_id of this TypesPullReqActivity.  # noqa: E501
        :type: int
        """

        self._repo_id = repo_id

    @property
    def resolved(self):
        """Gets the resolved of this TypesPullReqActivity.  # noqa: E501


        :return: The resolved of this TypesPullReqActivity.  # noqa: E501
        :rtype: int
        """
        return self._resolved

    @resolved.setter
    def resolved(self, resolved):
        """Sets the resolved of this TypesPullReqActivity.


        :param resolved: The resolved of this TypesPullReqActivity.  # noqa: E501
        :type: int
        """

        self._resolved = resolved

    @property
    def resolver(self):
        """Gets the resolver of this TypesPullReqActivity.  # noqa: E501


        :return: The resolver of this TypesPullReqActivity.  # noqa: E501
        :rtype: TypesPrincipalInfo
        """
        return self._resolver

    @resolver.setter
    def resolver(self, resolver):
        """Sets the resolver of this TypesPullReqActivity.


        :param resolver: The resolver of this TypesPullReqActivity.  # noqa: E501
        :type: TypesPrincipalInfo
        """

        self._resolver = resolver

    @property
    def sub_order(self):
        """Gets the sub_order of this TypesPullReqActivity.  # noqa: E501


        :return: The sub_order of this TypesPullReqActivity.  # noqa: E501
        :rtype: int
        """
        return self._sub_order

    @sub_order.setter
    def sub_order(self, sub_order):
        """Sets the sub_order of this TypesPullReqActivity.


        :param sub_order: The sub_order of this TypesPullReqActivity.  # noqa: E501
        :type: int
        """

        self._sub_order = sub_order

    @property
    def text(self):
        """Gets the text of this TypesPullReqActivity.  # noqa: E501


        :return: The text of this TypesPullReqActivity.  # noqa: E501
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """Sets the text of this TypesPullReqActivity.


        :param text: The text of this TypesPullReqActivity.  # noqa: E501
        :type: str
        """

        self._text = text

    @property
    def type(self):
        """Gets the type of this TypesPullReqActivity.  # noqa: E501


        :return: The type of this TypesPullReqActivity.  # noqa: E501
        :rtype: EnumPullReqActivityType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this TypesPullReqActivity.


        :param type: The type of this TypesPullReqActivity.  # noqa: E501
        :type: EnumPullReqActivityType
        """

        self._type = type

    @property
    def updated(self):
        """Gets the updated of this TypesPullReqActivity.  # noqa: E501


        :return: The updated of this TypesPullReqActivity.  # noqa: E501
        :rtype: int
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this TypesPullReqActivity.


        :param updated: The updated of this TypesPullReqActivity.  # noqa: E501
        :type: int
        """

        self._updated = updated

    @property
    def user_group_mentions(self):
        """Gets the user_group_mentions of this TypesPullReqActivity.  # noqa: E501


        :return: The user_group_mentions of this TypesPullReqActivity.  # noqa: E501
        :rtype: dict(str, TypesUserGroupInfo)
        """
        return self._user_group_mentions

    @user_group_mentions.setter
    def user_group_mentions(self, user_group_mentions):
        """Sets the user_group_mentions of this TypesPullReqActivity.


        :param user_group_mentions: The user_group_mentions of this TypesPullReqActivity.  # noqa: E501
        :type: dict(str, TypesUserGroupInfo)
        """

        self._user_group_mentions = user_group_mentions

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
        if issubclass(TypesPullReqActivity, dict):
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
        if not isinstance(other, TypesPullReqActivity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
