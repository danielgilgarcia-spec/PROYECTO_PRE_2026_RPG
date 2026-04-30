"""
music.py  –  Gestión centralizada de música del juego.

Rutas esperadas:
    assets/music/music_explore.ogg   -> exploración
    assets/music/music_battle.ogg    -> combate
    assets/music/music_story.ogg     -> narrativa / historia
    assets/music/music_dialogue.ogg  -> conversaciones (enemigo vs héroe)

Si un archivo no existe, el módulo falla silenciosamente sin romper el juego.
"""

import pygame

# Claves de estado musical
MUSIC_EXPLORE = "explore"
MUSIC_BATTLE  = "battle"
MUSIC_STORY   = "story"
MUSIC_DIALOGUE = "dialogue"

_TRACKS = {
    MUSIC_EXPLORE: "assets/music/music_explore.mp3",
    MUSIC_BATTLE:  "assets/music/music_battle.ogg",
    MUSIC_STORY:   "assets/music/music_story.ogg",
    MUSIC_DIALOGUE: "assets/music/music_dialogue.mp3",
}

_current_track = None


def play(track_key: str, loops: int = -1, volume: float = 0.5, fade_ms: int = 500):
    """Reproduce la pista indicada con transición suave."""
    global _current_track

    if track_key == _current_track:
        return

    path = _TRACKS.get(track_key)
    if not path:
        return

    try:
        pygame.mixer.music.fadeout(fade_ms)
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops, fade_ms=fade_ms)
        _current_track = track_key
    except Exception as e:
        print(f"[music] No se pudo cargar '{path}': {e}")


def stop(fade_ms: int = 300):
    """Para la música actual con fade."""
    global _current_track
    try:
        pygame.mixer.music.fadeout(fade_ms)
    except Exception:
        pass
    _current_track = None


def set_volume(volume: float):
    try:
        pygame.mixer.music.set_volume(volume)
    except Exception:
        pass