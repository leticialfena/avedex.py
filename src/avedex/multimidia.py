"""Download, cache, visualização de imagens e reprodução de sons."""
import time
from pathlib import Path
from urllib.parse import urlparse
from src.avedex.utils import (
    mensagem_aviso,
    mensagem_erro,
    mensagem_sucesso,
    slugificar,
    titulo,
)

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
    """Devolve a URL de imagem ou som cadastrada para uma ave."""
    midia = ave.get("midia", {})
    if not isinstance(midia, dict):
        return ""
    campo = "imagem_url" if tipo == "imagem" else "som_url"
    return str(midia.get(campo, "")).strip()


def descobrir_extensao(url, tipo):
    """Tenta obter uma extensão segura a partir da URL."""
    caminho_url = urlparse(url).path
    extensao = Path(caminho_url).suffix.lower()
    if extensao in EXTENSOES_PERMITIDAS[tipo]:
        return extensao
    return EXTENSOES_PADRAO[tipo]


def criar_caminho_cache(ave, tipo, url):
    """Monta o caminho local usado para armazenar a mídia."""
    slug = ave.get("slug") or slugificar(ave.get("nome_popular", "ave"))
    extensao = descobrir_extensao(url, tipo)
    return PASTA_CACHE / f"{slug}_{tipo}{extensao}"


def baixar_arquivo(url, caminho_destino):
    """Baixa um arquivo e devolve True quando a operação funciona."""
    try:
        import requests
    except ImportError:
        mensagem_aviso("A biblioteca requests não está instalada.")
        mensagem_aviso("Execute: pip install -r requirements.txt")
        return False

    try:
        caminho_destino.parent.mkdir(parents=True, exist_ok=True)
        resposta = requests.get(url, timeout=20)
        resposta.raise_for_status()
        caminho_destino.write_bytes(resposta.content)
        return True
    except requests.RequestException as erro:
        mensagem_erro(f"Não foi possível baixar a mídia: {erro}")
        return False
    except OSError as erro:
        mensagem_erro(f"Não foi possível salvar a mídia: {erro}")
        return False


def obter_arquivo_midia(ave, tipo):
    """Usa o cache ou baixa a mídia e devolve seu caminho local."""
    url = obter_url_midia(ave, tipo)
    if url == "":
        mensagem_aviso(f"Esta ave não possui URL de {tipo} cadastrada.")
        return None

    caminho = criar_caminho_cache(ave, tipo, url)
    if caminho.exists():
        mensagem_sucesso(f"{tipo.capitalize()} encontrada no cache local.")
        return caminho

    mensagem_aviso(f"{tipo.capitalize()} ainda não está no cache. Baixando...")
    if baixar_arquivo(url, caminho):
        mensagem_sucesso(f"{tipo.capitalize()} salva em {caminho.name}.")
        return caminho

    return None


def visualizar_imagem(ave):
    """Baixa, armazena e tenta mostrar a imagem de uma ave no terminal."""
    titulo("IMAGEM DA AVE")
    caminho = obter_arquivo_midia(ave, "imagem")
    if caminho is None:
        return

    try:
        from term_image.image import from_file
    except ImportError:
        mensagem_aviso("A biblioteca term-image não está instalada.")
        mensagem_aviso(f"A imagem foi salva em: {caminho}")
        return

    try:
        imagem = from_file(str(caminho))
        print(imagem)
    except Exception as erro:
        mensagem_aviso("O terminal não conseguiu exibir a imagem.")
        mensagem_aviso(f"Abra o arquivo manualmente: {caminho}")
        mensagem_erro(str(erro))


def tocar_som(ave, duracao_segundos=None, mostrar_mensagem=True):
    """Baixa, armazena e tenta reproduzir o som de uma ave."""
    if mostrar_mensagem:
        titulo("SOM DA AVE")

    caminho = obter_arquivo_midia(ave, "som")
    if caminho is None:
        return

    try:
        import pygame
    except ImportError:
        mensagem_aviso("A biblioteca pygame não está instalada.")
        mensagem_aviso(f"O som foi salvo em: {caminho}")
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(str(caminho))
        pygame.mixer.music.play()

        if mostrar_mensagem:
            mensagem_sucesso(
                f"Reproduzindo o som de {ave.get('nome_popular', 'ave')}."
            )

        inicio = time.monotonic()
        while pygame.mixer.music.get_busy():
            if (
                duracao_segundos is not None
                and time.monotonic() - inicio >= duracao_segundos
            ):
                pygame.mixer.music.stop()
                break
            time.sleep(0.1)

    except pygame.error as erro:
        mensagem_erro(f"Não foi possível reproduzir o som: {erro}")
        mensagem_aviso(f"Abra o arquivo manualmente: {caminho}")
    finally:
        if pygame.mixer.get_init():
            try:
                pygame.mixer.music.unload()
            except pygame.error:
                pass
            pygame.mixer.quit()
