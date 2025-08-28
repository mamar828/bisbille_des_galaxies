operating_mode = "Jeux Photoniques"  # valid values are "Jeux Photoniques" and "Gentec"
gentec_planet_index = 7  # only used if operating_mode is "Gentec", codes are 0=Hoth, 1=Coruscant, 2=Yavin4, 3=Dathomir, 4=Kashyyyk, 5=Naboo, 6=Kamino, 7=Umbara
default_beamage_file = "/Users/mathieumarquis/Documents/Divers/Python/bisbille_des_galaxies/beamage.txt"  # filepath of the beamage data acquisition file relative to the game's root directory, leave "" for having to select the file in the app each time
default_score_folder = "/Users/mathieumarquis/Documents/Divers/Python/bisbille_des_galaxies"  # folder in which the "bisbille_scores.csv" file will be saved, relative to the game's root directory, leave "" for having to select the file in the app each time
collision_radius = 10  # radius of the collision detection square in pixels
peak_saturation_limit = 5  # percentage of the camera's saturation to detect the laser, lower the value if the game does not detect the laser, or higher if the game detects too many false positives
health_bar_depletion_hit_rate = 20  # rate at which the health bar depletes when hit by the laser
health_bar_depletion_default_rate = 2.5  # rate at which the health bar depletes naturally, set to 0 to disable natural depletion
