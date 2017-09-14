# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from webService.models import Usuario


class UsuarioForm(ModelForm):
    def clean(self):
        cleaned_data = super(UsuarioForm, self).clean()
        if self.instance.pk is None:
            uid = self.instance.get_UID_from_servidor()
            cleaned_data['uid'] = uid
        else:
            instance_old = Usuario.objects.get(pk=self.instance.pk)
            if cleaned_data['uid'] != instance_old.uid:
                raise ValidationError("No puede cambiarse en el formulario el uid, debe ser automático")

        return cleaned_data