import unittest
from FinalAssignment.StudentResultDBMS import *

DBMS_test = DBMS_Connection()


class Test_class(unittest.TestCase):

    def test_username(self):
        result = DBMS_test.get_username("student1")
        self.assertTrue(result)

    def test_faculty(self):
        result = DBMS_test.get_faculty("student1")
        self.assertEqual(result, 'student')

    def test_password(self):
        result = DBMS_test.get_password("student1")
        self.assertEqual(result, 'student1')

    def test_name(self):
        result = DBMS_test.show_name("student1")
        self.assertEqual(result, 'Student User')

    def test_username_check(self):
        result = DBMS_test.get_username("student3")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
