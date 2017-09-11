# -*- coding: utf-8 -*-

from psycopg2 import IntegrityError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger

class GlobalTestOpenAcademyCourse(TransactionCase):
    """
        Global test for openacademy course model.
        Test:
            - Create course
            - Trigger constraints
    """

    # Seudo-constructor of test setUp
    def setUp(self):
        # Define global variables to test methods
        super(GlobalTestOpenAcademyCourse, self).setUp()
        self.course = self.env['openacademy.course']

    # Method of class that is not a test.
    def create_course(self, course_name, course_description,
                      course_responsible_id):
        # create a course with paramters received
        course_id = self.course.create({
            'name' : course_name,
            'description' : course_description,
            'responsible_id' : course_responsible_id,
        })

        return course_id

    # Test methods must start with 'def test_*(self):'

    # Mute the error odoo.sql_db to avoid it in log
    @mute_logger('odoo.sql_db')
    def test_10_same_name_description(self):
        """
            Create a course with same name and description
            to raise constraint "name different of description"
        """

        # Error raised expected with message expected
        with self.assertRaisesRegexp(
                 IntegrityError,
                 'new row for relation "openacademy_course" violates'
                 ' check constraint "openacademy_course_name_description_check"'):
            # create a course with same name and description to raise an error
            self.create_course('test','test',None)

    @mute_logger('odoo.sql_db')
    def test_20_two_courses_same_name(self):
        """
            Create two courses with the same name,
            to raise constraint of unique name
        """
        new_id = self.create_course('test1', 'test_description', None)
        print "new_id: ", new_id

        with self.assertRaisesRegexp(
                 IntegrityError,
                 'duplicate key value violates unique'
                 ' constraint "openacademy_course_name_unique"'
                ):
            new_id2 = self.create_course('test1', 'test_description', None)
            print "new_id2: ", new_id2

    def test_15_duplicate_course(self):
        """
            Duplicate a course and check that work fine!
        """

        course = self.env.ref('openacademy.course0')
        course_id = course.copy()

        print "copy_course_id: ", course_id
