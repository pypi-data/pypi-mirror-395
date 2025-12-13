#!/usr/bin/env python3

'''
Author = Yaqi Jiao
Date: 16th October, 2025
PART 2 (Student 2) of RE - 2 with Chetana

Description:
Read a file with amino acids and print the absolute abundances of each amino acid to a file

Procedure:
        1. import class and initialize the tool
        2. read input file, perform data type evaluation and quality control
        3. count aa numbers
        4. write result to the output file

Input: amino_count.py, amino.faa
Output: output_file

Usage Example: 
python amino_count.py data/amino.faa result/Q2_output_file

'''

import sys
# import SeqProcessingTool
from SeqProcessingTool import SeqProcessingTool

def main():
# Access arguments passed from the command line you write in the terminal
# check we have 3 arguements: the python script, input file path and output file path
        if len(sys.argv) == 3: 
                input_file_path = sys.argv[1]  
                output_file_path = sys.argv[2]
        else:
                sys.exit(1)

        try:
                ToolforQ2 = SeqProcessingTool()  # Initialize the tool
                ToolforQ2.read_fasta(input_file_path)  # Read fasta file
                result = ToolforQ2.count()  # count aa numbers 
                ToolforQ2.write_file(result, output_file_path, mode="table")  # Write the result to output file

        except FileNotFoundError:
               print(f"Error: The file '{input_file_path}' does not exist.")
               sys.exit(1)
        except ValueError as e:
               print(f"Incorrect file content: {e}")
               sys.exit(1)
        except Exception as e:
               print(f"Unexpected error: {e}")  # other errors
               sys.exit(1)

        print(f"Conversion completed!\nOutput saved to: {output_file_path}")
               
if __name__ == "__main__":
    main()