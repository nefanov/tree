#include <stdio.h>
#include <unistd.h>

int main() {
	int p;
	int i=0;
	for (;i<1024;i++) {
		p=fork();
		if (!p) {
// do all of children's stuff here, then:
                        if ((i%500)==0)
                             printf("Iteration %d/1024\n",i);
			if ((i%2000)==0)
				setsid();
			
			break;
		}
	}
	while(1);

return 0;
}
