#include <stdio.h> //declaracao de biblioteca

float soma (float operando1, float operando2){
      return operando1+operando2;
}
float subtracao (float operando1, float operando2){
      return operando1-operando2;
}
float divisao (float operando1, float operando2){
      return operando1/operando2;
}
float multiplicacao (float operando1, float operando2){
      return operando1/operando2;
}
void testar (float a){
      a = 10;
}

int main(int argc, char *argv[]) //função main
{
    int soma = 5.25;
    int testar = 5;
    int subtracao = 6.75;
    int arg3 = soma(soma ,subtracao) - subtracao(subtracao,soma) * multiplicacao (soma ,subtracao) / divisao(subtracao,soma);
    printf ("%i", arg3);
    return soma;
}
