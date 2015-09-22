from unittest2 import TestCase
from pillowtop import get_all_pillows
from pillowtop.listener import BasicPillow
from inspect import isclass


def import_settings():
    class MockSettings(object):
        PILLOWTOPS = {'test': ['pillowtop.tests.FakePillow']}

    return MockSettings()


class PillowTopTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        import pillowtop.run_pillowtop
        pillowtop.utils.import_settings = import_settings

    def test_import_pillows_class_only(self):
        pillows = get_all_pillows(instantiate=False)
        self.assertEquals(len(pillows), 1)
        self.assertTrue(isclass(pillows[0]))

    def test_import_pillows(self):
        pillows = get_all_pillows(instantiate=True)
        self.assertEquals(len(pillows), 1)
        self.assertFalse(isclass(pillows[0]))


class FakePillow(BasicPillow):
    pass
