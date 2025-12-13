"""
ETL Runtime Tracker - Two Modes: With and Without Pipelinemon
============================================================

This version provides two solid ways to track ETL execution:

1. WITH Pipelinemon Integration:
   - Leverages existing Pipelinemon patterns
   - Extracts rich execution data from Pipelinemon's built-in tracking
   - Use from_pipelinemon() and complete_from_pipelinemon()

2. WITHOUT Pipelinemon (Standalone):
   - Simple ETL tracking without Pipelinemon dependency
   - Manual status updates and completion
   - Use standard constructor and complete()

Usage Pattern - WITH Pipelinemon:
```python
# Initialize with Pipelinemon integration
tracker = ETLRuntimeTracker.from_pipelinemon(
    etl_name="oracle_fincore_historic_market_eod_sourcing",
    pipelinemon=your_existing_pipelinemon,
    trigger_type=ActionTrigger.SCHEDULER,
    compute_resource="CLOUD_RUN_JOB"
)

# Your ETL runs with existing Pipelinemon (externally call pipelinemon.end())
# ... ETL logic with pipelinemon.add_log() calls ...

# Complete by extracting from finished Pipelinemon
tracker.complete_from_pipelinemon(
    countable_subject_name="tickers",
    total_countables=150
)
```

Usage Pattern - WITHOUT Pipelinemon:
```python
# Initialize standalone
tracker = ETLRuntimeTracker(
    etl_name="custom_data_processing",
    trigger_type=ActionTrigger.MANUAL,
    compute_resource="LOCAL"
)

# Your ETL logic
tracker.start()
tracker.update_status("PROCESSING")
# ... your ETL logic ...

# Complete manually
tracker.complete(
    execution_status=ProgressStatus.DONE,
    countable_subject_name="records",
    total_countables=1000
)
```
"""

import os
import json
import uuid
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any, Union
from google.cloud import bigquery

# Import your existing Pipelinemon and related classes
from ipulse_shared_data_eng_ftredge.pipelines.pipelinemon import Pipelinemon
from ipulse_shared_base_ftredge import LogLevel, ProgressStatus, DataPrimaryCategory, DatasetScope, ActionTrigger, ComputeResource


class ETLRuntimeTracker:
    """
    ETL Runtime Tracker with deep Pipelinemon integration.
    
    This version extracts rich execution data directly from your existing
    Pipelinemon instance, minimizing additional tracking overhead.
    """
    
    def __init__(
        self,
        etl_name: str,
        trigger_type: Union[ActionTrigger, str],
        compute_resource: Union[ComputeResource, str],
        pipelinemon: Optional[Pipelinemon] = None,
        parent_etl_run_id: Optional[str] = None,
        etl_version: Optional[int] = None,
        compute_resource_description: Optional[str] = None,
        etl_primary_purpose: Optional[str] = None,
        data_scope_affected: Optional[DatasetScope] = None,
        data_subjects_execution_coverage: Optional[str] = None,
        environment: Optional[str] = None,
        initiated_by: Optional[str] = None,
        cost_center: Optional[str] = None,
        sla_deadline_utc: Optional[datetime] = None,
        bigquery_client: Optional[bigquery.Client] = None,
        etl_runtime_table_path: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        generallogger_id: Optional[str] = None,
        monlogger_id: Optional[str] = None,
        inputs: Optional[List[Dict[str, Any]]] = None,
        outputs: Optional[List[Dict[str, Any]]] = None
    ):
        """Initialize ETL Runtime Tracker"""
        self.etl_run_id = str(uuid.uuid4())
        self.parent_etl_run_id = parent_etl_run_id
        self.etl_name = etl_name
        self.etl_version = etl_version
        self.trigger_type = str(trigger_type) if isinstance(trigger_type, ActionTrigger) else trigger_type
        self.compute_resource = str(compute_resource) if isinstance(compute_resource, ComputeResource) else compute_resource
        self.compute_resource_description = compute_resource_description
        self.etl_primary_purpose = etl_primary_purpose
        self.data_scope_affected = data_scope_affected
        self.data_subjects_execution_coverage = data_subjects_execution_coverage
        self.environment = environment or os.getenv('ENV', 'local')
        self.initiated_by = initiated_by or os.getenv('USER_ID', 'unknown')
        self.cost_center = cost_center
        self.sla_deadline_utc = sla_deadline_utc
        
        # Pipelinemon integration
        self.pipelinemon = pipelinemon
        self.pipelinemon_id = pipelinemon.id if pipelinemon else None
        
        # Infrastructure
        self.bq_client = bigquery_client
        self.etl_runtime_table_path = etl_runtime_table_path or f"{os.getenv('PROJECT_ID', 'data-platform-436809')}.{os.getenv('ENV_PREFIX', 'staging')}__dp_shared_governance__monitoring.etl_runtime"
        self.logger = logger or logging.getLogger(__name__)
        
        # Logger tracking
        self.generallogger_id = generallogger_id
        self.monlogger_id = monlogger_id
        
        # Runtime state
        self.started_at_utc = None
        self.completed_at_utc = None
        self.execution_progress_status = ProgressStatus.IN_PROGRESS
        
        # Data lineage - simple lists of dictionaries
        self.inputs: List[Dict[str, Any]] = inputs or []
        self.outputs: List[Dict[str, Any]] = outputs or []
        
        # Data categories
        self.data_primary_categories: List[DataPrimaryCategory] = []
        
        # Flag to track if data lineage needs database update
        self._data_lineage_needs_update: bool = False
        
        # Countable tracking for standalone mode
        self.countable_subject_name: Optional[str] = None
        self.total_countables: Optional[int] = None
        
        # Error tracking
        self.error_message: Optional[str] = None
        self.notes: Optional[str] = None
        
        # SLA tracking
        self.estimated_cost_usd: Optional[float] = None
        self.pipelineflow_final_report: Optional[str] = None

    def _convert_array_to_string(self, value: Any) -> Optional[str]:
        """Convert array/list to comma-separated string for STRING database fields"""
        if value is None:
            return None
        if isinstance(value, list):
            # Handle empty lists
            if not value:
                return ""
            # Convert all items to strings and join with comma
            return ','.join(str(item) for item in value if item is not None)
        elif isinstance(value, str):
            return value  # Already a string
        else:
            return str(value)
    
    @classmethod
    def from_pipelinemon(
        cls,
        etl_name: str,
        pipelinemon: Pipelinemon,
        trigger_type: Union[ActionTrigger, str],
        compute_resource: Union[ComputeResource, str],
        parent_etl_run_id: Optional[str] = None,
        etl_version: Optional[int] = None,
        compute_resource_description: Optional[str] = None,
        etl_primary_purpose: Optional[str] = None,
        data_scope_affected: Optional[DatasetScope] = None,
        data_subjects_execution_coverage: Optional[str] = None,
        environment: Optional[str] = None,
        initiated_by: Optional[str] = None,
        cost_center: Optional[str] = None,
        sla_deadline_utc: Optional[datetime] = None,
        bigquery_client: Optional[bigquery.Client] = None,
        etl_runtime_table_path: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        generallogger_id: Optional[str] = None,
        inputs: Optional[List[Dict[str, Any]]] = None,
        outputs: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> 'ETLRuntimeTracker':
        """
        Create tracker directly from existing Pipelinemon instance.
        
        This is the recommended way to initialize when you already have
        a Pipelinemon running your ETL.
        """
        return cls(
            etl_name=etl_name,
            trigger_type=trigger_type,
            compute_resource=compute_resource,
            pipelinemon=pipelinemon,
            parent_etl_run_id=parent_etl_run_id,
            etl_version=etl_version,
            compute_resource_description=compute_resource_description,
            etl_primary_purpose=etl_primary_purpose,
            data_scope_affected=data_scope_affected,
            data_subjects_execution_coverage=data_subjects_execution_coverage,
            environment=environment,
            initiated_by=initiated_by,
            cost_center=cost_center,
            sla_deadline_utc=sla_deadline_utc,
            bigquery_client=bigquery_client,
            etl_runtime_table_path=etl_runtime_table_path,
            logger=logger,
            generallogger_id=generallogger_id,
            monlogger_id=pipelinemon.logger.name if pipelinemon else None,
            inputs=inputs,
            outputs=outputs,
            **kwargs
        )
    
    def start(self, execution_parameters: Optional[Dict[str, Any]] = None) -> str:
        """Start ETL execution tracking"""
        try:
            self.started_at_utc = datetime.now(timezone.utc)
            self.execution_parameters = execution_parameters or {}
            
            self.logger.debug(f"ETL tracker starting: pipeline={self.etl_name}, trigger={self.trigger_type}, compute={self.compute_resource}")
            
            # Insert initial record
            self._insert_initial_record()
            
            self.logger.info(f"ETL runtime tracking started. Run ID: {self.etl_run_id}")
            return self.etl_run_id
            
        except Exception as e:
            self.logger.error(f"Failed to start ETL runtime tracking: {str(e)}")
            self.logger.debug(f"ETL start failure: pipeline={self.etl_name}, bq_table={self.etl_runtime_table_path}")
            return self.etl_run_id

    def add_data_input(self, input_type: str, logical_domain: Optional[str] = None, physical_domain: Optional[str] = None,
                      system: Optional[str] = None, location: Optional[str] = None, schema_id: Optional[str] = None,
                       schema_name: Optional[str] = None, schema_version: Optional[int] = None):
        """Add a data input to the lineage"""
        self.inputs.append({
            "type": input_type,
            "logical_domain": logical_domain,
            "physical_domain": physical_domain,
            "system": system,
            "location": location,
            "schema_id": schema_id,
            "schema_name": schema_name,
            "schema_version": schema_version
        })
        
        # Mark that data lineage needs to be updated in database
        self._data_lineage_needs_update = True

    def add_data_output(self, output_type: str, logical_domain: Optional[str] = None, physical_domain: Optional[str] = None,
                       system: Optional[str] = None, location: Optional[str] = None, schema_id: Optional[str] = None, 
                       schema_name: Optional[str] = None, schema_version: Optional[int] = None):
        """Add a data output to the lineage"""
        self.outputs.append({
            "type": output_type,
            "logical_domain": logical_domain,
            "physical_domain": physical_domain,
            "system": system,
            "location": location,
            "schema_id": schema_id,
            "schema_name": schema_name,
            "schema_version": schema_version
        })
        
        # Mark that data lineage needs to be updated in database
        self._data_lineage_needs_update = True
    
    def add_data_primary_category(self, category: DataPrimaryCategory):
        """Add a data primary category"""
        if category not in self.data_primary_categories:
            self.data_primary_categories.append(category)
            
            # Mark that data lineage needs to be updated in database
            self._data_lineage_needs_update = True
    
    def set_error_message(self, error_message: str):
        """Set the error message for this ETL run"""
        self.error_message = error_message
    
    def set_notes(self, notes: str):
        """Set notes for this ETL run"""
        self.notes = notes
    
    def set_etl_primary_purpose(self, etl_primary_purpose: str):
        """Set the primary purpose of this ETL"""
        self.etl_primary_purpose = etl_primary_purpose
    
    def set_data_scope_affected(self, data_scope_affected: DatasetScope):
        """Set the data scope affected by this ETL"""
        self.data_scope_affected = data_scope_affected
    
    def set_data_subjects_execution_coverage(self, data_subjects_execution_coverage: str):
        """Set data subjects execution coverage dynamically"""
        self.data_subjects_execution_coverage = data_subjects_execution_coverage
        
    def set_pipelineflow_final_report(self, pipelineflow_final_report: str):
        """Set PipelineFlow final report (truncates to 5000 characters if needed)"""
        if len(pipelineflow_final_report) > 5000:
            self.logger.warning(f"PipelineFlow final report truncated from {len(pipelineflow_final_report)} to 5000 characters")
            self.pipelineflow_final_report = pipelineflow_final_report[:5000]
        else:
            self.pipelineflow_final_report = pipelineflow_final_report
    
    def set_generallogger_id(self, generallogger_id: str):
        """Set general logger ID for traceability"""
        self.generallogger_id = generallogger_id
    
    def set_monlogger_id(self, monlogger_id: str):
        """Set monitoring logger ID for traceability"""
        self.monlogger_id = monlogger_id
    
    def get_all_logical_domains(self) -> List[str]:
        """Get all unique logical domains involved in this ETL"""
        domains = set()
        for entry in self.inputs + self.outputs:
            if entry.get("logical_domain"):
                domains.add(entry["logical_domain"])
        return list(domains)
    
    def get_all_physical_domains(self) -> List[str]:
        """Get all unique physical domains involved in this ETL"""
        domains = set()
        for entry in self.inputs + self.outputs:
            if entry.get("physical_domain"):
                domains.add(entry["physical_domain"])
        return list(domains)
    
    def get_all_domains(self) -> List[str]:
        """Get all unique domains involved in this ETL (legacy method - returns logical domains)"""
        return self.get_all_logical_domains()
    
    def is_cross_domain(self) -> bool:
        """Check if this ETL involves multiple logical domains"""
        return len(self.get_all_logical_domains()) > 1 or len(self.get_all_physical_domains()) > 1

    def update_status(self, execution_status: Union[ProgressStatus, str], progress_percentage: Optional[int] = None):
        """Update execution status during ETL run"""
        self.execution_progress_status = execution_status  # Keep as enum
        
        self.logger.debug(f"ETL status update: {execution_status}")
        
        if self.bq_client:
            try:
                update_data = {
                    "execution_progress_status": str(execution_status),  # Convert to string for storage
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }
                
                if progress_percentage is not None:
                    update_data["progress_percentage"] = progress_percentage
                
                self._safe_update_record(update_data)
                
            except Exception as e:
                self.logger.error(f"Failed to update ETL status: {str(e)}")
                self.logger.debug(f"Status update failure: table={self.etl_runtime_table_path}, status={execution_status}")
        else:
            self.logger.debug("Status update skipped - no BigQuery client")
    
    def set_countable_info(self, countable_subject_name: str, total_countables: int):
        """Set countable information for standalone ETL tracking"""
        self.countable_subject_name = countable_subject_name
        self.total_countables = total_countables
    
    def _update_data_lineage(self):
        """Update database record with current data lineage information"""
        try:
            logical_domains = self.get_all_logical_domains()
            physical_domains = self.get_all_physical_domains()
            self.logger.debug(f"ETL data lineage update: {len(logical_domains)} logical domains, {len(physical_domains)} physical domains, {len(self.inputs)} inputs, {len(self.outputs)} outputs")
            
            update_data = {
                "logical_domains_involved": self._convert_array_to_string(logical_domains),  # Convert to comma-separated string for STRING field
                "physical_domains_involved": self._convert_array_to_string(physical_domains),  # Convert to comma-separated string for STRING field
                "cross_domain_flag": self.is_cross_domain(),
                "inputs": self.inputs if self.inputs else None,  # Pass as Python object for JSON field
                "outputs": self.outputs if self.outputs else None,  # Pass as Python object for JSON field
                "data_primary_categories": self._convert_array_to_string([str(cat) for cat in self.data_primary_categories]) if self.data_primary_categories else None,  # Convert to comma-separated string
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            self._safe_update_record(update_data)
            
            # Reset the flag after successful update
            self._data_lineage_needs_update = False
            
        except Exception as e:
            self.logger.error(f"Failed to update data lineage: {str(e)}")
            self.logger.debug(f"Data lineage failure: {len(self.get_all_logical_domains())} logical domains, {len(self.get_all_physical_domains())} physical domains, bq_client={'present' if self.bq_client else 'missing'}")
    
    def complete_from_pipelinemon(
        self,
        countable_subject_name: str,
        total_countables: int,
        estimated_cost_usd: Optional[float] = None,
        pipelineflow_final_report: Optional[str] = None
    ):
        """
        Complete ETL tracking by extracting data from Pipelinemon.
        
        IMPORTANT: This method expects that pipelinemon.end() has already been called
        externally. It only extracts data from the completed Pipelinemon instance.
        """
        if not self.pipelinemon:
            raise ValueError("complete_from_pipelinemon() requires a pipelinemon instance. Use complete() for standalone mode.")
        
        try:
            self.completed_at_utc = datetime.now(timezone.utc)
            self.estimated_cost_usd = estimated_cost_usd
            self.pipelineflow_final_report = pipelineflow_final_report
            
            self.logger.debug(f"ETL pipelinemon completion: {countable_subject_name}={total_countables}")
            
            # Extract data from Pipelinemon (assumes end() was already called)
            pipelinemon_data = self._extract_pipelinemon_data(
                countable_subject_name,
                total_countables
            )
            
            # Auto-update progress to 100% for successful completion
            status_str = pipelinemon_data.get('execution_progress_status')
            print ("PROGRESS STATUS STR:", status_str)
            if status_str:
                try:
                    # Access enum by name using bracket notation - this is the standard way!
                    status_enum = ProgressStatus[status_str]
                    if status_enum in ProgressStatus.closed_or_skipped_statuses():
                        pipelinemon_data['progress_percentage'] = 100
                    print(">>>>>progress_percentage:", pipelinemon_data['progress_percentage'])
                except KeyError:
                    # If status string doesn't match any enum name, skip progress update
                    self.logger.debug(f"Unknown status string: {status_str}")
                    pass
            
            # Update data lineage if needed before final record update
            if self._data_lineage_needs_update and self.bq_client:
                self._update_data_lineage()
            
            # Update final record with all data
            self._update_final_record_with_pipelinemon(pipelinemon_data)
            
            self.logger.info(f"ETL runtime tracking completed. Run ID: {self.etl_run_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to complete ETL runtime tracking: {str(e)}")
            self.logger.debug(f"Pipelinemon completion failure: pipelinemon_present={self.pipelinemon is not None}")
    
    def complete(
        self,
        execution_progress_status: Union[ProgressStatus, str],
        countable_subject_name: Optional[str] = None,
        total_countables: Optional[int] = None,
        estimated_cost_usd: Optional[float] = None,
        execution_final_log_level: str = "INFO",
        execution_summary: Optional[str] = None,
        pipelineflow_final_report: Optional[str] = None,
        countables_success: Optional[int] = None,
        countables_warnings: Optional[int] = None,
        countables_errors: Optional[int] = None,
        countables_skipped: Optional[int] = None,
        count_log_debug: Optional[int] = None,
        count_log_info: Optional[int] = None,
        count_log_notice: Optional[int] = None,
        count_log_warning: Optional[int] = None,
        count_log_error: Optional[int] = None,
        count_log_critical: Optional[int] = None
    ):
        """
        Complete ETL tracking without Pipelinemon integration.
        
        This method is for standalone ETL tracking where pipelinemon is not used.
        """
        try:
            self.completed_at_utc = datetime.now(timezone.utc)
            self.estimated_cost_usd = estimated_cost_usd
            self.execution_progress_status = execution_progress_status  # Keep as enum
            self.pipelineflow_final_report = pipelineflow_final_report
            
            self.logger.debug(f"ETL standalone completion: status={execution_progress_status}, {countable_subject_name}={total_countables}")
            
            # Create standalone completion data
            completion_data = {
                "execution_progress_status": str(execution_progress_status),  # Convert to string only for storage
                "execution_final_log_level": execution_final_log_level,
                "execution_summary": execution_summary,
                # Note: pipelinemon_event_breakdown is omitted for standalone execution (no placeholder needed)
            }
            
            # Add countable information only if provided
            if countable_subject_name is not None:
                completion_data["countable_subject_name"] = countable_subject_name
            if total_countables is not None:
                completion_data["total_countables"] = total_countables
            
            # Add countable metrics only if explicitly provided
            countable_metrics = {}
            if countables_success is not None:
                countable_metrics["countables_success"] = countables_success
            if countables_warnings is not None:
                countable_metrics["countables_warnings"] = countables_warnings
            if countables_errors is not None:
                countable_metrics["countables_errors"] = countables_errors
            if countables_skipped is not None:
                countable_metrics["countables_skipped"] = countables_skipped
            
            completion_data.update(countable_metrics)
            
            # Add log counts only if explicitly provided
            log_metrics = {}
            if count_log_debug is not None:
                log_metrics["count_log_debug"] = count_log_debug
            if count_log_info is not None:
                log_metrics["count_log_info"] = count_log_info
            if count_log_notice is not None:
                log_metrics["count_log_notice"] = count_log_notice
            if count_log_warning is not None:
                log_metrics["count_log_warning"] = count_log_warning
            if count_log_error is not None:
                log_metrics["count_log_error"] = count_log_error
            if count_log_critical is not None:
                log_metrics["count_log_critical"] = count_log_critical
                
            completion_data.update(log_metrics)
            
            # Auto-update progress to 100% for successful completion
            if execution_progress_status in ProgressStatus.closed_or_skipped_statuses():
                completion_data["progress_percentage"] = 100
            
            # Update data lineage if needed before final record update
            if self._data_lineage_needs_update and self.bq_client:
                self._update_data_lineage()
            
            # Update final record
            self._update_final_record_with_pipelinemon(completion_data)
            
            self.logger.info(f"ETL runtime tracking completed (standalone). Run ID: {self.etl_run_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to complete ETL runtime tracking: {str(e)}")
            self.logger.debug(f"Standalone completion failure: status={execution_progress_status}")
    
    def _extract_pipelinemon_data(self, countable_subject_name: str, total_countables: int) -> Dict[str, Any]:
        """Extract all relevant data from Pipelinemon after end() has been called"""
        pmon = self.pipelinemon
        
        # Get execution status directly from Pipelinemon properties (set after end())
        progress_status = pmon.progress_status
        final_level = pmon.final_level
        
        
        # Get execution summary and event breakdown
        execution_summary = pmon.generate_execution_summary(
            countable_subj_name=countable_subject_name,
            total_countables=total_countables,
            final_level=final_level
        )
        
        event_breakdown = pmon.get_breakdown_by_event()
        
        # Extract log level counts
        log_counts = pmon.by_level_code_count
        
        # Calculate countable success/failure metrics
        # This uses Pipelinemon's event tracking to determine success rates
        countables_data = self._calculate_countables_from_pipelinemon(
            pmon, total_countables, countable_subject_name
        )
        
        return {
            "execution_progress_status": str(progress_status) if progress_status else str(ProgressStatus.UNKNOWN),
            "execution_final_log_level": str(final_level) if final_level else str(LogLevel.INFO),
            "execution_summary": execution_summary,
            "pipelinemon_event_breakdown": event_breakdown,
            "countable_subject_name": countable_subject_name,
            "total_countables": total_countables,
            "count_log_debug": log_counts.get(LogLevel.DEBUG.value, 0),
            "count_log_info": log_counts.get(LogLevel.INFO.value, 0),
            "count_log_notice": log_counts.get(LogLevel.NOTICE.value, 0),
            "count_log_warning": log_counts.get(LogLevel.WARNING.value, 0),
            "count_log_error": log_counts.get(LogLevel.ERROR.value, 0),
            "count_log_critical": log_counts.get(LogLevel.CRITICAL.value, 0),
            **countables_data
        }
    
    def _calculate_countables_from_pipelinemon(self, pmon: Pipelinemon, total_countables: int, subject_name: str) -> Dict[str, int]:
        """
        Get countable success/failure metrics from Pipelinemon's stored subject counts.
        
        Uses the subject counts that were calculated and stored during pipelinemon.end()
        to ensure we're counting only relevant subject events, not all pipeline events.
        """
        # Get the subject counts that were calculated and stored in pipelinemon.end()
        subject_counts = pmon.subject_counts
        
        return {
            "countables_success": subject_counts.get('countables_success', 0),
            "countables_warnings": subject_counts.get('countables_warnings', 0),
            "countables_errors": subject_counts.get('countables_errors', 0),
            "countables_skipped": 0  # Can add this to pipelinemon calculation if needed
        }
    
    def _insert_initial_record(self):
        """Insert initial record in etl_runtime table"""
        if not self.bq_client:
            return
        
        # Get all domains for cross-domain flag and domain tracking
        logical_domains = self.get_all_logical_domains()
        physical_domains = self.get_all_physical_domains()
        
        initial_record = {
            "etl_run_id": self.etl_run_id,
            "parent_etl_run_id": self.parent_etl_run_id,
            "etl_name": self.etl_name,
            "etl_version": self.etl_version,
            "trigger_type": self.trigger_type,
            "compute_resource": self.compute_resource,
            "compute_resource_description": self.compute_resource_description,
            "initiated_by": self.initiated_by,
            "started_at_utc": self.started_at_utc.isoformat() if self.started_at_utc else datetime.now(timezone.utc).isoformat(),
            "execution_progress_status": str(ProgressStatus.IN_PROGRESS),
            "progress_percentage": 0,
            "cross_domain_flag": self.is_cross_domain(),
            "logical_domains_involved": self._convert_array_to_string(logical_domains),  # Convert to comma-separated string for STRING field
            "physical_domains_involved": self._convert_array_to_string(physical_domains),  # Convert to comma-separated string for STRING field
            "data_primary_categories": self._convert_array_to_string([str(cat) for cat in self.data_primary_categories]) if self.data_primary_categories else None,  # Convert to comma-separated string
            "etl_primary_purpose": self.etl_primary_purpose,
            "data_scope_affected": str(self.data_scope_affected) if self.data_scope_affected else None,
            "data_subjects_execution_coverage": self.data_subjects_execution_coverage,
            "inputs": self.inputs if self.inputs else None,  # JSON field - pass as dict/list for JSON serialization
            "outputs": self.outputs if self.outputs else None,  # JSON field - pass as dict/list for JSON serialization
            "pipelinemon_id": self.pipelinemon_id,
            "generallogger_id": self.generallogger_id,
            "monlogger_id": self.monlogger_id,
            "environment": self.environment,
            "cost_center": self.cost_center,
            "sla_deadline_utc": self.sla_deadline_utc.isoformat() if self.sla_deadline_utc else None,
            "error_message": self.error_message,
            "notes": self.notes,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        self._safe_insert_record([initial_record])
    
    def _update_final_record_with_pipelinemon(self, pipelinemon_data: Dict[str, Any]):
        """Update record with final completion data from Pipelinemon"""
        if not self.bq_client:
            return
        
        duration_seconds = (self.completed_at_utc - self.started_at_utc).total_seconds() if self.completed_at_utc and self.started_at_utc else None
        # Convert to Decimal for BigQuery NUMERIC compatibility
        if duration_seconds is not None:
            from decimal import Decimal
            duration_seconds = Decimal(str(round(float(duration_seconds), 3)))
        
        # Calculate SLA compliance
        sla_met = None
        if self.sla_deadline_utc and self.completed_at_utc:
            sla_met = self.completed_at_utc <= self.sla_deadline_utc
        
        update_data = {
            "completed_at_utc": self.completed_at_utc.isoformat() if self.completed_at_utc else None,
            "duration_seconds": duration_seconds,
            "sla_met": sla_met,
            "estimated_cost_usd": self.estimated_cost_usd,
            "pipelineflow_final_report": self.pipelineflow_final_report,
            "error_message": self.error_message,
            "notes": self.notes,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            **pipelinemon_data
        }
        
        self._safe_update_record(update_data)
    
    def _safe_insert_record(self, records: List[Dict]):
        """Safely insert record using batch load job to avoid streaming buffer conflicts"""
        try:
            if not self.bq_client:
                self.logger.warning("BigQuery insert skipped - no client available")
                return
                
            self.logger.debug(f"ETL BigQuery insert: {len(records)} records")
            
            # Use load_table_from_json like in cloud_gcp_bigquery.py
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
                autodetect=False  # Use existing table schema
            )
            
            load_job = self.bq_client.load_table_from_json(
                records,
                self.etl_runtime_table_path,
                job_config=job_config
            )
            
            load_job.result()  # Wait for completion
            
            if load_job.errors:
                self.logger.error(f"BigQuery batch insert errors: {load_job.errors}")
                
        except Exception as e:
            self.logger.error(f"Failed to insert ETL runtime record: {str(e)}")
            self.logger.debug(f"Insert failure: table_path={self.etl_runtime_table_path}")
    
    def _safe_update_record(self, update_data: Dict):
        """Safely update record without breaking ETL if it fails"""
        try:
            if not update_data:
                return
                
            if not self.bq_client:
                self.logger.warning("BigQuery update skipped - no client available")
                return
                
            # Use parameterized query to handle complex data types
            set_clauses = []
            params = {}
            
            for key, value in update_data.items():
                if value is not None:
                    param_name = f"param_{key}"
                    # Special handling for JSON fields - use PARSE_JSON function with STRING parameter
                    if key in ["inputs", "outputs"] and isinstance(value, list):
                        set_clauses.append(f"{key} = PARSE_JSON(@{param_name})")
                    else:
                        set_clauses.append(f"{key} = @{param_name}")
                    params[param_name] = value
            
            if set_clauses:
                merge_query = f"""
                MERGE `{self.etl_runtime_table_path}` AS target
                USING (SELECT @etl_run_id AS etl_run_id) AS source
                ON target.etl_run_id = source.etl_run_id
                WHEN MATCHED THEN UPDATE SET {', '.join(set_clauses)}
                """
                
                # Add etl_run_id parameter
                params['etl_run_id'] = self.etl_run_id
                
                # Configure query with parameters
                from google.cloud import bigquery
                from decimal import Decimal
                job_config = bigquery.QueryJobConfig()
                
                # Build parameters with proper type handling
                query_parameters = []
                
                for param_name, param_value in params.items():
                    if isinstance(param_value, list):
                        # Special handling for inputs/outputs fields that are JSON in BigQuery schema
                        if param_name in ["param_inputs", "param_outputs"]:
                            # For BigQuery JSON fields, we need to pass the actual JSON string
                            # But we want to avoid double-encoding, so we serialize once here
                            json_string = json.dumps(param_value) if param_value else None
                            query_parameters.append(bigquery.ScalarQueryParameter(param_name, "STRING", json_string))
                        else:
                            # For other array fields, treat as array parameters
                            if param_value and isinstance(param_value[0], str):
                                query_parameters.append(bigquery.ArrayQueryParameter(param_name, "STRING", param_value))
                            elif param_value and isinstance(param_value[0], dict):
                                query_parameters.append(bigquery.ArrayQueryParameter(param_name, "JSON", param_value))
                            else:
                                query_parameters.append(bigquery.ArrayQueryParameter(param_name, "STRING", param_value))
                    elif isinstance(param_value, str):
                        # All string parameters including domains_involved and data_primary_categories (now converted to strings)
                        query_parameters.append(bigquery.ScalarQueryParameter(param_name, "STRING", param_value))
                    elif isinstance(param_value, bool):
                        query_parameters.append(bigquery.ScalarQueryParameter(param_name, "BOOL", param_value))
                    elif isinstance(param_value, int):
                        query_parameters.append(bigquery.ScalarQueryParameter(param_name, "INT64", param_value))
                    elif isinstance(param_value, (float, Decimal)):
                        # Handle NUMERIC fields properly
                        if param_name == "param_duration_seconds":
                            query_parameters.append(bigquery.ScalarQueryParameter(param_name, "NUMERIC", param_value))
                        else:
                            query_parameters.append(bigquery.ScalarQueryParameter(param_name, "FLOAT64", float(param_value)))
                    else:
                        query_parameters.append(bigquery.ScalarQueryParameter(param_name, "STRING", str(param_value)))
                
                job_config.query_parameters = query_parameters
                
                job = self.bq_client.query(merge_query, job_config=job_config)
                job.result()
                
        except Exception as e:
            self.logger.error(f"Failed to update ETL runtime record: {str(e)}")
            self.logger.debug(f"Update failure: table_path={self.etl_runtime_table_path}, fields={list(update_data.keys()) if update_data else []}")


# ======================================================================================
# USAGE EXAMPLES: TWO MODES - WITH AND WITHOUT PIPELINEMON
# ======================================================================================

# Example Integration (commented out to avoid execution errors)
"""
def example_with_pipelinemon():
    '''
    Example showing ETL tracking WITH Pipelinemon integration
    '''
    
    # Your existing Pipelinemon setup (unchanged)
    pipelinemon = Pipelinemon(
        base_context="oracle_fincore_historic_market_eod_sourcing",
        logger=your_logger
    )
    
    # Create ETL runtime tracker from existing Pipelinemon
    etl_tracker = ETLRuntimeTracker.from_pipelinemon(
        etl_name="oracle_fincore_historic_market_eod_sourcing",
        pipelinemon=pipelinemon,
        trigger_type=ActionTrigger.SCHEDULER,
        compute_resource="CLOUD_RUN_JOB",
        sla_deadline_utc=datetime(2024, 1, 16, 6, 0, 0, tzinfo=timezone.utc)
    )
    
    # Start tracking (creates initial record)
    etl_tracker.start({
        "provider": "eodhd",
        "batch_size": 1000,
        "max_retries": 3
    })
    
    # Add data lineage information
    etl_tracker.add_data_input(
        input_type="api",
        logical_domain="fincore_historic_market",
        physical_domain="eodhd_api",
        system="eodhd_api",
        location="https://eodhd.com/api/eod"
    )
    
    etl_tracker.add_data_output(
        output_type="table", 
        location="data-platform-436809.dp_oracle_fincore_historic_market__datasets.fact_ohlcva_eod",
        logical_domain="fincore_historic_market",
        physical_domain="dp_oracle_fincore",
        system="bigquery"
    )
    
    # Your existing ETL logic with Pipelinemon (UNCHANGED)
    pipelinemon.start("Processing EOD data for fincore historic market")
    
    try:
        # Your ETL logic with existing Pipelinemon patterns
        with pipelinemon.context("data_extraction"):
            # ... your data extraction logic ...
            # pipelinemon.add_log(SLog(...))  # Your existing logging
        
        with pipelinemon.context("data_transformation"):
            # ... your transformation logic ...
            
        with pipelinemon.context("data_loading"):
            # ... your loading logic ...
        
        # Complete your pipelinemon externally
        pipelinemon.end()
        
        # Complete ETL tracking by extracting from completed pipelinemon
        etl_tracker.complete_from_pipelinemon(
            countable_subject_name="tickers",
            total_countables=150,
            estimated_cost_usd=0.25
        )
        
    except Exception as e:
        # Handle failure
        pipelinemon.end()
        etl_tracker.complete_from_pipelinemon(
            countable_subject_name="tickers",
            total_countables=150,
            estimated_cost_usd=0.10
        )
        raise


def example_standalone_mode():
    '''
    Example showing ETL tracking WITHOUT Pipelinemon (standalone mode)
    '''
    
    # Create ETL runtime tracker without pipelinemon
    etl_tracker = ETLRuntimeTracker(
        etl_name="custom_data_processing",
        trigger_type=ActionTrigger.MANUAL,
        compute_resource="LOCAL",
        etl_primary_purpose="packaging_records_for_consumption",
        data_scope_affected=DatasetScope.SINGLE_DATASET,
        data_subjects_execution_coverage="sequential_batch_subjects_per_loop",
        environment="staging",
        initiated_by="john.doe@company.com"
    )
    
    # Start tracking
    etl_tracker.start({
        "source_file": "customers.csv",
        "target_table": "processed_customers",
        "validation_enabled": True
    })
    
    # Add data lineage
    etl_tracker.add_data_input(
        input_type="file",
        location="/path/to/customers.csv",
        logical_domain="customer_data",
        physical_domain="local_filesystem",
        system="local_file"
    )
    
    etl_tracker.add_data_output(
        output_type="table",
        location="data-platform-436809.customer_mart.processed_customers", 
        logical_domain="customer_data",
        physical_domain="customer_mart",
        system="bigquery"
    )
    
    # Set countable information
    etl_tracker.set_countable_info("customer_records", 10000)
    
    try:
        # Your custom ETL logic
        
        # Update status during processing
        etl_tracker.update_status("PROCESSING", progress_percentage=25)
        
        # ... data extraction logic ...
        
        etl_tracker.update_status("TRANSFORMING", progress_percentage=50)
        
        # ... data transformation logic ...
        
        etl_tracker.update_status("LOADING", progress_percentage=75)
        
        # ... data loading logic ...
        
        # Complete successfully
        etl_tracker.complete(
            execution_progress_status=ProgressStatus.DONE,
            countable_subject_name="customer_records",
            total_countables=10000,
            estimated_cost_usd=1.50,
            execution_final_log_level="INFO",
            execution_summary="Successfully processed 10,000 customer records with data validation",
            countables_success=9950,
            countables_warnings=50,
            countables_errors=0,
            count_log_info=100,
            count_log_warning=5
        )
        
    except Exception as e:
        # Complete with error
        etl_tracker.complete(
            execution_progress_status=ProgressStatus.FAILED,
            countable_subject_name="customer_records", 
            total_countables=10000,
            estimated_cost_usd=0.75,
            execution_final_log_level="ERROR",
            execution_summary=f"ETL failed: {str(e)}",
            countables_success=5000,
            countables_errors=5000,
            count_log_error=1,
            count_log_info=50
        )
        raise
"""
