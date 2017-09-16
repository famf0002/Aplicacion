# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from webService.grabarRFID import grabarRFID
from webService.models import Usuario, Grabador


class UsuarioForm(ModelForm):
    def clean(self):
        cleaned_data = super(UsuarioForm, self).clean()
        #Si es nuevo usuario, se grabará la tarjeta
        puerto = Grabador.objects.get(id=cleaned_data.grabador_id).puerto
        if self.instance.pk is None:
            try:
                uid = grabarRFID().grabar(
                                    puerto= puerto,
                                    dni= cleaned_data.dni)
                cleaned_data['uid'] = uid
            except:
                raise ValidationError("Error al grabar la tarjeta")
        else:
            instance_old = Usuario.objects.get(pk=self.instance.pk)
            #Si se intenta modificar el UID manualmente
            if cleaned_data['uid'] != instance_old.uid:
                raise ValidationError("No puede modificar UID manualmente")
            else:
                #Si se modifica DNI se grabará de nuevo la tarjeta
                if cleaned_data['dni'] != instance_old.dni:
                    try:
                        uid = grabarRFID().grabar(
                                            puerto=puerto,
                                            dni=cleaned_data.dni)
                        cleaned_data['uid'] = uid
                    except:
                        raise ValidationError("Error al grabar la tarjeta")

        return cleaned_data