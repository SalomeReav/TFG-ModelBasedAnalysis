#include <stdio.h>
#include <unistd.h>

struct Person {
  char name[50];
  int citNo;
  float salary;
}person_insider;

int main(){
	struct Person person_0;
	struct Person persons[20];
	return 0;
}