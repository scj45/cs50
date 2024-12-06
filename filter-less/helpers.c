#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++) // Loop over all pixels
    {
        for (int j = 0; j < width; j++)
        {
            float gray = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) /
                         3.0; // Average RBG
            int grayrgbt = round(gray);
            image[i][j].rgbtRed = grayrgbt;
            image[i][j].rgbtGreen = grayrgbt;
            image[i][j].rgbtBlue = grayrgbt; // Update pixel values
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute sepia values
            float sepiaRed = (.393 * image[i][j].rgbtRed) + (.769 * image[i][j].rgbtGreen) +
                             (.189 * image[i][j].rgbtBlue);
            float sepiaGreen = (.349 * image[i][j].rgbtRed) + (.686 * image[i][j].rgbtGreen) +
                               (.168 * image[i][j].rgbtBlue);
            float sepiaBlue = (.272 * image[i][j].rgbtRed) + (.534 * image[i][j].rgbtGreen) +
                              (.131 * image[i][j].rgbtBlue);
            int sepiaR = round(sepiaRed);
            if (sepiaR > 255)
            {
                sepiaR = 255;
            }
            int sepiaG = round(sepiaGreen);
            if (sepiaG > 255)
            {
                sepiaG = 255;
            }
            int sepiaB = round(sepiaBlue);
            if (sepiaB > 255)
            {
                sepiaB = 255;
            }
            image[i][j].rgbtRed = sepiaR;
            image[i][j].rgbtGreen = sepiaG;
            image[i][j].rgbtBlue = sepiaB; // Update pixel values
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    int middle = width / 2;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < middle; j++) // Only go through half the row
        {
            RGBTRIPLE tmp = image[i][j]; // Swap pixels
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width]; // Create a copy of image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++) // Loop over all pixels
    {
        for (int j = 0; j < width; j++) // Find average of neighbouring pixels
        {
            float avgR;
            float avgG;
            float avgB;

            if ((i == 0) && (j == 0)) // top left corner
            {

                RGBTRIPLE rightctr = copy[i][j + 1];
                RGBTRIPLE middown = copy[i + 1][j];
                RGBTRIPLE rightdown = copy[i + 1][j + 1];

                avgR = (float) (copy[i][j].rgbtRed + rightctr.rgbtRed + middown.rgbtRed +
                                rightdown.rgbtRed) /
                       4;
                avgG = (float) (copy[i][j].rgbtGreen + rightctr.rgbtGreen + middown.rgbtGreen +
                                rightdown.rgbtGreen) /
                       4;
                avgB = (float) (copy[i][j].rgbtBlue + rightctr.rgbtBlue + middown.rgbtBlue +
                                rightdown.rgbtBlue) /
                       4;

                int blurR = round(avgR);
                int blurG = round(avgG);
                int blurB = round(avgB);

                image[i][j].rgbtRed = blurR;
                image[i][j].rgbtGreen = blurG;
                image[i][j].rgbtBlue = blurB;
            }

            else if ((i == 0) && (0 < j) && (j < width - 1)) // top edge
            {
                RGBTRIPLE leftctr = copy[i][j - 1];
                RGBTRIPLE rightctr = copy[i][j + 1];
                RGBTRIPLE leftdown = copy[i + 1][j - 1];
                RGBTRIPLE middown = copy[i + 1][j];
                RGBTRIPLE rightdown = copy[i + 1][j + 1];

                avgR = (float) (leftctr.rgbtRed + copy[i][j].rgbtRed + rightctr.rgbtRed +
                                leftdown.rgbtRed + middown.rgbtRed + rightdown.rgbtRed) /
                       6;
                avgG = (float) (leftctr.rgbtGreen + copy[i][j].rgbtGreen + rightctr.rgbtGreen +
                                leftdown.rgbtGreen + middown.rgbtGreen + rightdown.rgbtGreen) /
                       6;
                avgB = (float) (leftctr.rgbtBlue + copy[i][j].rgbtBlue + rightctr.rgbtBlue +
                                leftdown.rgbtBlue + middown.rgbtBlue + rightdown.rgbtBlue) /
                       6;

                int blurR = round(avgR);
                int blurG = round(avgG);
                int blurB = round(avgB);

                image[i][j].rgbtRed = blurR;
                image[i][j].rgbtGreen = blurG;
                image[i][j].rgbtBlue = blurB;
            }

            else if ((0 < i) && (i < height - 1) && (j == 0)) // left edge
            {

                RGBTRIPLE midup = copy[i - 1][j];
                RGBTRIPLE rightup = copy[i - 1][j + 1];
                RGBTRIPLE rightctr = copy[i][j + 1];
                RGBTRIPLE middown = copy[i + 1][j];
                RGBTRIPLE rightdown = copy[i + 1][j + 1];

                avgR = (float) (midup.rgbtRed + rightup.rgbtRed + copy[i][j].rgbtRed +
                                rightctr.rgbtRed + middown.rgbtRed + rightdown.rgbtRed) /
                       6;
                avgG = (float) (midup.rgbtGreen + rightup.rgbtGreen + copy[i][j].rgbtGreen +
                                rightctr.rgbtGreen + middown.rgbtGreen + rightdown.rgbtGreen) /
                       6;
                avgB = (float) (midup.rgbtBlue + rightup.rgbtBlue + copy[i][j].rgbtBlue +
                                rightctr.rgbtBlue + middown.rgbtBlue + rightdown.rgbtBlue) /
                       6;

                int blurR = round(avgR);
                int blurG = round(avgG);
                int blurB = round(avgB);

                image[i][j].rgbtRed = blurR;
                image[i][j].rgbtGreen = blurG;
                image[i][j].rgbtBlue = blurB;
            }

            else if ((i == height - 1) && (j == 0)) // bottom left corner
            {
                RGBTRIPLE midup = copy[i - 1][j];
                RGBTRIPLE rightup = copy[i - 1][j + 1];
                RGBTRIPLE rightctr = copy[i][j + 1];

                avgR = (float) (midup.rgbtRed + rightup.rgbtRed + copy[i][j].rgbtRed +
                                rightctr.rgbtRed) /
                       4;
                avgG = (float) (midup.rgbtGreen + rightup.rgbtGreen + copy[i][j].rgbtGreen +
                                rightctr.rgbtGreen) /
                       4;
                avgB = (float) (midup.rgbtBlue + rightup.rgbtBlue + copy[i][j].rgbtBlue +
                                rightctr.rgbtBlue) /
                       4;

                int blurR = round(avgR);
                int blurG = round(avgG);
                int blurB = round(avgB);

                image[i][j].rgbtRed = blurR;
                image[i][j].rgbtGreen = blurG;
                image[i][j].rgbtBlue = blurB;
            }

            else if ((i == height - 1) && (0 < j) && (j < width - 1)) // bottom edge
            {
                RGBTRIPLE leftup = copy[i - 1][j - 1];
                RGBTRIPLE midup = copy[i - 1][j];
                RGBTRIPLE rightup = copy[i - 1][j + 1];
                RGBTRIPLE leftctr = copy[i][j - 1];
                RGBTRIPLE rightctr = copy[i][j + 1];

                avgR = (float) (leftup.rgbtRed + midup.rgbtRed + rightup.rgbtRed + leftctr.rgbtRed +
                                copy[i][j].rgbtRed + rightctr.rgbtRed) /
                       6;
                avgG = (float) (leftup.rgbtGreen + midup.rgbtGreen + rightup.rgbtGreen +
                                leftctr.rgbtGreen + copy[i][j].rgbtGreen + rightctr.rgbtGreen) /
                       6;
                avgB = (float) (leftup.rgbtBlue + midup.rgbtBlue + rightup.rgbtBlue +
                                leftctr.rgbtBlue + copy[i][j].rgbtBlue + rightctr.rgbtBlue) /
                       6;

                int blurR = round(avgR);
                int blurG = round(avgG);
                int blurB = round(avgB);

                image[i][j].rgbtRed = blurR;
                image[i][j].rgbtGreen = blurG;
                image[i][j].rgbtBlue = blurB;
            }

            else if ((i == height - 1) && (j == width - 1)) // bottom right corner
            {
                RGBTRIPLE leftup = copy[i - 1][j - 1];
                RGBTRIPLE midup = copy[i - 1][j];
                RGBTRIPLE leftctr = copy[i][j - 1];

                avgR = (float) (leftup.rgbtRed + midup.rgbtRed + leftctr.rgbtRed +
                                copy[i][j].rgbtRed) /
                       4;
                avgG = (float) (leftup.rgbtGreen + midup.rgbtGreen + leftctr.rgbtGreen +
                                copy[i][j].rgbtGreen) /
                       4;
                avgB = (float) (leftup.rgbtBlue + midup.rgbtBlue + leftctr.rgbtBlue +
                                copy[i][j].rgbtBlue) /
                       4;

                int blurR = round(avgR);
                int blurG = round(avgG);
                int blurB = round(avgB);

                image[i][j].rgbtRed = blurR;
                image[i][j].rgbtGreen = blurG;
                image[i][j].rgbtBlue = blurB;
            }

            else if ((0 < i) && (i < height - 1) && (j == width - 1)) // right edge
            {
                RGBTRIPLE leftup = copy[i - 1][j - 1];
                RGBTRIPLE midup = copy[i - 1][j];
                RGBTRIPLE leftctr = copy[i][j - 1];
                RGBTRIPLE leftdown = copy[i + 1][j - 1];
                RGBTRIPLE middown = copy[i + 1][j];

                avgR = (float) (leftup.rgbtRed + midup.rgbtRed + leftctr.rgbtRed +
                                copy[i][j].rgbtRed + leftdown.rgbtRed + middown.rgbtRed) /
                       6;
                avgG = (float) (leftup.rgbtGreen + midup.rgbtGreen + leftctr.rgbtGreen +
                                copy[i][j].rgbtGreen + leftdown.rgbtGreen + middown.rgbtGreen) /
                       6;
                avgB = (float) (leftup.rgbtBlue + midup.rgbtBlue + leftctr.rgbtBlue +
                                copy[i][j].rgbtBlue + leftdown.rgbtBlue + middown.rgbtBlue) /
                       6;

                int blurR = round(avgR);
                int blurG = round(avgG);
                int blurB = round(avgB);

                image[i][j].rgbtRed = blurR;
                image[i][j].rgbtGreen = blurG;
                image[i][j].rgbtBlue = blurB;
            }

            else if ((i == 0) && (j == width - 1)) // top right corner
            {
                RGBTRIPLE leftctr = copy[i][j - 1];
                RGBTRIPLE leftdown = copy[i + 1][j - 1];
                RGBTRIPLE middown = copy[i + 1][j];

                avgR = (float) (leftctr.rgbtRed + copy[i][j].rgbtRed + leftdown.rgbtRed +
                                middown.rgbtRed) /
                       4;
                avgG = (float) (leftctr.rgbtGreen + copy[i][j].rgbtGreen + leftdown.rgbtGreen +
                                middown.rgbtGreen) /
                       4;
                avgB = (float) (leftctr.rgbtBlue + copy[i][j].rgbtBlue + leftdown.rgbtBlue +
                                middown.rgbtBlue) /
                       4;

                int blurR = round(avgR);
                int blurG = round(avgG);
                int blurB = round(avgB);

                image[i][j].rgbtRed = blurR;
                image[i][j].rgbtGreen = blurG;
                image[i][j].rgbtBlue = blurB;
            }

            else if ((0 < i) && (i < height - 1) && (0 < j) && (j < width - 1)) // middle
            {
                RGBTRIPLE leftup = copy[i - 1][j - 1];
                RGBTRIPLE midup = copy[i - 1][j];
                RGBTRIPLE rightup = copy[i - 1][j + 1];
                RGBTRIPLE leftctr = copy[i][j - 1];
                RGBTRIPLE rightctr = copy[i][j + 1];
                RGBTRIPLE leftdown = copy[i + 1][j - 1];
                RGBTRIPLE middown = copy[i + 1][j];
                RGBTRIPLE rightdown = copy[i + 1][j + 1];

                avgR = (float) (leftup.rgbtRed + midup.rgbtRed + rightup.rgbtRed + leftctr.rgbtRed +
                                copy[i][j].rgbtRed + rightctr.rgbtRed + leftdown.rgbtRed +
                                middown.rgbtRed + rightdown.rgbtRed) /
                       9;
                avgG = (float) (leftup.rgbtGreen + midup.rgbtGreen + rightup.rgbtGreen +
                                leftctr.rgbtGreen + copy[i][j].rgbtGreen + rightctr.rgbtGreen +
                                leftdown.rgbtGreen + middown.rgbtGreen + rightdown.rgbtGreen) /
                       9;
                avgB = (float) (leftup.rgbtBlue + midup.rgbtBlue + rightup.rgbtBlue +
                                leftctr.rgbtBlue + copy[i][j].rgbtBlue + rightctr.rgbtBlue +
                                leftdown.rgbtBlue + middown.rgbtBlue + rightdown.rgbtBlue) /
                       9;

                int blurR = round(avgR);
                int blurG = round(avgG);
                int blurB = round(avgB);

                image[i][j].rgbtRed = blurR;
                image[i][j].rgbtGreen = blurG;
                image[i][j].rgbtBlue = blurB;
            }
        }
    }

    return;
}
