from xfintech.engine.kernel.kernel import Kernel


def test_member_values_and_flags():
    assert Kernel.PANDAS.value == "pandas"
    assert Kernel.PANDAS.support is True
    assert Kernel.PANDAS.distributed is False
    assert Kernel.PANDAS.bytesio is False
    assert Kernel.PANDAS.internal is False

    assert Kernel.DASK.value == "dask"
    assert Kernel.DASK.support is False
    assert Kernel.DASK.distributed is True
    assert Kernel.DASK.bytesio is False
    assert Kernel.DASK.internal is False

    assert Kernel.POLARS.value == "polars"
    assert Kernel.POLARS.support is True
    assert Kernel.POLARS.distributed is True
    assert Kernel.POLARS.bytesio is False
    assert Kernel.POLARS.internal is False

    assert Kernel.ARROW.value == "arrow"
    assert Kernel.ARROW.support is True
    assert Kernel.ARROW.distributed is True
    assert Kernel.ARROW.bytesio is True
    assert Kernel.ARROW.internal is True

    assert Kernel.SPARK.value == "spark"
    assert Kernel.SPARK.support is False
    assert Kernel.SPARK.distributed is True
    assert Kernel.SPARK.bytesio is True
    assert Kernel.SPARK.internal is True


def test_default_is_alias_of_arrow():
    assert Kernel.DEFAULT is Kernel.ARROW
    assert Kernel.DEFAULT.value == "arrow"

    names = [m.name for m in Kernel]
    assert "DEFAULT" not in names
    assert ["PANDAS", "DASK", "POLARS", "ARROW", "SPARK"] == names
