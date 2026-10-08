from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Duracao(models.Model):
    ID_Duracao = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )
    class OpcoesDuracao(models.TextChoices):
        DIA = 'DIA', 'Um dia'
        DIAS = 'DIAS', 'Mais de um dia'

    duracao = models.CharField(
        max_length=5,
        choices=OpcoesDuracao.choices,
        default=OpcoesDuracao.DIA
    )

    data_inicio = models.DateField(
        null=False,
        blank=False
    )
    data_termino = models.DateField(
        null=False,
        blank=False
    )
    def save(self, *args, **kwargs):
        if not self.data_termino and self.data_inicio:
            self.data_termino = self.data_inicio
        super().save(*args, **kwargs)

    hora_inicio = models.TimeField(
        null=False,
        blank=False
    )
    hora_termino = models.TimeField(
        null=False,
        blank=False
    )

class Bebidas(models.Model):
    ID_Bebidas = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )
    class OpcoesBebidas(models.TextChoices):
        EXPRESSO = 'EXPRESSO', 'Expresso'
        CAPPUCCINO = 'CAPPUCCINO', 'Cappuccino'
        CHOC_QUENTE = 'CHOC_QUENTE', 'Chocolate quente cremoso'
        BEBIDAS_GELADAS = 'BEBIDAS_GELADAS', 'Bebidas geladas'
        OUTRO = 'OUTRO', 'Outro'
    
    bebidas = models.CharField(
        max_length=20,
        choices=OpcoesBebidas.choices,
        null=False,
        blank=False
    )

class Categoria(models.Model):
    ID_Categoria = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )
    class OpcoesCategoria(models.TextChoices):
        SOCIAL = 'SOCIAL', 'Social'
        CORPORATIVO = 'CORPORATIVO', 'Corporativo'
    categoria = models.CharField(
        max_length=11,
        choices=OpcoesCategoria.choices,
        null=False,
        blank=False
    )

class Canal(models.Model):
    ID_Canal = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )
    class OpcoesCanal(models.TextChoices):
        INDICACAO = 'INDICACAO', 'Indicação'
        INSTAGRAM = 'INSTAGRAM', 'Instagram'
        GOOGLE = 'GOOGLE', 'Google'
        CASAMENTOS = 'CASAMENTOS.COM', 'Casamentos.com'
        OUTRO = 'OUTROS', 'Outro'
    descoberta = models.CharField(
        max_length=15,
        choices=OpcoesCanal.choices,
        null=False,
        blank=False
    )

class Servico_Adicional(models.Model):
    ID_Servico = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    drip_station = models.BooleanField(
        default=False
    )
    impressora = models.BooleanField(
        default=False
    )

class Cliente(models.Model):
    Email = models.EmailField(
        primary_key=True,
        null=False,
        blank=False
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,11}$'
    )
    telefone = models.CharField(
        validators=[phone_regex], 
        max_length=20, 
        null=False,
        blank=False
    )

    nome = models.CharField(
        max_length = 80,
        null=False,
        blank=False
    )

    data_envio = models.DateTimeField(
        auto_now_add=True
    )

class Evento(models.Model):
    ID_Evento = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    endereco = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    num_convidados = models.IntegerField(
        null=False,
        blank=False
    )

    mensagem = models.TextField(
        null=True,
        blank=True
    )

    observacao = models.TextField(
        max_length=500,
        null=True,
        blank=True
    )

    FK_Servico = models.OneToOneField(
        'Servico_Adicional', 
        on_delete=models.PROTECT, 
        verbose_name="Serviço Adicional do Evento"
    )
    
    FK_Canal = models.OneToOneField(
        'Canal', 
        on_delete=models.PROTECT, 
        verbose_name="Canal de descoberta deste Evento"
    )
    
    FK_Duracao = models.OneToOneField(
        'Duracao', 
        on_delete=models.PROTECT, 
        verbose_name="Duração do Evento"
    )
    
    FK_Categoria = models.OneToOneField(
        'Categoria', 
        on_delete=models.PROTECT, 
        verbose_name="Categoria do evento"
    )

    FK_Cliente = models.ForeignKey(
        'Cliente', 
        on_delete=models.CASCADE, 
        verbose_name="Cliente Responsável"
    )

class Corporativo(models.Model):
    ID_Corporativo = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    class OpcoesCorporativo(models.TextChoices):
        REUNIAO = 'REUNIAO', 'Reunião/Treinamento'
        FEIRA = 'FEIRA', 'Feira/Congresso'
        LANCAMENTO = 'LANCAMENTO', 'Lançamento de produto'
        FIM_DE_ANO = 'FIM_ANO', 'Evento de fim de ano'
        OUTRO = 'OUTRO', 'Outro'

    tipo_evento = models.CharField(
        max_length=15,
        choices=OpcoesCorporativo.choices,
        null=False,
        blank=False
    )

    outro_evento = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    class OpcoesDoses(models.IntegerChoices):
        DOSES_200  = 200,  '200 doses'
        DOSES_300  = 300,  '300 doses'
        DOSES_400  = 400,  '400 doses'
        DOSES_500  = 500,  '500 doses'
        DOSES_600  = 600,  '600 doses'
        DOSES_700  = 700,  '700 doses'
        DOSES_800  = 800,  '800 doses'
        DOSES_900  = 900,  '900 doses'
        DOSES_1000 = 1000, '1000 doses'

    estimativa_doses = models.IntegerField(
        choices=OpcoesDoses.choices,
        null=False,
        blank=False,
        verbose_name="Estimativa de Doses diárias"
    )

    mais_doses = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    copos_personalizados = models.BooleanField(
        default=False
    )

    detalhes = models.TextField(
        max_length=255,
        null=True,
        blank=True
    )

    FK_Evento = models.OneToOneField(
        'Evento',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Evento Corporativo Relacionado"
    )

    FK_Bebidas = models.ManyToManyField(
        'Bebidas',
        blank=True,
        verbose_name="Bebidas Selecionadas"
    )

class Social(models.Model):
    ID_Social = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    class OpcoesSocial(models.TextChoices):
        CASAMENTO = 'CASAMENTO', 'Casamento'
        ANIVERSARIO = 'ANIVERSARIO', 'Aniversário'
        FORMATURA = 'FORMATURA', 'Formatura'
        CONFRATERNIZACAO = 'CONFRATERNIZACAO', 'Confraternização Particular'
        OUTRO = 'OUTRO', 'Outro'
    
    tipo_evento = models.CharField(
        max_length=30,
        choices=OpcoesSocial.choices,
        null=False,
        blank=False
    )

    outro_evento = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    class OpcoesAlcoolicas(models.TextChoices):
        SIM = 'SIM', 'Sim'
        NAO = 'NAO', 'Não'
        TALVEZ = 'TALVEZ', 'Talvez'

    bebida_alcoolica = models.CharField(
        max_length=6,
        choices=OpcoesAlcoolicas.choices,
        null=False,
        blank=False
    )

    FK_Evento = models.OneToOneField(
    'Evento',
    on_delete=models.CASCADE,
    null=False,
    blank=False,
    verbose_name="Evento Social Relacionado"
    )