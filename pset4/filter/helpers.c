#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //loop through each pixel
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            //calculate average rgb value and swap
            double grey = image[h][w].rgbtBlue + image[h][w].rgbtGreen + image[h][w].rgbtRed;
            grey =  round(grey / 3);
            image[h][w].rgbtBlue = grey;
            image[h][w].rgbtGreen = grey;
            image[h][w].rgbtRed = grey;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // loop through each pixel
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            if (w < (width - (w + 1)))
            {
                // store temp rbg value
                RGBTRIPLE swap;
                swap.rgbtBlue = image[h][w].rgbtBlue;
                swap.rgbtGreen = image[h][w].rgbtGreen;
                swap.rgbtRed = image[h][w].rgbtRed;

                // swap leftmost pixel
                image[h][w].rgbtBlue = image[h][width - (w + 1)].rgbtBlue;
                image[h][w].rgbtGreen = image[h][width - (w + 1)].rgbtGreen;
                image[h][w].rgbtRed = image[h][width - (w + 1)].rgbtRed;

                //swap rightmost pixel
                image[h][width - (w + 1)].rgbtBlue = swap.rgbtBlue;
                image[h][width - (w + 1)].rgbtGreen = swap.rgbtGreen;
                image[h][width - (w + 1)].rgbtRed = swap.rgbtRed;

            }


        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //create a temp image to store original values
    
    RGBTRIPLE temp[height][width];
    
    //copy from original to temporary image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    
    //loop through each pixel
    for (int h = 0; h < height; h++)
    {

        for (int w = 0; w < width; w++)
        {
            // set a count to use in calculating average
            int count = 0;

            // create temporary arrays to hold values of the neigboring pixels
            int blurb = 0;
            int blurg = 0;
            int blurr = 0;

            //store values for current column

            //center
            blurb += temp[h][w].rgbtBlue;
            blurg += temp[h][w].rgbtGreen;
            blurr += temp[h][w].rgbtRed;
            count++;

            //down
            if (h != (height - 1))
            {
                blurb += temp[h + 1][w].rgbtBlue;
                blurg += temp[h + 1][w].rgbtGreen;
                blurr += temp[h + 1][w].rgbtRed;
                count++;
            }
            
            //up
            if (h != 0)
            {
                blurb += temp[h - 1][w].rgbtBlue;
                blurg += temp[h - 1][w].rgbtGreen;
                blurr += temp[h - 1][w].rgbtRed;
                count++;
            }

            // store values for the next column

            //center
            if (w != (width - 1))
            {
                blurb += temp[h][w + 1].rgbtBlue;
                blurg += temp[h][w + 1].rgbtGreen;
                blurr += temp[h][w + 1].rgbtRed;
                count++;
            }

            //down
            if ((h != (height - 1)) && (w != (width - 1)))
            {
                blurb += temp[h + 1][w + 1].rgbtBlue;
                blurg += temp[h + 1][w + 1].rgbtGreen;
                blurr += temp[h + 1][w + 1].rgbtRed;
                count++;
            }
            
            //up
            if ((h != 0) && (w != (width - 1)))
            {
                blurb += temp[h - 1][w + 1].rgbtBlue;
                blurg += temp[h - 1][w + 1].rgbtGreen;
                blurr += temp[h - 1][w + 1].rgbtRed;
                count++;
            }

            //store values for the previous column
            //center
            if (w != 0)
            {
                blurb += temp[h][w - 1].rgbtBlue;
                blurg += temp[h][w - 1].rgbtGreen;
                blurr += temp[h][w - 1].rgbtRed;
                count++;
            }
            
            //down
            if ((h != (height - 1)) && (w != 0))
            {
                blurb += temp[h + 1][w - 1].rgbtBlue;
                blurg += temp[h + 1][w - 1].rgbtGreen;
                blurr += temp[h + 1][w - 1].rgbtRed;
                count++;
            }

            //up
            if ((h != 0) && (w != 0))
            {
                blurb += temp[h - 1][w - 1].rgbtBlue;
                blurg += temp[h - 1][w - 1].rgbtGreen;
                blurr += temp[h - 1][w - 1].rgbtRed;
                count++;
            }
            
            //get average and update pixels
            image[h][w].rgbtBlue = (round((double)blurb / (double)count));
            image[h][w].rgbtGreen = (round((double)blurg / (double)count));
            image[h][w].rgbtRed = (round((double)blurr / (double)count));
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    //create a temp image to store original values
    
    RGBTRIPLE temp[height][width];
    
    //copy from original to temporary image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    
    //loop through each pixel to claculate GX and GY
    for (int h = 0; h < height; h++)
    {

        for (int w = 0; w < width; w++)
        {
            // create GX and GY variables to hold values of the 3 by 3 grid
            int GXb = 0;
            int GXg = 0;
            int GXr = 0;

            int GYb = 0;
            int GYg = 0;
            int GYr = 0;

            //store values for current column

            //center
            GXb += temp[h][w].rgbtBlue * 0;
            GXg += temp[h][w].rgbtGreen * 0;
            GXr += temp[h][w].rgbtRed * 0;

            GYb += temp[h][w].rgbtBlue * 0;
            GYg += temp[h][w].rgbtGreen * 0;
            GYr += temp[h][w].rgbtRed * 0;

            //down
            if (h != (height - 1))
            {
                GXb += temp[h + 1][w].rgbtBlue * 0;
                GXg += temp[h + 1][w].rgbtGreen * 0;
                GXr += temp[h + 1][w].rgbtRed * 0;

                GYb += temp[h + 1][w].rgbtBlue * 2;
                GYg += temp[h + 1][w].rgbtGreen * 2;
                GYr += temp[h + 1][w].rgbtRed * 2;
            }

            //up
            if (h != 0)
            {
                GXb += temp[h - 1][w].rgbtBlue * 0;
                GXg += temp[h - 1][w].rgbtGreen * 0;
                GXr += temp[h - 1][w].rgbtRed * 0;

                GYb -= temp[h - 1][w].rgbtBlue * 2;
                GYg -= temp[h - 1][w].rgbtGreen * 2;
                GYr -= temp[h - 1][w].rgbtRed * 2;
            }

            // store values for the next column

            //center
            if (w != (width - 1))
            {
                GXb += temp[h][w + 1].rgbtBlue * 2;
                GXg += temp[h][w + 1].rgbtGreen * 2;
                GXr += temp[h][w + 1].rgbtRed * 2;

                GYb += temp[h][w + 1].rgbtBlue * 0;
                GYg += temp[h][w + 1].rgbtGreen * 0;
                GYr += temp[h][w + 1].rgbtRed * 0;
            }

            //down
            if ((h != (height - 1)) && (w != (width - 1)))
            {
                GXb += temp[h + 1][w + 1].rgbtBlue * 1;
                GXg += temp[h + 1][w + 1].rgbtGreen * 1;
                GXr += temp[h + 1][w + 1].rgbtRed * 1;

                GYb += temp[h + 1][w + 1].rgbtBlue * 1;
                GYg += temp[h + 1][w + 1].rgbtGreen * 1;
                GYr += temp[h + 1][w + 1].rgbtRed * 1;
            }

            //up
            if ((h != 0) && (w != (width - 1)))
            {
                GXb += temp[h - 1][w + 1].rgbtBlue * 1;
                GXg += temp[h - 1][w + 1].rgbtGreen * 1;
                GXr += temp[h - 1][w + 1].rgbtRed * 1;

                GYb -= temp[h - 1][w + 1].rgbtBlue * 1;
                GYg -= temp[h - 1][w + 1].rgbtGreen * 1;
                GYr -= temp[h - 1][w + 1].rgbtRed * 1;
            }

            //store values for the previous column
            //center
            if (w != 0)
            {
                GXb -= temp[h][w - 1].rgbtBlue * 2;
                GXg -= temp[h][w - 1].rgbtGreen * 2;
                GXr -= temp[h][w - 1].rgbtRed * 2;

                GYb += temp[h][w - 1].rgbtBlue * 0;
                GYg += temp[h][w - 1].rgbtGreen * 0;
                GYr += temp[h][w - 1].rgbtRed * 0;
            }

            //down
            if ((h != (height - 1)) && (w != 0))
            {
                GXb -= temp[h + 1][w - 1].rgbtBlue * 1;
                GXg -= temp[h + 1][w - 1].rgbtGreen * 1;
                GXr -= temp[h + 1][w - 1].rgbtRed * 1;

                GYb += temp[h + 1][w - 1].rgbtBlue * 1;
                GYg += temp[h + 1][w - 1].rgbtGreen * 1;
                GYr += temp[h + 1][w - 1].rgbtRed * 1;
            }

            //up
            if ((h != 0) && (w != 0))
            {
                GXb -= temp[h - 1][w - 1].rgbtBlue * (1);
                GXg -= temp[h - 1][w - 1].rgbtGreen * (1);
                GXr -= temp[h - 1][w - 1].rgbtRed * (1);

                GYb -= temp[h - 1][w - 1].rgbtBlue * (1);
                GYg -= temp[h - 1][w - 1].rgbtGreen * (1);
                GYr -= temp[h - 1][w - 1].rgbtRed * (1);
            }

            // calculate the sorbel algorithm
            int edgeG = round(sqrt(pow(GXg, 2)  + pow(GYg, 2)));
            int edgeB = round(sqrt(pow(GXb, 2)  + pow(GYb, 2)));
            int edgeR = round(sqrt(pow(GXr, 2)  + pow(GYr, 2)));

            //update pixels cap at 225
            if (edgeG < 255)
            {
                image[h][w].rgbtGreen = edgeG;
            }
            else
            {
                image[h][w].rgbtGreen = 255;
            }

            if (edgeB < 255)
            {
                image[h][w].rgbtBlue = edgeB;
            }
            else
            {
                image[h][w].rgbtBlue = 255;
            }

            if (edgeR < 255)
            {
                image[h][w].rgbtRed = edgeR;
            }
            else
            {
                image[h][w].rgbtRed = 255;
            }

        }
    }

}
