import pytest
from datetime import datetime
from ipulse_shared_base_ftredge import ProgressStatus, Action, DataResource, FileExtension
from ipulse_shared_data_eng_ftredge.pipelines.dependency import Dependency, DependencyType
from ipulse_shared_data_eng_ftredge.pipelines.pipelineflow import PipelineTask, PipelineSequence, PipelineSequenceTemplate

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



class TestDependency:
    def test_init(self):
        dep = Dependency("step1", DependencyType.TO_SUCCESS)
        assert dep.step_name == "step1"
        assert dep.requirement == DependencyType.TO_SUCCESS
        assert not dep.optional
        assert dep.timeout_s is None

    def test_start_timeout(self):
        dep = Dependency("step1", timeout_s=10)
        before = datetime.now()
        dep.start_timeout()
        assert isinstance(dep._start_time, datetime)
        assert before <= dep._start_time <= datetime.now()

    def test_is_timeout(self):
        dep = Dependency("step1", timeout_s=1)
        dep.start_timeout()
        assert not dep.is_timeout()
        # Wait for timeout
        import time
        time.sleep(1.1)
        assert dep.is_timeout()

    def test_check_satisfied(self, simple_task):
        dep = Dependency("step1", DependencyType.TO_SUCCESS)
        simple_task.progress_status = ProgressStatus.DONE
        assert dep.check_satisfied(simple_task)

        simple_task.progress_status = ProgressStatus.FAILED
        assert not dep.check_satisfied(simple_task)
