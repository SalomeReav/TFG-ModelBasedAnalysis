#include <stdio.h>
#include <unistd.h>

void function_7(char* filename){
	if(!access(filename, W_OK)){ // Time of Check
		FILE* file = fopen(filename, "a+"); // Time of Use
		fclose(file);
	} else {
		printf("[+] ERROR\n");
	}
}

void function_6(char* filename){
	function_7(filename);
}

void function_5(char* filename){
	function_6(filename);
}

void function_4(char* filename){
	function_5(filename);
}

void function_3(char* filename){
	function_4(filename);
}

void function_2(char* filename){
	function_3(filename);
}

void function_1(char* filename){
	function_2(filename);
}

void main(int argc, char *argv[]){
	char *filename = argv[1];
	function_1(filename);
}