#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int get_score(string word);

string get_winner(int score1, int score2);

int main(void)
{
    string player1 = get_string("Player 1 input: "); // Prompt Player 1 for input
    string player2 = get_string("Player 2 input: "); // Prompt Player 2 for input

    int score1 = get_score(player1); // Calculatr score of both words
    int score2 = get_score(player2);

    if (score1 > score2) // Print winner
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else if (score1 == score2)
    {
        printf("It's a tie!\n");
    }
}

int get_score(string word)
{
    int score = 0; // Keep track of score

    for (int i = 0, len = strlen(word); i < len; i++) // Calculate score
    {
        if (isupper(word[i]))
        {
            score += POINTS[word[i] - 'A'];
        }
        else if (islower(word[i]))
        {
            score += POINTS[word[i] - 'a'];
        }
        else
        {
            score += 0;
        }
    }
    return score;
}
