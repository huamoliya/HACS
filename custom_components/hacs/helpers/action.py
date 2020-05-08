"""Checks to run as an action."""
from custom_components.hacs.hacsbase.exceptions import HacsException
from custom_components.hacs.helpers.information import get_tree

BRANDS_REPO = "https://github.com/home-assistant/brands"
WHEEL_REPO = "https://github.com/home-assistant/wheels-custom-integrations"


async def run_action_checks(repository):
    """Checks to run as an action."""
    brands = await repository.hacs.github.get_repo("home-assistant/brands")
    brandstree = await get_tree(brands, "master")
    repository.logger.info(repository.integration_manifest.get("requirements"))
    if repository.integration_manifest["domain"] not in [
        x.filename for x in brandstree
    ]:
        raise HacsException(f"Integration not added to {BRANDS_REPO}")
    repository.logger.info(f"Integration is added to {BRANDS_REPO}, nice!")

    if (
        repository.integration_manifest.get("requirements") is not None
        and len(repository.integration_manifest.get("requirements")) != 0
    ):
        wheels = await repository.hacs.github.get_repo(
            "home-assistant/wheels-custom-integrations"
        )
        wheeltree = await get_tree(wheels, "master")
        repository.logger.info([x.filename for x in brandstree])
        if f"{repository.integration_manifest['domain']}.jsons" not in [
            x.filename for x in wheeltree
        ]:
            raise HacsException(f"Integration not added to {WHEEL_REPO}")
        repository.logger.info(f"Integration is added to {WHEEL_REPO}, nice!")