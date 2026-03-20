from kubernetes import client, config

config.load_kube_config()

api_client = client.ApiClient()
core_api = client.CoreV1Api(api_client)
apis_api = client.ApisApi(api_client)

all_resources = []

velero_restored_resources_to_clean = []

# Core API group (v1)
for r in core_api.get_api_resources().resources:
    all_resources.append({
        "name": r.name,
        "namespaced": r.namespaced,
        "kind": r.kind,
        "group": "",
        "version": "v1",
    })

# All named API groups (apps, batch, networking.k8s.io, etc.)
for group in apis_api.get_api_versions().groups:
    group_version = group.preferred_version.group_version  # e.g. "apps/v1"
    group_name = group.name
    try:
        result = api_client.call_api(
            f"/apis/{group_version}", "GET",
            auth_settings=["BearerToken"],
            response_type="V1APIResourceList",
            _return_http_data_only=True,
        )
        for r in result.resources:
            all_resources.append({
                "name": r.name,
                "namespaced": r.namespaced,
                "kind": r.kind,
                "group": group_name,
                "version": group.preferred_version.version,
            })
    except Exception as e:
        print(f"  [warn] skipped {group_version}: {e}")

for resource in all_resources:
    if "/" in resource["name"]:  # skip subresources like pods/log
        continue

    # Build list URL — omitting namespace prefix returns all namespaces for namespaced resources
    if resource["group"] == "":
        url = f"/api/{resource['version']}/{resource['name']}"
    else:
        url = f"/apis/{resource['group']}/{resource['version']}/{resource['name']}"

    try:
        response = api_client.call_api(
            url, "GET",
            auth_settings=["BearerToken"],
            response_type="object",
            _return_http_data_only=True,
        )
        items = response.get("items", [])
        for item in items:
            metadata = item.get("metadata", {})
            labels = metadata.get('labels') or {}
            if ("velero.io/backup-name" in labels or "velero.io/restore-name" in labels) and metadata.get('namespace') != "velero":
                velero_restored_resources_to_clean.append({
                    "kind": resource['kind'],
                    "resource_name": resource['name'],
                    "group": resource['group'],
                    "version": resource['version'],
                    "name": metadata.get('name'),
                    "namespace": metadata.get('namespace'),
                    "uid": metadata.get('uid'),
                    "labels": labels,
                })
    except Exception as e:
        msg = str(e)
        if "(404)" not in msg and "(405)" not in msg:
            print(f"[warn] could not list {resource['name']}: {e}")


if velero_restored_resources_to_clean is not None:
    print("The following resources have velero restore labels on them. Verify them and then choose to unlabel them \n")
    for item in velero_restored_resources_to_clean:
        print(f"{item['kind']}: {item['namespace']}/{item['name']}")
        if item['labels'] is not None:
            print(f"    Labels: ")
            for key, value in item['labels'].items():
                if (key == "velero.io/backup-name" or key == "velero.io/restore-name"):
                    print(f"      {key}: {value}")
            print("\n")
    answer = input("Continue to unlabel? [y/n]")
    if answer.strip().lower() != "y":
        print("Aborted")
    else:
        for item in velero_restored_resources_to_clean:
            if item["group"] == "":
                if item["namespace"]:
                    url = f"/api/{item['version']}/namespaces/{item['namespace']}/{item['resource_name']}/{item['name']}"
                else:
                    url = f"/api/{item['version']}/{item['resource_name']}/{item['name']}"
            else:
                if item["namespace"]:
                    url = f"/apis/{item['group']}/{item['version']}/namespaces/{item['namespace']}/{item['resource_name']}/{item['name']}"
                else:
                    url = f"/apis/{item['group']}/{item['version']}/{item['resource_name']}/{item['name']}"

            patch_body = {"metadata": {"labels": {
                "velero.io/backup-name": None,
                "velero.io/restore-name": None,
            }}}

            try:
                api_client.call_api(
                    url, "PATCH",
                    auth_settings=["BearerToken"],
                    response_type="object",
                    _return_http_data_only=True,
                    header_params={"Content-Type": "application/merge-patch+json"},
                    body=patch_body,
                )
                print(f"Unlabeled {item['kind']}: {item['namespace']}/{item['name']}")
            except Exception as e:
                print(f"[error] failed to unlabel {item['kind']} {item['namespace']}/{item['name']}: {e}")