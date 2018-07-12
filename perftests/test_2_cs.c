#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
	int p,l;
        int limit = 8*1024;
	int i=0;
        int tmp=0;
        int last=0;
	for (; i<limit; i++) {
		p=fork();
                if (p)
                    break;
		if (!p) {
			if ((i%7)==0) {
                                last=7;
				setpgid(0,0);
                        }
/*
			if ((i%3)==0 && last==7) {
				setpgid(0, 0);
                                last = 3;
                                tmp = getpid();
                        }

                        if ((i%5) == 0 && last==3) {
                            setpgid(0, tmp);
                        }
*/
                        if (((i%limit) == 0) && (i>limit*2/3) ) {
                            if ((i%20) == 0)
                                setpgid(0,0);
                            p=fork();
                            if (p) {
                                sleep(10);
                                exit(0);
                           }
                 
                                
                        }
                        if ((i % (limit / 10)) == 0)
                            printf("Iteration %d: %d %%\n", i, (int)(100*i/(double)limit) );
		if (i>=limit-1)
                    printf("Execution is ended\n");
		}
	}
	while(1);
return 0;
}
