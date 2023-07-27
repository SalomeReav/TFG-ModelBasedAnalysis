#include <stdio.h>
#include <unistd.h>

int random(){
	return 7;
}

void main(int argc, char *argv[]){

	int z = 5;
	if((z != random()) && random()){
		printf("Yes.");
	} else if(random() > 10 && !random()){
		printf("Well.");
	}

}