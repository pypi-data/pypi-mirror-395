import unittest
import logging
import json
from ipulse_shared_base_ftredge import LogLevel, Action, DataResource,AbstractResource, ProgressStatus, Alert, ReviewStatus, DataUnit, StructLog
from ipulse_shared_data_eng_ftredge import Pipelinemon


class TestPipelinemon(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("test_pipelinemon")
        self.logger.setLevel(logging.DEBUG)
        self.pipelinemon = Pipelinemon(
            base_context="test_pipeline_base_context",
            logger=self.logger
        )

    test_log = StructLog(
            level=LogLevel.INFO,
            action=Action.PERSIST_WRITE,
            resource=DataResource.DB,
            progress_status=ProgressStatus.DONE,
            q=40,
            q_unit=DataUnit.DBROW,
            description="Single log entry test."
        )

    def test_add_single_log(self):
        """Test adding a single log entry to Pipelinemon and verifying it's stored."""
        self.pipelinemon.add_log(self.test_log)
        logs = self.pipelinemon.get_all_logs()
        self.assertEqual(len(logs), 1, "Should have exactly one log in the collector.")

    def test_add_multiple_logs(self):
        """Test adding multiple logs and verify correct count."""
        logs_to_add = [
            StructLog(level=LogLevel.INFO, description="Log 1"),
            StructLog(level=LogLevel.WARNING, description="Log 2"),
            StructLog(level=LogLevel.ERROR, description="Log 3"),
        ]
        self.pipelinemon.add_logs(logs_to_add)
        self.assertEqual(len(self.pipelinemon.get_all_logs()), 3, "All 3 logs should be stored.")

    def test_context_manager(self):
        """Test using Pipelinemon as a context to track logs in a nested context."""
        with self.pipelinemon.context("DataLoad"):
            log1 = StructLog(level=LogLevel.INFO, description="Loading data step 1")
            self.pipelinemon.add_log(log1)
            # Nested context
            with self.pipelinemon.context("Validation"):
                log2 = StructLog(level=LogLevel.WARNING, description="Potential data issue found")
                self.pipelinemon.add_log(log2)

        all_logs = self.pipelinemon.get_all_logs()
        self.assertEqual(len(all_logs), 2, "Two logs should be captured in nested contexts.")
        self.assertIn("DataLoad", all_logs[0]["context"], "First log context should contain DataLoad.")
        self.assertIn("DataLoad", all_logs[1]["context"], "Second log context should contain DataLoad.")
        self.assertIn("Validation", all_logs[1]["context"], "Second log context should contain Validation.")

    def test_early_stop(self):
        """Test pipeline early-stop functionality."""
        # Add a few logs
        self.pipelinemon.add_log(StructLog(level=LogLevel.INFO, description="Starting pipeline."))
        # Trigger early stop
        self.pipelinemon.set_early_stop("Encountered a critical error.")
        self.assertTrue(self.pipelinemon.early_stop, "Early stop should be True.")
        self.assertEqual(self.pipelinemon.early_stop_reason, "Encountered a critical error.", "Early stop reason should match.")

    def test_clearing_logs(self):
        """Test clearing logs and counts."""
        self.pipelinemon.add_log(StructLog(level=LogLevel.INFO, description="Test log"))
        self.assertEqual(len(self.pipelinemon.get_all_logs()), 1, "Should have 1 log initially.")
        # Now clear
        self.pipelinemon.clear_logs_and_counts()
        self.assertEqual(len(self.pipelinemon.get_all_logs()), 0, "All logs should be cleared.")

    def test_larger_log_fields(self):
        """Test adding a log with potentially large field values to see if truncation or counting works."""
        log = StructLog(
            level=LogLevel.INFO,
            description="A" * 10000,
            note="B" * 8500,
            alert=Alert.DATA_VALIDATION_ISSUES,
            log_review_status=ReviewStatus.CLOSED
        )
        self.pipelinemon.add_log(log)
        stored_logs = self.pipelinemon.get_all_logs()
        self.assertEqual(len(stored_logs), 1, "Should store the large log.")
        self.assertTrue(stored_logs[0]["truncated"] is True, "Truncated field should be set to True if any of the fields was truncated")
        self.assertTrue(len(stored_logs[0]["description"]) <= 8000, "Description should be truncated to max_log_field_len.")
        self.assertTrue(len(stored_logs[0]["note"]) <= 8000, "Note should be truncated to max_log_field_len.")

    def test_json_output(self):
        """Test retrieving logs in JSON format."""
        self.pipelinemon.add_log(self.test_log)
        json_output = self.pipelinemon.get_all_logs(in_json_format=True)
        self.assertIsInstance(json_output, str, "JSON output should be a string.")
        parsed_logs = json.loads(json_output)
        self.assertEqual(len(parsed_logs), 1, "There should be 1 log in JSON output.")

    def test_event_and_event_count(self):
        """Test that Pipelinemon tracks event counts correctly."""
        # Create two logs with distinct events
        log1 = StructLog(level=LogLevel.INFO, description="Test Event 1", action=Action.READ)
        log2 = StructLog(level=LogLevel.WARNING,  description="Test Event 2", action=Action.PERSIST_WRITE, resource=DataResource.DB, q=10, q_unit=DataUnit.DBROW)
        log3= StructLog(level=LogLevel.WARNING, description="Test Event 3", action=Action.PERSIST_WRITE,resource=DataResource.DB, q=55, q_unit=DataUnit.DBROW)

        # Add logs and verify counts
        self.pipelinemon.add_log(log1)
        self.pipelinemon.add_log(log2)
        self.pipelinemon.add_log(log3)

        # Internal dictionaries by_event_count and by_level_count should now be updated
        all_logs = self.pipelinemon.get_all_logs()
        self.assertEqual(len(all_logs), 3, "There should be 3 logs stored.")

        # Verify that each event is counted
        event1 = log1.getEvent()
        event2 = log2.getEvent()
        event3 = log3.getEvent()
        self.assertIn(event1, self.pipelinemon.by_event_count, "Event 1 should be tracked in by_event_count.")
        self.assertIn(event2, self.pipelinemon.by_event_count, "Event 2 should be tracked in by_event_count.")
        self.assertIn(event3, self.pipelinemon.by_event_count, "Event 3 should be tracked in by_event_count.")
        self.assertEqual(self.pipelinemon.by_event_count[event1], 1, "Event 1 count should be 1.")
        self.assertEqual(self.pipelinemon.by_event_count[event2], 2, "Event 2 count should be 2.")
        self.assertEqual(self.pipelinemon.by_event_count[event3], 2, "Event 3 count should be 2.")


    def test_count_functions(self):
        """Test multiple counting methods in Pipelinemon."""
        # Add a few logs of different levels and statuses
        logs_to_add = [
            StructLog(level=LogLevel.DEBUG, description="Debug log"),
            StructLog(level=LogLevel.INFO, description="Info log"),
            StructLog(level=LogLevel.WARNING, description="Warning log"),
            StructLog(level=LogLevel.WARNING, description="Another warning"),
            StructLog(level=LogLevel.ERROR, description="Error found"),
        ]
        self.pipelinemon.add_logs(logs_to_add)

        # Test contains_any_logs_for_level
        self.assertTrue(self.pipelinemon.contains_any_logs_for_levels(LogLevel.INFO), "Should have INFO logs.")
        self.assertTrue(self.pipelinemon.contains_any_logs_for_levels([LogLevel.WARNING, LogLevel.ERROR]), "Should have WARNING or higher logs.")
        self.assertFalse(self.pipelinemon.contains_any_logs_for_levels(LogLevel.CRITICAL), "Should have no CRITICAL logs.")

        # Test count_warnings_and_errors
        we_count = self.pipelinemon.count_warnings_and_errors()
        self.assertEqual(we_count, 3, "There should be 3 logs at WARNING level or higher (2 warnings + 1 error).")

        # Test count_total_logs_for_level
        debug_count = self.pipelinemon.count_total_logs_for_levels(LogLevel.DEBUG)
        self.assertEqual(debug_count, 1, "Should have exactly 1 DEBUG log.")
        error_count = self.pipelinemon.count_total_logs_for_levels(LogLevel.ERROR)
        self.assertEqual(error_count, 1, "Should have exactly 1 ERROR log.")

        # Test count_logs_for_events_containing (filter by status, context, resource, etc.)
        # For demonstration, we'll add a log with a ProgressStatus for improved coverage
        self.pipelinemon.add_log(StructLog(level=LogLevel.ERROR, progress_status=ProgressStatus.FAILED, description="Completed something"))
        count_completed = self.pipelinemon.count_logs_for_events_containing(
            levels=LogLevel.ERROR, progress_statuses=ProgressStatus.FAILED
        )
        self.assertEqual(count_completed, 1, "Should have exactly 1 log with FAILED status at ERROR level.")

        self.pipelinemon.add_log(StructLog(level=LogLevel.INFO, progress_status=ProgressStatus.DONE, description="Completed something"))
        self.pipelinemon.add_log(StructLog(level=LogLevel.INFO, progress_status=ProgressStatus.DONE_WITH_NOTICES, description="Completed something"))
        self.pipelinemon.add_log(StructLog(level=LogLevel.INFO, progress_status=ProgressStatus.DONE_WITH_NOTICES, description="Completed something"))
        count_completed = self.pipelinemon.count_logs_for_events_containing(
             progress_statuses=ProgressStatus.success_statuses()
        )
        self.assertEqual(count_completed, 3, "Should have exactly 1 log with FAILED status at ERROR level.")
    # def test_count_statuses_for_resources(self):
    #     """Test count_statuses_for_resource to ensure it counts specific progress status for a given resource."""
    #     # Add logs with different resources and statuses
    #     logs = [
    #         PipelineLog(level=LogLevel.INFO, resource=AbstractResource.PIPELINE_ITERATION, progress_status=ProgressStatus.DONE),
    #         PipelineLog(level=LogLevel.WARNING, resource=AbstractResource.PIPELINE_ITERATION, progress_status=ProgressStatus.FAILED),
    #         PipelineLog(level=LogLevel.ERROR, resource=AbstractResource.PIPELINE_ITERATION, progress_status=ProgressStatus.FAILED),
    #         PipelineLog(level=LogLevel.INFO, action= Action.READ, resource=DataResource.DB,  progress_status=ProgressStatus.DONE),
    #     ]
    #     self.pipelinemon.add_logs(logs)

    #     # Only logs for Resource.PIPELINE_ITERATION should be counted
    #     done_count_for_iterations = self.pipelinemon.count_statuses_for_resources(
    #         status=ProgressStatus.DONE,
    #         resource=AbstractResource.PIPELINE_ITERATION
    #     )
    #     self.assertEqual(done_count_for_iterations, 1, "Should count exactly one DONE PIPELINE_ITERATION log.")

    #     failed_iteration_count = self.pipelinemon.count_statuses_for_resource(
    #         status=ProgressStatus.FAILED,
    #         resource=AbstractResource.PIPELINE_ITERATION
    #     )
    #     self.assertEqual(failed_iteration_count, 2, "Should count exactly two FAILED PIPELINE_ITERATION log.")

    def test_count_count_logs_for_events_containing(self):
        """Test count_statuses_for_resource to ensure it counts specific progress status for a given resource."""
        # Add logs with different resources and statuses
        logs = [
            StructLog(level=LogLevel.INFO, resource=AbstractResource.PIPELINE_ITERATION, progress_status=ProgressStatus.DONE),
            StructLog(level=LogLevel.WARNING, resource=AbstractResource.PIPELINE_ITERATION, progress_status=ProgressStatus.FAILED),
            StructLog(level=LogLevel.ERROR, resource=AbstractResource.PIPELINE_ITERATION, progress_status=ProgressStatus.FAILED),
            StructLog(level=LogLevel.INFO, action=Action.READ, resource=DataResource.DB, progress_status=ProgressStatus.DONE),
            StructLog(level=LogLevel.INFO, resource=AbstractResource.PIPELINE_ITERATION, progress_status=ProgressStatus.IN_PROGRESS),
            StructLog(level=LogLevel.INFO, resource=AbstractResource.PIPELINE_ITERATION, progress_status=ProgressStatus.PAUSED),
            StructLog(level=LogLevel.INFO, resource=AbstractResource.PIPELINE_ITERATION, progress_status=ProgressStatus.IN_PROGRESS_WITH_ISSUES),
            StructLog(level=LogLevel.INFO, resource=AbstractResource.PIPELINE_ITERATION, progress_status=ProgressStatus.INTENTIONALLY_SKIPPED),
            StructLog(level=LogLevel.INFO, resource=AbstractResource.PIPELINE_ITERATION, progress_status=ProgressStatus.DONE_WITH_WARNINGS),
            StructLog(level=LogLevel.INFO, resource=AbstractResource.PIPELINE_ITERATION, progress_status=ProgressStatus.DONE_WITH_NOTICES),
        ]
        self.pipelinemon.add_logs(logs)

        # Only logs for Resource.PIPELINE_ITERATION should be counted
        done_count_for_iterations = self.pipelinemon.count_logs_for_events_containing(
            progress_statuses=ProgressStatus.DONE,
            resources=AbstractResource.PIPELINE_ITERATION
        )
        self.assertEqual(done_count_for_iterations, 1, "Should count exactly one DONE PIPELINE_ITERATION log.")

        failed_iteration_count = self.pipelinemon.count_logs_for_events_containing(
            progress_statuses=ProgressStatus.FAILED,
            resources=AbstractResource.PIPELINE_ITERATION
        )
        self.assertEqual(failed_iteration_count, 2, "Should count exactly two FAILED PIPELINE_ITERATION logs.")

        in_progress_count = self.pipelinemon.count_logs_for_events_containing(
            progress_statuses=ProgressStatus.IN_PROGRESS,
            resources=AbstractResource.PIPELINE_ITERATION
        )
        self.assertEqual(in_progress_count, 1, "Should count exactly one IN_PROGRESS PIPELINE_ITERATION log.")

        paused_count = self.pipelinemon.count_logs_for_events_containing(
            progress_statuses=ProgressStatus.PAUSED,
            resources=AbstractResource.PIPELINE_ITERATION
        )
        self.assertEqual(paused_count, 1, "Should count exactly one PAUSED PIPELINE_ITERATION log.")

        cancelled_count = self.pipelinemon.count_logs_for_events_containing(
            progress_statuses=ProgressStatus.IN_PROGRESS_WITH_ISSUES,
            resources=AbstractResource.PIPELINE_ITERATION
        )
        self.assertEqual(cancelled_count, 1, "Should count exactly one IN_PROGRESS_WITH_ISSUES PIPELINE_ITERATION log.")

        intentionally_skipped_count = self.pipelinemon.count_logs_for_events_containing(
            progress_statuses=ProgressStatus.INTENTIONALLY_SKIPPED,
            resources=AbstractResource.PIPELINE_ITERATION
        )
        self.assertEqual(intentionally_skipped_count, 1, "Should count exactly one INTENTIONALLY_SKIPPED PIPELINE_ITERATION log.")

        done_with_warnings_count = self.pipelinemon.count_logs_for_events_containing(
            progress_statuses=ProgressStatus.DONE_WITH_WARNINGS,
            resources=AbstractResource.PIPELINE_ITERATION
        )
        self.assertEqual(done_with_warnings_count, 1, "Should count exactly one DONE_WITH_WARNINGS PIPELINE_ITERATION log.")

        done_with_notices_count = self.pipelinemon.count_logs_for_events_containing(
            progress_statuses=ProgressStatus.DONE_WITH_NOTICES,
            resources=AbstractResource.PIPELINE_ITERATION
        )
        self.assertEqual(done_with_notices_count, 1, "Should count exactly one DONE_WITH_NOTICES PIPELINE_ITERATION log.")

        # Test counting with success_statuses frozenset
        success_count = self.pipelinemon.count_logs_for_events_containing(
            progress_statuses=ProgressStatus.success_statuses(),
            resources=AbstractResource.PIPELINE_ITERATION
        )
        self.assertEqual(success_count, 3, "Should count 3 logs with success statuses (DONE, DONE_WITH_WARNINGS, DONE_WITH_NOTICES).")

        # Test counting with failure_statuses frozenset
        failures_count = self.pipelinemon.count_logs_for_events_containing(
            progress_statuses=ProgressStatus.failure_statuses(),
            resources=AbstractResource.PIPELINE_ITERATION
        )
        self.assertEqual(failures_count, 2, "Should count 3 logs with failure statuses (failed, IN_PROGRESS_WITH_ISSUES).")

        # Test counting with PENDING_STATUSES frozenset
        pending_count = self.pipelinemon.count_logs_for_events_containing(
            progress_statuses=ProgressStatus.pending_statuses(),
            resources=AbstractResource.PIPELINE_ITERATION
        )
        self.assertEqual(pending_count, 2, "Should count 2 logs with pending statuses (in_progress,IN_PROGRESS_WITH_ISSUES).")

        # Test counting with SKIPPED_STATUSES frozenset
        skipped_count = self.pipelinemon.count_logs_for_events_containing(
            progress_statuses=ProgressStatus.skipped_statuses(),
            resources=AbstractResource.PIPELINE_ITERATION
        )
        self.assertEqual(skipped_count, 2, "Should count 2 logs with skipped statuses (intentionally_skipped, paused).")

    def test_get_breakdown_by_event(self):
        """Test get_breakdown_by_event method for event counts."""
        log1 = StructLog(level=LogLevel.INFO, action=Action.READ, description="Reading data")
        log2 = StructLog(level=LogLevel.WARNING, action=Action.PERSIST_WRITE, description="Writing warning data")
        self.pipelinemon.add_logs([log1, log2])

        breakdown_str = self.pipelinemon.get_breakdown_by_event()
        self.assertIn("INFO | read: 1", breakdown_str, "Breakdown should include the first log event.")
        self.assertIn("WARNING | persist_write: 1", breakdown_str, "Breakdown should include the second log event.")

    def test_count_logs_with_frozenset_statuses(self):
        """
        Verify that count_logs_for_events_containing correctly matches
        when we pass a frozenset (e.g., success_statuses).
        """
        logs = [
            StructLog(
                level=LogLevel.INFO,
                progress_status=ProgressStatus.DONE,
                description="done should match success_statuses"
            ),
            StructLog(
                level=LogLevel.WARNING,
                progress_status=ProgressStatus.DONE_WITH_WARNINGS,
                description="done_with_warnings should match success_statuses"
            ),
            StructLog(
                level=LogLevel.ERROR,
                progress_status=ProgressStatus.FINISHED_WITH_ISSUES,
                description="finished_with_issues should NOT match success_statuses"
            ),
            StructLog(
                level=LogLevel.ERROR,
                progress_status=ProgressStatus.FAILED,
                description="failed should NOT match success_statuses"
            )
        ]
        self.pipelinemon.add_logs(logs)

        # Count logs that have a status in success_statuses, across all levels
        count_successes = self.pipelinemon.count_logs_for_events_containing(
            levels=[LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR],
            progress_statuses=ProgressStatus.success_statuses()
        )
        print(" \n ALL LOGS:  \n  ",  self.pipelinemon.get_all_logs())
        print(" \n DONE PRINTING:  \n  ")
        # We expect 2 logs to match (DONE, DONE_WITH_NOTICES)
        self.assertEqual(count_successes, 2, "Should only count logs that match success_statuses.")

    def test_generate_execution_summary(self):
        """Test generate_execution_summary output and format."""
        # Start the pipelinemon to set start time
        self.pipelinemon.start("Begin pipeline for summary test.")
        
        # Add some logs with different statuses
        self.pipelinemon.add_log(StructLog(
            level=LogLevel.INFO,
            resource=AbstractResource.PIPELINE_SUBJECT,
            progress_status=ProgressStatus.DONE,
            description="Subject completed successfully"
        ))
        self.pipelinemon.add_log(StructLog(
            level=LogLevel.INFO,
            resource=AbstractResource.PIPELINE_SUBJECT,
            progress_status=ProgressStatus.DONE_WITH_NOTICES,
            description="Subject completed successfully"
        ))
        self.pipelinemon.add_log(StructLog(
            level=LogLevel.WARNING,
            resource=AbstractResource.PIPELINE_SUBJECT,
            progress_status=ProgressStatus.IN_PROGRESS,
            description="Subject still in progress"
        ))
        self.pipelinemon.add_log(StructLog(
            level=LogLevel.ERROR,
            resource=AbstractResource.PIPELINE_SUBJECT,
            progress_status=ProgressStatus.FAILED,
            description="Subject failed unexpectedly"
        ))

        # Generate the summary
        summary = self.pipelinemon.generate_execution_summary(
            countable_subj_name="stocks",
            total_countables=4,
            subj_resource=AbstractResource.PIPELINE_SUBJECT
        )

        self.assertIn("DONE pipeline_subject(s): [2/4] stocks(s)", summary, "Summary should reference  2/4 done subject.")
        self.assertIn("DONE_WITH_NOTICES: [1]", summary, "Summary should include DONE_WITH_NOTICES: [1 in progress subject.")
        self.assertIn("FINISHED_WITH_ISSUES pipeline_subject(s): [1/4] stocks(s)", summary, "Should show FINISHED WITH ISSUES pipeline_subject(s): [1/4] stocks(s) in the summary.")
        self.assertIn("PENDING pipeline_subject(s): [1/4] stocks(s)", summary, "Should reflect that 1/4 subject is still PENDING.")
        self.assertIn("SKIPPED pipeline_subject(s): [0/4] stocks(s)", summary, "Log level summary should include Skipped.")
        self.assertIn("DONE_WITH_WARNINGS: [0]", summary, "Log level summary should include warnings.")
        self.assertIn("FINISHED_WITH_ISSUES pipeline_subject(s): [1/4]", summary, "Log level summary should include errors.")
        self.assertIn("Duration:", summary, "Should show some pipeline duration in the summary.")


if __name__ == "__main__":
    unittest.main()