#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>


int main(int argc, string argv[])
{
   
    //checks if there'a a 26 letter string
    if ((argc != 2) || (strlen(argv[1]) != 26))
    {
        printf("Please input a single 26 character key, with no repitition or number\n");
        return 1;
    }
    
    //checks for numbers in the string
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (argv[1][i] < 'A' || argv[1][i] > 'z')
        {
            printf("Please input a single 26 character key, with no repitition or number\n");
            return 1; 
        }
    }
        
    //checks for duplicates in the string (case insensitive)
    for (int i = 0 ; i < strlen(argv[1]); i++)
    {
        for (int n = i + 1; n < strlen(argv[1]); n++)
        {
            if (tolower(argv[1][i]) == tolower(argv[1][n]))
            {
                printf("Please input a single 26 character key, with no repitition or number\n");
                return 1;
            }
        }
    }

    // get plain text from user
    string plain = get_string("plaintext:");
    
    //create cipher text
    char cipher[strlen(plain)];
    string alpha = "abcdefghijklmnopqrstuvwxyz";
    
    printf("ciphertext:");
    
    //go through each char in plain text
    for (int p = 0; p < strlen(plain); p++)
    {
        // check if alphabet
        if (plain[p] >= 'A' && plain[p] <= 'z')
        {
            // go through each char in aplha
            for (int a = 0; a < strlen(alpha); a++)
            {
                //check if they match to know the position, case insensitive
                if (tolower(plain[p]) == alpha[a])
                {
                    // create cipher text if capital
                    if (plain[p] >= 'A' && plain[p] <= 'Z')
                    {
                        cipher[p] = toupper(argv[1][a]);
                        printf("%c", cipher[p]);
                        a = 25;
                    }
                    // create cipher text is small 
                    else if (plain[p] >= 'a' && plain[p] <= 'z')
                    {
                        cipher[p] = tolower(argv[1][a]);
                        printf("%c", cipher[p]);
                        a = 25;
                    }
    
                }
            
            }
        
        
           
        }
        
        // return non alphabet characters
        else if (plain[p] < 'A' || plain[p] > 'z')
        {
            cipher[p] = plain[p];
            printf("%c", cipher[p]);
        }
    }
    
    
    printf("\n");
    
    // The cs50 bot refused to take the results as a string so i had to print it letter by letter

}