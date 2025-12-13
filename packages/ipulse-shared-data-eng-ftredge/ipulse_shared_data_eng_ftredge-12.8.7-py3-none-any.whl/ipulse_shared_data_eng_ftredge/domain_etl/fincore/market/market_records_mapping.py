from datetime import datetime, date, time, timezone
from ipulse_shared_base_ftredge import RecordsSamplingType

def _to_firestore_datetime(val):
    if isinstance(val, date) and not isinstance(val, datetime):
        return datetime.combine(val, time.min, tzinfo=timezone.utc)
    return val

def build_firestore_record_from_sourced_records(collection_name: str, record: dict, dt: datetime) -> dict:
    match collection_name:
        case "papp_oracle_fincore_historic_market__datasets.eod_ohlcv":  # Uses AutoStrEnum string value
            return {
                "date": dt,
                "open":   record["open"],
                "high":   record["high"],
                "low":    record["low"],
                "close":  record["close"],
                "volume": record["volume"]
            }
        case "papp_oracle_fincore_historic_market__datasets.eod_close":
            return {
                "date": dt,
                "close": record["close"]
            }
        case "papp_oracle_fincore_historic_market__datasets.eod_close_with_actions":
            return {
                "date": dt,
                "close": record["close"]
            }
        case _:
            raise ValueError(f"Unsupported record type: {collection_name}")
        

def build_firestore_record_from_bigquery_data(record_type: str, record: dict, dt: datetime | date) -> dict:
    """
    Build firestore record from BigQuery fact table data.
    This is similar to build_firestore_record_from_sourced_records but handles BQ field names.
    """
    # Ensure dt is datetime (Firestore requirement)
    dt = _to_firestore_datetime(dt)

    match record_type:

        case "eod_close":
            # Raw close only (for client-side adjustment)
            return {
                "date": dt,
                "close": record.get("close"),
            }

        case "eod_actions":
            # Corporate actions only (splits, dividends, etc.)
            return {
                "ex_dt": dt,
                "type": record.get("action_type"),
                "n": record.get("numerator"),
                "d": record.get("denominator"),
                "curr": record.get("currency_code"),  # Important for dividends
                "decl": _to_firestore_datetime(record.get("declaration_date")),
                "rec": _to_firestore_datetime(record.get("record_date")),
                "pay": _to_firestore_datetime(record.get("payment_date")),
            }

        case "eod_dividend":
            return {
                "ex_dt": dt,
                "amount": record.get("numerator"),
                "curr": record.get("currency_code"),
                "decl": _to_firestore_datetime(record.get("declaration_date")),
                "rec": _to_firestore_datetime(record.get("record_date")),
                "pay": _to_firestore_datetime(record.get("payment_date")),
            }

        case "eod_split":
            return {
                "ex_dt": dt,
                "n": record.get("numerator"),
                "d": record.get("denominator"),
            }
        
        case "eod_close_volume":
            return {
                "date": dt,
                "close": record.get("close"),
                "vol": record.get("volume"),
            }
        
        case "eod_ohlcv":
            return {
                "date": dt,
                "open": record.get("open"),
                "high": record.get("high"),
                "low": record.get("low"),
                "close": record.get("close"),
                "vol": record.get("volume"),
            }

        case "eod_ohlcvad":
            # OHLCV + adjusted for splits AND dividends
            return {
                "date": dt,
                "open": record.get("open"),
                "high": record.get("high"),
                "low": record.get("low"),
                "close": record.get("close"),
                "adjc": record.get("adjc_with_divd"),  # splits + dividends
                "vol": record.get("volume"),
            }


        case "eod_adjc":
            return {
                "date": dt,
                "adjc": record.get("adjc"),
            }

        case "eod_ohlcva":
            return {
                "date": dt,
                "open": record.get("open"),
                "high": record.get("high"),
                "low": record.get("low"),
                "close": record.get("close"),
                "adjc": record.get("adjc"),
                "vol": record.get("volume"),
            }

        

       

        case _:
            raise ValueError(f"Unsupported record type: {record_type}")

def get_bigquery_select_fields_for_record_type(record_type: str) -> str:
    """
    Get the appropriate SELECT fields for BigQuery based on record type.
    """
    match record_type:
        case "eod_close":
            # Raw close only (from fact_ohlcva_eod table)
            return "date_id, close"
            
        case "eod_actions":
            # Corporate actions (from fact_asset_actions table)
            # Note: Uses ex_date instead of date_id
            return "ex_date, action_type, numerator, denominator, currency_code, declaration_date, record_date, payment_date"

        case "eod_close_volume":
            return "date_id, close, volume"

        case "eod_ohlcv":
            return "date_id, open, high, low, close, volume"
            
        case "eod_adjc":
            return "date_id, adjc"
            
        case "eod_ohlcva":
            return "date_id, open, high, low, close, adjc, volume"

        case "eod_adjc_volume":
            return "date_id, adjc, volume"

        case "eod_ohlcvad":
            # OHLCV + adjusted for splits AND dividends
            return "date_id, open, high, low, close, adjc_with_divd, volume"
            
        case _:
            # Default to close if unsupported type
            return "date_id, close"