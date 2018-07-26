
import os
import json
import unicodedata
import numbers

from glob import iglob
from decimal import Decimal
from collections import OrderedDict
from pycnab240 import errors
from past.builtins import basestring, long


class BaseField(object):
    def __init__(self):
        self._value = None

    def _normalize_str(self, string):
        """
        Remove special characters and strip spaces
        """
        if string:
            if not isinstance(string, basestring):
                string = str(string).encode('utf-8')

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
            if not isinstance(value, (int, long)):
                print("{0} - {1}".format(self.name, value))
                raise errors.TypeError(self, value)
            if len(str(value)) > self.digits:
                print("{0} - {1}".format(self.name, value))
                raise errors.DigitsNumberExceeded(self, value)

        self._value = value

    def get_field_default_value(self):
        if self.decimals:
            value = Decimal('{0:0.{1}f}'.format(self.default or 0,
                                                self.decimals))
        elif self.format == 'num':
            value = self.default or 0
        else:
            value = self.default or ''
        return value

    def __str__(self):

        if self.value is None:
            self.value = self.get_field_default_value()

        if self.format == 'alfa' or self.decimals:
            if self.decimals:
                value = str(self.value).replace('.', '')
                missing_chars = self.digits - len(value)
                return ('0' * missing_chars) + value
            else:
                value = self.value
                missing_chars = self.digits - len(value)
                return value + (' ' * missing_chars)

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

    return type(str(name), (BaseField,), attrs)


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

    def load_line(self, string):
        for field in self._fields.values():
            value = string[field.start:field.end].strip()
            if field.decimals:
                exponente = field.decimals * -1
                dec = value[:exponente] + '.' + value[exponente:]
                field.value = Decimal(dec)
            elif field.format == 'num':
                try:
                    field.value = int(value)
                except ValueError:
                    raise errors.TypeError(field, value)
            else:
                field.value = value


class Records(object):
    def __init__(self, specs_dirpath):
        record_filepath_list = iglob(os.path.join(specs_dirpath, '*.json'))

        for record_filepath in record_filepath_list:
            record_file = open(record_filepath)
            spec = json.load(record_file)
            record_file.close()
            specs = self.create_specs_from_subsegments(spec)
            for spec in specs:
                self.check_json_spec(spec)
                setattr(self, spec.get('nome'), self.create_record_class(spec))

    def __getitem__(self, key):
        return getattr(self, key)

    def create_specs_from_subsegments(self, spec):
        if not any("subsegmentos" in campo for campo in spec.get(
                "campos").values()):
            return [spec]
        default_fields, subsegment_field = self.get_subsegments(spec)
        specs = []
        for sub in spec.get('campos')[subsegment_field]['subsegmentos']:
            campos = {field: spec.get('campos')[field] for field in
                      default_fields}
            campos.update({'{}.{}'.format(subsegment_field, key): value for
                          key, value in sub.get('campos').items()})
            specs.append({
                'nome': '{}_{}'.format(spec.get('nome'), sub.get('nome')),
                'campos': campos
            })
        return specs

    def get_subsegments(self, spec):
        campos = spec.get('campos')
        default_fields = [campo for campo, value in campos.items() if
                          "subsegmentos" not in value]
        subsegment_field = [campo for campo in campos if campo not in
                            default_fields][0]
        return default_fields, subsegment_field

    def check_json_spec(self, spec):
        self.check_record_names(spec)
        self.check_record_positions(spec)
        self.check_record_format(spec)

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

    def create_record_class(self, spec):
        fields = OrderedDict()
        attrs = {'_fields_cls': fields}
        cls_name = spec.get('nome')

        field_specs = spec.get('campos', {})
        for key in sorted(field_specs.keys()):
            Field = create_field_class(field_specs[key])
            field_input = {Field.name: Field}

            fields.update(field_input)

        return type(str(cls_name), (BaseRecord, ), attrs)
