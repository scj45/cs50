#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

float count_letters(string text);

float count_words(string text);

float count_sentences(string text);

int main(void)
{
    string text = get_string("Insert text here: "); // PROMPT USER FOR TEXT

    float letters = count_letters(text); // COUNT NUMBER OF LETTERS

    float words = count_words(text); // COUNT NUMBER OF WORDS

    float sentences = count_sentences(text); // COUNT NUMBER OF SENTENCES

    float L = (letters / words) * 100;
    float S = (sentences / words) * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8); // COMPUTE COLEMAN-LIAU INDEX m f f       

    if ((1 <= index) && (index < 16)) // PRINT GRADE LEVEL
    {
        printf("Grade %i\n", index);
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
}

float count_letters(string text)
{
    float letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters; // RETURN LETTER COUNT
}

float count_words(string text)
{
    int words = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isblank(text[i]))
        {
            words++;
        }
    }
    return words; // RETURN WORD COUNT
}

float count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }
    return sentences; // RETURN SENTENCE COUNT
}
