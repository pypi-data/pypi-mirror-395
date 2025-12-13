
import unittest
from unittest.mock import Mock, patch
import logging
from ipulse_shared_base_ftredge import (
    Action, Alert, LogLevel, ProgressStatus, Resource, AbstractResource, StructLog, DataUnit
)
from ipulse_shared_data_eng_ftredge.pipelines.pipe_and_ops_exceptions import handle_pipeline_operation_exception
from ipulse_shared_data_eng_ftredge.pipelines.function_result import FunctionResult

class TestHandlePipelineOperationException(unittest.TestCase):
    def setUp(self):
        self.logger = Mock(spec=logging.Logger)
        self.pipelinemon = Mock()
        self.test_exception = Exception("Test error")
        
        # Create basic OpResult for testing
        self.op_result = FunctionResult()

    def test_handle_exception_with_op_result(self):
        """Test handling exception with OpResult object"""
        handle_pipeline_operation_exception(
            e=self.test_exception,
            result=self.op_result,
            action=Action.EXECUTE,
            resource=AbstractResource.PIPELINE_TASK,
            logger=self.logger,
            pipelinemon=self.pipelinemon
        )

        # Verify OpResult was updated
        self.assertEqual(self.op_result.progress_status, ProgressStatus.FAILED)
        self.assertTrue("->Exception/Issue: Test error" in self.op_result.execution_state[-2])
        self.assertTrue(len(self.op_result.issues) > 0)

        # Verify logger was called
        self.logger.warning.assert_called_once()

        # Verify pipelinemon was updated
        self.pipelinemon.add_log.assert_called_once()
        log_call = self.pipelinemon.add_log.call_args[0][0]
        self.assertIsInstance(log_call, StructLog)
        self.assertEqual(log_call.level, LogLevel.ERROR)
        self.assertEqual(log_call.progress_status, ProgressStatus.FAILED)

    def test_handle_exception_with_dict_result(self):
        """Test handling exception with dictionary result"""
        result_dict = {
            "status": {
                "execution_state": "",
                "progress_status": ProgressStatus.IN_PROGRESS,
                "issues": []
            }
        }

        handle_pipeline_operation_exception(
            e=self.test_exception,
            result=result_dict,
            action=Action.EXECUTE,
            resource=AbstractResource.PIPELINE_TASK,
            logger=self.logger,
            pipelinemon=self.pipelinemon
        )

        # Verify dict was updated
        self.assertEqual(result_dict["status"]["progress_status"], ProgressStatus.FAILED)
        self.assertTrue("EXCEPTION" in result_dict["status"]["execution_state"])
        self.assertTrue(len(result_dict["status"]["issues"]) > 0)

        # Verify logger was called
        self.logger.warning.assert_called_once()

    def test_handle_exception_with_alert_and_quantity(self):
        """Test handling exception with alert and quantity parameters"""
        handle_pipeline_operation_exception(
            e=self.test_exception,
            result=self.op_result,
            action=Action.EXECUTE,
            resource=AbstractResource.PIPELINE_OPERATION,
            alert=Alert.ALLOWED_ISSUES_THRESHOLD_REACHED,
            q=100,
            q_unit=DataUnit.DBRECORD,
            logger=self.logger,
            pipelinemon=self.pipelinemon
        )

        # Verify pipelinemon log contains alert and quantity
        log_call = self.pipelinemon.add_log.call_args[0][0]
        self.assertEqual(log_call.alert, Alert.ALLOWED_ISSUES_THRESHOLD_REACHED)
        self.assertEqual(log_call.q, 100)
        self.assertEqual(log_call.q_unit, DataUnit.DBRECORD)

    def test_handle_exception_without_logger(self):
        """Test handling exception without logger"""
        handle_pipeline_operation_exception(
            e=self.test_exception,
            result=self.op_result,
            action=Action.EXECUTE,
            resource=AbstractResource.PIPELINE,
            pipelinemon=self.pipelinemon
        )

        # Verify operation completed without error
        self.assertEqual(self.op_result.progress_status, ProgressStatus.FAILED)
        self.assertTrue(len(self.op_result.issues) > 0)

    def test_handle_exception_without_pipelinemon(self):
        """Test handling exception without pipelinemon"""
        handle_pipeline_operation_exception(
            e=self.test_exception,
            result=self.op_result,
            action=Action.EXECUTE,
            resource=AbstractResource.PIPELINE,
            logger=self.logger
        )

        # Verify operation completed without error
        self.assertEqual(self.op_result.progress_status, ProgressStatus.FAILED)
        self.assertTrue(len(self.op_result.issues) > 0)
        self.logger.warning.assert_called_once()

    def test_handle_exception_with_raise(self):
        """Test handling exception with raise_e=True"""
        with self.assertRaises(Exception):
            handle_pipeline_operation_exception(
                e=self.test_exception,
                result=self.op_result,
                action=Action.EXECUTE,
                resource=AbstractResource.PIPELINE,
                logger=self.logger,
                raise_e=True
            )

        # Verify updates were still made before raising
        self.assertEqual(self.op_result.progress_status, ProgressStatus.FAILED)
        self.logger.warning.assert_called_once()

if __name__ == '__main__':
    unittest.main()