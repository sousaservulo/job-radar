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