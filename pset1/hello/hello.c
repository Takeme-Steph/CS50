#include <stdio.h>
#include <cs50.h>

int main(void)
{
    
    //Get name from user
    string name = get_string("what's your name?\n");
    
    //Print hello name
    printf("hello,%s \n", name);
    
}