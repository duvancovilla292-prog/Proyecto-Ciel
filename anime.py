import os
import random

TABLERO_REACCIONES = {
    "angry": (["#enojado"], "está muy enojado con el chat. 💢", "expresó su enojo hacia {target}. 💢","angry"),
    "bath": ([], "se está dando un baño virtual. 🧼", "metió a {target} a la bañera a la fuerza. 🧼","bath"),
    "bite": ([], "se mordió el labio con nerviosismo.", "le dio un mordisco tierno pero agresivo a {target}! 🦷","bite"),
    "bleh": ([], "sacó la lengua en señal de burla: ¡Bleh! 😜", "le sacó la lengua a {target} para burlarse. 😜","bleh"),
    "blush": ([], "se ha sonrojado por completo, ¡qué timidez! 😳", "se sonrojó notablemente al mirar a {target}. 😳","blush"),
    "bored": (["#aburrido"], "está soberanamente aburrido en este grupo. 🥱", "mostró desinterés total ante el mensaje de {target}. 🥱","bored"),
    "call": ([], "está haciendo un ademán de llamar por teléfono.", "está llamando intensamente a {target}. 📞","call"),
    "clap": (["#aplaudir"], "empezó a aplaudir ante la situación. 👏", "le aplaude de pie a {target} por su brillantez. 👏","clap"),
    "coffee": (["#cafe"], "se está tomando una deliciosa taza de café. ☕", "le invitó una taza de café caliente a {target}. ☕","coffee"),
    "cold": ([], "tiene muchísimo frío y está temblando. 🥶", "se acercó a {target} porque se está muriendo de frío. 🥶","cold"),
    "cook": ([], "se puso el delantal y está cocinando algo delicioso. 🍳", "le está cocinando un platillo especial a {target}. 🍳","cook"),
    "cry": ([], "rompió a llorar de forma dramática. 😭", "está llorando desconsoladamente por culpa de {target}. 😭","cry"),
    "cuddle": ([], "necesita mimos y un apapache.", "se acurrucó cálidamente al lado de {target}. 🥰","cuddle"),
    "dance": ([], "sacó los pasos prohibidos y se puso a bailar. 💃", "se puso a bailar una coreografía de anime junto a {target}. 🕺","dance"),
    "dramatic": (["#drama"], "está haciendo una escena exageradamente dramática. 🎭", "le armó un drama tremendo a {target}. 🎭","dramatic"),
    "draw": ([], "está concentrado dibujando una obra de arte. 🎨", "dibujó un retrato perfecto de {target}. 🎨","draw"),
    "drunk": ([], "andá borracho perdido bajo los efectos del alcohol. 🥴", "se tomó unos tragos de más y se le empezó a lanzar a {target}. 🥴","drunk"),
    "eat": (["#comer"], "está comiendo un platillo delicioso. 🍔", "está compartiendo un almuerzo delicioso con {target}. 🍕","eat"),
    "facepalm": ([], "se dio una palmada en la frente por la decepción. 🤦‍♂️", "se dio un facepalm tras leer la tremenda pendejada que dijo {target}. 🤦‍♂️","facepalm"),
    "gaming": ([], "declaró que está ocupado dándole duro a los videojuegos. 🎮", "invitó a {target} a una partida intensa en cooperativo. 🎮","gaming"),
    "greet": (["#hi"], "mandó un saludo amigable a todos los del grupo! 👋", "le mandó un saludo muy especial a {target}. 👋","greet"),
    "happy": (["#feliz"], "está saltando de pura alegría y felicidad! 🎉", "celebra con descontrol junto a {target}. 🎉","happy"),
    "heat": ([], "se está quejando del perro calor que está haciendo. 🥵", "le está echando aire a {target} porque se está asando del calor. 🥵","heat"),
    "hug": ([], "está buscando un abrazo de alguien.", "le dio un fuerte y reconfortante abrazo a {target}. 🤗","hug"),
    "impregnate": (["#preg", "#preñar"], "está buscando a quién preñar en este chat. 🤰", "activó la acción ficticia y acaba de embarazar a {target}! 🤰","impregnate"),
    "jump": ([], "está dando saltos llenos de energía. 🦘", "está saltando de la emoción alrededor de {target}.","jump"),
    "kill": ([], "sacó un arma imaginaria y empezó a disparar.", "sacó un arma del arsenal místico y acabó con {target}. ☠️","kill"),
    "kiss": (["#muak"], "está mandando besos al aire. 💋", "le plantó un beso sumamente apasionado a {target}! 💋","kiss"),
    "kisscheek": (["#beso"], "se auto-besó la mano... qué triste.", "le dio un tierno y dulce beso en la mejilla a {target}. 😊","kisscheek"),
    "laugh": ([], "se está riendo descontroladamente en el chat. 🤣", "se está burlando y riendo a carcajadas en la cara de {target}. 🤣","laugh"),
    "lewd": ([], "se puso en modo cochambroso y lascivo. 😏", "le sugirió algo sumamente lascivo y cochino a {target}. 😏","lewd"),
    "lick": ([], "está lamiendo la pantalla de su celular.", "le dio una lamedura juguetona y extraña a {target}. 👅","lick"),
    "love": (["#amor"], "está profundamente enamorado de la vida. ❤️", "le declaró su amor eterno e incondicional a {target}. ❤️","love"),
    "nope": ([], "dejó una rotunda negativa en el chat. 🙅‍♂️", "le dijo firmemente que NO a la solicitud de {target}. 🙅‍♂️","nope"),
    "pat": ([], "quiere que alguien le acaricie la cabeza.", "le dio unas palmaditas suaves en la cabeza a {target}. 🫳","pat"),
    "poke": ([], "está picando el aire con el dedo.", "le picó el torso con el dedo a {target} para llamar su atención. 👉","poke"),
    "pout": ([], "hizo un puchero tierno de molestia. 🥺", "le hizo un berrinche y un puchero de molestia a {target}. 🥺","pout"),
    "psycho": ([], "se volvió loco, entró en modo psicópata desquiciado. 👁️👁️", "miró fijamente a {target} con ojos de psicópata de anime. 👁️👁️","psycho"),
    "punch": ([], "está tirando golpes al aire entrenando.", "le propinó un fuerte puñetazo directo en la cara a {target}! 👊","punch"),
    "push": ([], "se tropezó solo.", "empujó físicamente a {target} a un lado del camino. 🫷","push"),
    "run": ([], "salió corriendo a toda velocidad de una situación incómoda. 🏃‍♂️", "salió huyendo a mil por hora de {target}. 🏃‍♂️","run"),
    "sad": (["#triste"], "se siente bastante decaído y melancólico hoy. 😢", "se puso muy triste por la actitud de {target}. 😢","sad"),
    "scared": ([], "se pegó un susto tremendo con el chat! 😨", "quedó horrorizado ante la presencia de {target}. 😨","scared"),
    "scream": ([], "pegó un grito sónico ensordecedor! 😱", "le pegó un grito ensordecedor directamente en el oído a {target}. 😱","scream"),
    "seduce": ([], "está intentando lucir sexy.", "desplegó todo su encanto místico para seducir a {target}. 😏","seduce"),
    "shy": (["#timido"], "está actuando con mucha timidez escondiéndose tras las letras. 🫣", "se escondió detrás de un poste al ver pasar a {target}. 🫣","shy"),
    "sing": ([], "rompió a cantar sus openings de anime favoritos en voz alta! 🎤", "le dedicó una canción espectacular a {target}. 🎤","sing"),
    "slap": ([], "se dio una bofetada a sí mismo por error.", "¡ZAS! Le acomodó una bofetada sonora a {target} por desubicado. 👋","slap"),
    "sleep": ([], "se desconectó y se fue a dormir plácidamente. 💤", "se quedó dormido profundamente encima de {target}. 💤","sleep"),
    "smoke": ([], "encendió un cigarro virtual y se puso a reflexionar. 🚬", "le echó todo el humo del cigarro en la cara a {target}. 🚬","smoke"),
    "spit": (["#escupir"], "escupió en el suelo con desprecio. 💦", "escupió directamente a {target} en señal de asco y desprecio. 💦","spit"),
    "step": (["#pisar"], "pisó un chicle en la calle.", "pisó firmemente a {target} de forma interactiva. 👣","step"),
    "think": ([], "se puso a reflexionar profundamente sobre el sentido de la vida. 🤔", "está analizando detalladamente la lógica de {target}. 🤔","think"),
    "tickle": ([], "tiene cosquillas solo.", "le empezó a hacer cosquillas implacables a {target} hasta dejarlo sin aire! 😂","tickle"),
    "walk": ([], "está caminando tranquilamente por el grupo. 🚶‍♂️", "se fue a dar un paseo relajante junto a {target}. 🚶‍♂️","walk")
}



def manejar_anime(db, user_id, comando, args, ahora):
    usuario = db[user_id]
    
    comando_encontrado = None
    textos_y_prefijo = None
    
    for raiz, datos in TABLERO_REACCIONES.items():
        alias = datos[0]
        t_solo = datos[1]
        t_mencion = datos[2]
        prefijo_archivo = datos[3] if len(datos) > 3 else ""
        
        if comando == f"#{raiz}" or comando in alias:
            comando_encontrado = raiz
            textos_y_prefijo = (t_solo, t_mencion, prefijo_archivo)
            break
            
    if not comando_encontrado:
        return None
        
    t_solo, t_mencion, prefijo_archivo = textos_y_prefijo
    nombre_emisor = f"*{usuario['nombre']}*"
    
    foto_archivo = ""
    if prefijo_archivo:
        try:
            ruta_carpeta = os.path.join(os.path.dirname(__file__), 'imagenes')
            
            archivos_disponibles = [
                f for f in os.listdir(ruta_carpeta) 
                if f.lower().startswith(prefijo_archivo.lower()) and os.path.isfile(os.path.join(ruta_carpeta, f))
            ]
            
            if archivos_disponibles:
                foto_archivo = random.choice(archivos_disponibles)
            else:
                foto_archivo = f"8.jpeg"
        except Exception as e:
            print(f"Error al escanear la carpeta multimedia: {e}")
            foto_archivo = f"8.jpeg"

    if args and args[0].startswith("@"):
        mencion_sucia = args[0].lstrip("@").split("@")[0]
        numeros_target = "".join(filter(str.isdigit, mencion_sucia))
        
        target_name = None
        for id_existente in db.keys():
            numeros_existentes = "".join(filter(str.isdigit, id_existente))
            if numeros_target == numeros_existentes:
                target_name = f"*{db[id_existente]['nombre']}*"
                break
                
        if not target_name:
            target_name = args[0]
            
        mensaje_final = f"「✿」 {nombre_emisor} {t_mencion.format(target=target_name)}"
    else:
        mensaje_final = f"「✿」 {nombre_emisor} {t_solo}"
        
    return f"{mensaje_final}|{foto_archivo}"