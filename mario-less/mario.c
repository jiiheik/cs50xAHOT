#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // prompt query
    int n;
    do
    {
        n = get_int("Height: ");
    }
    // condition
    while (n < 1 || n > 8);
    // print pyramid
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (i + j < n - 1)
                printf(" ");
            else
                printf("#");
        }
        {
            printf("\n");
        }
    }
}