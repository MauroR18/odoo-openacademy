# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase

from odoo.exceptions import ValidationError

class GlobalTestOpenAcademySession(TransactionCase):
    """
        Global test for session model.
        Test:
            - Create a session with the same instructor and attendee
    """

    # Seudo-constructor method
    def setUp(self):
        super(GlobalTestOpenAcademySession, self).setUp()
        self.session = self.env['openacademy.session']
        self.partner = self.env.ref('base.res_partner_address_31')
        self.course = self.env.ref('openacademy.course1')

    # Generic methods

    # Test methods
    def test_10_instructor_not_in_attendees(self):
        """
            Check constraint:
                "A session's instructor can't be an attendee"
        """

        with self.assertRaisesRegexp(
                ValidationError,
                "A session's instructor can't be an attendee"
            ):
            self.session.create({
                'name' : 'Session test 1',
                'seats' : 1,
                'instructor_id' : self.partner.id,
                'attendee_ids' : [(6, 0, [self.partner.id])],
                'course_id' : self.course.id
            })
