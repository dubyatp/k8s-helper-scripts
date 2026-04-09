from kubernetes import client, config
from helper import identifyVolume

config.load_kube_config()

api_client = client.ApiClient()
core_api = client.CoreV1Api(api_client)

pods = []

ret = core_api.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    pod_volumes = i.spec.volumes
    backed_up_volumes = []
    if "backup.velero.io/backup-volumes" in (i.metadata.annotations or {}):
        vol_type = ""
        data = (i.metadata.annotations.get("backup.velero.io/backup-volumes")).split(",")
        for vol in data:
            for podvol in pod_volumes:
                if podvol.name == vol:
                    vol_type = identifyVolume(podvol)
            backed_up_volumes.append(f"{vol} ({vol_type})")
    pods.append({
        "namespace": i.metadata.namespace,
        "name": i.metadata.name,
        "volumes": backed_up_volumes,
        })
    

col_ns  = max(len(p["namespace"]) for p in pods) if pods else 9
col_name = max(len(p["name"]) for p in pods) if pods else 4

print(f"{'Namespace':<{col_ns}}  {'Name':<{col_name}}  Backed Up Volumes")
for p in pods:
    volumes = p["volumes"]
    first = volumes[0] if volumes else "<none>"
    print(f"{p['namespace']:<{col_ns}}  {p['name']:<{col_name}}  {first}")
    for vol in volumes[1:]:
        print(f"{'':<{col_ns}}  {'':<{col_name}}  {vol}")