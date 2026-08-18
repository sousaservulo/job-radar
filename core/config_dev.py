# Perfil de Desenvolvimento

KEYWORDS_CARGO_FORTE_DEV = [
    "Desenvolvedor Backend",
    "Backend Developer",
    "Backend Engineer",
    "Desenvolvedor de Software",
    "Software Developer",
    "Software Engineer",
    "Desenvolvedor .NET",
    ".NET Developer",
    "Desenvolvedor C#",
    "C# Developer",
    "Desenvolvedor Java",
    "Java Developer",
    "Desenvolvedor PHP",
    "PHP Developer",
    "Desenvolvedor Laravel",
    "Laravel Developer",
    "Desenvolvedor Full Stack",
    "Full Stack Developer",
    "Fullstack Developer",
    "Analista Desenvolvedor",
]

KEYWORDS_CARGO_AMBIGUO_DEV = [
    "Desenvolvedor",
    "Developer",
    "Programador",
    "Analista de Sistemas",
    "Systems Analyst",
]

QUALIFICADORES_DEV = [
    "backend",
    ".net",
    "dotnet",
    "c#",
    "csharp",
    "java",
    "spring",
    "spring boot",
    "php",
    "laravel",
    "api",
    "rest",
    "sql",
    "full stack",
    "fullstack",
    "microservices",
    "microserviços",
]

FERRAMENTAS_TITULO_DEV = [
    ".NET",
    "C#",
    "Java",
    "Spring Boot",
    "PHP",
    "Laravel",
]

QUALIFICADORES_CARGO_DEV = [
    "desenvolvedor",
    "developer",
    "engenheiro",
    "engineer",
    "programador",
    "analista",
    "analyst",
    "backend",
    "full stack",
    "fullstack",
]

KEYWORDS_DEV = KEYWORDS_CARGO_FORTE_DEV + KEYWORDS_CARGO_AMBIGUO_DEV

TERMOS_BUSCA_DEV = [
    "desenvolvedor backend",
    "backend developer",
    "desenvolvedor de software",
    "software developer junior",
    "desenvolvedor .net",
    ".net developer",
    "desenvolvedor c#",
    "c# developer",
    "desenvolvedor java",
    "java developer",
    "spring boot developer",
    "desenvolvedor php",
    "php developer",
    "laravel developer",
    "desenvolvedor full stack",
    "full stack junior",
    "analista desenvolvedor",
]

TERMOS_POR_CICLO_DEV = 8

CIDADES_DEV = [
    "Remoto",
    "Natal",
    "Parnamirim",
    "João Pessoa",
    "Recife",
]

MERCADOS_REMOTO_ACEITOS_DEV = [
    "Brasil",
    "Portugal",
    "Estados Unidos",
    "Canadá",
    "Uruguai",
    "Paraguai",
]

LOCATIONS_LINKEDIN_DEV = []

LOCATIONS_LINKEDIN_REMOTO_DEV = [
    "Brasil",
    "Portugal",
    "United States",
    "Canada",
    "Uruguay",
    "Paraguay",
]

LOCATIONS_LINKEDIN_CIDADES_DEV = [
    cidade
    for cidade in CIDADES_DEV
    if cidade != "Remoto"
]