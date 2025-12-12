from __future__ import annotations

from wexample_filestate.item.file.yaml_file import YamlFile
from wexample_filestate_git.remote.github_remote import GithubRemote
from wexample_helpers.decorator.base_class import base_class


@base_class
class FlutterPubspecYamlFile(YamlFile):
    def get_dependencies_versions(
        self, optional: bool = False, group: str = "dev"
    ) -> dict[str, str]:
        config = self.read_config()

        dependencies = config.search(path="dependencies").get_dict_or_default(
            default={}
        )
        dev_dependencies = config.search(path="dev_dependencies").get_dict_or_default(
            default={}
        )

        merged = dict(dependencies)

        if group == "dev":
            merged.update(dev_dependencies)

        return merged

    def dumps(self, content: dict | None = None) -> str:
        workdir = self.get_parent_item()

        # Always have a dict
        content = content or {}

        # Always set the package name
        content["name"] = workdir.get_package_name()
        content["version"] = workdir.get_project_version()

        # Get repo remote URL (fallback: origin)
        repo_url = workdir.git_run(
            cmd=[
                "remote",
                "get-url",
                workdir._get_deployment_remote_name() or "origin",
            ],
            capture=True,
        ).stdout.strip()

        # Auto-fill URLs if this is a GitHub repo
        if GithubRemote.is_github_repo(repo_url):
            resolved_repo_url = GithubRemote.resolve_url_from_repo_url(repo_url)

            if resolved_repo_url:
                # Fill homepage if missing
                content.setdefault("homepage", resolved_repo_url)

                # Fill repository if missing
                content.setdefault("repository", resolved_repo_url)

                # Fill issue tracker if missing
                content.setdefault("issue_tracker", f"{resolved_repo_url}/issues")

        return super().dumps(content)
