"""o-o command line interface"""

import contextlib
import functools
import io
import pathlib
import re
import tarfile
import tempfile
import time

import asciidag.graph
import asciidag.node
import dotenv
import git
import pendulum
import typer
from pydantic import ValidationError
from rich import padding
from rich.console import Console
from rich.markup import escape
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from oocli import clitools, config, data, datastores, projects, runs, tags

app = typer.Typer(
    add_completion=False,
    rich_markup_mode="markdown",
    pretty_exceptions_show_locals=False,
)

console = Console(
    highlight=False,
    theme=Theme(
        {
            "info": "dim cyan",
            "warning": "magenta",
            "danger": "bold red",
            "sha": "yellow",
        }
    ),
)
print = console.print
dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv(usecwd=True))


def command(*args, **kwargs):
    """Wrap the typer command for uncaught exception handling"""

    def decorator(func):
        @app.command(*args, **kwargs)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (typer.BadParameter, typer.Exit):
                raise
            except ValidationError as e:
                error = clitools.format_validation_error(e)
                print(f"[danger]{e.__class__.__name__}:[/danger] {error}")
                raise typer.Exit(1) from None
            except Exception as e:
                print(f"[danger]{e.__class__.__name__}:[/danger] {e}")
                raise typer.Exit(1) from None

        return wrapper

    return decorator


@command("cp")
def cp_command(
    sources: list[str] = typer.Argument(..., hidden=True, metavar="SOURCE..."),
    destination: str = typer.Argument(..., hidden=True, metavar="DESTINATION"),
    datastore: str | None = typer.Option(
        None,
        "--datastore",
        "-d",
        show_default=False,
        help="Override default datastore.",
        rich_help_panel="Options for uploads",
    ),
    message: str | None = typer.Option(
        None,
        "--message",
        "-m",
        show_default=False,
        help="A description of the upload.",
        rich_help_panel="Options for uploads",
    ),
    project: str | None = typer.Option(
        None,
        "--project",
        "-p",
        help="Override configured project.",
        show_default=False,
    ),
    copy_tags: list[str] = typer.Option(
        [],
        "--tag",
        "-t",
        help="Tag the upload with the given tag(s).",
        rich_help_panel="Options for uploads",
    ),
):
    """Copy files to and from datastores.

    Copy SOURCE to DESTINATION, or multiple SOURCE(s) to DESTINATION directory,
    where SOURCE and/or DESTINATION are o-o datastore locations. For example, to
    upload a file to o-o:

        $ o-o cp --message "Importing data" data.txt o://output/

    Uploading creates a dummy run where the uploaded files are ouputs to be
    used as inputs to other runs.

        $ o-o run --list
        ...
        fojaopi1t5 Importing data

    Outputs from any run (including our example upload above) can also be
    downloaded:

        $ o-o cp o://fojaopi1t5/data.txt .
    """
    project = projects.get_name(project)

    if len(sources) > 1 and not destination.endswith("/"):
        print(
            "[warning]Destination must be a directory with multiple sources[/warning]"
        )
        raise typer.Exit(1)

    oo_path_pattern = re.compile(rf"^o://(?P<sha>{tags.PATTERN})/(?P<path>\S*)")
    match = oo_path_pattern.match(destination)
    if match:
        try:
            datastore = config.get_value("datastores", datastore)
        except ValueError as e:
            raise typer.BadParameter(str(e), param_hint=["--datastore", "-d"]) from None

        if match["sha"] != "output":
            print(
                f"[warning]Cannot write to {destination}, only o://output/ and local destinations are supported[/warning]"
            )
            raise typer.Exit(1)

        message = message or clitools.prompt_for_message(
            default="Copying files into datastore",
        )
        if not message:
            print("[warning]Aborting due to empty message.[/warning]")
            raise typer.Exit(1)

        run, _ = runs.create(
            command=["cp"] + sources + [destination],
            commit_sha=None,
            datastore=datastore,
            environment=data.Environment(
                name="cp",
                provider="local",
                image="None",
                machinetype="None",
                region="None",
            ),
            message=message,
            project=project,
            tags=copy_tags,
        )

        try:
            destination_path = pathlib.Path(run.sha) / match["path"]
            destination_is_dir = match["path"].endswith("/") or match["path"] == ""

            with clitools.TaskDisplay(console) as tasks:
                for i, source in enumerate(sources):
                    tasks.set_current(
                        f"[{i+1}/{len(sources)}] copying {source} -> {destination}"
                    )
                    match = oo_path_pattern.match(source)
                    if match:
                        print(
                            f"[warning]Copying between datastores ({source} -> {destination}) not supported[/warning]"
                        )
                        raise typer.Exit(1)
                    else:
                        source_path = pathlib.Path(source)
                        if destination_is_dir:
                            datastores.put(
                                datastore,
                                source_path.as_posix(),
                                (destination_path / source_path.name).as_posix(),
                            )
                        else:
                            datastores.put(
                                datastore,
                                source_path.as_posix(),
                                destination_path.as_posix(),
                            )
        except KeyboardInterrupt:
            runs.completed(run, exit_status=130)
            raise
        except Exception:
            runs.completed(run, exit_status=1)
            raise
        else:
            runs.completed(run, exit_status=0)

    else:
        if datastore is not None:
            print("[info]Datastore provided, but is not used for downloads.[/info]")
        if message is not None:
            print("[info]Message provided, but is not used for downloads.[/info]")
        if copy_tags:
            print("[info]Tag provided, but is not used for downloads.[/info]")
        destination_path = pathlib.Path(destination)
        with clitools.TaskDisplay(console) as tasks:
            for i, source in enumerate(sources):
                tasks.set_current(
                    f"[{i+1}/{len(sources)}] copying {source} -> {destination}"
                )
                match = oo_path_pattern.match(source)
                if match:
                    source_run = runs.read(project, match["sha"])
                    source_path = pathlib.Path(source_run.sha) / match["path"]
                    if destination_path.is_dir():
                        datastores.get(
                            source_run.datastore,
                            source_path.as_posix(),
                            (destination_path / source_path.name).as_posix(),
                        )
                    else:
                        datastores.get(
                            source_run.datastore,
                            source_path.as_posix(),
                            destination_path.as_posix(),
                        )
                else:
                    print(
                        f"[warning]Copying from local file to local file ({source} -> {destination}) not supported[/warning]"
                    )
                    raise typer.Exit(1)


@command("diff")
def diff_command(
    left: str = typer.Argument(..., hidden=True, metavar="RUN"),
    right: str = typer.Argument(..., hidden=True, metavar="RUN"),
    project: str | None = typer.Option(
        None,
        "--project",
        "-p",
        help="Override configured project.",
        show_default=False,
    ),
):
    """Show code changes between runs."""
    project = projects.get_name(project)
    left, right = [runs.read(project, r) for r in [left, right]]
    runs_without_source = [r.short_sha for r in [left, right] if r.commit_sha is None]
    if runs_without_source:
        raise typer.BadParameter(
            f"Run(s) {' and '.join(runs_without_source)} did not include source code"
        )

    if left.commit_sha == right.commit_sha:
        return

    with tempfile.TemporaryDirectory() as directory:
        directory = pathlib.Path(directory)

        with clitools.TaskDisplay(console) as tasks:
            for run in [left, right]:
                tasks.set_current(f"Downlading {run.short_sha} source...")
                source_archive = f"{run.commit_sha}.tar.gz"
                datastores.get(
                    run.datastore,
                    source_archive,
                    directory / source_archive,
                )
                with tarfile.open(directory / source_archive) as tar:
                    tar.extractall(directory / run.short_sha)

        with contextlib.chdir(directory):
            clitools.print_diffs(
                pathlib.Path(left.short_sha),
                pathlib.Path(right.short_sha),
                print_fn=console.print,
            )


@command("log")
def log_command(
    run: str = typer.Argument(..., hidden=True),
    max_lines: int = typer.Option(200, help="Maximum number of lines."),
    show_all: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Show all system logged messages, not just from the job.",
    ),
    timestamps: bool = typer.Option(
        False,
        "--timestamps",
        help="Show timestamps in output.",
    ),
    project: str | None = typer.Option(
        None,
        "--project",
        "-p",
        help="Override configured project.",
        show_default=False,
    ),
):
    """Show run output."""
    project = projects.get_name(project)
    try:
        for log in runs.connect(
            runs.read(project, run), max_lines=max_lines, show_all=show_all
        ):
            message = escape(log.message)
            if timestamps:
                timestamp = log.timestamp.in_tz(pendulum.local_timezone())
                timestamp = timestamp.format("L LTS")
                message = f"[dim]{timestamp}[/dim] {message}"
            print(message, highlight=False)
    except runs.RunFinished as exception:
        raise typer.Exit(exception.exit_code) from None


@command("login")
def login_command(
    host: str = typer.Option(
        config.DEFAULT_HOST,
        "--host",
        "-h",
        help="Override default host.",
    ),
):
    """Login to o-o."""
    host = host.rstrip("/")
    print(f"Visit {host}/activate")
    token = Prompt.ask("Paste token", console=console, password=True)
    while True:
        sshkey = Prompt.ask(
            "Enter ssh key location",
            console=console,
            default="~/.ssh/id_ed25519",
        )
        sshkey = pathlib.Path(sshkey).expanduser()
        if not sshkey.exists():
            print(f"[danger]ssh key {sshkey} not found")
        else:
            break
    config.write(token=token, host=host, sshkey=sshkey.as_posix())


@command("project")
def project_command():
    """List projects."""
    for project in projects.read_all():
        print(project)


@command("run")
def run_command(
    command: list[str] = typer.Argument(
        [],
        hidden=True,
        metavar="-- COMMAND [ARGS...]",
        show_default=False,
    ),
    list_runs: bool = typer.Option(
        False,
        "--list",
        "-l",
        help="List runs and exit (default if no COMMAND is given).",
    ),
    datastore: str | None = typer.Option(
        None,
        "--datastore",
        "-d",
        show_default=False,
        help="Override default datastore.",
    ),
    environment: str | None = typer.Option(
        None,
        "--environment",
        "-e",
        show_default=False,
        help="Override default environment.",
    ),
    message: str | None = typer.Option(
        None,
        "--message",
        "-m",
        show_default=False,
        help="A description of the run.",
    ),
    project: str | None = typer.Option(
        None,
        "--project",
        "-p",
        help="Override configured project.",
        show_default=False,
    ),
    run_tags: list[str] = typer.Option(
        [],
        "--tag",
        "-t",
        help="Tag the run with the given tag(s).",
    ),
    timestamps: bool = typer.Option(
        False,
        "--timestamps",
        help="Show timestamps in output.",
    ),
    sourcecode: bool = typer.Option(
        None,
        help="Upload Git repository source code to run environment (will override configuration).",
        rich_help_panel="Git source code options",
    ),
    commit: str | None = typer.Option(
        None,
        "--commit",
        "-c",
        show_default="HEAD",
        metavar="REF",
        help="Upload source with this reference (implies --sourcecode).",
        rich_help_panel="Git source code options",
    ),
    allow_dirty: bool = typer.Option(
        False,
        "--dirty",
        help="Upload source with changes in your working tree (implies --sourcecode).",
        rich_help_panel="Git source code options",
    ),
):
    """Create or list run(s)."""
    project = projects.get_name(project)
    if list_runs or not command:
        for run in runs.read_all(project):
            print(clitools.one_line(run))
        raise typer.Exit(0)

    try:
        datastore = config.get_value("datastores", datastore)
    except ValueError as e:
        raise typer.BadParameter(str(e), param_hint=["--datastore", "-d"]) from None
    try:
        environment = config.get_value("environments", environment)
    except ValueError as e:
        raise typer.BadParameter(str(e), param_hint=["--environment", "-e"]) from None
    sourcecode = config.CachedConfig().sourcecode if sourcecode is None else sourcecode

    message = message or clitools.prompt_for_message()
    if not message:
        print("[warning]Aborting due to empty message.[/warning]")
        raise typer.Exit(1)

    if not datastores.exists(datastore):
        region_info = f" in '{datastore.region}'" if datastore.region else ""
        print(
            f"[warning]Invalid datastore[/warning]: {datastore.provider} "
            f"bucket '{datastore.bucket}' does not exists{region_info}, "
            f"please create with provider"
        )
        raise typer.Exit(1)

    with clitools.TaskDisplay(console=console) as tasks:
        source = None
        if sourcecode or commit or allow_dirty:
            tasks.set_current(
                f"Packaging git commit {commit or 'HEAD'}"
                f"{' with working directory changes' if allow_dirty else ''}...",
            )
            try:
                repo = git.Repo("./")
                if commit is not None and allow_dirty:
                    raise typer.BadParameter(
                        "--commit cannot be used with --dirty.",
                    )
                if commit is None and repo.is_dirty() and not allow_dirty:
                    raise typer.BadParameter(
                        "You have uncommitted changes, either commit changes or use --dirty / --commit"
                    )
                source = datastores.store_source(
                    datastore, repo, commit, allow_dirty=allow_dirty
                )
            except git.InvalidGitRepositoryError:
                param_hint = []
                if sourcecode:
                    param_hint.append("--sourcecode")
                if commit:
                    param_hint.append("--commit")
                if allow_dirty:
                    param_hint.append("--dirty")
                raise typer.BadParameter(
                    "connot be used, not in Git repositoriy",
                    param_hint=param_hint,
                ) from None
            except git.BadName:
                if commit is not None:
                    raise typer.BadParameter(
                        f"ref '{commit}' not found.",
                        param_hint=["--commit", "-c"],
                    ) from None
                raise

        run = None
        try:
            tasks.set_current("Creating run...")
            run, key = runs.create(
                command=command,
                commit_sha=source,
                datastore=datastore,
                environment=environment,
                message=message,
                project=project,
                tags=run_tags,
            )
            if run.inputs:
                tasks.set_current("Waiting for input(s) to complete...")
                runs.wait_for_inputs(run)
            while True:
                try:
                    tasks.set_current(f"Starting {environment.provider} environment...")
                    runs.start(run, key)
                except runs.EnvironmentNotAvailable as e:
                    tasks.set_current(f"{e}, retrying in 60s...")
                    time.sleep(60)
                else:
                    break
        except BaseException as e:
            if run is not None:
                tasks.set_current(
                    f"Run cancelled ({e.__class__.__name__}), stopping {environment.provider} environment..."
                )
                try:
                    runs.kill(run)
                except Exception as e:
                    print(
                        f"[warning]Error occurred while stopping environment: {e}[/warning]"
                    )
            raise

        try:
            tasks.set_current(f"Running {run.short_sha}...")
            log_command(
                run.sha,
                max_lines=None,
                show_all=False,
                timestamps=timestamps,
                project=project,
            )
        except KeyboardInterrupt:
            print(
                f"[info]Exiting, but job is still running, reconnect with 'o-o log {run.short_sha}'[/info]"
            )
            raise


@command("show")
def show_command(
    run: str = typer.Argument(..., hidden=True),
    extra: bool = typer.Option(
        False,
        "--extra",
        "-e",
        help="Show extra info (full command, datastore, environment).",
    ),
    inputs: bool = typer.Option(False, "--inputs", "-i", help="Show inputs."),
    outputs: bool = typer.Option(False, "--outputs", "-o", help="Show outputs."),
    project: str | None = typer.Option(
        None,
        "--project",
        "-p",
        help="Override configured project.",
        show_default=False,
    ),
):
    """Show run details."""
    project = projects.get_name(project)
    run = runs.read(project, run)
    print(
        f"[sha]Run {run.sha}",
        f"[sha]([bold]{', '.join(run.tags)}[/bold])" if run.tags else "",
    )

    grid = Table.grid()
    grid.add_column()
    grid.add_column()
    grid.add_row("Creator: ", f"{run.creator}")
    if run.commit_sha is not None:
        grid.add_row("Commit: ", f"{run.commit_sha}")
    grid.add_row(
        "Started: ",
        f"{run.started.in_tz(pendulum.local_timezone()).to_rss_string()}",
    )
    if run.ended is not None:
        msg = f"{run.ended.in_tz(pendulum.local_timezone()).to_rss_string()}"
        if run.exit_status != 0:
            msg = msg + f" [red][{run.exit_status}][/red]"
        grid.add_row("Ended: ", msg)
    grid.add_row("Command: ", Text(" ".join(run.command), no_wrap=not extra))
    if extra:
        grid.add_row(
            "Environment: ",
            f"{run.environment.name} "
            f"({run.environment.provider} machinetype={run.environment.machinetype} image={run.environment.image})",
        )
        grid.add_row(
            "Datastore: ",
            f"{run.datastore.name} "
            f"({run.datastore.provider} bucket={run.datastore.bucket})",
        )
    print(grid, highlight=False)
    print(padding.Padding(run.message, pad=(1, 0, 0, 4)))
    print()

    if inputs:
        node_table = {}

        def _graph_inputs(inputs):
            result = []
            for i in inputs:
                if i.sha in node_table:
                    result.append(node_table[i.sha])
                else:
                    new_node = asciidag.node.Node(
                        clitools.one_line(i),
                        parents=_graph_inputs(i.inputs),
                    )
                    result.append(new_node)
                    node_table[i.sha] = new_node
            return result

        print("Inputs:")
        if run.inputs:
            s = io.StringIO()
            graph = asciidag.graph.Graph(s)
            graph.show_nodes(
                [asciidag.node.Node("", parents=_graph_inputs(run.inputs))]
            )
            for line in s.getvalue().splitlines()[1:]:
                print("  " + re.sub(r"\* ", "o ", line))
        print()

    if outputs:
        print("Output files:")
        for o in runs.outputs(run):
            print(f"  {o}")
        print()


@command("stop")
def stop_command(
    run: str = typer.Argument(..., hidden=True),
    kill: bool = typer.Option(False, "--kill", "-k", help="Terminate the environment."),
    project: str | None = typer.Option(
        None,
        "--project",
        "-p",
        help="Override configured project.",
        show_default=False,
    ),
):
    """Stop a run."""
    project = projects.get_name(project)
    run = runs.read(project, run)
    with clitools.TaskDisplay(console) as tasks:
        if kill:
            tasks.set_current(f"Killing {run.short_sha}...")
            runs.kill(run)
        else:
            tasks.set_current(f"Stopping {run.short_sha}...")
            runs.stop(run)


@command("tag")
def tag_command(
    name: str = typer.Argument(default=None, hidden=True, metavar="NAME"),
    run: str = typer.Argument(default=None, hidden=True, metavar="RUN"),
    list_tags: bool = typer.Option(
        False,
        "--list",
        "-l",
        help="List tags and exit (default if NAME and RUN is not given).",
    ),
    project: str | None = typer.Option(
        None,
        "--project",
        "-p",
        help="Override configured project.",
        show_default=False,
    ),
):
    """Create or list run tags."""
    project = projects.get_name(project)
    if list_tags or (not name and not run):
        for tag in tags.read_all(project):
            print(tag)
        return

    if run and name:
        tags.create(name, run, project=project)
    else:
        raise typer.BadParameter(
            "NAME and RUN required when creating a tag",
        )


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        help="Show version and exit.",
        callback=clitools.print_version_and_exit,
    ),
):
    """A command line interface for running cloud jobs."""


if __name__ == "__main__":
    app()
