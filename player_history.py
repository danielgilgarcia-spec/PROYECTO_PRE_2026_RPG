"""
player_history.py  –  Esquema de referencia del historial de jugadores.

El historial real se persiste en 'player_history.txt' y se gestiona
íntegramente desde menu.py mediante load_history() y save_history().
Este módulo define únicamente la estructura esperada de cada entrada.

Estructura de cada entrada:
    {
        "name":       str,   # nombre del jugador
        "max_level":  int,   # nivel máximo alcanzado
        "difficulty": str,   # nombre de la dificultad ("Fácil", "Normal", "Difícil")
    }
"""

# Estructura de ejemplo (no se usa en tiempo de ejecución)
PLAYER_HISTORY_SCHEMA = {
    "name":       "",
    "max_level":  0,
    "difficulty": "",
}

# Mantenido por compatibilidad con imports existentes (lista vacía)
PLAYER_HISTORY = []