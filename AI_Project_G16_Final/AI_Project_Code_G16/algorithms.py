import boards as b
import game_state as gs
from collections import deque
import resource
import time
import aux
import heapq

#BFS

#Breadth-First Search on the state tree
#returns a tuple as: (Final Board, Move count, Depth, Time taken (seconds), Memory use)
def bfs(initial_state):
    # initialize queue with initial state
    queue = deque([(initial_state, [initial_state])])
    
    # initialize set to keep track of visited states
    visited = [initial_state.board]
    
    # initialize time and memory usage
    start_time = time.time()
    max_memory_usage = 0
    
    # initialize node counter
    nodes_explored = 0
    
    while queue:
        # get next state and path from queue
        state, path = queue.popleft()
        
        # check if state is complete
        if state.isComplete():
            end_time = time.time()
            time_elapsed = end_time - start_time
            max_memory_usage = max(max_memory_usage, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1024
            return state.board, state.move_history, nodes_explored, time_elapsed, max_memory_usage
        
        # generate children and add to queue if not visited before
        for child in state.children():
            if child.checkAllPairs() and child.board not in visited:
                queue.append((child, path + [child]))
                nodes_explored += 1
                visited.append(child.board)
        # measure memory usage after each iteration
        max_memory_usage = max(max_memory_usage, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1024
    
    # if no complete state is found, return None
    end_time = time.time()
    time_elapsed = end_time - start_time
    return None, None, nodes_explored, time_elapsed, max_memory_usage




#--------------------------------------------------------------------------------------------------------

# LIMITED DFS / IDDFS

#Iterative Deepening Search on the state tree
#returns a tuple as: (Final Board, Number of nodes explored, Time taken (seconds), Memory use (KBs))
def ids(start_state, max_depth):
    # Initialize the search with a depth limit of 1.
    depth_limit = 1

    # Initialize counters for nodes explored, time spent, and memory used.
    nodes_explored = 0
    start_time = time.time()
    max_memory_usage = 0

    # Repeat the search with increasingly larger depth limits until a complete state is found.
    while True:
        # Call the recursive depth-limited search function.
        result, num_nodes, visited = depth_limited_search(start_state, depth_limit)

        # Update the nodes explored counter.
        nodes_explored += num_nodes

        # If the search found a complete state, return it along with the search information.
        if result is not None:
            end_time = time.time()
            max_memory_usage = max(max_memory_usage, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            search_time = end_time - start_time
            memory_used = max_memory_usage / 1024
            return result.board, result.move_history, nodes_explored, search_time, memory_used

        # If the search reached the maximum depth without finding a complete state, increase the depth limit.
        if depth_limit == max_depth:
            print("Reached max depth")
            end_time = time.time()
            max_memory_usage = max(max_memory_usage, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            search_time = end_time - start_time
            memory_used = max_memory_usage / 1024
            return None, None, nodes_explored, search_time, memory_used
        depth_limit += 1


#Auxiliary function to IDS
#Does a depth-first search on the state tree but only up to a certain depth_limit
def depth_limited_search(state, depth_limit):
    # Increment the nodes explored counter.
    num_nodes = 1

    # initialize set to keep track of visited states
    visited = [state.board]

    # If the state is complete, return it.
    if state.isComplete():
        return state, num_nodes, visited

    # If the depth limit has been reached, return None to signal that the search failed.
    if depth_limit == 0:
        return None, num_nodes, visited

    # Otherwise, recursively call the depth-limited search on each child state.
    for child in state.children():
        if child.checkAllPairs() and child.board not in visited:
            result, child_nodes, child_visited = depth_limited_search(child, depth_limit - 1)
            num_nodes += child_nodes
            visited += child_visited
            if result is not None:
                return result, num_nodes, visited

    # If none of the children resulted in a complete state, return None to signal that the search failed.
    return None, num_nodes, visited

#--------------------------------------------------------------------------------------------------------

# HEURISTICS

# Heuristic based the number of incorrect placed pieces
# An incorrect placed piece is one that either:
#    1) should have an empty list of positions but doesn't
#    2) doesn't have the right positions in its list
def h1(state, final_board):
    count = 0
    for color, pieces in state.board.items():
        if color == "blank" or color == "size":
            continue
        for piece_id, positions in pieces.items():
            final_positions = final_board[color][piece_id]
            if not final_positions:
                count += len(positions)
            elif not positions:
                count += len(final_positions)
            else:
                common_positions = set(positions).intersection(set(final_positions))
                count += abs(len(positions) - len(common_positions))
    return count

# Heuristic that determines the distance from a given board to the other
# Returns the final distance
def h2(state, final_board):
    total_distance = 0
    for color, pieces in state.board.items():
        if color in ['blank', 'size']:
            continue

        final_color = final_board[color]
        for piece in final_color.items():
            if piece[1]:
                final_positions = piece[1]

        for piece_num, positions in pieces.items():
            if not positions:
                continue

            total_distance += aux.piece_distance(positions,final_positions)
    return total_distance




#--------------------------------------------------------------------------------------------------------

# GREEDY SEARCH


# Greedy Search on the state tree
# This implementation of Greedy Search always chooses the node with the lowest cost
def greedy_search(init_state,final_board, heuristic):
    setattr(gs.CohesionState, "__lt__", lambda self, other: heuristic(self,final_board) < heuristic(other,final_board))
    states = [init_state]
    visited = set()
    explored_nodes = 0
    
    max_mem_used = 0
    start_time = time.time()

    while states:
        current = heapq.heappop(states)

        visited.add(current)
        explored_nodes += 1

        if current.isComplete():
            end_time = time.time()
            # found the best solution
            return current.move_history, end_time - start_time, max_mem_used, explored_nodes

        for child in current.children():
            if child not in visited:
                heapq.heappush(states, child)

        # Calculate memory usage at each iteration
        current_mem_used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if current_mem_used > max_mem_used:
            max_mem_used = current_mem_used

    return None


#--------------------------------------------------------------------------------------------------------

# A* SEARCH


# A* Search on the state tree
# this is very similar to greedy, the difference is that it takes into account the cost of the path so far
# Uses the greedy search implementation that always chooses the node with lowest heuristic score
def a_star_search(init_state, final_board, heuristic):
    
    return greedy_search(init_state, final_board, lambda state,final_board: heuristic(state,final_board) + len(state.move_history) - 1)

#--------------------------------------------------------------------------------------------------------

# WEIGHTED A* SEARCH


# Weighted A* Search on the state tree
# Similar to A* Search, but adds a weight factor to the heuristic
def weighted_a_star_search(init_state, final_board, heuristic, weight):

    return greedy_search(init_state, final_board, lambda state, final_board: heuristic(state, final_board) + weight * (len(state.move_history) - 1))

#--------------------------------------------------------------------------------------------------------
