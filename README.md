# Générateur de pavages

Cette application permet de générer à partir d'une tuile des pavages sphériques, euclidiens ou hyperboliques.

Cette application a été initialement conçue pour une formation organisée par l'académie de Versailles
à l'Institut Henri Poincaré en avril 2024 autour du thème *Mathématiques et création*.

## Installation

### Dépendances.

L'application nécessite [Python 3](https://www.python.org), 
ainsi que les bibliothèques [numpy](https://numpy.org/) et [PySide6](https://wiki.qt.io/Qt_for_Python).
On recommande d'installer ces bibliothèques grâce au gestionnaire de paquets [pip](https://pip.pypa.io/en/stable/) :

```shell
pip install numpy
pip install PySide6
```


### Installation

Télécharger le code source et le placer dans le dossier de votre choix.
L'application ne fonctionne pas pour le moment en "standalone".
Il faudra la lancer via un terminal (cf. ci-dessous).

## Fonctionnement

### Démarrer l'application

Pour lancer l'application 
- Lancer une fenêtre de terminal
- Naviguer jusqu'au dossier contenant le code l'application
- Lancer l'application avec la commande 
    ```shell
    python main.py
    ```
Une fenêtre (essentiellement vide) doit alors apparaître à l'écran

### Dessiner un pavage

- À partir du menu *Fichier* > *Ouvrir*, choisir un fichier image contenant une tuile du pavage à générer.
- À partir d'un des autres menus, choisir le type de pavage à générer.
- Suivant le pavage choisi, la forme de la tuile peut être un triangle, un rectangle, un carré, etc. 
Délimiter la tuile en cliquant sur les sommets de celle-ci avec la souris
- Cliquer sur le bouton *Dessiner le pavage* pour générer celui-ci.
- Une nouvelle fenêtre doit s'ouvrir avec le pavage dessiné.
Suivant le pavage, la fenêtre de rendu peut offrir certaines options (échelle, rotation, contraintes de formes, etc).

**Astuce** : La barre d'état de la fenêtre principale fournit quelques instructions sommaires.

**Avertissement** : 
Pour les pavages sphériques, la tuile demandée n'est pas nécessairement un domaine fondamental du groupe d'isométries utilisé.
Pour que le pavage soit cohérent, la tuile doit donc potentiellement respecter certaines symétries.

## Pour aller plus loin

Pour en savoir plus sur les mathématiques qui sous-tendent l'application, 
on pourra consulter par exemple les page Wikipédia suivantes :
- [Pavages de la sphère](https://fr.wikipedia.org/wiki/Pavage_de_la_sph%C3%A8re)
- [Pavages du plan](https://fr.wikipedia.org/wiki/Pavage_du_plan)
- [Groupes de papier-peint](https://fr.wikipedia.org/wiki/Groupe_de_papier_peint)

## Todo

- Ajouter un export des pavages générés sous forme de fichier image (jpg, png, avec choix de la résolution)
- Assurer la compatibilité de l'application sur tous les systèmes d'exploitation (Linux, Windows, OSX)
- Ajouter la possibilité de changer la couleur de fond pour le pavage hyperbolique (en incluant un canal alpha pour l'export image)
- Packager sous forme d'une application "standalone"
- Améliorer l'ergonomie générale de l'application (par exemple organiser l'application en une seule fenêtre)
- Ajouter une aide pour les utilisateurs (sous une forme à définir : indication dans la barre d'état, de bulles, d'un menu d'aide, etc)
- Traduire du logiciel en anglais
- Pour chaque pavage, ajouter un lien vers une documentation mathématique (page Wikipédia ou autre à définir)
- Ajouter un bouton pour partager le résultat d'un pavage sur les réseaux sociaux
- Ajouter un outil de dessin pour qu'au lieu de charger une image on puisse dessier une tuile et voir en temps réel les modifications sur le pavage calculé

### Fonctionnalités nécessitant des modifications en lien avec les maths

- Déplacer un pavage (sur la sphère / le plan / le plan hyperbolique) avec un "drag and drop" à la souris ou au clavier
- Ajouter les pavages sphériques manquants
- Ajouter les pavages triangulaires du plan hyperbolique

## Licence.

Le présent logiciel est distribué sous licence GNU [General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html), version 3 ou ultérieure

## Auteur

[Rémi Coulon](http://rcoulon.perso.math.cnrs.fr/) 
