
from urllib.parse import urlparse, urlunparse


def noslash(txt: str) -> str:
    """Remove leading and trailing slashes from the given text.

    Args:
        txt (str): The text.

    Returns:
        str: The text without leading and trailing slashes.
    """    
    return txt.removeprefix("/").removesuffix("/")


def endslash(txt: str) -> str:
    """Add a trailing slash to the given text if not present.

    Args:
        txt (str): The text.

    Returns:
        str: The text with a trailing slash.
    """    
    return txt.removesuffix("/") + "/"


def http_href_to_s3(href: str) -> str:
    """Generate an S3 href from an HTTP href

    Args:
        href (str): The HTTP href.

    Returns:
        str: The S3 href.
    """ 
    url = urlparse(href)
    components = list(url[:])
    if len(components) == 5:
        components.append('')
    components[0] = "s3"
    components[1] = ""
    components[2] = components[2].removeprefix("/")
    s3url = urlunparse(tuple(components))
    return s3url


def join_pathes(*ps: str) -> str:
    """Join multiple pathes ensuring there is exactly one '/' between them.

    Returns:
        str: The joined path.
    """    
    pathes: list[str] = list(filter(lambda p: p != "", ps))
    if len(pathes) == 1:
        return pathes[0]
    if len(pathes) > 1:
        pathes[0] = pathes[0].removesuffix("/")
        pathes[-1] = pathes[-1].removeprefix("/")
        for i in range(1, len(pathes) - 1):
            pathes[i] = pathes[i].removeprefix("/").removesuffix("/")
    return "/".join(pathes)
