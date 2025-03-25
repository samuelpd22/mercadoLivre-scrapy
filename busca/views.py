from django.shortcuts import render
from .services.services import MercadoLivreScraper

#Simplificamos o codigo, retirando responsabilidade
def buscar_produto(request):
    product = request.GET.get('product', '')

    if product:
        scraper = MercadoLivreScraper()
        resultado = scraper.buscar_produto(product)
        

        if isinstance(resultado, str):
            return render(request, 'erro.html', {'erro': resultado})

        return render(request, 'resultados.html', {
            'product': product,
            'produtos': resultado
        })

    return render(request, 'busca.html')
