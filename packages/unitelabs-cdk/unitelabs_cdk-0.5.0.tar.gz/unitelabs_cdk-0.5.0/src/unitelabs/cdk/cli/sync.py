import json
import pathlib
import subprocess

import click

DEFAULT_BRANCH = "chore/cruft-update"


class CruftNotConfigured(Exception):
    """Cruft is not configured."""

    def __init__(self):
        msg = "Run `cruft link https://gitlab.com/unitelabs/cdk/connector-factory.git` to configure cruft."
        super().__init__(msg)


class CiCdNotConfigured(Exception):
    """CI/CD required environment variables are not present."""


@click.option(
    "--repo-url",
    envvar="REPO_API_URL",
    show_envvar=True,
    help="The git api url for the connector to be updated.",
)
@click.option(
    "--token",
    envvar="CRUFT_BOT_TOKEN",
    show_envvar=True,
    help="A git access token with API and write_repository permissions.",
)
@click.option(
    "--branch",
    default=DEFAULT_BRANCH,
    type=str,
    required=False,
    help="Explicitly name the git branch. If running without `--ci`, this will create a new branch and switch to it.",
)
@click.option(
    "--ci",
    is_flag=True,
    default=False,
    help="Run the sync as part of CI/CD. This creates an MR with the changes in the specified branch.",
)
@click.option(
    "--dry-run", is_flag=True, default=False, help="Show the changes that would be applied, without applying them."
)
@click.command()
def sync(repo_url: str, token: str, branch: str, ci: bool, dry_run: bool) -> None:
    """
    Update the current connector boilerplate.

    Check for changes to the connector-factory template and apply using `cruft update`.

    In GitLab CI/CD REPO_API_URL should follow the form "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}"
    """

    if ci:
        msg = ""
        if not repo_url:
            msg += "REPO_API_URL must be set. "
        if not token:
            msg += "CRUFT_BOT_TOKEN must be set. "
        if msg:
            msg += "CI/CD cannot run in the current state."
            raise CiCdNotConfigured(msg)

    has_changes = cruft_check()
    if not has_changes:
        click.echo("No changes to apply.")
        return

    if dry_run:
        subprocess.run(["cruft", "diff"], check=True)
        return

    if ci or (branch != DEFAULT_BRANCH and not ci):
        subprocess.run(["git", "switch", "-c", branch], check=True)

    cruft_info = json.loads(pathlib.Path("./.cruft.json").resolve().read_text())
    runner = cruft_info["context"]["cookiecutter"].get("env", "poetry")  # default poetry for older conn-factory
    subprocess.run([runner, "run", "cruft", "update", "--skip-apply-ask"], check=True)

    if ci:
        push_to_gitlab(branch, repo_url, token)


def cruft_check() -> bool:
    """
    Run `cruft check` to see if there are any updates to apply.

    Returns:
      Whether or not there are changes to the cruft template that can be applied.

    Raises:
      NotConfigured: If no `.cruft.json` file can be found.
    """

    has_changes = False
    cruft_file = pathlib.Path("./.cruft.json").resolve()

    if not cruft_file.exists():
        raise CruftNotConfigured
    try:
        subprocess.check_output(["cruft", "check"])
    except subprocess.CalledProcessError as e:
        if (
            e.returncode == 1
            and e.output == b"FAILURE: Project's cruft is out of date! Run `cruft update` to clean this mess up.\n"
        ):
            has_changes = True
        else:
            click.echo(e.output)
            raise e
    return has_changes


def push_to_gitlab(branch: str, repo_url: str, auth: str) -> None:
    """Commit and push changes, and create an MR on git."""
    cruft_info = json.loads(pathlib.Path("./.cruft.json").resolve().read_text())
    commit_sha = cruft_info["commit"][:8]
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f'"chore: cruft update to {commit_sha}"'], check=True)
    subprocess.run(["git", "push", "--set-upstream", "origin", branch], check=True)

    git_mr_args = [
        "curl",
        "-sL",
        "--header",
        f"PRIVATE-TOKEN: {auth}",
        "--data",
        f"source_branch={branch}",
        "--data",
        "target_branch=main",
        "--data",
        "title=Cruft-Update",
        "-X",
        "POST",
        f"{repo_url}/merge_requests",
    ]
    subprocess.run(git_mr_args, check=True)
