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
    num_zona = models.IntegerField(
        unique=True,
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
    tipo = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        help_text="Tipo de aula (p. ej. Clase, C.P.D...)"
    )
    descripcion = models.TextField(
        max_length=1000,
        help_text="Introduce una descripción de la zona."
    )
    dentro = models.BooleanField(
        default=False,
        help_text="La zona se encuentra ocupada o no."
    )

    usuario_dentro = False

    def __str__(self):
        """
        String que representa al objeto Zona
        """
        return "%s %s" % (self.num_zona, self.tipo)

    class Meta:
        """
        Clase para ordenar las zonas segun el número y la ip
        """
        ordering = ["num_zona", "ip"]
        unique_together = (
            "ip", "num_zona"
        )

class ConjuntoZona(models.Model):
    """
    Modelo para representar zonas de las mismas características
    """
    zona = models.ManyToManyField(
        Zona,
        help_text="Elige las zonas que quieres agrupar"
    )
    conjunto_zona = models.CharField(
        max_length=20,
        help_text="Nombre para agrupar zonas (p. ej. Baños, Despachos...)"
    )
    grupos_con_acceso = models.ManyToManyField(
        Group
    )

    def __str__(self):
        """
        String que representa el conjunto de zonas
        """
        return self.conjunto_zona

    class Meta:
        """
        Clase para ordenar conjuntos
        """
        ordering = ["conjunto_zona"]

class Puerto(models.Model):
    """
    Modelo que representa un puerto
    """
    ip = models.ForeignKey(
        Zona,
        on_delete=models.CASCADE,
        help_text="Ip de la zona"
    )
    num_puerto = models.IntegerField(
        help_text="Número de puerto del arduino"
    )
    descripcion = models.CharField(
        max_length=35,
        help_text="Acción que realiza dicho puerto"
    )
    encendido = models.BooleanField(
        default=False
    )

    class Meta:
        """
        Clase para ordenar los puertos por ip y número de puerto.
        Clase para que 'ip' u 'num_puerto' sean únicos:
        -- Clave primaria formada por dos campos --
        """
        ordering = ["ip", "num_puerto"]
        unique_together = (
            "ip", "num_puerto"
        )

    def __str__(self):
        """
        Método que identifica a un puerto en concreto
        """
        return "%s (%s) [%s]" % (self.ip, self.num_puerto, self.descripcion)

class ConjuntoPuerto(models.Model):
    """
    Modelo para representar zonas de las mismas características
    """
    puerto = models.ManyToManyField(
        Puerto,
        help_text="Elige los puertos que quieres agrupar"
    )
    conjunto_puerto = models.CharField(
        max_length=20,
        help_text="Nombre para agrupar los puertos (p. ej. Baños, Despachos...)"
    )
    grupos_con_acceso = models.ManyToManyField(
        Group
    )

    def __str__(self):
        """
        String que representa el conjunto de zonas
        """
        return self.conjunto_puerto

    class Meta:
        """
        Clase para ordenar conjuntos
        """
        ordering = ["conjunto_puerto"]

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
        """
        Clase para ordenar los empleados por Nombre y rfid
        """
        ordering = ["user", "rfid"]


    def __str__(self):
        """
        Método que representa a un usuario
        """
        return str(self.user)

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
    )
    f_salida = models.DateTimeField(
        null=True,
        blank=True
    )
    dentro = models.BooleanField(
        null=False,
        default=False
    )

    class Meta:
        """
        Clase para ordenar los registros por usuario e ip
        """
        ordering = ["rfid", "ip"]


    def __str__(self):
        """
        Cadena para devolver RFID e IP
        """
        return '%s (%s)' % (self.rfid, self.ip)
