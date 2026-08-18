import pytest

from core.job import Job
from core.perfis import PERFIS
from utils.filtro import filtrar_vagas


def _vaga(
    titulo: str,
    local: str = "Brasil",
    modalidade: str = "Remoto",
) -> Job:
    return Job(
        titulo=titulo,
        empresa="Empresa Teste",
        local=local,
        link="https://example.com/vaga",
        site="Teste",
        modalidade=modalidade,
    )


@pytest.mark.parametrize(
    "titulo",
    [
        "Desenvolvedor Backend Java Júnior",
        ".NET Developer Jr",
        "Software Developer C#",
        "Laravel Developer",
        "Full Stack Developer Jr",
        "Analista Desenvolvedor Java",
    ],
)
def test_dev_aceita_cargos_alvo(titulo):
    perfil = PERFIS["dev"]
    assert _vaga(titulo).combina_com(perfil.regras)


@pytest.mark.parametrize(
    "titulo",
    [
        "Data Analyst",
        "Product Manager",
        "Analista Financeiro",
        "UX Designer",
        "Analista de Marketing",
    ],
)
def test_dev_rejeita_cargos_fora_do_alvo(titulo):
    perfil = PERFIS["dev"]
    assert not _vaga(titulo).combina_com(perfil.regras)


@pytest.mark.parametrize(
    "titulo",
    [
        "Analista de Suporte N1",
        "Analista de Suporte N2",
        "Service Desk Analyst",
        "Técnico de Suporte",
        "IT Support Analyst",
        "Analista NOC Jr",
    ],
)
def test_suporte_aceita_cargos_alvo(titulo):
    perfil = PERFIS["suporte"]
    assert _vaga(titulo).combina_com(perfil.regras)


@pytest.mark.parametrize(
    "titulo",
    [
        "Analista Financeiro",
        "Customer Success",
        "Desenvolvedor Backend",
        "Product Manager",
        "Coordenador Comercial",
    ],
)
def test_suporte_rejeita_cargos_fora_do_alvo(titulo):
    perfil = PERFIS["suporte"]
    assert not _vaga(titulo).combina_com(perfil.regras)


@pytest.mark.parametrize(
    "local",
    [
        "Remote - Brazil",
        "Remote - Portugal",
        "Remote - United States",
        "Remote - Canada",
        "Remote - Uruguay",
        "Remote - Paraguay",
    ],
)
def test_dev_aceita_mercados_remotos_configurados(local):
    perfil = PERFIS["dev"]
    vaga = _vaga(
        "Desenvolvedor Backend Java Júnior",
        local=local,
    )
    assert vaga.combina_com(perfil.regras)


@pytest.mark.parametrize(
    "local",
    [
        "Remote - Brazil",
        "Remote - Portugal",
    ],
)
def test_suporte_aceita_brasil_e_portugal_remotos(local):
    perfil = PERFIS["suporte"]
    vaga = _vaga(
        "Analista de Suporte N1",
        local=local,
    )
    assert vaga.combina_com(perfil.regras)


def test_suporte_nao_aceita_canada_remoto():
    perfil = PERFIS["suporte"]

    vaga = _vaga(
        "Analista de Suporte N1",
        local="Remote - Canada",
    )

    assert not vaga.combina_com(perfil.regras)


@pytest.mark.parametrize("perfil_chave,titulo", [
    ("dev", "Desenvolvedor Backend Java Júnior"),
    ("suporte", "Analista de Suporte N1"),
])
def test_perfis_aceitam_presencial_em_natal(perfil_chave, titulo):
    perfil = PERFIS[perfil_chave]

    vaga = _vaga(
        titulo,
        local="Natal, RN",
        modalidade="Presencial",
    )

    assert vaga.combina_com(perfil.regras)


@pytest.mark.parametrize("perfil_chave,titulo", [
    ("dev", "Desenvolvedor Backend Java Júnior"),
    ("suporte", "Analista de Suporte N1"),
])
def test_perfis_rejeitam_presencial_em_sao_paulo(perfil_chave, titulo):
    perfil = PERFIS[perfil_chave]

    vaga = _vaga(
        titulo,
        local="São Paulo, SP",
        modalidade="Presencial",
    )

    assert not vaga.combina_com(perfil.regras)


def test_dev_junior_pontua_acima_de_senior():
    perfil = PERFIS["dev"]

    junior = _vaga("Desenvolvedor Backend Java Júnior")
    senior = _vaga("Desenvolvedor Backend Java Sênior")

    aprovadas, _ = filtrar_vagas(
        [junior, senior],
        perfil.regras,
    )

    assert len(aprovadas) == 2
    assert junior.relevancia >= 7
    assert junior.relevancia > senior.relevancia


def test_suporte_junior_pontua_acima_de_senior():
    perfil = PERFIS["suporte"]

    junior = _vaga("Analista de Suporte N1 Júnior")
    senior = _vaga("Analista de Suporte N2 Sênior")

    aprovadas, _ = filtrar_vagas(
        [junior, senior],
        perfil.regras,
    )

    assert len(aprovadas) == 2
    assert junior.relevancia >= 7
    assert junior.relevancia > senior.relevancia