#include <stdio.h>

int main(void) {
    int v_fita = 10;
    float v_cola = 2.5f;
    int v_ligado = 1;
    v_fita = v_fita + 5;
    v_cola = v_cola * 2;
    printf("%s%d\n", "fita: ", v_fita);
    printf("%s%g\n", "cola: ", v_cola);
    printf("%s%s\n", "ligado: ", (v_ligado ? "firme" : "quebrado"));
    printf("%s\n", "Sistema Gambiarra iniciado");
    return 0;
}
