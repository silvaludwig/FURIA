import requests
from bs4 import BeautifulSoup


def get_elenco_furia():
    url = "https://www.hltv.org/team/8297/furia"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        jogadores = []
        for div in soup.select(".bodyshot-team a"):
            nome = div["href"].split("/")[-1]
            nome_formatado = nome.replace("-", " ").title()
            jogadores.append(nome_formatado)
        return jogadores
    else:
        print("Erro ao acessar a página:", response.status_code)
        return []


print(get_elenco_furia())
