from manga import Mangayabu
from time import sleep
from os import system
import platform

MENU = ["--- MENU ---", "[1] PROCURAR MANGÁ", "[2] BAIXAR", "[3] INFORMAÇÃO", "[4] CONFIGURAR DIRETORIO", "[5] ENCERRAR"]
CLEAR = ''
def Infos(Engine, json_Data):
    anime = []
    anime.append(Engine.GetNome(json_Data))
    anime.append(Engine.GetQtdCapitulos(json_Data))
    anime.append(Engine.GetDescricao(json_Data))
    anime.append(Engine.GetGenero(json_Data))
    for i in anime:
        print(f'[ ENGINE ] {i}')

def Buscar_Anime(Engine, nome):
    json_Data = Engine.Pesquisar_anime(nome)
    if json_Data != -1:
        return json_Data
    return -1

def Baixar(Engine, json_Data, capitulo, diretorio):
    link = Engine.GetCapitulo(capitulo, json_Data)

    if link != -1:
        download_resultado = Engine.Download(link, diretorio)
        if download_resultado != -1:
            print("[ ENGINE ] CONCLUÍDO")
        else:
            print("[ ENGINE ] MANGÁ NÃO CONSEGUIU BAIXAR ")
def main():
    print("[ ENGINE ] RODANDO\n")
    Manga_engine = Mangayabu()
    data = [-1, '']
    diretorio = ''
    if(platform.system() == 'Windows'): CLEAR = 'cls'
    else: CLEAR = 'clear'

    while True != 4:
        for i in MENU:
            print(i)
        input_usuario = int(input("\n>> "))

        if input_usuario == 1:
            nome_anime_str = str(input("\nNome do Mangá>> "))
            resposta = Buscar_Anime(Manga_engine, nome_anime_str)
            if resposta != -1:
                data[0] = 0
                data[1] = resposta
                sleep(5)
                system(CLEAR)

        elif input_usuario == 2:
            if data[0] != -1 and diretorio != '':
                capitulo = int(input("\nCapitulo >> "))
                Baixar(Manga_engine, data[1], capitulo, diretorio)
                sleep(5)
                print("\n")
            else:print("Oops, Você ainda não buscou uma Mangá /ou não definiu um diretorio\n")

        elif input_usuario == 3:
            if data[0] != -1 and diretorio != '':
                Infos(Manga_engine, data[1])
                sleep(5)
                print("\n")
            else:print("Oops, Você ainda não buscou uma Mangá /ou não definiu um diretorio\n")
        
        elif input_usuario == 4:
            diretorio = str(input("\n>> "))
            print("[ ENGINE ] Diretorio Definido\n")

        elif input_usuario == 5:
            print("Engine Encerrada")
            break
        
        else:
            print("[ ENGINE ] COMANDO INVALIDO\n")
main()
