from django.test import TestCase


class BasicTestingTest(TestCase):

    def test_addition(self):
        result = 10 + 20

        self.assertEqual(result, 30)
