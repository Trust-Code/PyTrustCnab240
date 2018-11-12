import re
import unittest
from datetime import date
from decimal import Decimal

from pycnab240.utils import decode_digitable_line


class TestUtils(unittest.TestCase):

    def test_decode_47_barcode(self):
        # Vencimento 11/11/2018
        # Valor 352,80
        # Banco Sicoob 756
        dig_line = '75691.30698 01245.640006 00371.460015 1 77050000035280'
        vals = decode_digitable_line(re.sub('[^0-9]', '', dig_line))
        self.assertEqual(len(vals['barcode']), 44)
        self.assertEqual(
            vals['barcode'], '75691770500000352801306901245640000037146001')
        self.assertEqual(vals['vencimento'], date(2018, 11, 11))
        self.assertEqual(vals['valor'], Decimal('352.80'))

    def test_decode_48_barcode(self):
        dig_line = '858700000049 800001791819 107622050820 415823300017'
        vals = decode_digitable_line(re.sub('[^0-9]', '', dig_line))
        self.assertEqual(len(vals['barcode']), 44)
        self.assertEqual(
            vals['barcode'], '85870000004800001791811076220508241582330001')
        self.assertEqual(vals['valor'], Decimal('480.00'))
