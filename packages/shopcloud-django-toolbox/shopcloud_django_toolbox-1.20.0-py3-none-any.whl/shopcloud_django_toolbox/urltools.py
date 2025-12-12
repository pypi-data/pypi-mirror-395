import os
from typing import Dict, List, Optional, Union
from urllib.parse import quote_plus, urlencode


def remove_slashes(part: str):
    part = part.strip()
    if part.startswith("/"):
        part = part[1:]
    if part.endswith("/"):
        part = part[:-1]
    return part


def url_combine(
        parts: List[str],
        credentials: Union[Optional[str], Optional[str]] = [None, None],
        params: Optional[Dict]= None,
        fragments=Union[str, dict],
        force_https: bool = os.environ.get("ENV", "develop") == "production",
        force_end_slash=True
) -> str:

    if len(parts) <= 0:
        return ""

    params = params if params is not None else {}

    protocol = ""
    part_1 = parts[0]
    if not part_1.startswith("http://") and not part_1.startswith("https://"):
        protocol = f"{'https://' if force_https else 'https://'}"
    else:
        if part_1.startswith("http://"):
            protocol = "http://"
            part_1 = part_1[7:]
        if part_1.startswith("https://"):
            protocol = "https://"
            part_1 = part_1[8:]
        protocol = "https://" if force_https else protocol

    cred_str = ""
    if not (credentials[0] is None and credentials[1] is None):
        cred_str = f"{credentials[0]}:{credentials[1]}@"

    fragment_str = ""
    if isinstance(fragments, str):
        fragment_str = f"#{fragments}"
    if isinstance(fragments, dict):
        fragment_str = "#{}".format("&".join([f"{k}={v}" for k, v in fragments.items()]))

    parts[0] = part_1
    parts = [remove_slashes(x) for x in parts]
    if "?" in parts[-1]:
        params_parts = parts[-1].split("?")[1].split("&")
        extr_params = {x.split("=")[0]: x.split("=")[1] for x in params_parts}
        params.update(extr_params)
        parts[-1] = parts[-1].split("?")[0]
    res = f"{protocol}{cred_str}{'/'.join(parts)}{'/' if force_end_slash else ''}"
    if len(params) > 0:
        res = f"{res}?{urlencode(params, quote_via=quote_plus)}"
    res = f"{res}{fragment_str}"
    return res
