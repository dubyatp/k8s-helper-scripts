# K8S helper scripts

This repo contains various k8s helper scripts I've created to reduce the burden of tedious tasks maintaining my kubernetes cluster. 

Most of them aren't too customizable by default (but certainly can be edited for your needs), there may be a limited amount of variable settings such as namespaces

Most of my scripts are in Python since it's my go-to quick-and-dirty scripting language. Unless stated otherwise, the only dependency would be the [official Kubernetes Python library](https://github.com/kubernetes-client/python) which is available on [PyPI](https://pypi.org/project/kubernetes/)

*Full disclosure: I do use Claude Code but mostly for debugging and cleaning up my spaghetti code after it's already written. 
I like to write my own code for functionality but let AI make it reliable and look somewhat presentable :-)*

### Disclaimer
**All these scripts are MIT licensed and are distributed with NO WARRANTY. I am not liable for anything that happens to your cluster and/or production environment** 

As a good practice, you should thoroughly review *any* script before running it in your environment. 

I do try to include a final confirmation prompt with proposed changes (especially when it comes to deleting resources), but you should never blindly trust some random guy on GitHub to do that (I know I wouldn't 😊)

## Scripts

| Script | Description | Notes
| ------ | ----------- | -----
| [cleanup-velero-resource-labels.py](./cleanup-velero-restore-labels.py) | Cleans up the `velero.io/backup-name` and `velero.io/restore-name` labels given to resources restored by Velero. | Built to work cluster-wide but not difficult to have it scoped to a specific namespace. 