#include<stdio.h>

int main(void)
{
	int i;
	char b[100];
	printf("請輸入一個字串：");
	scanf("%s", b);
	for( i = 0; i < 100; i++ ){
	    if ( i % 2 == 1 ){
	        printf("%c",b[i]);
	    }
	}
	
	return 0;
 } 
