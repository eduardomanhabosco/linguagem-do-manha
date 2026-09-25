#include <stdio.h>

int main(void) {
    int v_limite = 0;
    printf("%s\n", "Quantos remendos?");
    scanf("%d", &v_limite);
    int v_a = 2 + (3 * 4);
    int v_b = (2 + 3) * 4;
    int v_c = (10 - 3) - 2;
    int v_d = 7 / 2;
    int v_e = 7 % 2;
    float v_media = (v_a + v_b) / 4.0f;
    printf("%s%d%s%d%s%d\n", "a = ", v_a, ", b = ", v_b, ", c = ", v_c);
    printf("%s%d%s%d%s%g\n", "d = ", v_d, ", e = ", v_e, ", media = ", v_media);
    int v_contador = 1;
    int v_soma = 0;
    while (v_contador <= v_limite) {
        v_soma = v_soma + v_contador;
        printf("%s%d%s\n", "remendo ", v_contador, " aplicado");
        v_contador = v_contador + 1;
    }
    printf("%s%d\n", "soma = ", v_soma);
    int v_firmeza = (v_soma > 5) && (!(v_limite == 0));
    if (v_firmeza || 0) {
        printf("%s%s\n", "A gambiarra esta firme: ", (v_firmeza ? "firme" : "quebrado"));
    } else {
        printf("%s\n", "A gambiarra quebrou");
    }
    return 0;
}
