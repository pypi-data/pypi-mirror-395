"""Systemd services and scripts deployed on environments"""

import textwrap

from libcloud.compute.deployment import (
    Deployment,
    MultiStepDeployment,
    ScriptDeployment,
)

from oocli import config, datastores
from oocli.data import Run


class ToFileDeployment(Deployment):
    """libcloud Deployment of contents to a target file"""

    def __init__(self, contents, target):
        self.contents = self._get_string_value(
            argument_name="contents", argument_value=contents
        )
        self.target = target

    def run(self, node, client):
        client.put(self.target, contents=self.contents)
        return node

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (
            f"<ToFileDeployment contents={self.contents[:15]}... target={self.target}>"
        )


def mount_inputs(inputs: list[Run]):
    """Deploy systemd services that mount the given inputs"""
    deployments = MultiStepDeployment()
    for i in inputs:
        location = f"/mnt/{i.sha}/"
        deployments.add(
            [
                ToFileDeployment(
                    textwrap.dedent(
                        f"""\
                        #!/usr/bin/env bash
                        {datastores.mount_command(i.datastore, i.sha, location)}
                        """
                    ),
                    f"/mount-{i.sha}.sh",
                ),
                ToFileDeployment(
                    textwrap.dedent(
                        f"""\
                        [Unit]
                        Description=rclone mount of {location}
                        After=o-o.service
                        Requires=o-o.service
                        Before=o-o-job.service
                        BindsTo=o-o-job.service
                        [Service]
                        Type=notify
                        NotifyAccess=all
                        Restart=no
                        ExecStartPre=mkdir -p {location}
                        ExecStart=bash /mount-{i.sha}.sh
                        ExecStop=/bin/fusermount -u {location}
                        [Install]
                        RequiredBy=o-o-job.service
                        """
                    ),
                    f"/etc/systemd/system/o-o-mount-{i.sha}.service",
                ),
            ]
        )
    return deployments


def oo_context(run: Run, *, key, setup="", teardown=""):
    """Deploy a systemd service that starts up and tears down the environment"""
    return MultiStepDeployment(
        [
            ToFileDeployment(
                textwrap.dedent(
                    f"""\
                    #!/usr/bin/env bash
                    export DEBIAN_FRONTEND=noninteractive
                    apt-get -y update && apt-get -y install curl podman
                    wget https://downloads.rclone.org/v1.71.1/rclone-v1.71.1-linux-amd64.deb
                    apt-get -y install ./rclone-v1.71.1-linux-amd64.deb
                    mkdir -p /mnt/output/
                    mkdir -p /mnt/workspace/
                    echo 1 > /exit_status
                    {datastores.copy_source_command(run, '/mnt/workspace/')}
                    {setup}
                    """
                ),
                "/setup.sh",
            ),
            ToFileDeployment(
                textwrap.dedent(
                    f"""\
                    #!/usr/bin/env bash
                    EXIT_STATUS=$(cat /exit_status)
                    echo o-o ExitStatus=$EXIT_STATUS

                    {datastores.store_output_command(run, '/mnt/output')}

                    curl -X PUT \
                        -H "X-API-Key: {key}" \
                        {config.CachedConfig().apiurl}/runs/{run.project}/{run.sha}/completed?exit_status=$EXIT_STATUS

                    {datastores.store_log_command(run)}

                    {teardown}
                    """
                ),
                "/teardown.sh",
            ),
            ToFileDeployment(
                textwrap.dedent(
                    """\
                    [Unit]
                    Description=setup and teardown o-o
                    Requires=multi-user.target
                    After=multi-user.target
                    BindsTo=o-o-job.service
                    [Service]
                    Type=oneshot
                    ExecStart=bash /setup.sh
                    Restart=no
                    RemainAfterExit=true
                    ExecStopPost=bash /teardown.sh
                    """
                ),
                "/etc/systemd/system/o-o.service",
            ),
        ]
    )


def job(*, command, image, podman_args=""):
    """Deploy a systemd service that runs a job"""
    return MultiStepDeployment(
        [
            ToFileDeployment(
                textwrap.dedent(
                    f"""\
                    [Unit]
                    Description=o-o job
                    After=o-o.service
                    Requires=o-o.service
                    OnFailure=o-o-failure.service
                    [Service]
                    Type=exec
                    Restart=no
                    ExecStart=podman run \
                        --entrypoint=/bin/sh \
                        --workdir=/workspace \
                        --quiet \
                        --init \
                        {podman_args} \
                        {image} \
                        -c {command}
                    ExecStopPost=bash -c 'echo $EXIT_STATUS > /exit_status'
                    """
                ),
                "/etc/systemd/system/o-o-job.service",
            ),
            ToFileDeployment(
                textwrap.dedent(
                    """\
                    [Unit]
                    Description=Stop o-o job on failure
                    [Service]
                    Type=oneshot
                    Restart=no
                    ExecStart=systemctl stop o-o-job
                    """
                ),
                "/etc/systemd/system/o-o-failure.service",
            ),
        ]
    )


def start():
    """Deploy a script that starts the job systemd service"""
    return ScriptDeployment(
        textwrap.dedent(
            """\
            #!/usr/bin/env bash
            systemctl daemon-reload
            systemctl enable /etc/systemd/system/o-o-mount-*
            systemctl start o-o-job
            """
        ),
        name="/startup.sh",
    )
