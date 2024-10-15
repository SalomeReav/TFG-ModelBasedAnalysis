#script de lanzamiento de ficheros de prueba 
import os 
import subprocess

main_dir = '../inputs/'

with os.scandir(main_dir) as files:
    for file in files:
        print("----------EJECUCION FICHERO: " + str(file) + "------------")
        subprocess.run(['python3', 'main.py', file])