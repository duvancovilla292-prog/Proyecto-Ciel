import random

CATALOGO_PERSONAJES = {
    #==================================================
    # Personajes de anime/manga | 4 estrellas | ★★★★
    #==================================================
    "Ciel": {
        "serie": "Tensura",
        "rareza": "Legendario",
        "estrellas": "★★★★",
        "puntos": 3,
        "valor_venta": 2500,
        "imagen": "ciel.jpeg",
        "descripcion": "La evolución del 'Gran Sabio' y 'Rafael'. Un Manas (núcleo inteligente espiritual) con un procesamiento lógico optimizado al 100% y consejera perfecta.",
        "visuales": ["🌐  [🧠] 🌐\n⚡ (  • ̀ω•́  ) 📊 < *Análisis lógico completo. Optimización de datos al 100%.*"]
    },
    "Sung Jin-woo": {
        "serie": "Solo Leveling",
        "rareza": "Legendario",
        "estrellas": "★★★★",
        "puntos": 10,
        "valor_venta": 15000,
        "imagen": "ll1.jpeg",
        "descripcion": "El Monarca de las Sombras. Pasó de ser el cazador más débil a un ser absoluto capaz de revivir a los caídos como sus soldados de sombras.",
        "visuales": ["⬛  [👁️] ⬛\n👑 (🔥_🔥) ⚔️  < *¡ALZATE (ARISE)!*"]
    },
    "Veldora Tempest": {
        "serie": "Tensura",
        "rareza": "Legendario",
        "estrellas": "★★★★",
        "puntos": 10,
        "valor_venta": 15000,
        "imagen": "Veldora.jpg",
        "descripcion": "El Dragón de la Tormenta, uno de los cuatro Dragones Verdaderos y el mejor amigo de Rimuru. Amante del manga, el caos y desatar su inmenso poder.",
        "visuales": ["⚡  [🐉] ⚡\n✨ (◣_◢) 💥  < *¡Kuajaja! ¡Es hora de usar el Kamehameha!*"]
    },
    "Diablo": {
        "serie": "Tensura",
        "rareza": "Legendario",
        "estrellas": "★★★★",
        "puntos": 10,
        "valor_venta": 15000,
        "imagen": "diablo.jpeg",
        "descripcion": "El Demonio Primordial Negro (Noir). Obsesionado con servir fielmente a Rimuru, su elegancia es tan inmensa como su crueldad hacia sus enemigos.",
        "visuales": ["🔴  [🧤] 🔴\n🤝 (  ͡° ͜ʖ ͡° ) 🍷 < *Todo sea por la absoluta voluntad de Rimuru-sama.*"]
    },
    "Veldanava": {
        "serie": "Tensura",
        "rareza": "Legendario",
        "estrellas": "★★★★",
        "puntos": 10,
        "valor_venta": 15000,
        "imagen": "veldanava.jpeg",
        "descripcion": "El Dragón Estelar de la Creación y el Dios original de todo el multiverso. Su poder omnipresente e intelecto absoluto dieron forma a la existencia misma.",
        "visuales": ["🌌  [✨] 🌌\n🪐 (  👁️_👁️ ) 🪐 < *Yo soy el principio y el fin de la realidad.*"]
    },
    "Albert Einstein": {
        "serie": "Ciencia",
        "rareza": "Legendario",
        "estrellas": "★★★★",
        "puntos": 10,
        "valor_venta": 15000,
        "imagen": "Albert.jpeg",
        "descripcion": "El físico teórico más famoso de la historia. Dominó el tejido del espacio-tiempo con su Teoría de la Relatividad y redefinió las leyes universales.",
        "visuales": ["🌌  [🧠] 🌌\n✨ (  ͡° 🧮 ͡° ) 💫  < *E = mc²... El espacio y el tiempo son relativos.*"]
    },
    "Guy Crimson": {
        "serie": "Tensura",
        "rareza": "Legendario",
        "estrellas": "★★★★",
        "puntos": 10,
        "valor_venta": 15000,
        "imagen": "guy.jpeg",
        "descripcion": "El Primordial Rojo (Rouge) y líder indiscutible de los Reyes Demonios de la Octagrama. Balancea el orden del mundo entero con su sola presencia.",
        "visuales": ["🔥  [👑] 🔥\n🍷 (🔥_🔥) 🗡️   < *El poder sin control no es más que un espectáculo barato.*"]
    },
    "Ryomen Sukuna": {
        "serie": "Jujutsu Kaisen",
        "rareza": "Legendario",
        "estrellas": "★★★★",
        "puntos": 10,
        "valor_venta": 15000,
        "imagen": "sukuna.jpeg",
        "descripcion": "El Rey de las Maldiciones. Un ser despiadado de la era Heian capaz de cortar la existencia misma con su Expansión de Dominio: Relicario Malévolo.",
        "visuales": ["💀  [👁️] 💀\n07 (◣_◢) 🩸   < *¡Párense firmes, insectos! Secar y Cortar.*"]
    },
    "Rimuru Tempest": {
        "serie": "Tensura",
        "rareza": "Legendario",
        "estrellas": "★★★★",
        "puntos": 10,
        "valor_venta": 15000,
        "imagen": "8.jpeg",
        "descripcion": "El fundador y rey de la Federación Jura Tempest. Un Slime extrañamente poderoso con la habilidad de devorar y copiar habilidades.",
        "visuales": ["🔹  [🔵] 🔹\n  ( • ω • )  < *¡Hola!*", "⚔️  [👤] ⚔️\n  空 (🔥_🔥) 斬  < *¡Forma Humana!*"]
    },
    "Gojo Satoru": {
        "serie": "Jujutsu Kaisen",
        "rareza": "Legendario",
        "estrellas": "★★★★",
        "puntos": 10,
        "valor_venta": 15000,
        "imagen": "https://i.imgur.com/GojoLegendary.png",
        "descripcion": "El chamán más fuerte del mundo. Poseedor de los Seis Ojos y la técnica de Infinito. Nadie puede tocarlo.",
        "visuales": ["👁️  [🕶️] 👁️\n  (  ͡° ͜ʖ ͡° )  < *No te preocupes, soy el más fuerte.*"]
    },

    #==================================================
    # Personajes de anime/manga | 3 estrellas | ★★★
    #==================================================

    "Senku Ishigami": {
        "serie": "Dr. Stone",
        "rareza": "Épico",
        "estrellas": "★★★",
        "puntos": 5,
        "valor_venta": 6000,
        "imagen": "senku.jpg",
        "descripcion": "Un genio científico determinado a reconstruir la civilización desde cero utilizando el poder de la ciencia pura tras 3700 años de petrificación.",
        "visuales": ["🧪  [🥬] 🧪\n🚀 (  • ̀ω•́  ) 🔬 < *¡Esto es un diez mil millones por ciento emocionante!*"]
    },
    "Milim Nava": {
        "serie": "Tensura",
        "rareza": "Épico",
        "estrellas": "★★★",
        "puntos": 5,
        "valor_venta": 6000,
        "imagen": "https://i.imgur.com/MilimDestroyer.png",
        "descripcion": "Uno de los Reyes Demonios más antiguos. Es conocida como 'La Destructora', poseyendo la mente de una niña inquieta y un poder de destrucción apocalíptico.",
        "visuales": ["🎀  [🍡] 🎀\n✨ ( ＞ヮ＜ ) ✨ < *¡Rimuru y yo somos mejores amigos del alma!*"]
    },
    "Benimaru": {
        "serie": "Tensura",
        "rareza": "Épico",
        "estrellas": "★★★",
        "puntos": 5,
        "valor_venta": 6000,
        "imagen": "benimaru.jpg",
        "descripcion": "El Comandante General del ejército de Tempest. Un Kijin de fuego bendecido con un liderazgo nato y letales habilidades tácticas de combate.",
        "visuales": ["🔥  [⚔️] 🔥\n👹 (🔥_🔥) 🗡️  < *¡Ardan en las Llamas del Purgatorio!*"]
    },
    "Tsukasa Shishio": {
        "serie": "Dr. Stone",
        "rareza": "Épico",
        "estrellas": "★★★",
        "puntos": 5,
        "valor_venta": 6000,
        "imagen": "sukasa.jpeg",
        "descripcion": "El estudiante de preparatoria más fuerte de todos. Su fuerza física le permite abatir leones a puño limpio, buscando crear un mundo primitivo e incorrupto.",
        "visuales": ["🦁  [🥊] 🦁\n💪 (◣_◢) 🦴     < *Estableceré un nuevo mundo libre de tecnología y adultos.*"]
    },
    "Dr. Xeno Houston": {
        "serie": "Dr. Stone",
        "rareza": "Épico",
        "estrellas": "★★★",
        "puntos": 5,
        "valor_venta": 6000,
        "imagen": "xeno.webp",
        "descripcion": "Un brillante ex-científico de la NASA que lidera la colonia americana. Su dominio de la ingeniería militar busca imponer el control absoluto.",
        "visuales": ["🔫  [⚙️] 🔫\n🚬 (  ͡~ ͜ʖ ͡° ) 🧪 < *La ciencia es elegante, pero el verdadero fin es el control.*"]
    },
    "Shion": {
        "serie": "Tensura",
        "rareza": "Épico",
        "estrellas": "★★★",
        "puntos": 5,
        "valor_venta": 6000,
        "imagen": "https://i.imgur.com/ShionSecretary.png",
        "descripcion": "La secretaria número uno y fiel guardaespaldas de Rimuru. Su habilidad única 'Cocinero' altera la causalidad, aunque sus platillos luzcan aterradores.",
        "visuales": ["💜  [🍲] 💜\n🥋 (  • ̀ω•́  ) 🗡️  < *¡Rimuru-sama! He preparado un almuerzo delicioso para usted.*"]
    },
    "Ryusui Nanami": {
        "serie": "Dr. Stone",
        "rareza": "Épico",
        "estrellas": "★★★",
        "puntos": 5,
        "valor_venta": 6000,
        "imagen": "riusui.jpg",
        "descripcion": "El codicioso y extraordinario navegante del Reino de la Ciencia. Su ambición impulsa la economía del nuevo mundo bajo su lema: ¡El deseo es justicia!",
        "visuales": ["🚢  [🪙] 🚢\n🎩 (  ͡💸 ͜ʖ ͡° ) 🌊 < *¡Todo en este mundo me pertenece! ¡Ja-ha!*"]
    },
    "Megumin": {
        "serie": "Konosuba",
        "rareza": "Épico",
        "estrellas": "★★★",
        "puntos": 5,
        "valor_venta": 6000,
        "imagen": "https://i.imgur.com/MeguminExplosion.png",
        "descripcion": "Archimaga del clan de los Demonios Carmesí. Dedicó todo su talento exclusivamente a perfeccionar un único hechizo místico: ¡Explosion!",
        "visuales": ["💥  [🧙‍♀️] 💥\n✨ (🔥_🔥) 🪄   < *¡EXPLOSIONNNN!* _(Se cae al suelo agotada)_"]
    },
    "Ben Tennyson": {
        "serie": "Ben 10",
        "rareza": "Épico",
        "estrellas": "★★★",
        "puntos": 5,
        "valor_venta": 6000,
        "imagen": "https://i.imgur.com/Ben10Epic.png",
        "descripcion": "Un chico normal de 10 años que encontró un reloj alienígena intergaláctico. ¡Es hora de ser héroe!",
        "visuales": ["⌚  [👽] ⌚\n  ( 🟢_🟢 )  < *¡Omnitrix activado!*"]
    },
    "Cid Kagenou": {
        "serie": "The Eminence in Shadow",
        "rareza": "Épico",
        "estrellas": "★★★",
        "puntos": 5,
        "valor_venta": 6000,
        "imagen": "https://i.imgur.com/CidEpic.png",
        "descripcion": "Líder de Shadow Garden. No le interesa ser el héroe ni el villano, él opera desde las sombras.",
        "visuales": ["⬛  [🧥] ⬛\n  (  👁️_👁️ )  < *I am... Atomic.*"]
    },

    #==================================================
    # Personajes de anime/manga | 2 estrellas | ★★
    #==================================================

    "Shuna": {
        "serie": "Tensura",
        "rareza": "Raro",
        "estrellas": "★★",
        "puntos": 3,
        "valor_venta": 2500,
        "imagen": "https://i.imgur.com/ShunaPrincess.png",
        "descripcion": "La princesa de los Kijin, experta en alta cocina y magia de soporte. Su dulce sonrisa esconde un aura intimidante que asusta al propio Rimuru.",
        "visuales": ["🌸  [🍵] 🌸\n👘 (✿ • ‿ • ) ✨ < *¿Rimuru-sama, prefiere mi comida o la de Shion?*"]
    },
    "Gen Asagiri": {
        "serie": "Dr. Stone",
        "rareza": "Raro",
        "estrellas": "★★",
        "puntos": 3,
        "valor_venta": 2500,
        "imagen": "gen.jpeg",
        "descripcion": "El astuto mentalista y psicólogo experto en la manipulación social. Es la mano derecha de Senku para manejar tratos difíciles e intrigas.",
        "visuales": ["🃏  [🎭] 🃏\n👘 (  ͡~ ͜ʖ ͡° ) 🥤  < *Solo soy un simple psicólogo superficial...*"]
    },
    "Chrome": {
        "serie": "Dr. Stone",
        "rareza": "Raro",
        "estrellas": "★★",
        "puntos": 3,
        "valor_venta": 2500,
        "imagen": "https://i.imgur.com/ChromeScience.png",
        "descripcion": "El 'hechicero' nativo del nuevo mundo que redescubrió la química por su cuenta recolectando minerales. Fiel discípulo y compañero de Senku.",
        "visuales": ["🪨  [🧪] 🪨\n⚒️ ( ⊙_⊙ ) 🔥   < *¡Esto no es brujería, esto es increíblemente genial!*"]
    },
    "Alpha": {
        "serie": "The Eminence in Shadow",
        "rareza": "Raro",
        "estrellas": "★★",
        "puntos": 3,
        "valor_venta": 2500,
        "imagen": "https://i.imgur.com/AlphaShadow.png",
        "descripcion": "La primera integrante y segunda al mando de Shadow Garden. Maneja impecablemente la organización desde las sombras con una lógica intachable.",
        "visuales": ["⬛  [📜] ⬛\n✨ ( • ω • ) ⚔️   < *Todo marcha en estricto orden de acuerdo al plan de Shadow-sama.*"]
    },
    "Isagi Yoichi": {
        "serie": "Blue Lock",
        "rareza": "Raro",
        "estrellas": "★★",
        "puntos": 3,
        "valor_venta": 2500,
        "imagen": "https://i.imgur.com/IsagiRare.png",
        "descripcion": "Un delantero que busca destruir el fútbol tradicional para convertirse en el egoísta definitivo de Blue Lock.",
        "visuales": ["⚽  [🏃‍♂️] ⚽\n  ( 🧩_🧩 )  < *¡Puedo ver las piezas del rompecabezas!*"]
    },
    "Megumi Fushiguro": {
        "serie": "Jujutsu Kaisen",
        "rareza": "Raro",
        "estrellas": "★★",
        "puntos": 3,
        "valor_venta": 2500,
        "imagen": "https://i.imgur.com/MegumiRare.png",
        "descripcion": "Chamán de primer grado que utiliza la técnica de las Diez Sombras para invocar Shikigamis.",
        "visuales": ["🐺  [👥] 🐺\n  (  🦹‍♂️_🦹‍♂️ )  < *¡Furia del Tigre y el Toro!*"]
    },

    #==================================================
    # Personajes de anime/manga | 1 estrella | ★
    #==================================================

    "Suika": {
        "serie": "Dr. Stone",
        "rareza": "Común",
        "estrellas": "★",
        "puntos": 1,
        "valor_venta": 1000,
        "imagen": "https://i.imgur.com/SuikaMelon.png",
        "descripcion": "Una tierna niña del Reino de la Ciencia que usa una cáscara de sandía para corregir su visión borrosa. Actúa como la espía perfecta.",
        "visuales": ["🍉  [👀] 🍉\n🤸 ( • ω • ) 🍃  < *¡Suika al rescate e investigación, de verdad!*"]
    },
    "Taiju Oki": {
        "serie": "Dr. Stone",
        "rareza": "Común",
        "estrellas": "★",
        "puntos": 1,
        "valor_venta": 1000,
        "imagen": "https://i.imgur.com/TaijuStone.png",
        "descripcion": "El mejor amigo de Senku, poseedor de una resistencia infinita y fuerza descomunal, manteniendo una estricta política de cero violencia.",
        "visuales": ["🪵  [💪] 🪵\n🗣️ (◣_◢)💥     < *¡SENKUUUU! ¡HE RECOLECTADO DIEZ MIL TRONCOS DE MADERA!*"]
    },
    "Yuzuriha Ogawa": {
        "serie": "Dr. Stone",
        "rareza": "Común",
        "estrellas": "★",
        "puntos": 1,
        "valor_venta": 1000,
        "imagen": "https://i.imgur.com/YuzurihaCraft.png",
        "descripcion": "Experta en artesanía, costura y reconstrucción textil. Su paciencia es vital para rearmar los fragmentos petrificados rotos de los humanos.",
        "visuales": ["🧵  [🌸] 🧵\n🎀 (✿ • ‿ • ) ✂️  < *¡Puedo coser y reparar cualquier tejido roto de inmediato!*"]
    },
    "Rigurd": {
        "serie": "Tensura",
        "rareza": "Común",
        "estrellas": "★",
        "puntos": 1,
        "valor_venta": 1000,
        "imagen": "https://i.imgur.com/RigurdGoblin.png",
        "descripcion": "El leal líder de los Goblins que pasó de ser un anciano débil a un musculoso sub-líder tras recibir un nombre de Rimuru.",
        "visuales": ["🍃  [💪] 🍃\n🧌 (🔥_🔥) ✨   < *¡RIMURU-SAMA ES NUESTRO SUPREMO LÍDER! ¡KUAJAAAA!*"]
    },
    "Fuego": {
        "serie": "Ben 10",
        "rareza": "Común",
        "estrellas": "★",
        "puntos": 1,
        "valor_venta": 1000,
        "imagen": "https://i.imgur.com/FuegoCommon.png",
        "descripcion": "Una forma de vida basada en plasma originaria de la estrella Pyros. Puede controlar el fuego a voluntad.",
        "visuales": ["🔥  [☄️] 🔥\n  ( 🔥_🔥 )  < *¡Está quemando!*"]
    },
    "Gobta": {
        "serie": "Tensura",
        "rareza": "Común",
        "estrellas": "★",
        "puntos": 1,
        "valor_venta": 1000,
        "imagen": "https://i.imgur.com/GobtaCommon.png",
        "descripcion": "Un duendecillo de Tempest que, a pesar de su apariencia tonta, es un genio oculto del combate.",
        "visuales": ["🍃  [👺] 🍃\n  ( ⊙_⊙ )  < *¡S-Sí, Rimuru-sama!*"]
    }
}

PRODUCTOS_TIENDA = {
    "ticket_epico": {"nombre": "Ticket Épico", "precio": 15000, "desc": "Asegura un personaje de 3 o 4 estrellas."},
    "amuleto": {"nombre": "Amuleto de Suerte", "precio": 25000, "desc": "Duplica los rates de Legendarios por 3 tiros."}
}

def manejar_gacha(db, user_id, comando, args, ahora):
    usuario = db[user_id]
    
    if "inventario" not in usuario: usuario["inventario"] = {}
    if "objetos" not in usuario: usuario["objetos"] = {}
    if "tiros_totales" not in usuario: usuario["tiros_totales"] = 0

    if comando in ["#gacha", "#pull", "#roll"]:
        costo_tiro = 5000
        if usuario["billetera"] < costo_tiro:
            return f"《✧》No tienes suficientes Coins en efectivo. Cada tiro cuesta *¥{costo_tiro:,}* Coins."
        
        usuario["billetera"] -= costo_tiro
        usuario["tiros_totales"] += 1
        
        azar = random.random()
        if azar < 0.05:     rareza_elegida = "Legendario"
        elif azar < 0.20:   rareza_elegida = "Épico"
        elif azar < 0.50:   rareza_elegida = "Raro"
        else:               rareza_elegida = "Común"
        
        opciones = [p for p, d in CATALOGO_PERSONAJES.items() if d["rareza"] == rareza_elegida]
        personaje = random.choice(opciones)
        datos_p = CATALOGO_PERSONAJES[personaje]
        
        usuario["inventario"][personaje] = usuario["inventario"].get(personaje, 0) + 1
        es_nuevo = "✨ *¡Has obtenido un nuevo personaje!*" if usuario["inventario"][personaje] == 1 else f"🔄 *¡Personaje repetido!* (Tienes x{usuario['inventario'][personaje]})"
        
        visual = random.choice(datos_p["visuales"])
        
        texto_respuesta = (
            f"「✿」*》》GACHA SPIN @{usuario['nombre']}《《*\n\n"
            f"🔮 La esfera mística brilla con fuerza...\n"
            f"{es_nuevo}\n\n"
            f"{visual}\n\n"
            f"👤 *Nombre:* {personaje} [{datos_p['serie']}]\n"
            f"🌟 *Rareza:* {datos_p['rareza']} ({datos_p['estrellas']})\n\n"
            f"> _¡Usa #chars para ver tu colección actual!_"
        )
        
        return f"{texto_respuesta}|{datos_p['imagen']}"

    elif comando in ["#characters", "#chars", "#personajes"]:
        if not usuario["inventario"]:
            return "《✧》Tu inventario está vacío. ¡Usa *#gacha* para empezar tu colección!"
            
        pag = int(args[0]) if args and args[0].isdigit() else 1
        items = list(usuario["inventario"].items())
        items_por_pag = 10
        total_pags = (len(items) - 1) // items_por_pag + 1
        
        if pag < 1 or pag > total_pags:
            return f"《✧》Página inválida. Tu inventario tiene {total_pags} página(s)."
            
        start = (pag - 1) * items_por_pag
        end = start + items_por_pag
        
        respuesta = f"「✿」*》》INVENTARIO @{usuario['nombre']}《《*\n\n🔮 Tu colección actual:\n\n"
        for idx, (char, copias) in enumerate(items[start:end], start=start+1):
            datos_p = CATALOGO_PERSONAJES[char]
            emoji = "👑" if datos_p["rareza"] == "Legendario" else "🧪" if datos_p["rareza"] == "Épico" else "⚔️" if datos_p["rareza"] == "Raro" else "🍃"
            respuesta += f"{emoji} {idx} » *{char}* (x{copias}) - {datos_p['estrellas']}\n"
            
        respuesta += f"\n> • Página *{pag}* de *{total_pags}*\n> _Uso: #chars [número de página]_"
        return respuesta

    elif comando in ["#gachashop", "#shop"]:
        respuesta = "「✿」*》》TIENDA GACHA《《*\n\n🛒 Gasta tus Coins en mano para ventajas místicas:\n\n"
        for k, v in PRODUCTOS_TIENDA.items():
            respuesta += f"🎫 » *{v['nombre']}* (id: {k})\n\t\t Precio: *¥{v['precio']:,} Coins*\n\t\t _Desc: {v['desc']}_\n\n"
        respuesta += "> _Para comprar usa: #buy [id] [cantidad]_"
        return respuesta
        
    elif comando == "#buy":
        if len(args) < 2: return "《✧》Uso correcto: #buy [id] [cantidad]"
        prod_id = args[0].lower()
        try: cant = int(args[1])
        except ValueError: return "《✧》Cantidad inválida."
        
        if prod_id not in PRODUCTOS_TIENDA or cant <= 0: return "《✧》ID de producto o cantidad inválida."
        
        costo_total = PRODUCTOS_TIENDA[prod_id]["precio"] * cant
        if usuario["billetera"] < costo_total: return "《✧>No tienes suficientes Coins en la billetera."
        
        usuario["billetera"] -= costo_total
        usuario["objetos"][prod_id] = usuario["objetos"].get(prod_id, 0) + cant
        return f"✿ Compraste x{cant} *{PRODUCTOS_TIENDA[prod_id]['nombre']}* exitosamente."

    elif comando in ["#gachaboard", "#topgacha", "#gtop"]:
        rank = []
        for uid, udata in db.items():
            inv = udata.get("inventario", {})
            puntos_u = sum(CATALOGO_PERSONAJES[c]["puntos"] * copias for c, copias in inv.items() if c in CATALOGO_PERSONAJES)
            rank.append((udata["nombre"], puntos_u, len(inv)))
            
        rank = sorted(rank, key=lambda x: x[1], reverse=True)
        respuesta = "「✿」Los mayores coleccionistas del grupo son:\n\n"
        for idx, (name, pts, distinct) in enumerate(rank[:10], start=1):
            respuesta += f"✰ {idx} » *{name}:*\n\t\t Colección→ *{pts} Puntos ({distinct} Chars)*\n"
        return respuesta + "\n> • Página *1* de *1*"

    elif comando in ["#gachainfo", "#ginfo"]:
        distinct = len(usuario["inventario"])
        total_global = len(CATALOGO_PERSONAJES)
        porcentaje = int((distinct / total_global) * 100) if total_global > 0 else 0
        fav = max(usuario["inventario"].items(), key=lambda x: x[1])[0] if usuario["inventario"] else "Ninguno"
        
        return (
            f"「✿」*》》ESTADÍSTICAS GACHA @{usuario['nombre']}《《*\n\n"
            f"🔮 Progreso en el multiverso:\n\n"
            f"🎫 Tiros totales » *{usuario['tiros_totales']} Giros*\n"
            f"🧩 Progreso global » *{distinct} / {total_global} Personajes ({porcentaje}%)*\n"
            f"👑 Favorito actual » *{fav}*\n\n"
            f"🎰 *Rates Base:* L: 5% - E: 15% - R: 30% - C: 50%"
        )

    elif comando in ["#gachasell", "#sellchar", "#vender"]:
        if not args: return "《✧》Escribe el nombre del personaje que quieres vender."
        busqueda = " ".join(args).lower()
        
        char_encontrado = None
        for c in usuario["inventario"].keys():
            if busqueda in c.lower():
                char_encontrado = c
                break
                
        if not char_encontrado: return "《✧》No tienes ese personaje en tu inventario."
        if usuario["inventario"][char_encontrado] <= 1:
            return f"《✧》No puedes vender tu única copia de *{char_encontrado}*. ¡Te quedarías sin él!"
            
        datos_p = CATALOGO_PERSONAJES[char_encontrado]
        usuario["inventario"][char_encontrado] -= 1
        usuario["billetera"] += datos_p["valor_venta"]
        
        return (
            f"「✿」*》》VENTA EXITOSA @{usuario['nombre']}《《*\n\n"
            f"💰 Has reciclado 1 copia repetida.\n\n"
            f"👤 *Personaje:* {char_encontrado}\n"
            f"🌟 *Rareza:* {datos_p['rareza']}\n"
            f"🪙 *Reembolso:* *+¥{datos_p['valor_venta']:,} Coins* directas a tu billetera."
        )

    elif comando in ["#gachagive", "#givechar", "#regalar"]:
        if len(args) < 2: return "《✧》Uso correcto: #regalar [@mención] [nombre_personaje]"
        target_mention = args[0]
        busqueda = " ".join(args[1:]).lower()
        
        char_encontrado = None
        for c in usuario["inventario"].keys():
            if busqueda in c.lower():
                char_encontrado = c
                break
                
        if not char_encontrado: return "《✧》No tienes ese personaje o escribiste mal el nombre."
        if usuario["inventario"][char_encontrado] <= 1:
            return f"《✧》No puedes regalar tu única copia de *{char_encontrado}*."
            
        target_id = target_mention.replace("@", "")
        if not target_id.endswith("@s.whatsapp.net"):
            target_id = f"{target_id}@s.whatsapp.net"
            
        if target_id == user_id:
            return "《✧》No puedes regalarte personajes a ti mismo."
            
        if target_id not in db: return "《✧》El usuario receptor no está registrado."
        
        if "inventario" not in db[target_id]: db[target_id]["inventario"] = {}
        
        usuario["inventario"][char_encontrado] -= 1
        db[target_id]["inventario"][char_encontrado] = db[target_id]["inventario"].get(char_encontrado, 0) + 1
        datos_p = CATALOGO_PERSONAJES[char_encontrado]
        
        return (
            f"「✿」*》》REGALO ENVIADO MÍSTICAMENTE《《*\n\n"
            f"🎁 ¡Un personaje ha cambiado de dueño!\n\n"
            f"👤 *De:* @{usuario['nombre']}\n"
            f"👥 *Para:* {target_mention}\n"
            f"🃏 *Personaje:* {char_encontrado} [{datos_p['serie']}]\n"
            f"⭐ *Rareza:* {datos_p['rareza']} ({datos_p['estrellas']})"
        )

    elif comando in ["#charinfo", "#winfo", "#waifuinfo"]:
        if not args: return "《✧》Ingresa el nombre de un personaje."
        busqueda = " ".join(args).lower()
        
        for name, data in CATALOGO_PERSONAJES.items():
            if busqueda in name.lower():
                texto_info = (
                    f"「✿」*》》INFORMACIÓN DE PERSONAJE《《*\n\n"
                    f"👤 *Nombre:* {name}\n"
                    f"📺 *Serie:* {data['serie']}\n"
                    f"🌟 *Rareza:* {data['rareza']} ({data['estrellas']})\n\n"
                    f"📝 *Descripción:* {data['descripcion']}"
                )

                return f"{texto_info}|{data['imagen']}"
        return "《✧》Personaje no encontrado en el catálogo místico."

    elif comando in ["#charimage", "#wimage", "#cimage"]:
        if not args: return "《✧》Ingresa el nombre de un personaje."
        busqueda = " ".join(args).lower()
        
        for name, data in CATALOGO_PERSONAJES.items():
            if busqueda in name.lower():
                texto_galeria = (
                    f"「✿」*》》GALERÍA MÍSTICA《《*\n\n"
                    f"👤 *Personaje:* {name} [{data['serie']}]\n"
                    f"🌟 *Rareza:* {data['rareza']}\n"
                )

                return f"{texto_galeria}|{data['imagen']}"
        return "《✧》No se encontró imagen para ese personaje."

    return None