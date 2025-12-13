# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=broad-exception-raised

import logging
from typing import Optional
import inspect
from google.cloud.secretmanager import SecretManagerServiceClient
from google.cloud.secretmanager_v1.types import AccessSecretVersionResponse

from ipulse_shared_base_ftredge import (DataResource ,
                                        LogLevel ,
                                        Action ,
                                        StructLog ,
                                        log_by_lvl)

from ..pipelines import handle_pipeline_operation_exception, Pipelinemon
from ..pipelines import FunctionResult


############################################################################
##################### SECRET MANAGER ##################################
############################################################################

def get_secret_from_gcp_secret_manager_extended(
    secret_id: str,
    gcp_project_id: str,
    version_id: str = "latest",
    secret_client: Optional[SecretManagerServiceClient] = None,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = True
) -> FunctionResult:
    """GCP-specific secret fetching implementation"""
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        secret_id=secret_id,
        gcp_project_id=gcp_project_id,
        version_id=version_id
    )
    action=Action.READ_SECRET

    try:
        # Create client if not provided
        if not secret_client:
            secret_client = SecretManagerServiceClient()

        name = f"projects/{gcp_project_id}/secrets/{secret_id}/versions/{version_id}"
        response: AccessSecretVersionResponse = secret_client.access_secret_version(request={"name": name})
        result.add_state("Got Response")
        
        if response and response.payload and response.payload.data:
            result.data = response.payload.data.decode("UTF-8")
            result.final()
            if pipelinemon:
                pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                action=action,
                source=DataResource.GCP_SECRET_MANAGER,
                destination=DataResource.IN_MEMORY_DATA,
                progress_status=result.progress_status,
                q=1,
                description=f"Successfully read secret {secret_id}"
            ))

            log_by_lvl(
                info_msg=f"{function_name}: Secret {secret_id} retrieved",
                debug_msg=result.get_final_report(),
                logger=logger,
                print_out=print_out
            )
        else:
            raise Exception(f"Secret {secret_id} not found in project {gcp_project_id}")
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=action,
            source=DataResource.GCP_SECRET_MANAGER,
            destination=DataResource.IN_MEMORY_DATA,
            logger=logger,
            pipelinemon=pipelinemon,
            print_out=print_out,
            raise_e=raise_e
        )
    return result
