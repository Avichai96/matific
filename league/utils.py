# utils.py

from django.db.models import Func

class Percentile(Func):
    function = 'PERCENTILE_CONT'
    template = "%(function)s(%(percentile)s) WITHIN GROUP (ORDER BY %(expressions)s)"

    def __init__(self, expression, percentile, **extra):
        super().__init__(expression, percentile=percentile, **extra)
