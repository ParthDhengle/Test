from unittest.mock import MagicMock

from src2.task.service import create_task, get_tasks
from src2.task.model import TaskModel
from src2.task.schema import TaskSchema
from src2.user.models import UserModel


def test_create_task():
    # Arrange
    db = MagicMock()

    user = UserModel(
        id=1,
        username="parth"
    )

    data = TaskSchema(
        title="Learn pytest",
        desc="Write unit tests",
        priority=1,
        is_completed=False
    )

    # Act
    result = create_task(data, db, user)

    # Assert
    assert result.title == "Learn pytest"
    assert result.desc == "Write unit tests"
    assert result.priority == 1
    assert result.is_completed is False
    assert result.user_id == 1

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(result)


def test_get_tasks():
    # Arrange
    db = MagicMock()

    user = UserModel(
        id=1,
        username="parth"
    )

    tasks = [
        TaskModel(
            id=1,
            title="Task 1",
            desc="Description 1",
            priority=1,
            is_completed=False,
            user_id=1
        ),
        TaskModel(
            id=2,
            title="Task 2",
            desc="Description 2",
            priority=2,
            is_completed=True,
            user_id=1
        )
    ]

    db.query.return_value.filter.return_value.all.return_value = tasks

    # Act
    result = get_tasks(db, user)

    # Assert
    assert len(result) == 2
    assert result[0].title == "Task 1"
    assert result[1].title == "Task 2"

    db.query.assert_called_once_with(TaskModel)