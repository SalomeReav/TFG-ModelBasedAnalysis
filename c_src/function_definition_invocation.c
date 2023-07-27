#include <stdio.h>
#include <unistd.h>

int my_function(char param1, int param2){
	return param1+param2;
}

void main(int argc, char *argv[]){

	my_function('a', 1);

}