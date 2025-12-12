__version__: str = "0.5.4"


def get_version() -> str:
    """Returns the version of the package."""
    return __version__


from picteus_extension_sdk.picteus_extension import PicteusExtension
