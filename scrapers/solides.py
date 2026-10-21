import time

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from core.job import Job, extrair_data_publicacao
from core.logger import get_logger
from scrapers.base import BaseScraper

logger = get_logger()

_MODALIDADES = {"remoto", "híbrido", "hibrido", "presencial"}
MAX_PAGINAS = 3


def _slug(termo: str) -> str:
    return termo.strip().lower().replace(" ", "-")


class SolidesScraper(BaseScraper):
    """Busca vagas no portal público Sólides.

    O portal mudou o markup em 2026 e o seletor antigo dos cards deixou de ser válido.
    Em vez de depender da tag do card, usamos o elemento mais estável do
    portal: links de detalhe ``/vaga/<id>``. O container do card é obtido
    a partir do próprio link, tornando o scraper menos sensível a mudanças
    de h2/h3/li/div.
    """

    def __init__(self, termos_busca: list[str]):
        self.termos_busca = termos_busca

    def buscar_vagas(self) -> list[Job]:
        vagas: list[Job] = []
        for termo in self.termos_busca:
            vagas.extend(self._buscar_termo(termo))
        logger.info(f"[Solides] {len(vagas)} vaga(s) encontrada(s) no total")
        return vagas

    def _buscar_termo(self, termo: str) -> list[Job]:
        logger.info(f"[Solides] Buscando: {termo}")
        vagas: list[Job] = []
        vistos: set[str] = set()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                )
            )
            page.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
            )

            try:
                for pagina in range(1, MAX_PAGINAS + 1):
                    url = f"https://vagas.solides.com.br/vagas/todos/{_slug(termo)}?page={pagina}"
                    page.goto(url, wait_until="domcontentloaded", timeout=60000)

                    try:
                        page.wait_for_selector('a[href*="/vaga/"]', state="attached", timeout=25000)
                    except PlaywrightTimeoutError:
                        corpo = page.inner_text("body").lower()
                        if pagina == 1 and (
                            "0 vaga" in corpo
                            or "nenhuma vaga" in corpo
                            or "não encontramos" in corpo
                        ):
                            logger.info(f"[Solides] 0 resultados reais para '{termo}'.")
                        else:
                            logger.warning(
                                f"[Solides] Nenhum link de vaga apareceu na página {pagina} de "
                                f"'{termo}' — possível mudança de layout, bloqueio ou fim da paginação."
                            )
                        break

                    time.sleep(1)
                    links = page.locator('a[href*="/vaga/"]')
                    total_links = links.count()
                    novos_na_pagina = 0

                    for i in range(total_links):
                        try:
                            link_el = links.nth(i)
                            href = link_el.get_attribute("href")
                            if not href or "/vaga/" not in href:
                                continue
                            link = href if href.startswith("http") else f"https://vagas.solides.com.br{href}"
                            if link in vistos:
                                continue

                            titulo = (link_el.inner_text() or "").strip()
                            # Alguns layouts deixam "Ver Vaga" no link e o título
                            # em um heading irmão/ancestral. Procura no card.
                            card = link_el.locator("xpath=ancestor::*[self::article or self::li or self::div][1]")
                            texto_card = card.inner_text().strip() if card.count() else ""
                            if not titulo or titulo.lower() in {"ver vaga", "ver detalhes", "candidatar-se"}:
                                heading = card.locator("h1, h2, h3, h4").first if card.count() else None
                                if heading is not None and heading.count():
                                    titulo = heading.inner_text().strip()
                            if not titulo or titulo.lower() in {"ver vaga", "ver detalhes", "candidatar-se"}:
                                continue

                            linhas = [x.strip() for x in texto_card.splitlines() if x.strip()]
                            empresa = "Não informado"
                            local = "Não informado"
                            modalidade = ""
                            for linha in linhas:
                                low = linha.lower()
                                if low in _MODALIDADES:
                                    modalidade = linha
                                if " - " in linha and len(linha) <= 100 and local == "Não informado":
                                    local = linha
                            # Evita inventar empresa quando o novo layout não a expõe
                            # claramente no card; o restante do pipeline aceita o fallback.
                            publicado_em = extrair_data_publicacao(texto_card)
                            vistos.add(link)
                            novos_na_pagina += 1
                            vagas.append(Job(
                                titulo=titulo,
                                empresa=empresa,
                                local=local,
                                link=link,
                                site="Solides",
                                publicado_em=publicado_em,
                                modalidade=modalidade,
                            ))
                        except Exception as e:
                            logger.warning(f"[Solides] Erro ao processar vaga: {e}")

                    if novos_na_pagina == 0:
                        break
            except Exception as e:
                logger.error(f"[Solides] Erro ao buscar '{termo}': {e}")
            finally:
                browser.close()

        return vagas
