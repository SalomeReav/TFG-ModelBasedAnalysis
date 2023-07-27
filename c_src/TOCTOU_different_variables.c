#include <stdio.h>
#include <unistd.h>

void main(int argc, char *argv[]){
	char *filename = argv[1];
	char *filename_2 = argv[1];;

	if(!access(filename, W_OK)){ // Time of Check
		FILE* file = fopen(filename_2, "a+"); // Time of Use
		fclose(file);
	} else {
		printf("[+] ERROR\n");
	}
}