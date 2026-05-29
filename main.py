import json
import time
import os
import sys
import descargador 
from economia import manejar_economia
from gacha import manejar_gacha
from anime import manejar_anime
from perfil import manejar_perfil

DB_FILE = "economia.json"

def cargar_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def guardar_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def registrar_usuario_si_no_existe(db, chat_id, user_id, nombre="Usuario"):
    if chat_id not in db:
        db[chat_id] = {}
        
    if user_id not in db[chat_id]:
        db[chat_id][user_id] = {
            "nombre": nombre,
            "billetera": 500,
            "banco": 0,
            "racha_daily": 0,
            "ultimo_daily": 0,
            "ultimo_work": 0,
            "ultimo_slut": 0,
            "ultimo_crime": 0,
            "ultima_actividad": int(time.time()),
            "inventario": {},
            "objetos": {},
            "tiros_totales": 0
        }

def enrutador_principal(user_id, nombre_remitente, texto_mensaje, chat_id):
    db = cargar_db()
    
    registrar_usuario_si_no_existe(db, chat_id, user_id, nombre_remitente)
    
    ahora = int(time.time())
    db[chat_id][user_id]["ultima_actividad"] = ahora
    
    partes = texto_mensaje.split()
    if not partes:
        return None
    comando = partes[0].lower()
    args_lista = partes[1:] 
    
    args_texto = " ".join(args_lista).strip()
    
    if comando in ['#mp4', '#ytmp4', '#play', '#yt', '#ytaudio', '#playaudio']:
        es_audio = comando in ['#play', '#yt', '#ytaudio', '#playaudio']
        mensaje, archivo = descargador.descargar_youtube(args_texto, es_audio=es_audio)
        if archivo:
            print(f"{mensaje} | {archivo}") 
        else:
            print(mensaje)
        sys.exit(0) 

    elif comando in ['#tiktok', '#tt']:
        mensaje, archivo = descargador.descargar_tiktok(args_texto, nombre_remitente)
        if archivo:
            print(f"{mensaje} | {archivo}")
        else:
            print(mensaje)
        sys.exit(0)

    elif comando in ['#facebook', '#fb', '#reel', '#ig', '#instagram']:
        mensaje, archivo = descargador.descargar_redes_sociales(args_texto)
        if archivo:
            print(f"{mensaje} | {archivo}")
        else:
            print(mensaje)
        sys.exit(0)

    respuesta = manejar_economia(db[chat_id], user_id, comando, args_lista, ahora)
    if respuesta:
        guardar_db(db)
        return respuesta
    
    respuesta = manejar_gacha(db[chat_id], user_id, comando, args_lista, ahora)
    if respuesta:
        guardar_db(db)
        return respuesta
        
    respuesta = manejar_anime(db[chat_id], user_id, comando, args_lista, ahora)
    if respuesta:
        guardar_db(db)
        return respuesta

    respuesta = manejar_perfil(db, user_id, comando, args_lista, ahora)
    if respuesta:
        guardar_db(db)
        print(respuesta)
        sys.exit(0)
        
    return "《✧》Comando no reconocido o no pertenece a las secciones activas."

if __name__ == "__main__":
    if len(sys.argv) >= 5:
        sender = sys.argv[1]
        pushName = sys.argv[2]
        texto = sys.argv[3]
        chatJid = sys.argv[4] 
        
        resultado = enrutador_principal(sender, pushName, texto, chatJid)
        if resultado:
            print(resultado)

    else:
        print(f"《✧》Error de parámetros. Esperados: 5, Recibidos: {len(sys.argv)}")
        print(f"       Argumentos actuales: {sys.argv}")