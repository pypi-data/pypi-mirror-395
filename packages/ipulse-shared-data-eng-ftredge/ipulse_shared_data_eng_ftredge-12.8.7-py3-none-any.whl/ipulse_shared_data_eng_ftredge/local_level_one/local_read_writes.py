# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
import os
import json
import csv
from typing import List, Optional, Dict
from ipulse_shared_base_ftredge import (DuplicationHandling, DuplicationHandlingStatus, MatchCondition,log_error, log_info, log_warning)
import logging

def prepare_file_path_and_directory(file_name: str, directory: str = None, create_dir_if_not_exist:bool=True) -> str:
    """
    Prepares the full file path, ensuring the output directory and subdirectories exist.

    Args:
        file_name (str): The name of the file, which may include subdirectories or a full path.
        output_directory (str, optional): The directory where the file should be saved. Defaults to the current working directory.

    Returns:
        str: The full path to the file.
    """
    if os.path.isabs(file_name):
        # If file_name is an absolute path, use it directly
        full_file_path = file_name
    else:
        # Prepare the output directory
        directory = directory or os.getcwd()
        full_file_path = os.path.join(directory, file_name)

    # Create the directory if it doesn't exist
    if create_dir_if_not_exist:
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
    else:
        if not os.path.exists(os.path.dirname(full_file_path)):
            msg = f"Error: Directory not found at path: {os.path.dirname(full_file_path)}"
            raise FileNotFoundError(msg)

    return full_file_path


def read_json_from_local(file_path:str, logger=None, print_out=False, raise_e=False):
    """
    Reads JSON data from a local file.

    Args:
        file_path (str): The path to the file to read.

    Returns:
        dict | list: The JSON data.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        error_msg = f"Error occurred while reading JSON from file path: {file_path} : {type(e).__name__}-{str(e)}"
        log_error(error_msg, logger=logger, print_out=print_out)
        if raise_e:
            raise e
        return None



def read_csv_from_local(file_path: str, delimiter: str = ',', encoding: str = 'utf-8', logger=None) -> Optional[List[Dict[str, str]]]:
    """
    Reads a CSV file and returns its contents as a list of dictionaries where each row is a dictionary.

    :param file_path: Path to the CSV file.
    :param delimiter: Delimiter used in the CSV file (default is ',').
    :param encoding: File encoding (default is 'utf-8').
    :return: A list of dictionaries representing rows in the CSV, or None if file read fails.
    """
    try:
        with open(file_path, mode='r', encoding=encoding) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=delimiter)
            data = list(row for row in reader)
            log_info(msg=f"Successfully read {len(data)} rows from {file_path}", logger=logger)
            return data
    except FileNotFoundError:
        log_error(msg=f"File not found: {file_path}", logger=logger)
    except csv.Error as e:
        log_error(msg=f"Error reading CSV file at {file_path}: {e}", logger=logger)
    except Exception as e:
        log_error(msg=f"An unexpected error occurred while reading {file_path}: {e}", logger=logger)
    return None


def write_csv_to_local(file_path: str, data: List[Dict[str, str]],
              directory:Optional[str]=None, fieldnames: Optional[List[str]] = None,
              delimiter: str = ',', encoding: str = 'utf-8',
              logger:logging.Logger=None) -> bool:
    """
    Writes a list of dictionaries to a CSV file.

    :param file_path: Path to the output CSV file.
    :param data: A list of dictionaries representing rows to be written.
    :param fieldnames: List of field names (optional). If not provided, keys from the first row in `data` will be used.
    :param delimiter: Delimiter used in the CSV file (default is ',').
    :param encoding: File encoding (default is 'utf-8').
    :return: True if the file was written successfully, False otherwise.
    """
    try:
        full_file_path = prepare_file_path_and_directory(file_name=file_path, directory=directory, create_dir_if_not_exist=True)


        if not data:
            log_error(msg="No data provided for writing to CSV.")
            return False

        if fieldnames is None:
            fieldnames = data[0].keys()

        with open(full_file_path, mode='w', encoding=encoding, newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)
            log_info(msg=f"Successfully wrote {len(data)} rows to {full_file_path}",logger=logger)
            return True
    except IOError as e:
        log_error(msg=f"Failed to write CSV file at {full_file_path}: {e}",logger=logger)
    except csv.Error as e:
        log_error(msg=f"Error writing CSV file at {full_file_path}: {e}",logger=logger)
    except Exception as e:
        log_error(msg=f"An unexpected error occurred while writing {full_file_path}: {e}",logger=logger)
    return False

###########################################################################
################## EXTENDED FUNCTIONS #####################################
###########################################################################


def write_json_to_local_extended(data:dict | list | str, file_name:str,
                                duplication_handling:DuplicationHandling ,
                                duplication_match_condition_type:MatchCondition,
                                output_directory:str=None,
                                duplication_match_condition:str | List[str] = "",
                                max_matched_deletable_files:int=1,
                                logger=None, print_out=False, raise_e=False):

    """Saves data to a local JSON file.
    """

    max_deletable_files_allowed = 3

    saved_to_file_path = None
    matched_duplicates_count = 0  # Default to 0
    duplication_handling_status = None
    matched_duplicates_deleted = None
    error_during_operation = None

    response={
        "saved_to_file_path": saved_to_file_path,
        "matched_duplicates_count": matched_duplicates_count,
        "matched_duplicates_deleted": matched_duplicates_deleted,
        "duplication_handling_status": duplication_handling_status,
        "duplication_match_condition_type": duplication_match_condition_type,
        "duplication_match_condition": duplication_match_condition,
        "error_during_operation": error_during_operation
    }

    supported_match_condition_types = [MatchCondition.EXACT, MatchCondition.PREFIX]
    supported_duplication_handling = [DuplicationHandling.RAISE_ERROR, DuplicationHandling.OVERWRITE, DuplicationHandling.INCREMENT, DuplicationHandling.SKIP]

    try:

         # Use the helper function to get the full file path
        full_file_path = prepare_file_path_and_directory(file_name=file_name, directory=output_directory)
        # Extract the directory path, base file name, and extension
        directory_path = os.path.dirname(full_file_path)

        if max_matched_deletable_files > max_deletable_files_allowed:
            msg = f"Error: max_deletable_files should be less than or equal to {max_deletable_files_allowed} for safety. For more, use specific Delete method."
            raise ValueError(msg)

        if duplication_handling not in supported_duplication_handling:
            msg = f"Error: Duplication handling not supported. Supported types: {supported_duplication_handling}"
            raise ValueError(msg)

        if duplication_match_condition_type not in supported_match_condition_types:
            msg = f"Error: Match condition type not supported. Supported types: {supported_match_condition_types}"
            raise ValueError(msg)

        elif duplication_match_condition_type!=MatchCondition.EXACT and not duplication_match_condition:
            msg = f"Error: Match condition is required for match condition type: {duplication_match_condition_type}"
            raise ValueError(msg)

        # Prepare data
        if isinstance(data, (list, dict)):
            data_str = json.dumps(data, indent=2)
        else:
            data_str = data


        # --- Check if File Exists ---
        if duplication_match_condition_type==MatchCondition.PREFIX:
            files_matched_on_condition = [
                os.path.join(directory_path, f) for f in os.listdir(directory_path)
                if f.startswith(duplication_match_condition)
            ]
            if files_matched_on_condition:
                matched_duplicates_count = len(files_matched_on_condition)
        elif duplication_match_condition_type==MatchCondition.EXACT:
            if os.path.exists(full_file_path):
                files_matched_on_condition = [full_file_path] # Always assign a list 
                matched_duplicates_count = 1

        if matched_duplicates_count:
            if duplication_handling==DuplicationHandling.RAISE_ERROR:
                msg = f"Error: File already exists at file path: {full_file_path}"
                raise FileExistsError(msg)

            if duplication_handling == DuplicationHandling.SKIP:
                log_warning(f"Skipping saving to file path: {full_file_path} - file already exists.", logger=logger, print_out=print_out)
                response["duplication_handling_status"] = DuplicationHandlingStatus.SKIPPED.value
                return response  # Return here
            # --- Overwrite Logic --> Delete  ---
            if duplication_handling==DuplicationHandling.OVERWRITE:
                if  matched_duplicates_count > max_matched_deletable_files:
                    msg = f"Error: Attempt to delete {len(files_matched_on_condition)} matched files, but limit is {max_matched_deletable_files}. Operation Cancelled."
                    raise ValueError(msg)

                for path in files_matched_on_condition:
                    os.remove(path)

                deleted_files=",,,".join( files_matched_on_condition)
                log_info(f"Deleted {len(files_matched_on_condition)} files that matched condition: {deleted_files}", logger=logger, print_out=print_out)
                response["matched_duplicates_deleted"] = deleted_files
                response["duplication_handling_status"] = DuplicationHandlingStatus.OVERWRITTEN.value
            # --- Increment Logic ---
            elif duplication_handling==DuplicationHandling.INCREMENT:
                increment = 0
                base_file_name, ext = os.path.splitext(os.path.basename(full_file_path))
                while os.path.exists(full_file_path):
                    increment += 1
                    file_name = f"{base_file_name}_v{increment}{ext}"
                    full_file_path = os.path.join(directory_path, file_name)
                response["duplication_handling_status"] = DuplicationHandlingStatus.INCREMENTED.value

        # --- Save the File ---
        with open(full_file_path, "w", encoding="utf-8") as f:
            f.write(data_str)
        response["saved_to_file_path"] = full_file_path


    except Exception as e:
        error_during_operation=f"Error occurred while writing JSON to file path: {full_file_path} : {type(e).__name__}-{str(e)}"
        log_error(error_during_operation, logger=logger, print_out=print_out)
        response["error_during_operation"] = error_during_operation
        if raise_e:
            raise e

    return response  # Return response once at the end


