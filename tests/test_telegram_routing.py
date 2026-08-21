from types import SimpleNamespace

import pytest

import notifier.telegram as telegram


@pytest.fixture
def chats(monkeypatch):
    monkeypatch.setattr(telegram, "TELEGRAM_CHAT_ID", "chat-principal")
    monkeypatch.setattr(telegram, "TELEGRAM_CHAT_ID_5", "chat-5")
    monkeypatch.setattr(telegram, "TELEGRAM_CHAT_ID_6", "chat-6")
    monkeypatch.setattr(telegram, "TELEGRAM_CHAT_ID_7", "chat-7")


@pytest.mark.parametrize(
    "score,esperado",
    [
        (0, ""),
        (4, ""),
        (5, "chat-5"),
        (6, "chat-6"),
        (7, "chat-7"),
        (8, "chat-7"),
        (9, "chat-7"),
        (10, "chat-7"),
    ],
)
def test_chat_id_por_relevancia(chats, score, esperado):
    assert telegram._chat_id_por_relevancia(score) == esperado


@pytest.mark.parametrize(
    "score,esperado",
    [
        (5, "chat-5"),
        (6, "chat-6"),
        (7, "chat-7"),
        (9, "chat-7"),
    ],
)
def test_notificar_vaga_envia_para_chat_correto(
    chats,
    monkeypatch,
    score,
    esperado,
):
    enviado = {}

    def fake_enviar_mensagem(texto, reply_markup=None, chat_id=None):
        enviado["texto"] = texto
        enviado["chat_id"] = chat_id
        return True

    monkeypatch.setattr(telegram, "enviar_mensagem", fake_enviar_mensagem)

    job = SimpleNamespace(
        id="job-teste",
        relevancia=score,
        motivo="Teste",
        empresa="Empresa Teste",
        titulo="Vaga Teste",
        senioridade="Júnior",
        local="Remoto",
        modalidade="Remoto",
        site="Teste",
        publicado_em="",
        publicacao_antiga=False,
        link="https://example.com/vaga",
    )

    assert telegram.notificar_vaga(job) is True
    assert enviado["chat_id"] == esperado


def test_digest_separa_as_tres_faixas_sem_duplicar(
    chats,
    monkeypatch,
):
    envios = []

    def fake_enviar_mensagem(texto, reply_markup=None, chat_id=None):
        envios.append((chat_id, texto))
        return True

    monkeypatch.setattr(telegram, "enviar_mensagem", fake_enviar_mensagem)

    vagas = [
        ("Vaga 4", "Empresa", "https://x/4", 4, 0),
        ("Vaga 5", "Empresa", "https://x/5", 5, 0),
        ("Vaga 6", "Empresa", "https://x/6", 6, 0),
        ("Vaga 7", "Empresa", "https://x/7", 7, 0),
        ("Vaga 9", "Empresa", "https://x/9", 9, 0),
    ]

    assert telegram.enviar_digest(vagas, "Brasil") is True

    assert len(envios) == 3

    chat5 = next(texto for chat, texto in envios if chat == "chat-5")
    chat6 = next(texto for chat, texto in envios if chat == "chat-6")
    chat7 = next(texto for chat, texto in envios if chat == "chat-7")

    assert "Vaga 5" in chat5
    assert "Vaga 6" not in chat5
    assert "Vaga 7" not in chat5

    assert "Vaga 6" in chat6
    assert "Vaga 5" not in chat6
    assert "Vaga 7" not in chat6

    assert "Vaga 7" in chat7
    assert "Vaga 9" in chat7
    assert "Vaga 5" not in chat7
    assert "Vaga 6" not in chat7

    # Abaixo de 5 não deve aparecer em lugar nenhum.
    assert all("Vaga 4" not in texto for _, texto in envios)


def test_digest_com_apenas_score_abaixo_de_5_nao_envia(
    chats,
    monkeypatch,
):
    envios = []

    def fake_enviar_mensagem(texto, reply_markup=None, chat_id=None):
        envios.append((chat_id, texto))
        return True

    monkeypatch.setattr(telegram, "enviar_mensagem", fake_enviar_mensagem)

    vagas = [
        ("Vaga 3", "Empresa", "https://x/3", 3, 0),
        ("Vaga 4", "Empresa", "https://x/4", 4, 0),
    ]

    assert telegram.enviar_digest(vagas, "Brasil") is True
    assert envios == []


def test_telegram_429_aguarda_retry_after_e_tenta_novamente(
    monkeypatch,
):
    monkeypatch.setattr(
        telegram,
        "TELEGRAM_BOT_TOKEN",
        "token-teste",
    )
    monkeypatch.setattr(
        telegram,
        "TELEGRAM_CHAT_ID_7",
        "chat-7",
    )

    # Neste teste queremos validar só o retry do 429,
    # não o throttle entre mensagens.
    monkeypatch.setattr(
        telegram,
        "_aguardar_limite_chat",
        lambda chat_id: None,
    )

    sleeps = []

    monkeypatch.setattr(
        telegram.time,
        "sleep",
        lambda segundos: sleeps.append(segundos),
    )

    class Resposta429:
        status_code = 429
        reason = "Too Many Requests"

        def json(self):
            return {
                "ok": False,
                "parameters": {
                    "retry_after": 2,
                },
            }

        def raise_for_status(self):
            raise AssertionError(
                "raise_for_status não deve ser chamado "
                "antes do retry do 429"
            )

    class RespostaOK:
        status_code = 200
        reason = "OK"

        def json(self):
            return {"ok": True}

        def raise_for_status(self):
            return None

    respostas = [
        Resposta429(),
        RespostaOK(),
    ]

    chamadas = []

    def fake_post(url, data, timeout):
        chamadas.append(
            {
                "url": url,
                "data": data,
                "timeout": timeout,
            }
        )
        return respostas.pop(0)

    monkeypatch.setattr(
        telegram.requests,
        "post",
        fake_post,
    )

    resultado = telegram.enviar_mensagem(
        "Teste",
        chat_id="chat-7",
    )

    assert resultado is True
    assert len(chamadas) == 2

    # retry_after=2 + margem de 1 segundo
    assert sleeps == [3]