from clios import OperatorFns


def load_operator_registry() -> OperatorFns:
    from .operators import cdo as cdo
    from .operators import fn_registry
    from .operators import info as info
    from .operators import mer_stat as mer_stat
    from .operators import misc as misc
    from .operators import missing_values as missing_values
    from .operators import plotting as plotting
    from .operators import renaming as renaming
    from .operators import selecting as selecting
    from .operators import time_stat as time_stat
    from .operators import zon_stat as zon_stat

    return fn_registry
