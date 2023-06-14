from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=127, verbose_name='название проекта')
    description = models.TextField(verbose_name='описание проекта')
    image = models.ImageField(upload_to='images', verbose_name='картинка проекта')
    is_aproved = models.BooleanField(default=False, verbose_name='отображаеть на сайте или нет')

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

class Application(models.Model):
    name = models.CharField(max_length=127, verbose_name='имя клиента')
    mail = models.EmailField(unique=True, verbose_name='почта')
    message = models.TextField(verbose_name='сообщение')

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
    