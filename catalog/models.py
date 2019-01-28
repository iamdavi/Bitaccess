from django.db import models
#Used to generate URLs by reversing the URL patterns
from django.urls import reverse
#Used to relate a User to Employer
from django.contrib.auth.models import User, Group

# Create your models here.

class Zona(models.Model):
    """
    Modelo que representa una Zona
    """
    num_aula=models.IntegerField(
        null=True,
        blank=True,
        help_text="Numero de aula (identificador)."
    )
    ip = models.CharField(
        primary_key=True,
        max_length=25,
        help_text="Ip del dispositivo asociado a esta aula"
    )
    modelo = models.CharField(
        max_length=25,
        help_text="Introduce el modelo del arduino (p. ej. Uno, Mega, etc.)"
    )
    tipo =models.CharField(
        max_length=25,
        blank = True,
        null=True,
        help_text = "Tipo de aula (p. ej. Clase, C.P.D...)"
    )
    descripcion = models.TextField(
        max_length = 1000,
        help_text="Introduce una descripción de la zona."
    )

    def __str__(self):
        """
        String que representa al objeto Zona
        """
        return "%s (%s)" % (self.ip, self.tipo)

    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Zona
        """
        return reverse('aula-detail', args=[str(self.id)])

    class Meta:
        ordering = ["num_aula","ip"]

class Puerto(models.Model):
    """
    Modelo que representa un puerto
    """
    ip=models.ForeignKey(
        Zona,
        on_delete = models.CASCADE,
        help_text="Ip de la zona"
    )
    num_puerto=models.IntegerField(
        help_text="Número de puerto del arduino"
    )
    descripcion=models.CharField(
        max_length= 35,
        help_text="Acción que realiza dicho puerto"
    )

    class Meta:
        ordering = ["ip", "num_puerto"]
        unique_together = (
            "ip", "num_puerto"
        )

    def __str__(self):
        """
        Método que identifica a un puerto en concreto
        """
        return "%s (%s)" % (self.ip, self.num_puerto)

class Empleado(models.Model):
    """
    Modelo que representa a un empleado
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    rfid = models.CharField(
        primary_key=True,
        max_length=30,
        help_text="Introduce el RFID del empleado"
    )
    dentro = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ["user", "rfid"]
    
    def __str__(self):
        """
        Método que representa a un usuario
        """
        return self.user

class RegistroAula(models.Model):
    """
    Modelo usado para estadísticas de Zonas
    """
    rfid = models.ForeignKey(
        Empleado,
        on_delete=models.DO_NOTHING,
        max_length=30
    )
    ip = models.CharField(
        max_length=30
    )
    f_entrada = models.DateTimeField(
        auto_now_add=True
    )
    f_salida = models.DateTimeField(
        auto_now = True
    )
    dentro = models.BooleanField(
        null = False,
        default = False
    )

    class Meta:
        ordering=["rfid","ip"]

    def __str__(self):
        """
        Cadena para devolver RFID e IP
        """
        return '%s (%s)' % (self.rfid, self.ip)

class PermisosAula(models.Model):
    """
    Modelo para gestionar al acceso a las zonas
    """
    grupo=models.ForeignKey(
        Group,
        on_delete=models.DO_NOTHING,
        help_text="Grupo al que quieres dar permiso."
    )
    zona = models.ForeignKey(
        Zona,
        on_delete=models.DO_NOTHING,
        help_text="Zona a la que tiene acceso el grupo."
    )

    def __str__(self):
        """
        Cadena que representa eun permiso
        """
        return "%s (%s)" % (self.grupo, self.zona)

class PermisosPuerto(models.Model):
    """
    Modelos para gestionar los permisos a los puertos
    """
    grupo=models.ForeignKey(
        Group,
        on_delete=models.DO_NOTHING,
        help_text="Grupo al que quieres dar permiso."
    )
    puerto = models.ForeignKey(
        Puerto,
        on_delete=models.DO_NOTHING,
        help_text="Puerto al que tiene permiso."
    )

    def __str__(self):
        """
        Cadena que representa eun permiso
        """
        return "%s (%s)" % (self.grupo, self.puerto)
