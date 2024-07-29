import time


current_num = 0
while True:
    time.sleep(0.01)
    try:
        with open(r"C:\Users\Proprio\Documents\Mathieu\bisbille_des_galaxies\test_measurements.txt", "r") as f:
            lines = f.readlines()
            if len(lines) > current_num:
                infos = lines[-1].split("\t")
                if float(infos[11]) > 50:   # peak saturation
                    print(f"x: {infos[-4]} y: {infos[-3]}") # x and y seem to range from ~-5000 to ~5000
                else:
                    print("Off")
                current_num = len(lines)
    except PermissionError:
        print("PermissionError encountered")
    
    if current_num % 100 == 0:
        with open(r"C:\Users\Proprio\Documents\Mathieu\bisbille_des_galaxies\test_measurements.txt", "w") as f:
            f.write("NOTHING")
            print("wrote")
            current_num = 1
