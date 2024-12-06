// Implements a dictionary's functionality

#include "dictionary.h"
#include <cs50.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 78;

// Hash table
node *table[N];

// Word count
unsigned int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hashindex = hash(word); // Hash word for hash value
    for (node *cursor = table[hashindex]; cursor != NULL;
         cursor = cursor->next) // Search hash table at value location
    {
        if (strcasecmp(word, cursor->word) == 0) // Return true if found
        {
            return true;
        }
    }
    return false; // Return false otherwise
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c;
    while ((c = *word++))
    {
        hash = ((hash << 5) + hash) + toupper(c); // hash * 33 + c
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    FILE *dict = fopen(dictionary, "r"); // Open dictionary file
    if (dict == NULL)
    {
        printf("Loading error \n");
        return false;
    }
    char word[LENGTH + 1];
    while (fscanf(dict, "%s", word) != EOF) // Read each word in the file
    {
        node *n = malloc(sizeof(node)); // Create new hash table node space
        n->next = NULL;
        if (n == NULL)
        {
            return false;
        }

        int hashindex = hash(word);

        strcpy(n->word, word); // Copy word into node

        if (table[hashindex] == NULL) // Add new node to hash table
        {
            table[hashindex] = n;
        }
        else
        {
            n->next = table[hashindex];
            table[hashindex] = n;
        }
        word_count += 1; // Add one to word count
    }
    fclose(dict); // Close the file
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int hashindex = 0; hashindex < N; hashindex++)
    {
        node *cursor = table[hashindex];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
