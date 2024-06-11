from django import forms
from .models import Barrio, Suscriptor, Micromedidor, SuscriptorMicromedidor, Lectura
#####################################################3
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class BarrioForm(forms.ModelForm):
    class Meta:
        model = Barrio
        fields = ['barrio', 'zona']

    def __init__(self, *args, **kwargs):
        super(BarrioForm, self).__init__(*args, **kwargs)

        # Opciones para el campo 'zona'
        self.fields['zona'].widget.choices = Barrio.OPCIONES_zona 




class SuscriptorForm(forms.ModelForm):
    class Meta:
        model = Suscriptor
        fields = ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'barrio', 'direccion_IMAGEN', 'Estrato_socioeconomico', 'Uso']

    def __init__(self, *args, **kwargs):
        super(SuscriptorForm, self).__init__(*args, **kwargs)
        self.fields['Estrato_socioeconomico'].widget.choices = Suscriptor.OPCIONES_Estrato_social
        self.fields['Uso'].widget.choices = Suscriptor.OPCIONES_Uso

        # Filtrar los barrios disponibles para seleccionar en el formulario
        self.fields['barrio'].queryset = Barrio.objects.all()  # Puedes ajustar este queryset según tu lógica de negocio


class MicromedidorForm(forms.ModelForm):
    class Meta:
        model = Micromedidor
        fields = ['nuid', 'medidor', 'fecha_instalacion'] 

    def clean_nuid(self):
        # Obtener el valor ingresado en el campo nuid
        nuid = self.cleaned_data.get('nuid')
        
        # Verificar si ya existe un Micromedidor con este nuid en la base de datos
        if Micromedidor.objects.filter(nuid=nuid).exists():
            # Obtener la instancia actual del micromedidor (si existe)
            instance = getattr(self, 'instance', None)
            if instance and instance.id:
                # Si la instancia existe y tiene un ID, significa que se está editando
                # En ese caso, excluimos este micromedidor de la verificación de duplicados
                if Micromedidor.objects.exclude(id=instance.id).filter(nuid=nuid).exists():
                    raise forms.ValidationError("El NUID ingresado ya está en uso. Por favor, ingrese un valor único.")
            else:
                raise forms.ValidationError("El NUID ingresado ya está en uso. Por favor, ingrese un valor único.")
        
        return nuid 


class SuscriptorMicromedidorForm(forms.ModelForm):
    class Meta:
        model = SuscriptorMicromedidor
        fields = ['suscriptor', 'micromedidor'] 
    def __init__(self, *args, **kwargs):
        super(SuscriptorMicromedidorForm, self).__init__(*args, **kwargs)
        self.fields['suscriptor'].queryset = Suscriptor.objects.all()
        self.fields['micromedidor'].queryset = Micromedidor.objects.all() 


class LecturaForm(forms.ModelForm):
    class Meta:
        model = Lectura
        fields = ['suscriptor_micromedidor', 'lectura_actual','mes_actual','mes_anterior', 'Observaciones', 'tipo_lectura', 'estado_micromedidor'] 

    def __init__(self, *args, **kwargs):
        super(LecturaForm, self).__init__(*args, **kwargs)
        self.fields['tipo_lectura'].widget.choices = Lectura.OPCIONES_Tipo_lectura
        self.fields['estado_micromedidor'].widget.choices = Lectura.OPCIONES_estado_micromedidor
        self.fields['suscriptor_micromedidor'].queryset = SuscriptorMicromedidor.objects.all() 

    def clean_lectura_actual(self):
        lectura_actual = self.cleaned_data['lectura_actual']
        return lectura_actual 
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

