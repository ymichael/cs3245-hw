from postings_file import PostingsFile, PostingsFileEntry
from nose.tools import eq_ as assert_eq
import os


def test_postings_file_noop():
    filename = 'test'
    with PostingsFile(filename, 'w+') as pfile:
        pass
    os.remove(filename)


def test_postings_file_pointer():
    filename = 'test'
    with PostingsFile(filename, 'w+') as pfile:
        assert_eq(0, pfile.pointer)
    os.remove(filename)


def test_postings_file_seek():
    filename = 'test'
    with PostingsFile(filename, 'w+') as pfile:
        assert_eq(0, pfile.pointer)
        pfile.seek(10)
        assert_eq(10, pfile.pointer)
    os.remove(filename)


def test_postings_file_write_entry():
    filename = 'test'
    with PostingsFile(filename, 'w+') as pfile:
        assert_eq(0, pfile.pointer)
        pfile.write_entry(PostingsFileEntry(1))
        pfile.write_entry(PostingsFileEntry(2))
        pfile.write_entry(PostingsFileEntry(3))

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
    with PostingsFile(filename, 'w+') as pfile:
        assert_eq(0, pfile.pointer)
        write_location = 0

        entry = PostingsFileEntry(1)
        entry.own_pointer = write_location

        pfile.write_entry(entry)

        assert_eq(
            PostingsFileEntry(1).to_string(),
            pfile.read_entry(write_location))

        entry.next_pointer = 2
        pfile.write_entry(entry)

        assert_eq(
            PostingsFileEntry(1, 2).to_string(),
            pfile.read_entry(write_location))

        entry.skip_pointer = 3
        pfile.write_entry(entry)

        assert_eq(
            PostingsFileEntry(1, 2, 3).to_string(),
            pfile.read_entry(write_location))

    os.remove(filename)

def test_postings_file_write_entry_out_of_order():
    filename = 'test'
    with PostingsFile(filename, 'w+') as pfile:
        first_write_location = pfile.pointer
        first_entry = PostingsFileEntry(1)
        first_entry.own_pointer = first_write_location

        pfile.write_entry(first_entry)

        assert_eq(
            PostingsFileEntry(1).to_string(),
            pfile.read_entry(first_write_location))

        second_write_location = pfile.pointer
        second_entry = PostingsFileEntry(2)
        second_entry.own_pointer = second_write_location
        pfile.write_entry(second_entry)

        assert_eq(
            PostingsFileEntry(2).to_string(),
            pfile.read_entry(second_write_location))

        # Update first entry
        first_entry.doc_id = 4
        pfile.write_entry(first_entry)

        assert_eq(
            first_entry.to_string(),
            pfile.read_entry(first_write_location))

        # Add third entry
        third_entry = PostingsFileEntry(3)
        pfile.write_entry(third_entry)

        # Check that second write location was not overwritten.
        assert_eq(
            PostingsFileEntry(2).to_string(),
            pfile.read_entry(second_write_location))

    os.remove(filename)


def test_postings_file_get_entry():
    filename = 'test'
    with PostingsFile(filename, 'w+') as pfile:
        head = pfile.pointer
        pfile.write_entry(PostingsFileEntry(1))

        # Test that we set the entries own pointer.
        assert_eq(head, pfile.get_entry(head).own_pointer)

        ptr = pfile.pointer
        pfile.write_entry(PostingsFileEntry(2))
        assert_eq(ptr, pfile.get_entry(ptr).own_pointer)

    os.remove(filename)


def test_postings_file_get_entry_from_pointer():
    filename = 'test'
    with PostingsFile(filename, 'w+') as pfile:
        head = pfile.pointer
        prev_ptr = head

        last = 12
        for i in xrange(1, last):
            current_entry = PostingsFileEntry(i)
            current_entry.own_pointer = pfile.pointer
            pfile.write_entry(current_entry)

            if i != last - 1:
                current_entry.next_pointer = pfile.pointer
                pfile.write_entry(current_entry)

        entries = pfile.get_entry_list_from_pointer(head)
        entries = [entry.doc_id for entry in entries]
        assert_eq([1,2,3,4,5,6,7,8,9,10,11], entries)

    os.remove(filename)


def test_postings_file_get_entry_reset_false():
    filename = 'test'
    with PostingsFile(filename, 'w+') as pfile:
        head = pfile.pointer
        prev_ptr = head

        last = 12
        for i in xrange(1, last):
            current_entry = PostingsFileEntry(i)
            current_entry.own_pointer = pfile.pointer
            pfile.write_entry(current_entry)

            if i != last - 1:
                current_entry.next_pointer = pfile.pointer
                pfile.write_entry(current_entry)

        entries = []
        entry = pfile.get_entry(head, reset=False)
        while entry:
            entries.append(entry)
            entry = entry.next()
        entries = [entry.doc_id for entry in entries]
        assert_eq([1,2,3,4,5,6,7,8,9,10,11], entries)

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
