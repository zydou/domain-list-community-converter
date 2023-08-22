#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert domain-list-community to clash and surge rules."""

from collections import defaultdict
from pathlib import Path


def parse_category(category: Path, rules: list, attrs: dict) -> tuple[list, dict]:
    """Parse category and return clash rules.

    Args:
        category (Path): path of the category
        rules (list): rules of default
        attrs (dict): rules of attrs

    Returns:
        tuple[list, dict]: parsed rules for default and attrs
    """
    with category.open() as f:
        for line in f.readlines():
            if line.startswith("#"):  # skip comments
                continue
            if line.startswith("regexp:"):  # skip regexp rules
                continue
            line = line.split("#")[0].strip()  # strip inline comments
            if "@" in line:
                rule = line.split("@")[0].strip()
                for attr in line.split("@")[1:]:  # parse attrs
                    attrs[attr].append(rule)
                line = rule
            if not line:  # skip empty line
                continue

            if line.startswith("include:"):
                sub_category = line.removeprefix("include:").strip()
                rules, attrs = parse_category(category.with_name(sub_category), rules, attrs)
            else:
                rules.append(line)
    return rules, attrs


def write_clash(category: str, rules: list, attrs: dict) -> None:
    """Write clash rules to file.

    Args:
        category (str): category name
        rules (list): rules of default
        attrs (dict): rules of attrs
    """

    def save_to_disk(outpath: Path, rule_lst: list) -> None:
        with outpath.open("w") as f:
            f.write("---\n")
            f.write("payload:\n")
            for rule in rule_lst:
                if rule.startswith("full:"):
                    f.write(f"  - {rule.removeprefix('full:')}\n")
                else:
                    # According to the documentation, the DOMAIN-SUFFIX rules should be wrapped in single quotes.
                    # source: https://lancellc.gitbook.io/clash/clash-config-file/syntax
                    f.write(f"  - '+.{rule}'\n")

    outroot = Path("clash")
    outroot.mkdir(parents=True, exist_ok=True)
    outpath = outroot / f"{category}.yml"
    save_to_disk(outpath, rules)
    for attr, rule_list in attrs.items():
        outpath = outroot / f"{category}@{attr}.yml"
        save_to_disk(outpath, rule_list)

def write_surge_domain_set(category: str, rules: list, attrs: dict) -> None:
    """Write surge domain-set rules to file.

    Args:
        category (str): category name
        rules (list): rules of default
        attrs (dict): rules of attrs
    """

    def save_to_disk(outpath: Path, rule_lst: list) -> None:
        with outpath.open("w") as f:
            for rule in rule_lst:
                if rule.startswith("full:"):
                    f.write(f"{rule.removeprefix('full:')}\n")
                else:
                    f.write(f".{rule}\n")

    outroot = Path("surge-domain-set")
    outroot.mkdir(parents=True, exist_ok=True)
    outpath = outroot / f"{category}.txt"
    save_to_disk(outpath, rules)
    for attr, rule_list in attrs.items():
        outpath = outroot / f"{category}@{attr}.txt"
        save_to_disk(outpath, rule_list)

def write_surge_rule_set(category: str, rules: list, attrs: dict) -> None:
    """Write surge rule-set rules to file.

    Args:
        category (str): category name
        rules (list): rules of default
        attrs (dict): rules of attrs
    """

    def save_to_disk(outpath: Path, rule_lst: list) -> None:
        with outpath.open("w") as f:
            for rule in rule_lst:
                if rule.startswith("full:"):
                    f.write(f"{rule.replace('full:', 'DOMAIN,')}\n")
                else:
                    f.write(f"DOMAIN-SUFFIX,{rule}\n")

    outroot = Path("surge-rule-set")
    outroot.mkdir(parents=True, exist_ok=True)
    outpath = outroot / f"{category}.txt"
    save_to_disk(outpath, rules)
    for attr, rule_list in attrs.items():
        outpath = outroot / f"{category}@{attr}.txt"
        save_to_disk(outpath, rule_list)


def main() -> None:
    """Entry point."""
    root = Path("domain-list-community/data")
    for category in root.iterdir():
        print(category)
        rules = []
        attrs = defaultdict(list)
        rules, attrs = parse_category(category, rules, attrs)
        write_clash(category.name, rules, attrs)
        write_surge_domain_set(category.name, rules, attrs)
        write_surge_rule_set(category.name, rules, attrs)


if __name__ == "__main__":
    main()
