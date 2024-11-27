Document de transition - Défi bisbille des galaxies (Défi Gentec-EO) - Jeux photoniques - Édition 2024

Dernière modification par Mathieu Marquis le 27 novembre 2024

# Matériel
- Ordinateur sur Windows avec prise USB-3.0 (important pour un mouvement du laser plus fluide)
- Câble d'alimentation de l'ordinateur
- Caméra Beamage-4M avec câble USB
- Pointeur laser avec piles de rechange

# Protocole
### Préparation de l'environnement
- Cloner le repository (`git clone https://github.com/mamar828/bisbille_des_galaxies.git`)

**Les explications suivantes sont pour l'IDE Visual Studio Code. Cet IDE n'est pas obligatoire, mais les conseils suivants permettent d'éviter les erreurs de type `ModuleNotFoundError`**.

- Ouvrir le repository dans Visual Studio Code
- Télécharger les modules requis : `pip install -r requirements.txt`
- S'assurer d'avoir installé Python et Python Debugger
- Dans l'onglet « Run and Debug », sélectionner « create a launch.json file », choisir « Python Debugger », puis « Python File »
<img width="387" alt="image" src="https://github.com/user-attachments/assets/f1d1736a-abc4-4337-aeb9-3962945b0df8">

- Une fois le fichier launch.json généré, il suffit d'ajouter la ligne suivante dans la liste configurations : "env": {"PYTHONPATH": "${workspaceFolder}"}
- Le fichier caché situé dans .vscode/launch.json devrait ressembler à :
<img width="700" alt="image" src="https://github.com/user-attachments/assets/bc7a138a-04f7-4365-bfd8-8f5ac8e16d9e">

### Téléchargement des modèles 3D
- Télécharger le dossier : https://drive.google.com/drive/folders/1HpwH1RNlUmcR1B5gHtB0RaP4ZLxdS0TR?usp=sharing
- Placer le dossier dans src/engine (le nom du dossier devrait être « objects » et devrait contenir 10 sous-dossiers)

### Téléchargement de PC-Beamage
- Sur le site internet de Gentec-EO, télécharger « Beamage » à l'adresse : https://www.gentec-eo.com/resources/download-center?DownloadCenterParamViewModel.DocumentTypes=0&DownloadCenterParamViewModel.Lang=en&DownloadCenterParamViewModel.IsUserFromChina=False#page:1
- Après avoir ouvert « Beamage Installer », cliquer sur « PC-Beamage »

### Setup dans PC-Beamage
- Lancer l'application « PC-Beamage »
- Brancher la caméra à l'ordinateur
- Appuyer sur « Connect » afin de connecter la caméra (bouton rond en haut à gauche)
- Si la connection ne fonctionne pas, débrancher la caméra, fermer l'application, attendre quelques secondes, brancher la caméra et relancer l'application
- Dans la fenêtre du programme, sous l'onglet « Setup », dans « Pixel Addressing » cocher « Decimate 2x2 » et dans « ADC Level » cocher « 10 bit »
- Dans l'onglet « Data Acquisition », s'assurer que le mode « Measurements only (.TXT) » est sélectionné, entrer une grande durée (1 Day est suffisant) et sélectionner un « sampling rate » de 1 / 1 Image(s)
- Sélectionner ensuite un chemin de fichier qui pourra facilement être retrouvé par la suite
- Appuyer sur « Start Capture »
- Pointer le laser dans la caméra afin de vérifier que l'aquisition fonctionne (un pic d'intensité devrait apparaître à l'écran)
- Appuyer sur « Start Data Acquisition »
 
### Jouer
- Sélectionner le fichier applications/main.py et l'exécuter en mode Debug avec le launch.json (dans le menu à droite du bouton pour exécuter le fichier, sélectionner « Python Debugger: Debug using launch.json »)
- Il se peut que le chargement de l'application prenne quelques minutes (les modèles 3D doivent tous être chargés)
- Une fois que le menu principal apparaît, sélectionner dans la barre de menus Fichier -> Sélectionner fichier Beamage 
- Sélectionner le fichier texte de l'acquisition de données avec PC-Beamage, créé à l'étape précédente.
- Dans Fichier -> Sélectionner dossier score, sélectionner un dossier dans lequel sera enregistré les pointages des équipes (le fichier créé sera nommé « bisbilles_scores.csv », et les scores seront ajoutés au fichier s'il existe déjà)
- Sélectionner le nombre de joueurs
- Sélectionner le numéro d'équipe
- Appuyer sur START
- Après la partie, les scores sont automatiquement enregistrés dans le dossier indiqué et il ne suffit que de changer le nombre de joueurs et le numéro de la prochaine équipe participante

# Notes
Les modèles 3D sont partagés avec l'adresse courrielle suivante :

bisbilledesgalaxies@gmail.com

MDP : bisbilledesgalaxies2024

---
La méthode de communication avec la caméra actuelle est assez rudimentaire et il serait certainement bénéfique de trouver une alternative, mais mes recherches n'ont pas trouvé de moyen simple d'effectuer le lien.
