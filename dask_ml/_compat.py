import contextlib
import os
from collections.abc import Mapping  # noqa
from typing import Any

import dask
import dask.array as da
import distributed
import packaging.version as pv as pv
import pandas
import sklearn
import sklearn.utils.validation

SK_VERSION = pv.parse(sklearn.__version__)
DASK_VERSION = pv.parse(dask.__version__)
PANDAS_VERSION = pv.parse(pandas.__version__)
DISTRIBUTED_VERSION = pv.parse(distributed.__version__)

DASK_240 = DASK_VERSION >= pv.parse("2.4.0")
DASK_2130 = DASK_VERSION >= pv.parse("2.13.0")
DASK_2_20_0 = DASK_VERSION >= pv.parse("2.20.0")
DASK_2_26_0 = DASK_VERSION >= pv.parse("2.26.0")
DASK_2_28_0 = DASK_VERSION > pv.parse("2.27.0")
DASK_2021_02_0 = DASK_VERSION >= pv.parse("2021.02.0")
DASK_2022_01_0 = DASK_VERSION > pv.parse("2021.12.0")
DISTRIBUTED_2_5_0 = DISTRIBUTED_VERSION > pv.parse("2.5.0")
DISTRIBUTED_2_11_0 = DISTRIBUTED_VERSION > pv.parse("2.10.0")  # dev
DISTRIBUTED_2021_02_0 = DISTRIBUTED_VERSION >= pv.parse("2021.02.0")
PANDAS_1_2_0 = PANDAS_VERSION > pv.parse("1.2.0")
WINDOWS = os.name == "nt"

SKLEARN_1_1_X = SK_VERSION >= pv.parse("1.1")

# 'log_loss' is preferred as of scikit-learn 1.1
if SKLEARN_1_1_X:
    SK_LOG_LOSS = "log_loss"
else:
    SK_LOG_LOSS = "log"


@contextlib.contextmanager
def dummy_context(*args: Any, **kwargs: Any):
    # Not needed if Python >= 3.7 is required
    # https://docs.python.org/3/library/contextlib.html#contextlib.nullcontext
    yield


annotate = dask.annotate if DASK_2021_02_0 else dummy_context

blockwise = da.blockwise


def _check_multimetric_scoring(estimator, scoring=None):
    # TODO: See if scikit-learn 0.24 solves the need for using
    # a private method
    from sklearn.metrics import check_scoring
    from sklearn.metrics._scorer import _check_multimetric_scoring

    if callable(scoring) or isinstance(scoring, (type(None), str)):
        scorers = {"score": check_scoring(estimator, scoring=scoring)}
        return scorers, False
    return _check_multimetric_scoring(estimator, scoring), True
