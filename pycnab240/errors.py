# -*- coding: utf-8 -*-


class Cnab240Error(Exception):
    """Base Exception for CNAB 240"""


class FieldAttributionError(Cnab240Error):
    """Invalid value attribution to field"""

    def __init__(self, field, value):
        self.field = field
        self.value = value
        super(FieldAttributionError, self).__init__()

    def __str__(self):
        return 'field:{0} format:{1} decimals:{2} digits:{3} - value:{4}'.\
            format(
                self.field.name,
                self.field.format,
                self.field.decimals,
                self.field.digits,
                repr(self.value),
            )


class DigitsNumberExceeded(FieldAttributionError):
    """Attribute value with more digits than field supports"""


class TypeError(FieldAttributionError):
    """Attribute value from type not supported by field"""


class DecimalsNumError(FieldAttributionError):
    """Wrong number of decimals digits"""


class ArgsMissingError(Cnab240Error):
    """Missing arguments when calling method"""

    def __init__(self, missing_args):
        self.missing_args = missing_args
        super(ArgsMissingError, self).__init__()

    def __str__(self):
        return ('Os seguintes kwargs sao obrigatorios e nao foram '
                'encontrados: {0}').format(', '.join(self.missing_args))


class EmptyFileError(Cnab240Error):
    """Trying to write in a empty file"""


class NoEventError(Cnab240Error):
    """Trying to write a Lot without any Event"""


class SpecErrors(Exception):
    """Invalid Spec File"""

    def __init__(self, spec, field=None):
        self.spec = spec
        self.field = field
        super(SpecErrors, self).__init__()

    def __str__(self):
        return ('Error in spec {}'.format(self.spec['nome']))


class UniqueSpecFieldName(SpecErrors):
    """Spec field names must be unique"""

    def __str__(self):
        return ('Spec {} contains duplicated record names.'.format(
            self.spec['nome']))


class SpecPositionError(SpecErrors):
    """Error on spec fields positions"""

    def __str__(self):
        message = 'Position error in spec {}'.format(self.spec['nome'])
        if self.field:
            message += ' on field {}'.format(self.field['nome'])
        return message


class SpecDefaultValueError(SpecErrors):
    """Default field value doesn't match field format"""

    def __str__(self):
        return ("Default value of field {} doesn't match field format in spec"
                " {}".format(self.field['nome'], self.spec['nome']))
