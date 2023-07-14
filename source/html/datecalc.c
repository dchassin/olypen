#include <stdlib.h>
#include <stdio.h>
#include <time.h>

int main(int argc, char *argv[])
{
	time_t now, then;
	int n_sec;
	char *format="%Y-%m-%d %H:%M:%S";
	char buffer[1024];
	if (argc==1)
	{
		fprintf(stderr,"Syntax: datecalc n_sec format\n");
		exit(1);
	}
	else if (argc==2)
	{
		n_sec = atoi(argv[1]);
	}
	else if (argc==3)
	{
		n_sec = atoi(argv[1]);
		format=argv[2];
	}
	else
	{
		fprintf(stderr,"error: too many options\n");
		exit(2);
	}
	time(&now);
	then = now + n_sec;
	
	if (strftime(buffer,sizeof(buffer),format,localtime(&then))>0)
	{
		printf("%s\n",buffer);
		exit(0);
	}
	else
	{
		printf("error: date format failed\n");
		exit(0);
	}
}
