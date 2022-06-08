#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path as osp
from typing import List


def parse_category(category: str) -> List[str]:
    """Parse category and return clash rules.

    Args:
        category (str): category name

    Returns:
        List[str]: clash rules
    """

    rules = []
    with open(osp.join(ROOT, category)) as f:
        for line in f.readlines():
            if line.startswith("#"):  # skip comments
                continue
            if line.startswith("regexp:"):  # skip regexp rules
                continue
            line = line.split("@")[0].strip()  # strip attrs
            line = line.split("#")[0].strip()  # strip inline comments
            if len(line) == 0:  # skip empty line
                continue

            if line.startswith("include:"):
                sub_category = line.split(":")[1]
                rules.extend(parse_category(sub_category))
            elif line.startswith("full:"):  # DOMAIN
                domain = line.split(":")[1]
                rules.append(domain)
            else:  # DOMAIN-SUFFIX
                rules.append(f".{line}")
    return rules


def main():
    categories = os.listdir(ROOT)
    for category in categories:
        print(category)
        rules = parse_category(category)
        with open(osp.join(OUT, category + ".txt"), "w") as f:
            f.writelines("\n".join(rules))


if __name__ == "__main__":
    ROOT = "domain-list-community/data"  # path to the root of the categories
    OUT = "surge-domain-set"  # path to the output directory
    os.makedirs(OUT, exist_ok=True)
    main()
