/* 程式範例: Ch8_6_2.c */ 
#include <stdio.h>

/* 函數的原型宣告 */
int factorial(int);
/* 主程式 */
int main(void) {
    int level;  /* 變數宣告 */
    do {
        printf("請輸入階層數==> ");
        scanf("%d", &level);
        if ( level > 0 )  /* 函數的呼叫 */
            printf("%d!函數=%d\n",level,factorial(level));
    } while( level != -1 );

    return 0;
}
/* 函數: 計算n!的值 */ 
int factorial(int n) {
    if ( n == 1 )  /* 終止條件 */
        return 1;
    else
        return n * factorial(n-1);
}

