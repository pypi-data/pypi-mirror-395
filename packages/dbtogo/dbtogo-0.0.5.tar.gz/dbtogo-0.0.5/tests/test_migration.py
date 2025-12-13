from dbtogo.datatypes import (
    AddCol,
    AddConstraint,
    DropCol,
    RemoveConstraint,
    RenameCol,
    RetypeCol,
    SQLConstraint,
)
from dbtogo.migrations import Migration


def test_migration_is_destructive():
    migration = Migration("test", [])
    assert not migration.is_destructive()

    migration.steps.append(AddCol(None))
    migration.steps.append(AddConstraint("", SQLConstraint.nullable.value))
    migration.steps.append(RemoveConstraint("", SQLConstraint.unique.value))
    migration.steps.append(RenameCol("", ""))

    assert not migration.is_destructive()

    migration.steps.append(RemoveConstraint("", SQLConstraint.primary.value))
    assert migration.is_destructive()
    migration.steps.pop()
    assert not migration.is_destructive()

    migration.steps.append(AddConstraint("", SQLConstraint.primary.value))
    assert migration.is_destructive()
    migration.steps.pop()
    assert not migration.is_destructive()

    migration.steps.append(DropCol(""))
    assert migration.is_destructive()
    migration.steps.pop()
    assert not migration.is_destructive()

    migration.steps.append(RetypeCol("", "", ""))
    assert migration.is_destructive()
    migration.steps.pop()
    assert not migration.is_destructive()
