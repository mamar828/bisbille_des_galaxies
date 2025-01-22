Document de transition - Défi bisbille des galaxies (Défi Gentec-EO) - Jeux photoniques - Édition 2024

Dernière modification par Mathieu Marquis le 15 janvier 2025

# Matériel
- Ordinateur sur Windows avec prise USB-3.0 (important pour un mouvement du laser plus fluide)
- Câble d'alimentation de l'ordinateur
- Caméra Beamage-4M avec câble USB
- Pointeur laser avec piles de rechange

# Protocole
### Préparation de l'environnement
- Cloner le repository : `git clone https://github.com/mamar828/bisbille_des_galaxies.git`
- Installer les modules requis : `pip install -r requirements.txt`
- Télécharger le dossier : https://drive.google.com/drive/folders/1HpwH1RNlUmcR1B5gHtB0RaP4ZLxdS0TR?usp=sharing
- Placer le dossier dans src/engine (le nom du dossier devrait être « objects » et le dossier devrait contenir 10 sous-dossiers)
- Pour run les fichiers depuis le terminal, [ajouter le chemin du repository au PYTHONPATH](https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-so-it-finds-my-modules-packages) en créant une variable PYTHONPATH ayant comme valeur le chemin complet dans l'ordinateur
- Redémarrer le terminal
- Pour vérifier que cela est fonctionnel, vérifier que la commande `python applications/main.py` ne soulève pas d'exception `ModuleNotFoundError`

### Téléchargement de PC-Beamage
- Sur le site internet de Gentec-EO, télécharger « Beamage » à l'adresse : https://www.gentec-eo.com/resources/download-center?DownloadCenterParamViewModel.DocumentTypes=0&DownloadCenterParamViewModel.Lang=en&DownloadCenterParamViewModel.IsUserFromChina=False#page:1
- Après avoir ouvert « Beamage Installer », cliquer sur « PC-Beamage » pour l'installer

### Setup dans PC-Beamage
- Lancer l'application « PC-Beamage »
- Brancher la caméra à l'ordinateur
- Appuyer sur « Connect » afin de connecter la caméra (bouton rond en haut à gauche)
- Si la connection ne fonctionne pas, débrancher la caméra, fermer l'application, attendre quelques secondes, brancher la caméra et relancer l'application
- Dans la fenêtre du programme, sous l'onglet « Setup », dans « Pixel Addressing » cocher « Decimate 2x2 » et dans « ADC Level » cocher « 10 bit »
- En haut à gauche, sélectionner un temps d'exposition fixe de 4 (l'unité correspond à des ms) et s'assurer que la case auto n'est pas cochée
- Dans l'onglet « Data Acquisition », s'assurer que le mode « Measurements only (.TXT) » est sélectionné, entrer une grande durée (1 Day est suffisant) et sélectionner un « sampling rate » de 1 / 1 Image(s)
- Sélectionner ensuite un chemin de fichier qui pourra facilement être retrouvé par la suite
- Appuyer sur « Start Capture »
- Pointer le laser dans la caméra afin de vérifier que l'aquisition fonctionne (un pic d'intensité devrait apparaître à l'écran)
- Appuyer sur « Start Data Acquisition »
 
### Jouer
- Run le fichier applications/main.py
- Il se peut que le chargement de l'application prenne quelques minutes (les modèles 3D doivent tous être chargés)
- Une fois que le menu principal apparaît, sélectionner dans la barre de menus Fichier -> Sélectionner fichier Beamage 
- Sélectionner le fichier texte de l'acquisition de données avec PC-Beamage, créé à la section précédente.
- Dans Fichier -> Sélectionner dossier score, sélectionner un dossier dans lequel sera enregistré les pointages des équipes (le fichier créé sera nommé « bisbilles_scores.csv », et les scores seront ajoutés au fichier s'il existe déjà)
- Sélectionner le nombre de joueurs
- Sélectionner le numéro d'équipe
- Appuyer sur START
- Après la partie, les scores sont automatiquement enregistrés dans le dossier indiqué et il ne suffit que de changer le nombre de joueurs et le numéro de la prochaine équipe participante

# Versions
Le jeu est offert sous deux versions.

### AppJeuxPhotoniques
Cette version est utilisée lors des Jeux Photoniques et permet de faire jouer une équipe de 1-8 joueurs contre des vaisseaux différents. Cette version est en français.

### AppGentec
Cette version est utilisée par Gentec-EO lors des démonstrations avec le jeu et comporte une liste de highscores et une sélection du nom du joueur. Cette version est en anglais. Le vaisseau utilisé est le même pour tous les joueurs et doit être sélectionné par l'argument `world_index` dans l'initialisation de l'application.

# Notes
La méthode de communication avec la caméra actuelle est assez rudimentaire et il serait certainement bénéfique de trouver une alternative, mais mes recherches n'ont pas trouvé de moyen simple d'effectuer le lien.

# Références
### Scènes
Coruscant : https://es.pinterest.com/pin/591660469831014591/

Dathomir : https://starwars.fandom.com/wiki/Dathomir

Hoth : https://www.reddit.com/r/StarWars/comments/1d45mm0/which_sw_planetmoon_does_your_home_environment/

Kamino : https://star-wars-extended-universe.fandom.com/wiki/Kamino

Naboo : https://www.swcombine.com/rules/?Small&ID=437

Kaskyyyk : https://fr.wikipedia.org/wiki/Kashyyyk

Umbara : https://www.reddit.com/r/TheCloneWars/comments/vqtro8/umbara_transparent_hd_planet/

Yavin4 : https://starwars.fandom.com/wiki/Yavin_4


### Modèles 3D
A-wing : https://sketchfab.com/3d-models/a-wing-starfighter-95b9162b139047b0a17b2359561a6ebd

Corvette : https://www.cgtrader.com/items/3436198/download-page

Imperial Shuttle : https://www.cgtrader.com/items/2188914/download-page

Malevolence : https://sketchfab.com/3d-models/the-malevolence-die-cast-d48949c425704a8dafbe7e65d6dcd8c1

Millenium Falcon : https://free3d.com/3d-model/star-wars-falcon-95795.html

Royal Starship : https://www.cgtrader.com/items/4145971/download-page

Star Destroyer : https://www.cgtrader.com/items/2560667/download-page

Tie Fighter : https://www.cgtrader.com/items/2195979/download-page
