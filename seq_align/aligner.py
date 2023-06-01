from Bio import pairwise2
from Bio.Align import substitution_matrices

blosum62 = substitution_matrices.load("BLOSUM62")

def parse_sequence_data(data):
    seqs = []

    string = data.replace('\n', '')
    if len(re.findall("protein_coding", string)) > 1:
        if re.findall(">", string):
            string1 = string + '>'
            string1 = re.findall("(?<=protein_coding)(.+?)(?=>)", string)
            for i in string1:
                seqs.append(i)
        else:
            string1 = string.split(' ')
            for split in string1:
                line1 = re.findall("protein_coding.+", split)
                for line in line1:
                    line = line.split("protein_coding")[1]
                    if re.findall("ENSAM", line):
                        line = re.findall(".+(?=ENSAM)", line)[0].split("ENSAM")[0]
                        seqs.append(line)
                    else:
                        seqs.append(line)


    elif len(re.findall("protein_coding", string)) == 1:
        string1 = re.findall("protein_coding.+", string)[0]
        string1 = string1.split("protein_coding")[1]
        seqs.append(string1)

    else:
        string1 = string
        seqs.append(string1)

    return seqs

def pairwise_alignment(seq1, seq2):
    return pairwise2.align.globalds(seq1, seq2, blosum62, -10, -0.5)