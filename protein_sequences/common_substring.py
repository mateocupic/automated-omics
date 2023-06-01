def longest_common_substring(seq1, seq2):
    matrix = [[0] * (1 + len(seq2)) for i in range(1 + len(seq1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(seq1)):
        for y in range(1, 1 + len(seq2)):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x][y] = matrix[x - 1][y - 1] + 1
                if matrix[x][y] > longest:
                    longest = matrix[x][y]
                    x_longest = x
            else:
                matrix[x][y] = 0
    return seq1[x_longest - longest: x_longest]