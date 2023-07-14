/* samplefreq.c
 *
 * 2005-12-28 DP Chassin
 *
 * read first N frequency samples from stdin, removes all non-printing characters, and formats output
 */

#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <signal.h>
#include <unistd.h>

int n_samples = 600;
int first=1;

void on_stop(int signum)
{
	if (n_samples>0)
	{
		n_samples = 0;
		alarm(1);
	}
	else
		if (first==0)
			printf(";\n");
		exit(1);
}

int main(int argc, char *argv[])
{
	enum {RAW, SQL} format=RAW;
	int i;
	struct {
		int len;
		char text[1024];
	} *bufptr=NULL;
	int buflen=0;

	alarm(n_samples/10 * 1.1);
	for (i=1; i<argc; i++)
	{
		if (argv[i][0]=='-')
		{
			if (isdigit(argv[i][1]))
				n_samples = atoi(argv[i]+1);
			else if (argv[i][1]=='h')
			{
				printf("%s","Syntax: samplefreq [-n] [--sql]\n  Samples first n frequency readings from stdin, strips non-printing characters and formats output as specified\n");
				exit(0);
			}
			else if (strcmp(argv[i],"--sql")==0)
				format=SQL;
			else 
			{
				fprintf(stderr,"%s","Syntax: samplefreq [-n]\n");
				exit(1);
			}
		}
	}

	signal(SIGINT,on_stop);
	signal(SIGHUP,on_stop);
	signal(SIGTERM,on_stop);
	signal(SIGALRM,on_stop);

	while (n_samples>0 && getline(&bufptr,&buflen,stdin)>=0)
	{
		if (format==SQL)
		{
			double frequency, readtime;
			if (bufptr->len>0 && sscanf(bufptr->text,"freq=%lf Hz; time=%lf",&frequency,&readtime)==2)
			{
				time_t tm;
				char now[64];
				n_samples--;
				if (first==0)
					printf(",\n");
				else
					printf("\nINSERT IGNORE INTO gridfreq (posttime, readtime, freq) VALUES\n");
				first = 0;
				time(&tm);
				strftime(now,sizeof(now),"%Y-%m-%d %H:%M:%S",(struct tm *)localtime(&tm));
				printf("('%s',%.6f,%.3f)",now,readtime,frequency);
			}
			else
			{
				printf("\n# %s\n", bufptr->text);
			}
		}
		else
		{
			if (strncmp(bufptr->text,"freq=",5)==0)
				n_samples--;
			printf("%s", bufptr->text);
		}
		fflush(stdout);
	}
	if (format==SQL)
		printf(";\n");
	exit(0);
}
