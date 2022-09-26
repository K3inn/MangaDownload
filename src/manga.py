import requests
import json
import os
import controlador_json
from bs4 import BeautifulSoup

class Mangayabu:
    def __init__(self):
        pass

    def __Request_Anime(self, url):
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta
        return -1

    def __Salvar_Anime(self, bytes, capitulo, caminho=False):
        for i in bytes:
            img = self.__Request_Anime(bytes[i])
            if(caminho != False):
                caminho_para_salvar = f'{caminho}/{self.GetNome()}_{capitulo}/{i}.jpeg'
                print(caminho)
                print(caminho_para_salvar)
            else:
                caminho_para_salvar = f"{controlador_json.Pegar_diretorio(self.json_obj['chapter_name'])}/{self.json_obj['chapter_name']}_{capitulo}/{i}.jpeg"
                if caminho_para_salvar == 0:
                    caminho_para_salvar = f'./Download_Padrão/{self.GetNome()}_{capitulo}/{i}.jpeg'
            
            os.makedirs(os.path.dirname(caminho_para_salvar), exist_ok=True)
            with open(caminho_para_salvar, 'wb') as arquivo:
                arquivo.write(img.content)

    def Pesquisar_anime(self, nome):
        nome = nome.replace(" ", '-')
        base_url_pesqusia = "https://mangayabu.top/manga/{}/page/14/"

        html_principal = self.__Request_Anime(base_url_pesqusia.format(nome))
        if html_principal != -1:
            modificador_html = BeautifulSoup(html_principal.text, 'html.parser')
            cadeia_de_cap = modificador_html.find_all("script", { "id" : "manga-info" })

            cadeia_de_cap_str = str(cadeia_de_cap[0])
            string_tratada = cadeia_de_cap_str[57:len(cadeia_de_cap_str)-9]
            self.json_obj = json.loads(string_tratada)
            print("[ ENGINE ] - Mangá encontrado")
            return self.json_obj
        else:
            print("[ ENGINE ] - Mangá não encontrado")
            return -1
    
    def Download(self, url, capitulo, caminho=False):
        data_img = {}
        html_principal = self.__Request_Anime(url)

        if html_principal != -1:
            try:
                modificador_html = BeautifulSoup(html_principal.text, 'html.parser')
                cadeia_de_imagens = modificador_html.find_all("div", {"class" : "section table-of-contents"})
                
                modificador_html_2 = BeautifulSoup(str(cadeia_de_imagens[0]), 'html.parser')
                imagens = modificador_html_2.find_all("img", {'class':'lazy'})

                for img in imagens: data_img[img.get('id')] = img.get('data-src')
            
                self.__Salvar_Anime(data_img, capitulo, caminho=False)
                print("[ ENGINE ] - Baixado com sucesso")
                return 0
            except Exception as erro:
                print(f"[ ENGINE ] {str(erro)}")
                return -1
        else:
            return -1

    def GetCapitulo(self, capitulo, data):
        for cap in data["allposts"]:
            if(cap['num'] == str(capitulo)):
                return cap['id']
    
    def GetNome(self):
        return self.json_obj['chapter_name']
    
    def GetQtdCapitulos(self):
        return self.json_obj['chapters']
    
    def GetDescricao(self):
        return self.json_obj['description']
    
    def GetGenero(self):
        return self.json_obj['genres']
    
    def GetCapa(self):
        return self.json_obj['cover']

    def __Printar(self, data):
        print(json.dumps(data, indent=4))