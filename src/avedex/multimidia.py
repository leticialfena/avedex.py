import time

from pathlib import Path
from urllib.parse import urlparse

from src.avedex.utils import mensagem_aviso


CAMINHO_PROJETO = Path(__file__).resolve().parents[2]

PASTA_CACHE = CAMINHO_PROJETO / "cache_midias"

EXTENSOES_PADRAO = {
    "imagem": ".jpg",
    "som": ".mp3",
}

EXTENSOES_PERMITIDAS = {
    "imagem": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "som": {".mp3", ".wav", ".ogg"},
}


def obter_url_midia(ave, tipo):
    midia = ave.get("midia", {})

    if not isinstance(midia, dict):
        return ""

    if tipo == "imagem":
        campo = "imagem_url"
    else:
        campo = "som_url"

    return str(
        midia.get(campo, "")
    ).strip()


def descobrir_extensao(url, tipo):
    caminho_url = urlparse(url).path

    extensao = Path(
        caminho_url
    ).suffix.lower()

    if extensao in EXTENSOES_PERMITIDAS[tipo]:
        return extensao

    return EXTENSOES_PADRAO[tipo]


def criar_caminho_cache(ave, tipo, url):
    nome = ave.get(
        "slug",
        ave.get("nome_popular", "ave")
    )

    nome = str(nome).lower().replace(" ", "-")

    extensao = descobrir_extensao(
        url,
        tipo
    )

    return (
        PASTA_CACHE
        / f"{nome}_{tipo}{extensao}"
    )


def baixar_arquivo(url, caminho_destino):
    try:
        import requests
    except ImportError:
        mensagem_aviso(
            "A biblioteca requests não está instalada."
        )
        return False

    try:
        caminho_destino.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        resposta = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": "AveDex/1.0 (projeto academico)"
            }
        )

        resposta.raise_for_status()

        caminho_destino.write_bytes(
            resposta.content
        )

        return True

    except requests.RequestException as erro:
        mensagem_aviso(
            f"Não foi possível baixar a mídia: {erro}"
        )
        return False

def obter_arquivo_midia(ave, tipo):
    url = obter_url_midia(ave, tipo)

    if not url:
        mensagem_aviso(
            f"Não há URL de {tipo} cadastrada para esta ave."
        )
        return None

    caminho_cache = criar_caminho_cache(
        ave,
        tipo,
        url
    )

    if caminho_cache.exists():
        return caminho_cache

    sucesso = baixar_arquivo(
        url,
        caminho_cache
    )

    if not sucesso:
        return None

    return caminho_cache

def visualizar_imagem(ave):
    caminho = obter_arquivo_midia(
        ave,
        "imagem"
    )

    if caminho is None:
        return

    try:
        from term_image.image import from_file
    except ImportError:
        mensagem_aviso(
            "A biblioteca term-image não está instalada."
        )
        mensagem_aviso(
            f"A imagem foi salva em: {caminho}"
        )
        return

    try:
        imagem = from_file(
            str(caminho)
        )

        print(imagem)

    except Exception as erro:
        mensagem_aviso(
            "O terminal não conseguiu exibir a imagem."
        )

        mensagem_aviso(
            f"Abra o arquivo manualmente: {caminho}"
        )

        mensagem_aviso(str(erro))

def tocar_som(
    ave,
    duracao_segundos=None,
    mostrar_mensagem=True
):
    if mostrar_mensagem:
        print("\nSOM DA AVE")
        print("=" * 50)

    caminho = obter_arquivo_midia(
        ave,
        "som"
    )

    if caminho is None:
        return

    try:
        import pygame
    except ImportError:
        mensagem_aviso(
            "A biblioteca pygame não está instalada."
        )
        mensagem_aviso(
            f"O som foi salvo em: {caminho}"
        )
        return

    try:
        pygame.mixer.init()

        pygame.mixer.music.load(
            str(caminho)
        )

        pygame.mixer.music.play()

        if mostrar_mensagem:
            print(
                f"Reproduzindo o som de "
                f"{ave.get('nome_popular', 'ave')}."
            )

        inicio = time.monotonic()

        while pygame.mixer.music.get_busy():
            if (
                duracao_segundos is not None
                and time.monotonic() - inicio
                >= duracao_segundos
            ):
                pygame.mixer.music.stop()
                break

            time.sleep(0.1)

    except Exception as erro:
        mensagem_aviso(
            "Não foi possível reproduzir o som."
        )
        mensagem_aviso(str(erro))