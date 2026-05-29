import random
import time
from datetime import datetime,timedelta

TEXTOS_WORK = [
    "✿ Realizaste trabajo de carcelero hoy y fuiste sobornado por un recluso, ganando *¥{ganancia}* Coins.",
    "✿ Tu madre te pidió que salieras a comprar unas cosas que faltaban en casa. (Por favor no lo gastes en apuestas dijo), Ahora tienes *¥{ganancia}* Coins.",
    "✿ Hoy trabajaste como loco para comprar la figura de anime que tanto deseabas, ganando *¥{ganancia}* Coins.",
    "✿ Limpiaste todo el cum de los integrantes del grupo y ganaste *¥{ganancia}* Coins.",
    "✿ Ayudaste a un streamer famoso a configurar su entorno de Linux y te donó *¥{ganancia}* Coins.",
    "✿ Pasaste toda la tarde programando un bot de WhatsApp para un negocio local y te pagaron *¥{ganancia}* Coins.",
    "✿ Le diste mantenimiento técnico a la computadora del admin (estaba llena de virus raros) y te recompensó con *¥{ganancia}* Coins.",
    "✿ Encontraste un bug crítico en el código del servidor, lo solucionaste antes de que crasheara y el equipo te dio *¥{ganancia}* Coins.",
    "✿ Te contrataron para moderar un grupo de WhatsApp caótico por un día, sobreviviste y ganaste *¥{ganancia}* Coins.",
    "✿ Armaste un servidor de Minecraft técnico con granjas automáticas para un cliente flojo y te pagó *¥{ganancia}* Coins.",
    "✿ Le soplaste todas las respuestas del examen de lógica de programación a un compañero adinerado y te dio *¥{ganancia}* Coins.",
    "✿ Hiciste un diseño de interfaz CSS hermoso para el portafolio de un amigo y ganaste *¥{ganancia}* Coins.",
    "✿ Tradujiste un repositorio completo de GitHub del inglés al español y te dieron una bonificación de *¥{ganancia}* Coins.",
    "✿ Te pagaron *¥{ganancia}* Coins por dar clases particulares sobre cómo resolver el algoritmo de paridad de un Rubik 4x4."
]

TEXTOS_SLUT_EXITO = [
    "✿ Te vistieron de maid en publico y te dieron *¥{ganancia}* Coins.",
    "✿ Le sobaste el pito a un cliente habitual y ganaste *¥{ganancia}* Coins.",
    "✿ Ayudaste al admin a eyacular y te dió *¥{ganancia}* Coins con la condicion de que no se lo cuentes a nadie.",
    "✿ Dejaste que un grupo de jóvenes te vistieran de puta a cambio de *¥{ganancia}* Coins.",
    "✿ Te pusiste orejitas de gato en stream privado y un usuario Premium te mandó *¥{ganancia}* Coins.",
    "✿ Hiciste un ASMR lamiendo el micrófono vestido de colegiala y ganaste *¥{ganancia}* Coins.",
    "✿ Aceptaste ser el sumiso de una sugar mommy por unas horas y te dejó *¥{ganancia}* Coins en la mesa.",
    "✿ Fuiste el 'esclavo de Redstone' de alguien en Minecraft vestidito de maid y te recompensó con *¥{ganancia}* Coins.",
    "✿ Te pagaron *¥{ganancia}* Coins por enviar fotos de tus patas con filtros góticos en un grupo privado.",
    "✿ Hiciste un bailecito privado en la webcam usando cosplay de elfo místico y ganaste *¥{ganancia}* Coins.",
    "✿ Un cliente te pagó *¥{ganancia}* Coins solo para que te sentaras en su regazo y le hablaras como personaje de anime."
]

TEXTOS_SLUT_EXITO.append("✿ Fuiste a la esquina pero te encontraste a tu vecino, hablaron de chismes toda la noche y solo te dio *¥{ganancia}* Coins por el rato.")


TEXTOS_SLUT_FALLO = [
    "✿ Dejaste que los integrantes del grupo te usaran como saco de cum, pero no te movias rico y te robaron *-¥{perdida}* Coins.",
    "✿ Un negro te la metió tan fuerte que tuviste que pagar una reconstruccion anal, perdiste *-¥{perdida}* Coins.",
    "✿ Te pillaron intentando hacer un trío sin permiso en el baño del club, te sacaron a patadas y perdiste *-¥{perdida}* Coins médicas.",
    "✿ Hiciste un show privado pero se te cayó el internet a mitad de camino, te denunciaron por estafa y tuviste que pagar *-¥{perdida}* Coins."
]

TEXTOS_CRIME_EXITO = [
    "✿ Vendiste la contraseña del wifi de tu ex por *¥{ganancia}* Coins.",
    "✿ Te dieron dinero por enfrentar feministas, felicidades, ganaste *¥{ganancia}* Coins.",
    "✿ Hiciste evasión de impuestos y ganaste *¥{ganancia}* Coins.",
    "✿ Vendiste a tu chihuahua a alguien de la calle por *¥{ganancia}* Coins.",
    "✿ Con que haciendo maldades? Toma *¥{ganancia}* Coins und no se lo digas a nadie.",
    "✿ Vendiste a tu hermana por *¥{ganancia}* Coins.",
    "✿ Saqueaste una tienda de los chinos y ganaste *¥{ganancia}* Coins.",
    "✿ Hackeaste la base de datos de la escuela para borrar tus reportes y encontraste una billetera virtual con *¥{ganancia}* Coins.",
    "✿ Le vendiste planos falsos de una base secreta de Minecraft a un clan enemigo por *¥{ganancia}* Coins.",
    "✿ Falsificaste un boleto VIP para un concierto de Morat, lo revendiste en la entrada y ganaste *¥{ganancia}* Coins.",
    "✿ Te colaste en el laboratorio místico del gobierno, robaste unos compuestos extraños y los vendistas en el mercado negro por *¥{ganancia}* Coins.",
    "✿ Creaste una criptomoneda falsa llamada 'SlimeCoin', estafaste a unos cuantos inversores y te embolsaste *¥{ganancia}* Coins."
]
TEXTOS_CRIME_FALLO = [
    "✿ Intentaste saquear una tienda y los chinos te corrieron 10 cuadras, perdiste *-¥{perdida}* Coins en el camino.",
    "✿ Estás pendejo, fallaste y perdiste *-¥{perdida}* Coins, pinche pendejo.",
    "✿ Intentaste revolucionar el mundo con un invento innovador, pero te silenciaron y perdiste *-¥{perdida}* Coins.",
    "✿ Intentaste vender a tu hermana pero te la quitaron y perdiste *-¥{perdida}* Coins.",
    "✿ Intentaste piratear un software de la NASA pero te rastrearon la IP al instante y te cobraron una fianza de *-¥{perdida}* Coins.",
    "✿ Quisiste robarle el gato místico a una bruja de la calle, pero el animal te arañó toda la cara y gastaste *-¥{perdida}* Coins en vacunas.",
    "✿ Te metiste a robar a una casa pero resultó ser la casa de un boxeador profesional; terminaste en el hospital pagando *-¥{perdida}* Coins.",
    "✿ Intentaste revender respuestas de un examen importante, pero te descubrió el director y tuviste que pagar *-¥{perdida}* Coins de soborno para que no te expulsaran.",
    "✿ Quisiste hackear un cajero automático usando un script de YouTube, el cajero se bloqueó, sonó la alarma y tiraste *-¥{perdida}* Coins al huir."
]

def obtener_proximo_mediodia():
    ahora_dt = datetime.now()
    mediodia_hoy = ahora_dt.replace(hour=12, minute=0, second=0, microsecond=0)
    
    if ahora_dt < mediodia_hoy:
        return int(mediodia_hoy.timestamp())
    else:
        mediodia_manana = mediodia_hoy + timedelta(days=1)
        return int(mediodia_manana.timestamp())
    
def manejar_economia(db, user_id, comando, args, ahora):
    usuario = db[user_id]

    if comando in ["#balance", "#bal", "#coins"]:
        target_user = usuario
        if args and args[0].startswith("@"):
            mencion_sucia = args[0].lstrip("@").split("@")[0]
            numeros_target = "".join(filter(str.isdigit, mencion_sucia))
            
            for id_existente in db.keys():
                numeros_existentes = "".join(filter(str.isdigit, id_existente))
                if numeros_target == numeros_existentes:
                    target_user = db[id_existente]
                    break
                    
        return (
            f"✿ *》》Economía de @{target_user['nombre']}《《* ✿\n\n"
            f"⛀ Dinero » *¥{target_user['billetera']:,} Coins*\n"
            f"⚿ Banco » *¥{target_user['banco']:,} Coins*\n"
            f"⛁ Total » *¥{target_user['billetera'] + target_user['banco']:,} Coins*\n\n"
            f"> _Para proteger tu dinero, ¡depósitalo en el banco usando #deposit!_"
        )
    elif comando in ["#help", "#ayuda", "#commands"]:
        return (
            f"「✿」*》》PANEL DE SOPORTE MÍSTICO《《*\n"
            f"¡Hola @{usuario['nombre']}! Aquí tienes la lista completa de comandos disponibles en el sistema ordenados por módulos:\n\n"
            f"⚙️ *SISTEMA CENTRAL (2)*\n"
            f"• `#on` » Activa las funciones del bot en el chat actual.\n"
            f"• `#off` » Pausa el bot y lo pone a dormir en este chat.\n\n"
            f"💰 *MÓDULO DE ECONOMÍA*\n"
            f"• `#balance` / `#bal` » Muestra tus Coins en billetera, banco y el total neto.\n"
            f"• `#work` / `#w` » Realiza un trabajo seguro para ganar entre ¥2,000 y ¥4,000 (Tiempo Espera: 45s).\n"
            f"• `#slut` » Ve a la esquina arriesgándote a ganar mucho o perder en el intento (Tiempo Espera: 2m).\n"
            f"• `#crime` » Comete un delito informático o estafa. Gran recompensa o costosa multa (Tiempo Espera: 2.5m).\n"
            f"• `#daily` » Reclama tu recompensa diaria acumulativa. ¡Mantén la racha!\n"
            f"• `#deposit [cant/all]` » Resguarda tus Coins en el banco para evitar que te las roben.\n"
            f"• `#withdraw [cant/all]` » Retira tus Coins del banco para poder utilizarlas.\n"
            f"• `#pay [@mención] [cantidad]` » Transfiere Coins de tu billetera a otro usuario.\n"
            f"• `#rob [@mención]` » Intenta asaltar a un usuario inactivo por más de 1 hora (Éxito: 35%).\n"
            f"• `#cf [cantidad/all] [cara/cruz]` » Apuesta tus Coins lanzando una moneda al aire.\n"
            f"• `#rt [cantidad] [red/black]` » Juega tus Coins en la ruleta de la suerte.\n"
            f"• `#einfo` / `#economyinfo` » Consulta detalladamente tus temporizadores de cooldown activos.\n"
            f"• `#baltop` / `#eboard` » Muestra el Top 10 de los usuarios más millonarios del grupo.\n\n"
            f"🔮 *MÓDULO GACHA *\n"
            f"• `#gacha` / `#pull` » Invoca un personaje aleatorio del catálogo por *¥5,000* Coins.\n"
            f"• `#chars` / `#personajes` `[pág]` » Revisa tu colección actual de personajes (10 por página).\n"
            f"• `#charinfo [nombre]` » Despliega la descripción, rareza y serie de un personaje específico.\n"
            f"• `#charimage [nombre]` » Obtén el enlace de la ilustración oficial del personaje.\n"
            f"• `#vender [nombre]` » Vende copias repetidas de tus personajes a cambio de Coins directas.\n"
            f"• `#regalar [@mención] [nombre]` » Cede de forma mística una de tus copias a un amigo.\n"
            f"• `#shop` / `#gachashop` » Visita la tienda para adquirir ventajas como Tickets Épicos o Amuletos.\n"
            f"• `#buy [id_producto] [cantidad]` » Adquiere artículos de la tienda gacha usando tus Coins.\n"
            f"• `#ginfo` / `#gachainfo` » Estadísticas de tu progreso global de colección y rates del gacha.\n"
            f"• `#gtop` / `#topgacha` » Tabla de clasificación con los mayores coleccionistas del servidor.\n\n"
            f"🎭 *MÓDULO DE REACCIONES ANIME (50)* _(Uso: #comando o #comando @mención)_\n"
            f"• `#angry` _(#enojado)_ \n• `#bath` \n• `#bite` \n• `#bleh` \n• `#blush`\n"
            f"• `#bored` _(#aburrido)_ \n• `#call` \n• `#clap` _(#aplaudir)_ \n• `#coffee` _(#cafe)_\n"
            f"• `#cold` \n• `#cook` \n• `#cry` \n• `#cuddle` \n• `#dance` \n• `#dramatic` _(#drama)_\n"
            f"• `#draw` \n• `#drunk` \n• `#eat` _(#comer)_ \n• `#facepalm` \n• `#gaming`\n"
            f"• `#greet` _(#hi)_ \n• `#happy` _(#feliz)_ \n• `#heat` \n• `#hug` \n• `#jump`\n"
            f"• `#impregnate` _(#preg / #preñar)_ \n• `#kill` \n• `#kiss` _(#muak)_\n"
            f"• `#kisscheek` _(#beso)_ \n• `#laugh` \n• `#lick` \n• `#love` \n• `#mad` \n• `#pat`\n"
            f"• `#poke` \n• `#pout` \n• `#punch` \n• `#run` \n• `#sad` \n• `#scared` \n• `#shrug`\n"
            f"• `#slap` \n• `#sleep` \n• `#smirk` \n• `#smoke` \n• `#spit` _(#escupir)_\n"
            f"• `#step` _(#pisar)_ \n• `#think` \n• `#tickle` \n• `#walk`\n\n"
            f"> _Recuerda escribir los comandos respetando los argumentos indicados entre corchetes._"
        )
    elif comando in ["#coinflip", "#cf"]:
        if len(args) < 2:
            return "《✧》Uso correcto: #cf [cantidad/all] [cara/cruz]"
        
        if args[0].lower() == "all":
            apuesta = usuario["billetera"]
        else:
            try:
                apuesta = int(args[0])
            except ValueError:
                return "《✧》Debes ingresar una cantidad numérica válida o 'all'."
        
        eleccion = args[1].lower()
        if eleccion not in ["cara", "cruz"]:
            return "《✧》Debes elegir entre *cara* o *cruz*."
            
        if apuesta < 200:
            return "《✧》Debes apostar al menos *¥200* Coins."
            
        if usuario["billetera"] < apuesta:
            return "《✧》No tienes suficientes *Coins* en la billetera para esta apuesta."
            
        resultado = random.choice(["cara", "cruz"])
        if eleccion == resultado:
            usuario["billetera"] += apuesta
            return f"「✿」La moneda ha caído en *{resultado.capitalize()}* y has ganado *¥{apuesta*2:,} Coins*!\n> Tu elección fue *{eleccion.capitalize()}*"
        else:
            usuario["billetera"] -= apuesta
            return f"「✿」La moneda ha caído en *{resultado.capitalize()}* y has perdido *¥{apuesta:,} Coins*!\n> Tu elección fue *{eleccion.capitalize()}*"

    elif comando == "#crime":
        cooldown = 150 
        if ahora - usuario["ultimo_crime"] < cooldown:
            restante = cooldown - (ahora - usuario["ultimo_crime"])
            return f"《✧》Debes esperar *{restante // 60} minutos {restante % 60} segundos* para usar *#crime* de nuevo."
            
        usuario["ultimo_crime"] = ahora
        if random.random() < 0.55:
            ganancia = random.randint(7000, 8000)
            usuario["billetera"] += ganancia
            return random.choice(TEXTOS_CRIME_EXITO).format(ganancia=f"{ganancia:,}")
        else:
            perdida = random.randint(10000, 11000)
            usuario["billetera"] = max(0, usuario["billetera"] - perdida)
            return random.choice(TEXTOS_CRIME_FALLO).format(perdida=f"{perdida:,}")

    elif comando in ["#daily"]:
        proximo_mediodia = obtener_proximo_mediodia()
        ultimo_daily = usuario.get("ultimo_daily", 0)
        
        inicio_ciclo_actual = proximo_mediodia - 86400
        
        if ultimo_daily >= inicio_ciclo_actual:
            restante = proximo_mediodia - ahora
            horas = restante // 3600
            minutos = (restante % 3600) // 60
            return f"《✧》Ya reclamaste tu recompensa diaria mística. El sistema se reinicia exactamente a las 12:00 PM del mediodía. Regresa en *{horas}h {minutos}m*."
            
        inicio_ciclo_anterior = inicio_ciclo_actual - 86400
        if ultimo_daily >= inicio_ciclo_anterior:
            usuario["racha_daily"] += 1
        else:
            usuario["racha_daily"] = 1
            
        base = 30000
        bono = min(usuario["racha_daily"] * 5000, 30000)
        total = base + bono
        
        usuario["billetera"] += total
        usuario["ultimo_daily"] = ahora
        return (
            f"「✿」*》》RECOMPENSA DIARIA MÍSTICA《《*\n\n"
            f"¡Felicidades *{usuario['nombre']}*! Has recolectado tus recursos diarios:\n"
            f"💰 *Premio:* *¥{total:,} Coins*\n"
            f"🔥 *Racha actual:* {usuario['racha_daily']} días seguidos.\n"
            f"> _¡El cooldown se reinicia globalmente todos los días a las 12:00 PM!_"
        )

    elif comando in ["#deposit", "#dep","#depositar"]:
        if len(args) < 1:
            return "《✧》Uso correcto: #dep [cantidad/all]"
            
        if args[0].lower() == "all":
            cantidad = usuario["billetera"]
        else:
            try:
                cantidad = int(args[0])
            except ValueError:
                cantidad = -1
                
        if cantidad <= 0:
            return "《✧》Debes depositar una cantidad válida.\n> Ejemplo 1 » *#dep 25000*\n> Ejemplo 2 » *#dep all*"
            
        if usuario["billetera"] < cantidad:
            return "《✧》No tienes suficientes Coins en efectivo."
            
        usuario["billetera"] -= cantidad
        usuario["banco"] += cantidad
        return f"✿ Depositaste *¥{cantidad:,} Coins* en el banco, ya no podrán robártelo."

    elif comando in ["#economyboard", "#eboard", "#baltop"]:
        usuarios_ordenados = sorted(db.items(), key=lambda x: x[1]["billetera"] + x[1]["banco"], reverse=True)
        respuesta = "「✿」Los usuarios con más *Coins* son:\n\n"
        for idx, (uid, datos) in enumerate(usuarios_ordenados[:10], start=1):
            neto = datos["billetera"] + datos["banco"]
            respuesta += f"✰ {idx} » *{datos['nombre']}:*\n\t\t Total→ *¥{neto:,} Coins*\n"
        respuesta += "\n> • Página *1* de *1*"
        return respuesta
    
    elif comando in ["#economyinfo", "#einfo"]:
        def calc_relativo(u, key, t):
            diff = ahora - u.get(key, 0)
            return "✅ Listo" if diff >= t else f"❌ {t - diff}s"
            
        proximo_mediodia = obtener_proximo_mediodia()
        inicio_ciclo_actual = proximo_mediodia - 86400
        if usuario.get("ultimo_daily", 0) >= inicio_ciclo_actual:
            restante_daily = proximo_mediodia - ahora
            h = restante_daily // 3600
            m = (restante_daily % 3600) // 60
            status_daily = f"❌ {h}h {m}m (12:00 PM)"
        else:
            status_daily = "✅ Listo"
            
        return (
            f"✿ *》》Economía @{usuario['nombre']}《《* ✿\n\n"
            f"ⴵ Work  » * {calc_relativo(usuario, 'ultimo_work', 45)}\n"
            f"ⴵ Slut  » * {calc_relativo(usuario, 'ultimo_slut', 120)}\n"
            f"ⴵ Crime » * {calc_relativo(usuario, 'ultimo_crime', 150)}\n"
            f"ⴵ Daily » * {status_daily}\n"
            f"⛁ Coins totales » *¥{usuario['billetera'] + usuario['banco']:,} Coins*"
        )

    elif comando in ["#withdraw", "#with"]:
        if len(args) < 1:
            return "《✧》Uso correcto: #with [cantidad/all]"
            
        if args[0].lower() == "all":
            cantidad = usuario["banco"]
        else:
            try:
                cantidad = int(args[0])
            except ValueError:
                return "《✧》Cantidad inválida."
                
        if cantidad <= 0 or usuario["banco"] < cantidad:
            return "《✧》No tienes suficientes fondos en el banco."
            
        usuario["banco"] -= cantidad
        usuario["billetera"] += cantidad
        return f"✿ Retiraste *¥{cantidad:,} Coins* del banco, ahora podrás usarlo pero también podrán robártelo."

    elif comando in ["#givecoins", "#pay"]:
        if len(args) < 2:
            return "《✧》Uso correcto: #pay [@mención] [cantidad]"
        try:
            monto = int(args[1])
        except ValueError:
            return "《✧》Monto inválido."
            
        if monto <= 0 or usuario["billetera"] < monto:
            return "《✧》No tienes suficientes Coins en efectivo."
            
        usuario["billetera"] -= monto
        return f"✿ Transferiste *¥{monto:,} Coins* a *{args[0]}*\n> Ahora tienes *¥{usuario['billetera']:,} Coins* en efectivo."

    elif comando in ["#rob", "#steal"]:
        if len(args) < 1:
            return "《✧》Menciona a quién quieres robar."
            
        target_id = args[0].replace("@", "")
        if not target_id.endswith("@s.whatsapp.net"):
            target_id = f"{target_id}@s.whatsapp.net"
            
        if target_id == user_id:
            return "《✧》No puedes robarte a ti mismo, genio. 🧠"
            
        target = db.get(target_id)
        if not target:
            return "《✧》El usuario objetivo no está registrado en el sistema de economía."
            
        if ahora - target["ultima_actividad"] < 3600:
            return "《✧》Solo puedes robarle *Coins* a un usuario si estuvo más de 1 hora inactivo."
            
        if target["billetera"] < 5000:
            return f"《✧》 *{target['nombre']}* no tiene suficientes *Coins* fuera del banco como para que valga la pena intentar robar."
            
        if random.random() < 0.35:
            botin = int(target["billetera"] * 0.25)
            target["billetera"] -= botin
            usuario["billetera"] += botin
            return f"「✿」¡Lograste asaltar a *{target['nombre']}* y te llevaste *¥{botin:,} Coins!*"
        else:
            multa = 4000
            usuario["billetera"] = max(0, usuario["billetera"] - multa)
            return f"《✧》¡Fallaste el robo! Te atraparon y pagaste una multa de *¥{multa:,} Coins*."

    elif comando in ["#work","#w","#W"]:
        cooldown = 45 
        tiempo_transcurrido = ahora - usuario["ultimo_work"]
        
        if tiempo_transcurrido < cooldown:

            tiempo_restante = cooldown - tiempo_transcurrido
            return f"《✧》Descansa un poco, tu cuerpo necesita recuperar energía. Cooldown activo. Espera *{tiempo_restante}* segundos."
        
        usuario["ultimo_work"] = ahora
        ganancia = random.randint(2000, 4000)
        usuario["billetera"] += ganancia
        return random.choice(TEXTOS_WORK).format(ganancia=f"{ganancia:,}")

    elif comando == "#slut":
        cooldown = 120 
        if ahora - usuario["ultimo_slut"] < cooldown:
            return f"《✧》Espera a recuperar energías antes de volver a la esquina."
            
        usuario["ultimo_slut"] = ahora
        if random.random() < 0.50:
            ganancia = random.randint(5000, 6000)
            usuario["billetera"] += ganancia
            return random.choice(TEXTOS_SLUT_EXITO).format(ganancia=f"{ganancia:,}")
        else:
            perdida = random.randint(8000, 10000)
            usuario["billetera"] = max(0, usuario["billetera"] - perdida)
            return random.choice(TEXTOS_SLUT_FALLO).format(perdida=f"{perdida:,}")
    
    elif comando in ["#roulette", "#rt"]:
        if len(args) < 2:
            return "《✧》Uso correcto: #rt [cantidad] [red/black]"
            
        try:
            apuesta = int(args[0])
        except ValueError:
            return "《✧》Monto inválido."
            
        color_elegido = args[1].lower()
        if color_elegido not in ["red", "black"]:
            return "《✧》Elige entre *red* o *black*."
            
        if usuario["billetera"] < apuesta:
            return f"《✧》No tienes suficientes *Coins* fuera del banco.\n> Tienes *¥{usuario['billetera']:,} Coins* en efectivo"
            
        color_ganador = random.choice(["red", "black"])
        if color_elegido == color_ganador:
            usuario["billetera"] += apuesta
            return f"「✿」La ruleta salió en *{color_ganador}* y has ganado *¥{apuesta*2:,} Coins*!"
        else:
            usuario["billetera"] -= apuesta
            return f"「✿」La ruleta salió en *{color_ganador}* y has perdido *¥{apuesta:,} Coins*!"
        
    elif comando in ["#javier","#jarvix"]:
        return "《✧》A Javier le gusta chupar pito!!!!!!."
    
    elif comando in ["#thomas"]:
        return "《✧》A Thomas hhhhhh."
    

    return None
