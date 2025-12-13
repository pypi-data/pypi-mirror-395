#!/usr/bin/env python3

'''
SeqProcessingTool.py

Author = Yaqi Jiao
Date: 16th October, 2025
PART 2 (Student 2) of RE - 2 with Chetana

Description:
-----------------
This is a python class for processing DNA and amino acid sequences from FASTA or fastq files.
It provides functionality for reading sequences, performing quality control, converting
DNA to amino acids, converting fastq to fasta files, handling barcodes, counting nucleotide or amino 
acid occurances, and exporting results to files.

Attributes:
-----------
data: dict, used to store header and associated sequence.
quality: dict, used to store header and associated quality sequence
standard_aas: storing standard amio acid letters
standard_dna: storing standard DNA letters with N

Methods:
--------
condon_table()
    Returns a dictionary storing the standard genetic condon table

barcode()
    Returns a list of default barcode sequences for identification and removal

read_fasta(file_path)
    1. Reads a FASTA file from given path
    2. Evaluate the data format (fasta or fastq)
    3. performs conversion and qc, different data format is processed differently
    4. stores cleaned sequences in self.data

isDNA(seq)
    Determine whether a sequence is a DNA or protein sequence by the proportion of non-base sequences in the sequence

fastq2fasta(input_f)
    If the input file is in fastq format, convert it into fasta, and return the path information
    It will generate a temp file in the py.script directory

fasta_qc(input_f)
    1. accept the fasta file, check the input file is empty or not
    2. Converts sequences to uppercase
    3. Performs quality control on the given input file object
        - 'DNA': 
            1. Perform a loose check on all letters
            2. concatenate the sequence
            3. return a cleaned dict with {header:sequence}
        - 'Protein':
            1. Replace all non-standard amino acid characters with X
            2. concatenates lines under the same header
            3. Returns a cleaned dict of with {header: sequences}.

match_convert(mode=None)
    Processes sequences in self.data based on the selected mode:
    - 'condon': 
        1. replace all T with U
        1. converts DNA sequences to amino acid sequences using codon table.
    - 'barcode': 
        1. Find barcode at the start and end of sequence.
        2. trim barcodes and corresponding quality sequence, if not matched, keep the original
        3. generate 2 dicts for sequence and quality score
        4. Returns a dictionary of processed sequences and quality sequences

count()
    1. Counts occurrences of each amino acid (or nucleotide) in self.data
    2. Returns a dictionary with characters as keys and counts as values
    3. extract the X, and sort the rest keys
    4. add X back to make sure it's at the bottom line

write_file(result_dict, output_path, mode='fasta')
    Writes a dictionary of sequences or counts to a file
    - 'fastq': outputs in fastq format
        1. unpack the tuple within the dict
        2. extract header, sequence and quality information
        3. turn the first symbol of header, from  ">" to "@"
        4. write sequences in fastq form
    - 'table': outputs in tab-delimited format
    - 'fasta': outputs in FASTA format

Test chunk:
    Use assert and simple input sequences to test that each function is functioning correctly.


Usage Example:
--------------
python SeqProcessingTool.py

tool = SeqProcessingTool()
tool.read_fasta("example.fasta")
aa_sequences = tool.match_convert(mode="condon")
counts = tool.count()
tool.write_file(aa_sequences, "aa_sequences.fasta")

'''

import time

class SeqProcessingTool:
    def __init__(self):
        self.data = {}  # data form is "header: seq/counts"
        self.quality = {}
        self.standard_aas = "ACDEFGHIKLMNPQRSTVWY"
        self.standard_dna = "ATCGN"  # here, qc allows the existence of N, but in read_file method, it will be screened more strictly

    def condon_table(self):  # generate a dictionary to store condon table
        genetic_code = {
    'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
    'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
    'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',
    'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W',

    'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
    'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',

    'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
    'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',

    'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
    'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
}
        return genetic_code
    
    def barcode(self):  # generate a list to store barcode information
        default_barcode = ['TATCCTCT', 'GTAAGGAG', 'TCTCTCCG']
        return default_barcode


#%% File reading, quality check, and pre-processing 
    # take file_path, read the file, identify the data format
    # perform the quality check and generate a clean file in dict form
    def read_fasta(self, file_path):
        with open(file_path) as input_f:
            first_char = input_f.read(1)  # extract the first letter of firstline
            input_f.seek(0)  # reset pointer

            if first_char == '>':  # input data is fasta, evaluate it's DNA or protein
                lines = input_f.readlines()  # read lines to take sample sequeces
                sample_seq = "".join([l.strip() for l in lines if not l.startswith(">")])[:1000]

                # detect non-standard DNA letters
                non_dna_chars = [base for base in sample_seq if base not in self.standard_dna]
                if non_dna_chars:
                    print(f"Warning: Non-standard DNA letters found: {set(non_dna_chars)}")

                # process DNA or protein sequence
                if self.isDNA(sample_seq):
                    print("Detected DNA FASTA file (minor non-standard bases tolerated).")
                    input_f.close()
                    with open(file_path) as f:
                        self.data = self.fasta_qc(f, mode="DNA")
                else:
                    print("Detected protein FASTA file.")
                    input_f.close()
                    with open(file_path) as f:
                        self.data = self.fasta_qc(f, mode="protein")
               
            elif first_char == '@':  # input data is fastaq, perform convertion, then qc
                temp_file_path = self.fastq2fasta(input_f)  # fastq2fasta will return a path
                with open(temp_file_path) as f:  # so we need to open it, read it again, then qc will take this temp file as input to perform qc
                    self.data = self.fasta_qc(f)
            else:  # not fastaq or fasta, raise error
                raise ValueError("Unknown file format")


    def isDNA(self, seq): 
        # NOTE: this function only perform type evaluation, not specific letter screen
        # calculate the ratio is a better way to determine data type, because there can be some non-DNA letters in DNA sequence
        non_dna_letter = 0
        for base in seq.upper():
            if base not in self.standard_dna:
                non_dna_letter += 1  # count the total number of non-DNA letters
        total_length = len(seq)
        ratio = non_dna_letter / total_length  # calculate the ratio of non-DNA letters
        if abs(ratio) > 0.5:  # threshold is adjustable
            return False
        else:
            return True


    def fastq2fasta(self, input_f): 
        # will return a file_path for downstream qc
        fasta_path = f"temp_{int(time.time())}.fasta"  # add time stamp to make sure qc won't open the wrong temp file
        # This function generates a temp file, BUT returns the path of this temp file.
        
        with open(fasta_path, "w") as fa:
            while True:
                    line = input_f.readline()
                    if not line:
                        break
                    line = line.strip()
                    if line.startswith('@'):
                        header = line
                        seq_line = input_f.readline().strip()
                        input_f.readline()  # skip the + line
                        qual_line = input_f.readline().strip()

                        header = ">" + header[1:].strip()
                        fa.write(f"{header}\n{seq_line}\n")  # write header and sequence lines into the temp file
                        self.quality[header] = qual_line
            return fasta_path  # return temp file path 


    # conduct quality check of input file
    # call isDNA in this function
    # This function generate a cleaned version file for downstreaming processing  
    def fasta_qc(self, input_f, mode="DNA"):
        header = ""
        clean_dic = {}  # generate a dictionary to store headers and CLEAN, filtered and concatenated sequences
        # standard_aas = self.standard_aa()
        # make sure it's not empty
        for line in input_f: 
            if not line:
                raise ValueError("Empty sequence encountered!")
               
            # read the header line, and store it in header
            line = line.strip()
            if line.startswith(">"):
                header = line
                clean_dic[header] = ""  # initialize the key-value pair, prepare for the seq concatenation
                continue

            line = line.upper()  # turn all the lowercase letter into uppercase and

            #evaluate the data type of file, if it's protein, filter non-aa letters 
            if mode == "DNA":
                # Perform strict check, if there are any non-DNA letters, capture it
                if not all(c in self.standard_dna for c in line):
                    raise ValueError(f"Non-DNA character found in {header}: {line}")
                # The DNA sequence remains as is, just concatenate the sequence
                # More DNA filtering logic can be added here in the future
                clean_dic[header] += line

            elif mode == "protein":
                # Protein sequence, replacing non-standard amino acids with X
                line = "".join(c if c in self.standard_aas else "X" for c in line)  # filter the non-aa sequences
                clean_dic[header] += line
                       
            # header = ""  # clear header, prepare for next matching

        return clean_dic

#%% Main functions of the class

    # find the matched patterns in the sequence
    # By setting different modes, different pattern matching and processing are performed on the sequence
    def match_convert(self, mode = None):
            result = {}  # used to store all outputs 
            condon_table = self.condon_table()  # load condon table
            barcode = self.barcode()  # load the barcode information

            # In this question, reverse is unnecessary, so just replace 'T' with 'N'
            # if reverse needs to be added, add HERE
            if mode == "condon":
                for header, seq in self.data.items():
                    aa_seq_list = []  # generate an empty list to store converted amino acids
                    aa_seq = "" # generate a string to store concatenated aa letters
                    seq = seq.upper().replace('T', 'U')  # replace 'T' into 'U '
                    
                    condon_num = len(seq)//3  # calculate the number of converted amino acids
                    # NOTE: Since the number of bases is not necessarily a multiple of 3, and the start codon is not considered, the remaining bases are ignored.
                    for i in range(condon_num):
                        condon = seq[i*3: i*3 + 3]  # extract corresponding bases through string slicing
                        # NOTE Python slices cannot use commas (a,b), use [:] 
                        # aa = self.condon_table[condon] 
                        aa = condon_table.get(condon, "X")  # find the matching amino acids in condon table
                        aa_seq_list.append(aa)  # add the converted amino acids into the list
                    aa_seq = "".join(aa_seq_list)  # generate the sequence string under specific header
                    result[header] = aa_seq
                    

            elif mode == "barcode":
                # set the output dictioanry based on matched barcode
                first_output, second_output, third_output, undetermined_output = {}, {}, {}, {}
                first_qual, second_qual, third_qual, undetermined_qual = {}, {}, {}, {}

                for header, seq in self.data.items():
                    qual = self.quality.get(header)
                    matched = False

                    for b in barcode:
                        # Look for the barcode at the beginning and the end of the sequence
                        # trim sequence and quality sequence through position and string slicing operations
                        if seq.startswith(b):
                            seq_trimmed = seq[len(b):]
                            qual_trimmed = qual[len(b):]
                        elif seq.endswith(b):
                            seq_trimmed = seq[:-len(b)]
                            qual_trimmed = qual[:-len(b)]
                        else:
                            continue

                            # after the trimming, distribute sequences and quality scores into different groups using dict
                        if b == barcode[0]:  # TATCCTCT
                            first_output[header] = seq_trimmed
                            first_qual[header] = qual_trimmed
                        elif b == barcode[1]:  # GTAAGGAG
                            second_output[header] = seq_trimmed
                            second_qual[header] = qual_trimmed
                        elif b == barcode[2]:  # TCTCTCCG
                            third_output[header] = seq_trimmed
                            third_qual[header] = qual_trimmed
                        matched = True
                        break
                    if not matched:
                        undetermined_output[header] = seq
                        undetermined_qual[header] = qual

                header = ""  # empty the header to accept new data
                result = {
                    barcode[0]:(first_output, first_qual),
                    barcode[1]: (second_output, second_qual),
                    barcode[2]: (third_output, third_qual),
                    "undetermined": (undetermined_output, undetermined_qual)
                }  # NOTE: the value of the output dict of "barcode" mode is tuple
            
            return result
                                            
    # count the number of each letters
    def count(self):
        counts = {}
        for seq in self.data.values():
            for char in seq:
                
                counts[char] = counts.get(char, 0) + 1
                # the counting function of dictionary
                # if char is in the dictionary, return value + 1, if not, return 0 + 1
        # if there is X in the sequence, put it the last row
        x_count = counts.pop("X", 0)  #extract the specified "X" and corresponding values of X from counts
        # if there is no X, return default: 0
        sort_keys = sorted(counts.keys()) 
        ordered_counts = {}
        for key in sort_keys:
            ordered_counts[key] = counts[key]
        
        if x_count > 0:  # if there is X in counts, add this pair at the end of the dict, if no X, no operation
            ordered_counts["X"] = x_count

        return ordered_counts  # return a dictionary of counts, with X in the last row
    
#%% Write files  
    # now we have dictionaries storing necessary information, still need to output them in general form
    # take a dictionary as input, output them as following forms:
    # {key}\n{value} (fasta form),
    # {key}\t{value} (table form)
    # {header}\n{trimmed_seq}\n+\n{quality score} (fastq form)
    def write_file(self, result_dict, output_path, mode = "fasta"):
        with open(output_path, "w") as output_f:
            if mode == "fastq":
                seq_dict, qual_dict = result_dict  # Unpacking the tuple first
                for header in seq_dict:
                        seq = seq_dict[header]
                        qual = qual_dict[header]  # they share the same header
                        header_fastq = header
                        if header.startswith(">"):
                            header_fastq = "@" + header[1:]  # convert '>' to '@'
                        output_f.write(f"{header_fastq}\n{seq}\n+\n{qual}\n")
                        # Extract values ​​from the tuple and output them in fastq format
                        # output_f.write("\n")
            else:
                for key, value in result_dict.items():               
                    if mode == "fasta":
                        output_f.write(f"{key}\n{value}\n\n")
                    if mode == "table":
                        output_f.write(f"{key}\t{value}\n")

                    

