from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Lliga(models.Model):
    nom = models.CharField(max_length=100)
    temporada = models.CharField(max_length=20)
    data_inici = models.DateField(null=True)
    data_fi = models.DateField(null=True)
    
    def __str__(self):
        return f"{self.nom} {self.temporada}"

class Equip(models.Model):
    nom = models.CharField(max_length=100)
    ciutat = models.CharField(max_length=100)
    fundacio = models.IntegerField(null=True)
    escut = models.ImageField(upload_to='escuts/', null=True, blank=True)
    lliga = models.ManyToManyField(Lliga, related_name='equips')
    
    def __str__(self):
        return self.nom

class Jugador(models.Model):
    nom = models.CharField(max_length=100)
    cognoms = models.CharField(max_length=100)
    data_naixement = models.DateField()
    nacionalitat = models.CharField(max_length=50)
    dorsal = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )
    posicio = models.CharField(max_length=50)
    equip = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name='jugadors')
    foto = models.ImageField(upload_to='fotos_jugadors/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.nom} {self.cognoms} ({self.equip})"

class Partit(models.Model):
    lliga = models.ForeignKey(Lliga, on_delete=models.CASCADE, related_name='partits')
    local = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name='partits_local')
    visitant = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name='partits_visitant')
    data = models.DateTimeField()
    #gols_local = models.IntegerField(default=0)
    #gols_visitant = models.IntegerField(default=0)
    finalitzat = models.BooleanField(default=False)
    class Meta:
        ordering = ['data']
        verbose_name_plural = 'partits'
    def __str__(self):
        return f"{self.local} - {self.visitant} ({self.data})"
    def gols_local(self):
        gols = self.events.filter(
                        tipus="GOL",
                        equip=self.local).count()
        return gols
    def gols_visitant(self):
        gols = self.events.filter(
                        tipus="GOL",
                        equip=self.visitant).count()
        return gols

class Event(models.Model):
    TIPUS_EVENT = [
        ('GOL', 'Gol'),
        ('AUTOGOL', 'Autogol'),
        ('FALTA', 'Falta'),
        ('PENALTY', 'Penalty'),
        ('MANS', 'Mans'),
        ('CESSIO', 'Cessió'),
        ('ENTRADA', 'Entrada'),
        ('SORTIDA', 'Sortida'),
        ('TARGETA_GROGA', 'Targeta Groga'),
        ('TARGETA_VERMELLA', 'Targeta Vermella'),
    ]
    
    partit = models.ForeignKey(Partit, on_delete=models.CASCADE, related_name='events')
    temps = models.TimeField()
    tipus = models.CharField(max_length=30, choices=TIPUS_EVENT)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='events')
    equip = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name='events')
    detalls = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.partit} - {self.tipus} de {self.jugador}"

