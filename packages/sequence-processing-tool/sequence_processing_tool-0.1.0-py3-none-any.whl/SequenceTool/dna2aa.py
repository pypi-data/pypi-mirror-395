#!/usr/bin/env python3

'''
Author = Yaqi Jiao
Date: 16th October, 2025
PART 2 (Student 2) of RE - 2 with Chetana

Description:
Read a DNA file and convert the DNA to amino acids

Procedure:
1. import class and initialize the tool
2. read input file, perform data type evaluation and quality control
3. convert DNA to amino acids
4. write result to the output file

Input: dna2aa.py, genes.fna
Output: output_file

Usage Example:
python dna2aa.py data/genes.fna result/Q1_output_file
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
                ToolforQ1 = SeqProcessingTool()  # Initialize the tool       
                ToolforQ1.read_fasta(input_file_path)  # Read fasta file
                result = ToolforQ1.match_convert("condon")  # Convert DNA to amino acids
                ToolforQ1.write_file(result, output_file_path)  # Write the result to output file

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