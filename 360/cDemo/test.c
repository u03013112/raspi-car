//test.c
#include<stdio.h>
int foo(int a, int b){
    printf("a:%d, b:%d\n", a, b);
    return 0;
}

// //先生成test.o文件；然后编译为动态库test.so
// gcc -o test.so -shared -fPIC test.c
