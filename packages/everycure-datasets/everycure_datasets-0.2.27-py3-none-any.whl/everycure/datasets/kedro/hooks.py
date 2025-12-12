import logging
import shutil
from pathlib import Path

from git import InvalidGitRepositoryError, Repo
from kedro.framework.hooks import hook_impl

from everycure.datasets.kedro.storage import GitStorageService

logger = logging.getLogger(__name__)


class GitStorageHook:
    """Kedro hook to clone or update a Git repository before running a pipeline."""

    def __init__(
        self,
        repo_url: str,
        target_dir: str = "data/external/data-catalog",
        branch: str = "main",
        force: bool = False,
        pull: bool = True,
    ):
        self.repo_url = repo_url
        self.target_dir = Path(target_dir)
        self.branch = branch
        self.force = force
        self.pull = pull

    @hook_impl
    def after_context_created(self, context):
        """Clone or update repo before the pipeline runs."""

        if self.force and self.target_dir.exists():
            shutil.rmtree(self.target_dir)

        if not self.target_dir.exists():
            repo = Repo.clone_from(self.repo_url, self.target_dir, branch=self.branch)

        else:
            try:
                repo = Repo(self.target_dir)
                logger.info(f"📁 Existing repo found: {repo.working_dir}")

                if self.pull:
                    logger.info(f"⬇️ Pulling latest changes from {self.branch}")
                    origin = repo.remotes.origin
                    origin.fetch()
                    origin.pull(self.branch)
                    logger.info("✅ Repository updated.")
                else:
                    logger.info("🔸 Skipping pull, using existing contents.")

                # Ensure branch consistency
                repo.git.checkout(self.branch)
            except InvalidGitRepositoryError:
                logger.info(
                    f"⚠️ {self.target_dir} exists but is not a Git repo. Re-cloning."
                )
                shutil.rmtree(self.target_dir)
                Repo.clone_from(self.repo_url, self.target_dir, branch=self.branch)

        self.git_service = GitStorageService(
            root_path=str(self.target_dir),
            user="Kedro",
            email="kedro@everycure.org",
        )

        logger.info(f"🔁 GitStorageService ready at {self.target_dir}")
