// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <strings.h>
#include <cs50.h>

#include "dictionary.h"



// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
// 2^16
const unsigned int N = 65536;

// Hash table
node *table[N];

// variable to count words for size function
int sizecount = 0;




// Returns true if word is in dictionary else false
bool check(const char *word)
{
  
    //hash the word to find its linked list location
    int point = hash(word);
    
    // go to list position and loop through to find the word

    // set temp node to check for matching word
    node *check;
    // make it point to first node on the linked list to begin the loop
    check = table[point];
    
    //loop through to find matching word
    while (check != NULL)
    {

        //check if match
        if (strcasecmp(check->word, word) == 0)
        {
            return true;
        }
        // else move to next
        else
        {
            check = check->next;
            
        }
        
        
    }
    // not found
    return false;
}





// Hashes word to a number
unsigned int hash(const char *word)
{
    //generates the hash code for a word
    // source : https://github.com/hathix/cs50-section/blob/master/code/7/sample-hash-functions/good-hash-function.c
    unsigned long hash = 5381;

    for (const char *ptr = word; *ptr != '\0'; ptr++)
    {
        hash = ((hash << 5) + hash) + tolower(*ptr);
    }

    return hash % N;
}



// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{   
    //open dictionary
    FILE *dic = fopen(dictionary, "r");
    
    // check if successfully opened
    if (dic == NULL)
    {
        printf("cannot open dictionary\n");
        return false;
    }
    
    // buffer to store words
    char word[LENGTH + 1];
    
    while (fscanf(dic, "%s", word) != EOF)
    {
        // malloc space for new word
        node *n = malloc(sizeof(node));
        
        // check if successful
        if (n == NULL)
        {
            //close file and exit
            fclose(dic);
            printf("not enough memory\n");
            return false;
        }
        
        else
        {
            //copy new word into node
            strcpy(n->word, word);
            // set next pointer to null
            n->next = NULL;
        
            // hash new word
            int point = hash(word);
        
            //insert new node
            n->next = table[point];
            table[point] = n;

            //increase word count for size function
            sizecount++;
        
        }
        
        
    }
    //close file
    fclose(dic);
    return true;
}



// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // returns sizecount variable, already counted while loading dictionary
    return sizecount;
}



// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // loop through all linked lists in the table array
    for (int i = 0; i < N; i++)
    {
        //temp pointers to help keep track
        node *check = table[i];
        node *tmp = table[i];
        
        //loop through all nodes in linked list
        while (check != NULL)
        {
            check = check->next;
            free(tmp);
            tmp = check;
        }
        
    }
    
    
    return true;
}
