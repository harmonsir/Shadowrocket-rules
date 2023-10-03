import re

import httpx


BLOCKING_FULL_SETS = set()
BLOCKING_RE_SETS = set()
BLOCKING_IPS_SETS = set()
DROP_SETS = set()

IP_RULE = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$")
REPLACE_RULE = re.compile(r"[\|\^]*")

GCDN_API = ""
FILE_PREFIX = "ruleset-"
# @formatter:off
DOWNLOADs = [
    (GCDN_API+"https://github.com/AdguardTeam/FiltersRegistry/raw/master/filters/filter_15_DnsFilter/filter.txt", "adguard-dns.conf"),
    (GCDN_API+"https://github.com/AdguardTeam/FiltersRegistry/raw/master/filters/filter_224_Chinese/filter.txt", "adguard-easylistCN.conf"),
    (GCDN_API+"https://github.com/AdguardTeam/AdguardFilters/raw/master/MobileFilter/sections/adservers.txt", "adguard-ads.conf"),
    (GCDN_API+"https://github.com/AdguardTeam/HostlistsRegistry/raw/main/assets/filter_29.txt", "adguard-adrules.conf"),
]

DROPs = [
    GCDN_API+"https://github.com/harmonsir/Shadowrocket-rules/raw/main/.github/assets/drop-domains.txt"
]
# @formatter:on


def load_drop_dataset():
    for uri in DROPs:
        dataset = httpx.get(uri, follow_redirects=True)
        DROP_SETS.update([u.strip() for u in dataset.text.split("\n")])


def update_dataset():
    skip_rules = []
    for uri, fn in DOWNLOADs:
        data = set()
        dataset = httpx.get(uri, follow_redirects=True)
        t = [u.strip() for u in dataset.text.split("\n")]

        for u in t:
            if u.startswith("/") and u.endswith("/"):
                u = u[1:-1]
                u = u.replace(r"\.", ".").replace(".", r"\.")
                BLOCKING_RE_SETS.add(f"URL-REGEX,{u}")
                continue

            if u.startswith("||") and u.endswith("^"):
                u = re.sub(REPLACE_RULE, "", u.strip())

                if re.search(IP_RULE, u):
                    BLOCKING_IPS_SETS.add(f"IP-CIDR,{u}/32")
                    continue
                if any(map(u.endswith, skip_rules)) or "*" in u:
                    u = u.replace(r"\.", ".").replace(".", r"\.")
                    BLOCKING_RE_SETS.add(f"URL-REGEX,{u}")
                    continue

                data.add(u)
                BLOCKING_FULL_SETS.add(u)

        with open(FILE_PREFIX + fn, "w", encoding="utf8") as wf:
            wf.write("\n".join(sorted(list(data))))

    for fn, data in (
        (f"{FILE_PREFIX}blacklist-ips.conf", BLOCKING_IPS_SETS),
        (f"{FILE_PREFIX}blacklist-regex.conf", BLOCKING_RE_SETS),
        (f"{FILE_PREFIX}blacklist-full.conf", BLOCKING_FULL_SETS),
        (f"{FILE_PREFIX}blacklist-slim.conf", BLOCKING_FULL_SETS - DROP_SETS),

    ):
        with open(fn, "w", encoding="utf8") as wf:
            wf.write("\n".join(sorted(list(data))))


if __name__ == '__main__':
    load_drop_dataset()
    update_dataset()
