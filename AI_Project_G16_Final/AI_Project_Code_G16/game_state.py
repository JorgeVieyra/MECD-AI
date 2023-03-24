from copy import deepcopy
import boards as b
import aux

# definition of the problem
class CohesionState:

    def __init__(self, board, move_history):
        self.board = deepcopy(board)
        # create an empty array and append move_history
        self.move_history = [] + move_history + [self.board]


    def children(self):
        # returns the possible moves
        functions = [self.up, self.down, self.left, self.right]

        children = []
        for color in set(self.board) - {"blank", "size"}:
            for pid in self.board[color]:
                for func in functions:
                    child = func(color, pid)
                    if child:
                        children.append(child)

        return children
    
    
    def update_board(self, color, id):
        # Get the list of points for the specified color and id
        points = self.board[color][id]

        # Check each point for adjacent points of the same color but different id
        for point in points:
            for other_id, other_points in self.board[color].items():
                if other_id != id:
                    for other_point in other_points:
                        if aux.isAdjacent(point, other_point):
                            # Remove the other point from its list and add it to the current id's list
                            self.board[color][other_id].remove(other_point)
                            self.board[color][id].append(other_point)
    

    # Checks the solvability of a board given 2 pieces of the same color
    # DOESN'T WORK 100%
    def checkInbetween(self, p1, p2):
        pieces = self.board
        pos1 = aux.findClosestPos(p1, p2)[0]
        pos2 = aux.findClosestPos(p1, p2)[1]

        # by default p1 is the bigger piece
        if len(p2) > len(p1):
            p1, p2 = p2, p1
                
        # choose the position from each piece that are the closest to each other and call them pos1 (for the position from p1) and pos2 (for the position from p2)
        # find the closest position in x axis
        if pos1[0] > pos2[0]:
            pos1, pos2 = pos2, pos1

        # check columns first (iterate through columns from the point that has the lowest value to the highest)
        res = True
        for col in range(pos1[0], pos2[0]+1):
            # get all positions in this column that are not part of p1 or p2
            blank_positions = [p for p in pieces['blank'] if p[0] == col]
            # if the number of blank positions is less than the size of p2, set has_enough_blank_positions to False
            wall = aux.get_positions_on_x(pieces,col)
            if len(wall) == pieces['size'][0] and aux.same_piece(pieces,wall):
                res = False
                return res
            if len(blank_positions) < len(p2) and not aux.common(p1,p2,wall) and not aux.same_piece(pieces,wall):
                res = False
        
        if pos1[1] > pos2[1]:
            pos1, pos2 = pos2, pos1
        # check rows second (iterate through rows from the point that has the highest value to the lowest)
        for row in range(pos1[1], pos2[1]+1):
            # get all positions in this row that are not part of p1 or p2
            blank_positions = [p for p in pieces['blank'] if p[1] == row]
            # if the number of blank positions is less than the size of p2, set has_enough_blank_positions to False
            wall = aux.get_positions_on_y(pieces,row)
            if len(wall) == pieces['size'][1] and aux.same_piece(pieces,wall) and not aux.same_piece(pieces,wall):
                res = False
                return res
            if (len(blank_positions) < len(p2) and not aux.common(p1,p2,wall)) and res == False:
                return res

        # Return the result based on whether or not there are enough blank positions
        if not res: res = True
        return res


    # Checks the solvability of the whole board by using the checkInbetween function for pairs of pieces
    # THIS ALSO DOESN'T WORK 100%
    def checkAllPairs(self):
        # Iterate over all colors
        for color in self.board.keys():
            # Skip non-piece keys
            if color in ["blank", "size"]:
                continue

            # Get the pieces of the current color
            pieces = self.board[color]

            # Get all pairs of pieces with non-empty position lists
            pairs = [(pieces[i], pieces[j]) for i in range(1, len(pieces)+1) for j in range(i+1, len(pieces)+1) if pieces[i] and pieces[j] and i < j]
                
            if len(pairs) > 0:
                # Check each pair using checkInbetween function
                for p in pairs:
                    if self.checkInbetween(p[0], p[1]) == False:
                        return False

        # All checks passed
        return True


    #Is called when one of the move functions is called, it defines if a move is possible or not
    #If it is, returns the updated state after the move is done
    def move(func):
            # decorator function to add to history everytime a move is made
            # functions with @move will apply this decorator
            def wrapper(self,color,id):
                state = CohesionState(self.board, self.move_history)
                value = func(state,color,id)
                if value:
                    return state
                else:
                    return None

            return wrapper

    @move
    def up(self, color, id):
        # Get the list of points for the specified color and id
        points = self.board[color][id]

        # Check if the piece can move up
        for point in points:
            # Check if the piece is already on the top row
            if point[1] == 0:
                return False

            # Check if there is a piece or invalid coordinate in the target position
            target_point = (point[0], point[1]-1)
            if target_point in self.board["blank"]:
                self.board["blank"].remove(target_point)
            elif target_point in points:
                continue
            else:
                return False

        # Move the piece up
        for i in range(len(points)):
            points[i] = (points[i][0], points[i][1]-1)

        # Add the previous position of the piece to the blank spaces list
        for point in points:
            if (point[0],point[1]+1) not in points:
                self.board["blank"].append((point[0], point[1]+1))
        
        # Update the board after moving the respective piece
        self.update_board(color, id)

        return True

    @move
    def down(self, color, id):
        # Get the list of points for the specified color and id
        points = self.board[color][id]

        # Check if the piece can move down
        for point in points:
            # Check if the piece is already on the bottom row
            if point[1] == self.board["size"][1]-1:
                return False

            # Check if there is a piece or invalid coordinate in the target position
            target_point = (point[0], point[1]+1)
            if target_point in self.board["blank"]:
                self.board["blank"].remove(target_point)
            elif target_point in points:
                continue
            else:
                return False

        # Move the piece down
        for i in range(len(points)):
            points[i] = (points[i][0], points[i][1]+1)

        # Add the previous position of the piece to the blank spaces list
        for point in points:
            if (point[0],point[1]-1) not in points:
                self.board["blank"].append((point[0], point[1]-1))
            
        # Update the board after moving the respective piece
        self.update_board(color, id)
        
        return True

    @move
    def left(self, color, id):
        # Get the list of points for the specified color and id
        points = self.board[color][id]

        # Check if the piece can move left
        for point in points:
            # Check if the piece is already on the leftmost column
            if point[0] == 0:
                return False

            # Check if there is a piece or invalid coordinate in the target position
            target_point = (point[0]-1, point[1])
            if target_point in self.board["blank"]:
                self.board["blank"].remove(target_point)
            elif target_point in points:
                continue
            else:
                return False

        # Move the piece left
        for i in range(len(points)):
            points[i] = (points[i][0]-1, points[i][1])

        # Add the previous position of the piece to the blank spaces list
        for point in points:
            if (point[0]+1,point[1]) not in points:
                self.board["blank"].append((point[0]+1, point[1]))
        
        # Update the board after moving the respective piece
        self.update_board(color, id)

        return True

    @move
    def right(self, color, id):
        # Get the list of points for the specified color and id
        points = self.board[color][id]

        # Check if the piece can move right
        for point in points:
            # Check if the piece is already on the rightmost column
            if point[0] == self.board["size"][0]-1:
                return False

            # Check if there is a piece or invalid coordinate in the target position
            target_point = (point[0]+1, point[1])
            if target_point in self.board["blank"]:
                self.board["blank"].remove(target_point)
            elif target_point in points:
                continue
            else:
                return False

        # Move the piece right
        for i in range(len(points)):
            points[i] = (points[i][0]+1, points[i][1])

        # Add the previous position of the piece to the blank spaces list
        for point in points:
            if (point[0]-1,point[1]) not in points:  
                self.board["blank"].append((point[0]-1, point[1]))
        
        # Update the board after moving the respective piece
        self.update_board(color, id)

        return True

    def isComplete(self):
        for color in self.board.keys():
            if color in ["blank", "size"]:
                continue
            non_empty_pieces = 0
            for id in self.board[color].keys():
                if len(self.board[color][id]) > 0:
                    non_empty_pieces += 1
            if non_empty_pieces != 1:
                return False
        return True

    def __hash__(self):
        # to be able to use the state in a set
        return hash(str(self.board))

    def __eq__(self, other):
        # compares the two matrices
        return str(self.board) == str(other.board)

def problems():
    return (
        CohesionState(b.b1,[]),
        CohesionState(b.b2,[]),
        CohesionState(b.b3,[]),
        CohesionState(b.b4,[]),
        CohesionState(b.b5,[]),
        CohesionState(b.b6,[]),
        CohesionState(b.b7,[])
    )


