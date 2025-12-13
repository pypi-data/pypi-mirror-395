# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
from typing import List
from ipulse_shared_base_ftredge import DatasetAttribute


def get_attribute_from_single_symbol_records(records_formatting_provider_short_ref:str, attribute_type:DatasetAttribute, records: List[dict]):


    if records_formatting_provider_short_ref=="eodhd__eod_historic_bulk_single_symbol":
        date_col_name = "date"
        if attribute_type==DatasetAttribute.OLDEST_DATE:
            records.sort(key=lambda x: x[date_col_name])
            return records[0][date_col_name]
        if attribute_type==DatasetAttribute.RECENT_DATE:
            records.sort(key=lambda x: x[date_col_name])
            return records[-1][date_col_name]
        else:
            raise ValueError(f"DatasetAttribute Type {attribute_type} not supported for records_origin_short_ref {records_formatting_provider_short_ref}.")

    elif records_formatting_provider_short_ref=="sourcing_schema_checked":
        date_col_name = "date_id"
        if attribute_type==DatasetAttribute.OLDEST_DATE:
            records.sort(key=lambda x: x[date_col_name])
            return records[0][date_col_name]
        if attribute_type==DatasetAttribute.RECENT_DATE:
            records.sort(key=lambda x: x[date_col_name])
            return records[-1][date_col_name]
        else:
            raise ValueError(f"DatasetAttribute Type {attribute_type} not supported for records_origin_short_ref {records_formatting_provider_short_ref}.")
    else:
        raise ValueError(f"Data Origin Reference {records_formatting_provider_short_ref} not supported.")
