


class SeleniumTimeoutError(Exception):
    """Levantada quando o tempo de espera do Selenium é excedido."""
    def __init__(self, mensagem ,*args):
        super().__init__(mensagem, *args)

class SeleniumElementNotFoundError(Exception):
    """Levantada quando um elemento não é encontrado na página."""
    def __init__(self, mensagem,*args):
        super().__init__(mensagem, *args)

class SeleniumWebDriverError(Exception):
    """Levantada quando ocorre um erro com o WebDriver."""
    def __init__(self, mensagem, *args):
        super().__init__(mensagem, *args)

class ScrapingError(Exception):
    """Levantada quando ocorre um erro durante o processo de scraping."""
    def __init__(self, mensagem, *args):
        super().__init__(mensagem, *args) 