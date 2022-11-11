import json

def Adicionar_diretorio(nome,diretorio):
    json_obj = []
    with open('./Data/diretorios.json', 'r') as arquivo:
        json_obj = json.load(arquivo)
    json_obj.append({
        nome.lower() : diretorio
    })

    with open('./Data/diretorios.json', 'w') as arquivo:
        json.dump(json_obj, arquivo, indent=4, separators=(',',': '))


def Pegar_diretorio(nome):
    json_obj = []
    with open('./Data/diretorios.json', 'r') as arquivo:
        json_obj = json.load(arquivo)
    
    for nome_ in json_obj:
        for chave in nome_:
            if chave == nome.lower():
                return nome_[chave]
    return 0

def Printar_Json(data):
    json_object = json.loads(data)
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)