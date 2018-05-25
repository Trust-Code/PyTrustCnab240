# -*- encoding: utf8 -*-

import codecs
from pycnab240 import errors
from io import IOBase


REGISTER_TYPE_SPECS = {
    2: 'SegmentoTeste'
}


class Event(object):

    def __init__(self, bank):  # event_code):
        self._segments = []
        self.bank = bank
        # self.event_code = event_code TODO FIND OUT WHAT IS THIS
        self._lot_code = None
        self._is_open = True

    def add_segment(self, seg_name, vals):
        segment = self.bank.records[seg_name](**vals)
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

    def __init__(self, bank, header=None, trailer=None):
        self.bank = bank
        self.header = header
        self.trailer = trailer
        self._code = None
        self._events = []
        self._is_open = True

    @property
    def code(self):
        return self._code

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
            raise TypeError('Object must be an instance of Lot')
        self._events.append(event)

    def create_new_event(self):
        event = self.get_active_event()
        if event:
            raise errors.ExistsOpenInstance(event)
        new_event = Event(self.bank)
        self._events.append(new_event)
        return new_event

    def get_active_event(self):
        open_event = False
        for event in self._events:
            if event._is_open:
                open_event = event
        return open_event

    def total_register_lot(self):
        total = 0
        for event in self._events:
            total += len(event)
        return total

    def close_lot(self, header=None, trailer=None):
        self.header = self.bank.records.HeaderLoteCobranca(header)
        self.header = self.bank.records.TrailerLoteCobranca(trailer)
        if hasattr(self.trailer, 'quantidade_registros') and\
                not trailer.get('quantidade_registros'):
            self.trailer.quantidade_registros = self.total_register_lot()
        self._is_open = False
        for event in self._events:
            event.close_event()

    # Breakpoint
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

    def __init__(self, bank, **kwargs):
        """Cnab240 File"""

        self._lots = []
        self.bank = bank
        # self.header = self.bank.records.HeaderArquivo(**kwargs)
        # self.trailer = self.bank.records.TrailerArquivo(**kwargs)

    @property
    def lots(self):
        return self._lots

    def add_lots(self, lot):
        if not isinstance(lot, Lot):
            raise TypeError('Object must be an instance of Lot')
        self._lots.append(lot)
        lot.code = len(self._lots)

    def create_new_lot(self):
        lot = self.get_active_lot()
        if lot:
            raise errors.ExistsOpenInstance(lot)
        new_lot = Lot(self.bank)
        self.add_lots(new_lot)
        return new_lot

    def get_active_lot(self):
        open_lot = False
        for lot in self._lots:
            if lot._is_open:
                open_lot = lot
        return open_lot

    def add_segment(self, seg_name, vals):
        lot = self.get_active_lot()
        if not lot:
            lot = self.create_new_lot()
        event = lot.get_active_event()
        if not event:
            event = lot.create_new_event()
        event.add_segment(seg_name, vals)

    def __str__(self):
        if not self._lots:
            raise errors.EmptyFileError()
        result = []
        # result.append(str(self.header)) Append header and trailer later
        result.extend(str(lot) for lot in self._lots)
        # result.append(str(self.trailer))
        # Empty element so the file will end with \r\n
        result.append('')
        return '\r\n'.join(result)

    def write_to_file(self, file_):
        file_.write(str(self))

    def load_return_file(self, file_):
        if isinstance(file_, (IOBase, codecs.StreamReaderWriter)):
            return TypeError("Wrong file type")
        for line in file:
            register_type = REGISTER_TYPE_SPECS[line[7]]
            segment = self.bank.records[register_type].load_line(line)
            self.add_segment(segment)
            if register_type == 'TrailerLote':
                self.get_active_lot().close_lot()
