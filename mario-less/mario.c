#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // ask user for positive whole number
    int height;
    do
    {
        height = get_int("Please give a whole number greater than 0: ");
    }
    while (height < 1);

    // print brick pyramid
    for (int i = 0; i < height; i++)
    {
        // print row
        for (int k = height - i; k > 1; k--) // spaces
        {
            printf(" ");
        }
        for (int j = 0; j <= i; j++) // bricks
        {
            printf("#");
        }
        printf("\n");
    }
}
