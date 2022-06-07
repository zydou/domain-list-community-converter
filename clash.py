#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path as osp
from typing import List

from ruamel.yaml import YAML


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
                rules.append(f"'+.{line}'")
    return rules


def transform(s: str) -> str:
    """Transform the final yaml string.

    By default, the generated yaml string adds a double quotes around the DOMAIN-SUFFIX rules.
    According to the official documentation, the DOMAIN-SUFFIX rules should be wrapped in single quotes.
    source: https://lancellc.gitbook.io/clash/clash-config-file/syntax

    Args:
        s (str): src string

    Returns:
        str: dst string
    """
    return s.replace('"', "")


def main():
    categories = os.listdir(ROOT)
    for category in categories:
        print(category)
        rules = parse_category(category)
        with open(osp.join(OUT, category + ".yml"), "w") as f:
            yaml.dump({"payload": sorted(rules)}, f, transform=transform)


if __name__ == "__main__":
    ROOT = "domain-list-community/data"  # path to the root of the categories
    OUT = "clash"  # path to the output directory
    os.makedirs(OUT, exist_ok=True)
    yaml = YAML(typ="rt")
    yaml.default_flow_style = False
    yaml.indent(offset=2)
    main()
