import os
import importlib

from pycnab240.record import Records


cwd = os.path.abspath(os.path.dirname(__file__))
bank_name = (fname for fname in os.listdir(cwd)
             if os.path.isdir(os.path.join(cwd, fname)))

for bank_name in bank_name:
    banco_module = importlib.import_module('.'.join((__package__, bank_name)))
    module_path = os.path.join(cwd, bank_name)
    module_specs_path = os.path.join(module_path, 'specs')
    banco_module.records = Records(module_specs_path)
