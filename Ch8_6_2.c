/* �{���d��: Ch8_6_2.c */ 
#include <stdio.h>

/* ��ƪ��쫬�ŧi */
int factorial(int);
/* �D�{�� */
int main(void) {
    int level;  /* �ܼƫŧi */
    do {
        printf("�п�J���h��==> ");
        scanf("%d", &level);
        if ( level > 0 )  /* ��ƪ��I�s */
            printf("%d!���=%d\n",level,factorial(level));
    } while( level != -1 );

    return 0;
}
/* ���: �p��n!���� */ 
int factorial(int n) {
    if ( n == 1 )  /* �פ���� */
        return 1;
    else
        return n * factorial(n-1);
}

