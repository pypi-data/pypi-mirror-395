import random
import string
import uuid
from inspect import getmembers, isfunction

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase
from django.apps import apps
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def random_float(min_value: float = 1.0, max_value: float = 1000.0) -> float:
    return random.uniform(min_value, max_value)


def random_int(min_value: int = 1, max_value: int = 1000) -> int:
    return random.randint(min_value, max_value)


def random_str() -> str:
    return str(uuid.uuid4())


class SetupClass(TestCase):
    username = "admin"
    pwd = ':L:3M3pFK"N$Y!Qj'

    def create_superuser(self):
        u = User.objects.create_superuser(username=self.username, password=self.pwd)
        u.save()

    def setUp(self):
        self.create_superuser()


class TestAdminTestCase(SetupClass):
    MODULE = "test"

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.client.login(
            username=TestAdminTestCase.username, password=TestAdminTestCase.pwd
        )

    def run_for_model(self, model: str, **kwargs):
        if kwargs.get("is_check_add", True):
            response = self.client.get(
                reverse(f"admin:{self.MODULE}_{model}_add"), follow=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.template_name[0],
                f"admin/{self.MODULE}/{model}/change_form.html",
            )

        if kwargs.get("is_check_detail", True):
            if kwargs.get("creation_parameters"):
                model_class = apps.get_model(self.MODULE, model)
                test_instance = model_class.objects.create(
                    **kwargs.get("creation_parameters")
                )
                content_type = ContentType.objects.get_for_model(model_class)
                response = self.client.get(
                    reverse(
                        f"admin:{content_type.app_label}_{content_type.model}_change",
                        args=[test_instance.pk],
                    ),
                    follow=True,
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    response.template_name[0],
                    f"admin/{content_type.app_label}/{content_type.model}/change_form.html",
                )

        response = self.client.get(
            reverse(f"admin:{self.MODULE}_{model}_changelist"), follow=True
        )
        self.assertEqual(response.status_code, 200)
        if kwargs.get("is_check_template", True):
            self.assertEqual(
                response.template_name[0],
                f"admin/{self.MODULE}/{model}/change_list.html",
            )

        if kwargs.get("is_check_search", False):
            response = self.client.get(
                "{}?q={}".format(
                    reverse(f"admin:{self.MODULE}_{model}_changelist"), "test"
                ),
                follow=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.template_name[0],
                f"admin/{self.MODULE}/{model}/change_list.html",
            )


class BaseTestApiAuthorization(TestCase):
    app_name = "test"

    username = "test.user"
    password = "test@123456789"

    admin_username = "test.admin"
    admin_password = "admin@123456789"

    def setUp(self) -> None:
        super().setUp()
        user, created = User.objects.get_or_create(
            username=self.username, password=self.password
        )
        User.objects.create_superuser(
            username=self.admin_username,
            password=self.admin_password,
        )
        user.save()

    def _test_no_login(self, endpoint: str):
        client = APIClient()
        r = client.get(endpoint)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def _test_user_no_model_permission(self, endpoint: str):
        client = APIClient()
        client.login(username=self.username, password=self.password)
        r = client.get(endpoint)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def _test_superuser_access(self, endpoint: str):
        client = APIClient()
        client.login(username=self.admin_username, password=self.admin_password)
        r = client.get(endpoint)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def run_test_endpoint(self, model_name: str):
        endpoint = f"/{self.app_name}/api/{model_name}/"
        self._test_no_login(endpoint=endpoint)
        self._test_user_no_model_permission(endpoint=endpoint)
        self._test_superuser_access(endpoint=endpoint)


class Representation(TestCase):
    """Tests all classes with a generate function from seeds.py for their string representation"""

    def _test_representations_from_seeds(self, seeds):
        members = getmembers(seeds, isfunction)

        for _name, func in [x for x in members if "generate" in x[0]]:
            model = func()
            if model is not None:
                model.__repr__()
                model.__str__()
