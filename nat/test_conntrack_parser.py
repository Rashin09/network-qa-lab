from pathlib import Path
from conntrack_parser import parse_conntrack, is_natted
import pytest

SAMPLE_FILE = Path(__file__).resolve().parent / "contrack.txt"


def test_file_parse():
     conntrack_content = SAMPLE_FILE.read_text()
     entries = parse_conntrack(conntrack_content)
     assert len(entries) == 3


def test_content_check():
    conntrack_content = SAMPLE_FILE.read_text()
    entries = parse_conntrack(conntrack_content)
    assert entries[0]["orig_src"] == "192.18.1.4"
    assert entries[0]["reply_dst"] == "172.16.13.2"

def test_nat_check():
    conntrack_content = SAMPLE_FILE.read_text()
    entry = parse_conntrack(conntrack_content)
    assert is_natted(entry[0])
    assert is_natted(entry[1])
    assert not is_natted(entry[2])

def test_empty_check():
    entries = parse_conntrack("")
    assert entries == []
