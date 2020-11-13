import unittest

from contacts_searcher.domain import inn


class InnTest(unittest.TestCase):
    def test_control_number_validation(self):
        assert inn.validate('1234567890') is False, '10 digits fake inn'
        assert inn.validate('3664069397') is True, '10 digits real inn'
        assert inn.validate('000000000123') is False, '12 digits fake inn'
        assert inn.validate('500100732259') is True, '12 digits real inn'

    def test_length_validation(self):
        assert inn.validate('366406939') is False, '9 digits fake inn'
        assert inn.validate('50010073225') is False, '11 digits fake inn'

    def test_wrong_format_validation(self):
        assert inn.validate('') is False, 'empty string'
        assert inn.validate('DA654315') is False, 'real inn in hex'
