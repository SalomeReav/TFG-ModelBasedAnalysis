#include <stdio.h>
#include <unistd.h>

int main(){

	int a = 0, b = 5;
	int *c;

	if(a == b){
		a++;
		--b;
	}

	// Unary operators

	++a; // Prefix
	--b; // Prefix
	a--; // Postfix
	b++; // Postfix
	!b;
	~a;
	a = -b;
	b = -(-(-b));
	sizeof(a);
	&a;
	*c;

	// Binary operators

	b*b;
	b%b;
	b/b;
	b+b;
	b-b;
	b << 1;
	b >> 1;
	b < 6;
	b > 5;
	b == b;
	b != b;
	b & b;
	b | b;
	b ^ b;
	b && b;
	b || b;

	return 0;
}