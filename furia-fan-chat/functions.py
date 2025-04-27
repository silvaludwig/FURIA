from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


def teste_de_funcao():
    return "testando função de busca de próximo jogo"


def proximo_jogo(): ...


def status_ao_vivo(): ...


def elenco_furia():
    try:
        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://www.hltv.org/team/8297/furia#tab-rosterBox")
        sleep(2)

        # Coach
        try:
            coach = navegador.find_element(
                By.XPATH,
                '//*[@id="rosterBox"]/div[2]/table/tbody/tr/td[1]/a/div[2]/div',
            ).text
        except Exception:
            coach = "Não identificado"

        # Jogadores
        jogadores = []
        for i in range(1, 6):
            try:
                jogador = navegador.find_element(
                    By.XPATH,
                    f'//*[@id="rosterBox"]/div[4]/table/tbody/tr[{i}]/td[1]/a/div[2]/div',
                ).text
                jogadores.append(jogador)
            except Exception:
                continue

        resposta = (
            f"👥 *Elenco da FURIA*\n"
            f"🎮 *Coach:* {coach}\n"
            f"🟡 *Jogadores:*\n- " + "\n- ".join(jogadores)
            if jogadores
            else "❌ Nenhum jogador encontrado."
        )

        return resposta

    except Exception as e:
        return f"❌ Erro ao buscar elenco: {str(e)}"

    finally:
        if "navegador" in locals():
            navegador.quit()


def ultimos_resultados(): ...
