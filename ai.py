#!/usr/bin/python3
# -*- coding:utf-8 -*-

from utils import create_map 
import numpy as np
import random
import tensorflow as tf

def play_minesweeper_game_as_ai():
    """
    Play Minesweeper game as AI
    """
    # Create the smallest map
    map_info = create_map(1)
    row_size = map_info['row_size']
    column_size = map_info['column_size']
    matrix = map_info['matrix'].split(',')

    # Initialize variables
    unrevealed_cell_indices = set(range(0, row_size * column_size))
    revealed_cell_indices = set()
    empty_cell_indices = set()
    picked_cell_index = -1

    # Get empty cell indices
    for matrix_index, matrix_value in enumerate(matrix):
        if matrix_value.startswith('0-'):
            empty_cell_indices.add(matrix_index)

    # Sweep empty cell for the first time
    if len(empty_cell_indices) > 0:
        picked_cell_index = random.choice(list(empty_cell_indices))
    else:
        picked_cell_index = random.choice(list(unrevealed_cell_indices))
    revealed_cell_indices = update_revealed_cell_indices(matrix, revealed_cell_indices, picked_cell_index)
    last_clicked_cell_row, last_clicked_cell_column = divmod(picked_cell_index, column_size)

    # Play until every cell has revealed
    while True:
        
        if len(revealed_cell_indices) == row_size * column_size:
            break
        
        # Find sweepable or flaggable cells
        indices = find_sweepable_or_flaggable_cells(matrix, row_size, column_size, 
                revealed_cell_indices, last_clicked_cell_row, last_clicked_cell_column)
    	
        # Pick random one if it is impossible to find index with given condition
        if indices == []:
            collect_data(matrix, revealed_cell_indices, row_size, column_size)
            unrevealed_cell_indices = set(range(0, row_size * column_size)) - revealed_cell_indices
            picked_cell_index = random.choice(list(unrevealed_cell_indices))
            revealed_cell_indices = update_revealed_cell_indices(matrix, revealed_cell_indices, picked_cell_index)
            last_clicked_cell_row, last_clicked_cell_column = divmod(picked_cell_index, column_size)
        
        # Sweep or flag cells with given condition
        else:
            for picked_cell_index in indices:
                revealed_cell_indices = update_revealed_cell_indices(matrix, revealed_cell_indices, picked_cell_index)
                last_clicked_cell_row, last_clicked_cell_column = divmod(picked_cell_index, column_size)
    
    return None

def update_revealed_cell_indices(matrix, revealed_cell_indices, picked_cell_index):
    """
    Update revealed cell indices
    """
    cell_value = matrix[picked_cell_index]

    if cell_value.startswith('0-'):
        # Filter by tag value
        cell_tag = cell_value.split('-')[1]
        currently_revealed_cell_indices = set(i for i, x in enumerate(matrix) if '-' in x and x.split('-')[1] == cell_tag)
        revealed_cell_indices |= currently_revealed_cell_indices
    else:
        revealed_cell_indices.add(picked_cell_index)

    return revealed_cell_indices

def find_sweepable_or_flaggable_cells(matrix, row_size, column_size, 
        revealed_cell_indices, last_clicked_cell_row, last_clicked_cell_column):
    """
    Find sweepable or flaggable cells
    Returns indices
    """
    max_distance = max(last_clicked_cell_row, last_clicked_cell_column, 
            row_size - last_clicked_cell_row, column_size - last_clicked_cell_column)

    # Search from last clicked cell with spiral shape
    for distance in range(0, max_distance + 1):
        
        # Top corner
        if last_clicked_cell_row - distance >= 0:
            
            left_top_cell_column = max(last_clicked_cell_column - distance, 0)
            right_top_cell_column = min(last_clicked_cell_column + distance, column_size - 1)
            
            for column in range(left_top_cell_column, right_top_cell_column + 1):
                indices = check_adjacent_cells(matrix, row_size, column_size, 
                        last_clicked_cell_row - distance, column, revealed_cell_indices)
                
                if indices != []:
                    return indices
        
        # Right corner
        if last_clicked_cell_column + distance <= column_size - 1:
            
            right_top_cell_row = max(last_clicked_cell_row - distance, 0)
            right_bottom_cell_row = min(last_clicked_cell_row + distance, row_size - 1)
            
            row_range = None
            if last_clicked_cell_row - distance >= 0:
                row_range = range(right_top_cell_row + 1, right_bottom_cell_row + 1)
            else:
                row_range = range(right_top_cell_row, right_bottom_cell_row + 1)
            
            for row in row_range:
                indices = check_adjacent_cells(matrix, row_size, column_size, 
                        row, last_clicked_cell_column + distance, revealed_cell_indices)
                
                if indices != []:
                    return indices
        
        # Bottom corner
        if last_clicked_cell_row + distance <= row_size - 1:
            
            right_bottom_cell_column = min(last_clicked_cell_column + distance, column_size - 1)
            left_bottom_cell_column = max(last_clicked_cell_column - distance, 0)
            
            column_range = None
            if last_clicked_cell_column + distance <= column_size - 1:
                column_range = range(left_bottom_cell_column, right_bottom_cell_column)
            else:
                column_range = range(left_bottom_cell_column, right_bottom_cell_column + 1)
            
            for column in list(reversed(column_range)):
                indices = check_adjacent_cells(matrix, row_size, column_size, 
                        last_clicked_cell_row + distance, column, revealed_cell_indices)
                
                if indices != []:
                    return indices
        
        # Left corner
        if last_clicked_cell_column - distance >= 0:
            
            left_bottom_cell_row = min(last_clicked_cell_row + distance, row_size - 1)
            left_top_cell_row = max(last_clicked_cell_row - distance, 0)
            
            row_range = None
            if last_clicked_cell_row + distance <= row_size - 1:
                if last_clicked_cell_row - distance >= 0:
                    row_range = range(left_top_cell_row + 1, left_bottom_cell_row)
                else:
                    row_range = range(left_top_cell_row, left_bottom_cell_row)
            else:
                if last_clicked_cell_row - distance >= 0:
                    row_range = range(left_top_cell_row + 1, left_bottom_cell_row + 1)
                else:
                    row_range = range(left_top_cell_row, left_bottom_cell_row + 1)
            
            for row in list(reversed(row_range)):
                indices = check_adjacent_cells(matrix, row_size, column_size, 
                        row, last_clicked_cell_column - distance, revealed_cell_indices)
                
                if indices != []:
                    return indices
    
    return []

def check_adjacent_cells(matrix, row_size, column_size, row, column, revealed_cell_indices):
    """
    Check adjacent cells with according to its row and colume values
    Returns sweepable or flaggable indices
    """
    center_cell_index = row * column_size + column
    center_cell_value = matrix[center_cell_index]
    
    # Check only if center cell is revealed cell and its content is positive number
    if center_cell_index in revealed_cell_indices and \
            center_cell_value != 'M' and center_cell_value.startswith('0-') == False:
        
        if '-' in center_cell_value:
            center_cell_value = int(center_cell_value.split('-')[0])
        else:
            center_cell_value = int(center_cell_value)
        
        partial_matrix = []
        row_range = range(max(row - 1, 0), min(row + 1, row_size - 1) + 1)
        column_range = range(max(column - 1, 0), min(column + 1, column_size - 1) + 1)
        
        for adjacent_row in row_range:
            for adjacent_column in column_range:
                
                cell_index = adjacent_row * column_size + adjacent_column
                cell_value = matrix[cell_index]
                
                if cell_index in revealed_cell_indices:
                    partial_matrix.append(cell_value)
                else:
                    partial_matrix.append('')
        
        # Check unrevealed cells in partial matrix are sweepable or flaggable
        action = get_action_to_unrevealed_cells(partial_matrix, center_cell_value)
        
        if action in ['flag', 'sweep']:
            return get_indices_of_unrevealed_cells(partial_matrix, row_range, column_range, column_size)
        else:
            return []

    return []

def get_action_to_unrevealed_cells(partial_matrix, center_cell_value):
    """
    Get action to unrevealed cells
        return value could be 'flag', 'sweep' or ''(= do nothing)
    For example,
        partial_matrix = ['1', '2', 'M',
                          '',  '3', '1',
                          '',  '3', '1-1']
        center_cell_value = 3
    Returns,
        'flag'
    """
    # Initialize variables
    number_of_unrevealed_cells = 0
    number_of_mines = 0

    for cell_value in partial_matrix:
        
        if cell_value == '':
            number_of_unrevealed_cells += 1
        elif cell_value == 'M':
            number_of_mines += 1

    if number_of_unrevealed_cells == 0:
        return ''
    elif number_of_mines == center_cell_value and number_of_unrevealed_cells > 0:
        return 'sweep'
    elif number_of_mines + number_of_unrevealed_cells == center_cell_value:
        return 'flag'
    else:
        return ''

def get_indices_of_unrevealed_cells(partial_matrix, row_range, column_range, column_size):
    """
    Get indices of unrevealed cells
    For example,
        partial_matrix = ['1', '2', 'M',
                          '',  '3', '1',
                          '',  '3', '1-1']
        row_range = range(3, 6)
        column_range = range(0, 3)
        column_size = 10
    Returns,
        [40, 50]
    Note that 'index = row * column_size + column'
    """
    # Initialize variables
    indices = []

    for temp_index, cell_value in enumerate(partial_matrix):
        
        if cell_value == '':
            row = min(row_range) + int(temp_index / len(column_range))
            column = min(column_range) + (temp_index % len(column_range))
            indices.append(row * column_size + column)
    
    return indices

def collect_data(matrix, revealed_cell_indices, row_size, column_size):
    """
    Collect data for machine learning
    """
    unrevealed_cell_indices = set(range(0, row_size * column_size)) - revealed_cell_indices

    for unrevealed_cell_index in unrevealed_cell_indices:
        
        statistics = get_statistics_from_around_cells(matrix, row_size, column_size,
                unrevealed_cell_index, revealed_cell_indices)
        
        # Find unrevealed cells which has at least one revealed number cell around
        if statistics['number_of_revealed_cells_around'] > 0 and \
                statistics['number_of_revealed_cells_around'] - statistics['number_of_revealed_mines_around'] > 0:
            
            sum_of_probabilities = 0
            
            row, column = divmod(unrevealed_cell_index, column_size)
            row_range = range(max(row - 1, 0), min(row + 1, row_size - 1) + 1)
            column_range = range(max(column - 1, 0), min(column + 1, column_size - 1) + 1)
            
            for adjacent_row in row_range:
                for adjacent_column in column_range:
                    
                    adjacent_cell_index = adjacent_row * column_size + adjacent_column
                    adjacent_cell_value = matrix[adjacent_cell_index]
                    if '-' in adjacent_cell_value:
                        adjacent_cell_value = int(adjacent_cell_value.split('-')[0])
                    elif adjacent_cell_value != 'M':
                        adjacent_cell_value = int(adjacent_cell_value)
                    
                    # Calulate sum of probabilities for revealed cells around
                    if adjacent_cell_index != unrevealed_cell_index and \
                            adjacent_cell_index in revealed_cell_indices and \
                            adjacent_cell_value != 'M' and adjacent_cell_value > 0:
                        
                        temp_statistics = get_statistics_from_around_cells(matrix, 
                                row_size, column_size, adjacent_cell_index, revealed_cell_indices)
                        sum_of_probabilities += (adjacent_cell_value - temp_statistics['number_of_revealed_mines_around']) \
                                / temp_statistics['number_of_unrevealed_cells_around']
            
            # X data
            # FIXME Filter X data to minimize cost
            x_data = str(sum_of_probabilities) + ' ' + \
                    str(statistics['number_of_revealed_mines_around']) + ' ' + \
                    str(statistics['number_of_revealed_cells_around']) + ' ' + \
                    str(statistics['number_of_unrevealed_cells_around']) 
            
            # Y data
            if matrix[unrevealed_cell_index] == 'M':
                y_data = 1
            else:
                y_data = 0
            
            # Record X, Y data
            training_data.write(str(x_data) + ' ' + str(y_data) + '\n')

    return None

def get_statistics_from_around_cells(matrix, row_size, column_size, cell_index, revealed_cell_indices):
    """
    Get statistics from around cells
    """
    # Initialize variables
    number_of_revealed_cells_around = 0
    number_of_revealed_mines_around = 0
    number_of_unrevealed_cells_around = 0
    
    row, column = divmod(cell_index, column_size)
    row_range = range(max(row - 1, 0), min(row + 1, row_size - 1) + 1)
    column_range = range(max(column - 1, 0), min(column + 1, column_size - 1) + 1)
    
    for adjacent_row in row_range:
        for adjacent_column in column_range:
            
            adjacent_cell_index = adjacent_row * column_size + adjacent_column
            adjacent_cell_value = matrix[adjacent_cell_index]
            if '-' in adjacent_cell_value:
                adjacent_cell_value = int(adjacent_cell_value.split('-')[0])
            elif adjacent_cell_value != 'M':
                adjacent_cell_value = int(adjacent_cell_value)
            
            # Except for the center cell
            if adjacent_cell_index != cell_index:
                
                if adjacent_cell_index in revealed_cell_indices:
                    number_of_revealed_cells_around += 1
                    
                    if adjacent_cell_value == 'M':
                        number_of_revealed_mines_around += 1
                else:
                    number_of_unrevealed_cells_around += 1

    return {'number_of_revealed_cells_around': number_of_revealed_cells_around,
            'number_of_revealed_mines_around': number_of_revealed_mines_around,
            'number_of_unrevealed_cells_around': number_of_unrevealed_cells_around}

if __name__ == '__main__':
    """
    Play Minesweeper game as AI for a given time
    """
    global training_data

    training_data = open('./train.txt', 'w')

    # Get training data set
    for count in range(0, 100):
        play_minesweeper_game_as_ai()
    
    training_data.close()

    # Read X, Y data using numpy
    xy = np.loadtxt('./train.txt', unpack=True, dtype='float32')
    x_data = xy[0:-1]
    y_data = xy[-1]

    # Logistic classification using TensorFlow
    X = tf.placeholder(tf.float32)
    Y = tf.placeholder(tf.float32)

    W = tf.Variable(tf.random_uniform([1, len(x_data)], -1.0, 1.0))

    # Hypothesis
    h = tf.matmul(W, X)
    hypothesis = tf.div(1.0, 1.0 + tf.exp(-h))

    # Cost function
    cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1 - Y) * tf.log(1 - hypothesis))

    # Learning rate
    a = tf.Variable(0.1)

    # Minimize cost by gradient descent algorithm
    optimizer = tf.train.GradientDescentOptimizer(a)
    train = optimizer.minimize(cost)

    # Data initialization
    init = tf.global_variables_initializer()
    
    # Launch the graph
    sess = tf.Session()
    sess.run(init)

    # Fit the line
    for step in range(0, 2001):
        sess.run(train, feed_dict={X: x_data, Y: y_data})
        if step % 20 == 0:
            print(step, sess.run(cost, feed_dict={X: x_data, Y: y_data}), sess.run(W))

    # TODO Test sets
