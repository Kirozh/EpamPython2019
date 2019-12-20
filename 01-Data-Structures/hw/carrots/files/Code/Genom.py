input_file_name = "dna.fasta"
codon_table_file_name = 'rna_codon_table.txt'


def read_rna_codon_table(file_name):
    """This function reads data from codon file and forms dictionary
    :param file_name: name of data-codon-file
    :return: dictionary

    """

    codon_table = open(file_name, 'r')
    codon_dict = {}
    iskey = True  # is current symbol locates in key
    isvalue = False  # is current symbol locates in value
    current_key = ''
    current_value = ''
    currently_in_pair_key_value = True  # is current space inside in pair key-value or it is outside

    for line in codon_table:
        for c in line:
            if c.isalpha():
                currently_in_pair_key_value = True
                if iskey:
                    current_key += c
                elif isvalue:
                    current_value += c
            else:
                if c == ' ':
                    if current_value == '' and currently_in_pair_key_value:
                        iskey = False
                        isvalue = True
                    else:
                        if currently_in_pair_key_value:
                            currently_in_pair_key_value = False
                            codon_dict.update({current_key: current_value})
                            iskey = True
                            isvalue = False
                            current_key = ''
                            current_value = ''
                elif c == '\n':
                    currently_in_pair_key_value = False
                    codon_dict.update({current_key: current_value})
                    iskey = True
                    isvalue = False
                    current_key = ''
                    current_value = ''

    codon_table.close()
    return codon_dict


def count_nucleotides(file_name):
    """This function counts nucleotides in file f by scanning all symbols
    in file lines that include only nucleotides
    :param file_name: string of file path or only file-name

    """

    input_file = open(file_name, 'r')
    count_nucleotides_file = open("counting_nucleotides.txt", 'w')
    nucleo_base = {"G": 0, "C": 0, "T": 0, "A": 0}  # dictionary with nucleotide-keys
    row = 0  # row number

    for lines in input_file:
        if not lines.startswith('>'):  # if this line includes only nucleotides
            nucleo_base.update({'G': nucleo_base['G'] + lines.count('G')})
            nucleo_base.update({'C': nucleo_base['C'] + lines.count('C')})
            nucleo_base.update({'T': nucleo_base['T'] + lines.count('T')})
            nucleo_base.update({'A': nucleo_base['A'] + lines.count('A')})

        elif row != 0:  # Checking if current line starts with '>' that means that first amount of nucleotides is over
                        # and counting must start anew
            count_nucleotides_file.write(str(tuple(nucleo_base.items())) + '\n')
            nucleo_base.update([("G", 0), ("C", 0), ("T", 0), ("A", 0)])  # zeroing dictionary

        row += 1

    count_nucleotides_file.write(str(tuple(nucleo_base.items())) + '\n')
    count_nucleotides_file.close()
    input_file.close()


def translate_dna_to_rna(file_name):
    """This function translates dna code to rna by replacing
    nucleotide G on C, C on G, T on A, A on U.
    :param file_name: file-path or file-name string

    """

    data_file = open(file_name,'r')
    dna_to_rna_file = open("translation_dna_to_rna.txt", 'w')
    for line in data_file:
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
            dna_to_rna_file.write(" ".join([line[:-1], '\n']))

    dna_to_rna_file.close()
    data_file.close()


def translate_rna_to_protein(codon_file_name):
    """ This function first of all reads codones from rna_codon_table file.
        Then it fills dictionary with rna-sequences and matched to them codones.
        After that the function takes rna_file, forms strings for each gene, devides line by three symbol and
        writes matching codon to output file - protein.

    """

    protein = open('translation_rna_to_protein.txt', 'w')
    rna_file = open('translation_dna_to_rna.txt', 'r')  # file that was got by translating DNA to RNA
    codon_dict = read_rna_codon_table(codon_file_name)
    ''' using function read_rna_codon_table to read codons and sequenced to them rna'''

    string_of_nucleotides = ''  # string of rna-nucleotides that must be translated to protein
    array_of_strings = []  # saving different genes
    array_of_protein_names = []  # saving gene`s names

    # reading rna_file and share different genes
    for line in rna_file:
        if line.startswith('>'):
            array_of_protein_names.append(line)
            if string_of_nucleotides != '':
                array_of_strings.append(string_of_nucleotides)
        else:
            string_of_nucleotides += line[:-1]

    array_of_strings.append(string_of_nucleotides)

    # translating rna to protein
    for i, string_of_nucleotides in enumerate(array_of_strings):
        protein.write(array_of_protein_names[i])  # writing gene`s name

        i = 0
        while i < len(string_of_nucleotides)-1:
            nucleotides_triple = string_of_nucleotides[i:i+3]

            for key in codon_dict:
                if key == nucleotides_triple:
                    protein.write(codon_dict[key] + ' ')

            if i % 90 == 0 and i != 0:  # newline for better file`s readability
                protein.write('\n')
            i += 3
        protein.write('\n')

    protein.close()
    rna_file.close()


translate_dna_to_rna(input_file_name)
count_nucleotides(input_file_name)
read_rna_codon_table(codon_table_file_name)
translate_rna_to_protein(codon_table_file_name)
