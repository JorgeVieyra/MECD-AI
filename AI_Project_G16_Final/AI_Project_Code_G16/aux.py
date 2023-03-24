# Determines if two positions are adjacent to each other
def isAdjacent(p1, p2):
        return ((p2[1] == p1[1]+1 and p2[0] == p1[0]) or
                (p2[1] == p1[1]-1 and p2[0] == p1[0]) or
                (p2[1] == p1[1] and p2[0] == p1[0]+1) or
                (p2[1] == p1[1] and p2[0] == p1[0]-1))

# Returns the closest position of each piece from one to the other
def findClosestPos(p1, p2):
    closest_p1, closest_p2 = None, None
    min_distance = float('inf')

    for pos1 in p1:
        for pos2 in p2:
            distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
            if distance < min_distance:
                closest_p1, closest_p2 = pos1, pos2
                min_distance = distance

    return [closest_p1, closest_p2]

# Determines the distance between a given piece to the other
def piece_distance(p1, p2):
    common_positions = set(p1) & set(p2)
    if len(common_positions) > 0:
        return len(p1) - len(common_positions)
    
    closest_positions = findClosestPos(p1, p2)
    return abs(closest_positions[0][0] - closest_positions[1][0]) + abs(closest_positions[0][1] - closest_positions[1][1]) + (len(p1) - len(common_positions))



def furthest_pos(p1, p2):
    closest_p1, closest_p2 = None, None
    min_distance = float('inf')

    # Find the closest positions between p1 and p2
    for pos1 in p1:
        for pos2 in p2:
            distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
            if distance < min_distance:
                closest_p1, closest_p2 = pos1, pos2
                min_distance = distance

    furthest_p2 = None
    max_distance = float('-inf')

    # Find the position in p2 that is furthest from the closest position of p1
    for pos2 in p2:
        distance = abs(pos2[0] - closest_p1[0]) + abs(pos2[1] - closest_p1[1])
        if distance > max_distance:
            furthest_p2 = pos2
            max_distance = distance

    return [closest_p1, furthest_p2]


# Checks whether a group of pieces all belong to the same piece or not
def same_piece(board, positions):
    for color in board.keys():
        if color in ['blank', 'size']:
            continue
        for piece in board[color].values():
            piece_positions = [p for p in piece]
            if set(positions).issubset(set(piece_positions)):
                return True
    return False

#Gets all the positions of pieces of the board with the given x
def get_positions_on_x(board, x):
    # Create an empty list to hold the positions
    positions = []
    
    # Iterate through each color on the board
    for color, pieces in board.items():
        # Skip the 'blank' and 'size' entries
        if color == 'blank' or color == 'size':
            continue
        
        # Iterate through each piece in the color
        for piece, coords in pieces.items():
            # Iterate through each coordinate in the piece
            for coord in coords:
                # Check if the x coordinate matches the input x
                if coord[0] == x:
                    positions.append(coord)
    
    # Return the list of positions with the same x coordinate
    return positions

#Gets all the positions of pieces of the board with the given y
def get_positions_on_y(board, y):
        all_positions = []
        for color, positions in board.items():
            if color not in ['blank', 'size']:
                for piece_positions in positions.values():
                    for pos in piece_positions:
                        if pos[1] == y:
                            all_positions.append(pos)
        return all_positions


# Given three lists of tuples (int, int), checks if the third list has any element in common with any of the two other lists.
# Returns True if it does, False otherwise.
def common(list1, list2, list3):
        
        for elem in list3:
            if elem in list1 or elem in list2:
                return True
        return False

# Returns the manhattan distance between two positions (x,y)
def manhattan_distance_pos(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Returns the manhattan distance between two pieces [(x,y)]
def manhattan_distance_piece(piece1, piece2):
    # Create a set of all positions in piece2
    piece2_positions = set(piece2)

    # Calculate the minimum Manhattan distance from any position in piece1 to any position in piece2
    min_distance = float('inf')
    for pos1 in piece1:
        for pos2 in piece2_positions:
            distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
            if distance < min_distance:
                min_distance = distance

    return min_distance




