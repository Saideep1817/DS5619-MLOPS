"""
A minimal, from-scratch expectations framework in the spirit of Great
Expectations / data contracts (this week's lecture). You are implementing
the checking logic yourself rather than importing a library — the goal is
to understand what these tools actually do under the hood.

Fill in the four functions marked # TODO. Do not change the Violation
dataclass or any function signature.
"""
from dataclasses import dataclass


@dataclass
class Violation:
    expectation: str      # name of the check, e.g. "expect_column_not_null"
    column: str            # which column it was checking
    row_index: int          # index into the rows list where it failed
    detail: str              # short human-readable reason


def _is_null(value):
    return value is None or (isinstance(value, str) and value.strip() == "")


def expect_column_not_null(rows, column):
    """Return a Violation for every row where rows[i][column] is null/empty."""
    # TODO: implement
    # raise NotImplementedError
    violations = []
    for i , row in enumerate(rows):
        value = row[column]
        if _is_null(value):
            violations.append(Violation(
                expectation="expect_column_not_null",
                column = column ,
                row_index = i ,
                detail = f"{value} is not allowed to null"
            ))
    return violations

def expect_column_positive(rows, column):
    """Return a Violation for every row where rows[i][column], cast to float,
    is not strictly greater than 0. If the value can't be cast to float at
    all, that also counts as a violation (detail should say so).
    """
    # TODO: implement
    violations = []
    for i , row in enumerate(rows):
        value = row[column]
        try :
            float_val = float(value)
            if float_val <=0 :
                violations.append(Violation(
                    expectation="value need to be strictly greater than zero",
                    column = column ,
                    row_index=i,
                    detail = "value need to greater than zero"
                ))
        except (ValueError,TypeError):
            violations.append(Violation(
                    expectation="value need to be strictly greater than zero",
                    column = column ,
                    row_index=i,
                    detail = "value can't be cast to float"
                ))
    return violations
    raise NotImplementedError


def expect_column_in_set(rows, column, allowed_values):
    """Return a Violation for every row where rows[i][column] is not a member
    of allowed_values (a set or list you're given).
    """
    # TODO: implement
    violations = []
    for i , row in enumerate(rows):
        value = row[column]
        if value not in allowed_values:
            violations.append(Violation(
                expectation="expect_column in allowed_values",
                column = column ,
                row_index = i ,
                detail = f"{value} is not in allowed members"
            ))
    return violations
    raise NotImplementedError


def expect_column_unique(rows, column):
    """Return a Violation for every row AFTER THE FIRST that repeats a value
    already seen in `column`. (i.e. if three rows share a value, rows 2 and 3
    are violations; row 1 is not.)
    """
    # TODO: implement
    violations = []
    for i , row in enumerate(rows):
        value = row[column]
        if _is_null(value):
            violations.append(Violation(
                expectation="expect_column_not_null",
                column = column ,
                row_index = i ,
                detail = f"{value} is not allowed to null"
            ))
    return violations
    raise NotImplementedError
