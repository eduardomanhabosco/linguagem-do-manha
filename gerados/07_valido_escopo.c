#include <stdio.h>

int main(void) {
    int v_x = 1;
    if (v_x > 0) {
        int v_x_2 = v_x + 10;
        printf("%s%d\n", "x de dentro: ", v_x_2);
    }
    printf("%s%d\n", "x de fora: ", v_x);
    return 0;
}
