from unittest import TestCase
from molecupy.pdb.pdbfile import PdbRecord

class RecordCreationTests(TestCase):

    def test_can_create_record(self):
        record = PdbRecord("TEST   123  123.8    HYT", 23)
        self.assertEqual(record._number, 23)
        self.assertEqual(record._name, "TEST")
        self.assertTrue(record._text.startswith("TEST   123  123.8    HYT"))
        self.assertTrue(record._content.startswith(" 123  123.8    HYT"))
        self.assertEqual(len(record._text), 80)
        self.assertEqual(len(record._content), 74)


    def test_number_must_be_int(self):
        with self.assertRaises(TypeError):
            PdbRecord("TEST   123  123.8    HYT", "23")
        with self.assertRaises(TypeError):
            PdbRecord("TEST   123  123.8    HYT", 23.5)


    def test_text_must_be_string(self):
        with self.assertRaises(TypeError):
            PdbRecord(100, 23)


    def test_cannot_provide_empty_string(self):
        with self.assertRaises(ValueError):
            PdbRecord("", 23)


    def test_repr(self):
        record = PdbRecord("TEST   123  123.8    HYT", 23)
        self.assertEqual(str(record), "<PdbRecord 23 (TEST)>")



class RecordPropertyTests(TestCase):

    def test_record_properties(self):
        record = PdbRecord("TEST   123  123.8    HYT", 23)
        self.assertEqual(record._number, record.number())
        self.assertEqual(record._name, record.name())
        self.assertEqual(record._text, record.text())
        self.assertTrue(record._content, record.content())



class RecordAccessTests(TestCase):

    def setUp(self):
        self.line = "TEST   123  123.8    HYT"


    def test_can_get_individual_characters(self):
        record = PdbRecord(self.line, 23)
        self.assertEqual(record[0], "T")
        self.assertEqual(record[21], "H")


    def test_can_get_strings_from_record(self):
        record = PdbRecord(self.line, 23)
        self.assertEqual(record[1:4], "EST")
        self.assertEqual(record[21:24], "HYT")


    def test_record_indexes_will_strip_strings(self):
        record = PdbRecord(self.line, 23)
        self.assertEqual(record[0:7], "TEST")
        self.assertEqual(record[19:24], "HYT")
        self.assertEqual(record[19:34], "HYT")


    def test_records_can_covert_to_int(self):
        record = PdbRecord(self.line, 23)
        self.assertEqual(record[5:11], 123)


    def test_records_can_covert_to_float(self):
        record = PdbRecord(self.line, 23)
        self.assertEqual(record[10:19], 123.8)


    def test_can_force_record_to_return_string(self):
        record = PdbRecord(self.line, 23)
        self.assertEqual(record.get_as_string(5, 11), "123")
        self.assertEqual(record.get_as_string(10, 19), "123.8")


    def test_empty_sections_return_none(self):
        record = PdbRecord(self.line, 23)
        self.assertIs(record[17:21], None)
        self.assertIs(record.get_as_string(17, 21), None)