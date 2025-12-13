import pytest
from ipulse_shared_base_ftredge import (
    ProgressStatus, Action, DataResource, 
    StatusCounts,  FileExtension
)
from ipulse_shared_data_eng_ftredge.pipelines.pipelineflow import (
    PipelineTask, PipelineSequence, PipelineDynamicIterator,
    PipelineFlow, PipelineSequenceTemplate
)
from ipulse_shared_data_eng_ftredge.pipelines.function_result import FunctionResult

# Test Fixtures
@pytest.fixture
def function_result():
    result = FunctionResult(name="test_function")
    result.add_issue("Test issue")
    result.add_warning("Test warning")
    result.add_notice("Test notice")
    result.add_metadata(test_key="test_value")
    return result

@pytest.fixture
def task_with_status_tracking():
    task = PipelineTask("test_task", Action.READ, DataResource.FILE)
    task.add_issue("Task issue")
    task.add_warning("Task warning")
    task.add_notice("Task notice")
    return task

@pytest.fixture
def sequence_with_tasks():
    sequence = PipelineSequence("seq1")
    task1 = PipelineTask("task1", Action.READ)
    task2 = PipelineTask("task2", Action.PERSIST_WRITE)
    sequence.add_steps([task1, task2])
    return sequence

@pytest.fixture
def iterator_with_iterations(sequence_with_tasks):
    template = PipelineSequenceTemplate([
        PipelineTask("template_task1", Action.READ),
        PipelineTask("template_task2", Action.PERSIST_WRITE)
    ])
    iterator = PipelineDynamicIterator("test_iterator", template)
    iterator.set_iterations_from_refs([1, 2])
    return iterator

class TestFunctionResultReporting:
    def test_status_report_content(self, function_result):
        report = function_result.get_final_report()
        assert isinstance(report, str)
        assert "Test issue" in report
        assert "Test warning" in report
        assert "Test notice" in report
        assert "test_key" in report
        assert "test_value" in report

    def test_final_report_after_completion(self, function_result):
        function_result.final(force_status=ProgressStatus.DONE)
        report_dict = function_result.to_dict()
        assert report_dict["status"]["progress_status"] == "DONE"
        assert "duration_s" in report_dict["status"]
        assert isinstance(report_dict["status"]["duration_s"], float)

class TestPipelineTaskReporting:
    def test_final_report_generation(self, task_with_status_tracking):
        task_with_status_tracking.validate_and_start()
        task_with_status_tracking.progress_status = ProgressStatus.DONE
        task_with_status_tracking.final()
        
        report = task_with_status_tracking.final_report
        assert isinstance(report, str)
        assert "Final Report for Task test_task" in report
        assert "Task issue" in report
        assert "Task warning" in report
        assert "Task notice" in report
        assert "Duration:" in report

    def test_task_str_representation(self, task_with_status_tracking):
        task_with_status_tracking.progress_status = ProgressStatus.DONE
        task_str = str(task_with_status_tracking)
        assert "✔" in task_str  # Success symbol
        assert "DONE" in task_str
        assert "read" in task_str
        assert "file" in task_str

class TestPipelineSequenceReporting:
    def test_sequence_status_reporting(self, sequence_with_tasks):
        # Set task statuses
        for task in sequence_with_tasks.steps.values():
            task.progress_status = ProgressStatus.DONE
        
        sequence_with_tasks.update_status_counts_and_progress_status(fail_or_unfinish_if_any_pending=True)
        sequence_with_tasks.final()
        
        report = sequence_with_tasks.final_report
        assert isinstance(report, str)
        assert "Final Report for Sequence sequence_seq1" in report
        assert "Status: DONE" in report
        assert "Total Steps: 2" in report
        assert sequence_with_tasks.status_counts.total_count == 2

    def test_sequence_str_representation(self, sequence_with_tasks):
        sequence_str = str(sequence_with_tasks)
        assert "[Sequence seq1" in sequence_str
        assert "Status:" in sequence_str
        for task in sequence_with_tasks.steps.values():
            assert task.name in sequence_str

class TestPipelineDynamicIteratorReporting:
    def test_iterator_final_reporting(self, iterator_with_iterations):
        # Set statuses for iterations
        for iteration in iterator_with_iterations.iterations.values():
            for task in iteration.steps.values():
                task.progress_status = ProgressStatus.DONE
            iteration.update_status_counts_and_progress_status(fail_or_unfinish_if_any_pending=True)
            iteration.final()
        
        iterator_with_iterations.evaluate_progress_status(fail_or_unfinish_if_any_pending=True)
        iterator_with_iterations.final()
        
        report = iterator_with_iterations.final_report
        assert isinstance(report, str)
        assert "Final Report for Iterator test_iterator" in report
        assert "Total Iterations: 2" in report
        assert "Step Status Summary Across All Iterations:" in report

    def test_iterator_step_status_counts(self, iterator_with_iterations):
        # Set some statuses
        for iteration in iterator_with_iterations.iterations.values():
            for task in iteration.steps.values():
                task.progress_status = ProgressStatus.DONE
                task.final()
            iteration.final()
        iterator_with_iterations.final()
        print("FINAL REPORT", iterator_with_iterations.final_report)
        counts = iterator_with_iterations.get_status_counts_across_iterations_for_step("template_task1")
        assert isinstance(counts, StatusCounts)
        assert ProgressStatus.DONE in counts.by_status_count
        assert counts.by_status_count[ProgressStatus.DONE] == 2  # Both iterations

class TestPipelineFlowReporting:
    def test_pipeline_completion_reporting(self, sequence_with_tasks):
        flow = PipelineFlow("test_pipeline")
        flow.add_step(sequence_with_tasks)

        # Set all tasks to done
        for task in sequence_with_tasks.steps.values():
            task.progress_status = ProgressStatus.DONE
            
        flow.final()
        report = flow.final_report
        assert isinstance(report, str)
        assert "Pipelineflow Context: test_pipeline" in report
        assert "Progress:" in report
        assert "2/2 tasks closed" in report
        assert flow.completion_percentage ==100

    def test_pipeline_flow_description(self, sequence_with_tasks):
        flow = PipelineFlow("test_pipeline")
        flow.add_step(sequence_with_tasks)
        
        description = flow.get_pipeline_description()
        assert isinstance(description, str)
        assert "Pipelineflow Context: test_pipeline" in description
        assert "Steps:" in description
        assert "Progress:" in description
        for task in sequence_with_tasks.steps.values():
            assert task.name in description

def test_status_integration_issues_allowed(task_with_status_tracking, function_result):
    """Test status integration between FunctionResult and PipelineTask"""
    
    # Setup statuses
    function_result.add_issue("Integration issue")
    function_result.progress_status = ProgressStatus.FINISHED_WITH_ISSUES
    
    # Incorporate function result into task
    task_with_status_tracking.incorporate_function_result(function_result, issues_allowed=True)
    
    # Verify status propagation
    task_with_status_tracking.final(issues_allowed=True)
    assert task_with_status_tracking.progress_status == ProgressStatus.FINISHED_WITH_ISSUES
    assert "Integration issue" in task_with_status_tracking.issues
    assert task_with_status_tracking.final_report and "Integration issue" in task_with_status_tracking.final_report



def test_status_integration_issues_not_allowed(task_with_status_tracking, function_result):
    """Test status integration between FunctionResult and PipelineTask"""
    
    # Setup statuses
    function_result.add_issue("Integration issue")
    function_result.progress_status = ProgressStatus.FINISHED_WITH_ISSUES
    
    # Incorporate function result into task
    task_with_status_tracking.incorporate_function_result(function_result, issues_allowed=True)
    
    # Verify status propagation
    task_with_status_tracking.final()
    assert task_with_status_tracking.progress_status == ProgressStatus.FAILED
    assert "Integration issue" in task_with_status_tracking.issues
    assert task_with_status_tracking.final_report and "Integration issue" in task_with_status_tracking.final_report
