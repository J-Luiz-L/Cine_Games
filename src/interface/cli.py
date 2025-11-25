import argparse
from pathlib import Path
from ..serviços.catalogo_service import CatalogoService
from ..modelos.jogo_pc import JogoPC
from ..modelos.jogo_console import JogoConsole
from ..modelos.jogo_mobile import JogoMobile

DB_PATH = Path(__file__).parent.parent.parent / "data" / "catalogo.json"

def main():
    parser = argparse.ArgumentParser("Cine Games CLI")
    parser.add_argument("--listar", action="store_true", help="Listar jogos")
    parser.add_argument("--add-pc", nargs=3, metavar=("TITULO","GENERO","REQUISITOS"),
                        help="Adicionar um jogo de PC: TITULO GENERO REQUISITOS")
    parser.add_argument("--add-console", nargs=3, metavar=("TITULO","GENERO","CONSOLE"),
                        help="Adicionar um jogo de Console: TITULO GENERO CONSOLE")
    parser.add_argument("--add-mobile", nargs=3, metavar=("TITULO","GENERO","SO"),
                        help="Adicionar um jogo Mobile: TITULO GENERO SO")
    args = parser.parse_args()

    svc = CatalogoService(caminho=DB_PATH)
    svc.carregar()

    if args.listar:
        for j in svc.listar():
            print(j)
        return

    if args.add_pc:
        titulo, genero, requisitos = args.add_pc
        jogo = JogoPC(titulo=titulo, genero=genero, requisitos=requisitos)
        svc.adicionar(jogo)
        svc.salvar()
        print("Jogo PC adicionado.")
        return

    if args.add_console:
        titulo, genero, console = args.add_console
        jogo = JogoConsole(titulo=titulo, genero=genero, console=console)
        svc.adicionar(jogo)
        svc.salvar()
        print("Jogo Console adicionado.")
        return

    if args.add_mobile:
        titulo, genero, so = args.add_mobile
        jogo = JogoMobile(titulo=titulo, genero=genero, sistema_operacional=so)
        svc.adicionar(jogo)
        svc.salvar()
        print("Jogo Mobile adicionado.")
        return

if __name__ == "__main__":
    main()
