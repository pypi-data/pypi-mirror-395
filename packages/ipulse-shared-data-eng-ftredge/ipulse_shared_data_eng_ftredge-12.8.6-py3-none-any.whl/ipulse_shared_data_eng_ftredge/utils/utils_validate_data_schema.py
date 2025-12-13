# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught

import datetime
from ipulse_shared_base_ftredge import LogLevel, DataResource, Action,StructLog


def check_format_against_schema_template(data_to_check, schema, resource:DataResource=DataResource.IN_MEMORY_DATA, dt_ts_to_str=True, check_max_length=True):
    """Ensure Update dict corresponds to the config schema, ensuring proper formats and lengths."""
    checked_data = {}
    warnings_or_error = []  # Group warnings and errors for a given run

    try:
        # Process updates to conform to the schema
        for field in schema:
            field_name = field["name"]
            field_type = field["type"]
            mode = field["mode"]

            # Initialize notice to None at the start of each field processing
            warning = None

            if field_name in data_to_check:
                value = data_to_check[field_name]
                if value is None:
                    if mode == "REQUIRED":
                        warnings_or_error.append(StructLog(level=LogLevel.WARNING,
                                                             resource=resource,
                                                             action=Action.VALIDATE_AGAINST_SCHEMA,
                                                            description=f"Required field -'{field_name}'- is missing in the updates."))
                        continue
                else:
                    # Handle date and timestamp formatting
                    if field_type == "DATE":
                        value, warning = handle_date_fields(field_name, value, dt_ts_to_str,resource)
                    elif field_type == "TIMESTAMP":
                        value, warning = handle_timestamp_fields(field_name, value, dt_ts_to_str,resource)
                    elif field_type in ["STRING", "INT64", "FLOAT64", "BOOL"]:
                        value, warning = handle_type_conversion(field_type, field_name, value,resource)

                    if warning:
                        warnings_or_error.append(warning)

                    # Check and handle max length restriction
                    if check_max_length and "max_length" in field:
                        value, warning = check_and_truncate_length(field_name, value, field["max_length"],resource)
                        if warning:
                            warnings_or_error.append(warning)

                    # Only add to the dictionary if value is not None or the field is required
                    checked_data[field_name] = value

            elif mode == "REQUIRED":
                warnings_or_error.append(StructLog(level=LogLevel.WARNING,
                                                    resource=resource,
                                                    action=Action.VALIDATE_AGAINST_SCHEMA,
                                                    description=f"Required field -'{field_name}'- is missing in the updates."))

    except Exception as e:
        warnings_or_error.append(StructLog(level=LogLevel.WARNING,
                                            resource=resource,
                                            action=Action.VALIDATE_AGAINST_SCHEMA,
                                            e=e,
                                            description=f"An error occurred during update check for value {data_to_check}: {str(e)}"))

    return checked_data, warnings_or_error



def handle_date_fields(field_name, value, dt_ts_to_str, resource):
    """Handles date fields, ensuring they are in the correct format and optionally converts them to string."""
    if isinstance(value, datetime.date):
        if dt_ts_to_str:
            return value.strftime("%Y-%m-%d"), None
        return value, None
    elif isinstance(value, str):
        try:
            parsed_date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
            if dt_ts_to_str:
                return value, None
            return parsed_date, None
        except ValueError:
            return None, StructLog(level=LogLevel.WARNING,
                                    resource=resource,
                                    action=Action.VALIDATE_AGAINST_SCHEMA,
                                    description=f"Expected a DATE in YYYY-MM-DD format but got '{value}'. for field -'{field_name}'")
    else:
        return None,  StructLog(level=LogLevel.WARNING,
                                  resource=resource,
                                                             action=Action.VALIDATE_AGAINST_SCHEMA,
                                  description= f"Expected a DATE or YYYY-MM-DD str format but got '{value}' of type {type(value).__name__}. for field -'{field_name}'")


def handle_timestamp_fields(field_name, value, dt_ts_to_str,resource):
    """Handles timestamp fields, ensuring they are in the correct format and optionally converts them to ISO format string."""
    if isinstance(value, datetime.datetime):
        if dt_ts_to_str:
            return value.isoformat(), None
        return value, None
    elif isinstance(value, str):
        try:
            parsed_datetime = datetime.datetime.fromisoformat(value)
            if dt_ts_to_str:
                return value, None
            return parsed_datetime, None
        except ValueError:
            return None,  StructLog(level=LogLevel.WARNING,
                                    resource=resource,
                                    action=Action.VALIDATE_AGAINST_SCHEMA,
                                         description= f"Expected ISO format TIMESTAMP but got '{value}'. for field -'{field_name}'")
    else:
        return None, StructLog(level=LogLevel.WARNING,
                                 resource=resource,
                                action=Action.VALIDATE_AGAINST_SCHEMA,
                                 description= f"Expected ISO format TIMESTAMP but got '{value}' of type {type(value).__name__} for field -'{field_name}'.")


def check_and_truncate_length(field_name, value, max_length,resource):
    """Checks and truncates the length of string fields if they exceed the max length."""
    if isinstance(value, str) and len(value) > max_length:
        return value[:max_length],StructLog(level=LogLevel.WARNING,
                                    resource=resource,
                                    action=Action.VALIDATE_AGAINST_SCHEMA,
                             description= f"Field exceeds max length: {len(value)}/{max_length}. Truncating. for field -'{field_name}'")

    return value, None



def handle_type_conversion(field_type, field_name, value,resource):
    if field_type == "STRING" and not isinstance(value, str):
        return str(value), StructLog(level=LogLevel.WARNING,
                                    resource=resource,
                                    action=Action.VALIDATE_AGAINST_SCHEMA,
                                    description= f"Expected STRING but got '{value}' of type {type(value).__name__} for field -'{field_name}'. ")

    if field_type == "INT64" and not isinstance(value, int):
        try:
            return int(value), None
        except ValueError:
            return None, StructLog(level=LogLevel.WARNING,
                                    resource=resource,
                                    action=Action.VALIDATE_AGAINST_SCHEMA,
                                    description=f"Expected INTEGER, but got '{value}' of type {type(value).__name__} for field -'{field_name}'.")
    if field_type == "FLOAT64" and not isinstance(value, float):
        try:
            return float(value), None
        except ValueError:
            return None, StructLog(level=LogLevel.WARNING,
                                    resource=resource,
                                    action=Action.VALIDATE_AGAINST_SCHEMA,
                                    description=f"Expected FLOAT, but got  '{value}' of type {type(value).__name__} for field -'{field_name}'.")
    if field_type == "BOOL" and not isinstance(value, bool):
        return bool(value), StructLog(level=LogLevel.WARNING,
                                    resource=resource,
                                    action=Action.VALIDATE_AGAINST_SCHEMA,
                                    description=f"Expected BOOL, but got  '{value}'. Converting as {bool(value)} for field -'{field_name}'.")

    return value, None