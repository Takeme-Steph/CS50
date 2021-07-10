#include <stdio.h>
#include <cs50.h>
#include <string.h>


int main(void)
{
    //get text
    string text = get_string("Text: ");
    
    //set letter, word count
    int letters = 0;
    int words = 1; // +1 for the final period in the text
    int sentences = 0;
    
    //loop through text and count letters
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] >= 'A' && text [i] <= 'z')
        {
            letters++;
        }
        
    }
    
    //loop through text and count words
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            words++;
        }
       
    }
    
    //loop through text and count setences
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;
        }
       
    }
    
    // calc average letters per words
    float l = (100 / (float)words) * letters;
    
    // calc average sentences per words
    float s = (100 / (float)words) * sentences;
    
    //calc index
    float index = 0.0588 * l - 0.296 * s - 15.8;
    
    //print results
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %0.f\n", index);
    }
    
}