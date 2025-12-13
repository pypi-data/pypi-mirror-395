"""Adjustments and fixes to the libcloud package

* Scaleway: Handle `baremetal` no longer a VM property returned by API
* Scaleway: Add # of GPUs from API to NodeSize
* Scaleway: Switch API to zoned endpoints at `api.scaleway.com`
* Scaleway: Be sure to pass regions (aka, zone) to API in `create_node`, `destroy_node`,
    and `wait_until_running`.
* Scaleway: Try delete first in `destroy_node` before terminate, terminate fails
    with stopped nodes.
* Scaleway: Delete attached volumes when destroying node with `destroy_node`.
* Google: Use credentials file when given to GoogleStorageDriver
"""

import collections
import json

import libcloud
import libcloud.compute.drivers.scaleway
import libcloud.compute.types
import libcloud.storage.drivers.google_storage
import libcloud.storage.types
from libcloud.common.base import ConnectionUserAndKey
from libcloud.common.exceptions import BaseHTTPError
from libcloud.common.types import ProviderError
from libcloud.compute.base import NodeLocation

libcloud.compute.ssh.LIBCLOUD_PARAMIKO_SHA2_BACKWARD_COMPATIBILITY = False

# ruff: noqa: UP031


class ScalewayConnection(libcloud.compute.drivers.scaleway.ScalewayConnection):
    def request(
        self,
        action,
        params=None,
        data=None,
        headers=None,
        method="GET",
        raw=False,
        stream=False,
        region=None,
    ):
        """Fixes: Switch to using zoned API endpoints"""
        if region is None:
            raise RuntimeError("region is required for request")
        self.host = "api.scaleway.com"
        if action.lstrip("/").split("/")[0] == "volumes":
            action = f"/block/v1/zones/{region}/{action}"
        else:
            action = f"/instance/v1/zones/{region}/{action}"
        return ConnectionUserAndKey.request(
            self, action, params, data, headers, method, raw, stream
        )


class ScalewayNodeDriver(libcloud.compute.drivers.scaleway.ScalewayNodeDriver):
    connectionCls = ScalewayConnection

    def _to_size(self, name, size, availability):
        """Fixes: Handle unavailable baremetal property and add # of GPUs"""
        baremetal_missing = "baremetal" not in size
        if baremetal_missing:
            size["baremetal"] = None

        node_size = super()._to_size(name, size, availability)
        node_size.extra["gpus"] = size["gpu"]

        if baremetal_missing:
            del node_size.extra["baremetal"]

        return node_size

    def create_node(
        self,
        name,
        size,
        image,
        ex_volumes=None,
        ex_tags=None,
        region=None,
    ):
        """Fixes: Add region (aka zone) to API requests, fix volume loop"""
        data = {
            "name": name,
            "organization": self.key,
            "image": image.id,
            "volumes": ex_volumes or {},
            "commercial_type": size.id,
            "tags": ex_tags or [],
        }

        allocate_space = image.extra.get("size", 50)
        for volume in data["volumes"].values():  # change from libcloud version
            allocate_space += libcloud.compute.drivers.scaleway._to_lib_size(
                volume["size"]
            )

        while allocate_space < size.disk:
            if size.disk - allocate_space > 150:
                bump = 150
            else:
                bump = size.disk - allocate_space

            vol_num = len(data["volumes"]) + 1
            data["volumes"][str(vol_num)] = {
                "name": "%s-%d" % (name, vol_num),
                "organization": self.key,
                "size": libcloud.compute.drivers.scaleway._to_api_size(bump),
                "volume_type": "l_ssd",
            }
            allocate_space += bump

        if allocate_space > size.extra.get("max_disk", size.disk):
            range = (
                "of %dGB" % size.disk
                if size.extra.get("max_disk", size.disk) == size.disk
                else "between %dGB and %dGB"
                % (size.extra.get("max_disk", size.disk), size.disk)
            )
            raise ProviderError(
                value=(
                    "%s only supports a total volume size %s; tried %dGB"
                    % (size.id, range, allocate_space)
                ),
                http_code=400,
                driver=self,
            )

        response = self.connection.request(
            "/servers", data=json.dumps(data), region=region, method="POST"
        )
        server = response.object["server"]
        node = self._to_node(server)
        node.extra["region"] = (
            region.id if isinstance(region, NodeLocation) else region
        ) or "par1"

        # Scaleway doesn't start servers by default, let's do it
        self._action(node.id, "poweron", region=region)  # change from libcloud version

        return node

    def destroy_node(self, node):
        """Fixes

        * Add region (aka zone) to API requests
        * Try delete first before terminate in case the node is already stopped
        * Destroy attached volumes as well
        """
        region = node.extra["region"]
        retry = libcloud.utils.retry.Retry(
            (libcloud.common.exceptions.BaseHTTPError,),
            retry_delay=5,
        )

        destroyed = False
        try:
            destroyed = self.connection.request(
                f"/servers/{node.id}",
                region=region,
                method="DELETE",
            ).success()
        except BaseHTTPError:
            destroyed = False

        if not destroyed:
            destroyed = retry(self._action)(node.id, "terminate", region=region)

        if destroyed:
            DuckStorageVolume = collections.namedtuple("StorageVolume", ["id"])
            for volume in node.extra["volumes"].values():
                # could still be terminating and the volume in use, may need to retry
                retry(self.destroy_volume)(
                    DuckStorageVolume(id=volume["id"]),
                    region=region,
                )

        return destroyed

    def wait_until_running(
        self,
        nodes,  # type: List[Node]
        ex_list_nodes_kwargs=None,  # type: Optional[Dict]
        **kwargs,
    ):
        """Fixes: Add region (aka zone) to API request"""
        region = nodes[0].extra["region"]
        assert all(n.extra["region"] == region for n in nodes)
        ex_list_nodes_kwargs = ex_list_nodes_kwargs or {}
        ex_list_nodes_kwargs["region"] = region
        return super().wait_until_running(
            nodes, ex_list_nodes_kwargs=ex_list_nodes_kwargs, **kwargs
        )


del libcloud.compute.providers.DRIVERS[libcloud.compute.types.Provider.SCALEWAY]
libcloud.compute.providers.set_driver(
    libcloud.compute.types.Provider.SCALEWAY,
    "oocli.libcloudfixes",
    "ScalewayNodeDriver",
)


class GoogleStorageDriver(libcloud.storage.drivers.google_storage.GoogleStorageDriver):
    """Fixes: Use credientials file when given to GoogleStorageDriver"""

    def __init__(self, key, secret=None, credential_file=None, **kwargs):
        self.credential_file = credential_file
        super().__init__(key, secret=secret, credential_file=credential_file, **kwargs)

    def _ex_connection_class_kwargs(self):
        return {
            "credential_file": self.credential_file,
        }


del libcloud.storage.providers.DRIVERS[libcloud.storage.types.Provider.GOOGLE_STORAGE]
libcloud.storage.providers.set_driver(
    libcloud.storage.types.Provider.GOOGLE_STORAGE,
    "oocli.libcloudfixes",
    "GoogleStorageDriver",
)
