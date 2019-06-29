import factory

from messaging_application_1.users import generate_users


class Task(object):
    NEW = 'new'
    IN_PROGRESS = 'in progress'
    DONE = 'done'

    def __init__(self, task_id, title, description, users=None, status='new'):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status
        if users is None:
            users = []
        self.users = users
        

class TaskFactory(factory.Factory):
    class Meta:
        model = Task

    task_id = factory.Sequence(lambda n: n)
    title = factory.Faker('title')
    description = factory.Faker('text')
    status = factory.Iterator([Task.NEW, Task.IN_PROGRESS, Task.DONE])
    users = generate_users()


def generate_task(task_id):
    return TaskFactory(task_id=task_id)
