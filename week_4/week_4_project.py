''' Week 4 Project '''

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
  ''' 
  input: alphabet: set of characters, three scores(integer)
  output: dictionary of dictionaries whose entries are indexed by pairs of
  characters in alphabet plus -.
  '''

  scoring_matrix = {}
  scoring_matrix['-'] = {}

  #initialize an object for each letter
  for char1 in alphabet:
    scoring_matrix[char1] = {}
    scoring_matrix['-'][char1] = dash_score
    for char2 in alphabet:
      if char1 == char2:
        scoring_matrix[char1][char2] = diag_score
      else:
        scoring_matrix[char1][char2] = off_diag_score
    scoring_matrix[char1]['-'] = dash_score
    
  scoring_matrix['-']['-'] = dash_score

  return scoring_matrix



def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
  '''
  Return an alignment matrix for two sequences(strings).
  If global flag is true: Compute global alignment matrix, otherwise
  local.
  '''

  alignment_matrix = []
  seq_x_length = len(seq_x)
  seq_y_length = len(seq_y)
  for row in range(0, seq_x_length + 1):
    current_row = []
    for col in range(0, seq_y_length + 1):
      current_row.append(0)
    alignment_matrix.append(current_row)

  
  for row in range(1, seq_x_length + 1):
    char = seq_x[row - 1]
    align_matrix_value = alignment_matrix[row - 1][0] + scoring_matrix[char]['-']
    if align_matrix_value < 0 and not global_flag:
      alignment_matrix[row][0] = 0
    else:
      alignment_matrix[row][0] = alignment_matrix[row - 1][0] + scoring_matrix[char]['-']

  for col in range(1, seq_y_length + 1):
    char = seq_y[col - 1]
    align_matrix_value = alignment_matrix[0][col - 1] + scoring_matrix[char]['-']
    if align_matrix_value < 0 and not global_flag:
      alignment_matrix[0][col] = 0
    else:
      alignment_matrix[0][col] = align_matrix_value

  for row in range(1, seq_x_length + 1):
    for col in range(1, seq_y_length + 1):
      char1 = seq_x[row - 1]
      char2 = seq_y[col - 1]
      align_matrix_value = max(scoring_matrix[char1][char2] + alignment_matrix[row - 1][col - 1], scoring_matrix['-'][char2] + alignment_matrix[row][col - 1], 
        scoring_matrix[char1]['-'] + alignment_matrix[row - 1][col])
      if align_matrix_value < 0 and not global_flag:
        alignment_matrix[row][col] = 0
      else:
        alignment_matrix[row][col] = align_matrix_value
  
  return alignment_matrix


#scoring_matrix = build_scoring_matrix(set(['G', 'C', 'A', 'T']), 20, 10, -5)
#print compute_alignment_matrix('AT', 'TG', scoring_matrix, False)