import re

def parse_workday_url(url: str):
    pattern = r"https://([^.]+)\.wd\d+\.myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([^/]+)"
    match = re.match(pattern, url)

    if not match:
        return None

    return {
        "tenant": match.group(1),
        "site": match.group(2)
    }


def extract_wd_part(url: str):
    try:
        return url.split(".")[1]
    except:
        return None


def parse_oracle_url(url: str):
    """
    Works for ALL Oracle domains:
    - jpmc.fa.oraclecloud.com
    - eofe.fa.us2.oraclecloud.com
    - etc.
    """

    try:
        domain = url.split("//")[1].split("/")[0]
        tenant = domain.split(".")[0]

        match = re.search(r"/sites/([^/]+)/", url)
        if not match:
            return None

        site = match.group(1)

        return {
            "tenant": tenant,
            "site": site,
            "base_url": f"https://{domain}"
        }

    except Exception:
        return None