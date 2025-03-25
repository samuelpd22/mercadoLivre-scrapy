from busca.exceptions.exceptions import ScrapingError
from busca.models import Produto
from busca.scraper.scraper import MercadoLivreScraper

class ScrapingService:

    def __init__(self, headless=True):
        self.scraper = MercadoLivreScraper(headless=headless)

    def realizar_scraping(self, product):
        try:
            # Realiza a busca de produtos no Mercado Livre
            produtos = self.scraper.buscar_produto(product)
            
            if produtos:
                for produto in produtos:
                    # Salva cada produto no banco de dados
                    Produto.objects.create(
                        imagem=produto['imagem'],
                        nome=produto['nome'],
                        preco_original=produto['preco_original'],
                        preco=produto['preco'],
                        parcelamento=produto['parcelamento'],
                        desconto=produto['desconto'],
                        link=produto['link'],
                        tipo_entrega=produto['tipo_entrega'],
                        frete_gratis=produto['frete_gratis']
                    )
                return produtos  # Retorna a lista de produtos coletados
            else:
                return []  # Retorna uma lista vazia se não houver produtos

        except ScrapingError as e:
            print(f"Erro ao realizar o scraping: {str(e)}")
            return []
