operating_mode = "Jeux Photoniques"  # valid values are "Jeux Photoniques" and "Gentec"
gentec_planet_index = 6  # only used if operating_mode is "Gentec", codes are 0=Coruscant, 1=Dathomir, 2=Hoth, 3=Kashyyyk, 4=Umbara, 5=Naboo, 6=Kamino, 7=Yavin4,
jeux_photoniques_random_world_order = False  # if True, the order of the worlds is randomized at each new game, only used if operating_mode is "Jeux Photoniques"
default_beamage_file = ""  # filepath of the beamage data acquisition file relative to the game's root directory, leave "" for having to select the file in the app each time
default_score_folder = ""  # folder in which the "bisbille_scores.csv" file will be saved, relative to the game's root directory, leave "" for having to select the file in the app each time
collision_radius = 10  # radius of the collision detection square in pixels
peak_saturation_limit = 5  # percentage of the camera's saturation to detect the laser, lower the value if the game does not detect the laser, or higher if the game detects too many false positives
health_bar_depletion_hit_rate = 20  # rate at which the health bar depletes when hit by the laser
health_bar_depletion_default_rate = 2.5  # rate at which the health bar depletes naturally, set to 0 to disable natural depletion
