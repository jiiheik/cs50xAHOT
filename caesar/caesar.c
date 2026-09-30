#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // Validate only one command
    if (argc != 2)
    {
        printf("Error: use only one command\n");
        return 1;
    }
    // Key
    string key = argv[1];

    // Input needs to be a full number
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Error: key needs to be full number\n");
            return 1;
        }
    }
    printf("Key OK\n");

    // Plain text query
    string plaintext = get_string("plaintext: ");

    // Key to int
    int keyint = atoi(key);
    printf("ciphertext: ");

    // Ciphertext
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isupper(plaintext[i]))
        {
            printf("%c", (((plaintext[i] - 65) + keyint) % 26) + 65);
        }
        else if (islower(plaintext[i]))
        {
            printf("%c", (((plaintext[i] - 97) + keyint) % 26) + 97);
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    {
        printf("\n");
    }
}