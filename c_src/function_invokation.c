#include <stdio.h>
#include <unistd.h>

void my_function(int a, int b, char c, int* d, char* e){

}

int return_10(){

	return 10;
}


int main(){

	int p = 10;
	int *r = &p;

	my_function(5, return_10(), 'a', r, "string");

	return 5;
}