from typing import Optional

from django.apps import apps
from django.conf import settings


class GID:
    """
    Microservice optimization for models to connect
    """

    @property
    def gid(self) -> Optional[str]:
        if self.pk is None:
            return None

        app_label = self._meta.app_label
        if getattr(self, "_gid_app_label", None) is not None:
            app_label = self._gid_app_label()
        model_name = self._meta.model_name
        if getattr(self, "_gid_model_name", None) is not None:
            model_name = self._gid_model_name()
        pk = self.pk

        return "gid://{app_name}/{app_label}/{model_name}/{pk}".format(
            app_name=settings.GID.get("APP_NAME"),
            app_label=app_label,
            model_name=model_name,
            pk=pk,
        )

    @classmethod
    def gid_to_query(cls, gid):
        if "gid://" not in gid:
            raise ValueError("for_gid has no gid://")
        pieces = gid.split("/")
        if len(pieces) != 6:
            raise ValueError("gid is not valid")
        app_label = pieces[3]
        model_name = pieces[4]
        pk = pieces[5]
        model = apps.get_model(app_label=app_label, model_name=model_name)
        return model.objects.filter(pk=pk)

    @classmethod
    def gid_type_query(cls, gid, pk):
        """
        Load gid-type query for example gid-type://shopcloud-backend/core/order/hash_id
        """
        if "gid-type://" not in gid:
            raise ValueError("for_gid has no gid-type://")
        pieces = gid.split("/")
        if len(pieces) != 6:
            raise ValueError("gid is not valid")
        app_label = pieces[3]
        model_name = pieces[4]
        pk_field = pieces[5]
        model = apps.get_model(app_label=app_label, model_name=model_name)
        return model.objects.filter(**{pk_field: pk})
