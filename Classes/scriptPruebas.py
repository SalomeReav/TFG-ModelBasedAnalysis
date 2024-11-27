#script tha launchs the tool with every test file in the inputs folder
import os 
import subprocess
import sys
import time

def calcular_media_tiempos(output_path):
    try:
        with open(output_path, 'r') as f:
            tiempos = []
            for linea in f:
                if "Tiempo de ejecución global:" in linea:
                    # Extraer el tiempo de la línea
                    tiempo_str = linea.split(":")[1].strip()  # Obtener la parte después de ":"
                    tiempo = float(tiempo_str.split()[0])  # Convertir a float
                    tiempos.append(tiempo)

            if tiempos:
                media = sum(tiempos) / len(tiempos)
                print(f"Tiempo medio de ejecución: {media:.4f} segundos")
            else:
                print("No se encontraron tiempos de ejecución.")
    except IOError as e:
        print("Error al abrir el archivo:", e)

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 scripPruebas.py <json_file> <num_test>")
        sys.exit(1)

    file = sys.argv[1]
    num_test = int(sys.argv[2])
    name_file = os.path.splitext(os.path.basename(file))[0]
    output_path = os.path.join(r"..\output_files",str(name_file)+"_prueba.txt")
    for n in range(num_test):
        process = subprocess.run(['python3', 'main.py', file],stdout=subprocess.PIPE)
        try:
            with open(output_path,'ab') as out:
                out.write(b'\n') 
                out.write(process.stdout)
        except IOError as e:
            print("Error al abrir archivo: ",e)
        time.sleep(30.0)
        print(f"Test {n} finished")
    calcular_media_tiempos(output_path)
    
if __name__== "__main__":
    main()
    