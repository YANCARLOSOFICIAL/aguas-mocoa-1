from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver 

class Barrio(models.Model):
    barrio = models.CharField(max_length=20, verbose_name='Nombre del Barrio')
     # Opciones para el campo 'zona'
    OPCIONES_zona= [
        ('zona1', 'Norte'),
        ('zona2', 'Sur occidente'),
        ('zona3', 'En expansion'), 
        
        # Añade más opciones según sea necesario 
    ]

    zona = models.CharField(
        max_length=50,
        choices=OPCIONES_zona,
        verbose_name='zona  ', 
        null=True
    )

    class Meta:
        verbose_name = 'Barrio'
        verbose_name_plural = 'Barrios'

 #eliminar modelo usuario, utilzar clase users de django 

   

class Suscriptor(models.Model):
    primer_nombre = models.CharField(max_length=50, verbose_name='Primer Nombre')
    segundo_nombre = models.CharField(max_length=59, verbose_name='Segundo Nombre')
    primer_apellido = models.CharField(max_length=50, verbose_name='Primer Apellido')
    segundo_apellido = models.CharField(max_length=50, verbose_name='Segundo Apellido')
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE, verbose_name='Barrio')
    direccion_IMAGEN = models.ImageField(upload_to='imagenes/', verbose_name='Dirección Imagen')
      # Opciones para el campo 'estrato_socioeconomico'
    OPCIONES_Estrato_social= [
        ('Estrato1', 'Bajo Bajo'),
        ('Estrato2', 'Bajo'),
        ('Estrato3', 'Medio Bajo'), 
        ('Estrato4', 'Medio '), 
        
        # Añade más opciones según sea necesario 
    ]

    Estrato_socioeconomico = models.CharField(
        max_length=50,
        choices=OPCIONES_Estrato_social,
        verbose_name='estrato socioeconimico  ', 
        null=True
    )
     # Opciones para el campo 'uso'
    OPCIONES_Uso= [
        ('Uso1', 'Comercial'),
        ('Uso2', 'Residencial'),
        ('Uso3', 'Oficial'), 
        
        
        # Añade más opciones según sea necesario 
    ]

    Uso = models.CharField(
        max_length=50,
        choices=OPCIONES_Uso,
        verbose_name='Uso  ', 
        null=True
    )

    class Meta:
        verbose_name = 'Suscriptor'
        verbose_name_plural = 'Suscriptores'

class Micromedidor(models.Model):
    nuid = models.CharField(max_length=20, verbose_name='NUID',unique=True) #dejar como unico 
    medidor = models.CharField(max_length=20, verbose_name='Medidor')
    fecha_instalacion = models.DateField(verbose_name='Fecha de Instalación') 
   


    class Meta:
        verbose_name = 'Micromedidor'
        verbose_name_plural = 'Micromedidores'

  

class SuscriptorMicromedidor(models.Model):
    suscriptor = models.ForeignKey(Suscriptor, on_delete=models.CASCADE, verbose_name='Suscriptor')
    micromedidor = models.ForeignKey(Micromedidor, on_delete=models.CASCADE, verbose_name='Micromedidor')

    class Meta:
        verbose_name = 'Relación Suscriptor-Micromedidor'
        verbose_name_plural = 'Relaciones Suscriptor-Micromedidor'



    
class Lectura(models.Model):
    suscriptor_micromedidor = models.ForeignKey(SuscriptorMicromedidor, on_delete=models.CASCADE, verbose_name='Relación Suscriptor-Micromedidor')
    mes_anterior = models.CharField(verbose_name='Mes anterior', max_length=50, blank=True, null=True)
    mes_actual = models.CharField(verbose_name='Mes actual', max_length=50, blank=True, null=True)
    lectura_anterior = models.IntegerField(verbose_name='Lectura anterior', default=0) 
    lectura_actual = models.IntegerField(verbose_name='Lectura actual', default=0) 
    FechaLectura = models.DateTimeField(verbose_name='Fecha de Lectura', auto_now_add=True, editable=False)
    Observaciones = models.CharField(max_length=100, verbose_name='Observaciones', blank=True, null=True)
    OPCIONES_Tipo_lectura = [
        ('tipo1', 'Lectura'),
        ('tipo2', 'Promedio'),
    ]

    tipo_lectura = models.CharField(
        max_length=50,
        choices=OPCIONES_Tipo_lectura,
        verbose_name='Tipo de lectura', 
        null=True
    )
    OPCIONES_estado_micromedidor = [
        ('estado1', 'Bueno'),
        ('estado2', 'Malo'),
    ]

    estado_micromedidor = models.CharField(
        max_length=50,
        choices=OPCIONES_estado_micromedidor,
        verbose_name='Estado del micromedidor',
        null=True
    )
    consumototal = models.IntegerField(verbose_name='Consumo total', default=0) 

    class Meta:
        verbose_name = 'Lectura'
        verbose_name_plural = 'Lecturas'

    def calcular_consumo_total(self):
        if self.lectura_anterior is not None and self.lectura_actual is not None:
            return self.lectura_actual - self.lectura_anterior
        return 0
    
def save(self, *args, **kwargs):
        self.consumototal = self.calcular_consumo_total()
        super(Lectura, self).save(*args, **kwargs)    

@receiver(post_save, sender=Lectura)
def actualizar_lectura_anterior(sender, instance, created, **kwargs):
    if created:
        # Obtener la última lectura anterior para el mismo suscriptor y micromedidor
        lectura_anterior = Lectura.objects.filter(
            suscriptor_micromedidor=instance.suscriptor_micromedidor
        ).exclude(id=instance.id).order_by('-FechaLectura').first()

        if lectura_anterior:
            instance.mes_anterior = lectura_anterior.mes_actual
            instance.lectura_anterior = lectura_anterior.lectura_actual
            instance.save() 

