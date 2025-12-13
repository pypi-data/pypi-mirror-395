"""Functions for working with Datastores"""

import contextlib
import gzip
import hashlib
import json
import pathlib
import tarfile
import tempfile

import libcloud.storage
from libcloud.storage.types import ObjectDoesNotExistError, Provider

from oocli import config
from oocli.data import DataStore, Run


def _rclone_environment(datastore):
    """Environment configuration needed to connect to the given datastore"""
    match datastore.provider:
        case "scaleway":
            credentials = config.scaleway_credentials()
            return (
                "RCLONE_CONFIG_REMOTE_TYPE=s3 "
                f"RCLONE_CONFIG_REMOTE_ACCESS_KEY_ID={credentials['SCW_ACCESS_KEY']} "
                f"RCLONE_CONFIG_REMOTE_SECRET_ACCESS_KEY={credentials['SCW_SECRET_KEY']} "
                f"RCLONE_CONFIG_REMOTE_REGION={datastore.region} "
                f"RCLONE_CONFIG_REMOTE_ENDPOINT=s3.{datastore.region}.scw.cloud "
            )
        case "gcp":
            credentials = config.gcp_credentials()
            return (
                "RCLONE_CONFIG_REMOTE_TYPE=gcs "
                f"RCLONE_CONFIG_REMOTE_SERVICE_ACCOUNT_CREDENTIALS='{json.dumps(credentials)}' "
                "RCLONE_CONFIG_REMOTE_BUCKET_POLICY_ONLY=true "
            )
        case _:
            raise RuntimeError(
                f"{datastore.provider}' is not a supported datastore provider"
            )


def mount_command(datastore: DataStore, path: str, target: str):
    """Command to mount the datastore"""
    return (
        f"{_rclone_environment(datastore)} "
        "rclone"
        " --read-only"
        " --log-systemd mount"
        " --poll-interval 0"
        " --cache-dir /var/rclone"
        " --dir-cache-time 1h"
        " --vfs-cache-mode full"
        " --vfs-cache-min-free-space 5G"
        " --vfs-cache-max-age 1d"
        " --vfs-cache-poll-interval 30s"
        " --vfs-read-ahead 128M"
        f" remote:{pathlib.Path(datastore.bucket) / path}"
        f" {target}"
    )


def copy_source_command(run: Run, target: str):
    """Command to copy a run's source code to the target location"""
    if run.commit_sha is None:
        return ""

    source_tar = pathlib.Path(run.datastore.bucket) / f"{run.commit_sha}.tar.gz"
    return (
        f"{_rclone_environment(run.datastore)} "
        f"rclone cat remote:{source_tar} | tar xz -C {target}"
    )


def podman_args(run: Run):
    """Extra podman arguments needed for the given run"""
    args = [f"-v /mnt/{i.sha}:/{i.sha}:ro" for i in run.inputs]
    args.append("-v /mnt/output:/output")
    args.append("-v /mnt/workspace:/workspace")
    return " ".join(args)


def store_output_command(run: Run, path: str):
    """Command to store the run's output files"""
    return (
        f"{_rclone_environment(run.datastore)} "
        f"rclone sync {path} remote:{pathlib.Path(run.datastore.bucket) / run.sha} "
    )


def store_log_command(run: Run):
    """Command to store the run's logs"""
    log_file = f"{run.sha}.log.gz"
    return (
        "journalctl --output=json | gzip | "
        f"{_rclone_environment(run.datastore)} "
        f"rclone rcat remote:{pathlib.Path(run.datastore.bucket) / log_file} "
    )


def get_logs(run: Run):
    """Command to retreive the run's logs"""
    with tempfile.NamedTemporaryFile(suffix=".gz") as archive:
        try:
            get(run.datastore, f"{run.sha}.log.gz", archive.name)
        except ObjectDoesNotExistError:
            raise RuntimeError(f"No log found for {run.short_sha}") from None
        with gzip.open(archive) as f:
            return f.readlines()


def _get_bucket(datastore: DataStore):
    match datastore.provider:
        case "scaleway":
            Driver = libcloud.storage.providers.get_driver(datastore.provider)
            credentials = config.scaleway_credentials()
            driver = Driver(
                credentials["SCW_ACCESS_KEY"],
                credentials["SCW_SECRET_KEY"],
                region=datastore.region,
            )
        case "gcp":
            Driver = libcloud.storage.providers.get_driver(Provider.GOOGLE_STORAGE)
            credentials = config.gcp_credentials()
            driver = Driver(
                credentials["client_email"],
                credentials,
                project=credentials["project_id"],
            )
        case _:
            raise RuntimeError(
                f"{datastore.provider}' is not a supported datastore provider"
            )
    return driver.get_container(datastore.bucket)


def list_contents(datastore: DataStore, prefix: str):
    """List the datastore's files with the given prefix"""
    bucket = _get_bucket(datastore)
    return [i.name.removeprefix(prefix) for i in bucket.list_objects(prefix=prefix)]


def put(datastore: DataStore, path: str, target: str):
    """Store a file in the datastore"""
    bucket = _get_bucket(datastore)
    bucket.upload_object(path, target)


def get(datastore: DataStore, path: str, target: str):
    """Retreive a file from the datastore"""
    bucket = _get_bucket(datastore)
    bucket.get_object(path).download(target, overwrite_existing=True)


def exists(datastore: DataStore, path: str | None = None):
    """Does the datastore exits, and if a path is given, does it also exist"""
    try:
        bucket = _get_bucket(datastore)
    except libcloud.storage.types.ContainerDoesNotExistError:
        return False

    if path is not None:
        try:
            bucket.get_object(path)
        except libcloud.storage.types.ObjectDoesNotExistError:
            return False

    return True


def store_source(datastore: DataStore, repository, commit, *, allow_dirty=False):
    """Store source code in datastore

    Args:
        datastore: The datastore to store to
        repository: The Git repository holding the source
        commit: The commit to store, if None, HEAD is used
        allow_dirty: Allow and include changes in the working director
    """
    file_name = lambda s: f"{s}.tar.gz"
    with tempfile.NamedTemporaryFile(suffix=".tar.gz") as f:
        if commit is None and repository.is_dirty():
            with open(f.name, "wb") as fileobj:
                # set mtime and filename for reproducable archives
                with gzip.GzipFile(
                    fileobj=fileobj, mode="wb", mtime=0, filename=""
                ) as gzipobj:
                    with tarfile.open(fileobj=gzipobj, mode="w") as tarobj:
                        for source_file in repository.git.ls_files().splitlines():
                            with contextlib.suppress(FileNotFoundError):
                                tarobj.add(source_file)
            with open(f.name, "rb") as fileobj:
                digest = hashlib.file_digest(fileobj, "sha256")
            source = "dirty~" + digest.hexdigest()
            if not exists(datastore, file_name(source)):
                put(datastore, f.name, file_name(source))
        else:
            source = repository.commit("HEAD" if commit is None else commit).hexsha
            if not exists(datastore, file_name(source)):
                repository.git.archive(source, "--output", f.name)
                put(datastore, f.name, file_name(source))
    return source
