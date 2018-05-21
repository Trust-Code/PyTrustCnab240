# -*- encoding: utf8 -*-

from cnab240 import errors


class Event(object):

    def __init__(self, bank, event_code):
        self._segments = []
        self.bank = bank
        self.event_code = event_code
        self._lot_code = None

    def add_segment(self, segment):
        self._segments.append(segment)
        for segment in self._segments:
            segment.servico_codigo_movimento = self.event_code

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


class Lot(object):

    def __init__(self, bank, header=None, trailer=None):
        self.bank = bank
        self.header = header
        self.trailer = trailer
        self._code = None
        self._events = []

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
        self.header = self.bank.records.HeaderArquivo(**kwargs)
        self.trailer = self.bank.records.TrailerArquivo(**kwargs)
        # file = kwargs.get('arquivo')

    @property
    def lots(self):
        return self._lots
