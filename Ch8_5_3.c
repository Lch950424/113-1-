/* �{���d��: Ch8_5_3.c */ 
#include <stdio.h>

/* ��ƪ��쫬�ŧi */
int nonUseStaticVar(void);
int usestaticVar(void);
static int r1, r2, r3; /* �R�A�����ܼƫŧi */
/* �D�{�� */
int main(void) {
    r1 = nonUseStaticVar();/* ��ƩI�s */
    r2 = nonUseStaticVar();
    r3 = nonUseStaticVar();
    printf("���ϥ��R�A�ܼ�: %d %d %d\n", r1, r2, r3);
    r1 = useStaticVar();
    r2 = useStaticVar();
    r3 = useStaticVar();
    printf("�ϥ��R�A�ܼ�1 : %d %d %d\n", r1, r2, r3); 
    printf("�ϥ��R�A�ܼ�2 : %d %d %d\n", useStaticVar(),
                    useStaticVar(), useStaticVar());

    return 0;
}
/* ���: ���ϥ��R�A�ܼ� */ 
int nonUseStaticVar() {
    int step = 0;   /* �ϰ��ܼƫŧi */
    step++;         /* �ϰ��ܼƥ[�@ */
    return step;
}
/* ���: �ϥ��R�A�ܼ� */ 
int useStaticVar() {
    static int step = 0;   /* �R�A�ܼ� */
    step++;         /* �R�A�ܼƥ[�@ */
    return step;
}
