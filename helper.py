def identifyVolume(vol):
    if vol.aws_elastic_block_store is not None:
        return "awsElasticBlockStore"
    if vol.azure_disk is not None:
        return "azureDisk"
    if vol.azure_file is not None:
        return "azureFile"
    if vol.cephfs is not None:
        return "cephfs"
    if vol.cinder is not None:
        return "cinder"
    if vol.config_map is not None:
        return "configMap"
    if vol.csi is not None:
        return "csi"
    if vol.downward_api is not None:
        return "downwardAPI"
    if vol.empty_dir is not None:
        return "emptyDir"
    if vol.ephemeral is not None:
        return "ephemeral"
    if vol.fc is not None:
        return "fc"
    if vol.flex_volume is not None:
        return "flexVolume"
    if vol.flocker is not None:
        return "flocker"
    if vol.gce_persistent_disk is not None:
        return "gcePersistentDisk"
    if vol.git_repo is not None:
        return "gitRepo"
    if vol.glusterfs is not None:
        return "glusterfs"
    if vol.host_path is not None:
        return "hostPath"
    if vol.image is not None:
        return "image"
    if vol.iscsi is not None:
        return "iscsi"
    if vol.nfs is not None:
        return "nfs"
    if vol.persistent_volume_claim is not None:
        return "persistentVolumeClaim"
    if vol.photon_persistent_disk is not None:
        return "photonPersistentDisk"
    if vol.portworx_volume is not None:
        return "portworxVolume"
    if vol.projected is not None:
        return "projected"
    if vol.quobyte is not None:
        return "quobyte"
    if vol.rbd is not None:
        return "rbd"
    if vol.scale_io is not None:
        return "scaleIO"
    if vol.secret is not None:
        return "secret"
    if vol.storageos is not None:
        return "storageos"
    if vol.vsphere_volume is not None:
        return "vsphereVolume"
    return vol.name
