# shopcloud-django-toolbox

## install

```sh
$ pip install shopcloud-django-toolbox
```

## Models

Add the GID as identifier to all django models

```python3
from shopcloud_django_toolbox import GID

class FooBarModel(models.Model, GID):
    pass
```

## URL-Signing

generate or load signed base64  encoded dict containing versioned with expiration date for access-control

### Usage

`settings.py`
```python3
DJ_TOOLBOX_SIGNER = {
    'VERSION': "1",
}
```

__dump values dict:__
```python3
from shopcloud django.toolbox import signer

signing_key = signer.dumps({"foo":"bar"}, expire_in_hours:12)

```

__load values dict:__

```python3
from shopcloud django.toolbox import signer
from django.http import HttpResponseForbidden

def some_view(request):
    sign_str = request.GET.get("sign")
    is_valid, data = signer.loads(sign_str)
    if not is_valid(request):
        return HttpResponseForbidden("Not allowed")
    data.get("xxx")
    #
    ## … some view logic
    #
```

__alternative for a django Request:__

```python3
from shopcloud django.toolbox import signer
from django.http import HttpResponseForbidden

def some_view(request):
    sign_str = request.GET.get("sign")
    is_valid, data = signer.loads_from_request(sign_str)
    if not is_valid(request):
            return HttpResponseForbidden("Not allowed")
    data.get("xxx")
    #
    ## … some view logic
    #
```

__Django View Decorator__

check if GET-parameter `sign` is set and has required keys in data objects

```
from shopcloud_django_toolbox import signer
from shopcloud_django_toolbox.decorators import


@require_toolbox_sign(needed_keys=['key_that_must_exist', 'foo', 'bar'])
def some_view(request):
    is_valid, data = signer.loads_from_request(request)
    #
    ## … some view logic
    #
```


## Testing

### API standart tests

Standart template for the `tests.py` file in all modules with admin and REST API`s

```python3
from shopcloud_django_toolbox import TestAdminTestCase
from shopcloud_django_toolbox.tests import BaseTestApiAuthorization
from shopcloud_django_toolbox import SetupClass
from shopcloud_django_toolbox.tests import Representation
__


class TestRepresentation(utils.Representation):
    def test_representation(self):
        from . import seeds
        self._test_representations_from_seeds(seeds)


class TestAdminPages(TestAdminTestCase):
    MODULE = 'url-name'

    def test_admin_easylineitem(self):
        self.run_for_model(
            'url-model-name',
            is_check_add=False,  # deactivate when add function is deactivated
            is_check_template=False,  # deactivate generic template check
            is_check_search=True,  # activate searchbar check
            is_check_detail=False, # erzeugt ein Model-Object und ruft den Detail-View auf,
            creation_parameters={}, # notwendig für den detailcheck da ein generisches erzeugen von spezeillen Models nicht mgl
        )


class TestApiAuthorization(BaseTestApiAuthorization):
    app_name = "url-module-name"

    def test_model_foo(self):
        self.run_test_endpoint("url-model-name")

    def test_model_bar(self):
        self.run_test_endpoint("url-model-name")


class YoutAPITest(SetupClass):
    def test_api_endpint(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

        r = client.get('/module/api/endpoint')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)


```

## Event

To fire events and run tasks in prarallel, need [PROJECT] to receive and run the output from log and call the API.

```python3
from shopcloud_django_toolbox import Event


class FooBarModel(models.Model):
    ...

    def do_event(self):
        event = Event(
            name="de.talk-point.platform/module/model/sync",
            model=self,
        )
        event.add_task(
            queue="default",
            url=f"moduke/api/model/{self.id}/action/",
            json={}
        )
        event.fire()
```

#### File Hash Generating

generate sha-384 file hash for sri with given filepath

```python3
from shopcloud-django-toolbox import hash_for_file


hash_for_file("./some-file.txt")
```

## deploy

```sh
# change version Number in setup.py ändern und dann erst releasen
# delete build and dist-directory
$ rm -rf build dist
$ pip3 install wheel twine
$ python3 setup.py sdist bdist_wheel
$ twine upload dist/*
  - username __token__
```
