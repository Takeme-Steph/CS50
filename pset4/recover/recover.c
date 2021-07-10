#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    //checks if there'a a 26 letter string
    if (argc != 2)
    {
        printf("Please input a single file\n");
        return 1;
    }


    // open file
    FILE *fr = fopen("card.raw", "r");
    
    // check if file is readable
    if (fr == NULL)
    {
        printf("Could not open\n");
        return 1;
    }
    
    
    // declare a buffer for the fread
    BYTE buffer[512];
    // jpeg filename counter
    int count = 0;
    // jpeg finder counter
    int jpegf = 0;
    // new jpeg file pointer
    FILE *img;

    // loop through file 
    while (1)
    {
        // read byte per byte for a block
        int end = fread(buffer, 1, 512, fr);
        
        // if at end of file close all files and stop
        if (end == 0) 
        {
            // close all files and exit
            fclose(img);
            fclose(fr);
    
            return 0;
        }
        
        // check if first 4 bytes of block match a jpeg header
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0))
        {
            jpegf++;
            
            //if the first jpeg found
            if (jpegf == 1)
            {
                //create file name
                char filename[15];
                sprintf(filename, "%03i.jpg", count);
                count++;
                // create new jpg
                img = fopen(filename, "w");
                // write from buffer block to new jpeg
                fwrite(buffer, 1, 512, img);
            }
            
            // if not create a new file
            else
            {
                //close and stop writting to current jpeg
                fclose(img);
                //create new jpeg
                char filename[15];
                sprintf(filename, "%03i.jpg", count);
                count++;
                // create new jpg
                img = fopen(filename, "w");
                // write from buffer block to new jpeg
                fwrite(buffer, 1, 512, img);
         
            }
        }
        
        // if not start of a jpeg then continue writing
        else
        {
            //keep writing to current jpeg
            if (jpegf >= 1)
            {
                fwrite(buffer, 1, 512, img);
            }
            
        }
        
        
            
        
        
    }
    
}
