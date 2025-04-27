from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


def teste_de_funcao():
    return "testando função de busca de próximo jogo"


def ultimos_jogos():
    try:
        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")
        sleep(2)  # Espera carregar

        resultados = []
        for i in range(1, 4):  # Pega os 3 últimos jogos
            try:
                # Extrai todos os dados de uma vez
                jogo = navegador.find_element(
                    By.XPATH, f'//*[@id="matchesBox"]/table/tbody[1]/tr[{i}]'
                )

                data = jogo.find_element(By.XPATH, "./td[1]/span").text
                time1 = jogo.find_element(By.XPATH, "./td[2]/div[1]/a").text
                time2 = jogo.find_element(By.XPATH, "./td[2]/div[3]/a").text
                placar = jogo.find_element(By.XPATH, "./td[2]/div[2]").text.replace(
                    "\n", " "
                )

                resultados.append(f"📅 {data}:\n {time1} {placar} {time2}")
            except Exception as e:
                return f"Erro ao extrair jogo {i}: {str(e)}"
                continue

        resposta = (
            "📊 Últimos Jogos:\n" + "\n".join(resultados)
            if resultados
            else "❌ Nenhum resultado recente"
        )

        return resposta.replace("\n", "<br>")

    except Exception as e:
        return f"❌ Erro ao buscar resultados: {str(e)}"
    finally:
        if "navegador" in locals():
            navegador.quit()


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

        return resposta.replace("\n", "<br>")

    except Exception as e:
        return f"❌ Erro ao buscar elenco: {str(e)}"

    finally:
        if "navegador" in locals():
            navegador.quit()


def proximos_jogos():
    try:
        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")

        prox_jogo = navegador.find_element(
            By.XPATH, '//*[@id="matchesBox"]/div[3]/span'
        ).text

        return f"🔥 Próximo Jogo:\n{prox_jogo}"

    except Exception as e:
        return f"❌ Erro ao buscar jogos: {str(e)}"
    finally:
        if "navegador" in locals():
            navegador.quit()
