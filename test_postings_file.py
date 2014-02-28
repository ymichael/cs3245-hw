from postings_file import PostingsFile, PostingsFileEntry
from nose.tools import eq_ as assert_eq
import os


def test_postings_file_noop():
    filename = 'test'
    with PostingsFile(filename) as pfile:
        pass
    os.remove(filename)


def test_postings_file_pointer():
    filename = 'test'
    with PostingsFile(filename) as pfile:
        assert_eq(0, pfile.pointer)
    os.remove(filename)


def test_postings_file_seek():
    filename = 'test'
    with PostingsFile(filename) as pfile:
        assert_eq(0, pfile.pointer)
        pfile.seek(10)
        assert_eq(10, pfile.pointer)
    os.remove(filename)


def test_postings_file_write_entry():
    filename = 'test'
    with PostingsFile(filename) as pfile:
        assert_eq(0, pfile.pointer)
        pfile.write_entry(1)
        pfile.write_entry(2)
        pfile.write_entry(3)

        assert_eq(
            PostingsFileEntry(1).to_string(),
            pfile.read_entry(0))

        assert_eq(
            PostingsFileEntry(2).to_string(),
            pfile.read_entry(0 + PostingsFileEntry.SIZE))

        assert_eq(
            PostingsFileEntry(3).to_string(),
            pfile.read_entry(0 + PostingsFileEntry.SIZE * 2))

    os.remove(filename)


def test_postings_file_write_entry_overwrite():
    filename = 'test'
    with PostingsFile(filename) as pfile:
        assert_eq(0, pfile.pointer)
        write_location = 0
        pfile.write_entry(1, write_location=write_location)

        assert_eq(
            PostingsFileEntry(1).to_string(),
            pfile.read_entry(write_location))

        pfile.write_entry(1, 2, write_location=write_location)

        assert_eq(
            PostingsFileEntry(1, 2).to_string(),
            pfile.read_entry(write_location))

        pfile.write_entry(1, 2, 3, write_location=write_location)

        assert_eq(
            PostingsFileEntry(1, 2, 3).to_string(),
            pfile.read_entry(write_location))

    os.remove(filename)


def test_postings_file_entry_to_string_only_doc_id():
    pfe = PostingsFileEntry(1)
    assert_eq(
        '0000000001 0000000000 0000000000 0000000000\n',
        pfe.to_string())


def test_postings_file_entry_to_string_wo_skip():
    pfe = PostingsFileEntry(11, 10)
    assert_eq(
        '0000000011 0000000010 0000000000 0000000000\n',
        pfe.to_string())


def test_postings_file_entry_to_string_with_skip():
    pfe = PostingsFileEntry(11, 10, 1000, 12)
    assert_eq(
        '0000000011 0000000010 0000001000 0000000012\n',
        pfe.to_string())


def test_postings_file_entry_eq():
    pfe1 = PostingsFileEntry(1)
    pfe2 = PostingsFileEntry(1, 10)
    pfe3 = PostingsFileEntry(1, 10, 100)
    pfe4 = PostingsFileEntry(1, 10, 100, 1000)

    assert_eq(pfe1, pfe1)
    assert_eq(pfe2, pfe2)
    assert_eq(pfe3, pfe3)
    assert_eq(pfe4, pfe4)

    assert not pfe1 == pfe2
    assert not pfe1 == pfe3
    assert not pfe1 == pfe4
    assert not pfe2 == pfe3
    assert not pfe2 == pfe4
    assert not pfe3 == pfe4


def test_postings_file_entry_from_string_only_doc_id():
    pfe = PostingsFileEntry(1)
    pfe_clone = PostingsFileEntry.from_string(pfe.to_string())
    assert_eq(pfe, pfe_clone)


def test_postings_file_entry_from_string_wo_skip():
    pfe = PostingsFileEntry(1, 10)
    pfe_clone = PostingsFileEntry.from_string(pfe.to_string())
    assert_eq(pfe, pfe_clone)


def test_postings_file_entry_from_string_with_skip():
    pfe = PostingsFileEntry(1, 10, 111, 123)
    pfe_clone = PostingsFileEntry.from_string(pfe.to_string())
    assert_eq(pfe, pfe_clone)
