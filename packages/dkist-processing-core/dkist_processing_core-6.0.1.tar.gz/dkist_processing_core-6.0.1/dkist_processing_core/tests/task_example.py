"""Example task subclass used in the tests."""

from dkist_processing_core import TaskBase


class Task(TaskBase):
    """Example task for testing."""

    log_url = "http://localhost:8080/log?execution_date=2021-01-07T18%3A19%3A38.214767%2B00%3A00&task_id=task_a&dag_id=test_dag"

    def __init__(self, *args, **kwargs):
        """Task base construction."""
        self.run_was_called = False
        self.pre_run_was_called = False
        self.post_run_was_called = False
        super().__init__(*args, **kwargs)

    def run(self):
        """Override base class run method."""
        self.run_was_called = True

    def pre_run(self) -> None:
        """Override base class pre-run method."""
        self.pre_run_was_called = True

    def post_run(self) -> None:
        """Override base class post-run method."""
        self.post_run_was_called = True


class Task2(Task):
    """Test task class."""

    pass


class Task3(Task):
    """Test task class."""

    pass


class Task4(Task):
    """Test task class."""

    pass
