#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool only_digits(string argv);

char caesar(char c, int n);

int main(int argc, string argv[])
{
    if (argc != 2) // RUN WITH ONLY ONE CLA
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    if (only_digits(argv[1]) == false) // ARGV[1] ONLY DIGITS
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int key = atoi(argv[1]); // ARGV[1] STRING TO INT

    string plaintext = get_string("plaintext:  "); // PROMPT FOR PLAINTEXT

    printf("ciphertext: "); // PRINT CIPHERTEXT

    for (int i = 0, n = strlen(plaintext); i < n; i++) // FOR EACH PLAINTEXT:
    {
        char ciphertext = caesar(plaintext[i], key);
        printf("%c", ciphertext);
    }
    printf("\n");
}

bool only_digits(string argv)
{
    bool isDigit = true;
    for (int i = 0, n = strlen(argv); i < n; i++)
    {
        if (!isdigit(argv[i]))
        {
            return false;
        }
    }
    return isDigit;
}

char caesar(char c, int n) // ROTATE EACH CHAR IF LETTER
{
    if (isupper(c))
    {
        return 'A' + (c - 'A' + n) % 26; // c = (p+k)%26
    }
    else if (islower(c))
    {
        return 'a' + (c - 'a' + n) % 26; // c = (p+k)%26
    }
    else if (ispunct(c))
    {
        return c;
    }
    return c;
}
