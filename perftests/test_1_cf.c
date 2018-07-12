#include <stdio.h>
#include <unistd.h>

int main() {
	int p;
	int i=0;
	for (;i<8*1024;i++) {
		p=fork();
		if (!p) {
// do all of children's stuff here, then:
			if ((i%2)==0)
				setsid();
			else
				setpgid(0, 0);
			
			break;
		}
	}
	while(1);

return 0;
}
