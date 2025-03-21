from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def buscar_produto(request):
    product = request.GET.get('product', '')
    
    if product:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            driver.get("https://www.mercadolivre.com.br/")
            search = driver.find_element(By.XPATH, '//input[@class="nav-search-input"]')
            search.send_keys(product)
            search.send_keys(Keys.RETURN)
            
            titulos = [titulo.text for titulo in driver.find_elements(
                By.XPATH, '//a[@class="poly-component__title"]')[:10]]
            
            return render(request, 'resultados.html', {
                'product': product,
                'titulos': titulos
            })
            
        except Exception as e:
            return render(request, 'erro.html', {'erro': str(e)})
            
        finally:
            driver.quit()
    
    return render(request, 'busca.html')
