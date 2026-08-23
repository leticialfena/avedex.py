"""Elementos visuais e menu principal da AveDex."""
import random
from src.avedex.multimidia import tocar_som
from src.avedex.utils import Cor, caixa, colorir, limpar_tela

BANNER_AVEDEX = r"""
___  ____
/   |  _ _____  / __ \___  _ __
/ /| | | | / / _ \/ / / / _ \| |/_/
/ ___ | | |/ / __/ /_/ / __/> <
/_/  |_||___/\___/_____/\___/_/|_|
"""

# Troque para True caso queira reproduzir um som curto na abertura.
TOCAR_SOM_NA_ABERTURA = False

OPCOES_MENU = [
    "1 Listar aves",
    "2 Buscar ave",
    "3 Ave aleatória",
    "4 Ver detalhes de uma ave",
    "5 Comparar duas aves",
    "6 Batalha AveDex",
    "7 Visualizar imagem de uma ave",
    "8 Tocar som de uma ave",
    "9 Verificar ambiente",
    "10 Créditos e fontes",
    "0 Sair",
]


def escolher_ave_com_som(aves):
    """Sorteia uma ave que possua URL de som."""
    aves_com_som = [
        ave
        for ave in aves
        if str(ave.get("midia", {}).get("som_url", "")).strip()
    ]
    if not aves_com_som:
        return None
    return random.choice(aves_com_som)


def abertura(aves):
    """Exibe a abertura visual e, opcionalmente, um som curto."""
    limpar_tela()
    print(colorir(BANNER_AVEDEX, Cor.CIANO))
    caixa(
        "CATÁLOGO INTERATIVO DE AVES",
        [
            f"Total de aves carregadas: {len(aves)}",
            "Explore detalhes, comparação, batalha, imagens e sons.",
        ],
        Cor.CIANO,
    )

    if TOCAR_SOM_NA_ABERTURA:
        ave_som = escolher_ave_com_som(aves)
        if ave_som is not None:
            print()
            print(
                colorir(
                    f"Som de abertura: {ave_som.get('nome_popular')}",
                    Cor.CINZA,
                )
            )
            tocar_som(
                ave_som,
                duracao_segundos=3,
                mostrar_mensagem=False,
            )


def exibir_menu_principal():
    """Exibe todas as opções da versão final da AveDex."""
    caixa("MENU PRINCIPAL", OPCOES_MENU, Cor.AZUL)
