import unittest
import os
import codecs

from tests.get_data import get_data_from_file, ARQS_DIRPATH
from pycnab240.file import File
from pycnab240.bancos import santander


class TestPyCnab240(unittest.TestCase):

    def setUp(self):
        self.data = get_data_from_file()
        self.file = File(santander)
        self.file.add_header(self.data['HeaderArquivo'])
        self.file.add_segment('HeaderLote', self.data['HeaderLote'])
        self.file.add_segment('SegmentoJ', self.data['SegmentoJ'])
        self.path_to_file = os.path.join(ARQS_DIRPATH, 'santander.rem')
        self.comparison_file = open(self.path_to_file, 'r').read().split('\n')

    def test_add_header(self):
        self.assertEqual(self.comparison_file[0], str(self.file.header))

    def test_add_segment(self):
        self.assertEqual(self.comparison_file[1],
                         str(self.file.get_active_lot().header))
        self.assertEqual(self.comparison_file[2],
                         str(self.file.get_active_lot().get_active_event().
                         segments[0]))

    def test_close_file(self):
        self.file.close_file()
        self.assertEqual(3, self.file.lots[0].trailer.quantidade_registros)
        self.assertEqual(3, self.file.trailer.totais_quantidade_lotes)
        self.assertEqual(7, self.file.trailer.totais_quantidade_registros)

    def test_str(self):
        self.file.close_file()
        self.assertEqual(str(self.file), '\r\n'.join(self.comparison_file))

    def test_load_return_file(self):
        file_ = codecs.open(self.path_to_file, encoding='ascii')
        loaded_cnab = File(santander)
        loaded_cnab.load_return_file(file_)
        file_.seek(0)
        self.assertEqual(file_.read().replace('\n', '\r\n'), str(loaded_cnab))
        file_.close()


if __name__ == '__main__':
    unittest.main()
