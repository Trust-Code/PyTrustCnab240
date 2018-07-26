# -*- encoding: utf8 -*-

import codecs
from pycnab240 import errors
from io import IOBase


RECORD_NAMES = {
    '0': 'HeaderArquivo',
    '1': 'HeaderLote',
    '3': {
        'A': 'SegmentoA',
        'B': 'SegmentoB',
        'G': 'SegmentoG',
        'H': 'SegmentoH',
        'J-52': 'SegmentoJ52',
        'J': 'SegmentoJ',
        'N': 'SegmentoN',
        'O': 'SegmentoO',
        'W': 'SegmentoW',
        'Z': 'SegmentoZ',
    },
    '5': 'TrailerLote',
    '9': 'TrailerArquivo'
}


class Event(object):

    def __init__(self, bank):  # event_code):
        self._segments = []
        self.bank = bank
        self._lot_code = None
        self._is_open = True

    def add_segment(self, seg_name, segment):
        if type(segment) == dict:
            segment = self.bank.records[seg_name](**segment)
        self._segments.append(segment)

    @property
    def segments(self):
        return self._segments

    def __getattribute__(self, name):
        for segment in object.__getattribute__(self, '_segments'):
            if hasattr(segment, name):
                return getattr(segment, name)
        return object.__getattribute__(self, name)

    def __str__(self):
        return '\r\n'.join(str(seg) for seg in self._segments)

    def __len__(self):
        return len(self._segments)

    @property
    def lot_code(self):
        return self._lot_code

    @lot_code.setter
    def lot_code(self, value):
        self._lot_code = value
        for segment in self._segments:
            segment.controle_lote = value

    def update_record_code(self, last_id):
        current_id = last_id
        for segment in self._segments:
            current_id += 1
            segment.servico_numero_registro = current_id
        return current_id

    def close_event(self):
        self._is_open = False


class Lot(object):

    def __init__(self, bank):
        self.bank = bank
        self._code = None
        self.header, self.trailer = None, None
        self._events = []
        self._is_open = True

    @property
    def code(self):
        return self._code

    def add_header(self, header):
        if type(header) == dict:
            header = self.bank.records.HeaderLote(**header)
        self.header = header

    def add_trailer(self, trailer):
        if type(trailer) == dict:
            trailer = self.bank.records.TrailerLote(**trailer)
        self.trailer = trailer

    @code.setter
    def code(self, value):
        self._code = value
        if self.header is not None:
            self.header.controle_lote = value
        if self.trailer is not None:
            self.trailer.controle_lote = value
        self.upadte_event_code()

    def upadte_event_code(self):
        for event in self._events:
            event.lot_code = self._code

    def update_record_code(self):
        last_id = 0
        for event in self._events:
            last_id = event.update_record_code(last_id)

    @property
    def events(self):
        return self._events

    def add_event(self, event):
        if not isinstance(event, Event):
            raise TypeError('Object must be an instance of Event')
        self._events.append(event)

    def create_new_event(self):
        new_event = Event(self.bank)
        self._events.append(new_event)
        return new_event

    def get_active_event(self, create=False):
        for event in self._events:
            if event._is_open:
                return event
        if create:
            return self.create_new_event()

    def close_lot(self):
        if not self.trailer:
            self.trailer = self.bank.records.TrailerLote()
        if not self.trailer.quantidade_registros:
            self.trailer.quantidade_registros = self.get_records_lot()
        self._is_open = False
        for event in self._events:
            event.close_event()

    def get_records_lot(self):
        return sum(len(event) for event in self._events) + 2

    def __str__(self):
        if not self._events:
            raise errors.NoEventError()

        result = []
        if self.header is not None:
            result.append(str(self.header))
        result.extend(str(event) for event in self._events)
        if self.trailer is not None:
            result.append(str(self.trailer))
        return '\r\n'.join(result)

    def __len__(self):
        return len(self._events)


class File(object):

    def __init__(self, bank):
        """Cnab240 File"""

        self._lots = []
        self.bank = bank
        self.header, self.trailer = None, None

    @property
    def lots(self):
        return self._lots

    def add_header(self, header):
        self.header = self.bank.records.HeaderArquivo(**header)

    def add_trailer(self, trailer):
        self.trailer = self.bank.records.TrailerArquivo(**trailer)

    def add_lots(self, lot):
        if not isinstance(lot, Lot):
            raise TypeError('Object must be an instance of Lot')
        self._lots.append(lot)
        lot.code = len(self._lots)

    def create_new_lot(self):
        new_lot = Lot(self.bank)
        self.add_lots(new_lot)
        return new_lot

    def get_active_lot(self, create=False):
        for lot in self._lots:
            if lot._is_open:
                return lot
        if create:
            return self.create_new_lot()

    def add_segment(self, seg_name, vals):
        lot = self.get_active_lot(create=True)
        if seg_name == 'HeaderLote':
            lot.add_header(vals)
        elif seg_name == 'TrailerLote':
            lot.add_trailer(vals)
        else:
            event = lot.get_active_event(create=True)
            event.add_segment(seg_name, vals)

    def close_file(self):
        lot = self.get_active_lot()
        if lot:
            lot.close_lot()
        if not self.trailer:
            self.trailer = self.bank.records.TrailerArquivo()
        if not self.trailer.totais_quantidade_lotes:
            self.trailer.totais_quantidade_lotes = self.get_total_lots()
        if not self.trailer.totais_quantidade_registros:
            self.trailer.totais_quantidade_registros = self.get_total_records()

    def get_total_lots(self):
        return len(self._lots)

    def get_total_records(self):
        total = sum(lot.get_records_lot() for lot in self._lots) + 2
        return total

    def __str__(self):
        if not self._lots:
            raise errors.EmptyFileError()
        result = []
        result.append(str(self.header))
        result.extend(str(lot) for lot in self._lots)
        result.append(str(self.trailer))
        # Empty element so the file will end with \r\n
        result.append('')
        return '\r\n'.join(result)

    def write_to_file(self, file_):
        file_.write(str(self))

    def load_return_file(self, file_):
        if not isinstance(file_, (IOBase, codecs.StreamReaderWriter)):
            return TypeError("Wrong file type")
        for line in file_:
            record_name = self.get_record_name(line)
            segment = self.bank.records[record_name]()
            segment.load_line(string=line)
            if record_name == 'HeaderArquivo':
                self.header = segment
            elif record_name == 'TrailerArquivo':
                self.trailer = segment
            else:
                self.add_segment(record_name, segment)
            if record_name == 'TrailerLote':
                self.get_active_lot()._is_open = False

    def get_record_name(self, line):
        record_code = line[7]
        if record_code == '3':
            return RECORD_NAMES[record_code][line[13]]
        else:
            return RECORD_NAMES[record_code]
