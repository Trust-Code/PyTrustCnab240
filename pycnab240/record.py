
import os
import json
import unicodedata
import numbers

from glob import iglob
from decimal import Decimal
from collections import OrderedDict
from pycnab240 import errors
from past.builtins import basestring


class BaseField(object):
    def __init__(self):
        self._value = None

    def _normalize_str(self, string):
        """
        Remove special characters and strip spaces
        """
        if string:
            if not isinstance(string, str):
                string = str(string, 'utf-8', 'replace')

            return unicodedata.normalize('NFKD', string).encode(
                'ASCII', 'ignore').decode('ASCII')
        return ''

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.format == 'alfa':
            if not isinstance(value, basestring):
                print("{0} - {1}".format(self.name, value))
                raise errors.TypeError(self, value)

            value = self._normalize_str(value)

            if len(value) > self.digits:
                raise errors.DigitsNumberExceeded(self, value)

        elif self.decimals:
            if not isinstance(value, Decimal):
                print("{0} - {1}".format(self.name, value))
                raise errors.TypeError(self, value)

            num_decimais = value.as_tuple().exponent * -1
            if num_decimais != self.decimals:
                print("{0} - {1}".format(self.name, value))
                raise errors.DecimalsNumError(self, value)

            if len(str(value).replace('.', '')) > self.digits:
                print("{0} - {1}".format(self.name, value))
                raise errors.DigitsNumberExceeded(self, value)

        else:
            if not isinstance(value, int):
                print("{0} - {1}".format(self.name, value))
                raise errors.TypeError(self, value)
            if len(str(value)) > self.digits:
                print("{0} - {1}".format(self.name, value))
                raise errors.DigitsNumberExceeded(self, value)

        self._value = value

    def __str__(self):

        if self.value is None:
            if self.default is not None:
                if self.decimals:
                    self.value = Decimal(
                        '{0:0.{1}f}'.format(self.default,
                                            self.decimals)
                    )
                else:
                    self.value = self.default
            elif (self.default is None) & (self.value is None):
                if self.decimals or self.format == 'num':
                    self.value = 0
                else:
                    self.value = ''
            else:
                raise errors.RequiredFieldError(self.name)

        if self.format == 'alfa' or self.decimals:
            if self.decimals:
                valor = str(self.value).replace('.', '')
                missing_chars = self.digits - len(valor)
                return ('0' * missing_chars) + valor
            else:
                valor = self.value
                missing_chars = self.digits - len(valor)
                return valor + (' ' * missing_chars)

        return '{0:0{1}d}'.format(self.value, self.digits)

    def __repr__(self):
        return str(self)

    def __set__(self, instance, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value


def create_field_class(spec):

    name = spec.get('nome')
    start_pos = spec.get('posicao_inicio') - 1
    end_pos = spec.get('posicao_fim')

    attrs = {
        'name': name,
        'start': start_pos,
        'end': end_pos,
        'digits': end_pos - start_pos,
        'format': spec.get('formato', 'alfa'),
        'decimals': spec.get('decimais', 0),
        'default': spec.get('default'),
    }

    return type(name, (BaseField,), attrs)


class BaseRecord(object):

    def __new__(cls, **kwargs):
        fields = OrderedDict()
        attrs = {'_fields': fields}

        for Field in list(cls._fields_cls.values()):
            field = Field()
            fields.update({field.name: field})
            attrs.update({field.name: field})

        new_cls = type(cls.__name__, (cls, ), attrs)
        return super(BaseRecord, cls).__new__(new_cls)

    def __init__(self, **kwargs):
        import ipdb
        ipdb.set_trace()
        self.fromdict(kwargs)

    def required(self):
        for field in list(self._fields.values()):
            is_control = field.name.startswith('controle_') or\
                field.name.startswith('servico_')
            if not is_control and field.value is not None:
                return True

        return False

    def todict(self):
        data_dict = dict()
        for campo in list(self._campos.values()):
            if campo.value is not None:
                data_dict[campo.name] = campo.value
        return data_dict

    def ignore_fields(self, key):
        return any(key.startswith('vazio'),
                   key.startswith('servico_'),
                   key.startswith('controle_'), )

    def fromdict(self, data_dict):
        for key, value in list(data_dict.items()):
            if hasattr(self, key):  # and not self.ignore_fields(key):
                setattr(self, key, value)

    def __str__(self):
        return ''.join([str(field) for field in list(self._fields.values())])

    def load_line(self, line):
        for field in self._fields.values():
            value = line[field.start:field.end].strip()
            if field.decimals:
                exponente = field.decimals * -1
                dec = value[:exponente] + '.' + value[exponente:]
                field.value = Decimal(dec)
            elif field.formato == 'num':
                try:
                    field.value = int(value)
                except ValueError:
                    raise errors.TipoError(field, value)
            else:
                field.value = value


class Records(object):
    def __init__(self, specs_dirpath):
        record_filepath_list = iglob(os.path.join(specs_dirpath, '*.json'))

        for record_filepath in record_filepath_list:
            record_file = open(record_filepath)
            spec = json.load(record_file)
            record_file.close()
            self.check_json_spec(spec)
            setattr(self, spec.get('nome'), self.create_record_class(spec))

    def __getitem__(self, key):
        return getattr(self, key)

    def check_record_names(self, spec):
        fields = spec['campos']
        names = [item['nome'] for item in fields.values()]
        if len(names) != len(set(names)):
            raise errors.UniqueSpecFieldName(spec)

    def check_record_positions(self, spec):
        fields = spec['campos']
        sorted_keys = sorted(fields.keys())
        init_pos = fields[sorted_keys[0]]['posicao_inicio']
        end_pos = fields[sorted_keys[-1]]['posicao_fim']
        if not (init_pos == 1 and end_pos == 240):
            raise errors.SpecPositionError(spec)
        init_pos = 1
        for key in sorted_keys:
            if fields[key]['posicao_inicio'] != init_pos:
                raise errors.SpecPositionError(spec, fields[key])
            init_pos = fields[key]['posicao_fim'] + 1

    def check_record_format(self, spec):
        fields = spec['campos']
        for field in fields.values():
            if not field.get('default'):
                continue
            if field['formato'] == 'num' and isinstance(
                    field['default'], numbers.Number):
                continue
            elif field['formato'] == 'alfa' and isinstance(
                    field['default'], basestring):
                continue
            raise errors.SpecDefaultValueError(spec, field)

    def check_json_spec(self, spec):
        self.check_record_names(spec)
        self.check_record_positions(spec)
        self.check_record_format(spec)

    def create_record_class(self, spec):
        fields = OrderedDict()
        attrs = {'_fields_cls': fields}
        cls_name = spec.get('nome')

        field_specs = spec.get('campos', {})
        for key in sorted(field_specs.keys()):
            Field = create_field_class(field_specs[key])
            field_input = {Field.name: Field}

            fields.update(field_input)

        return type(cls_name, (BaseRecord, ), attrs)
