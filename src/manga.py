# -*- coding: utf-8 -*-
import requests
import json
import os
from bs4 import BeautifulSoup

class Mangayabu:
    def __init__(self):
        pass

    # Faz a requisição das url's
    def __Request_Anime(self, url):
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta
        return -1

    # Processo de Salvamento
    def __Salvar_Anime(self, bytes, capitulo, caminho=False):
        caminho_para_salvar = ''
        diretorios = []
        if(caminho != False):
            caminho_para_salvar = f'{caminho}/{self.GetNome()}/{capitulo}/index.jpeg'
        else:
            caminho_para_salvar = f'Download_Padrão/{self.GetNome()}/{capitulo}/index.jpeg'
        os.makedirs(os.path.dirname(caminho_para_salvar), exist_ok=True)
        for i in bytes:
            img = self.__Request_Anime(bytes[i])
            diretorio_para_salvar = caminho_para_salvar.replace('index.jpeg', f'{i}.jpeg')
            
            diretorios.append(diretorio_para_salvar)
            with open(diretorio_para_salvar, 'wb') as arquivo:
                arquivo.write(img.content)
        return diretorios

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
                imagens = modificador_html_2.find_all("img")
                for img in imagens: data_img[img.get('id')] = img.get('src'); 

                dires = self.__Salvar_Anime(data_img, capitulo, caminho)
                return dires
            except Exception as erro:
                print(f"[ ENGINE ] {str(erro)}")
                return -1
        else:
            return -1

    def GetCapitulo(self, capitulo, data):
        for cap in data["allposts"]:
            if(cap['num'] == str(capitulo)):
                return cap['chapters'][0]['id']
    
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