# TFG-ModelBasedAnalysis
Este repositorio contiene la documentación sobre un trabajo final de la Universidad de Zaragoza, llamado "Detección de vulnerabilidades en código fuente a través de Redes de Petri". 
## Funcionamiento
Transforma a red de Petri ficheros de código fuente en C/C++ procesando el AST obtenido de la compilación con Clang. 

Para la obtención del AST parseado para este escenario, se ha utilizado un script de @RazviOverflow.
## Ficheros
En este repositorio los códigos fuente utilizados se encuentran en la carpeta c_src, la fuente de estos ficheros de prueba es @RazviOverflow. 

En la carpeta inputs se encuentran los ficheros .json que contienen el AST final de los c_src y que se usan como entrada para ejecutar la herramienta. 
## Ejecución 
Para ejecutrar la herramienta con un fichero se tiene que lanzar el comando siguiente dentro de la carpeta Clasess: `pyhton3 main.py ..\inputs\{nombre fichero json}` 

El comando generará en la carpeta output_files un fichero .pnml que contiene la red de Petri en formato PNML.
## Visualización 
En este caso se ha usado el entorno PIPE (https://sarahtattersall.github.io/PIPE/) como medio de visualización del fichero final obtenido. 

Se puede ejecutar desde la carpeta raíz de este repositorio con el comando: `java -jar PIPE-gui-5.0.2.jar`


