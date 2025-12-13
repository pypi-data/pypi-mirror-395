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

class RepoRepositoryOutput(object):
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
        'archived': 'bool',
        'created': 'int',
        'created_by': 'int',
        'default_branch': 'str',
        'deleted': 'int',
        'description': 'str',
        'fork_id': 'int',
        'git_ssh_url': 'str',
        'git_url': 'str',
        'id': 'int',
        'identifier': 'str',
        'importing': 'bool',
        'is_empty': 'bool',
        'is_favorite': 'bool',
        'is_public': 'bool',
        'last_git_push': 'int',
        'num_closed_pulls': 'int',
        'num_forks': 'int',
        'num_merged_pulls': 'int',
        'num_open_pulls': 'int',
        'num_pulls': 'int',
        'parent_id': 'int',
        'path': 'str',
        'size': 'int',
        'size_lfs': 'int',
        'size_updated': 'int',
        'state': 'EnumRepoState',
        'tags': 'object',
        'updated': 'int'
    }

    attribute_map = {
        'archived': 'archived',
        'created': 'created',
        'created_by': 'created_by',
        'default_branch': 'default_branch',
        'deleted': 'deleted',
        'description': 'description',
        'fork_id': 'fork_id',
        'git_ssh_url': 'git_ssh_url',
        'git_url': 'git_url',
        'id': 'id',
        'identifier': 'identifier',
        'importing': 'importing',
        'is_empty': 'is_empty',
        'is_favorite': 'is_favorite',
        'is_public': 'is_public',
        'last_git_push': 'last_git_push',
        'num_closed_pulls': 'num_closed_pulls',
        'num_forks': 'num_forks',
        'num_merged_pulls': 'num_merged_pulls',
        'num_open_pulls': 'num_open_pulls',
        'num_pulls': 'num_pulls',
        'parent_id': 'parent_id',
        'path': 'path',
        'size': 'size',
        'size_lfs': 'size_lfs',
        'size_updated': 'size_updated',
        'state': 'state',
        'tags': 'tags',
        'updated': 'updated'
    }

    def __init__(self, archived=None, created=None, created_by=None, default_branch=None, deleted=None, description=None, fork_id=None, git_ssh_url=None, git_url=None, id=None, identifier=None, importing=None, is_empty=None, is_favorite=None, is_public=None, last_git_push=None, num_closed_pulls=None, num_forks=None, num_merged_pulls=None, num_open_pulls=None, num_pulls=None, parent_id=None, path=None, size=None, size_lfs=None, size_updated=None, state=None, tags=None, updated=None):  # noqa: E501
        """RepoRepositoryOutput - a model defined in Swagger"""  # noqa: E501
        self._archived = None
        self._created = None
        self._created_by = None
        self._default_branch = None
        self._deleted = None
        self._description = None
        self._fork_id = None
        self._git_ssh_url = None
        self._git_url = None
        self._id = None
        self._identifier = None
        self._importing = None
        self._is_empty = None
        self._is_favorite = None
        self._is_public = None
        self._last_git_push = None
        self._num_closed_pulls = None
        self._num_forks = None
        self._num_merged_pulls = None
        self._num_open_pulls = None
        self._num_pulls = None
        self._parent_id = None
        self._path = None
        self._size = None
        self._size_lfs = None
        self._size_updated = None
        self._state = None
        self._tags = None
        self._updated = None
        self.discriminator = None
        if archived is not None:
            self.archived = archived
        if created is not None:
            self.created = created
        if created_by is not None:
            self.created_by = created_by
        if default_branch is not None:
            self.default_branch = default_branch
        if deleted is not None:
            self.deleted = deleted
        if description is not None:
            self.description = description
        if fork_id is not None:
            self.fork_id = fork_id
        if git_ssh_url is not None:
            self.git_ssh_url = git_ssh_url
        if git_url is not None:
            self.git_url = git_url
        if id is not None:
            self.id = id
        if identifier is not None:
            self.identifier = identifier
        if importing is not None:
            self.importing = importing
        if is_empty is not None:
            self.is_empty = is_empty
        if is_favorite is not None:
            self.is_favorite = is_favorite
        if is_public is not None:
            self.is_public = is_public
        if last_git_push is not None:
            self.last_git_push = last_git_push
        if num_closed_pulls is not None:
            self.num_closed_pulls = num_closed_pulls
        if num_forks is not None:
            self.num_forks = num_forks
        if num_merged_pulls is not None:
            self.num_merged_pulls = num_merged_pulls
        if num_open_pulls is not None:
            self.num_open_pulls = num_open_pulls
        if num_pulls is not None:
            self.num_pulls = num_pulls
        if parent_id is not None:
            self.parent_id = parent_id
        if path is not None:
            self.path = path
        if size is not None:
            self.size = size
        if size_lfs is not None:
            self.size_lfs = size_lfs
        if size_updated is not None:
            self.size_updated = size_updated
        if state is not None:
            self.state = state
        if tags is not None:
            self.tags = tags
        if updated is not None:
            self.updated = updated

    @property
    def archived(self):
        """Gets the archived of this RepoRepositoryOutput.  # noqa: E501


        :return: The archived of this RepoRepositoryOutput.  # noqa: E501
        :rtype: bool
        """
        return self._archived

    @archived.setter
    def archived(self, archived):
        """Sets the archived of this RepoRepositoryOutput.


        :param archived: The archived of this RepoRepositoryOutput.  # noqa: E501
        :type: bool
        """

        self._archived = archived

    @property
    def created(self):
        """Gets the created of this RepoRepositoryOutput.  # noqa: E501


        :return: The created of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this RepoRepositoryOutput.


        :param created: The created of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._created = created

    @property
    def created_by(self):
        """Gets the created_by of this RepoRepositoryOutput.  # noqa: E501


        :return: The created_by of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this RepoRepositoryOutput.


        :param created_by: The created_by of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._created_by = created_by

    @property
    def default_branch(self):
        """Gets the default_branch of this RepoRepositoryOutput.  # noqa: E501


        :return: The default_branch of this RepoRepositoryOutput.  # noqa: E501
        :rtype: str
        """
        return self._default_branch

    @default_branch.setter
    def default_branch(self, default_branch):
        """Sets the default_branch of this RepoRepositoryOutput.


        :param default_branch: The default_branch of this RepoRepositoryOutput.  # noqa: E501
        :type: str
        """

        self._default_branch = default_branch

    @property
    def deleted(self):
        """Gets the deleted of this RepoRepositoryOutput.  # noqa: E501


        :return: The deleted of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._deleted

    @deleted.setter
    def deleted(self, deleted):
        """Sets the deleted of this RepoRepositoryOutput.


        :param deleted: The deleted of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._deleted = deleted

    @property
    def description(self):
        """Gets the description of this RepoRepositoryOutput.  # noqa: E501


        :return: The description of this RepoRepositoryOutput.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this RepoRepositoryOutput.


        :param description: The description of this RepoRepositoryOutput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def fork_id(self):
        """Gets the fork_id of this RepoRepositoryOutput.  # noqa: E501


        :return: The fork_id of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._fork_id

    @fork_id.setter
    def fork_id(self, fork_id):
        """Sets the fork_id of this RepoRepositoryOutput.


        :param fork_id: The fork_id of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._fork_id = fork_id

    @property
    def git_ssh_url(self):
        """Gets the git_ssh_url of this RepoRepositoryOutput.  # noqa: E501


        :return: The git_ssh_url of this RepoRepositoryOutput.  # noqa: E501
        :rtype: str
        """
        return self._git_ssh_url

    @git_ssh_url.setter
    def git_ssh_url(self, git_ssh_url):
        """Sets the git_ssh_url of this RepoRepositoryOutput.


        :param git_ssh_url: The git_ssh_url of this RepoRepositoryOutput.  # noqa: E501
        :type: str
        """

        self._git_ssh_url = git_ssh_url

    @property
    def git_url(self):
        """Gets the git_url of this RepoRepositoryOutput.  # noqa: E501


        :return: The git_url of this RepoRepositoryOutput.  # noqa: E501
        :rtype: str
        """
        return self._git_url

    @git_url.setter
    def git_url(self, git_url):
        """Sets the git_url of this RepoRepositoryOutput.


        :param git_url: The git_url of this RepoRepositoryOutput.  # noqa: E501
        :type: str
        """

        self._git_url = git_url

    @property
    def id(self):
        """Gets the id of this RepoRepositoryOutput.  # noqa: E501


        :return: The id of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this RepoRepositoryOutput.


        :param id: The id of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def identifier(self):
        """Gets the identifier of this RepoRepositoryOutput.  # noqa: E501


        :return: The identifier of this RepoRepositoryOutput.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this RepoRepositoryOutput.


        :param identifier: The identifier of this RepoRepositoryOutput.  # noqa: E501
        :type: str
        """

        self._identifier = identifier

    @property
    def importing(self):
        """Gets the importing of this RepoRepositoryOutput.  # noqa: E501


        :return: The importing of this RepoRepositoryOutput.  # noqa: E501
        :rtype: bool
        """
        return self._importing

    @importing.setter
    def importing(self, importing):
        """Sets the importing of this RepoRepositoryOutput.


        :param importing: The importing of this RepoRepositoryOutput.  # noqa: E501
        :type: bool
        """

        self._importing = importing

    @property
    def is_empty(self):
        """Gets the is_empty of this RepoRepositoryOutput.  # noqa: E501


        :return: The is_empty of this RepoRepositoryOutput.  # noqa: E501
        :rtype: bool
        """
        return self._is_empty

    @is_empty.setter
    def is_empty(self, is_empty):
        """Sets the is_empty of this RepoRepositoryOutput.


        :param is_empty: The is_empty of this RepoRepositoryOutput.  # noqa: E501
        :type: bool
        """

        self._is_empty = is_empty

    @property
    def is_favorite(self):
        """Gets the is_favorite of this RepoRepositoryOutput.  # noqa: E501


        :return: The is_favorite of this RepoRepositoryOutput.  # noqa: E501
        :rtype: bool
        """
        return self._is_favorite

    @is_favorite.setter
    def is_favorite(self, is_favorite):
        """Sets the is_favorite of this RepoRepositoryOutput.


        :param is_favorite: The is_favorite of this RepoRepositoryOutput.  # noqa: E501
        :type: bool
        """

        self._is_favorite = is_favorite

    @property
    def is_public(self):
        """Gets the is_public of this RepoRepositoryOutput.  # noqa: E501


        :return: The is_public of this RepoRepositoryOutput.  # noqa: E501
        :rtype: bool
        """
        return self._is_public

    @is_public.setter
    def is_public(self, is_public):
        """Sets the is_public of this RepoRepositoryOutput.


        :param is_public: The is_public of this RepoRepositoryOutput.  # noqa: E501
        :type: bool
        """

        self._is_public = is_public

    @property
    def last_git_push(self):
        """Gets the last_git_push of this RepoRepositoryOutput.  # noqa: E501


        :return: The last_git_push of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._last_git_push

    @last_git_push.setter
    def last_git_push(self, last_git_push):
        """Sets the last_git_push of this RepoRepositoryOutput.


        :param last_git_push: The last_git_push of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._last_git_push = last_git_push

    @property
    def num_closed_pulls(self):
        """Gets the num_closed_pulls of this RepoRepositoryOutput.  # noqa: E501


        :return: The num_closed_pulls of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._num_closed_pulls

    @num_closed_pulls.setter
    def num_closed_pulls(self, num_closed_pulls):
        """Sets the num_closed_pulls of this RepoRepositoryOutput.


        :param num_closed_pulls: The num_closed_pulls of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._num_closed_pulls = num_closed_pulls

    @property
    def num_forks(self):
        """Gets the num_forks of this RepoRepositoryOutput.  # noqa: E501


        :return: The num_forks of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._num_forks

    @num_forks.setter
    def num_forks(self, num_forks):
        """Sets the num_forks of this RepoRepositoryOutput.


        :param num_forks: The num_forks of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._num_forks = num_forks

    @property
    def num_merged_pulls(self):
        """Gets the num_merged_pulls of this RepoRepositoryOutput.  # noqa: E501


        :return: The num_merged_pulls of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._num_merged_pulls

    @num_merged_pulls.setter
    def num_merged_pulls(self, num_merged_pulls):
        """Sets the num_merged_pulls of this RepoRepositoryOutput.


        :param num_merged_pulls: The num_merged_pulls of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._num_merged_pulls = num_merged_pulls

    @property
    def num_open_pulls(self):
        """Gets the num_open_pulls of this RepoRepositoryOutput.  # noqa: E501


        :return: The num_open_pulls of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._num_open_pulls

    @num_open_pulls.setter
    def num_open_pulls(self, num_open_pulls):
        """Sets the num_open_pulls of this RepoRepositoryOutput.


        :param num_open_pulls: The num_open_pulls of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._num_open_pulls = num_open_pulls

    @property
    def num_pulls(self):
        """Gets the num_pulls of this RepoRepositoryOutput.  # noqa: E501


        :return: The num_pulls of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._num_pulls

    @num_pulls.setter
    def num_pulls(self, num_pulls):
        """Sets the num_pulls of this RepoRepositoryOutput.


        :param num_pulls: The num_pulls of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._num_pulls = num_pulls

    @property
    def parent_id(self):
        """Gets the parent_id of this RepoRepositoryOutput.  # noqa: E501


        :return: The parent_id of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """Sets the parent_id of this RepoRepositoryOutput.


        :param parent_id: The parent_id of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._parent_id = parent_id

    @property
    def path(self):
        """Gets the path of this RepoRepositoryOutput.  # noqa: E501


        :return: The path of this RepoRepositoryOutput.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this RepoRepositoryOutput.


        :param path: The path of this RepoRepositoryOutput.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def size(self):
        """Gets the size of this RepoRepositoryOutput.  # noqa: E501

        size of the repository in KiB  # noqa: E501

        :return: The size of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this RepoRepositoryOutput.

        size of the repository in KiB  # noqa: E501

        :param size: The size of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._size = size

    @property
    def size_lfs(self):
        """Gets the size_lfs of this RepoRepositoryOutput.  # noqa: E501

        size of the repository LFS in KiB  # noqa: E501

        :return: The size_lfs of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._size_lfs

    @size_lfs.setter
    def size_lfs(self, size_lfs):
        """Sets the size_lfs of this RepoRepositoryOutput.

        size of the repository LFS in KiB  # noqa: E501

        :param size_lfs: The size_lfs of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._size_lfs = size_lfs

    @property
    def size_updated(self):
        """Gets the size_updated of this RepoRepositoryOutput.  # noqa: E501


        :return: The size_updated of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._size_updated

    @size_updated.setter
    def size_updated(self, size_updated):
        """Sets the size_updated of this RepoRepositoryOutput.


        :param size_updated: The size_updated of this RepoRepositoryOutput.  # noqa: E501
        :type: int
        """

        self._size_updated = size_updated

    @property
    def state(self):
        """Gets the state of this RepoRepositoryOutput.  # noqa: E501


        :return: The state of this RepoRepositoryOutput.  # noqa: E501
        :rtype: EnumRepoState
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this RepoRepositoryOutput.


        :param state: The state of this RepoRepositoryOutput.  # noqa: E501
        :type: EnumRepoState
        """

        self._state = state

    @property
    def tags(self):
        """Gets the tags of this RepoRepositoryOutput.  # noqa: E501


        :return: The tags of this RepoRepositoryOutput.  # noqa: E501
        :rtype: object
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this RepoRepositoryOutput.


        :param tags: The tags of this RepoRepositoryOutput.  # noqa: E501
        :type: object
        """

        self._tags = tags

    @property
    def updated(self):
        """Gets the updated of this RepoRepositoryOutput.  # noqa: E501


        :return: The updated of this RepoRepositoryOutput.  # noqa: E501
        :rtype: int
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this RepoRepositoryOutput.


        :param updated: The updated of this RepoRepositoryOutput.  # noqa: E501
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
        if issubclass(RepoRepositoryOutput, dict):
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
        if not isinstance(other, RepoRepositoryOutput):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
