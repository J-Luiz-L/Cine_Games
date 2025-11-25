# Cine_Games - Refatorado

Estrutura mínima e funcional com:
- Classe base `Jogo` encapsulada (propriedades + validação)
- Subclasses: `JogoPC`, `JogoConsole`, `JogoMobile`
- `Colecao` para agrupar jogos
- `CatalogoService` para persistência em `data/catalogo.json`
- `repositorio.py` utilitário (opcional)

Como usar:
- Instale dependências (se houver)
- Rodar CLI: `python main.py --listar` ou `python main.py --add-pc "Titulo" "Genero" "Req"`
- Rodar testes: `pytest -q` (os testes exemplo estão em `tests/`)
