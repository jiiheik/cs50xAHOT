#include "helpers.h"
#include "math.h"
#include "cs50.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float Red = image[i][j].rgbtRed;
            float Green = image[i][j].rgbtGreen;
            float Blue = image[i][j].rgbtBlue;

            int avg = round((Red + Green + Blue) / 3);
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = avg;
        }
    }
    return;

}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float originalRed = image[i][j].rgbtRed;
            float originalGreen = image[i][j].rgbtGreen;
            float originalBlue = image[i][j].rgbtBlue;

            int sepiaRed = round(0.393 * originalRed + 0.769 * originalGreen + 0.189 * originalBlue);
            int sepiaGreen = round(0.349 * originalRed + 0.686 * originalGreen + 0.168 * originalBlue);
            int sepiaBlue = round(0.272 * originalRed + 0.534 * originalGreen + 0.131 * originalBlue);

            // Set value as 255, if value is over 255
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            RGBTRIPLE r = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = r;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Copy image
    RGBTRIPLE imgcopy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            imgcopy[i][j] = image[i][j];
        }
    }
    // Sums
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int redsum;
            int bluesum;
            int greensum;
            redsum = bluesum = greensum = 0;
            float c = 0;

            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    int cx = i + x;
                    int cy = j + y;

                    // Validity check
                    if (cx < 0 || cx > (height - 1) || cy < 0 || cy > (width - 1))
                    {
                        continue;
                    }

                    redsum += image[cx][cy].rgbtRed;
                    greensum += image[cx][cy].rgbtGreen;
                    bluesum += image[cx][cy].rgbtBlue;
                    c++;
                }
                // Averages
                imgcopy[i][j].rgbtRed = round(redsum / c);
                imgcopy[i][j].rgbtGreen = round(greensum / c);
                imgcopy[i][j].rgbtBlue = round(bluesum / c);
            }

        }
    }
    // Copy
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = imgcopy[i][j].rgbtRed;
            image[i][j].rgbtGreen = imgcopy[i][j].rgbtGreen;
            image[i][j].rgbtBlue = imgcopy[i][j].rgbtBlue;
        }
    }
    return;
}