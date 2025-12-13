# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=broad-exception-caught

from typing import Any, Optional, Dict
from ipulse_shared_base_ftredge import CloudProvider, DataResource, DuplicationHandling, MatchCondition, FileExtension
from ipulse_shared_data_eng_ftredge import Pipelinemon
from ipulse_shared_data_eng_ftredge.pipelines.function_result import FunctionResult
from .cloud_gcp_storage import read_file_from_gcs_extended, write_file_to_gcs_extended, read_json_from_gcs
from .cloud_gcp_secrets import get_secret_from_gcp_secret_manager_extended


#######################################################################################################################
################################ SECRET MANAGERS        ############################################################### 

def get_secret_from_cloud_provider_extended(
    secret_id: str,
    secret_manager_type: DataResource=DataResource.GCP_SECRET_MANAGER,
    secret_client: Any = None,
    gcp_project_id: Optional[str] = None,
    aws_region_name: Optional[str] = None,
    azure_vault_url: Optional[str] = None,
    version: str = "latest",
    pipelinemon = None,
    logger = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """Cross-cloud secret fetching function"""
    
    supported_providers = [DataResource.GCP_SECRET_MANAGER]

    if secret_manager_type == DataResource.GCP_SECRET_MANAGER:
            if not gcp_project_id:
                raise ValueError("gcp_project_id is required for GCP Secret Manager")
            return get_secret_from_gcp_secret_manager_extended(
                secret_client=secret_client,
                secret_id=secret_id,
                gcp_project_id=gcp_project_id,
                version_id=version,
                pipelinemon=pipelinemon,
                logger=logger,
                print_out=print_out,
                raise_e=raise_e
            )
    
    raise ValueError(f"Unsupported secret_manager_type: {secret_manager_type}. Supported: {supported_providers}")


#######################################################################################################################
#######################################################################################################################
#################################################     cloud IO functions      ########################################

def write_file_to_cloud_storage_extended(cloud_storage:CloudProvider | DataResource,
                                         storage_client, data:dict | list | str, bucket_name: str, file_path: str,
                                        duplication_handling:DuplicationHandling, 
                                        duplication_match_condition_type: MatchCondition,
                                        duplication_match_condition: str = "",
                                max_retries:int=2, max_matched_deletable_files:int=1, file_extension:Optional[FileExtension]=None,
                                json_format: str = "standard", # or "newline_delimited"
                                pipelinemon: Optional[Pipelinemon] = None, logger=None, print_out=False, raise_e=False):

    """
    This function writes data to a cloud storage location, based on the cloud storage provider and data source type.
    Pipelinemon if provided, will be used to log the operation. Systems impacted and Write operation status will be logged.
    
    Args:
        json_format: Format for JSON files. "standard" (default) creates regular JSON with indentation.
                    "newline_delimited" creates NEWLINE_DELIMITED_JSON format (one object per line) for BigQuery.
    """

    supported_cloud_storage_values = [CloudProvider.GCP, DataResource.GCS]

    if cloud_storage in [CloudProvider.GCP, DataResource.GCS]:
        return write_file_to_gcs_extended(
            pipelinemon=pipelinemon,
            storage_client=storage_client,
            data=data,
            bucket_name=bucket_name,
            file_path=file_path,
            duplication_handling=duplication_handling,
            duplication_match_condition_type=duplication_match_condition_type,
            duplication_match_condition=duplication_match_condition,
            max_retries=max_retries,
            max_deletable_files=max_matched_deletable_files,
            file_extension=file_extension,
            json_format_if_json_used=json_format,
            logger=logger,
            print_out=print_out,
            raise_e=raise_e
        )

    raise ValueError(f"Unsupported cloud storage : {cloud_storage}. Supported cloud storage values: {supported_cloud_storage_values}")


def read_file_from_cloud_storage_extended(cloud_storage:CloudProvider | DataResource, storage_client,
                                          bucket_name:str, file_path:str, file_extension:Optional[FileExtension]=None,
                                          pipelinemon:Optional[Pipelinemon]=None,logger=None, print_out:bool=False, raise_e:bool=False) -> FunctionResult: 

    supported_cloud_storage_values = [CloudProvider.GCP, DataResource.GCS]

    if cloud_storage in [CloudProvider.GCP, DataResource.GCS]:
        return read_file_from_gcs_extended(storage_client=storage_client, bucket_name=bucket_name, file_extension=file_extension, pipelinemon=pipelinemon,  file_path=file_path, logger=logger, print_out=print_out,raise_e=raise_e)

    raise ValueError(f"Unsupported cloud storage: {cloud_storage}. Supported cloud storage values: {supported_cloud_storage_values}")



def read_json_from_cloud_storage(cloud_storage:CloudProvider | DataResource , storage_client, bucket_name:str, file_name:str, logger=None, print_out:bool=False, raise_e:bool=False):

    supported_cloud_storage_values = [CloudProvider.GCP, DataResource.GCS]

    if cloud_storage in [CloudProvider.GCP, DataResource.GCS]:
        return read_json_from_gcs(storage_client=storage_client, bucket_name=bucket_name, file_name=file_name, logger=logger, print_out=print_out, raise_e=raise_e)

    raise ValueError(f"Unsupported cloud storage: {cloud_storage}. Supported cloud storage values: {supported_cloud_storage_values}")

