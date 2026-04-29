"""
music.py  –  Gestión centralizada de música del juego.

Rutas esperadas (formato .ogg recomendado, también acepta .mp3):
    assets/music/music_explore.ogg   -> exploración
    assets/music/music_battle.ogg    -> combate
    assets/music/music_story.ogg     -> diálogos / historia

Si un archivo no existe, el módulo falla silenciosamente sin romper el juego.
"""

import pygame

# Claves de estado musical
MUSIC_EXPLORE = "explore"
MUSIC_BATTLE  = "battle"
MUSIC_STORY   = "story"

_TRACKS = {
    MUSIC_EXPLORE: "assets/music/music_explore.ogg",
    MUSIC_BATTLE:  "assets/music/music_battle.ogg",
    MUSIC_STORY:   "assets/music/music_story.ogg",
}

_current_track = None


def play(track_key: str, loops: int = -1, volume: float = 0.5):
    """Reproduce la pista indicada. Si ya está sonando, no la reinicia."""
    global _current_track
    if track_key == _current_track:
        return
    path = _TRACKS.get(track_key)
    if not path:
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)
        _current_track = track_key
    except Exception as e:
        print(f"[music] No se pudo cargar '{path}': {e}")


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