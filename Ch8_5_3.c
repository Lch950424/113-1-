/* 祘Α絛ㄒ: Ch8_5_3.c */ 
#include <stdio.h>

/* ㄧ计 */
int nonUseStaticVar(void);
int usestaticVar(void);
static int r1, r2, r3; /* 繰篈办跑计 */
/* 祘Α */
int main(void) {
    r1 = nonUseStaticVar();/* ㄧ计㊣ */
    r2 = nonUseStaticVar();
    r3 = nonUseStaticVar();
    printf("ぃㄏノ繰篈跑计: %d %d %d\n", r1, r2, r3);
    r1 = useStaticVar();
    r2 = useStaticVar();
    r3 = useStaticVar();
    printf("ㄏノ繰篈跑计1 : %d %d %d\n", r1, r2, r3); 
    printf("ㄏノ繰篈跑计2 : %d %d %d\n", useStaticVar(),
                    useStaticVar(), useStaticVar());

    return 0;
}
/* ㄧ计: ぃㄏノ繰篈跑计 */ 
int nonUseStaticVar() {
    int step = 0;   /* 跋办跑计 */
    step++;         /* 跋办跑计 */
    return step;
}
/* ㄧ计: ㄏノ繰篈跑计 */ 
int useStaticVar() {
    static int step = 0;   /* 繰篈跑计 */
    step++;         /* 繰篈跑计 */
    return step;
}
