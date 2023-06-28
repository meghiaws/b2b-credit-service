import factory

from app.core.tests.utils import faker

from django.contrib.auth import get_user_model

from app.credits.models import Customer, Organization, TransferTransaction


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    password = factory.LazyAttribute(lambda _: "1342917****")
    email = factory.LazyAttribute(lambda _: faker.unique.email())


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    user = factory.SubFactory(UserFactory)
    phone = factory.LazyAttribute(
        lambda _: faker.pystr_format(string_format="0914###{{random_int}}")
    )


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    user = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda _: faker.user_name())
