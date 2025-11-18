# Cine_Games
# Catálogo Pessoal de Jogos Digitais

## Objetivo do Projeto
Este projeto tem como objetivo desenvolver um sistema de linha de comando (CLI) para gerenciar um catálogo pessoal de jogos digitais. O foco principal é aplicar e demonstrar os conceitos fundamentais da **Programação Orientada a Objetos (POO)**, como **Encapsulamento**, **Herança** (simples e, se aplicável, múltipla/Mixins) e **Polimorfismo**.

O sistema permitirá o cadastro de jogos, o registro de progresso de jogatina, a organização por coleções e a geração de relatórios de desempenho e tempo jogado.

## Estrutura de Classes Planejada 

A solução será estruturada em torno das seguintes classes principais:

1.  **`Jogo` (Classe Base):**
    * **Responsabilidade:** Define a estrutura e o comportamento comum a *todos* os tipos de jogos (atributos como título, status, horas, e métodos de atualização de progresso).
    * **Conceitos POO:** Implementa o **encapsulamento** dos atributos sensíveis (como `horas_jogadas` e `avaliacao`) utilizando o decorador `@property` para garantir a integridade dos dados e aplicar validações.

2.  **`JogoPC`, `JogoConsole`, `JogoMobile` (Classes Filhas):**
    * **Responsabilidade:** Especializam a classe `Jogo`, fixando o valor do atributo `plataforma` e permitindo a inclusão de comportamentos específicos para cada ambiente (ex: verificar compatibilidade).
    * **Conceitos POO:** Demonstra a **Herança Simples** (Geralização/Especialização).

3.  **`Colecao`:**
    * **Responsabilidade:** Agrupar objetos `Jogo` em listas personalizadas nomeadas pelo usuário (ex: "Favoritos").
    * **Conceitos POO:** Representa uma relação de **Composição/Agregação** (`Colecao` *tem* `Jogos`).

4.  **`Catalogo` (Camada de Serviço/Repositório):**
    **Responsabilidade:** Gerenciar a lista completa de jogos, aplicar as regras de negócio (ex: limite de jogos "JOGANDO" ), executar filtros/buscas e coordenar a persistência dos dados (JSON/SQLite).
    * **Conceitos POO:** Atua como um *Gerenciador Central*, isolando a lógica de negócio da interface do usuário.

5.  **`Settings`:**
    **Responsabilidade:** Armazenar as configurações externas e regras de negócio configuráveis, como a meta anual de jogos finalizados.
    * **Conceitos POO:** Ajuda a desacoplar as regras de negócio fixas do código principal, facilitando a manutenção.

```mermaid
%%{init: {'classDiagram': {'layout':'LR'}}}%%
classDiagram

    %% ===============================
    %%        CLASSE BASE
    %% ===============================

    class Jogo {
        -titulo: string
        -genero: string
        -plataforma: string
        -horas_jogadas: float
        -status: string
        -avaliacao: int
        +atualizar_progresso(horas)
        +alterar_status(novo_status)
        +registrar_avaliacao(nota)
        +reiniciar()
        +__str__()
        +__repr__()
        +__eq__()
        +__lt__()
    }

    %% ===============================
    %%       HERANÇA (SIMPLES)
    %% ===============================

    class JogoPC
    class JogoConsole
    class JogoMobile

    JogoPC --|> Jogo
    JogoConsole --|> Jogo
    JogoMobile --|> Jogo


    %% ===============================
    %%        COLEÇÃO DE JOGOS
    %% ===============================

    class Colecao {
        -nome: string
        -jogos: list~Jogo~
        +adicionar_jogo(jogo: Jogo)
        +remover_jogo(jogo: Jogo)
        +listar_jogos()
    }

    Colecao o-- "0..*" Jogo : contém >


    %% ===============================
    %%     CATÁLOGO (SERVIÇO)
    %% ===============================

    class Catalogo {
        -jogos: list~Jogo~
        +adicionar(jogo: Jogo)
        +remover(jogo: Jogo)
        +buscar_por_titulo(texto)
        +filtrar_por_genero(genero)
        +filtrar_por_status(status)
        +ordenar_por_tempo()
        +salvar()
        +carregar()
    }

    Catalogo o-- "0..*" Jogo


    %% ===============================
    %%     CONFIGURAÇÕES (SETTINGS)
    %% ===============================

    class Settings {
        -generos_favoritos: list
        -meta_anual: int
        -plataforma_principal: string
        +carregar()
        +salvar()
    }


    %% ===============================
    %%     USUÁRIO (OPCIONAL)
    %% ===============================
    %% O doc .docx cita o usuário opcionalmente.
    %% Ative se quiser incluir no futuro.

    class Usuario {
        -nome: string
        -colecoes: list~Colecao~
        +criar_colecao(nome)
        +remover_colecao(nome)
    }

    Usuario o-- "0..*" Colecao
