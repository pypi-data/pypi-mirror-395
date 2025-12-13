"""Functions for working with Runs"""

import collections
import json
import re
import shlex
import textwrap
import time

import paramiko
import pendulum
import requests
from libcloud.compute.deployment import MultiStepDeployment

from oocli import config, datastores, services, tags
from oocli.data import Environment, LogMessage, Run
from oocli.libcloudfixes import libcloud


def get_driver(environment: Environment):
    """Get libcloud driver for environment"""
    match environment.provider:
        case "gcp":
            Driver = libcloud.compute.providers.get_driver(
                libcloud.compute.types.Provider.GCE
            )
            credentials = config.gcp_credentials()
            driver = Driver(
                credentials["client_email"],
                credentials,
                project=credentials["project_id"],
                datacenter=environment.region,
            )
        case libcloud.compute.types.Provider.SCALEWAY:
            Driver = libcloud.compute.providers.get_driver(environment.provider)
            credentials = config.scaleway_credentials()
            driver = Driver(
                credentials["SCW_DEFAULT_ORGANIZATION_ID"],
                credentials["SCW_SECRET_KEY"],
            )
        case _:
            raise RuntimeError(
                f"'{environment.provider}' is not a supported environment provider"
            )
    return driver


def safe_command(run: Run):
    """Get a properly escaped command for the given run"""
    oo_path_pattern = re.compile(rf"(?P<space>\s)o://(?P<input>{tags.PATTERN})/")

    def repl(m):
        match m["input"]:
            case "output":
                return f"{m['space']}/output/"
            case i:
                i = read(run.project, i)
                return f"{m['space']}/{i.sha}/"

    return shlex.quote(oo_path_pattern.sub(repl, " ".join(run.command)))


def create(*, project, environment, datastore, **kwargs):
    """Create a new run"""
    assert "sha" not in kwargs
    assert "started" not in kwargs
    assert "ended" not in kwargs
    assert "error" not in kwargs
    assert "inputs" not in kwargs

    data = {
        "project": project,
        "environment": environment.model_dump(),
        "datastore": datastore.model_dump(),
        **kwargs,
    }
    response = requests.post(
        f"{config.CachedConfig().apiurl}/runs/{project}",
        data=json.dumps(data),
        headers={"X-API-Key": config.CachedConfig().token},
    )
    if response.status_code == 422:
        raise RuntimeError(response.text)
    response.raise_for_status()
    sha = response.json()["sha"]
    key = response.json()["key"]
    return read(project, sha), key


class EnvironmentNotAvailable(Exception):
    """Raised when environment is currently not available"""


def start(run, key):
    """Start a run"""
    match run.environment.provider:
        case "gcp":
            _start_gcp(run, key)
        case libcloud.compute.types.Provider.SCALEWAY:
            _start_scaleway(run, key)
        case _:
            raise RuntimeError(
                f"'{run.environment.provider}' is not a supported environment provider"
            )


def _start_gcp(run: Run, key: str):
    driver = get_driver(run.environment)
    private_key = config.CachedConfig().sshkey
    public_key = private_key.with_name(f"{private_key.name}.pub")
    metadata = {
        "items": [
            {
                "key": "ssh-keys",
                "value": f"root: {public_key.read_text().strip()}",
            },
        ],
    }

    sizes = driver.list_sizes()
    size = next((s for s in sizes if s.name == run.environment.machinetype), None)
    if size is None:
        raise RuntimeError(
            f"{run.environment.machinetype} not available in {run.environment.region}"
        )
    podman_args = datastores.podman_args(run)
    if size.extra["accelerators"]:
        image = driver.ex_get_image_from_family(
            "ubuntu-accelerator-2404-amd64-with-nvidia-570",
            ("ubuntu-os-accelerator-images",),
        )
        setup = textwrap.dedent(
            """\
            curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
            curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
                sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
                tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
            apt-get -y update
            apt-get install -y \
                nvidia-container-toolkit \
                nvidia-container-toolkit-base \
                libnvidia-container-tools \
                libnvidia-container1
            nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml
            """
        )
        podman_args += " --device nvidia.com/gpu=all"
        on_host_maintenance = "TERMINATE"
    else:
        image = driver.ex_get_image_from_family(
            "ubuntu-2404-lts-amd64", ("ubuntu-os-cloud",)
        )
        setup = ""
        on_host_maintenance = None

    teardown = textwrap.dedent(
        """\
        NAME=$(curl -X GET http://metadata.google.internal/computeMetadata/v1/instance/name -H 'Metadata-Flavor: Google')
        ZONE=$(curl -X GET http://metadata.google.internal/computeMetadata/v1/instance/zone -H 'Metadata-Flavor: Google')
        gcloud --quiet beta compute instances delete $NAME --zone=$ZONE --no-graceful-shutdown
        """
    )

    deployments = MultiStepDeployment(
        [
            services.mount_inputs(run.inputs),
            services.oo_context(run, key=key, setup=setup, teardown=teardown),
            services.job(
                command=safe_command(run),
                image=run.environment.image,
                podman_args=podman_args,
            ),
            services.start(),
        ]
    )

    try:
        driver.deploy_node(
            name=_node_name(run),
            ssh_key=config.CachedConfig().sshkey.as_posix(),
            size=size,
            image=image,
            ex_metadata=metadata,
            deploy=deployments,
            ex_service_accounts=[{"email": "default", "scopes": ["compute-rw"]}],
            ex_disk_size=int(run.environment.size.to("GB") + 0.5),
            ex_on_host_maintenance=on_host_maintenance,
        )
    except libcloud.common.google.GoogleBaseError as e:
        if e.code == "ZONE_RESOURCE_POOL_EXHAUSTED":
            raise EnvironmentNotAvailable(
                f"{run.environment.machinetype} not available in {run.environment.region}"
            ) from None
        else:
            raise


def _start_scaleway(run: Run, key: str):
    driver = get_driver(run.environment)
    sizes = driver.list_sizes(region=run.environment.region)
    size = next((s for s in sizes if s.name == run.environment.machinetype), None)
    if size is None:
        raise EnvironmentNotAvailable(
            f"{run.environment.machinetype} not available in {run.environment.region}"
        )

    # Get around libcloud checks
    size.extra["max_disk"] = run.environment.size.to("GB") + 21

    ex_volumes = {"0": {"size": run.environment.size, "volume_type": "sbs_volume"}}

    gpus = size.extra["gpus"] > 0
    podman_args = datastores.podman_args(run)
    DuckImage = collections.namedtuple("Image", ["id", "extra"])
    if gpus:
        image = DuckImage(extra={"size": 20}, id="ubuntu_noble_gpu_os_12")
        setup = "nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml"
        podman_args += " --device nvidia.com/gpu=all"
    else:
        image = DuckImage(extra={"size": 10}, id="ubuntu_noble")
        setup = ""

    scaleway_key = config.scaleway_credentials()["SCW_SECRET_KEY"]
    teardown = textwrap.dedent(
        f"""\
        ID=$(scw-metadata | grep "^ID=" | cut -d "=" -f 2)
        ZONE=$(scw-metadata | grep "^ZONE=" | cut -d "=" -f 2)
        VOLUME=$(scw-metadata | grep "^VOLUMES_0_ID=" | cut -d "=" -f 2)
        curl --fail-early \
            -X POST \
            -H "X-Auth-Token: {scaleway_key}" \
            -H "Content-Type: application/json" \
            -d '{{"volume_id": "'$VOLUME'"}}' \
            https://api.scaleway.com/instance/v1/zones/$ZONE/servers/$ID/detach-volume \
          -: \
            -X DELETE \
            --retry 5 --retry-all-errors --fail \
            -H "X-Auth-Token: {scaleway_key}" \
            https://api.scaleway.com/block/v1/zones/$ZONE/volumes/$VOLUME \
          -: \
            -X POST \
            -H "X-Auth-Token: {scaleway_key}" \
            -H "Content-Type: application/json" \
            -d '{{"action":"terminate"}}' \
            https://api.scaleway.com/instance/v1/zones/$ZONE/servers/$ID/action
        """
    )

    deployments = MultiStepDeployment(
        [
            services.mount_inputs(run.inputs),
            services.oo_context(run, key=key, setup=setup, teardown=teardown),
            services.job(
                command=safe_command(run),
                image=run.environment.image,
                podman_args=podman_args,
            ),
            services.start(),
        ]
    )

    try:
        driver.deploy_node(
            name=_node_name(run),
            region=run.environment.region,
            ssh_key=config.CachedConfig().sshkey.as_posix(),
            size=size,
            image=image,
            ex_volumes=ex_volumes,
            deploy=deployments,
        )
    except libcloud.common.exceptions.BaseHTTPError as e:
        if "resource is out of stock" in str(e):
            raise EnvironmentNotAvailable(str(e)) from None
        else:
            raise


class RunFinished(Exception):
    """Raised when run has completed the job"""

    def __init__(self, exit_code=0):
        super().__init__()
        self.exit_code = exit_code


def _log_messages(log, *, show_all=False):
    exit_pattern = re.compile(r"^o-o ExitStatus=(?P<exit_code>\w+)")
    exit_code = 0
    for line in log:
        entry = json.loads(line)
        # TODO: figure out how this is possible, sometimes getting list of ints
        if not isinstance(entry["MESSAGE"], str):
            continue

        exit_match = exit_pattern.match(entry["MESSAGE"])
        if exit_match:
            exit_code = exit_match.group("exit_code")
            match exit_match.group("exit_code"):
                case "TERM":
                    exit_code = 143
                case "KILL":
                    exit_code = 137
                case value:
                    exit_code = int(value)
            if not show_all:
                raise RunFinished(exit_code)

        if show_all or (
            entry.get("_SYSTEMD_UNIT", None) == "o-o-job.service"
            and entry.get("SYSLOG_IDENTIFIER", None) == "podman"
            and entry.get("_TRANSPORT", None) == "stdout"
        ):
            yield LogMessage(
                message=entry["MESSAGE"],
                timestamp=pendulum.from_timestamp(
                    int(entry["__REALTIME_TIMESTAMP"]) / 1000000
                ),
            )
    raise RunFinished(exit_code)


def _node_name(run: Run):
    return f"{config.CachedConfig().nodeprefix}{run.sha}"


def _get_node(run: Run):
    driver = get_driver(run.environment)
    kwargs = {}
    if run.environment.provider == libcloud.compute.types.Provider.SCALEWAY:
        kwargs["region"] = run.environment.region

    node = next(
        (n for n in driver.list_nodes(**kwargs) if n.name == _node_name(run)),
        None,
    )
    if node is not None:
        node.extra["region"] = run.environment.region
    return node


def _get_node_ip(run: Run):
    node = _get_node(run)
    if node is None:
        raise RuntimeError(f"{run.sha} not running")
    _, ip_addresses = node.driver.wait_until_running([node])[0]
    return ip_addresses[0]


def connect(run: Run, *, max_lines=200, show_all=False):
    """Connect to a job and yield output messages"""
    if run.ended is None:
        try:
            ip = _get_node_ip(run)
            with paramiko.SSHClient() as client:
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(
                    ip,
                    username="root",
                    key_filename=config.CachedConfig().sshkey.as_posix(),
                )
                _, output, _ = client.exec_command(
                    f"journalctl --follow --lines={max_lines or 'all'} --output=json",
                )
                yield from _log_messages(output, show_all=show_all)

        except RunFinished:
            raise
        except Exception:
            try_datastore = True
        else:
            try_datastore = False
    else:
        try_datastore = True

    if try_datastore:
        output = datastores.get_logs(run)
        if max_lines is not None:
            output = output[-max_lines:]
        yield from _log_messages(output, show_all=show_all)


def stop(run):
    """Stop a running job, nicely"""
    ip = _get_node_ip(run)
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            ip,
            username="root",
            key_filename=config.CachedConfig().sshkey.as_posix(),
        )
        client.exec_command("systemctl stop o-o-job")


def kill(run: Run):
    """Stop a running job by destroying the node

    NOTE: logs and outputs will likely be lost.
    """
    node = _get_node(run)
    if node is not None:
        node.destroy()
    completed(run, exit_status=137)  # Bash exit code for sigkill


def completed(run: Run, *, exit_status=0):
    """Mark the run as completed, with given exit_status"""
    response = requests.put(
        f"{config.CachedConfig().apiurl}/runs/{run.project}/{run.sha}/completed",
        headers={"X-API-Key": config.CachedConfig().token},
        params={"exit_status": str(exit_status)},
    )
    if response.status_code == 422:
        if "already completed" in response.text:
            return
        raise RuntimeError(response.text)
    response.raise_for_status()


def read(project, run_sha):
    """Retrieve the run in the project with the given run_sha"""
    response = requests.get(
        f"{config.CachedConfig().apiurl}/runs/{project}/{run_sha}",
        headers={"X-API-Key": config.CachedConfig().token},
    )
    if response.status_code == 422:
        raise RuntimeError(response.text)
    response.raise_for_status()
    return Run.model_validate(response.json())


def read_all(project):
    """Retreive all runs in the project"""
    response = requests.get(
        f"{config.CachedConfig().apiurl}/runs/{project}",
        headers={"X-API-Key": config.CachedConfig().token},
    )
    response.raise_for_status()
    return [Run.model_validate(r) for r in response.json()]


def outputs(run: Run):
    """Retreive all the run's outputs"""
    return datastores.list_contents(run.datastore, f"{run.sha}/")


def wait_for_inputs(run: Run):
    """Wait for the run's inputs to complete successfully."""
    while True:
        errored = [
            i.short_sha
            for i in run.inputs
            if i.ended is not None and i.exit_status != 0
        ]
        if errored:
            raise RuntimeError(
                f"input(s) {errored} did not complete successfully, cannot start run"
            )

        unfinished = (i.ended is None for i in run.inputs)
        if not any(unfinished):
            break

        time.sleep(10)
        run = read(run.project, run.sha)
