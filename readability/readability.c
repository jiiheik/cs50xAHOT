#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int main(void)
{
    // Text input
    string t = get_string("Text: ");

    // No of letters
    int l = 0;
    for (int i = 0; i < strlen(t); i++)
    {
        if (((t[i] >= 'a') && t[i] <= 'z') ||
            (t[i] >= 'A' && t[i] <= 'Z'))
        {
            l++;
        }
    }

    // No of words
    int w = 1;
    for (int i = 0; i < strlen(t); i++)
    {
        if (t[i] == ' ')
        {
            w++;
        }
    }

    // No of sentences
    int s = 0;
    for (int i = 0; i < strlen(t); i++)
    {
        if (t[i] == '?' || t[i] == '!' || t[i] == '.')
        {
            s++;
        }
    }

    // Calculate index
    float result = (0.0588 * l / w * 100) - (0.296 * s / w * 100) - 15.8;
    int clindex = round(result);

    if (clindex < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (clindex >= 16)
    {

        printf("Grade 16+\n");

    }
    else
    {

        printf("Grade %i\n", clindex);

    }
}