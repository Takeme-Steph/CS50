#include <stdio.h>
#include <cs50.h>

int length(long cardcon);

int main(void)
{
    
    //get credit card details from user
    
    int cardlen;
    long card;
    card = get_long("Please input credit card number\n");
        
    //get lenght of digits
    cardlen = length(card);
    
        
    //seperate each number
    long dval = 1;
    int sum = 0;
    for (int i = 0; i < cardlen; i++, dval = dval * 10)
    {
        int num = (card / dval) % 10;
        
        //multiply every other digit by 2, starting from the second-to-last digit
        if (i % 2 != 0)
        {
            int ev = num * 2;
            int evl = length(ev);
            int evd = 1;
            int sumd = 0;
            //seperate the multiplied result into individual digits and add to a grand sum
            for (int j = 0; j < evl; j++, evd = evd * 10)
            {
                sumd = ev / evd % 10;
                sum = sum + sumd;
            
            }
            
        }
        //sum the other numbers that were not multiplied
        else
        {
            
            sum = sum + num;
        }
        
        
    }
    
    // check if last digit is zero
        
    char check;
    if (sum % 10 == 0)
     
    {
        check = 121;
    }
    else
    {
        check = 110;
    }
        
    
    // get the first 2 numbers 
    int fn;
    //get first number
    long fd = 1;
    for (int j = 1; j < cardlen; j++)
    {
        fd =  fd * 10;
           
    }
    fn = (card / fd) % 10;
         
    //get second number
    int sn;
    fd = 1;
    for (int j = 2; j < cardlen; j++)
    {
        fd =  fd * 10;
            
    }
    sn = (card / fd) % 10;
       
    // check the type of card
    if ((cardlen == 15) && (check == 121) && (fn == 3) && ((sn == 4) || (sn == 7)))
    {
        printf("AMEX\n");
    }
    else if ((cardlen == 16) && (fn == 5) && (check == 121) && ((sn == 1) || (sn == 2) || (sn == 3) || (sn == 4) || (sn == 5)))
    {
        printf("MASTERCARD\n");
    }
    else if (((cardlen == 13) || (cardlen == 16)) && (check == 121) && (fn == 4))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
        
    }
    
    
   
    
}

//function to count lenght 
int length(long n)
{
    int l;
    for (int i = 0; n > 0; i++, l = i)
    {
        
        n = n / 10;
     
    }
    return l;
}