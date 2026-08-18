# Perfil de Suporte / Service Desk

KEYWORDS_CARGO_FORTE_SUPORTE = [
    "Analista de Suporte",
    "Analista de Suporte N1",
    "Analista de Suporte N2",
    "Suporte Técnico",
    "Técnico de Suporte",
    "Assistente de Suporte",
    "Service Desk",
    "Analista de Service Desk",
    "Help Desk",
    "Analista de Help Desk",
    "Technical Support",
    "Support Analyst",
    "IT Support",
    "Support Engineer",
    "Analista NOC",
    "NOC Analyst",
]

KEYWORDS_CARGO_AMBIGUO_SUPORTE = [
    "Analista de TI",
    "IT Analyst",
    "Analista de Sistemas",
    "Systems Analyst",
]

QUALIFICADORES_SUPORTE = [
    "suporte",
    "support",
    "service desk",
    "help desk",
    "n1",
    "n2",
    "incidente",
    "incidentes",
    "incident",
    "infraestrutura",
    "active directory",
    "microsoft 365",
    "office 365",
    "windows",
    "monitoramento",
    "noc",
    "sql",
]

FERRAMENTAS_TITULO_SUPORTE = [
    "N1",
    "N2",
]

QUALIFICADORES_CARGO_SUPORTE = [
    "analista",
    "analyst",
    "suporte",
    "support",
    "técnico",
    "technician",
]

KEYWORDS_SUPORTE = (
    KEYWORDS_CARGO_FORTE_SUPORTE
    + KEYWORDS_CARGO_AMBIGUO_SUPORTE
)

TERMOS_BUSCA_SUPORTE = [
    "analista de suporte",
    "analista de suporte n1",
    "analista de suporte n2",
    "service desk",
    "help desk",
    "technical support",
    "support analyst",
    "it support",
    "técnico de suporte",
    "suporte técnico",
    "analista noc",
    "noc analyst",
]

TERMOS_POR_CICLO_SUPORTE = 8

CIDADES_SUPORTE = [
    "Remoto",
    "Natal",
    "Parnamirim",
    "João Pessoa",
    "Recife",
]

MERCADOS_REMOTO_ACEITOS_SUPORTE = [
    "Brasil",
    "Portugal",
]

LOCATIONS_LINKEDIN_SUPORTE = []

LOCATIONS_LINKEDIN_REMOTO_SUPORTE = [
    "Brasil",
    "Portugal",
]

LOCATIONS_LINKEDIN_CIDADES_SUPORTE = [
    cidade
    for cidade in CIDADES_SUPORTE
    if cidade != "Remoto"
]