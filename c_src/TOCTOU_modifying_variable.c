#include <stdio.h>
#include <unistd.h>

void main(int argc, char *argv[]){
	char *filename = argv[1];

	if(!access(filename, W_OK)){ // Time of Check
		*filename = 'a';
		printf("Some random opeartion\n");
		*filename = argv[1];
		FILE* file = fopen(filename, "a+"); // Time of Use
		fclose(file);
	} else {
		printf("[+] ERROR\n");
	}
}