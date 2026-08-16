import random

from src.avedex.utils import (
    paginar_aves,
    normalizar_texto,
    mensagem_aviso,
    pausar,
    titulo,
)


def listar_aves(catalogo):
    return paginar_aves(
        catalogo,
        "AVES CADASTRADAS"
    )


def mostrar_ave_aleatoria(catalogo):
    if not catalogo:
        mensagem_aviso(
            "Nenhuma ave disponível para sorteio."
        )
        return

    ave = random.choice(catalogo)

    titulo("AVE ALEATÓRIA")

    print(
        f"Ave sorteada: "
        f"{ave.get('nome_popular', 'Ave')}"
    )

    exibir_detalhes_ave(ave)


def ler_id_ave(mensagem):
    while True:
        entrada = input(mensagem).strip()

        if entrada.isdigit():
            return int(entrada)

        mensagem_aviso("Digite apenas números.")


def buscar_ave_por_id(catalogo, id_procurado):
    for ave in catalogo:
        if ave["id"] == id_procurado:
            return ave

    return None


def buscar_aves(catalogo, termo_busca):
    resultados = []

    termo = normalizar_texto(termo_busca)

    for ave in catalogo:
        campos_busca = [
            ave.get("nome_popular", ""),
            ave.get("nome_cientifico", ""),
            ave.get("familia", ""),
            ave.get("ordem", ""),
            ave.get("dieta_tipo", ""),
        ]

        texto_busca = " ".join(campos_busca)
        texto_busca = normalizar_texto(texto_busca)

        if termo in texto_busca:
            resultados.append(ave)

    return resultados


def exibir_resultados_busca(resultados):
    titulo("RESULTADOS DA BUSCA")

    print(
        f"Foram encontradas "
        f"{len(resultados)} ave(s).\n"
    )

    if len(resultados) == 0:
        print("Nenhuma ave encontrada.")
    else:
        for ave in resultados:
            print(
                f"{ave['id']} - "
                f"{ave['nome_popular']} "
                f"({ave['familia']}, "
                f"{ave['dieta_tipo']})"
            )


def selecionar_resultado_busca(resultados):
    escolha = input(
        "\nDigite o ID para ver detalhes "
        "ou ENTER para voltar: "
    ).strip()

    if escolha == "":
        return

    if not escolha.isdigit():
        mensagem_aviso(
            "Digite apenas números."
        )
        return

    ave_encontrada = buscar_ave_por_id(
        resultados,
        int(escolha)
    )

    if ave_encontrada is None:
        mensagem_aviso(
            "ID não encontrado nos resultados."
        )
    else:
        exibir_detalhes_ave(ave_encontrada)


def tela_busca(catalogo):
    termo = input(
        "Digite parte do nome, família, "
        "ordem ou dieta: "
    ).strip()

    if termo == "":
        mensagem_aviso(
            "Digite algum texto para realizar a busca."
        )
        return

    resultados = buscar_aves(
        catalogo,
        termo
    )

    exibir_resultados_busca(resultados)

    if len(resultados) > 0:
        selecionar_resultado_busca(resultados)


def exibir_detalhes_ave(ave):
    titulo("DETALHES DA AVE")

    print(f"ID: {ave['id']}")
    print(
        f"Nome popular: "
        f"{ave['nome_popular']}"
    )
    print(
        f"Nome científico: "
        f"{ave['nome_cientifico']}"
    )
    print(f"Ordem: {ave.get('ordem', 'Não informado')}")
    print(f"Família: {ave.get('familia', 'Não informado')}")
    print(f"Habitat: {ave['habitat']}")
    print(
        f"Dieta: "
        f"{ave.get('dieta_tipo', 'Não informado')}"
    )
    print(
        f"Alimentação: "
        f"{ave['alimentacao']}"
    )
    print(
        f"Comprimento: "
        f"{ave.get('comprimento_cm', 'Não informado')} cm"
    )
    print(
        f"Peso: "
        f"{ave.get('peso_g', 'Não informado')} g"
    )
    print(
        f"Conservação: "
        f"{ave.get('status_conservacao', 'Não informado')}"
    )
    print(
        f"Curiosidade: "
        f"{ave.get('curiosidade', 'Não informada')}"
    )

    pausar()


def selecionar_ave_por_id(catalogo):
    ave_encontrada = listar_aves(catalogo)

    if ave_encontrada is not None:
        exibir_detalhes_ave(
            ave_encontrada
        )


def escolher_ave(catalogo, mensagem):
    print()
    print(mensagem)

    ave = paginar_aves(
        catalogo,
        "SELECIONE UMA AVE"
    )

    return ave