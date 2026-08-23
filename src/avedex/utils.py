"""Funções auxiliares compartilhadas pela AveDex."""
import os
import sys
import unicodedata

# Largura padrão usada em títulos, linhas e caixas.
LARGURA_TELA = 78

# Permite desativar as cores caso o terminal não ofereça suporte adequado.
USAR_CORES = True


class Cor:
    """Códigos ANSI usados na interface do terminal."""
    RESET = "\033[0m"
    NEGRITO = "\033[1m"
    VERDE = "\033[92m"
    AZUL = "\033[94m"
    CIANO = "\033[96m"
    AMARELO = "\033[93m"
    VERMELHO = "\033[91m"
    ROXO = "\033[95m"
    CINZA = "\033[90m"


def colorir(texto, cor):
    """Aplica uma cor ANSI ao texto quando as cores estão habilitadas."""
    if not USAR_CORES:
        return str(texto)
    return f"{cor}{texto}{Cor.RESET}"


def limpar_tela():
    """Limpa a tela quando a aplicação está sendo usada em um terminal real."""
    if not sys.stdout.isatty():
        return
    os.system("cls" if os.name == "nt" else "clear")


def linha(caractere="=", largura=LARGURA_TELA):
    """Retorna uma linha formada pela repetição de um caractere."""
    return caractere * largura


def titulo(texto, cor=Cor.CIANO):
    """Exibe um título padronizado."""
    print()
    print(colorir(linha("="), cor))
    print(colorir(texto, cor))
    print(colorir(linha("="), cor))


def subtitulo(texto):
    """Exibe um subtítulo com uma linha inferior."""
    print()
    print(colorir(texto, Cor.NEGRITO))
    print(colorir(linha("-", len(texto)), Cor.CINZA))


def mensagem_sucesso(texto):
    """Exibe uma mensagem positiva."""
    print(colorir(f"[OK] {texto}", Cor.VERDE))


def mensagem_aviso(texto):
    """Exibe uma mensagem de atenção."""
    print(colorir(f"[AVISO] {texto}", Cor.AMARELO))


def mensagem_erro(texto):
    """Exibe uma mensagem de erro."""
    print(colorir(f"[ERRO] {texto}", Cor.VERMELHO))


def pausar():
    """Pausa o fluxo para que o usuário consiga ler a tela."""
    input("\nPressione ENTER para continuar...")


def normalizar_texto(texto):
    """Converte texto para minúsculas e remove acentos e espaços externos."""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )
 


def slugificar(texto):
    """Transforma um texto em um nome simples e seguro para arquivos."""
    texto = normalizar_texto(texto)
    caracteres = []
    for caractere in texto:
        if caractere.isalnum():
            caracteres.append(caractere)
        elif caractere in [" ", "-", "_"]:
            caracteres.append("_")
    slug = "".join(caracteres).strip("_")
    return slug or "arquivo"


def valor_ou_indisponivel(valor, unidade=""):
    """Formata um valor, tratando dados ausentes e unidades opcionais."""
    if valor is None or valor == "":
        return "Não informado"
    if unidade:
        return f"{valor} {unidade}"
    return str(valor)


def cortar_texto(texto, tamanho=25):
    """Limita um texto para preservar o alinhamento de tabelas."""
    if texto is None or str(texto).strip() == "":
        return "Não informado"
    texto = str(texto).strip()
    if len(texto) <= tamanho:
        return texto
    return texto[: tamanho - 3] + "..."


def caixa(titulo_caixa, linhas, cor=Cor.CIANO):
    """Exibe um conjunto de linhas dentro de uma caixa visual."""
    largura = LARGURA_TELA - 4
    print(colorir("+" + "-" * (largura + 2) + "+", cor))
    print(colorir(f"| {titulo_caixa.center(largura)} |", cor))
    print(colorir("+" + "-" * (largura + 2) + "+", cor))
    for linha_texto in linhas:
        texto = str(linha_texto)
        if len(texto) > largura:
            texto = texto[: largura - 3] + "..."
        print(colorir(f"| {texto.ljust(largura)} |", cor))
    print(colorir("+" + "-" * (largura + 2) + "+", cor))


def ler_comando_paginacao():
    """Lê um comando de navegação ou um ID durante a paginação."""
    print()
    print("ENTER - próxima página")
    print("p - página anterior")
    print("q - sair")
    print("ID - escolher uma ave")
    return input("Comando: ").strip().lower()


def paginar_aves(aves, titulo_lista="AVES", tamanho_pagina=10):
    """Mostra aves por páginas e devolve a ave escolhida pelo ID."""
    if not aves:
        mensagem_aviso("Nenhuma ave disponível.")
        return None

    pagina = 0
    while True:
        limpar_tela()
        total = len(aves)
        inicio = pagina * tamanho_pagina
        fim = inicio + tamanho_pagina
        aves_pagina = aves[inicio:fim]
        total_paginas = (total + tamanho_pagina - 1) // tamanho_pagina
        titulo(f"{titulo_lista} - página {pagina + 1} de {total_paginas}")
        for ave in aves_pagina:
            identificador = ave.get("id", "-")
            nome = ave.get("nome_popular", "Nome não informado")
            familia = ave.get("familia", "-")
            print(f"{str(identificador):>3} - {nome} ({familia})")

        print()
        print(f"Mostrando {inicio + 1} a {min(fim, total)} de {total} aves.")

        comando = ler_comando_paginacao()

        if comando == "":
            if fim < total:
                pagina += 1
            else:
                mensagem_aviso("Você já está na última página.")
                pausar()

        elif comando == "p":
            if pagina > 0:
                pagina -= 1
            else:
                mensagem_aviso("Você já está na primeira página.")
                pausar()

        elif comando == "q":
            return None

        elif comando.isdigit():
            for ave in aves:
                if str(ave.get("id")) == comando:
                    return ave
            mensagem_aviso("ID não encontrado.")
            pausar()

        else:
            mensagem_aviso("Comando inválido.")
            pausar()
