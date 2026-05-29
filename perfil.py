import random
from datetime import datetime

ALIAS_PERFIL = {
    "allbirthdays": ["#allbirthdays", "#allbirths"],
    "birthdays": ["#birthdays", "#cumpleaños", "#births"],
    "delbirth": ["#delbirth"],
    "delgenre": ["#delgenre"],
    "divorce": ["#divorce"],
    "group": ["#gp", "#group"],
    "leaderboard": ["#leaderboard", "#lboard", "#top"],
    "level": ["#level", "#lvl"],
    "marry": ["#marry", "#casarse"],
    "profile": ["#profile", "#perfil"],
    "setbirth": ["#setbirth"],
    "setdescription": ["#setdescription", "#setdesc"],
    "setfavourite": ["#setfavourite", "#setfav"],
    "setgenre": ["#setgenre"]
}

def manejar_perfil(db, user_id, comando, args, ahora, chat_jid=None):
    usuario = db[user_id]
    
    if "nivel" not in usuario: usuario["nivel"] = 1
    if "xp" not in usuario: usuario["xp"] = 0
    if "genero" not in usuario: usuario["genero"] = "No definido"
    if "cumpleanos" not in usuario: usuario["cumpleanos"] = "No registrado"
    if "descripcion" not in usuario: usuario["descripcion"] = "Sin biografía mística."
    if "pareja" not in usuario: usuario["pareja"] = "Soltero/a"
    if "propuesta_pendiente" not in usuario: usuario["propuesta_pendiente"] = None
    if "inventario" not in usuario: usuario["inventario"] = {}

    accion = None
    for clave, comandos in ALIAS_PERFIL.items():
        if comando == f"#{clave}" or comando in comandos:
            accion = clave
            break
            
    if not accion:
        return None

    if accion == "profile":
        target_id = user_id
        if args and args[0].startswith("@"):
            mencion_sucia = args[0].lstrip("@").split("@")[0]
            numeros_target = "".join(filter(str.isdigit, mencion_sucia))
            for id_existente in db.keys():
                if numeros_target in id_existente:
                    target_id = id_existente
                    break
        
        u_target = db[target_id]
        

        lvl = u_target.get("nivel", 1)
        xp = u_target.get("xp", 0)
        xp_necesaria = lvl * 1000
        gen = u_target.get("genero", "No definido")
        birth = u_target.get("cumpleanos", "No registrado")
        desc = u_target.get("descripcion", "Sin biografía mística.")
        

        id_pareja = u_target.get("pareja", "Soltero/a")
        nombre_pareja = db[id_pareja]["nombre"] if id_pareja in db else "Soltero/a"
        

        fav = u_target.get("favorito", "Ninguno")

        tarjeta = (
            f"「✿」*》》PERFIL DE TEMPEST《《*\n\n"
            f"👤 *Nombre:* @{u_target['nombre']}\n"
            f"🏅 *Rango/Nivel:* Nivel {lvl} ({xp}/{xp_necesaria} XP)\n"
            f"🧬 *Género:* {gen}\n"
            f"🎂 *Cumpleaños:* {birth}\n"
            f"💖 *Relación:* {f'Casado/a con @{nombre_pareja}' if nombre_pareja != 'Soltero/a' else 'Soltero/a'}\n"
            f"👑 *Compañero Favorito:* {fav}\n\n"
            f"📝 *Biografía:*\n> {desc}\n\n"
            f"💰 *Efectivo:* ¥{u_target.get('billetera', 0):,} Coins\n"
            f"🏦 *Banco:* ¥{u_target.get('banco', 0):,} Coins"
        )
        
        if fav != "Ninguno":
            return f"{tarjeta}|{fav.replace(' ', '')}.png"
        return tarjeta

    elif accion == "setgenre":
        if not args: return "《✧》Uso: #setgenre [Hombre | Mujer]"
        opcion = args[0].capitalize()
        if opcion in ["Hombre", "Mujer"]:
            usuario["genero"] = opcion
            return f"✿ Género actualizado exitosamente a: *{opcion}*."
        return "《✧》Género inválido. Elige entre *Hombre* o *Mujer*."

    elif accion == "delgenre":
        usuario["genero"] = "No definido"
        return "✿ Has eliminado el género de tu perfil místico."

    elif accion == "setdescription":
        if not args: return "《✧》Uso: #setdesc [Tu nueva biografía]"
        nueva_desc = " ".join(args)
        usuario["descripcion"] = nueva_desc
        return "✿ Tu descripción biográfica ha sido refinada en los registros."

    elif accion == "setfavourite":
        if not args: return "《✧》Uso: #setfav [Nombre exacto del Personaje]"
        busqueda = " ".join(args).lower()
        
        personaje_encontrado = None
        for char in usuario.get("inventario", {}).keys():
            if busqueda in char.lower():
                personaje_encontrado = char
                break
                
        if not personaje_encontrado:
            return "《✧》No puedes poner como favorito un personaje que no posees en tu #chars."
            
        usuario["favorito"] = personaje_encontrado
        return f"👑 *{personaje_encontrado}* ahora es el compañero visible en tu perfil."

    elif accion == "setbirth":
        if not args: return "《✧》Uso: #setbirth [DD/MM] (Ejemplo: #setbirth 02/07)"
        fecha_str = args[0]
        try:
            datetime.strptime(fecha_str, "%d/%m")
            usuario["cumpleanos"] = fecha_str
            return f"🎂 Tu cumpleaños ha sido registrado el *{fecha_str}* misticamente."
        except ValueError:
            return "《✧》Formato de fecha inválido. Usa el formato místico *DD/MM* (Ej: #setbirth 02/07)."

    elif accion == "delbirth":
        usuario["cumpleanos"] = "No registrado"
        return "🎂 Tu fecha de cumpleaños ha sido borrada de la base de datos."

    elif accion == "allbirthdays":
        respuesta = "「✿」*》》CALENDARIO MULTIVERSAL《《*\n\n"
        hay_cumples = False
        for uid, udata in db.items():
            cumple = udata.get("cumpleanos", "No registrado")
            if cumple != "No registrado":
                respuesta += f"• *{udata['nombre']}:* {cumple} 🎈\n"
                hay_cumples = True
        if not hay_cumples: return "《✧》No hay cumpleaños registrados en el grupo aún."
        return respuesta

    elif accion == "birthdays":
        hoy = datetime.now()
        lista_cumples = []
        for uid, udata in db.items():
            cumple = udata.get("cumpleanos", "No registrado")
            if cumple != "No registrado":
                try:
                    dia, mes = map(int, cumple.split("/"))
                    fecha_cumple = datetime(hoy.year, mes, dia)
                    if fecha_cumple < hoy:
                        fecha_cumple = datetime(hoy.year + 1, mes, dia)
                    dias_faltantes = (fecha_cumple - hoy).days
                    lista_cumples.append((udata["nombre"], cumple, dias_faltantes))
                except: continue
                
        if not lista_cumples: return "《✧》No hay fechas registradas para calcular."
        
        lista_cumples = sorted(lista_cumples, key=lambda x: x[2])
        respuesta = "「✿」*》》CUMPLEAÑOS CERCANOS《《*\n\n"
        for nombre, cumple, dias in lista_cumples[:5]:
            respuesta += f"🎉 » *{nombre}* - {cumple} *(Faltan {dias} días)*\n"
        return respuesta

    elif accion == "marry":
        if not args or not args[0].startswith("@"):
            return "《✧》Debes mencionar a la persona con la que deseas unirte en matrimonio sagrado."
            
        if usuario["pareja"] != "Soltero/a":
            return "《✧》Ya te encuentras en un matrimonio civil del bot. Usa *#divorce* primero."
            
    
        mencion_sucia = args[0].lstrip("@").split("@")[0]
        numeros_target = "".join(filter(str.isdigit, mencion_sucia))
        target_id = None
        for id_existente in db.keys():
            if numeros_target in id_existente:
                target_id = id_existente
                break
                
        if not target_id or target_id == user_id:
            return "《✧》No puedes casarte contigo mismo ni con un fantasma."
            
        if db[target_id].get("pareja", "Soltero/a") != "Soltero/a":
            return f"《✧》*{db[target_id]['nombre']}* ya está casado/a con alguien más."


        db[target_id]["propuesta_pendiente"] = user_id
        return f"💖 ¡Atención! @{usuario['nombre']} le ha propuesto matrimonio a @{db[target_id]['nombre']}! 🥰\n\n> _Para aceptar, la persona mencionada debe responder ejecutando el comando #marry @{usuario['nombre']}_"

    elif accion == "divorce":
        if usuario["pareja"] == "Soltero/a":
            return "《✧》No puedes divorciarte si estás completamente soltero/a."
            
        id_ex = usuario["pareja"]
        usuario["pareja"] = "Soltero/a"
        if id_ex in db:
            db[id_ex]["pareja"] = "Soltero/a"
            nombre_ex = db[id_ex]["nombre"]
        else:
            nombre_ex = "tu ex-pareja"
            
        return f"💔 Rompiste los lazos místicos. Te has divorciado oficialmente de @{nombre_ex}."

    elif accion == "level":
        target_id = user_id
        if args and args[0].startswith("@"):
            mencion_sucia = args[0].lstrip("@").split("@")[0]
            numeros_target = "".join(filter(str.isdigit, mencion_sucia))
            for id_existente in db.keys():
                if numeros_target in id_existente:
                    target_id = id_existente
                    break
                    
        u_target = db[target_id]
        lvl = u_target.get("nivel", 1)
        xp = u_target.get("xp", 0)
        xp_necesaria = lvl * 1000
        barra_progreso = "▓" * int((xp / xp_necesaria) * 10) + "░" * (10 - int((xp / xp_necesaria) * 10))
        
        return (
            f"「✿」*》》SISTEMA DE EXPERIENCIA《《*\n\n"
            f"👤 *Usuario:* @{u_target['nombre']}\n"
            f"⭐ *Nivel:* {lvl}\n"
            f"📊 *Progreso:* [{barra_progreso}] ({xp}/{xp_necesaria} XP)"
        )

    elif accion == "leaderboard":
        rank = []
        for uid, udata in db.items():
            lvl = udata.get("nivel", 1)
            xp = udata.get("xp", 0)
            puntos_totales = (lvl * 1000) + xp
            rank.append((udata["nombre"], lvl, xp, puntos_totales))
            
        rank = sorted(rank, key=lambda x: x[3], reverse=True)
        
        pag = int(args[0]) if args and args[0].isdigit() else 1
        respuesta = "「✿」*》》RANKING GLOBAL DE PODER (XP)《《*\n\n"
        for idx, (name, lvl, xp, _) in enumerate(rank[:10], start=1):
            respuesta += f"🏅 {idx} » *{name}* - Nivel {lvl} ({xp} XP)\n"
        return respuesta

    elif accion == "group":
        total_usuarios = len(db)
        banco_total = sum(u.get("banco", 0) for u in db.values())
        billetera_total = sum(u.get("billetera", 0) for u in db.values())
        
        return (
            f"「✿」*》》ESTADÍSTICAS TÉCNICAS DEL GRUPO《《*\n\n"
            f"👥 *Miembros Registrados:* {total_usuarios} usuarios\n"
            f"🪙 *Economía en Circulación:* ¥{billetera_total + banco_total:,} Coins\n"
            f"⚗️ *Núcleo del Sistema:* Python 3.x + Baileys Hybrid Engine\n"
            f"🛰️ *Estado del Enrutador:* Óptimo y respondiendo misticamente."
        )

    return None