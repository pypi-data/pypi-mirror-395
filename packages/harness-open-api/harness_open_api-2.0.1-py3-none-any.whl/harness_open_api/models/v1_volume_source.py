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

class V1VolumeSource(object):
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
        'aws_elastic_block_store': 'V1AWSElasticBlockStoreVolumeSource',
        'azure_disk': 'V1AzureDiskVolumeSource',
        'azure_file': 'V1AzureFileVolumeSource',
        'cephfs': 'V1CephFSVolumeSource',
        'cinder': 'V1CinderVolumeSource',
        'config_map': 'V1ConfigMapVolumeSource',
        'csi': 'V1CSIVolumeSource',
        'downward_api': 'V1DownwardAPIVolumeSource',
        'empty_dir': 'V1EmptyDirVolumeSource',
        'ephemeral': 'V1EphemeralVolumeSource',
        'fc': 'V1FCVolumeSource',
        'flex_volume': 'V1FlexVolumeSource',
        'flocker': 'V1FlockerVolumeSource',
        'gce_persistent_disk': 'V1GCEPersistentDiskVolumeSource',
        'git_repo': 'V1GitRepoVolumeSource',
        'glusterfs': 'V1GlusterfsVolumeSource',
        'host_path': 'V1HostPathVolumeSource',
        'image': 'V1ImageVolumeSource',
        'iscsi': 'V1ISCSIVolumeSource',
        'nfs': 'V1NFSVolumeSource',
        'persistent_volume_claim': 'V1PersistentVolumeClaimVolumeSource',
        'photon_persistent_disk': 'V1PhotonPersistentDiskVolumeSource',
        'portworx_volume': 'V1PortworxVolumeSource',
        'projected': 'V1ProjectedVolumeSource',
        'quobyte': 'V1QuobyteVolumeSource',
        'rbd': 'V1RBDVolumeSource',
        'scale_io': 'V1ScaleIOVolumeSource',
        'secret': 'V1SecretVolumeSource',
        'storageos': 'V1StorageOSVolumeSource',
        'vsphere_volume': 'V1VsphereVirtualDiskVolumeSource'
    }

    attribute_map = {
        'aws_elastic_block_store': 'awsElasticBlockStore',
        'azure_disk': 'azureDisk',
        'azure_file': 'azureFile',
        'cephfs': 'cephfs',
        'cinder': 'cinder',
        'config_map': 'configMap',
        'csi': 'csi',
        'downward_api': 'downwardAPI',
        'empty_dir': 'emptyDir',
        'ephemeral': 'ephemeral',
        'fc': 'fc',
        'flex_volume': 'flexVolume',
        'flocker': 'flocker',
        'gce_persistent_disk': 'gcePersistentDisk',
        'git_repo': 'gitRepo',
        'glusterfs': 'glusterfs',
        'host_path': 'hostPath',
        'image': 'image',
        'iscsi': 'iscsi',
        'nfs': 'nfs',
        'persistent_volume_claim': 'persistentVolumeClaim',
        'photon_persistent_disk': 'photonPersistentDisk',
        'portworx_volume': 'portworxVolume',
        'projected': 'projected',
        'quobyte': 'quobyte',
        'rbd': 'rbd',
        'scale_io': 'scaleIO',
        'secret': 'secret',
        'storageos': 'storageos',
        'vsphere_volume': 'vsphereVolume'
    }

    def __init__(self, aws_elastic_block_store=None, azure_disk=None, azure_file=None, cephfs=None, cinder=None, config_map=None, csi=None, downward_api=None, empty_dir=None, ephemeral=None, fc=None, flex_volume=None, flocker=None, gce_persistent_disk=None, git_repo=None, glusterfs=None, host_path=None, image=None, iscsi=None, nfs=None, persistent_volume_claim=None, photon_persistent_disk=None, portworx_volume=None, projected=None, quobyte=None, rbd=None, scale_io=None, secret=None, storageos=None, vsphere_volume=None):  # noqa: E501
        """V1VolumeSource - a model defined in Swagger"""  # noqa: E501
        self._aws_elastic_block_store = None
        self._azure_disk = None
        self._azure_file = None
        self._cephfs = None
        self._cinder = None
        self._config_map = None
        self._csi = None
        self._downward_api = None
        self._empty_dir = None
        self._ephemeral = None
        self._fc = None
        self._flex_volume = None
        self._flocker = None
        self._gce_persistent_disk = None
        self._git_repo = None
        self._glusterfs = None
        self._host_path = None
        self._image = None
        self._iscsi = None
        self._nfs = None
        self._persistent_volume_claim = None
        self._photon_persistent_disk = None
        self._portworx_volume = None
        self._projected = None
        self._quobyte = None
        self._rbd = None
        self._scale_io = None
        self._secret = None
        self._storageos = None
        self._vsphere_volume = None
        self.discriminator = None
        if aws_elastic_block_store is not None:
            self.aws_elastic_block_store = aws_elastic_block_store
        if azure_disk is not None:
            self.azure_disk = azure_disk
        if azure_file is not None:
            self.azure_file = azure_file
        if cephfs is not None:
            self.cephfs = cephfs
        if cinder is not None:
            self.cinder = cinder
        if config_map is not None:
            self.config_map = config_map
        if csi is not None:
            self.csi = csi
        if downward_api is not None:
            self.downward_api = downward_api
        if empty_dir is not None:
            self.empty_dir = empty_dir
        if ephemeral is not None:
            self.ephemeral = ephemeral
        if fc is not None:
            self.fc = fc
        if flex_volume is not None:
            self.flex_volume = flex_volume
        if flocker is not None:
            self.flocker = flocker
        if gce_persistent_disk is not None:
            self.gce_persistent_disk = gce_persistent_disk
        if git_repo is not None:
            self.git_repo = git_repo
        if glusterfs is not None:
            self.glusterfs = glusterfs
        if host_path is not None:
            self.host_path = host_path
        if image is not None:
            self.image = image
        if iscsi is not None:
            self.iscsi = iscsi
        if nfs is not None:
            self.nfs = nfs
        if persistent_volume_claim is not None:
            self.persistent_volume_claim = persistent_volume_claim
        if photon_persistent_disk is not None:
            self.photon_persistent_disk = photon_persistent_disk
        if portworx_volume is not None:
            self.portworx_volume = portworx_volume
        if projected is not None:
            self.projected = projected
        if quobyte is not None:
            self.quobyte = quobyte
        if rbd is not None:
            self.rbd = rbd
        if scale_io is not None:
            self.scale_io = scale_io
        if secret is not None:
            self.secret = secret
        if storageos is not None:
            self.storageos = storageos
        if vsphere_volume is not None:
            self.vsphere_volume = vsphere_volume

    @property
    def aws_elastic_block_store(self):
        """Gets the aws_elastic_block_store of this V1VolumeSource.  # noqa: E501


        :return: The aws_elastic_block_store of this V1VolumeSource.  # noqa: E501
        :rtype: V1AWSElasticBlockStoreVolumeSource
        """
        return self._aws_elastic_block_store

    @aws_elastic_block_store.setter
    def aws_elastic_block_store(self, aws_elastic_block_store):
        """Sets the aws_elastic_block_store of this V1VolumeSource.


        :param aws_elastic_block_store: The aws_elastic_block_store of this V1VolumeSource.  # noqa: E501
        :type: V1AWSElasticBlockStoreVolumeSource
        """

        self._aws_elastic_block_store = aws_elastic_block_store

    @property
    def azure_disk(self):
        """Gets the azure_disk of this V1VolumeSource.  # noqa: E501


        :return: The azure_disk of this V1VolumeSource.  # noqa: E501
        :rtype: V1AzureDiskVolumeSource
        """
        return self._azure_disk

    @azure_disk.setter
    def azure_disk(self, azure_disk):
        """Sets the azure_disk of this V1VolumeSource.


        :param azure_disk: The azure_disk of this V1VolumeSource.  # noqa: E501
        :type: V1AzureDiskVolumeSource
        """

        self._azure_disk = azure_disk

    @property
    def azure_file(self):
        """Gets the azure_file of this V1VolumeSource.  # noqa: E501


        :return: The azure_file of this V1VolumeSource.  # noqa: E501
        :rtype: V1AzureFileVolumeSource
        """
        return self._azure_file

    @azure_file.setter
    def azure_file(self, azure_file):
        """Sets the azure_file of this V1VolumeSource.


        :param azure_file: The azure_file of this V1VolumeSource.  # noqa: E501
        :type: V1AzureFileVolumeSource
        """

        self._azure_file = azure_file

    @property
    def cephfs(self):
        """Gets the cephfs of this V1VolumeSource.  # noqa: E501


        :return: The cephfs of this V1VolumeSource.  # noqa: E501
        :rtype: V1CephFSVolumeSource
        """
        return self._cephfs

    @cephfs.setter
    def cephfs(self, cephfs):
        """Sets the cephfs of this V1VolumeSource.


        :param cephfs: The cephfs of this V1VolumeSource.  # noqa: E501
        :type: V1CephFSVolumeSource
        """

        self._cephfs = cephfs

    @property
    def cinder(self):
        """Gets the cinder of this V1VolumeSource.  # noqa: E501


        :return: The cinder of this V1VolumeSource.  # noqa: E501
        :rtype: V1CinderVolumeSource
        """
        return self._cinder

    @cinder.setter
    def cinder(self, cinder):
        """Sets the cinder of this V1VolumeSource.


        :param cinder: The cinder of this V1VolumeSource.  # noqa: E501
        :type: V1CinderVolumeSource
        """

        self._cinder = cinder

    @property
    def config_map(self):
        """Gets the config_map of this V1VolumeSource.  # noqa: E501


        :return: The config_map of this V1VolumeSource.  # noqa: E501
        :rtype: V1ConfigMapVolumeSource
        """
        return self._config_map

    @config_map.setter
    def config_map(self, config_map):
        """Sets the config_map of this V1VolumeSource.


        :param config_map: The config_map of this V1VolumeSource.  # noqa: E501
        :type: V1ConfigMapVolumeSource
        """

        self._config_map = config_map

    @property
    def csi(self):
        """Gets the csi of this V1VolumeSource.  # noqa: E501


        :return: The csi of this V1VolumeSource.  # noqa: E501
        :rtype: V1CSIVolumeSource
        """
        return self._csi

    @csi.setter
    def csi(self, csi):
        """Sets the csi of this V1VolumeSource.


        :param csi: The csi of this V1VolumeSource.  # noqa: E501
        :type: V1CSIVolumeSource
        """

        self._csi = csi

    @property
    def downward_api(self):
        """Gets the downward_api of this V1VolumeSource.  # noqa: E501


        :return: The downward_api of this V1VolumeSource.  # noqa: E501
        :rtype: V1DownwardAPIVolumeSource
        """
        return self._downward_api

    @downward_api.setter
    def downward_api(self, downward_api):
        """Sets the downward_api of this V1VolumeSource.


        :param downward_api: The downward_api of this V1VolumeSource.  # noqa: E501
        :type: V1DownwardAPIVolumeSource
        """

        self._downward_api = downward_api

    @property
    def empty_dir(self):
        """Gets the empty_dir of this V1VolumeSource.  # noqa: E501


        :return: The empty_dir of this V1VolumeSource.  # noqa: E501
        :rtype: V1EmptyDirVolumeSource
        """
        return self._empty_dir

    @empty_dir.setter
    def empty_dir(self, empty_dir):
        """Sets the empty_dir of this V1VolumeSource.


        :param empty_dir: The empty_dir of this V1VolumeSource.  # noqa: E501
        :type: V1EmptyDirVolumeSource
        """

        self._empty_dir = empty_dir

    @property
    def ephemeral(self):
        """Gets the ephemeral of this V1VolumeSource.  # noqa: E501


        :return: The ephemeral of this V1VolumeSource.  # noqa: E501
        :rtype: V1EphemeralVolumeSource
        """
        return self._ephemeral

    @ephemeral.setter
    def ephemeral(self, ephemeral):
        """Sets the ephemeral of this V1VolumeSource.


        :param ephemeral: The ephemeral of this V1VolumeSource.  # noqa: E501
        :type: V1EphemeralVolumeSource
        """

        self._ephemeral = ephemeral

    @property
    def fc(self):
        """Gets the fc of this V1VolumeSource.  # noqa: E501


        :return: The fc of this V1VolumeSource.  # noqa: E501
        :rtype: V1FCVolumeSource
        """
        return self._fc

    @fc.setter
    def fc(self, fc):
        """Sets the fc of this V1VolumeSource.


        :param fc: The fc of this V1VolumeSource.  # noqa: E501
        :type: V1FCVolumeSource
        """

        self._fc = fc

    @property
    def flex_volume(self):
        """Gets the flex_volume of this V1VolumeSource.  # noqa: E501


        :return: The flex_volume of this V1VolumeSource.  # noqa: E501
        :rtype: V1FlexVolumeSource
        """
        return self._flex_volume

    @flex_volume.setter
    def flex_volume(self, flex_volume):
        """Sets the flex_volume of this V1VolumeSource.


        :param flex_volume: The flex_volume of this V1VolumeSource.  # noqa: E501
        :type: V1FlexVolumeSource
        """

        self._flex_volume = flex_volume

    @property
    def flocker(self):
        """Gets the flocker of this V1VolumeSource.  # noqa: E501


        :return: The flocker of this V1VolumeSource.  # noqa: E501
        :rtype: V1FlockerVolumeSource
        """
        return self._flocker

    @flocker.setter
    def flocker(self, flocker):
        """Sets the flocker of this V1VolumeSource.


        :param flocker: The flocker of this V1VolumeSource.  # noqa: E501
        :type: V1FlockerVolumeSource
        """

        self._flocker = flocker

    @property
    def gce_persistent_disk(self):
        """Gets the gce_persistent_disk of this V1VolumeSource.  # noqa: E501


        :return: The gce_persistent_disk of this V1VolumeSource.  # noqa: E501
        :rtype: V1GCEPersistentDiskVolumeSource
        """
        return self._gce_persistent_disk

    @gce_persistent_disk.setter
    def gce_persistent_disk(self, gce_persistent_disk):
        """Sets the gce_persistent_disk of this V1VolumeSource.


        :param gce_persistent_disk: The gce_persistent_disk of this V1VolumeSource.  # noqa: E501
        :type: V1GCEPersistentDiskVolumeSource
        """

        self._gce_persistent_disk = gce_persistent_disk

    @property
    def git_repo(self):
        """Gets the git_repo of this V1VolumeSource.  # noqa: E501


        :return: The git_repo of this V1VolumeSource.  # noqa: E501
        :rtype: V1GitRepoVolumeSource
        """
        return self._git_repo

    @git_repo.setter
    def git_repo(self, git_repo):
        """Sets the git_repo of this V1VolumeSource.


        :param git_repo: The git_repo of this V1VolumeSource.  # noqa: E501
        :type: V1GitRepoVolumeSource
        """

        self._git_repo = git_repo

    @property
    def glusterfs(self):
        """Gets the glusterfs of this V1VolumeSource.  # noqa: E501


        :return: The glusterfs of this V1VolumeSource.  # noqa: E501
        :rtype: V1GlusterfsVolumeSource
        """
        return self._glusterfs

    @glusterfs.setter
    def glusterfs(self, glusterfs):
        """Sets the glusterfs of this V1VolumeSource.


        :param glusterfs: The glusterfs of this V1VolumeSource.  # noqa: E501
        :type: V1GlusterfsVolumeSource
        """

        self._glusterfs = glusterfs

    @property
    def host_path(self):
        """Gets the host_path of this V1VolumeSource.  # noqa: E501


        :return: The host_path of this V1VolumeSource.  # noqa: E501
        :rtype: V1HostPathVolumeSource
        """
        return self._host_path

    @host_path.setter
    def host_path(self, host_path):
        """Sets the host_path of this V1VolumeSource.


        :param host_path: The host_path of this V1VolumeSource.  # noqa: E501
        :type: V1HostPathVolumeSource
        """

        self._host_path = host_path

    @property
    def image(self):
        """Gets the image of this V1VolumeSource.  # noqa: E501


        :return: The image of this V1VolumeSource.  # noqa: E501
        :rtype: V1ImageVolumeSource
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this V1VolumeSource.


        :param image: The image of this V1VolumeSource.  # noqa: E501
        :type: V1ImageVolumeSource
        """

        self._image = image

    @property
    def iscsi(self):
        """Gets the iscsi of this V1VolumeSource.  # noqa: E501


        :return: The iscsi of this V1VolumeSource.  # noqa: E501
        :rtype: V1ISCSIVolumeSource
        """
        return self._iscsi

    @iscsi.setter
    def iscsi(self, iscsi):
        """Sets the iscsi of this V1VolumeSource.


        :param iscsi: The iscsi of this V1VolumeSource.  # noqa: E501
        :type: V1ISCSIVolumeSource
        """

        self._iscsi = iscsi

    @property
    def nfs(self):
        """Gets the nfs of this V1VolumeSource.  # noqa: E501


        :return: The nfs of this V1VolumeSource.  # noqa: E501
        :rtype: V1NFSVolumeSource
        """
        return self._nfs

    @nfs.setter
    def nfs(self, nfs):
        """Sets the nfs of this V1VolumeSource.


        :param nfs: The nfs of this V1VolumeSource.  # noqa: E501
        :type: V1NFSVolumeSource
        """

        self._nfs = nfs

    @property
    def persistent_volume_claim(self):
        """Gets the persistent_volume_claim of this V1VolumeSource.  # noqa: E501


        :return: The persistent_volume_claim of this V1VolumeSource.  # noqa: E501
        :rtype: V1PersistentVolumeClaimVolumeSource
        """
        return self._persistent_volume_claim

    @persistent_volume_claim.setter
    def persistent_volume_claim(self, persistent_volume_claim):
        """Sets the persistent_volume_claim of this V1VolumeSource.


        :param persistent_volume_claim: The persistent_volume_claim of this V1VolumeSource.  # noqa: E501
        :type: V1PersistentVolumeClaimVolumeSource
        """

        self._persistent_volume_claim = persistent_volume_claim

    @property
    def photon_persistent_disk(self):
        """Gets the photon_persistent_disk of this V1VolumeSource.  # noqa: E501


        :return: The photon_persistent_disk of this V1VolumeSource.  # noqa: E501
        :rtype: V1PhotonPersistentDiskVolumeSource
        """
        return self._photon_persistent_disk

    @photon_persistent_disk.setter
    def photon_persistent_disk(self, photon_persistent_disk):
        """Sets the photon_persistent_disk of this V1VolumeSource.


        :param photon_persistent_disk: The photon_persistent_disk of this V1VolumeSource.  # noqa: E501
        :type: V1PhotonPersistentDiskVolumeSource
        """

        self._photon_persistent_disk = photon_persistent_disk

    @property
    def portworx_volume(self):
        """Gets the portworx_volume of this V1VolumeSource.  # noqa: E501


        :return: The portworx_volume of this V1VolumeSource.  # noqa: E501
        :rtype: V1PortworxVolumeSource
        """
        return self._portworx_volume

    @portworx_volume.setter
    def portworx_volume(self, portworx_volume):
        """Sets the portworx_volume of this V1VolumeSource.


        :param portworx_volume: The portworx_volume of this V1VolumeSource.  # noqa: E501
        :type: V1PortworxVolumeSource
        """

        self._portworx_volume = portworx_volume

    @property
    def projected(self):
        """Gets the projected of this V1VolumeSource.  # noqa: E501


        :return: The projected of this V1VolumeSource.  # noqa: E501
        :rtype: V1ProjectedVolumeSource
        """
        return self._projected

    @projected.setter
    def projected(self, projected):
        """Sets the projected of this V1VolumeSource.


        :param projected: The projected of this V1VolumeSource.  # noqa: E501
        :type: V1ProjectedVolumeSource
        """

        self._projected = projected

    @property
    def quobyte(self):
        """Gets the quobyte of this V1VolumeSource.  # noqa: E501


        :return: The quobyte of this V1VolumeSource.  # noqa: E501
        :rtype: V1QuobyteVolumeSource
        """
        return self._quobyte

    @quobyte.setter
    def quobyte(self, quobyte):
        """Sets the quobyte of this V1VolumeSource.


        :param quobyte: The quobyte of this V1VolumeSource.  # noqa: E501
        :type: V1QuobyteVolumeSource
        """

        self._quobyte = quobyte

    @property
    def rbd(self):
        """Gets the rbd of this V1VolumeSource.  # noqa: E501


        :return: The rbd of this V1VolumeSource.  # noqa: E501
        :rtype: V1RBDVolumeSource
        """
        return self._rbd

    @rbd.setter
    def rbd(self, rbd):
        """Sets the rbd of this V1VolumeSource.


        :param rbd: The rbd of this V1VolumeSource.  # noqa: E501
        :type: V1RBDVolumeSource
        """

        self._rbd = rbd

    @property
    def scale_io(self):
        """Gets the scale_io of this V1VolumeSource.  # noqa: E501


        :return: The scale_io of this V1VolumeSource.  # noqa: E501
        :rtype: V1ScaleIOVolumeSource
        """
        return self._scale_io

    @scale_io.setter
    def scale_io(self, scale_io):
        """Sets the scale_io of this V1VolumeSource.


        :param scale_io: The scale_io of this V1VolumeSource.  # noqa: E501
        :type: V1ScaleIOVolumeSource
        """

        self._scale_io = scale_io

    @property
    def secret(self):
        """Gets the secret of this V1VolumeSource.  # noqa: E501


        :return: The secret of this V1VolumeSource.  # noqa: E501
        :rtype: V1SecretVolumeSource
        """
        return self._secret

    @secret.setter
    def secret(self, secret):
        """Sets the secret of this V1VolumeSource.


        :param secret: The secret of this V1VolumeSource.  # noqa: E501
        :type: V1SecretVolumeSource
        """

        self._secret = secret

    @property
    def storageos(self):
        """Gets the storageos of this V1VolumeSource.  # noqa: E501


        :return: The storageos of this V1VolumeSource.  # noqa: E501
        :rtype: V1StorageOSVolumeSource
        """
        return self._storageos

    @storageos.setter
    def storageos(self, storageos):
        """Sets the storageos of this V1VolumeSource.


        :param storageos: The storageos of this V1VolumeSource.  # noqa: E501
        :type: V1StorageOSVolumeSource
        """

        self._storageos = storageos

    @property
    def vsphere_volume(self):
        """Gets the vsphere_volume of this V1VolumeSource.  # noqa: E501


        :return: The vsphere_volume of this V1VolumeSource.  # noqa: E501
        :rtype: V1VsphereVirtualDiskVolumeSource
        """
        return self._vsphere_volume

    @vsphere_volume.setter
    def vsphere_volume(self, vsphere_volume):
        """Sets the vsphere_volume of this V1VolumeSource.


        :param vsphere_volume: The vsphere_volume of this V1VolumeSource.  # noqa: E501
        :type: V1VsphereVirtualDiskVolumeSource
        """

        self._vsphere_volume = vsphere_volume

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
        if issubclass(V1VolumeSource, dict):
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
        if not isinstance(other, V1VolumeSource):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
