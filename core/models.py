# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Feed(models.Model):
    title = models.CharField(max_length=1000)
    privado = models.BooleanField(auto_created=True)
    link = models.TextField()
    subtitle = models.TextField()
    data_criacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'feed'  # nome da tabela no BD

    def __str__(self):
        return self.title

    @property
    def get_data_criacao(self):
        return self.data_criacao

    @property
    def get_link(self):
        return self.link

    @property
    def get_usuario(self):
        return self.usuario

    @property
    def get_title(self):
        return self.title

    @property
    def get_subtitle(self):
        return self.subtitle

    @property
    def get_summary(self):
        return self.summary
