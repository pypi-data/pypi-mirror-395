from clios import Clios

from .registry import load_operator_registry

app = Clios(load_operator_registry(), exe_name="xcdo")
