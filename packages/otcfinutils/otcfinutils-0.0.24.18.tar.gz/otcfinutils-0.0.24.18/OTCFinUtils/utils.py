import numbers
import re
import math
import json
import pandas as pd
from datetime import datetime
from typing import Optional, Any, Union
from OTCFinUtils.data_structs import _TOKEN_REGEX, MappingFields, Condition, Operator, Category


def extract_segment_object_line(lines: list[str]) -> str:
    for line in lines:
        if "@odata.context" in line:
            return line
    raise ValueError(f"Object line not found in batch response. Lines: {lines}")


def extract_segment_response_id(lines: list[str], id_column: str) -> Optional[str]:
    """
    From a list of lines of a batch response, returns 
    the id of the entity in the response. If a null
    id column name is provided, return None.
    """
    try:
        if not id_column:
            return None

        object_line = extract_segment_object_line(lines)
        json_object = json.loads(object_line)
        object_id: str = json_object[id_column]

        return object_id
    
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON error in response id logic: {e}")
    except KeyError as e:
        raise RuntimeError(f"Key error in response id logic: {e}")
    except Exception as e:
        raise RuntimeError(f"Error in response id logic: {e}")


def extract_segment_status_code(lines: list[str]) -> int:
    """
    From a list of lines of a batch response,
    returns the HTTP status code.
    """
    status_code_line = lines[4]
    status_code_line_parts = status_code_line.split(" ")
    status_code = status_code_line_parts[1]
    status_code = int(status_code)
    
    return status_code


def extract_segment_table_name(lines: list[str]) -> str:
    """
    From a list of lines of a batch response,
    returns the table name of the entity using regex.
    """
    object_line = extract_segment_object_line(lines)
    pattern = r'metadata#([a-z0-9_]+)'
    pattern_matches = re.findall(pattern, object_line)
    
    if not pattern_matches:
        raise RuntimeError(f"Could not find table pattern in string: {object_line}")
    
    table = pattern_matches[0]
    return table


def process_data_type(data: dict) -> None:
    """
    Resolves conflicts between file data types and DV data types.
    """
    try:
        for key, value in data.items():
            if isinstance(value, pd.Timestamp):
                if pd.isna(value):
                    data[key] = None
                else:
                    data[key] = value.strftime("%Y-%m-%d")

            elif isinstance(value, datetime):
                data[key] = value.strftime("%Y-%m-%d")

            elif isinstance(value, str):
                # Try parsing string to date if the key is likely a date field
                if "date" in key.lower() and not re.search(r'\b\d{4}-\d{2}-\d{2}->\d{4}-\d{2}-\d{2}\b', value):
                    try:
                        parsed = pd.to_datetime(value)
                        data[key] = parsed.strftime("%Y-%m-%d")
                    except Exception:
                        data[key] = None

            elif value is None or (not isinstance(value, str) and math.isnan(value)):
                data[key] = None
    
    except Exception as e:
        raise RuntimeError(f"Error: {e}, while processing data object: {data}")
    

def extract_lookup_column(mapping: dict) -> str:
    """
    Gets the lookup column value from the 
    JSON string in the mapping.
    """
    try:
        column_string: str = mapping[MappingFields.LOOKUP_COLUMN]
        # TODO: Remove when no longer needed
        column_string = column_string.replace("'", '"')
        column = json.loads(column_string)[0]
        return column
    
    except Exception as e:
        raise RuntimeError(f"Error while extracting the lookup column: {e}")
    

def extract_file_data(row: pd.Series, mapping: dict):
    """
    Get the data from the appropriate file column, 
    depending on whether the data matches the "exclude 
    values" list from the mapping.
    """
    try:
        if data_equals_exclude_value(row, mapping):
            alternative_file_column: str = mapping[MappingFields.ALTERNATIVE_FILE_COLUMN]
            file_data = row[alternative_file_column]
        else:
            file_column: str = mapping[MappingFields.FILE_COLUMN]
            file_data = row[file_column]
        
        return trim_string_values(file_data)
    
    except Exception as e:
        raise RuntimeError(f"Could not extract file data. Error: {e}")
    

def data_equals_exclude_value(row: pd.Series, mapping: dict) -> bool:
    """
    Checks if the file data matches one of the 
    "exclude values" from the mapping.
    """
    try:
        file_column: str = mapping[MappingFields.FILE_COLUMN]
        exclude_values_list: str = mapping[MappingFields.EXCLUDE_VALUE]
        
        if not exclude_values_list:
            return False
        
        exclude_values: list = json.loads(exclude_values_list)
        
        if row[file_column] in exclude_values:
            return True
        
        return False
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not decode JSON string: {exclude_values_list}. Error: {e}") # type: ignore
    
    except KeyError as e:
        raise KeyError(f"Key error for 'exclude value' logic: {e}")

    except Exception as e:
        raise RuntimeError(f"Error for 'exclude value' logic: {e}")
    

def trim_string_values(value: Any) -> Any:
    """
    If the value is a string trims and returns it.
    Returns all other types of values.
    """
    if isinstance(value, str):
        return value.strip()
    return value


def is_date(value: Any) -> bool:
    """
    Helper function.
    """
    if isinstance(value, pd.Timestamp):
        return True 
    
    elif isinstance(value, str) and re.fullmatch(r"^\d{4}-\d{2}-\d{2}$", value):
        return True
    
    return False


def extract_date_string(value: pd.Timestamp | str) -> str:
    """
    Helper function.
    """
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")
    elif isinstance(value, str):
        return value
    else:
        raise RuntimeError(f"The provided value is not a Timestamp or string: {value}")


def choice_value(file_data: str, mapping: dict) -> int | bool:
    """
    Should return the DV value (number) of the choice we need,
    based on the file data value. 
    """
    choice_string: str = mapping[MappingFields.CHOICE_DICTIONARY]
    
    try:
        choice_mappings: list[dict] = json.loads(choice_string)
    except json.JSONDecodeError:
        raise RuntimeError(f"The choice dictionary: {choice_string} is not a valid JSON object.")
    
    choice_mapping: dict = normalize_choice_map(choice_mappings)
    
    # To normalize the choice strings
    file_data = str(file_data).upper()
    
    return choice_mapping[file_data]


def normalize_choice_map(choice_mappings: list[dict]) -> dict:
    """
    Should return a normalized dictionary of the mappings,
    from the un-normalized list of mappings.
    """
    try:
        choice_mapping = dict()
        
        for item in choice_mappings:
            dv_value: int | bool = item["Value"]
            excel_value: str = item["Excel_Value"]
            
            # To normalize the choice strings
            excel_value = excel_value.upper()
            
            choice_mapping[excel_value] = dv_value
        
        return choice_mapping
    
    except KeyError as e:
        raise KeyError(f"Key Error for choice map normalization: {e}")
    
    except Exception as e:
        raise RuntimeError(f"Error while normalizing choice map: {e}")
    

def default_value(default_value_string: str, column_value: Optional[str] = None, static_mappings: Optional[dict] = None):
    static_mappings = static_mappings or {}

    try:
        raw = default_value_string.strip()

        if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
            raw = raw[1:-1]

        default_value_info = json.loads(raw)

        dv_type = default_value_info.get("type", "")
        dv_value = default_value_info.get("value")
        dv_format = default_value_info.get("format", "")
        dv_old_format = default_value_info.get("old_format", "")

        if dv_type == "current_date":
            date_format = dv_format or "%Y-%m-%d"
            current_time = datetime.now()
            date_string = current_time.strftime(date_format)
            return pd.to_datetime(date_string)
        
        elif dv_type == "timestamp":
            parsed_time = datetime.strptime(column_value, dv_old_format) if column_value else None
            return parsed_time.strftime(dv_format) if parsed_time else None

        elif dv_type == "static_mapping":
            key = dv_value
            if key not in static_mappings:
                raise KeyError(f"Static mapping '{key}' not found")
            v = static_mappings[key]
            return v() if callable(v) else v

        else:
            return dv_value

    except json.JSONDecodeError:
        raise ValueError(f"Could not decode the string: {default_value_string}")

    except KeyError as e:
        raise KeyError(f"Could not read key for default value logic: {e}")

    
def is_float_value(val) -> bool:
    if isinstance(val, numbers.Real) and not isinstance(val, bool):
        return True
    if isinstance(val, str):
        try:
            float(val)
            return True
        except ValueError:
            return False
    return False


def tokenize(formula: str):
    tokens = []
    for mo in re.finditer(_TOKEN_REGEX, formula):
        kind = mo.lastgroup
        value = mo.group()
        if kind in ('COL', 'NUMBER', 'IDENT', 'STRING'):
            tokens.append((kind, value))
        elif kind == 'OP':
            tokens.append((value, value))  # '+', '-', '*', '/', '(', ')'
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise ValueError(f"Unexpected character {value!r} in formula")
    return tokens


def cast_data(value: Any, data_type: str) -> Any:
    """
    Casts the provided value to the given data type.
    Return the value if the data type is unknown.
    """
    try:
        if pd.isna(value):
            return value
        elif data_type == "string":
            return str(value)
        elif data_type == "integer":
            return int(value)
        elif data_type == "decimal":
            return float(value)
        elif data_type == "boolean":
            return bool(value)
        else:
            return value
    
    except Exception as e:
        raise RuntimeError(f"Error while type-casting data: {e}")
    

def get_skip_flag(row: pd.Series, mapping: dict) -> bool:
    """
    Return a flag for whether to skip the current entity or not,
    depending on whether the file data matches one of the "exclude 
    values" in the mapping or if the file data is an empty value.
    """
    is_key: bool = mapping[MappingFields.IS_KEY]

    return (
        (is_key and data_is_empty(row, mapping)) or 
        data_equals_exclude_value(row, mapping)
    )


def data_is_empty(row: pd.Series, mapping: dict) -> bool:
    """
    Checks if the file data is an empty cell. Returns True 
    if empty. Returns False otherwise. Does not take into 
    consideration the alternative file column.
    """
    file_column: str = mapping[MappingFields.FILE_COLUMN]
    file_data = row[file_column]
    
    if pd.isna(file_data) or not file_data:
        return True
    
    return False


def evaluate_condition(row: pd.Series, mappping: dict) -> bool:
    """
    Checks if the mapping has a condition and 
    if the row satisfies the condtition. If true,
    returns the resulting value, otherwise "None".
    """
    try:
        condition_string = mappping[MappingFields.CONDITION]

        if not condition_string:
            return False
        
        condition_dict = json.loads(condition_string)
        condition = Condition.create(condition_dict)
        
        return is_valid(condition, row)
    
    except Exception as e:
        raise RuntimeError(f"Could not evaluate condition. Mapping: {mappping}. Error: {e}")
    

def is_valid(condition: Condition, row: pd.Series) -> bool:
    """
    Evaluates if the row satisfies the given condition.
    """
    if (
        condition.operator == Operator.EQUALS and 
        condition.is_static_value and 
        row[condition.column] == condition.compare_value
    ):
        return True
    
    elif (
        condition.operator == Operator.EQUALS and 
        not condition.is_static_value and 
        row[condition.column] == row[condition.compare_value]
    ):
        return True
    
    # ----------------------------------------------------
    
    elif (
        condition.operator == Operator.NOT_EQUALS and
        condition.is_static_value and
        row[condition.column] != condition.compare_value
    ):
        return True
    
    elif (
        condition.operator == Operator.NOT_EQUALS and
        not condition.is_static_value and
        row[condition.column] != row[condition.compare_value]
    ):
        return True
    
    # ----------------------------------------------------
    
    elif (
        condition.operator == Operator.IS_NULL and
        row[condition.column] == None
    ):
        return True
    
    elif (
        condition.operator == Operator.IS_NOT_NULL and
        row[condition.column] != None
    ):
        return True
    
    # ----------------------------------------------------
    
    elif (
        condition.operator == Operator.SMALLER and
        condition.is_static_value and
        row[condition.column] < condition.compare_value
    ):
        return True
    
    elif (
        condition.operator == Operator.SMALLER and
        not condition.is_static_value and
        row[condition.column] < row[condition.compare_value]
    ):
        return True
    
    # ----------------------------------------------------
    
    elif (
        condition.operator == Operator.GREATER and
        condition.is_static_value and
        row[condition.column] > condition.compare_value
    ):
        return True
    
    elif (
        condition.operator == Operator.GREATER and
        not condition.is_static_value and
        row[condition.column] > row[condition.compare_value]
    ):
        return True
    
    # ----------------------------------------------------

    elif (
        condition.operator == Operator.SMALLER_OR_EQUAL and
        condition.is_static_value and
        row[condition.column] <= condition.compare_value
    ):
        return True
    
    elif (
        condition.operator == Operator.SMALLER_OR_EQUAL and
        not condition.is_static_value and
        row[condition.column] <= row[condition.compare_value]
    ):
        return True
    
    # ----------------------------------------------------
    
    elif (
        condition.operator == Operator.GREATER_OR_EQUAL and
        condition.is_static_value and
        row[condition.column] >= condition.compare_value
    ):
        return True
    
    elif (
        condition.operator == Operator.GREATER_OR_EQUAL and
        not condition.is_static_value and
        row[condition.column] >= row[condition.compare_value]
    ):
        return True
    
    return False


def group_mappings(mappings: list[dict]) -> dict[Category, list[dict]]:
    """
    From all the mapping, return a dictionary of grouped mapping lists,
    based on their categories (sheet name + order number + DV table).
    """
    grouped_mappings: dict[Category, list[dict]] = dict()

    for mapping in mappings:
        group: int = mapping[MappingFields.MAP_GROUP_ORDER]
        table: str = mapping[MappingFields.DV_TABLE]
        sheet: str = mapping[MappingFields.SHEET]

        file_mapping_category = Category(group, table, sheet)

        if file_mapping_category not in grouped_mappings:
            grouped_mappings[file_mapping_category] = list()

        grouped_mappings[file_mapping_category].append(mapping)

    return grouped_mappings


RowLike = Union[pd.Series, dict]

def evaluate_formula_expression_generic(formula: str, row: RowLike) -> Any:
    """
    Shared formula evaluator for importer/exporter.

    Row: pd.Series or dict.
    Formula uses [Column Name] tokens, e.g.:
      [Comm /K] * -1000
      [AcctCode] + '_' + [Symbol] + '_' + DATE([Trade Date]) + '_' + [Buys or Sells]
    """
    # normalize row to plain dict
    if isinstance(row, pd.Series):
        context = row.to_dict()
    elif isinstance(row, dict):
        context = row
    else:
        raise TypeError(f"Row must be dict or Series, got {type(row)}")

    tokens = tokenize(formula)
    pos = 0

    def peek():
        nonlocal pos
        return tokens[pos] if pos < len(tokens) else None

    def advance():
        nonlocal pos
        tok = peek()
        pos += 1
        return tok

    def apply_op(op, left, right):
        # text concatenation
        if isinstance(left, str) or isinstance(right, str):
            if op != '+':
                raise ValueError(f"Operator '{op}' not allowed for text operands")
            return ('' if left is None else str(left)) + ('' if right is None else str(right))

        # numeric ops
        if left is None or right is None:
            raise ValueError("Operations with NULL are not allowed")

        if not (is_float_value(left) and is_float_value(right)):
            raise ValueError(
                f"Incompatible types for operator '{op}': {type(left)}, {type(right)}"
            )

        l = float(left)
        r = float(right)

        if op == '+':
            return l + r
        if op == '-':
            return l - r
        if op == '*':
            return l * r
        if op == '/':
            return l / r
        raise ValueError(f"Unsupported operator '{op}'")

    def parse_factor():
        tok = peek()
        if tok is None:
            raise ValueError("Unexpected end of expression")

        ttype, value = tok

        # [Column Name]
        if ttype == 'COL':
            advance()
            name = value[1:-1]
            if name not in context:
                raise KeyError(f"Column '{name}' not found in row")
            return context[name]

        # numbers
        if ttype == 'NUMBER':
            advance()
            return float(value) if '.' in value else int(value)

        # quoted strings
        if ttype == 'STRING':
            advance()
            return value[1:-1]

        # IDENT (DATE(...), bare names, null)
        if ttype == 'IDENT':
            name = value
            nxt = tokens[pos + 1] if pos + 1 < len(tokens) else None

            # function call, e.g. DATE(...)
            if nxt and nxt[0] == '(':
                func_name = name.upper()
                advance()  # IDENT
                advance()  # '('
                arg = parse_expression()
                if not peek() or peek()[0] != ')':
                    raise ValueError("Missing closing parenthesis in function call")
                advance()  # ')'

                if func_name == "DATE":
                    if arg is None:
                        return None
                    if hasattr(arg, "date"):
                        return arg.date().isoformat()
                    if isinstance(arg, str):
                        return arg.split(" ")[0]
                    return str(arg)

                raise ValueError(f"Unknown function '{func_name}'")

            # bare variable
            advance()
            if name.lower() == 'null':
                return None
            if name not in context:
                raise KeyError(f"Name '{name}' not found in row")
            return context[name]

        # parentheses
        if ttype == '(':
            advance()
            v = parse_expression()
            if not peek() or peek()[0] != ')':
                raise ValueError("Missing closing parenthesis")
            advance()
            return v

        # unary +/- 
        if ttype == '+':
            advance()
            return parse_factor()
        if ttype == '-':
            advance()
            v = parse_factor()
            if not is_float_value(v):
                raise ValueError("Unary '-' only allowed on numeric values")
            return -float(v)

        raise ValueError(f"Unexpected token {tok} in factor")

    def parse_term():
        v = parse_factor()
        while True:
            tok = peek()
            if tok is None or tok[0] not in ('*', '/'):
                break
            op = tok[0]
            advance()
            right = parse_factor()
            v = apply_op(op, v, right)
        return v

    def parse_expression():
        v = parse_term()
        while True:
            tok = peek()
            if tok is None or tok[0] not in ('+', '-'):
                break
            op = tok[0]
            advance()
            right = parse_term()
            v = apply_op(op, v, right)
        return v

    result = parse_expression()
    if pos != len(tokens):
        raise ValueError("Unexpected extra tokens in formula")
    return result


def resolve_condition_output_generic(value_def, row: RowLike):
    """
    Shared logic for Condition.result_value / else_value:
    - If scalar -> return as-is.
    - If dict with keys:
          IS_FORMULA, DIRECT_VALUE, FORMULA
      then:
          IS_FORMULA == "Y" -> evaluate FORMULA on the row
          otherwise          -> DIRECT_VALUE
    """
    if not isinstance(value_def, dict):
        return value_def

    is_formula = str(value_def.get("IS_FORMULA", "N")).upper() == "Y"
    if is_formula:
        formula = value_def.get("FORMULA")
        if not formula:
            return value_def.get("DIRECT_VALUE")
        return evaluate_formula_expression_generic(formula, row)
    else:
        return value_def.get("DIRECT_VALUE")


def extract_sorted_categories(grouped_mappings: dict[Category, list]) -> list[Category]:
    categories: list[Category] = list(grouped_mappings.keys())
    return sorted(categories, key=lambda category: category.group_num)


def extract_sheets(ordered_categories: list[Category]) -> list[str]:
    """
    From the provided categories, returns an ordered list of the sheet names,
    based on the map group ordering of the categories.
    """
    sheets: list[str] = []
    for category in ordered_categories:
        if category.sheet not in sheets:
            sheets.append(category.sheet)
    return sheets


def trim_string_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def test_func():
    return "..."