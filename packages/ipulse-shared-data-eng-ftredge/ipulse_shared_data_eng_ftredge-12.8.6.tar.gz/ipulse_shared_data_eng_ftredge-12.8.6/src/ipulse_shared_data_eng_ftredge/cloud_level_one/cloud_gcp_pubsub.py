import json
import inspect
import logging
from typing import Any, Dict, Optional
from google.cloud import pubsub_v1
from ipulse_shared_base_ftredge import (
    LogLevel, DataResource, Action, ProgressStatus, StructLog,make_json_serializable
)
from ..pipelines import FunctionResult, Pipelinemon, handle_pipeline_operation_exception

def publish_message_to_pubsub_extended(
    message_data: Dict[str, Any],
    topic_path: str,
    project_id: str,
    publisher_client: Optional[pubsub_v1.PublisherClient] = None,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """Publishes a message to Google Cloud Pub/Sub.

    Args:
        message_data: Dictionary containing message data
        topic_path: Full path to pub/sub topic
        project_id: GCP Project ID
        publisher_client: Optional pre-initialized publisher client
        pipelinemon: Optional pipeline monitoring object
        logger: Optional logger instance
        print_out: Whether to print output
        raise_e: Whether to raise exceptions

    Returns:
        FunctionResult with publishing status and message ID
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        project_id=project_id,
        topic_path=topic_path
    )

    try:
        # Initialize client if needed
        if not publisher_client:
            publisher_client = pubsub_v1.PublisherClient()

        # Make message data JSON serializable
        serializable_data = make_json_serializable(message_data)

        # Convert message to JSON and encode
        message_json = json.dumps(serializable_data)
        message_bytes = message_json.encode('utf-8')

        # Publish message
        result.add_state("PUBLISHING_MESSAGE")
        future = publisher_client.publish(topic_path, message_bytes)
        message_id = future.result()  # Wait for message to be published

        result.add_state(f"MESSAGE_PUBLISHED: {message_id}")
        result.add_metadata(message_id=message_id)
        result.final()

        if pipelinemon:
            pipelinemon.add_system_impacted(f"pubsub_topic: {topic_path}")
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                action=Action.PERSIST_PUBLISH_MESSAGE,
                source=DataResource.IN_MEMORY_DATA,
                destination=DataResource.MESSAGING_PUBSUB_TOPIC,
                progress_status=ProgressStatus.DONE,
                q=1,  # Always 1 message
                description=f"Published message {message_id} to {topic_path}"
            ))

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.PERSIST_PUBLISH_MESSAGE,
            source=DataResource.IN_MEMORY_DATA,
            destination=DataResource.MESSAGING_PUBSUB_TOPIC,
            logger=logger,
            q=1,
            pipelinemon=pipelinemon,
            print_out=print_out,
            raise_e=raise_e
        )

    return result
