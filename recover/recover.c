#include <cs50.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2) // Only single argv
    {
        printf("Usage: ./recover FILE\n"); // Error message if more than one
        return 1;
    }

    FILE *card = fopen(argv[1], "r"); // Open memory card
    if (card == NULL)                 // Error message if fails
    {
        printf("Could not open %s.\n", argv[1]);
        return 2;
    }

    uint8_t buffer[512]; // Buffer for block of data

    FILE *currentImage = NULL;
    int jpegnum = 0;
    char fname[8];
    while (fread(buffer, 1, 512, card) == 512) // While data remaining in memory card
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0) // If start of new JPEG  // Create JPEGs from data
        {
            if (currentImage == NULL) // If first JPEG
            {
                sprintf(fname, "%03i.jpg", 0);
                currentImage = fopen(fname, "w");
                if (currentImage != NULL)
                {
                    fwrite(buffer, 1, 512, currentImage);
                }
            }
            else // else
            {
                fclose(currentImage);
                jpegnum++;
                sprintf(fname, "%03i.jpg", jpegnum);
                currentImage = fopen(fname, "w");
                if (currentImage != NULL)
                {
                    fwrite(buffer, 1, 512, currentImage);
                }
            }
        }
        else // else if already found JPEG
        {
            if (currentImage != NULL)
            {
                fwrite(buffer, 1, 512, currentImage);
            }
        }
    }
    fclose(currentImage);
    fclose(card);
}
