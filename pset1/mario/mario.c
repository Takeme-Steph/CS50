#include <stdio.h>
#include <cs50.h>

void space(int n);
void block(int n);

int main(void)
{
    
    //Get height from user
    int height;
    do 
    {
        height = get_int("How tall?\n");
        
    }
    //ensure it's between 1 and 8 inclusive
    while (height < 1 || height > 8);
    int i;
    int h = height;
    //alternate functions to create appropriate pyramid height
    for (i = 1; i < (height + 1); i++, h--)
    {
        space(h);
        block(i);
        printf("  ");
        block(i);
        printf("\n");
        
    }
    
    
}
//function to create appropriate number of space
void space(int n)
{ 
    for (int i = 0; i < (n - 1); i++)
    {
        printf(" ");
        
    }
   
}
//Function to create hashes
void block(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("#");
      
    }
    
}