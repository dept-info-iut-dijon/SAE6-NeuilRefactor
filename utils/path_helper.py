import sys
import os

def get_resource_path(relative_path):
    """ Retourne le bon chemin d'accès aux fichiers, que l'application soit packagée ou non """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)