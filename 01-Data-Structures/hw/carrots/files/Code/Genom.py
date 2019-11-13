dna_fasta = open("Data.txt", 'r')
# dna_fasta = open('dna.fasta', 'r')

dna_to_rna = open("Translated_from_dna_to_rna.txt", 'w')

count = open("Count_nucleotides.txt", 'w')


def translate_from_dna_to_rna(f):
    #dna_to_rna = open("Translated_from_dna_to_rna", 'w')
    for line in f:
        if not line.startswith('>'):

            for letter in line:

                if letter == 'G':
                    dna_to_rna.write('C')

                elif letter == 'C':
                    dna_to_rna.write('G')

                elif letter == 'T':
                    dna_to_rna.write('A')

                elif letter == 'A':
                    dna_to_rna.write('U')

                else:
                    dna_to_rna.write('\n')

        else:

            dna_to_rna.write(" ".join([line[:-1], "translated to RNA", '\n']))

    dna_to_rna.close()
    #return dna_to_rna
    # return output


def count_nucleotides(f):

    nucleo_base = {"G": 0, "C": 0, "T": 0, "A": 0}
    row = 0  # row number

    for lines in f:
        if not lines.startswith('>'):
            # print(lines)
            # Считаем количество вхождений
            nucleo_base.update({'G': nucleo_base.get('G') + lines.count('G')})
            nucleo_base.update({'C': nucleo_base.get('C') + lines.count('C')})
            nucleo_base.update({'T': nucleo_base.get('T') + lines.count('T')})
            nucleo_base.update({'A': nucleo_base.get('A') + lines.count('A')})

            # for letter in lines:
            #     if letter == 'G':
            #         num = nytro_base.get('G')
            #         num += 1
            #         nytro_base.update({"G": num})
            #     elif letter == 'C':
            #         num = nytro_base.get('C')
            #         num += 1
            #         nytro_base.update({"C": num})
            #     elif letter == 'T':
            #         num = nytro_base.get('T')
            #         num += 1
            #         nytro_base.update({"T": num})
            #     else:
            #         num = nytro_base.get('A')
            #         num += 1
            #         nytro_base.update({"A": num})
        elif row != 0:
            #
            #print(nucleo_base.items())
            count.write(str(tuple(nucleo_base.items())) + '\n')  # записываем в файл
            nucleo_base.update([("G", 0), ("C", 0), ("T", 0), ("A", 0)])  # обнуляем словарь

        # print(nytro_base.items())
        row += 1
    count.write(str(tuple(nucleo_base.items())) + '\n')
    # dict_list.append(tuple(nucleo_base.items()))
    count.close()
    # return dict_list

# print(f.read())


def translate_rna_to_protein():
    codon = open('rna_codon_table.txt', 'r')
    # cod = open('rna_cod.txt', 'w')
    protein = open('rna_to_protein.txt', 'w')

    try:
        rna = open('Translated_from_dna_to_rna.txt', 'r')
    except IOError:
        print('no file')

    codon_d = {}  # считывание кодонов из файла rna_codon, и добавление каждого из них словарь
    for line in codon:
        # print(line)
        '''
        обработка строк файла rna_codon_table, в которых нет слова stop
        '''
        if (not line.startswith('UAA')) and (not line.startswith('UAG')) and (not line.startswith('UGA')):

            i = 0
            for j in range(4):
                codon_d.update({line[i:i+3]: line[i+4]})
                i += 11
        # обработка строк, в которых есть слово stop
        else:

            codon_d.update({line[0:3]: line[4:8]})
            i = 11
            for j in range(3):
                codon_d.update({line[i:i + 3]: line[i + 4]})
                i += 11

    # перевод rna в protein

    for line in rna:
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
    # dna_to_rna.close()
    codon.close()


translate_from_dna_to_rna(dna_fasta)

count_nucleotides(dna_fasta)

translate_rna_to_protein()

dna_fasta.close()
dna_to_rna.close()
