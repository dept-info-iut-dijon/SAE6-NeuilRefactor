# **Générateur de pavages**  

Cette application permet de générer, à partir d'une tuile, des **pavages sphériques, euclidiens ou hyperboliques**.  

L’application a été initialement conçue pour une formation organisée par l’**académie de Versailles** à l’**Institut Henri Poincaré** en avril 2024 autour du thème *Mathématiques et création*.

---

## **📥 Installation et exécution**  

### **🔗 Version standalone (Windows uniquement)**  
L’application est disponible sous forme d’un exécutable **Windows** prêt à l’emploi, sans installation nécessaire.  

📌 **Téléchargement**  
1. Récupérer le fichier **`GenerateurPavages.exe`** disponible dans **`dist/`** de la branche `main` du dépôt.  
2. Placer le fichier dans un dossier de votre choix.  

📌 **Exécution**  
- **Double-cliquer** sur `GenerateurPavages.exe` pour lancer l’application.  
- Aucune installation supplémentaire n'est requise.  

---

### **💻 Version Python (Windows, Linux, macOS)**  

Si vous souhaitez exécuter l’application depuis le code source, assurez-vous d’avoir **Python 3** installé, ainsi que les bibliothèques suivantes :  

#### **🔧 Dépendances**  
- [numpy](https://numpy.org/)  
- [PySide6](https://wiki.qt.io/Qt_for_Python)  

📌 **Installation des dépendances avec `pip`** :  
```shell
pip install numpy
pip install PySide6
```

📌 **Lancer l’application depuis le code source** :  
1. Télécharger le projet et naviguer jusqu’à son dossier dans un terminal :  
   ```shell
   cd /chemin/vers/le/projet
   ```
2. Exécuter l’application avec la commande :  
   ```shell
   python main.py
   ```

---

## **🚀 Guide d'utilisation**  

### **🎯 Démarrer l'application**  
- **Windows (standalone)** : Double-cliquer sur **GenerateurPavages.exe**  
- **Linux/macOS/Python** : Exécuter **`python main.py`**  

---

### **📐 Dessiner un pavage**  
1. **Ouvrir une tuile**  
   - Dans le menu **Fichier** → **Ouvrir**, sélectionner une **image contenant une tuile** du pavage à générer.  
2. **Choisir un type de pavage**  
   - Via l’un des **menus dédiés**, sélectionner le type de pavage souhaité (**sphérique, euclidien, hyperbolique**).  
3. **Délimiter la tuile**  
   - Selon le pavage choisi, la tuile peut être un **triangle, un carré, un rectangle**, etc.  
   - Définir la forme en **cliquant sur les sommets** de celle-ci avec la souris.  
4. **Générer le pavage**  
   - Cliquer sur **"Dessiner le pavage"**.  
   - Une **nouvelle fenêtre** s’ouvrira avec le pavage calculé.  
   - Certaines options supplémentaires peuvent être proposées (échelle, rotation, etc.).  

📌 **Astuces** :  
✔ La **barre d’état** de la fenêtre principale fournit des instructions utiles.  
✔ Pour les pavages sphériques, la tuile doit respecter certaines **symétries** pour être valide.  

---

## **🛠️ Fonctionnalités encore en cours de développement**  

- **Compatibilité multi-OS** 💻 : finalisation de la version standalone pour **Linux et macOS**.  
- **Amélioration de l’interface** 🎨 : réorganisation pour une meilleure ergonomie (une seule fenêtre, options accessibles).  
- **Traduction en anglais** 🌍 : permettre une accessibilité internationale.  
- **Partage sur les réseaux sociaux** 📤 : ajouter un bouton pour diffuser les pavages générés.  
- **Déplacement dynamique** 🖱️ : déplacer les pavages dans l’espace en **drag & drop**.  

---

## **📚 Pour aller plus loin**  

Pour approfondir les concepts mathématiques liés aux pavages, voici quelques ressources utiles :  
- [Pavages de la sphère](https://fr.wikipedia.org/wiki/Pavage_de_la_sph%C3%A8re)  
- [Pavages du plan](https://fr.wikipedia.org/wiki/Pavage_du_plan)  
- [Groupes de papier-peint](https://fr.wikipedia.org/wiki/Groupe_de_papier_peint)  

---

## **📜 Licence**  

Ce logiciel est distribué sous la licence **GNU General Public License v3** ([GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)).

---

## **👨‍💻 Auteur**  

Développé initialement par **[Rémi Coulon](http://rcoulon.perso.math.cnrs.fr/)**, et enrichi dans le cadre de la **SAE6**.

---

### **✅ Mise à jour :**  
- Ajout de la **version standalone pour Windows** 💻  
- Ajout d’un **guide utilisateur détaillé** 📖  
- Clarification des étapes d’installation et d’utilisation 💡  
- Listage des fonctionnalités en cours de développement 🔄  
