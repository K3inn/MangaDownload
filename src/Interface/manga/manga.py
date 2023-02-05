# -*- coding: utf-8 -*-
import requests
import json
import os
from bs4 import BeautifulSoup
from PyQt5.QtCore import pyqtSignal, QObject

import base64

from io import BytesIO
from PIL import Image
from PyPDF2 import PdfWriter, PdfFileReader, PageObject

class Mangayabu(QObject):
    finished = pyqtSignal(dict)
    downloaded = pyqtSignal(str)
    def __init__(self, nome=None, capitulo=None, url=None):
        super().__init__()
        self.nome = nome
        self.capitulo = capitulo
        self.url = url
        pass

    # Faz a requisição das url's
    def __Request_Anime(self, url):
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta
        return -1

    # Processo de Salvamento
    def __Salvar_Anime(self, bytes, capitulo):
        caminho_para_salvar = f'Download_Padrão/{self.nome}/{str(capitulo)}/index.jpeg'
        os.makedirs(os.path.dirname(caminho_para_salvar), exist_ok=True)

        for i in bytes:
            img = self.__Request_Anime(bytes[i])
            diretorio_para_salvar = caminho_para_salvar.replace('index.jpeg', f'{i}.jpeg')
            with open(diretorio_para_salvar, 'wb') as arquivo:
                arquivo.write(img.content)

        self.downloaded.emit('Download Concluído')

    def Pesquisar_anime(self):
        self.nome = self.nome.replace(" ", '-')
        base_url_pesqusia = "https://mangayabu.top/manga/{}/page/14/"

        html_principal = self.__Request_Anime(base_url_pesqusia.format(self.nome))
        if html_principal != -1:
            modificador_html = BeautifulSoup(html_principal.text, 'html.parser')
            cadeia_de_cap = modificador_html.find_all("script", { "id" : "manga-info" })

            cadeia_de_cap_str = str(cadeia_de_cap[0])
            string_tratada = cadeia_de_cap_str[57:len(cadeia_de_cap_str)-9]
            self.json_obj = json.loads(string_tratada)
            url = self.GetCapitulo(self.capitulo, self.json_obj)
            self.finished.emit({'url':url, 'cap':self.capitulo, 'nome':self.nome,'data':self.json_obj})
            return 
        else:
            self.finished.emit({})
            return -1
    
    def Download(self):
        data_img = {}
        html_principal = self.__Request_Anime(self.url)

        if html_principal != -1:
            try:
                modificador_html = BeautifulSoup(html_principal.text, 'html.parser')
                cadeia_de_imagens = modificador_html.find_all("div", {"class" : "section table-of-contents"})
                
                modificador_html_2 = BeautifulSoup(str(cadeia_de_imagens[0]), 'html.parser')
                imagens = modificador_html_2.find_all("img")
                for img in imagens: data_img[img.get('id')] = img.get('src'); 
                self.__Salvar_Anime(data_img, self.capitulo)
            except Exception as erro:
                print(f"[ ENGINE ] {str(erro)}")
                return -1
        else:
            return -1

    def GetCapitulo(self, capitulo, data):
        for cap in data["allposts"]:
            if(cap['num'] == str(capitulo)):
                return cap['chapters'][0]['id']
    
    def GetNome(self, json):
        return json['chapter_name']
    
    def GetQtdCapitulos(self, json):
        return json['chapters']
    
    def GetDescricao(self, json):
        return json['description']
    
    def GetGenero(self, json):
        return json['genres']
    
    def GetCapa(self, json):
        return json['cover']

    def __Printar(self, data):
        print(json.dumps(data, indent=4))