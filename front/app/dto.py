class DadosDashboardDTO:
    def __init__(self, lista_usuarios, lista_imagens, lista_analises, lista_notas):
        self.lista_usuarios = lista_usuarios
        self.lista_imagens = lista_imagens
        self.lista_analises = lista_analises
        self.lista_notas = lista_notas
        self.quantidade_usuarios = len(lista_usuarios)
        self.quantidade_imagens = len(lista_imagens)
        self.quantidade_analises = len(lista_analises)
        self.quantidade_notas = len(lista_notas)

    def __repr__(self):
        return f"DadosDashboardDTO(lista_usuarios={self.lista_usuarios}, lista_imagens={self.lista_imagens}, lista_analises={self.lista_analises}, lista_notas={self.lista_notas}, quantidade_usuarios={self.quantidade_usuarios}, quantidade_imagens={self.quantidade_imagens}, quantidade_analises={self.quantidade_analises}, quantidade_notas={self.quantidade_notas})"