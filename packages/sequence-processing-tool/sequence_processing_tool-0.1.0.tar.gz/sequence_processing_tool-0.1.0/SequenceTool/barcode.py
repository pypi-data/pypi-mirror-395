#!/usr/bin/env python3

'''
Author = Yaqi Jiao
Date: 16th October, 2025
PART 2 (Student 2) of RE - 2 with Chetana

Description:
Read a DNA file, read a barcode file, trim the barcodes, and write the final DNA to a file

Procedure:
        1. import class and initialize the tool
        2. read input fastq file, convert to fasta file, then quality control
        3. trim the barcodes
        4. write result to the output file according to their barcode. If one dict is empty, no output will be written

Input: barcode.py, amino.faa
Output: output_file.fastq

Usage Example:
python barcode.py data/barcode.fastq result/Q3_sample
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
                ToolforQ3 = SeqProcessingTool()  # Initialize the tool
                ToolforQ3.read_fasta(input_file_path)  # Read file
                result = ToolforQ3.match_convert("barcode")  # trim the barcodes
                # iterate all sub-dictionaries within result
                # By using format, the contents of different sub-dictionaries are output to different files
                for barcode, subdict in result.items():
                        if not subdict:  # if any sub-dict is empty, skip it
                                continue
                        ToolforQ3.write_file(subdict, f"{output_file_path}_{barcode}.fastq", mode = "fastq")

        except FileNotFoundError:
               print(f"Error: The file '{input_file_path}' does not exist.")
               sys.exit(1)
        except ValueError as e:
               print(f"Incorrect file content: {e}")
               sys.exit(1)
        except Exception as e:
               print(f"Unexpected error: {e}")
               sys.exit(1)


        print(f"Conversion completed!\nOutput saved to: {output_file_path}")

if __name__ == "__main__":
    main()