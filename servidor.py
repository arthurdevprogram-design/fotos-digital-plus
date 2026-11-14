import os

import requests
from mcp.server.fastmcp import FastMCP

# A chave fica guardada no servidor (variável de ambiente), nunca no código.
PIXABAY_KEY = os.environ["PIXABAY_API_KEY"]

mcp = FastMCP(
    "fotos-digital-plus",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "8000")),
)


@mcp.tool()
def buscar_foto(termo: str, orientacao: str = "vertical", quantidade: int = 5) -> list[dict]:
    """Busca fotos reais no banco do Pixabay.

    termo: o que procurar, em português ou inglês (ex.: "consulta online", "médico sorrindo").
    orientacao: "vertical" (feed 4:5 ou stories) ou "horizontal".
    quantidade: de 3 a 20 fotos.
    Retorna o link direto da imagem (link_imagem) e a página original (pagina).
    """
    params = {
        "key": PIXABAY_KEY,
        "q": termo,
        "lang": "pt",
        "image_type": "photo",
        "safesearch": "true",
        "orientation": "vertical" if orientacao == "vertical" else "horizontal",
        "per_page": max(3, min(quantidade, 20)),
    }
    resposta = requests.get("https://pixabay.com/api/", params=params, timeout=15)
    resposta.raise_for_status()
    fotos = resposta.json().get("hits", [])
    return [
        {
            "id": foto["id"],
            "link_imagem": foto["largeImageURL"],
            "pagina": foto["pageURL"],
            "autor": foto["user"],
        }
        for foto in fotos
    ]


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
