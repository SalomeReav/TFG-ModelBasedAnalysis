#include <stdio.h>
#include <unistd.h>

int returned(){
	return 5;
}

int main(){
	for(int i = 0; i < 10; i++){
		i++;
	}

	for(int i = 0, y = 0, x = returned(); i < 10 && i>15; i++){
		i++;
	}

	int i = 0;
	for(;1 < 10;){
		i++;
	}

	for(;;i++){
		i++;
	}

	for(;;){
		i++;
	}
	return 0;
}