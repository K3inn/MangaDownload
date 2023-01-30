from manga import Mangayabu
from time import sleep
from os import system
import platform

MENU = ["--- MENU ---", "[1] PROCURAR MANGÁ", "[2] BAIXAR", "[3] INFORMAÇÃO", "[4] CONFIGURAR DIRETORIO", "[5] ENCERRAR"]
CLEAR = ''
def Infos(Engine):
    anime = []
    anime.append(Engine.GetNome())
    anime.append(Engine.GetQtdCapitulos())
    anime.append(Engine.GetDescricao())
    anime.append(Engine.GetGenero())
    for i in anime:
        print(f'[ ENGINE ] {i}')

def Buscar_Anime(Engine, nome):
    json_Data = Engine.Pesquisar_anime(nome)
    if json_Data != -1:
        return json_Data
    return -1

def Baixar(Engine, json_Data, capitulo, caminho):
    link = Engine.GetCapitulo(capitulo, json_Data)
    if link != -1:
        download_resultado = Engine.Download(link, capitulo, caminho)
        print(download_resultado)
        if download_resultado != -1:
            print("[ ENGINE ] - BAIXADO COM SUCESSO")
            print("[ ENGINE ] - CONCLUÍDO")
        else:
            print("[ ENGINE ] MANGÁ NÃO CONSEGUIU BAIXAR ")
def main():
    print("[ ENGINE ] RODANDO\n")
    Manga_engine = Mangayabu()
    data = [-1, '']
    diretorio = False
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
                sleep(2)
                system(CLEAR)

        elif input_usuario == 2:
            if data[0] != -1 and diretorio != False:
                capitulo = int(input("\nCapitulo >> "))
                mangas = Baixar(Manga_engine, data[1], capitulo, diretorio)
                print(mangas)
                sleep(5)
                print("\n")
            else:print("Oops, Você ainda não buscou uma Mangá / Ou não definiu diretorio\n")

        elif input_usuario == 3:
            if data[0] != -1:
                Infos(Manga_engine)
                sleep(5)
                print("\n")
            else:print("Oops, Você ainda não buscou uma Mangá\n")
        
        elif input_usuario == 4:
            if data[0] != -1:
                diretorio = str(input("\n>> "))
            else:print("Oops, Você ainda não buscou uma Mangá\n")

            print("[ ENGINE ] Diretorio Definido\n")

        elif input_usuario == 5:
            print("Engine Encerrada")
            break

        
        else:
            print("[ ENGINE ] COMANDO INVALIDO\n")
main()