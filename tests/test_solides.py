from scrapers.solides import _converter_vaga, _modalidade


def test_converte_vaga_solides_api():
    item = {
        "id": 938616,
        "title": "Desenvolvedor Full Stack Pleno",
        "companyName": "Empresa Teste",
        "city": {"name": "Belo Horizonte"},
        "state": {"code": "MG"},
        "jobType": "remoto",
        "createdAt": "2026-10-20T12:00:00Z",
    }

    vaga = _converter_vaga(item)

    assert vaga is not None
    assert vaga.titulo == "Desenvolvedor Full Stack Pleno"
    assert vaga.empresa == "Empresa Teste"
    assert vaga.local == "Belo Horizonte - MG"
    assert vaga.modalidade == "Remoto"
    assert vaga.link == "https://vagas.solides.com.br/vaga/938616"


def test_solides_nao_forca_remoto():
    assert _modalidade({"jobType": "presencial"}) == "Presencial"
    assert _modalidade({"jobType": "hibrido"}) == "Híbrido"
    assert _modalidade({}) == ""
