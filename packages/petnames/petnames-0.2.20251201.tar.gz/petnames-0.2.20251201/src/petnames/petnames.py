#!/usr/bin/env python3
# Copyright 2025-2025 Kevin Steen <code at kevinsteen.net>
# SPDX-License-Identifier: AGPL-3.0-or-later
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""PetName and Distributed Directory Name resolver

Resolves dns-like names using a local database of PetNames and by contacting
distributed directory servers. Returns properties stored under that name as
strings, or bytes if the property name begins with 'b_'

Key functions:

get_property()
    Resolves the name and property to a list of values
get_properties(name)
    Resolves the name and returns all properties stored under that name
get_properties_local()
    As for get_properties(), but only searches the local database
get_petname()
    Searches the local database for the name matching the supplied property

list_names()  NOT YET IMPLEMENTED
    List names matching the supplied prefix
get_display_properties()  NOT YET IMPLEMENTED
    Describes how to display a PetName
register_display_callback()  NOT YET IMPLEMENTED
    Called when display properties are changed

Known property names:

[Current list at https://codeberg.org/skyguy/petnames/known_props.txt]

Properties starting with 'b_' are treated as bytes, otherwise strings.
Case is irrelevant - comparisons are case-insensitive

suggested_name
    Suggested name to use when storing this PetName
ttl_secs
    Duration to regard PetName data as valid (time-to-live)
b_lxmf_dh0
    Reticulum LXMF destination address
b_nomadnet_dh0
     Reticulum Nomadnet destination
b_reti_rnsh_dh0
     Reticulum rnsh destination
b_reti_rnx_dh0
    Reticulum rnx destination
b_ygg_ip6
    Yggdrasil IPv6 address
b_ygg_id
    Yggdrasil node address
"""

import argparse
import logging
from pathlib import Path
from typing import Callable, Mapping, MutableMapping, Protocol, Any, Self

DEFAULT_TTL_SECS = 300
MAX_NAMEPARTS = 32
_db_path: Path = Path("~/.local/share/petnames/").expanduser()  # TODO: xdg path

#logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("petnames")


class PetName:
    """Object containing the properties of a PetName

    Special properties (always present):
        name: (str) Canonical name as recorded in the database
        ttl_secs: (int) Validity duration of the record (Time to Live)

    Note: properties may occur multiple times. PetName.property will return a
    list of strings (which will be empty if the property is not defined)
    Properties whose name begins with 'b_' return a list of bytes
    """

    @classmethod
    def from_text_record(cls, name: str, text_record: str, prop: str = 'all') \
            -> Self:
        """Create and return a PetName from a text record

        If prop is not 'all', limit record to property 'prop'
        """
        prop = prop.lower()
        petname = cls(name)
        for line in text_record.splitlines():
            log.debug("line:%s", line)
            line = line.strip()
            if line.startswith("#") or line == "":
                continue
            field, value = line.split('=', maxsplit=1)
            field = field.strip()
            if (
                    prop == 'all'
                    or field.lower() in ["base_url", "ttl_secs", "refer_dir"]
                    or field.lower() == prop
            ):
                value = value.strip()
                log.debug("Found property: %s, %s", field, value)
                if field.lower() == "ttl_secs":
                    petname.ttl_secs = int(value)
                elif field.lower() == "base_url":
                    petname.base_url = value
                elif field.lower() == "refer_dir":
                    petname.refer_dir = value
                else:
                    if field.startswith("b_"):
                        petname[field] = bytes.fromhex(value)
                    else:
                        petname[field] = value
        return petname

    def __init__(self, name: str) -> None:
        self._props: MutableMapping[str, list] = {}
        self.name: str = name
        self.ttl_secs: int = DEFAULT_TTL_SECS
        self.refer_dir: str = ""
        self.base_url: str = "ddir:lo:/"

    def __format__(self, format_spec):
        return self.__str__().__format__(format_spec)

    def __getattr__(self, name):
        name = name.lower()
        res = []
        for k, v in self._props.items():
            if k.lower() == name:
                res += v
        return res

    def __getitem__(self, name):
        name = name.lower()
        res = []
        for k, v in self._props.items():
            if k.lower() == name:
                res += v
        return res

    def __setitem__(self, key, value):
        if key.lower() in self._props:
            self._props[key.lower()].append(value)
        else:
            self._props[key.lower()] = [value]

    def __str__(self):
        return 'PetName<<"' + self.name + '">>'

    def as_records(self):
        res = ""
        for prop, value in self._props.items():
            for v in value:
                res += f"{self.name} {self.ttl_secs} {prop} {v} {self.base_url}\n"
        return res


def get_petname(prop: str, value: str, default: Any = None) -> PetName | Any:
    """Return the petname where property = value. WARNING: SLOW!!

    If not found, returns default
    """
    log.debug("get_petname for %s = %s", prop, value)
    namespath = _db_path / "local"
    for target in namespath.glob("*.txt"):
        petname = PetName.from_text_record(
            target.stem,
            target.read_text(encoding='utf8'),
            prop,
        )
        log.debug("Checking PetName: %s", petname.name)
        log.debug("_props = %s", petname._props)
        try:
            if value in petname._props[prop]:
                return petname
        except KeyError:
            pass
    return default  # Not found


def get_property(name: str, prop: str) -> list[str | bytes] | None:
    res = get_properties(name, prop)
    log.debug("get_property res:%s", res)
    if res:
        log.debug("get_property res[prop]:%s", res[prop])
        return res[prop]
    return None


def get_properties(name: str, prop: str = "all", start_url: str = "ddir:lo:/") \
        -> PetName | None:
    """Resolve name and return properties stored under that name

    prop: property to return or 'all'. Default: 'all'

    Returns: None or a PetName instance - A Mapping of properties to values including:
        name: Resolved name as stored in the database
        ttl_secs: Time to Live - number of seconds results are valid for
        Other properties return a list to allow for multiple values

    Exceptions:
        + ValueError if name has too many parts (see MAX_NAMEPARTS) or contains
          invalid characters
    """
    if not name:
        raise ValueError("Name cannot be empty")
    nameparts = _parse_name(name)
    if len(nameparts) > MAX_NAMEPARTS:
        raise ValueError("Too many name components. max:%s" % MAX_NAMEPARTS)
    ddirectory = _get_directory(start_url)
    for namepart in nameparts:
        log.debug("Search for %s", namepart)
        result = ddirectory.get_properties(namepart, prop)
        log.debug("result: %s", result)
        if result:
            if result.refer_dir:
                log.debug("Referral to %s", result.refer_dir)
                ddirectory = _get_directory(result.refer_dir)
                continue
            else:
                log.debug("returning result")
                return result
        else:
            log.debug("result False")
    return None


def get_properties_local(name: str, prop: str = "all") -> PetName | None:
    """As for get_properties() but only queries the local database"""
    if not name:
        raise ValueError("Name cannot be empty")
    nameparts = _parse_name(name)
    if len(nameparts) > MAX_NAMEPARTS:
        raise ValueError("Too many name components. max:%s" % MAX_NAMEPARTS)
    ddirectory = LocalDirectoryClient("ddir:lo:/")
    for namepart in nameparts:
        log.debug("Local search for %s", namepart)
        result = ddirectory.get_properties(namepart, prop)
        log.debug("result: %s", result)
        if result:
            if result.refer_dir:
                log.debug("Referral to %s", result.refer_dir)
                if not result.refer_dir.startswith("ddir:lo"):  # Not a local reference
                    return None
                ddirectory = _get_directory(result.refer_dir)
                continue
            else:
                log.debug("returning result")
                return result
        else:
            log.debug("result False")
    return None


class DirectoryClient(Protocol):
    """Implements the search functionality for a specific type of Distributed Directory

    baseurl is the starting point for queries. So get_properties(name) should
    query baseurl/name
    urls should be of the form 'ddir:NAME:/path' where NAME is a unique code
    identifying the type of directory. See 'directory_types_map'
    """

    def __init__(self, baseurl: str) -> None: ...

    def get_properties(self, name: str, prop: str = "all") -> PetName: ...


class LocalDirectoryClient(DirectoryClient):
    def __init__(self, baseurl: str) -> None:
        self.path = baseurl.split(":", maxsplit=2)[2]
        log.debug("Directory Client path=%s", self.path)

    def get_properties(self, name: str, prop: str = "all") -> PetName | None:
        log.debug("LocalDirectory get_prop for %s in %s", name, self.path)
        if not name:
            raise ValueError("Name cannot be empty")
        prop = prop.strip().lower()
        path = self.path
        while path.startswith("/"):
            path = path[1:]
        while path.endswith("/"):
            path = path[:-1]
        log.debug("Cleaned path: %s", path)
        namespath = _db_path / "local" / path

        # Look for Record (txt file)
        log.debug("Checking for file: %s", namespath / (name + ".txt"))
        target = list(namespath.glob(name + ".txt", case_sensitive=False))
        if target:
            target = target[0]
            log.debug("Found target: %s", target)
            result = PetName.from_text_record(
                target.stem,
                target.read_text(encoding='utf8'),
                prop,
            )
            return result

        # Look for collection (directory)
        target = list(namespath.glob(name, case_sensitive=False))
        log.debug("Checking for directory: %s", namespath / name)
        if target:
            log.debug("Found collection: %s", target[0])
            p = PetName("LocalDirectory")
            if path:
                path = "/" + path
            p.refer_dir = "ddir:lo:" + "/".join([path, name])
            log.debug("refer_dir=%s", p.refer_dir)
            return p

        log.debug("Not found: %s", namespath / name)
        return None


def get_dbpath() -> Path:
    return _db_path


def set_dbpath(path: str):
    global _db_path
    _db_path = Path(path)


def _parse_name(name: str) -> list[str]:
    """Parse a dns-like name into a list of strings"""
    log.debug("parse_name: %s", name)
    for char in ":/\r\n":
        if char in name:
            raise ValueError('Names may not contain "{char}"')
    res = []
    for n in name.split('.'):
        if n: res.append(n)
    log.debug("parse_name returning: %s", res)
    return res


directory_types_map: Mapping[str, Callable[[str], DirectoryClient]] = {
    'lo': LocalDirectoryClient,
    #'rn': ReticulumDirectoryClient,
}


def _get_directory(url: str) -> DirectoryClient:
    try:
        if url.startswith("ddir:"):
            return directory_types_map[url[5:7]](url)
    except Exception:
        raise ValueError("Unable to handle Directory type " + url)
    raise KeyError("Not a Distributed Directory URL")


#################################################################
# commandline functionality
#################################################################

def _get_args():
    parser = argparse.ArgumentParser(
        description=(
            "Petname and Distributed Directory name resolver. "
            "Looks up NAME and returns the specified PROPERTY."),
        #usage="ddig [-h] NAME [PROPERTY]",
    )
    # parser.add_argument("-s", "--service",
    #     help="directory service to send the query to")
    parser.add_argument("NAME", help="name to resolve")
    parser.add_argument(
        "PROPERTY", default="all", nargs="?",
        help="property to return (default:'all')(optional)",
    )
    return parser.parse_args()


def _main(args):
    result = get_properties(args.NAME, args.PROPERTY)
    if result is None:
        print("name not found")
        return 1
    print(result.as_records())
    return 0


def main():
    args = _get_args()
    return _main(args)


if __name__ == '__main__':
    import sys

    sys.exit(main())
