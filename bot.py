import os
import json
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SEEN_FILE = "seen_ads.json"

URLS = [
    "https://www.zapimoveis.com.br/aluguel/imoveis/rj+rio-de-janeiro/2-quartos/?quartos=2%2C3%2C4&vagas=1%2C2%2C3%2C4&precoTotal=true&precoMaximo=3500&areaMinima=60",
    "https://www.vivareal.com.br/aluguel/rj/rio-de-janeiro/?quartos=2%2C3%2C4&vagas=1%2C2%2C3%2C4&precoTotal=true&precoMaximo=3500&areaMinima=60",
    "https://www.quintoandar.com.br/alugar/imovel/rio-de-janeiro-rj-brasil/de-500-a-3500-reais/2-quartos/1-2-3-vagas/de-60-a-1000-m2"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_seen(ids):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(ids), f)


def send_telegram(msg):
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg,
            "disable_web_page_preview": False
        }
    )

    print("STATUS TELEGRAM:", r.status_code)
    print("RESPOSTA TELEGRAM:", r.text)


print("================================")
print("BOT INICIADO")
print("================================")

seen = load_seen()
new_seen = set(seen)

print("ANUNCIOS JA VISTOS:", len(seen))

novos = []

for url in URLS:

    print("\nPROCESSANDO:")
    print(url)

    try:
        html = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        ).text

        print("HTML RECEBIDO:", len(html), "caracteres")

        soup = BeautifulSoup(html, "html.parser")

        links = soup.find_all("a", href=True)

        print("LINKS ENCONTRADOS:", len(links))

        encontrados_nessa_url = 0

        for link in links:

            href = link["href"]

            if "/imovel/" not in href and "/imoveis/" not in href:
                continue

            if href.startswith("/"):
                href = "https://www.zapimoveis.com.br" + href

            anuncio_id = href

            encontrados_nessa_url += 1

            if anuncio_id not in seen:
                novos.append(href)
                new_seen.add(anuncio_id)

        print("ANUNCIOS VALIDOS:", encontrados_nessa_url)

    except Exception as e:
        print("ERRO:", str(e))

print("\n================================")
print("NOVOS ENCONTRADOS:", len(novos))
print("================================")

if novos:

    mensagem = "🏠 NOVOS IMÓVEIS ENCONTRADOS\n\n"

    for item in novos[:20]:
        mensagem += f"{item}\n\n"

    send_telegram(mensagem)

else:
    print("NENHUM IMOVEL NOVO ENCONTRADO")

save_seen(new_seen)

print("FIM DO PROCESSAMENTO")
