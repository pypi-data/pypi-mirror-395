import logging

import packaging.version
import requests

logger = logging.getLogger("bluequbit-python-sdk")


def equal_other_than_post_version(pip_version, local_version):
    """Check if the versions are equal except for the post version."""
    return (
        pip_version.major == local_version.major
        and pip_version.minor == local_version.minor
        and pip_version.micro == local_version.micro
        and pip_version.pre == local_version.pre
    )


MESSAGE_TEMPLATE = (
    "There is a {} of BlueQubit Python SDK available on PyPI. We"
    " recommend upgrading. Run 'pip install --upgrade bluequbit' to upgrade"
    " from your version {} to {}."
)


def check_version(version):
    local_version = packaging.version.parse(version)
    if local_version.is_prerelease:
        logger.warning(
            "Beta version %s of BlueQubit Python SDK is being used.", version
        )
    req = requests.get("https://pypi.python.org/pypi/bluequbit/json", timeout=2.0)
    if not req.ok:
        message = "PyPI version check unsuccessful."
        logger.debug(message)
        return message

    # find max version on PyPI
    releases = req.json().get("releases", [])
    pip_version = packaging.version.parse("0")
    for release in releases:
        ver = packaging.version.parse(release)
        if not ver.is_prerelease or local_version.is_prerelease:
            pip_version = max(pip_version, ver)

    if pip_version.major > local_version.major:
        message = MESSAGE_TEMPLATE.format("major upgrade", local_version, pip_version)
        logger.warning(message)
    elif pip_version > local_version and not equal_other_than_post_version(
        pip_version, local_version
    ):
        message = MESSAGE_TEMPLATE.format("newer version", local_version, pip_version)
        logger.info(message)
    else:
        message = ""
    return message
