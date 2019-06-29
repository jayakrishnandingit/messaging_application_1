import factory


class User(object):
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_OTHER = 'o'

    def __init__(self, name, email, gender, job):
        self.name = name
        self.email = email
        self.gender = gender
        self.job = job

    def __str__(self):
        return '%s' % self.name


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker('name', locale='en_GB')
    email = factory.Sequence(lambda n: 'jayakrishnandamodaran+%d@gmail.com' % n)
    gender = factory.Iterator([User.GENDER_MALE, User.GENDER_FEMALE, User.GENDER_OTHER])
    job = factory.Faker('job', locale='en_GB')


def generate_users(size=10):
    return UserFactory.create_batch(size=size)
