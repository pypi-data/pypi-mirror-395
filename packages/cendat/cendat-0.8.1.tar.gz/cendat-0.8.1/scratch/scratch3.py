import operator
import re

OPERATOR_MAP = {
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
    "in": lambda a, b: a in b,
    "not in": lambda a, b: a not in b,
}
ALLOWED_OPERATORS = set(OPERATOR_MAP.keys())

sorted_operators = sorted(ALLOWED_OPERATORS, key=len, reverse=True)
operators_pattern = "|".join(re.escape(op) for op in sorted_operators)

all_columns = {"one", "two", "three", "NAME"}

if not all_columns:
    # Fallback or handle case with no data/names
    all_columns_pattern = ""
else:
    # FIX: Add re.escape() to handle column names with special regex characters.
    all_columns_pattern = "|".join(re.escape(col) for col in all_columns)

patternL = re.compile(
    r"^\s*("
    + all_columns_pattern
    + r")\s*("
    + operators_pattern
    + r")\s*(.+?)\s*$"  # <-- Change is here
)
patternR = re.compile(
    r"^\s*(.+?)\s*("  # <-- Change is here
    + operators_pattern
    + r")\s*("
    + all_columns_pattern
    + r")\s*$"
)
patternFrac = re.compile(
    r"^\s*(("
    + all_columns_pattern
    + r")\s*/\s*("
    + all_columns_pattern
    + r"))\s*("
    + operators_pattern
    + r")\s*(.+?)\s*$"  # <-- Change is here
)

condition_string = "'CDP' not in NAME"

matchL = patternL.match(condition_string)
matchR = patternR.match(condition_string)
matchFrac = patternFrac.match(condition_string)

if not (matchL or matchR or matchFrac):
    raise ValueError(f"Invalid condition format: '{condition_string}'")

if matchL:
    print(matchL.groups())
elif matchR:
    print(matchR.groups())
else:
    print(matchFrac.groups())
