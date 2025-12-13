#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
import dataclasses
import locale
import logging
import os
import re
from shlex import quote
from pathlib import Path
import tomllib

import psutil


__version__ = "0.1.0"

USER = os.getresuid()
XDG_CONFIG = os.environ.get("XDG_CONFIG_PATH", str(Path.home() / ".config"))
LOGGER = logging.getLogger("petique")


def from_ionice(obj):
    if obj[0] == psutil.IOPRIO_CLASS_BE:
        return f"b{obj[1]}"
    elif obj[0] == psutil.IOPRIO_CLASS_RT:
        return f"rt{obj[1]}"
    elif obj[0] == psutil.IOPRIO_CLASS_IDLE:
        return "idle"
    elif obj[0] == psutil.IOPRIO_CLASS_NONE:
        return "none"
    raise ValueError(f"{obj} is not recognized")


def to_ionice(s):
    if s == "idle":
        return (psutil.IOPRIO_CLASS_IDLE, None)

    m = re.fullmatch(r"b([0-7])", s)
    if m:
        return (psutil.IOPRIO_CLASS_BE, int(m[1]))

    m = re.fullmatch(r"rt([0-7])", s)
    if m:
        return (psutil.IOPRIO_CLASS_RT, int(m[1]))

    raise ValueError(f"{s!r} is not a valid ionice string")


@dataclasses.dataclass
class Rule:
    rule_name: str
    cmdline: str | None = None
    exe: str | None = None
    name: str | None = None
    oom_adj: int | None = None
    nice: int | None = None
    ionice: str | None = None
    all_users: bool = False
    dry_run: bool = False

    def __post_init__(self):
        if self.exe:
            self.exe = re.compile(self.exe)
        if self.cmdline:
            self.cmdline = re.compile(self.cmdline)
        if self.name:
            self.name = re.compile(self.name)

        if self.ionice is not None:
            self.ionice = to_ionice(self.ionice)

    def matches(self, proc):
        if not self.all_users:
            if proc.uids() != USER:
                return False

        try:
            proc.exe()
        except psutil.Error:
            return False

        if self.name:
            return self.name.fullmatch(proc.name())
        if self.exe:
            return self.exe.fullmatch(proc.exe())
        if self.cmdline:
            return self.cmdline.fullmatch(" ".join(map(quote, proc.cmdline())))

        return False

    def apply(self, proc, dry_run=True):
        dry_run = dry_run or self.dry_run

        LOGGER.info(f"matched {proc.pid} ({proc.exe()}) with rule {self.rule_name}")

        if self.nice is not None and proc.nice() != self.nice:
            LOGGER.info(f"  renicing {proc.pid} from {proc.nice()} to {self.nice}")
            if not dry_run:
                try:
                    proc.nice(self.nice)
                except psutil.AccessDenied:
                    LOGGER.warn(f"  cannot renice {proc.pid} from {proc.nice()} to {self.nice}")

        if self.oom_adj is not None:
            adj_file = Path(f"/proc/{proc.pid}/oom_score_adj")
            current_adj = adj_file.read_text().strip()
            if current_adj:
                current_adj = int(current_adj)

            if current_adj != self.oom_adj:
                LOGGER.info(f"  chooming {proc.pid} from {current_adj} to {self.oom_adj}")
                if not dry_run:
                    adj_file.write_text(str(self.oom_adj))

        if self.ionice is not None:
            if proc.ionice() != self.ionice:
                LOGGER.info(f"  ionicing {proc.pid} from {from_ionice(proc.ionice())} to {from_ionice(self.ionice)}")
            if not dry_run:
                proc.ionice(*self.ionice)


def _first_not_none(values):
    for value in values:
        if value is not None:
            return value
    return None


def apply_rules(proc, rules, dry_run=False):
    if not rules:
        return

    rules = reversed(rules)
    nice = ionice = oom_adj = None
    for rule in rules:
        if nice is None and rule.nice is not None:
            nice = rule.nice
        if ionice is None and rule.ionice is not None:
            ionice = rule.ionice
        if oom_adj is None and rule.oom_adj is not None:
            oom_adj = rule.oom_adj

    if nice is not None and proc.nice() != nice:
        LOGGER.info(f"  renicing {proc.pid} from {proc.nice()} to {nice}")
        if not dry_run:
            try:
                proc.nice(nice)
            except psutil.AccessDenied:
                LOGGER.warn(f"  cannot renice {proc.pid} from {proc.nice()} to {nice}")

    if oom_adj is not None:
        adj_file = Path(f"/proc/{proc.pid}/oom_score_adj")
        current_adj = adj_file.read_text().strip()
        if current_adj:
            current_adj = int(current_adj)

        if current_adj != oom_adj:
            LOGGER.info(f"  chooming {proc.pid} from {current_adj} to {oom_adj}")
            if not dry_run:
                adj_file.write_text(str(oom_adj))

    if ionice is not None:
        if proc.ionice() != ionice:
            LOGGER.info(f"  ionicing {proc.pid} from {from_ionice(proc.ionice())} to {from_ionice(ionice)}")
        if not dry_run:
            proc.ionice(*ionice)


def print_list():
    for proc in psutil.process_iter():
        LOGGER.info(f"process {proc.pid}")
        try:
            LOGGER.info(f"  name: {proc.name()!r}")
            LOGGER.info(f"  exe: {proc.exe()!r}")
            LOGGER.info(f"  cmdline: {' '.join(map(quote, proc.cmdline()))!r}")
        except psutil.AccessDenied:
            LOGGER.warning("  permission denied")


def main():
    locale.setlocale(locale.LC_ALL, "")

    default_config = XDG_CONFIG + "/petique.toml"
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--rule", action="append", dest="rules",
        help="Only use RULE in config instead of all (can be passed multiple times)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
    )
    parser.add_argument(
        "--list", action="store_true",
    )
    parser.add_argument(
        "--config", dest="file", default=default_config,
        help=f"config file (default: {default_config})",
    )
    args = parser.parse_args()

    if args.dry_run or args.list:
        args.verbose = True

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARN)

    if args.list:
        print_list()
        return

    with open(args.file, "rb") as fp:
        conf = tomllib.load(fp)

    for rule in conf:
        conf[rule] = Rule(**conf[rule], rule_name=rule)

    for proc in psutil.process_iter():
        rules_to_apply = []
        for rule in conf.values():
            if args.rules and rule.rule_name not in args.rules:
                continue

            if rule.matches(proc):
                LOGGER.info(f"matched {proc.pid} ({proc.exe()}) with rule {rule.rule_name}")
                rules_to_apply.append(rule)
                # rule.apply(proc, dry_run=bool(args.dry_run))

        apply_rules(proc, rules_to_apply, dry_run=bool(args.dry_run))


if __name__ == "__main__":
    main()
