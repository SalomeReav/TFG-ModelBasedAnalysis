#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>

void main(int argc, char *argv[]){
	char *filename = argv[1];
	struct stat fileStat;

	if(stat(filename, &fileStat) = 0){ // Time of Check
		if(fileStat.st_mode & S_IWUSR){
			FILE* file = fopen(filename, "a+"); // Time of Use
			fclose(file);
		}
		else{
			printf("[+] ERROR\n");
	} else {
		printf("[+] ERROR\n");
	}
}
