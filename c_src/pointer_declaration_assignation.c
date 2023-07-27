#include <stdio.h>
#include <unistd.h>

void main(int argc, char *argv[]){

	int a = 0xdeadbeef;
	int* my_integer;
	my_integer = &a;
	printf("My integer is at %lX and its value is %lX.\n", my_integer, *my_integer);
}