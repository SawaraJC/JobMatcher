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
    

def parse_oracle_url(url: str):
    """
    Extract tenant + site from Oracle URLs reliably
    """

    try:
        # tenant = jpmc
        tenant = url.split("//")[1].split(".")[0]

        # find /sites/<site>/
        match = re.search(r"/sites/([^/]+)/", url)

        if not match:
            return None

        site = match.group(1)

        return {
            "tenant": tenant,
            "site": site,
            "base_url": f"https://{tenant}.fa.oraclecloud.com"
        }

    except Exception:
        return None