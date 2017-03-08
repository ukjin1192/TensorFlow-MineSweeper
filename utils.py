#!usr/bin/python3
# -*- coding:utf-8 -*-

import math
import random

def create_map(maximum_users):
    """
    create map according to maximum users
    Here is sample output
    {
        'maximum_users': 1, 
        'total_mines': 20, 
        'row_size': 10, 
        'column_size': 10, 
        'matrix': 
            '1,M,M,1-0,0-0,0-0,0-0,0-0,1-0,1,
             1-1,2-1,3-1,2-0,2-0,2-0,3-0,3-0,3-0,M,
             0-1,0-1,1-1,M,2,M,M,M,M,2,
             0-1,1-1,3-1,3,4,4,5,4,2,1,
             0-1,2-1,M,M,3,M,M,1,1,1,
             0-1,2-1,M,M,3-1,2-1,2-1,1-1,1,M,
             0-1,1-1,2-1,2-1,1-1,0-1,0-1,1-1,2,2,
             0-1,0-1,0-1,0-1,0-1,0-1,0-1,2-1,M,3,
             0-1,0-1,0-1,1-1,1-1,1-1,0-1,2-1,M,M,
             0-1,0-1,0-1,1-1,M,1-1,0-1,1-1,3,M'
    }
    """
    if isinstance(maximum_users, int) == False or maximum_users < 1:
        raise ValueError('Input must be the positive integer.')

    # Estimated size
    total_cells = maximum_users * 100
    length_difference = int(math.sqrt(total_cells) * 0.2) 

    row_size = int(math.sqrt(total_cells)) + random.randint(-1 * length_difference, length_difference)
    column_size = int(total_cells / row_size)

    # Exact size
    total_cells = row_size * column_size
    total_mines = int(total_cells * 0.2)
    position_of_mines = random.sample(range(total_cells), total_mines)

    matrix = []

    # Set mines at proper position
    for row in range(row_size):
        for column in range(column_size):
            
            if row * column_size + column in position_of_mines:
                matrix.append({'row': row, 'column': column, 'value': 'M'});
            else: 
                matrix.append({'row': row, 'column': column, 'value': '0'});

    # Caculate value for each cell
    for row in range(row_size):
        for column in range(column_size):
            
            if matrix[row * column_size + column]['value'] != 'M':
                number_of_adjacent_mines = 0
                
                for adjacent_row in range(max(row - 1, 0), min(row + 1, row_size - 1) + 1):
                    for adjacent_column in range(max(column - 1, 0), min(column + 1, column_size - 1) + 1):
                        
                        if matrix[adjacent_row * column_size + adjacent_column]['value'] == 'M':
                            number_of_adjacent_mines += 1
                
                matrix[row * column_size + column]['value'] = str(number_of_adjacent_mines)

    # Set block tag for empty cell
    block_tag = 0

    for row in range(row_size):
        for column in range(column_size):
            
            if matrix[row * column_size + column]['value'] == '0':
                
                adjacent_tags = set()
                
                # Check left-top cell
                if row >= 1 and column >= 1 and matrix[(row - 1) * column_size + column - 1]['value'].startswith('0-'):
                    adjacent_tags.add(matrix[(row - 1) * column_size + column - 1]['value'])
                # Check top cell
                if row >= 1 and matrix[(row - 1) * column_size + column]['value'].startswith('0-'):
                    adjacent_tags.add(matrix[(row - 1) * column_size + column]['value'])
                # Check right-top cell
                if row >= 1 and column <= column_size - 2 and matrix[(row - 1) * column_size + column + 1]['value'].startswith('0-'):
                    adjacent_tags.add(matrix[(row - 1) * column_size + column + 1]['value'])
                # Check left cell
                if column >= 1 and matrix[row * column_size + column - 1]['value'].startswith('0-'):
                    adjacent_tags.add(matrix[row * column_size + column - 1]['value'])
                # Check right cell
                if column <= column_size - 2 and matrix[row * column_size + column + 1]['value'].startswith('0-'):
                    adjacent_tags.add(matrix[row * column_size + column + 1]['value'])
                # Check left-bottom cell
                if row <= row_size - 2 and column >= 1 and matrix[(row + 1) * column_size + column - 1]['value'].startswith('0-'):
                    adjacent_tags.add(matrix[(row + 1) * column_size + column - 1]['value'])
                # Check bottom cell
                if row <= row_size - 2 and matrix[(row + 1) * column_size + column]['value'].startswith('0-'):
                    adjacent_tags.add(matrix[(row + 1) * column_size + column]['value'])
                # Check right-bottom cell
                if row <= row_size - 2 and column <= column_size - 2 and matrix[(row + 1) * column_size + column + 1]['value'].startswith('0-'):
                    adjacent_tags.add(matrix[(row + 1) * column_size + column + 1]['value'])
                
                # Set new block tag
                if len(adjacent_tags) == 0:
                    matrix[row * column_size + column]['value'] = '0-' + str(block_tag)
                    block_tag += 1
                # Set existing block tag
                elif len(adjacent_tags) == 1:
                    matrix[row * column_size + column]['value'] = adjacent_tags.pop()
                # Unify linked block tags
                else:
                    standard_tag = adjacent_tags.pop()
                    matrix[row * column_size + column]['value'] = standard_tag
                    
                    for adjacent_tag in adjacent_tags:
                        for temp_row in range(row_size):
                            for temp_column in range(column_size):
                                
                                if matrix[temp_row * column_size + temp_column]['value'] == adjacent_tag:
                                    matrix[temp_row * column_size + temp_column]['value'] = standard_tag

    # Set block tag for cells beside empty cell
    for row in range(row_size):
        for column in range(column_size):
            
            if matrix[row * column_size + column]['value'].startswith('0-') == False:
                block_tags = []
                
                for adjacent_row in range(max(row - 1, 0), min(row + 1, row_size - 1) + 1):
                    for adjacent_column in range(max(column - 1, 0), min(column + 1, column_size - 1) + 1):
                        
                        if matrix[adjacent_row * column_size + adjacent_column]['value'].startswith('0-') and \
                            matrix[adjacent_row * column_size + adjacent_column]['value'].split('0-')[1] not in block_tags:
                            
                            block_tags.append(matrix[adjacent_row * column_size + adjacent_column]['value'].split('0-')[1])
                
                if len(block_tags) > 0:
                    matrix[row * column_size + column]['value'] += '-' + '-'.join(block_tags)
    
    # Matrix with string format
    matrix_with_string_format = []
    for cell in matrix:
        matrix_with_string_format.append(cell['value'])
    matrix_with_string_format = ','.join(matrix_with_string_format)

    return {'row_size': row_size, 
            'column_size': column_size,
            'total_mines': total_mines, 
            'matrix': matrix_with_string_format,
            'maximum_users': maximum_users}
