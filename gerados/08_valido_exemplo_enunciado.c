#include <stdio.h>

int main(void) {
    int v_repeticoes = 3;
    float v_carga = 10.5f;
    while (v_repeticoes > 0) {
        printf("%d\n", v_repeticoes);
        v_carga = v_carga + (2 * 1.5f);
        v_repeticoes = v_repeticoes - 1;
    }
    if (v_carga >= 15) {
        printf("%s\n", "Treino concluido!");
    } else {
        printf("%s\n", "Ainda falta carga.");
    }
    return 0;
}
