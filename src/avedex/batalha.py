"""Batalha didática entre duas aves da AveDex."""
from src.avedex.catalogo import escolher_ave
from src.avedex.utils import (
    Cor,
    colorir,
    mensagem_aviso,
    subtitulo,
    titulo,
    valor_ou_indisponivel,
)

ATRIBUTOS_BATALHA = {
    "1": {
        "campo": "comprimento_cm",
        "nome": "Comprimento",
        "unidade": "cm",
        "explicacao": "Nesta rodada, vence a ave com maior comprimento.",
    },
    "2": {
        "campo": "peso_g",
        "nome": "Peso médio",
        "unidade": "g",
        "explicacao": "Nesta rodada, vence a ave com maior peso médio.",
    },
    "3": {
        "campo": "indice_conservacao",
        "nome": "Índice de conservação",
        "unidade": "",
        "explicacao": (
            "Nesta rodada, vence o maior índice, que representa maior nível "
            "de atenção para conservação."
        ),
    },
}


def escolher_atributo_batalha():
    """Mostra os atributos disponíveis e devolve a configuração escolhida."""
    subtitulo("Escolha o atributo da batalha")
    print("1 - Comprimento")
    print("2 - Peso médio")
    print("3 - Índice de conservação")
    print("0 - Cancelar")

    opcao = input("Opção: ").strip()
    if opcao == "0":
        return None

    atributo = ATRIBUTOS_BATALHA.get(opcao)
    if atributo is None:
        mensagem_aviso("Atributo inválido.")
        return None

    return atributo


def obter_valor_numerico(ave, campo):
    """Devolve um campo numérico ou None quando o dado não pode ser usado."""
    valor = ave.get(campo)
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return None
    return valor


def exibir_participante(ave, valor, unidade):
    """Exibe uma ave e o valor usado na rodada."""
    nome = valor_ou_indisponivel(ave.get("nome_popular"))
    valor_formatado = valor_ou_indisponivel(valor, unidade)
    print(f"- {nome}: {valor_formatado}")


def batalha_avedex(aves):
    """Permite escolher duas aves e realizar uma batalha por atributo."""
    titulo("BATALHA AVEDEX", Cor.ROXO)

    ave_1 = escolher_ave(aves, "Escolha a primeira ave da batalha")
    if ave_1 is None:
        return

    ave_2 = escolher_ave(aves, "Escolha a segunda ave da batalha")
    if ave_2 is None:
        return

    if ave_1.get("id") == ave_2.get("id"):
        mensagem_aviso("Escolha duas aves diferentes para a batalha.")
        return

    atributo = escolher_atributo_batalha()
    if atributo is None:
        return

    campo = atributo["campo"]
    valor_1 = obter_valor_numerico(ave_1, campo)
    valor_2 = obter_valor_numerico(ave_2, campo)

    if valor_1 is None or valor_2 is None:
        mensagem_aviso("Uma das aves não possui um valor numérico válido.")
        return

    titulo(f"RODADA: {atributo['nome'].upper()}", Cor.ROXO)
    print(atributo["explicacao"])
    print()

    exibir_participante(ave_1, valor_1, atributo["unidade"])
    exibir_participante(ave_2, valor_2, atributo["unidade"])
    print()

    if valor_1 == valor_2:
        print(colorir("Resultado: empate!", Cor.AMARELO))
        return

    vencedora = ave_1 if valor_1 > valor_2 else ave_2
    nome_vencedora = vencedora.get("nome_popular", "Ave")
    print(colorir(f"Vencedora da rodada: {nome_vencedora}!", Cor.VERDE))
