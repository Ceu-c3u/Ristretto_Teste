import logging
import resend
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import escape

logger = logging.getLogger(__name__)


def _linha(rotulo, valor):
    if not valor:
        return ''
    return f'<p><strong>{rotulo}:</strong> {escape(str(valor))}</p>'


def _resumo_html(evento):
    d = evento.FK_Duracao
    periodo = d.data_inicio.strftime('%d/%m/%Y')
    if d.duracao == 'DIAS':
        periodo += ' a ' + d.data_termino.strftime('%d/%m/%Y')

    return (
        _linha('Categoria', evento.FK_Categoria.get_categoria_display())
        + _linha('Data', periodo)
        + _linha('Horário', f'{d.hora_inicio:%H:%M} às {d.hora_termino:%H:%M}')
        + _linha('Endereço', evento.endereco)
        + _linha('Convidados', evento.num_convidados)
        + _linha('Drip station', 'Sim' if evento.FK_Servico.drip_station else 'Não')
        + _linha('Impressora', 'Sim' if evento.FK_Servico.impressora else 'Não')
        + _linha('Observação', evento.observacao)
        + _linha('Mensagem', evento.mensagem)
    )


def enviar_emails_orcamento(evento, social, corporativo, duplicatas):
    resend.api_key = settings.RESEND_API_KEY
    cliente = evento.FK_Cliente

    # 1) Aviso para os stakeholders (template + alerta de duplicata)
    try:
        html = render_to_string('emails/orcamento_stakeholder.html', {
            'cliente': cliente,
            'evento': evento,
            'duracao': evento.FK_Duracao,
            'servico': evento.FK_Servico,
            'canal': evento.FK_Canal,
            'social': social,
            'corporativo': corporativo,
            'bebidas': corporativo.FK_Bebidas.all() if corporativo else [],
            'duplicatas': duplicatas,
        })

        assunto = f'Novo orçamento: {cliente.nome}'
        if duplicatas:
            assunto = f'⚠️ Possível duplicata: {assunto}'

        resend.Emails.send({
            'from': settings.EMAIL_REMETENTE,
            'to': settings.EMAIL_DESTINO,
            'reply_to': cliente.Email,
            'subject': assunto,
            'html': html,
        })
    except Exception:
        logger.exception('Falha ao enviar e-mail para os stakeholders')

    # 2) Confirmação para o cliente
    try:
        resend.Emails.send({
            'from': settings.EMAIL_REMETENTE,
            'to': [cliente.Email],
            'subject': 'Recebemos o seu pedido de orçamento',
            'html': (
                f'<h2>Olá, {escape(cliente.nome)}!</h2>'
                '<p>Recebemos o seu pedido e entraremos em contato em breve.</p>'
                '<p>Confira abaixo os dados que você enviou:</p>'
                + _resumo_html(evento)
            ),
        })
    except Exception:
        logger.exception('Falha ao enviar e-mail de confirmação ao cliente')