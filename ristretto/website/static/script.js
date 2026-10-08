// ─── Radio "Outro" Social: habilita o input ───
const radioOutro = document.getElementById('radio-outro');
const inputOutro = document.getElementById('input-outro');
const radiosEvento = document.querySelectorAll('input[name="social-evento"]');

radiosEvento.forEach(function(radio) {
    radio.addEventListener('change', function() {
        if (radioOutro.checked) {
            inputOutro.disabled = false;
            inputOutro.focus();
        } else {
            inputOutro.disabled = true;
            inputOutro.value = '';
            limparErro('input-outro');
        }
    });
});

// ─── Radio "Outro" Corporativo: habilita o input ───
const corpRadioOutro = document.getElementById('corp-radio-outro');
const corpInputOutro = document.getElementById('corp-input-outro');
const radiosCorpEvento = document.querySelectorAll('input[name="corp-evento"]');

radiosCorpEvento.forEach(function(radio) {
    radio.addEventListener('change', function() {
        if (corpRadioOutro.checked) {
            corpInputOutro.disabled = false;
            corpInputOutro.focus();
        } else {
            corpInputOutro.disabled = true;
            corpInputOutro.value = '';
            limparErro('corp-input-outro');
        }
    });
});

// ─── Painéis "Um dia" / "Mais de um dia" ───
const btnUmDia   = document.getElementById('pills-um-tab');
const btnMaisDia = document.getElementById('pills-mais-tab');
const painelUm   = document.getElementById('pills-home');
const painelMais = document.getElementById('pills-profile');

btnUmDia.addEventListener('click', function() {
    painelMais.style.display = 'none';
    painelUm.style.display   = '';
    btnUmDia.classList.add('active');
    btnMaisDia.classList.remove('active');
});

btnMaisDia.addEventListener('click', function() {
    painelUm.style.display   = 'none';
    painelMais.style.display = '';
    btnMaisDia.classList.add('active');
    btnUmDia.classList.remove('active');
});

// ─── Helpers ───
function abaSocialAtiva() {
    return document.getElementById('home-tab-pane').classList.contains('active');
}

function radioMarcado(name) {
    return document.querySelector('input[name="' + name + '"]:checked') !== null;
}

function campoPreenchido(id) {
    var el = document.getElementById(id);
    return el && el.value.trim() !== '' && el.value !== '';
}

function destacarErro(id) {
    var el = document.getElementById(id);
    if (el) {
        el.style.outline = '2px solid red';
        el.style.borderRadius = '4px';
    }
}

function limparErro(id) {
    var el = document.getElementById(id);
    if (el) el.style.outline = '';
}

function destacarErroRadio(name) {
    document.querySelectorAll('input[name="' + name + '"]').forEach(function(r) {
        r.style.outline = '2px solid red';
    });
}

function limparErroRadio(name) {
    document.querySelectorAll('input[name="' + name + '"]').forEach(function(r) {
        r.style.outline = '';
    });
}

// ─── Validação completa ───
function validarFormulario() {
    var valido = true;
    var social = abaSocialAtiva();

    // Duração: um dia ou mais de um dia
    var umDiaVisivel = painelMais.style.display === 'none';
    if (umDiaVisivel) {
        if (!campoPreenchido('umDia-data'))        { destacarErro('umDia-data');        valido = false; } else { limparErro('umDia-data'); }
        if (!campoPreenchido('umDia-horaInicio'))  { destacarErro('umDia-horaInicio');  valido = false; } else { limparErro('umDia-horaInicio'); }
        if (!campoPreenchido('umDia-horaTermino')) { destacarErro('umDia-horaTermino'); valido = false; } else { limparErro('umDia-horaTermino'); }
    } else {
        if (!campoPreenchido('maisDias-dataInicio'))  { destacarErro('maisDias-dataInicio');  valido = false; } else { limparErro('maisDias-dataInicio'); }
        if (!campoPreenchido('maisDias-dataTermino')) { destacarErro('maisDias-dataTermino'); valido = false; } else { limparErro('maisDias-dataTermino'); }
        if (!campoPreenchido('maisDias-horaInicio'))  { destacarErro('maisDias-horaInicio');  valido = false; } else { limparErro('maisDias-horaInicio'); }
        if (!campoPreenchido('maisDias-horaTermino')) { destacarErro('maisDias-horaTermino'); valido = false; } else { limparErro('maisDias-horaTermino'); }
    }

    // Endereço e convidados
    if (!campoPreenchido('endereco'))       { destacarErro('endereco');       valido = false; } else { limparErro('endereco'); }
    if (!campoPreenchido('num-convidados')) { destacarErro('num-convidados'); valido = false; } else { limparErro('num-convidados'); }

    // Dados pessoais
    if (!campoPreenchido('nome'))     { destacarErro('nome');     valido = false; } else { limparErro('nome'); }
    if (!emailValido())               { destacarErro('email');    valido = false; } else { limparErro('email'); }
    if (!telefoneValido())            { destacarErro('telefone'); valido = false; } else { limparErro('telefone'); }

    if (social) {
        // Aba Social
        if (!radioMarcado('social-evento')) { destacarErroRadio('social-evento'); valido = false; } else { limparErroRadio('social-evento'); }
        if (!radioMarcado('social-alcool')) { destacarErroRadio('social-alcool'); valido = false; } else { limparErroRadio('social-alcool'); }
        if (radioOutro.checked && !campoPreenchido('input-outro')) {
            destacarErro('input-outro'); valido = false;
        } else {
            limparErro('input-outro');
        }
    } else {
        // Aba Corporativo
        if (!radioMarcado('corp-evento')) { destacarErroRadio('corp-evento'); valido = false; } else { limparErroRadio('corp-evento'); }
        if (!radioMarcado('corp-copos'))  { destacarErroRadio('corp-copos');  valido = false; } else { limparErroRadio('corp-copos'); }

        // Doses: select ou campo "mais de 1000"
        var dosesSelect = document.getElementById('corp-doses');
        var dosesMais   = document.getElementById('corp-doses-mais');
        var dosesOk = (dosesSelect && dosesSelect.value !== '') || (dosesMais && dosesMais.value.trim() !== '');
        if (!dosesOk) {
            if (dosesSelect) dosesSelect.style.outline = '2px solid red';
            valido = false;
        } else {
            if (dosesSelect) dosesSelect.style.outline = '';
        }

        // Bebidas: ao menos uma marcada
        var bebidasMarcadas = document.querySelector('input[name="bebidas"]:checked') !== null;
        if (!bebidasMarcadas) {
            document.querySelectorAll('input[name="bebidas"]').forEach(function(b) { b.style.outline = '2px solid red'; });
            valido = false;
        } else {
            document.querySelectorAll('input[name="bebidas"]').forEach(function(b) { b.style.outline = ''; });
        }

        // "Outro" corporativo
        if (corpRadioOutro.checked && !campoPreenchido('corp-input-outro')) {
            destacarErro('corp-input-outro'); valido = false;
        } else {
            limparErro('corp-input-outro');
        }
    }

    return valido;
}

function getCookie(name) {
    var valor = null;
    document.cookie.split(';').forEach(function(c) {
        c = c.trim();
        if (c.startsWith(name + '=')) valor = decodeURIComponent(c.substring(name.length + 1));
    });
    return valor;
}

function val(id) {
    return document.getElementById(id).value.trim();
}

function radioValor(name) {
    var r = document.querySelector('input[name="' + name + '"]:checked');
    return r ? r.value : '';
}

function coletarDados() {
    var social   = abaSocialAtiva();
    var maisDias = painelMais.style.display !== 'none';

    var dados = {
        tipo: social ? 'SOCIAL' : 'CORPORATIVO',

        // Duração
        duracao:      maisDias ? 'DIAS' : 'DIA',
        data_inicio:  maisDias ? val('maisDias-dataInicio')  : val('umDia-data'),
        data_termino: maisDias ? val('maisDias-dataTermino') : '',
        hora_inicio:  maisDias ? val('maisDias-horaInicio')  : val('umDia-horaInicio'),
        hora_termino: maisDias ? val('maisDias-horaTermino') : val('umDia-horaTermino'),

        // Comum
        endereco:       val('endereco'),
        num_convidados: val('num-convidados'),
        observacao:     val('observacao'),
        canal:          val('como-conheceu'),

        // Cliente
        nome:     val('nome'),
        email:    val('email').toLowerCase(),
        telefone: val('telefone').replace(/\D/g, ''),
        mensagem: val('msg')
    };

    if (social) {
        dados.drip_station = document.getElementById('social-drip').checked;
        dados.impressora   = document.getElementById('social-impressora').checked;
        dados.social = {
            tipo_evento:      radioValor('social-evento'),
            outro_evento:     val('input-outro'),
            bebida_alcoolica: radioValor('social-alcool')
        };
    } else {
        dados.drip_station = document.getElementById('corp-drip').checked;
        dados.impressora   = false;  // não existe no formulário corporativo
        dados.corporativo = {
            tipo_evento:          radioValor('corp-evento'),
            outro_evento:         val('corp-input-outro'),
            estimativa_doses:     val('corp-doses'),
            mais_doses:           val('corp-doses-mais'),
            bebidas:              Array.from(document.querySelectorAll('input[name="bebidas"]:checked'))
                                       .map(function(b) { return b.value; }),
            copos_personalizados: radioValor('corp-copos') === 'SIM',
            detalhes:             val('corp-mais-detalhes')
        };
    }
    return dados;
}

// ─── Botão Enviar ───
document.getElementById('enviar').addEventListener('click', async function(e) {
    e.preventDefault();
    if (!validarFormulario()) return;

    try {
        var resposta = await fetch(URL_ENVIAR, {   // URL_ENVIAR é definida no HTML
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(coletarDados())
        });
        var resultado = await resposta.json();

        if (resultado.ok) {
            new bootstrap.Modal(document.getElementById('modal-msg')).show();
            document.getElementById('cancelar').click();   // limpa o formulário
        } else {
            alert(resultado.erro || 'Não foi possível enviar. Tente novamente.');
        }
    } catch (erro) {
        alert('Erro de conexão. Tente novamente em instantes.');
    }
});

// ─── Botão Cancelar ───
document.getElementById('cancelar').addEventListener('click', function(e) {
    e.preventDefault();

    // Limpa todos os inputs, selects e textareas do formulário
    document.querySelectorAll('#form-orcamento input, #form-orcamento select, #form-orcamento textarea').forEach(function(el) {
        if (el.type === 'checkbox' || el.type === 'radio') {
            el.checked = false;
        } else {
            el.value = '';
        }
        el.style.outline = '';
    });

    // Desabilita e limpa inputs "Outro"
    inputOutro.disabled = true;
    inputOutro.value = '';
    corpInputOutro.disabled = true;
    corpInputOutro.value = '';

    // Restaura painel de duração para "Um dia" (radio checked + painel visível)
    document.getElementById('pills-um-tab').checked  = true;
    document.getElementById('pills-mais-tab').checked = false;
    painelMais.style.display = 'none';
    painelUm.style.display   = '';

    // Volta para aba Social
    var socialTab = new bootstrap.Tab(document.getElementById('social-tab'));
    socialTab.show();
});

// mascara e validação do Email e Telefone
var inputEmail    = document.getElementById('email');
var inputTelefone = document.getElementById('telefone');

function emailValido() {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(inputEmail.value.trim());
}

function telefoneValido() {
    var digitos = inputTelefone.value.replace(/\D/g, '');
    return digitos.length === 10 || digitos.length === 11;
}

function formatarTelefone(valor) {
    var d = valor.replace(/\D/g, '').slice(0, 11);
    if (d.length > 10) return '(' + d.slice(0, 2) + ') ' + d.slice(2, 7) + '-' + d.slice(7);
    if (d.length > 6)  return '(' + d.slice(0, 2) + ') ' + d.slice(2, 6) + '-' + d.slice(6);
    if (d.length > 2)  return '(' + d.slice(0, 2) + ') ' + d.slice(2);
    if (d.length > 0)  return '(' + d;
    return '';
}

inputTelefone.setAttribute('inputmode', 'tel');
inputTelefone.setAttribute('maxlength', '15');
inputTelefone.addEventListener('input', function() {
    this.value = formatarTelefone(this.value);
    limparErro('telefone');
});

inputEmail.setAttribute('inputmode', 'email');
inputEmail.addEventListener('input', function() {
    var limpo = this.value.replace(/\s/g, '').toLowerCase();
    if (limpo !== this.value) {
        var pos = this.selectionStart - (this.value.length - limpo.length);
        this.value = limpo;
        try { this.setSelectionRange(pos, pos); } catch (e) {}
    }
    limparErro('email');
});

// tootip da Professora

document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function(el) {
    new bootstrap.Tooltip(el, { customClass: 'tooltip-ristretto' });
});