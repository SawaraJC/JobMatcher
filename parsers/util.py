import re

def parse_workday_url(url: str):
    """
    Extract tenant and site from Workday URL
    Example:
    https://transunion.wd5.myworkdayjobs.com/en-GB/TransUnion
    """

    pattern = r"https://([^.]+)\.wd\d+\.myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([^/]+)"
    match = re.match(pattern, url)

    if not match:
        return None

    return {
        "tenant": match.group(1),
        "site": match.group(2)
    }


def extract_wd_part(url: str):
    """
    Extract wdX (wd1, wd5, wd10 etc.)
    """
    try:
        return url.split(".")[1]
    except:
        return None