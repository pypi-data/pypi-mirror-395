from xfintech.fabric.datakind.datakind import DataKind


def test_datakind_members_exist():
    assert DataKind.INTEGER.value == "Integer"
    assert DataKind.FLOAT.value == "Float"
    assert DataKind.STRING.value == "String"
    assert DataKind.BOOLEAN.value == "Boolean"
    assert DataKind.DATETIME.value == "Datetime"
    assert DataKind.CATEGORICAL.value == "Categorical"
    assert DataKind.UNKNOWN.value == "Unknown"


def test_from_str_basic_cases():
    assert DataKind.from_str("Integer") == DataKind.INTEGER
    assert DataKind.from_str("Float") == DataKind.FLOAT
    assert DataKind.from_str("String") == DataKind.STRING
    assert DataKind.from_str("Boolean") == DataKind.BOOLEAN
    assert DataKind.from_str("Datetime") == DataKind.DATETIME
    assert DataKind.from_str("Categorical") == DataKind.CATEGORICAL


def test_from_str_case_insensitive():
    assert DataKind.from_str("integer") == DataKind.INTEGER
    assert DataKind.from_str("FLOAT") == DataKind.FLOAT
    assert DataKind.from_str("sTrInG") == DataKind.STRING
    assert DataKind.from_str("boolean") == DataKind.BOOLEAN
    assert DataKind.from_str("DATETIME") == DataKind.DATETIME
    assert DataKind.from_str("cAtEgOrIcAl") == DataKind.CATEGORICAL


def test_from_str_unknown_returns_unknown():
    assert DataKind.from_str("SomethingElse") == DataKind.UNKNOWN
    assert DataKind.from_str("") == DataKind.UNKNOWN
    assert DataKind.from_str("???") == DataKind.UNKNOWN


def test_str_representation():
    assert str(DataKind.INTEGER) == "Integer"
    assert str(DataKind.STRING) == "String"
    assert str(DataKind.UNKNOWN) == "Unknown"


def test_repr_representation():
    assert repr(DataKind.INTEGER) == "DataKind.INTEGER"
    assert repr(DataKind.CATEGORICAL) == "DataKind.CATEGORICAL"


def test_equality_with_string():
    assert DataKind.INTEGER == "Integer"
    assert DataKind.FLOAT == "float"
    assert DataKind.STRING != "Boolean"
    assert DataKind.DATETIME != "datetime2"
    assert DataKind.CATEGORICAL == "CATEGORICAL"


def test_inequality_with_string():
    assert DataKind.INTEGER != "Float"
    assert DataKind.BOOLEAN != "boolean2"
    assert DataKind.UNKNOWN != "Known"


def test_equality_with_enum():
    assert DataKind.INTEGER == DataKind.INTEGER
    assert DataKind.FLOAT != DataKind.STRING
    assert DataKind.UNKNOWN == DataKind.UNKNOWN


def test_inequality_with_enum():
    assert DataKind.INTEGER != DataKind.FLOAT
    assert DataKind.BOOLEAN != DataKind.DATETIME
    assert DataKind.CATEGORICAL != DataKind.UNKNOWN


def test_missing_method():
    assert DataKind("integer") == DataKind.INTEGER
    assert DataKind("FLOAT") == DataKind.FLOAT
    assert DataKind("unknown_value") == DataKind.UNKNOWN
