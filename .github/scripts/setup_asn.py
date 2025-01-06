import re

import httpx


http_client = httpx.Client()
pattern = re.compile(r"AS\d+")

r = http_client.get("https://bgp.he.net/country/CN")
as_numbers = re.findall(pattern, r.text)
as_numbers = sorted(map(lambda x: x.upper().strip("AS"), set(as_numbers)))

FILE_PREFIX = "ruleset-"
with open(f"{FILE_PREFIX}ans-cn.conf", "w", encoding="utf8") as wf:
    wf.write("\n".join([f"IP-ASN,{as_number}" for as_number in as_numbers]))
