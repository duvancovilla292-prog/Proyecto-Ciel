import json
import time
import os
import sys
import descargador 
from economia import manejar_economia
from gacha import manejar_gacha
from anime import manejar_anime
from perfil import manejar_perfil

# ==========================================
# CONFIGURACIÓN MÍSTICA DE MONGODB ATLAS
# ==========================================
from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://cielbot:cielbot292@cluster0.o3phddj.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db_mongo = client['BotCielDB']
    coleccion_economia = db_mongo['sistema_economia'] # <--- Colección en la nube para economia.json
except Exception as e:
    print(f"🛑 [PYTHON-MONGO] Error crítico de conexión: {e}", file=sys.stderr)
    sys.exit(1)

# ==========================================
# CONTROLADORES DE ALMACENAMIENTO EN LA NUBE
# ==========================================

def cargar_grupo_db(chat_id):
    """Carga los datos de economía de un grupo específico desde MongoDB Atlas"""
    try:
        documento = coleccion_economia.find_one({"_id": chat_id})
        if documento:
            return documento.get("usuarios", {})
        return {}
    except Exception as e:
        print(f"⚠️ Error al cargar datos desde MongoDB: {e}", file=sys.stderr)
        return {}

def guardar_grupo_db(chat_id, usuarios_data):
    """Guarda o actualiza los datos de economía de un grupo en la nube"""
    try:
        coleccion_economia.update_one(
            {"_id": chat_id},
            {"$set": {"usuarios": usuarios_data}},
            upsert=True
        )
    except Exception as e:
        print(f"⚠️ Error al guardar datos en MongoDB: {e}", file=sys.stderr)

def registrar_usuario_si_no_existe(usuarios_chat, user_id, nombre="Usuario"):
    """Registra al usuario localmente en el diccionario del chat si no existe"""
    if user_id not in list(usuarios_chat.keys()):
        # Si por alguna razón los datos de perfil global venían anidados (como en tu database anterior), los limpiamos
        if isinstance(usuarios_chat.get(user_id), dict) and "billetera" in usuarios_chat[user_id]:
            return
            
        usuarios_chat[user_id] = {
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
    # 1. Cargamos de la nube únicamente los usuarios de ESTE chat/grupo
    usuarios_chat = cargar_grupo_db(chat_id)
    
    # 2. Verificamos y registramos si es nuevo en el grupo
    registrar_usuario_si_no_existe(usuarios_chat, user_id, nombre_remitente)
    
    ahora = int(time.time())
    
    # Manejo seguro por si el formato antiguo interfiere con el nombre
    if isinstance(usuarios_chat[user_id], dict):
        usuarios_chat[user_id]["ultima_actividad"] = ahora
    
    partes = texto_mensaje.split()
    if not partes:
        return None
    comando = partes[0].lower()
    args_lista = partes[1:] 
    
    args_texto = " ".join(args_lista).strip()
    
    # ==========================================
    # COMANDOS DE DESCARGAS MULTIMEDIA
    # ==========================================
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

    # ==========================================
    # ENRUTADORES DE MÓDULOS DE JUEGOS Y PERFIL
    # ==========================================
    
    # Pasamos 'usuarios_chat' que simula ser el db[chat_id] original
    respuesta = manejar_economia(usuarios_chat, user_id, comando, args_lista, ahora)
    if respuesta:
        guardar_grupo_db(chat_id, usuarios_chat)
        return respuesta
    
    respuesta = manejar_gacha(usuarios_chat, user_id, comando, args_lista, ahora)
    if respuesta:
        guardar_grupo_db(chat_id, usuarios_chat)
        return respuesta
        
    respuesta = manejar_anime(usuarios_chat, user_id, comando, args_lista, ahora)
    if respuesta:
        guardar_grupo_db(chat_id, usuarios_chat)
        return respuesta

    # Para el perfil que requería toda la estructura json, le armamos un diccionario compatible en caliente
    db_compatible_perfil = {chat_id: usuarios_chat}
    respuesta = manejar_perfil(db_compatible_perfil, user_id, comando, args_lista, ahora)
    if respuesta:
        guardar_grupo_db(chat_id, usuarios_chat)
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