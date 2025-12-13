"""
petnames - PetName and Distributed Directory Name resolver
SPDX-FileCopyrightText: Copyright 2025 Kevin Steen
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import pytest

import petnames
from pathlib import Path
from petnames.petnames import _parse_name
from petnames import (get_properties, get_properties_local, get_dbpath, set_dbpath,
    PetName, DEFAULT_TTL_SECS)


def test_solo_lookup(min_db):
    res = petnames.get_property("jen", "reti_dest")
    assert "jen_reti_dest" == res[0]


def test_solo_lookup_name_notfound(min_db):
    assert petnames.get_property("bob", "ip_host") is None


def test_solo_lookup_prop_notfound(min_db):
    res = petnames.get_property("jen", "ip_host")
    assert [] == res


def test_solo_lookup_bytes(min_db):
    res = petnames.get_property("jen", "b_reti_dst0")
    assert [b"\xaa\xbb\xcc"] == res


def test_single_lookup(min_db):
    res = get_properties("jen", "reti_dest")
    assert ["jen_reti_dest"] == res.reti_dest


def test_single_lookup_noprop(min_db):
    res = get_properties("jen", "batman")
    assert [] == res.reti_dest


def test_single_lookup_missing(min_db):
    assert get_properties("Robin", "reti_dest") is None


def test_default_lookup(min_db):
    """Default lookup should return all properties"""
    p = get_properties("jen")
    assert "Jen" == p.name
    assert ["jen_reti_dest"] == p.reti_dest
    assert ["jen_reti_id", "jen_reti_id2"] == p.reti_id
    assert ["555-1234"] == p.tel
    assert [b"\xaa\xbb\xcc"] == p.b_reti_dst0


def test_lookup_all_properties(min_db):
    p = get_properties_local("jen", "all")
    assert ["jen_reti_dest"] == p.reti_dest
    assert ["jen_reti_id", "jen_reti_id2"] == p.reti_id
    assert ["555-1234"] == p.tel
    assert ["Jennifer"] == p.suggested_name


def test_single_field_lookup(min_db):
    p = get_properties_local("Jen", "reti_dest")
    assert ["jen_reti_dest"] == p.reti_dest
    assert [] == p.reti_id


def test_local_collection(min_db):
    """Local collections are recognised, not searched on the network"""
    p = get_properties_local("servers.hilltop")
    assert ["servers_hilltop_reti_dest"] == p.reti_dest


def test_local_nested_collection(min_db):
    """Local collections can be nested"""
    p = get_properties_local("servers.nested.nestserv")
    assert ["servers_nested_reti_dest"] == p.reti_dest


def test_local_nested_collection_missing(min_db):
    """Missing local collection returns None"""
    assert get_properties_local("servers.nested.batman") is None


def test_nonexistent_property(min_db):
    assert get_properties_local("Mom", "reti_dest").reti_dest == []


def test_empty_nameparts():
    assert list(_parse_name("bob.")) == ["bob"]
    assert list(_parse_name(".bob")) == ["bob"]
    assert list(_parse_name(".bob.")) == ["bob"]
    assert list(_parse_name(".bob..mary")) == ["bob", "mary"]
    assert list(_parse_name("..bob..mary")) == ["bob", "mary"]
    assert list(_parse_name("1")) == ["1"]


@pytest.mark.parametrize(
    "badname", [
        "bob/mary", "bob:mary", "bob\n", "bob\r", ""
    ],
)
def test_invalid_chars(badname):
    with pytest.raises(ValueError):
        get_properties_local(badname)
        # assert resolve(badname) == badname
        # assert _parse_name(badname)


def test_set_dbpath():
    set_dbpath("some/random/path")
    assert Path("some/random/path") == get_dbpath()


def test_too_many_nameparts(min_db):
    saved = petnames.petnames.MAX_NAMEPARTS
    petnames.petnames.MAX_NAMEPARTS = 2
    try:
        with pytest.raises(ValueError):
            get_properties("servers.nested.nestserv")
    finally:
        petnames.petnames.MAX_NAMEPARTS = saved


def test_too_many_nameparts_local(min_db):
    saved = petnames.petnames.MAX_NAMEPARTS
    petnames.petnames.MAX_NAMEPARTS = 2
    try:
        with pytest.raises(ValueError):
            get_properties_local("servers.nested.nestserv")
    finally:
        petnames.petnames.MAX_NAMEPARTS = saved


def test_local_referral(min_db):
    """Returns a referral, but with no further names to query, that's a no-result"""
    assert get_properties("remy", "prop1") is None


def test_local_referral_with_name(min_db):
    p = get_properties("remy.jen", "tel")
    assert ["555-1234"] == p.tel


def test_petname_basic():
    a = PetName("Anon")
    assert a.name == "Anon"
    assert a.ttl_secs == DEFAULT_TTL_SECS
    assert a.bob == []
    a["Bob"] = "bobval1"
    assert a.bob == ["bobval1"]
    a["bob"] = "alice"
    assert a.bob == ["bobval1", "alice"]


def test_petname_formatted_str():
    a = PetName("FormatMe")
    assert f"{a:25}" == 'PetName<<"FormatMe">>    '


def test_petname_from_good_text():
    txt = """
        suggested_name = Mary
        # Comment line
        reti_dest = dest value
        reti_dest = value2
        reti_dest2 = =value2
        ttl_secs = 42
    """
    p = PetName.from_text_record("MBob", txt)
    assert ["Mary"] == p.suggested_name
    assert 42 == p.ttl_secs
    assert ["dest value", "value2"] == p.reti_dest
    assert ["=value2"] == p.reti_dest2


def test_petname_from_no_final_LF():
    txt = "suggested_name = Mary"
    p = PetName.from_text_record("MBob", txt)
    assert ["Mary"] == p.suggested_name


@pytest.mark.parametrize(
    "badline", [
        "suggested_name : Mary",
        "reti_dest  dest value",
        "ttl_secs = eighty",
])
def test_petname_from_bad_text(badline):
    with pytest.raises(ValueError):
        PetName.from_text_record("MBob", badline)


@pytest.fixture
def min_db(tmp_path):
    p = Path(tmp_path, "local")
    p.mkdir()
    q = p / "Jen.txt"
    q.write_text(
        "suggested_name=Jennifer\n"
        "reti_id=jen_reti_id\n"
        "reti_dest=jen_reti_dest\n"
        "tel=555-1234\n"
        " reti_id  =   jen_reti_id2\n"
        "b_reti_dst0 = aabbcc\n"
    )
    q = p / "MOM.txt"
    q.write_text(
        "lifetime=28\n"
        "url=MOM/url\n"
    )
    q = p / "servers"
    q.mkdir()
    r = q / "hilltop.txt"
    r.write_text("reti_dest=servers_hilltop_reti_dest")
    r = q / "nested"
    r.mkdir()
    (r / "nestserv.txt").write_text("reti_dest=servers_nested_reti_dest")

    q = p / "Remy.txt"
    q.write_text("refer_dir=ddir:lo:/")
    set_dbpath(tmp_path)
    return tmp_path


