class PostingsFile(object):
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

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

    def read_entry(self, byte_no):
        if byte_no is None:
            return None

        self.seek(byte_no)
        return self.f.read(PostingsFileEntry.SIZE)

    def get_entry(self, byte_no):
        if byte_no is None:
            return None

        entry = PostingsFileEntry.from_string(
            self.read_entry(byte_no))
        entry.own_pointer = byte_no
        entry.set_postings_file(self)
        return entry

    def get_entry_list_from_pointer(self, head):
        if head is None:
            return []

        current_node = self.get_entry(head)
        entries = []
        while (current_node):
            entries.append(current_node)
            current_node = current_node.next()

        return entries

    def get_doc_ids_from_pointer(self, head):
        entries = self.get_entry_list_from_pointer(head)
        return [entry.doc_id for entry in entries]

    def write_entry(
            self,
            doc_id,
            next_pointer=0,
            skip_pointer=0,
            skip_doc_id=0,
            write_location=None):
        """Writes entry to file.

        Overrides entry at write_location if specified. Defaults to current
        location otherwise.
        """
        if write_location is None:
            write_location = self.pointer
        postings_entry = PostingsFileEntry(
            doc_id, next_pointer, skip_pointer, skip_doc_id)

        self.f.seek(write_location)
        self.f.write(postings_entry.to_string())


class SkipListNode(object):
    def val(self):
        raise NotImplementedError()

    def skip_val(self):
        raise NotImplementedError()

    def next(self):
        raise NotImplementedError()

    def skip(self):
        raise NotImplementedError()


class PostingsFileEntry(SkipListNode):
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
        return self._postings_file.get_entry(self.next_pointer)

    def skip(self):
        if not self.skip_pointer:
            return None
        if self._postings_file is None:
            raise Exception('Postings File is not set.')
        return self._postings_file.get_entry(self.skip_pointer)

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

    @staticmethod
    def from_string(string):
        assert len(string) == PostingsFileEntry.SIZE

        doc_id, next_pointer, skip_pointer, skip_doc_id = string[:-1].split(' ')

        doc_id = int(doc_id)
        next_pointer = int(next_pointer)
        skip_pointer = int(skip_pointer)
        skip_doc_id = int(skip_doc_id)

        return PostingsFileEntry(
                doc_id,
                next_pointer,
                skip_pointer,
                skip_doc_id)

