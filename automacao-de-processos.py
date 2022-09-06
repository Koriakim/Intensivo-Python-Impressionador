from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

navegador = webdriver.Chrome()


# Passo 1: Pegar a cotação do Dólar
# Comando ".get(<site>)" realiza o acesso à página.
navegador.get("https://www.google.com/")
navegador.find_element(
    By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação do dólar")
navegador.find_element(
    By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
cotacao_dolar = navegador.find_element(
    By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")

print(f"Dolar: R${cotacao_dolar}")

# Passo 2: Pegar a cotação do Euro
navegador.get("https://www.google.com/")
navegador.find_element(
    By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação do euro")
navegador.find_element(
    By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
cotacao_euro = navegador.find_element(
    By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")

print(f"Euro: R${cotacao_euro}")

# Passo 3: Pegar a cotação do Ouro

navegador.get("https://www.melhorcambio.com/ouro-hoje")
cotacao_ouro = navegador.find_element(
    By.XPATH, '//*[@id="comercial"]').get_attribute("value")
cotacao_ouro = cotacao_ouro.replace(",", ".")

print(f"Ouro: R${cotacao_ouro}")

navegador.quit()

# Passo 4: Importar a lista de produtos
print(' ')
tabela = pd.read_excel("Produtos.xlsx")
print(tabela)

# Passo 5: Atualizar as colunas com a cotação atualizada
print(' ')
tabela.loc[tabela["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)
tabela.loc[tabela["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)
tabela.loc[tabela["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)
print(tabela)

# Recalcular valores
print(' ')
tabela["Preço de Compra"] = tabela["Preço Original"] * tabela["Cotação"]
tabela["Preço de Venda"] = tabela["Preço de Compra"] * tabela["Margem"]
print(tabela)

# Passo 6: Exportar o resultado para uma planilha Excel

tabela.to_excel("Produtos Novo.xlsx", index=False)
