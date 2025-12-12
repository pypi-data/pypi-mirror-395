"""
Este es el módulo que incluye la clase
del reproductor de música
"""

class Player:
    """
    Esta clase crea un reproductor
    de música
    """

    def play(self, song):
        """
        Reproduce la canción que recibio
        como parámetro
        :param song: este es un string con el path de la canción
        :return: devuelve 1 si reproduce con exito, en caso de fracaso devuelve 0
        """
        print(f"Reproduciendo canción {song}")

    def stop(self):
        print("stopping")