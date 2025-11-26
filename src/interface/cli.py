import argparse
from pathlib import Path
from src.servicos.catalogo_service import CatalogoService
from src.modelos.jogo_pc import JogoPC
from src.modelos.jogo_console import JogoConsole
from src.modelos.jogo_mobile import JogoMobile

DB_PATH = Path(__file__).parent.parent.parent / "data" / "catalogo.json"

def main():
    parser = argparse.ArgumentParser("Cine Games CLI")
    parser.add_argument("--listar", action="store_true", help="Listar jogos")
    parser.add_argument("--relatorio", action="store_true", help="Gerar relatório inicial (total de jogos e horas jogadas)")
    
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

    if args.relatorio:
        rel = svc.gerar_relatorio_inicial()
        print("\n--- Relatório Inicial ---")
        print(f"Total de jogos cadastrados: {rel['total_jogos']}")
        print(f"Total de horas jogadas: {rel['total_horas_jogadas']:.2f}h")
        print("-------------------------\n")
        return
        
    if args.add_pc:
        titulo, genero, requisitos = args.add_pc
        try:
            jogo = JogoPC(titulo=titulo, genero=genero, requisitos=requisitos)
            svc.adicionar(jogo)
            svc.salvar()
            print(f"Jogo PC '{titulo}' adicionado e salvo.")
        except ValueError as e:
            print(f"ERRO: {e}")
        return

    if args.add_console:
        titulo, genero, console = args.add_console
        try:
            jogo = JogoConsole(titulo=titulo, genero=genero, console=console)
            svc.adicionar(jogo)
            svc.salvar()
            print(f"Jogo Console '{titulo}' adicionado e salvo.")
        except ValueError as e:
            print(f"ERRO: {e}")
        return

    if args.add_mobile:
        titulo, genero, so = args.add_mobile
        try:
            jogo = JogoMobile(titulo=titulo, genero=genero, sistema_operacional=so)
            svc.adicionar(jogo)
            svc.salvar()
            print(f"Jogo Mobile '{titulo}' adicionado e salvo.")
        except ValueError as e:
            print(f"ERRO: {e}")
        return

if __name__ == "__main__":
    main()