"""
music.py  –  Gestión centralizada de música del juego.

Archivos esperados en assets/music/:
    music_battle.wav      -> combate
    music_dialogue.mp3    -> conversaciones (diálogos con jefes)
    music_explore.mp3     -> exploración del mapa
    music_story.ogg       -> narrativa (intro y cierre final)

Si un archivo no existe, falla silenciosamente sin romper el juego.
"""

import pygame

# Claves de estado musical
MUSIC_EXPLORE  = "explore"
MUSIC_BATTLE   = "battle"
MUSIC_STORY    = "story"
MUSIC_DIALOGUE = "dialogue"

_TRACKS = {
    MUSIC_EXPLORE:  "assets/music/music_explore.mp3",
    MUSIC_BATTLE:   "assets/music/music_battle.wav",
    MUSIC_STORY:    "assets/music/music_story.ogg",
    MUSIC_DIALOGUE: "assets/music/music_dialogue.mp3",
}

_current_track = None


def play(track_key: str, loops: int = -1, volume: float = 0.5):
    """
    Reproduce la pista indicada.
    Para la música actual primero (sin fade asíncrono) y luego carga la nueva.
    Si ya está sonando la misma pista, no hace nada.
    """
    global _current_track

    if track_key == _current_track:
        return

    path = _TRACKS.get(track_key)
    if not path:
        print(f"[music] Clave desconocida: '{track_key}'")
        return

    try:
        pygame.mixer.music.stop()       # stop síncrono, sin problemas de timing
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)
        _current_track = track_key
    except Exception as e:
        print(f"[music] No se pudo cargar '{path}': {e}")
        _current_track = None


def stop():
    """Para la música actual."""
    global _current_track
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass
    _current_track = None


def set_volume(volume: float):
    try:
        pygame.mixer.music.set_volume(volume)
    except Exception:
        pass