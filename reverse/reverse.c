#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

const int header_size = 44;

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 3)
    {
        printf("Usage: ./reverse [input.wav] [output.wav]\n");
        return 1;
    }

    // Open input file for reading
    FILE *file1 = fopen(argv[1], "r");
    if (file1 == NULL)
    {
        printf("Error: file could not be opened\n");
        return 1;
    }

    // Read header into an array
    WAVHEADER head;
    fread(&head, sizeof(head), 1, file1);

    // Use check_format to ensure WAV format
    if (check_format(head) != 0)
    {
        printf("Invalid file format\n");
        return 2;
    }

    // Open output file for writing
    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Can't open output file\n");
        return 1;
    }
    // Write header to file
    fwrite(&head, sizeof(head), 1, output);

    // Use get_block_size to calculate size of block
    int block_size = get_block_size(head);

    // Write reversed audio to file
   
}

int check_format(WAVHEADER header)
{
    if (header.format[0] == 'W' && header.format[1] == 'A' && header.format[2] == 'V' && header.format[3] == 'E')
    {
        return 0;
    }
    return 1;
}

int get_block_size(WAVHEADER header)
{
    int block_size = header.numChannels * (header.bitsPerSample / 8);
    return block_size;
}