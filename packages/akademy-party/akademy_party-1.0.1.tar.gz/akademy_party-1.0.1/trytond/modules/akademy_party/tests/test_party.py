import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase

class PartyTestCase(ModuleTestCase):
    'Test party module'
    module = 'akademy_party'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        PartyTestCase))
    return suite
