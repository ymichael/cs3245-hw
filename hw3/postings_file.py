from skip_list_node import SkipListNode


class PostingsFileEntry(SkipListNode):
    """Generic Postings File Entry.

    Encodes doc_id, next_pointer, skip_pointer, skip_doc_id.
    """
    FORMAT = "%010d %010d %010d %010d\n"
    SIZE = (10 * 4) + 4

    def __init__(
            self,
            doc_id,
            next_pointer=0,
            skip_pointer=0,
            skip_doc_id=0):
        self.doc_id = doc_id
        self.skip_doc_id = skip_doc_id

        # NOTE(michael): next/skip pointers should never be 0.
        # (that'll link to another node # :x)
        self.next_pointer = next_pointer or None
        self.skip_pointer = skip_pointer or None
        self.own_pointer = None
        self._postings_file = None

    def set_postings_file(self, pfile):
        self._postings_file = pfile

    def val(self):
        return self.doc_id

    def skip_val(self):
        return self.skip_doc_id

    def next(self):
        if not self.next_pointer:
            return None
        if self._postings_file is None:
            raise Exception('Postings File is not set.')
        # NOTE(michael): Set reset to be false when using the list node
        # interface to avoid unnecessary seeks.
        return self._postings_file.get_entry(self.next_pointer, reset=False)

    def skip(self):
        if not self.skip_pointer:
            return None
        if self._postings_file is None:
            raise Exception('Postings File is not set.')
        # NOTE(michael): Set reset to be false when using the list node
        # interface to avoid unnecessary seeks.
        return self._postings_file.get_entry(self.skip_pointer, reset=False)

    def to_string(self):
        return self.FORMAT % (
            self.doc_id,
            self.next_pointer or 0,
            self.skip_pointer or 0,
            self.skip_doc_id)

    def __str__(self):
        return 'Entry(%d)' % self.doc_id

    def __eq__(self, other):
        if not isinstance(other, PostingsFileEntry):
            return False

        return self.doc_id == other.doc_id and \
            self.next_pointer == other.next_pointer and \
            self.skip_pointer == other.skip_pointer and \
            self.skip_doc_id == other.skip_doc_id

    def __lt__(self, other):
        if not isinstance(other, PostingsFileEntry):
            return False
        return self.doc_id < other.doc_id

    def __gt__(self, other):
        if not isinstance(other, PostingsFileEntry):
            return False
        return self.doc_id > other.doc_id

    @classmethod
    def from_string(cls, string):
        assert len(string) == cls.SIZE

        doc_id, next_pointer, skip_pointer, skip_doc_id = string[:-1].split(' ')

        doc_id = int(doc_id)
        next_pointer = int(next_pointer)
        skip_pointer = int(skip_pointer)
        skip_doc_id = int(skip_doc_id)

        return cls(doc_id, next_pointer, skip_pointer, skip_doc_id)


class PostingsFileEntryWithFrequencies(PostingsFileEntry):
    """Postings File Entry with additional Term Frequencies."""
    FORMAT = "%010d %010d %010d %010d %010d\n"
    SIZE = (10 * 5) + 5

    def __init__(
            self,
            doc_id,
            term_freq=0,
            next_pointer=0,
            skip_pointer=0,
            skip_doc_id=0):
        super(PostingsFileEntryWithFrequencies, self).__init__(
            doc_id,
            next_pointer=next_pointer,
            skip_pointer=skip_pointer,
            skip_doc_id=skip_doc_id)
        self.term_freq = term_freq

    def val(self):
        return (self.doc_id, self.term_freq)

    @classmethod
    def from_string(cls, string):
        assert len(string) == cls.SIZE

        doc_id, term_freq, next_pointer, skip_pointer, skip_doc_id = \
            string[:-1].split(' ')

        doc_id = int(doc_id)
        term_freq = int(term_freq)
        next_pointer = int(next_pointer)
        skip_pointer = int(skip_pointer)
        skip_doc_id = int(skip_doc_id)

        return cls(doc_id, term_freq, next_pointer, skip_pointer, skip_doc_id)

    def to_string(self):
        return self.FORMAT % (
            self.doc_id,
            self.term_freq,
            self.next_pointer or 0,
            self.skip_pointer or 0,
            self.skip_doc_id)

    def __str__(self):
        return 'Entry(%d, %d)' % (self.doc_id, self.term_freq)

    def __repr__(self):
        return 'Entry(%d, %d)' % (self.doc_id, self.term_freq)


class PostingsFile(object):
    def __init__(self, filename, mode, entry_cls=PostingsFileEntry):
        self.filename = filename
        self.mode = mode
        self.entry_cls = entry_cls

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def open(self):
        self.f = open(self.filename, self.mode)

    def close(self):
        self.f.close()

    @property
    def pointer(self):
        return self.f.tell()

    def seek(self, byte_no):
        if byte_no is None:
            return
        self.f.seek(byte_no)

    def read_entry(self, byte_no, reset=True):
        """Reads line at byte_no.

        Returns pointer to the old postion after seeking and reading the
        line at the specified byte_no.
        """
        if byte_no is None:
            return None

        if reset:
            # Keep old pointer.
            old_pointer = self.pointer

        self.seek(byte_no)
        retval = self.f.read(self.entry_cls.SIZE)

        if reset:
            # Reset pointer after reading entry.
            self.seek(old_pointer)

        return retval

    def get_entry(self, byte_no, reset=True):
        if byte_no is None:
            return None

        entry = self.entry_cls.from_string(
            self.read_entry(byte_no, reset))

        entry.own_pointer = byte_no
        entry.set_postings_file(self)
        return entry

    def get_entry_list_from_pointer(self, head):
        if head is None:
            return []

        current_node = self.get_entry(head, reset=False)
        entries = []
        while (current_node):
            entries.append(current_node)
            current_node = current_node.next()

        return entries

    def get_doc_ids_from_pointer(self, head):
        entries = self.get_entry_list_from_pointer(head)
        return [entry.doc_id for entry in entries]

    def write_entry(self, entry_obj):
        """Writes entry to file.

        Overrides entry at its own_pointer if set. Defaults to current
        location otherwise.

        Postings file pointer is reset/updated to either:
        - The new location (if entry is new)
        - The previous location at the end of the file (if entry is an update).

        This ensures that subsequent writes what are new (not yet written) will
        be appended to the end of the file and not override existing entries.
        """
        old_pointer = self.pointer

        if entry_obj.own_pointer is None:
            write_location = self.pointer
        else:
            write_location = entry_obj.own_pointer

        self.f.seek(write_location)
        self.f.write(entry_obj.to_string())

        if self.pointer < old_pointer:
            self.seek(old_pointer)
