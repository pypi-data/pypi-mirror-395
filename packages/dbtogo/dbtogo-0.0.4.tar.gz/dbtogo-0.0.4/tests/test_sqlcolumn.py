from dbtogo.datatypes import SQLColumn


def test_sqlcolumn():
    name = "name"
    datatype = "type"
    nullable = False
    default = None
    primary = False
    unique = False

    test_col1 = SQLColumn(name, datatype, nullable, default, primary, unique)
    test_col2 = SQLColumn(name, datatype, nullable, default, primary, unique)

    test_col3 = SQLColumn("X", datatype, nullable, default, primary, unique)
    test_col4 = SQLColumn(name, "X", nullable, default, primary, unique)
    test_col5 = SQLColumn(name, datatype, not nullable, default, primary, unique)
    test_col6 = SQLColumn(name, datatype, nullable, False, primary, unique)
    test_col7 = SQLColumn(name, datatype, nullable, default, not primary, unique)
    test_col8 = SQLColumn(name, datatype, nullable, default, primary, not unique)

    assert test_col1.signature() == test_col2.signature()
    assert test_col1.signature() == test_col3.signature()

    assert test_col1.signature() != test_col4.signature()
    assert test_col1.signature() != test_col5.signature()
    assert test_col1.signature() != test_col6.signature()
    assert test_col1.signature() != test_col7.signature()
    assert test_col1.signature() != test_col8.signature()

    assert test_col1.name == name
    assert test_col1.datatype == datatype
    assert test_col1.nullable == nullable
    assert test_col1.default == default
    assert test_col1.primary_key == primary
    assert test_col1.unique == unique
