import pytest
from ipulse_shared_base_ftredge import ProgressStatus, Action, DataResource, FileExtension

from ipulse_shared_data_eng_ftredge.pipelines.dependency import Dependency
from ipulse_shared_data_eng_ftredge.pipelines.pipelineflow import (
  Step, PipelineTask, PipelineSequence,
    PipelineDynamicIterator, PipelineFlow, PipelineSequenceTemplate
)

# -------------------- Fixtures --------------------
@pytest.fixture
def simple_task():
    return PipelineTask("test_task", Action.READ, DataResource.FILE)

@pytest.fixture
def simple_sequence():
    return PipelineSequence("seq1", steps=[
        PipelineTask("task1", Action.READ, DataResource.FILE),
        PipelineTask("task2", Action.PERSIST_WRITE, DataResource.FILE)
    ])

@pytest.fixture
def template_with_tasks():
    tasks = [
        PipelineTask("template_task1", Action.READ, DataResource.FILE),
        PipelineTask("template_task2", Action.PERSIST_WRITE, DataResource.FILE)
    ]
    return PipelineSequenceTemplate(tasks)


# -------------------- Step Tests --------------------
class TestStep:
    def test_init(self):
        step = Step("test_step")
        assert step.name == "test_step"
        assert not step.disabled
        assert step.progress_status == ProgressStatus.NOT_STARTED
        assert step.dependencies == []

    def test_validate_and_start(self):
        step = Step("test_step")
        success = step.validate_and_start()
        assert success
        assert step.progress_status == ProgressStatus.IN_PROGRESS
        assert step.validation_error is None

    def test_disabled_step(self):
        step = Step("test_step", disabled=True)
        success = step.validate_and_start()
        assert not success
        assert step.progress_status == ProgressStatus.DISABLED
        assert step.validation_error is None

    def test_non_validated_step_without_pipelineflow(self):
        step = Step("test_step", disabled=False, dependencies=[Dependency("nonexistent_step")])
        success = step.validate_and_start()
        assert not success
        assert step.progress_status == ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY
        assert step.validation_error == "Pipeline flow not set for dependency resolution"

    def test_non_validated_step_dependencies(self):
        step = Step("test_step", disabled=False, dependencies=[Dependency("nonexistent_step")])
        step.set_pipeline_flow(PipelineFlow("test_pipeline"))
        success = step.validate_and_start()
        assert not success
        assert step.progress_status == ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY
        assert step.validation_error == "Unsatisfied dependencies: Missing dependency: nonexistent_step"

    def test_duration_tracking(self):
        step = Step("test_step")
        step.validate_and_start()
        assert step.duration_s > 0
        step.calculate_duration()
        assert isinstance(step.duration_s, float)

    def test_validate_dependencies_with_skipped_dependency(self):
        """Test that step gets marked as skipped if dependency is skipped"""
        pipeline = PipelineFlow("test_pipeline")
        dep_step = PipelineTask("dep_step")
        main_step = PipelineTask("main_step", dependencies=[Dependency("dep_step")])
        
        pipeline.add_step(dep_step)
        pipeline.add_step(main_step)
        
        # Set dependency step as skipped
        dep_step.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
        
        # Validate dependencies should return False and set main step as skipped
        assert not main_step.validate_dependencies()
        assert main_step.progress_status == ProgressStatus.INTENTIONALLY_SKIPPED
        assert "Dependencies skipped" in main_step.validation_error

    def test_validate_and_start_with_skipped_dependency(self):
        """Test validate_and_start behavior with skipped dependency"""
        pipeline = PipelineFlow("test_pipeline")
        dep_step = PipelineTask("dep_step")
        main_step = PipelineTask("main_step", dependencies=[Dependency("dep_step")])
        
        pipeline.add_step(dep_step)
        pipeline.add_step(main_step)
        
        # Set dependency step as skipped
        dep_step.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
        
        # validate_and_start should return False and set status to INTENTIONALLY_SKIPPED
        assert not main_step.validate_and_start()
        assert main_step.progress_status == ProgressStatus.INTENTIONALLY_SKIPPED
        assert "Dependencies skipped" in main_step.validation_error

    def test_validate_dependencies_with_multiple_dependencies(self):
        """Test dependency validation with mix of normal and skipped dependencies"""
        pipeline = PipelineFlow("test_pipeline")
        
        # Set up steps
        dep1 = PipelineTask("dep1")
        dep2 = PipelineTask("dep2")
        dep3 = PipelineTask("dep3")
        main_step = PipelineTask("main_step", dependencies=[
            Dependency("dep1"),
            Dependency("dep2"),
            Dependency("dep3")
        ])
        
        pipeline.add_step(dep1)
        pipeline.add_step(dep2)
        pipeline.add_step(dep3)
        pipeline.add_step(main_step)
        
        # Set different statuses
        dep1.progress_status = ProgressStatus.DONE
        dep2.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
        dep3.progress_status = ProgressStatus.IN_PROGRESS
        
        # Should be marked as skipped due to dep2
        assert not main_step.validate_dependencies()
        assert main_step.progress_status == ProgressStatus.INTENTIONALLY_SKIPPED

    def test_validate_dependencies_with_optional_skipped(self):
        """Test that optional skipped dependencies don't cause step to be skipped"""
        pipeline = PipelineFlow("test_pipeline")
        
        dep1 = PipelineTask("dep1")
        dep2 = PipelineTask("dep2")
        main_step = PipelineTask("main_step", dependencies=[
            Dependency("dep1"),
            Dependency("dep2", optional=True)
        ])
        
        pipeline.add_step(dep1)
        pipeline.add_step(dep2)
        pipeline.add_step(main_step)
        
        # Set statuses
        dep1.progress_status = ProgressStatus.DONE
        dep2.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
        
        # Should pass validation since dep2 is optional
        assert main_step.validate_dependencies()
        assert main_step.progress_status != ProgressStatus.INTENTIONALLY_SKIPPED

    def test_validate_and_start_state_transitions(self):
        """Test various state transitions in validate_and_start"""
        step = Step("test_step")
        
        # Test disabled state
        step.disabled = True
        assert not step.validate_and_start()
        assert step.progress_status == ProgressStatus.DISABLED
        
        # Test already closed state
        step.disabled = False
        step.progress_status = ProgressStatus.DONE
        assert not step.validate_and_start()
        assert "already completed" in step.validation_error
        
        # Test already skipped state
        step.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
        assert not step.validate_and_start()
        assert "Intentionally Skipped" in step.validation_error
        
        # Test successful start
        step.progress_status = ProgressStatus.NOT_STARTED
        assert step.validate_and_start()
        assert step.progress_status == ProgressStatus.IN_PROGRESS
        assert step._start_time is not None

# -------------------- PipelineTask Tests --------------------
class TestPipelineTask:
    def test_init(self):
        task = PipelineTask("task1", Action.READ, DataResource.FILE)
        assert task.name == "task1"
        assert task.action == Action.READ
        assert task.source == DataResource.FILE
        assert task.nb_tasks() == 1

    def test_incorporate_function_result(self):
        from ipulse_shared_data_eng_ftredge.pipelines.function_result import FunctionResult
        task = PipelineTask("task1")
        result = FunctionResult()
        result.progress_status = ProgressStatus.DONE
        task.incorporate_function_result(result)
        task.final()
        assert task.progress_status == ProgressStatus.DONE

# -------------------- PipelineSequence Tests --------------------
class TestPipelineSequence:
    def test_init(self):
        sequence = PipelineSequence("seq1")
        assert sequence.sequence_ref == "seq1"
        assert sequence.steps == {}

    def test_add_step(self, simple_task):
        sequence = PipelineSequence("seq1")
        sequence.add_step(simple_task)
        assert "test_task" in sequence.steps
        assert sequence.nb_tasks() == 1

    def test_collect_status_counts(self, simple_sequence):
        counts = simple_sequence.collect_status_counts()
        assert counts.total_count == 2
        assert counts.get_category_count('pending_statuses') == 2

    def test_update_status_counts_and_progress_status(self, simple_sequence):
        for step in simple_sequence.steps.values():
            step.progress_status = ProgressStatus.DONE
        simple_sequence.update_status_counts_and_progress_status(fail_or_unfinish_if_any_pending=True)
        assert simple_sequence.progress_status == ProgressStatus.DONE

# -------------------- PipelineDynamicIterator Tests --------------------
class TestPipelineDynamicIterator:
    def test_init(self, template_with_tasks):
        iterator = PipelineDynamicIterator("iterator1", template_with_tasks)
        assert iterator.name == "iterator1"
        assert iterator.total_iterations == 0
        assert iterator.max_iterations_allowed == 100

    def test_set_iterations_from_refs(self, template_with_tasks):
        iterator = PipelineDynamicIterator("iterator1", template_with_tasks)
        iterator.set_iterations_from_refs([1, 2, 3])
        assert iterator.total_iterations == 3
        assert all(ref in iterator.iterations for ref in [1, 2, 3])

    def test_max_iterations_limit(self, template_with_tasks):
        iterator = PipelineDynamicIterator("iterator1", template_with_tasks, max_iterations_allowed=2)
        with pytest.raises(ValueError):
            iterator.set_iterations_from_refs([1, 2, 3])

    def test_can_continue(self, template_with_tasks):
        iterator = PipelineDynamicIterator("iterator1", template_with_tasks)
        iterator.set_iterations_from_refs([1])
        can_continue = iterator.can_continue()
        assert can_continue
        
        # Test max issues
        iterator.status_counts.add_status(ProgressStatus.FAILED)
        iterator.status_counts.add_status(ProgressStatus.FAILED)
        iterator.status_counts.add_status(ProgressStatus.FAILED)
        iterator.status_counts.add_status(ProgressStatus.FAILED)
        can_continue = iterator.can_continue()
        assert not can_continue
        assert "Max issues exceeded" in iterator.failure_reason

# -------------------- PipelineFlow Tests --------------------
class TestPipelineFlow:
    def test_init(self):
        flow = PipelineFlow("test_pipeline")
        assert flow.base_context == "test_pipeline"
        assert flow.completion_percentage == 0.0

    def test_add_step(self, simple_task):
        flow = PipelineFlow("test_pipeline")
        assert flow.add_step(simple_task)
        assert simple_task.name in flow.steps
        assert flow._total_tasks == 1

    def test_update_task_completion(self):
        flow = PipelineFlow("test_pipeline")
        flow._total_tasks = 10
        flow.update_task_completion(3)
        assert flow._closed_tasks == 3
        assert flow.completion_percentage == 30.0

    def test_get_step(self, simple_task):
        flow = PipelineFlow("test_pipeline")
        flow.add_step(simple_task)
        assert flow.get_step(simple_task.name) == simple_task
        with pytest.raises(KeyError):
            flow.get_step("nonexistent_step")

    def test_validate_steps_dependencies_exist(self):
        flow = PipelineFlow("test_pipeline")
        task1 = PipelineTask("task1")
        task2 = PipelineTask("task2", dependencies=[Dependency("task1")])
        flow.add_step(task1)
        flow.add_step(task2)
        assert flow.validate_steps_dependencies_exist()

        # Test missing dependency
        flow = PipelineFlow("test_pipeline")
        task_with_missing_dep = PipelineTask("task1", dependencies=[Dependency("nonexistent")])
        flow.add_step(task_with_missing_dep)
        with pytest.raises(ValueError):
            flow.validate_steps_dependencies_exist()

    def test_final_report_generation(self, simple_sequence):
        flow = PipelineFlow("test_pipeline")
        flow.add_step(simple_sequence)
        flow.validate_and_start()
        for step in simple_sequence.steps.values():
            step.progress_status = ProgressStatus.DONE
        simple_sequence.final()
        flow.final()
        report = flow.final_report
        assert isinstance(report, str)
        assert "Pipelineflow Context: test_pipeline" in report
        assert "Status: DONE" in report

    def test_completion_tracking(self, simple_task):
        """Test that completion percentage updates correctly as tasks complete"""
        flow = PipelineFlow("test_pipeline")
        flow.add_step(simple_task)
        
        # Initially 0%
        assert flow.completion_percentage == 0.0
        assert flow._closed_tasks == 0
        
        # Update task status to DONE
        simple_task.progress_status = ProgressStatus.DONE
        flow.update_status_counts_and_progress_status(fail_or_unfinish_if_any_pending=True)
        
        # Should now be 100% as the only task is complete
        print("FLOW STATUSSSS", flow.final_report)
        assert flow._closed_tasks == 1
        assert flow.completion_percentage == 100.0

    def test_completion_tracking_multiple_tasks(self, simple_sequence):
        """Test completion tracking with multiple tasks"""
        flow = PipelineFlow("test_pipeline")
        flow.add_step(simple_sequence)  # Contains 2 tasks
        
        # Initially 0%
        assert flow.completion_percentage == 0.0
        assert flow._closed_tasks == 0
        
        # Complete first task
        tasks = list(simple_sequence.steps.values())
        tasks[0].progress_status = ProgressStatus.DONE
        flow.update_status_counts_and_progress_status(fail_or_unfinish_if_any_pending=False)
        
        # Should be 50% complete
        assert flow._closed_tasks == 1
        assert flow.completion_percentage == 50.0
        
        # Complete second task
        tasks[1].progress_status = ProgressStatus.DONE
        flow.update_status_counts_and_progress_status(fail_or_unfinish_if_any_pending=False)
        
        # Should now be 100%
        assert flow._closed_tasks == 2
        assert flow.completion_percentage == 100.0

    def test_completion_with_skipped_tasks(self, simple_sequence):
        """Test completion tracking handles skipped tasks correctly"""
        flow = PipelineFlow("test_pipeline")
        flow.add_step(simple_sequence)
        
        # Skip one task, complete another
        tasks = list(simple_sequence.steps.values())
        tasks[0].progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
        tasks[1].progress_status = ProgressStatus.DONE
        flow.update_status_counts_and_progress_status(fail_or_unfinish_if_any_pending=False)
        
        # Both skipped and completed tasks count toward completion
        assert flow._closed_tasks == 2
        assert flow.completion_percentage == 100.0

    def test_chain_of_skipped_dependencies(self):
        """Test chain reaction of skipped dependencies in a sequence of steps"""
        flow = PipelineFlow("test_pipeline")
        
        # Create a chain of dependent tasks
        task1 = PipelineTask("task1")
        task2 = PipelineTask("task2", dependencies=[Dependency("task1")])
        task3 = PipelineTask("task3", dependencies=[Dependency("task2")])
        task4 = PipelineTask("task4", dependencies=[Dependency("task3")])
        
        # Add all tasks to flow
        flow.add_step(task1)
        flow.add_step(task2)
        flow.add_step(task3)
        flow.add_step(task4)
        
        # Start pipeline
        assert flow.validate_and_start()
        
        # Set task1 to DONE
        task1.progress_status = ProgressStatus.DONE
        task1.final()

        # Validate and set task2 to INTENTIONALLY_SKIPPED
        assert task2.validate_and_start()  # Should validate since task1 is DONE
        task2.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
        # Task3 should automatically become INTENTIONALLY_SKIPPED due to task2
        assert not task3.validate_and_start()
        assert task3.progress_status == ProgressStatus.INTENTIONALLY_SKIPPED
        assert "Dependencies skipped" in task3.validation_error
        
        # Task4 should also automatically become INTENTIONALLY_SKIPPED due to task3
        assert not task4.validate_and_start()
        assert task4.progress_status == ProgressStatus.INTENTIONALLY_SKIPPED
        assert "Dependencies skipped" in task4.validation_error
        
        # Update pipeline status
        # flow.update_status_counts_and_progress_status() #done as part of final()
        flow.final()
        
        # Check final statuses
        assert task1.progress_status == ProgressStatus.DONE
        assert task2.progress_status == ProgressStatus.INTENTIONALLY_SKIPPED
        assert task3.progress_status == ProgressStatus.INTENTIONALLY_SKIPPED
        assert task4.progress_status == ProgressStatus.INTENTIONALLY_SKIPPED
        
        # Pipeline overall status should be DONE or DONE_WITH_NOTICES since skipped tasks are expected
        assert flow.progress_status in [ProgressStatus.DONE]
        
        # Verify the counts in status_counts
        assert flow.status_counts.count_statuses(ProgressStatus.DONE) == 1
        assert flow.status_counts.count_statuses(ProgressStatus.INTENTIONALLY_SKIPPED) == 3
