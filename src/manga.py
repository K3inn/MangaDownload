import requests
import json
from bs4 import BeautifulSoup

class Mangayabu:
    def __init__(self):
        pass

    def __Request_Anime(self, url):
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta
        return -1

    def Pesquisar_anime(self, nome):
        nome = nome.replace(" ", '-')
        base_url_pesqusia = "https://mangayabu.top/manga/{}/page/14/"

        html_principal = self.__Request_Anime(base_url_pesqusia.format(nome))
        if html_principal != -1:
            modificador_html = BeautifulSoup(html_principal.text, 'html.parser')
            cadeia_de_cap = modificador_html.find_all("script", { "id" : "manga-info" })

            cadeia_de_cap_str = str(cadeia_de_cap[0])
            string_tratada = cadeia_de_cap_str[57:len(cadeia_de_cap_str)-9]
            json_obj = json.loads(string_tratada)
            print("[ ENGINE ] - Mangá encontrado")
            return json_obj
        else:
            print("[ ENGINE ] - Mangá não encontrado")
            return -1
    
    def Download(self, url, caminho):
        data_img = {}
        html_principal = self.__Request_Anime(url)

        if html_principal != -1:
            try:
                modificador_html = BeautifulSoup(html_principal.text, 'html.parser')
                cadeia_de_imagens = modificador_html.find_all("div", {"class" : "section table-of-contents"})
                
                modificador_html_2 = BeautifulSoup(str(cadeia_de_imagens[0]), 'html.parser')
                imagens = modificador_html_2.find_all("img", {'class':'lazy'})

                for img in imagens:
                    data_img[img.get('id')] = img.get('data-src')
            
                for i in data_img:
                    img = self.__Request_Anime(data_img[i])
                    with open(caminho+"/"+i+".jpeg", 'wb') as arquivo:
                        arquivo.write(img.content)
                print("[ ENGINE ] - Baixado com sucesso")
                return 0
            except Exception as erro:
                print(f"[ ENGINE ] {str(erro)}")
        else:
            return -1

    def GetCapitulo(self, capitulo, data):
        for cap in data["allposts"]:
            if(cap['num'] == str(capitulo)):
                return cap['id']
    
    def GetNome(self, data):
        return data['chapter_name']
    
    def GetQtdCapitulos(self, data):
        return data['chapters']
    
    def GetDescricao(self, data):
        return data['description']
    
    def GetGenero(self, data):
        return data['genres']
    
    def GetCapa(self, data):
        return data['cover']

    def Printar(self, data):
        print(json.dumps(data, indent=4))