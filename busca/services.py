import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from busca.exceptions.exceptions import ScrapingError, SeleniumElementNotFoundError, SeleniumTimeoutError, SeleniumWebDriverError
from .models import Produto


class MercadoLivreScraper:

    #__INIT__ -> Construtor de -> MercadoLivreScraper
    def __init__(self, headless=True): # Define por Default Headless=true
        
        try:
            chrome_options = webdriver.ChromeOptions()
            if headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-notifications')

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        except Exception as e:
            raise SeleniumWebDriverError(f"Erro ao iniciar WebDriver: {str(e)}")
        


    def buscar_produto(self, product):
        try:
            self.driver.get("https://www.mercadolivre.com.br/")
            
            try:
                #Vai buscar o INPUT de pesquisar
                pesquisar = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@class="nav-search-input"]'))
                )
                pesquisar.send_keys(product + Keys.RETURN)

            except Exception:
                raise SeleniumWebDriverError("Campo de pesquisa não encontrado")



            try:
            #Vai buscar os "li" contendo os argumentos 
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//li[@class="ui-search-layout__item"]'))
                )
            except Exception:
                raise SeleniumWebDriverError("Tempo de espera excedido ao buscar lista de produtos")


            #Rola para baixo 3 vezes, para que carregue as imagens
            for _ in range(3):
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(2)

            #Vai buscar por 10 elementos que contenham a Class Abaixo
            produtos = self.driver.find_elements(By.XPATH, '//li[@class="ui-search-layout__item"]')[:10]

            lista_produtos = []
            
            for produto in produtos:
                try:
                    dados = {
                        'imagem': produto.find_element(By.XPATH, './/img').get_attribute('src') 
                        if produto.find_elements(By.XPATH, './/img') else None,

                        'nome': produto.find_element(By.XPATH, './/*[contains(@class, "poly-component__title")]').text,

                        'preco_original': produto.find_element(
                            By.XPATH, './/s//span[contains(@class, "andes-money-amount__fraction")]'
                        ).text if produto.find_elements(
                            By.XPATH, './/s//*[contains(@class, "andes-money-amount__fraction")]'
                        ) else 'Não disponível',

                        'preco': produto.find_element(
                            By.XPATH, './/span[contains(@class, "andes-money-amount") and not(parent::s)]//span[contains(@class, "andes-money-amount__fraction")]'
                        ).text if produto.find_elements(
                            By.XPATH, './/*[contains(@class, "andes-money-amount") and not(parent::s)]//span[contains(@class, "andes-money-amount__fraction")]'
                        ) else 'Não informado',

                        'parcelamento': produto.find_element(
                            By.XPATH, './/span[contains(@class, "poly-price__installments")]'
                        ).text if produto.find_elements(
                            By.XPATH, './/*[contains(@class, "poly-price__installments")]') else 'Não informado',

                        'desconto': produto.find_element(
                            By.XPATH, './/span[contains(text(), "%")]'
                        ).text if produto.find_elements(
                            By.XPATH, './/*[contains(text(), "%")]'
                        ) else 'Sem desconto',

                        'link': produto.find_element(By.XPATH, './/a').get_attribute('href') 
                        if produto.find_elements(By.XPATH, './/a') else 'Link indisponível',

                        'tipo_entrega': 'Full' if produto.find_elements(
                            By.XPATH, './/span[contains(@class, "poly-component__shipped-from")]') else 'Normal',

                        'frete_gratis': 'Sim' if produto.find_elements(
                            By.XPATH, './/div[contains(@class, "poly-component__shipping")]') else 'Não'
                    }

                    lista_produtos.append(dados)
                    Produto.objects.create(**dados)

                except Exception as e:
                    raise ScrapingError(f"Erro ao coletar dados de um produto: {str(e)}")

            return lista_produtos

        except SeleniumElementNotFoundError as e:
            print(f"Erro: {str(e)}")
            return []
        
        except SeleniumTimeoutError  as e:
            print(f"Erro: {str(e)}")
            return []
        
        except ScrapingError  as e:
            print(f"Erro durante o scraping: {str(e)}")
            return []
        
        except Exception as e:
            raise SeleniumWebDriverError(f"Erro inesperado ao buscar produto:{str(e)} ")
        


        finally:
            self.driver.quit()
