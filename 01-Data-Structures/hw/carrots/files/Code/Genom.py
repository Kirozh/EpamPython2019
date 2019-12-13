input_file_name = "dna.fasta"


def translate_from_dna_to_rna(file_name):
    """This function translates dna code to rna by replacing
    nucleotide G on C, C on G, T on A, A on U.

    """
    f = open(file_name,'r')
    dna_to_rna_file = open("translation_from_dna_to_rna.txt", 'w')
    for line in f:
        if not line.startswith('>'):
            for letter in line:
                if letter == 'G':
                    dna_to_rna_file.write('C')
                elif letter == 'C':
                    dna_to_rna_file.write('G')
                elif letter == 'T':
                    dna_to_rna_file.write('A')
                elif letter == 'A':
                    dna_to_rna_file.write('U')
                else:
                    dna_to_rna_file.write('\n')
        else:
            dna_to_rna_file.write(" ".join([line[:-1], "translated to RNA", '\n']))

    dna_to_rna_file.close()
    f.close()


def count_nucleotides(file_name):
    """This function counts nucleotides in file f by scanning all symbols
    in file lines that include only nucleotides
    :param f: input file

    """

    f = open(file_name, 'r')
    count_nucleotides_file = open("counting_nucleotides.txt", 'w')
    nucleo_base = {"G": 0, "C": 0, "T": 0, "A": 0}  # dictionary with nucleotide-keys
    row = 0  # row number

    for lines in f:
        if not lines.startswith('>'):  # if this line includes only nucleotides
            nucleo_base.update({'G': nucleo_base.get('G') + lines.count('G')})
            nucleo_base.update({'C': nucleo_base.get('C') + lines.count('C')})
            nucleo_base.update({'T': nucleo_base.get('T') + lines.count('T')})
            nucleo_base.update({'A': nucleo_base.get('A') + lines.count('A')})

        elif row != 0:  # Checking if current line starts with '>' that means that first amount of nucleotides is over
                        # and counting must start anew
            count_nucleotides_file.write(str(tuple(nucleo_base.items())) + '\n')
            nucleo_base.update([("G", 0), ("C", 0), ("T", 0), ("A", 0)])  # zeroing dictionary

        row += 1

    count_nucleotides_file.write(str(tuple(nucleo_base.items())) + '\n')
    count_nucleotides_file.close()
    f.close()


def translate_rna_to_protein():
    """This function first of all reads codones from rna_codon_table file.
    Then it fills dictionary with codons and matched to them rna-sequences.
    After that this function takes input file, divides each line by three symbol and
    writes matching codon to output file - protein

    """

    codon = open('rna_codon_table.txt', 'r')
    protein = open('rna_to_protein.txt', 'w')
    rna_file = open('translated_from_dna_to_rna.txt', 'r')

    codon_d = {}

    for line in codon:
        # processing lines in codon-file that don`t include STOP

        if (not line.startswith('UAA')) and (not line.startswith('UAG')) and (not line.startswith('UGA')):
            i = 0
            for j in range(4):
                codon_d.update({line[i:i+3]: line[i+4]})
                i += 11

        # processing line that include STOP
        else:
            codon_d.update({line[0:3]: line[4:8]})
            i = 11
            for j in range(3):
                codon_d.update({line[i:i + 3]: line[i + 4]})
                i += 11

    # translating rna to protein
    for line in rna_file:
        if not line.startswith('>'):
            i = 0
            len_ = len(line)

            while i < len_ - 1:
                temp_string = line[i: i + 3]
                protein.write(str(codon_d.get(temp_string)) + ' ')
                i += 3

            protein.write('\n')

        else:
            protein.write(str(line[:-5]) + 'protein\n')

    protein.close()
    codon.close()
    rna_file.close()


translate_from_dna_to_rna(input_file_name)
count_nucleotides(input_file_name)
translate_rna_to_protein()


