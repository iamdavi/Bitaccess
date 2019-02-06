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
    ip = models.CharField(
        max_length=25,
        help_text="Ip del dispositivo asociado a esta aula"
    )
    modelo = models.CharField(
        max_length=25,
        help_text="Introduce el modelo del arduino (p. ej. Uno, Mega, etc.)"
    )
    id_zona = models.CharField(
        max_length=25,
        help_text="Identificador de zona (p. ej. Clase 2, Baño 4...)"
    )
    descripcion = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text="Introduce una descripción de la zona."
    )

    @property
    def usuario_dentro(self):
        """
        Usuario que está dentro de la zona, si no hay ninguno devuele None
        """
        registros_activos = RegistroAula.objects.filter(f_salida=None,
                                                         ip=self.ip)
        if registros_activos:
            return registros_activos[0].rfid.user
        return None

    def __str__(self):
        """
        String que representa al objeto Zona
        """
        return self.id_zona


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
    zona = models.ForeignKey(
        Zona,
        on_delete=models.CASCADE,
        help_text="Zona donde se encuentra el dispositivo."
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
        ordering = ["zona", "num_puerto"]
        unique_together = (
            "zona", "num_puerto"
        )

    def __str__(self):
        """
        Método que identifica a un puerto en concreto
        """
        return f"{self.zona} {self.descripcion}"

class ConjuntoPuerto(models.Model):
    """
    Modelo para representar zonas de las mismas características
    """
    puertos = models.ManyToManyField(
        Puerto,
        help_text="Elige los puertos que quieres agrupar"
    )
    conjunto_puerto = models.CharField(
        max_length=20,
        help_text="Nombre para agrupar los puertos (p. ej. Luces, Puertas...)"
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
    grupo = models.ManyToManyField(
        Group
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
    f_entrada = models.DateTimeField()
    f_salida = models.DateTimeField(
        null=True,
        blank=True
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

    @property
    def zona(self):
        """
        Zona asociada a la ip del registro
        """
        return Zona.objects.get(ip=self.ip)
