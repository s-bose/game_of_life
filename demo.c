#include <stdio.h>

int main() {
    int choice; 
    float a, b;
    printf("\n1.Add");
    printf("\n1.Subtract");
    printf("\n1.Multiply");
    printf("\n1.Division\n");

    scanf("%d", &choice);

    printf("Enter two numbers: ");
    scanf("%f %f", &a, &b);

    if (choice == 1) {
        printf("%f", a + b);
    }
}