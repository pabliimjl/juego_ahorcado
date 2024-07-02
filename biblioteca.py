import json

def abrir_json(nombre_archivo:str, clave:str):
    with open(nombre_archivo, 'r') as archivo:
        datos = json.load(archivo)[clave]
    return datos

def guardar_json(nombre_archivo:str,clave:str,datos:list):
    with open(nombre_archivo,'w', encoding='utf-8') as archivo:
        json.dump({clave:datos}, archivo, indent=4, ensure_ascii=False)