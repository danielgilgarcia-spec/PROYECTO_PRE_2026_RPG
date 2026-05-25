"""
text.py  –  Todos los textos del juego.

Formato de cada pantalla de diálogo:
    {
        "speaker": str,           # nombre del hablante (se muestra en la caja)
        "text":    str,           # texto del bocadillo (\\n para saltos de línea)
        "color":   (r, g, b),     # color del nombre del hablante
        "image":   str,           # ruta imagen personaje (puede ser "")
        "image_background": str   # ruta fondo (puede ser "")
    }

Todas las líneas de texto están escritas para caber dentro del bocadillo
de 440 px de ancho que usa renderer.draw_dialog().  Máximo ~38 caracteres
por línea.  Usar \\n para forzar salto manual.
"""

# ── Colores base de personajes ────────────────────────────────────────────────
_ZORO   = (34,  139,  34)    # verde
_MIHAWK = (139,  69,  19)    # marrón oscuro
_PICA   = (180, 100,  20)    # naranja quemado
_KING   = (148,   0, 211)    # púrpura real
_NARR   = (255, 215,   0)    # dorado (narrador / sin imagen)


# ── Intro ─────────────────────────────────────────────────────────────────────
INTRO_SCREENS = [
    {
        "speaker": "",
        "title":   "",
        "text":    "En el Nuevo Mundo...\ntras salir de Wano, Zoro\ncomienza a tener unos extraños sueños.",
        "color":   _NARR,
        "image":   "",
    },
    {
        "speaker": "",
        "title":   "",
        "text":    "En ellos, escucha el eco de espadas\nchocando y una voz de mujer que susurra:\n\n«El filo definitivo solo nace\ndel combate eterno.»",
        "color":   _NARR,
        "image":   "",
    },
    {
        "speaker": "",
        "title":   "",
        "text":    "Zoro despierta solo en una isla\ndesconocida.  No sabe cómo llegó\naquí, y comienza a caminar...",
        "color":   _NARR,
        "image":   "",
    },
    {
        "speaker": "Zoro",
        "title":   "",
        "text":    "«Vaya, parece que se han vuelto\na perder todos...»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/history_bkg/fondo_historia.png",
    },
    {
        "speaker": "Zoro",
        "title":   "",
        "text":    "«Echaré un ojo a ver\nsi los encuentro.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/history_bkg/fondo_historia.png",
    },
    {
        "speaker": "",
        "title":   "",
        "text":    "Una figura misteriosa se dibuja\nen la niebla.  Su voz susurra:\n«Encuentra el camino del filo.»",
        "color":   _NARR,
        "image":   "",
    },
    {
        "speaker": "",
        "title":   "TU AVENTURA COMIENZA",
        "text":    "Usa las FLECHAS para moverte.\nUSA ESPACIO para interactuar.",
        "color":   (144, 238, 144),
        "image":   "",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
#  ENEMY 1 — MIHAWK
# ═══════════════════════════════════════════════════════════════════════════════
ENEMY1_DIALOG_PRE = [
    {
        "speaker": "Mihawk",
        "text":    "«Vaya… el cazador de piratas\nha vuelto.  ¿Sigues queriendo\nser el mejor espadachín?»",
        "color":   _MIHAWK,
        "image":   "assets/big_enemies/mihawk_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Hice una promesa...\nasí que voy a vencerte.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
    {
        "speaker": "Mihawk",
        "text":    "«Hm.  Tu ambición no ha\ncambiado… pero tu mirada sí.»",
        "color":   _MIHAWK,
        "image":   "assets/big_enemies/mihawk_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Esta vez no voy a perder.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
    {
        "speaker": "Mihawk",
        "text":    "«Bien.\nSería aburrido si siguieras\nsiendo débil.»",
        "color":   _MIHAWK,
        "image":   "assets/big_enemies/mihawk_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
    {
        "speaker": "Mihawk",
        "text":    "«Muéstrame lo que has\nmejorado con tus espadas.»",
        "color":   _MIHAWK,
        "image":   "assets/big_enemies/mihawk_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«¡Prepárate!»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
]

ENEMY1_DIALOG_POST = [
    {
        "speaker": "Mihawk",
        "text":    "«…Impresionante.»",
        "color":   _MIHAWK,
        "image":   "assets/big_enemies/mihawk_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Tch…  Como ves,\naún sigo en pie.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
    {
        "speaker": "Mihawk",
        "text":    "«Por un instante pensé que\nmorirías antes de lograrlo.»",
        "color":   _MIHAWK,
        "image":   "assets/big_enemies/mihawk_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«No puedo morir…\nhasta ser el mejor\nespadachín del mundo.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
    {
        "speaker": "Mihawk",
        "text":    "«Entonces supongo…\nque ese título ahora\nte pertenece.»",
        "color":   _MIHAWK,
        "image":   "assets/big_enemies/mihawk_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«No.  Solo significa que\nestoy un poco más cerca\nde conseguirlo.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Hmph…  Quizá el mundo\nde los espadachines aún tenga\nalgo interesante que ofrecer.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_mar.png",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
#  ENEMY 2 — PICA
# ═══════════════════════════════════════════════════════════════════════════════
ENEMY2_DIALOG_PRE = [
    {
        "speaker": "Pica",
        "text":    "«Así que el espadachín\nde los piratas del sombrero\nviene hasta aquí.»",
        "color":   _PICA,
        "image":   "assets/big_enemies/pica_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Pica.  Sabía que\nalgún día nos cruzaríamos.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
    {
        "speaker": "Pica",
        "text":    "«¿Crees que puedes con\nla piedra?  Nadie ha\nlogrado alcanzarme.»",
        "color":   _PICA,
        "image":   "assets/big_enemies/pica_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«La piedra se rompe.\nY yo tengo tres espadas\npara hacerlo.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
    {
        "speaker": "Pica",
        "text":    "«Jah.  ¡Que ver\nsi puedes atravesar\nesta roca!»",
        "color":   _PICA,
        "image":   "assets/big_enemies/pica_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Isla… cortada.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
    {
        "speaker": "Pica",
        "text":    "«¡¿QUÉ?!  ¡Imposible!\n¡Esa roca era de granito!»",
        "color":   _PICA,
        "image":   "assets/big_enemies/pica_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
]

ENEMY2_DIALOG_POST = [
    {
        "speaker": "Pica",
        "text":    "«No… no puede ser…»",
        "color":   _PICA,
        "image":   "assets/big_enemies/pica_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Te lo dije.  La piedra\nsiempre cede ante el filo.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
    {
        "speaker": "Pica",
        "text":    "«¿Cuánto más puedes crecer,\nespadachín?»",
        "color":   _PICA,
        "image":   "assets/big_enemies/pica_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Todo lo que haga falta\nhasta que nadie por encima\nde mí quede en pie.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
    {
        "speaker": "Pica",
        "text":    "«Doflamingo no te\nperdonará esto.»",
        "color":   _PICA,
        "image":   "assets/big_enemies/pica_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Que venga.  Tengo\ntres respuestas afiladas\npreparadas para él.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Uno menos.\nSigo adelante.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_desierto.png",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
#  ENEMY 3 — KING
# ═══════════════════════════════════════════════════════════════════════════════
ENEMY3_DIALOG_PRE = [
    {
        "speaker": "King",
        "text":    "«Zoro Roronoa.  He oído\nque derrotaste a Pica.\nNo debería sorprenderme.»",
        "color":   _KING,
        "image":   "assets/big_enemies/king_historia.png",
        "image_background": "assets/battle_backgrounds/bg_fortaleza.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«King.  El hombre\nalado de las llamas.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_fortaleza.png",
    },
    {
        "speaker": "King",
        "text":    "«¿Sabes por qué sigo\naquí después de Wano?\nPorque aún no terminé.»",
        "color":   _KING,
        "image":   "assets/big_enemies/king_historia.png",
        "image_background": "assets/battle_backgrounds/bg_fortaleza.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Yo tampoco.\nSigo buscando ese\nfilo definitivo.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_fortaleza.png",
    },
    {
        "speaker": "King",
        "text":    "«Enma… ese sable\nte eligió a ti.\nDemostrarás que lo mereces.»",
        "color":   _KING,
        "image":   "assets/big_enemies/king_historia.png",
        "image_background": "assets/battle_backgrounds/bg_fortaleza.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«No necesito demostrarlo.\nSolo necesito sobrevivir\ny seguir cortando.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_fortaleza.png",
    },
    {
        "speaker": "King",
        "text":    "«Entonces que el fuego\njuzgue si mereces\nese camino.»",
        "color":   _KING,
        "image":   "assets/big_enemies/king_historia.png",
        "image_background": "assets/battle_ecimientos/bg_fortaleza.png",
    },
]

ENEMY3_DIALOG_POST = [
    {
        "speaker": "King",
        "text":    "«Imposible…\n¿Cortaste incluso\nel fuego?»",
        "color":   _KING,
        "image":   "assets/big_enemies/king_historia.png",
        "image_background": "assets/battle_backgrounds/bg_fortaleza.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«El fuego no detiene\nun filo que va en serio.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_fortaleza.png",
    },
    {
        "speaker": "King",
        "text":    "«Sobreviví a Wano pensando\nque nadie me superaría\nen combate…»",
        "color":   _KING,
        "image":   "assets/big_enemies/king_historia.png",
        "image_background": "assets/battle_backgrounds/bg_fortaleza.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Nadie llega a la cima\nsin pasar por encima\nde alguien que lo era todo.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_fortaleza.png",
    },
    {
        "speaker": "King",
        "text":    "«¿A dónde vas\ncon esa fuerza,\nespadachín?»",
        "color":   _KING,
        "image":   "assets/big_enemies/king_historia.png",
        "image_background": "assets/battle_backgrounds/bg_fortaleza.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Al único lugar que\nimporta: más arriba.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_fortaleza.png",
    },
    {
        "speaker": "Zoro",
        "text":    "«Esto no acaba aquí.\nPero hoy, yo sigo\nen pie.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/battle_backgrounds/bg_fortaleza.png",
    },
]


# ── Pantalla final ────────────────────────────────────────────────────────────
FINAL_SCREENS = [
    {
        "speaker": "",
        "title":   "FIN",
        "text":    "Después de la gran batalla,\nreaparece la misteriosa niebla\ny se vuelve a escuchar la voz.",
        "color":   _NARR,
        "image":   "",
    },
    {
        "speaker": "",
        "title":   "",
        "text":    "La voz sonaba con\nmás intensidad…\ncasi como si gritara.",
        "color":   _NARR,
        "image":   "",
    },
    {
        "speaker": "",
        "title":   "",
        "text":    "«¡Zoro!»",
        "color":   _ZORO,
        "image":   "",
    },
    {
        "speaker": "",
        "title":   "",
        "text":    "«¡ZORO!»",
        "color":   _ZORO,
        "image":   "",
    },
    {
        "speaker": "",
        "title":   "",
        "text":    "«¡¡DESPIERTA!!»",
        "color":   _ZORO,
        "image":   "",
    },
    {
        "speaker": "",
        "title":   "",
        "text":    "La niebla se disipa\ny Zoro se levanta.",
        "color":   _NARR,
        "image":   "",
        "image_background": "assets/history_bkg/fondo_historia.png",
    },
    {
        "speaker": "Zoro",
        "title":   "",
        "text":    "«Vaya, todo había sido\nun sueño.  Pero ahora\nestoy despierto.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/history_bkg/fondo_historia.png",
    },
    {
        "speaker": "Zoro",
        "title":   "",
        "text":    "«Y no dejaré de luchar\npara alcanzar mi sueño.»",
        "color":   _ZORO,
        "image":   "assets/big_enemies/zoro_historia.png",
        "image_background": "assets/history_bkg/fondo_historia.png",
    },
]
