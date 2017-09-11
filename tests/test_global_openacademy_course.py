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
    def test_01_same_name_description(self):
         """
                Create a course with same name and description
                to test constraint "name different of description"
         """
         # Error raised expected with message expected
         with self.assertRaisesRegexp(
                 IntegrityError,
                 'new row for relation "openacademy_course" violates'
                 ' check constraint "openacademy_course_name_description_check"'
                ):
             # create a course with same name and description to raise an error
             self.create_course('test','test',None)
