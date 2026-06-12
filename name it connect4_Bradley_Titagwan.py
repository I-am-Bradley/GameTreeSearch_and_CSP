# Bradley Titagwan

import numpy as np
import time
import os

# ---- SHARED COFIGURATION ------
# We are setting the structure for the board by defining the number
# rows and columns. We defined who is the first and the second player.
# The timeout is used for the logic in the mcts algo.

ROWS = 6
COLS = 7
AGENT = 1
HUMAN = 2
EMPTY = 0
TIMEOUT = 1


# ---- SHARED BOARD LOGIC ----
# We used numpy here to create the structure of the board for the game.
def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

# This function is used to verify if the move proved by the agent or the
# human is valid. It checks each column to see if there is still room in
# that column for one more piece. Board[0][c] checks the top row and the
# every column to validate the move provided by the player.
def get_valid_moves(board):
    valid_cols = []
    # The loop goes through all the 7 columns to verify if the top row is
    # empty.
    for c in range(COLS):
        if board[0][c] == EMPTY:
            valid_cols.append(c)
    #This returns a list
    return valid_cols


# This function accepts the boards state, the column provided by the player
# and the player playing. With this information, we can know where the new
# piece is been placed on the board and what color the piece is based on
# the player.
def drop_piece(board, col, player):
    # The loop goes through all the rows, the loop stops before index 0 and 
    # the loop takes a backward steps meaning starting from the top coming 
    # down. This is because the pieces are being filled from top down and so
    # the bottom columns must be filled before the top.
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == EMPTY:
            # We are making each position with the player's ID depending on
            # which player's turn it is
            board[r][col] = player
            return True
    return False

# This function is used to check if a player has indeed won the game. It will
# check all possibilities of a win, whether horizontally, vertically or horizontally.
def check_win(board, p):
    # Horizontal verification. We will loop through all the rows and columns to 
    # verify if there are four consistent columns with the same player marking or id
    for r in range(ROWS):
        # Why we do columns minus three is because if we have four consistent markers,
        # we do not need to loop through all the columns
        for c in range(COLS-3):
            if (board[r][c] == p and 
                board[r][c+1] == p and 
                board[r][c+2] == p and 
                board[r][c+3] == p):
                    return True
    # Vertical verification. We will loop through all the rows and columns to 
    # verify if there are four consistent rows with the same player marking or id.
    # Using the same logic as it partains to columns, we do rows minus three is because
    # if we have four consistent markers, in a row we don't need to go through all rows.
    for r in range(ROWS-3):
        for c in range(COLS):
            if (board[r][c] == p and 
                board[r+1][c] == p and 
                board[r+2][c] == p and 
                board[r+3][c] == p):
                return True
    # Diagonals verification.
    # We will have 2 types of verification for the diagonal checking because we have the
    # increasing and decreasing slants.
    # The first loop checks the slant increasingly and we do rows and column minus 3
    # for the same logic as the horizontal and vertical checking.
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if (board[r][c] == p and 
                board[r+1][c+1] == p and 
                board[r+2][c+2] == p and 
                board[r+3][c+3] == p):
                return True
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if (board[r][c] == p and 
                board[r-1][c+1] == p and 
                board[r-2][c+2] == p and 
                board[r-3][c+3] == p):
                return True
    return False


# ------- ALPHA-BETA LOGIC -------
# This function is used for scoring, it takes the state of the game and counts how many
# dots belong to the agent and how many belong to the human and also which slots are empty.
# We then apply scores to different scenarios. We initialize the score as zero then go from
# there.
def evaluate_window(window, p):
    score = 0
    # We specify which player it is. 
    if p == AGENT:
        opp = HUMAN
    else:
        opp = AGENT
    
    # This condition is a winning state and so gets the highest score.
    if np.count_nonzero(window == p) == 4:
        score += 10000
    # This condition is closest to the winning position and so we give it the second highest
    # score. This incentivizes the agent to complete the line.
    elif np.count_nonzero(window == p) == 3 and np.count_nonzero(window == EMPTY) == 1:
        score += 1000
    # This condition is 2 agent pieces and 2 empty slots. This helps the agent keep the upper
    # hand by building potential future threats even when no immediate win is available.
    elif np.count_nonzero(window == p) == 2 and np.count_nonzero(window == EMPTY) == 2:
        score += 100
    # This condition is when there are 3 human pieces and one empty slot. This defense is needed
    # to help keep the agent aware of the fact that the human is in a possible winning situation
    # and needs to be neutralize by placing a piece there.
    if np.count_nonzero(window == opp) == 3 and np.count_nonzero(window == EMPTY) == 1:
        score -= 950
    return score

# This function is used by the ab agent to keep track of the entire scoreboard. While the
# evaluate window looks at a single 4-slot segment, the score position scans the entire
# board. Since it is a human versus an agent, then this function is for the agent.
# It scans all possible horizontal, vertical and diagonal lines of tour.
def score_position(board, p):
    score = 0
    # Center Column Bonus. We add a bonus to the center because any player who successfully
    # has the center part of the board can easily win the game.
    # We add 6 points for every agent piece at the center.
    center_array = board[:, COLS//2]
    score += np.count_nonzero(center_array == p) * 6
    
    # Horizontal scan. Uses the evaluate window function to scan all columns
    for r in range(ROWS):
        for c in range(COLS-3):
            score += evaluate_window(board[r, c:c+4], p)
    # Vertical scan. Uses the evaluate window function to scan all rows.
    for c in range(COLS):
        for r in range(ROWS-3):
            score += evaluate_window(board[r:r+4, c], p)
    # Diagonals scan. 
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = np.array([board[r+i, c+i] for i in range(4)])
            score += evaluate_window(window, p)
            window = np.array([board[r+3-i, c+i] for i in range(4)])
            score += evaluate_window(window, p)
    return score

# This function is used to record the depth the ab agent reaches everytime and log it unto a file
def log_depth_progression(move_num, final_depth, time_spent, log_path="ab_depth_timeline.csv"):
    """
    Logs the final depth reached for each move in a game session.
    """
    # We open the file with append since we are updating it everytime.
    with open(log_path, "a") as f:
        # if the file is empty, we will place the headings move number, final depth reached
        if f.tell() == 0:
            f.write("Move_Number,Final_Depth_Reached,Time_Spent_Seconds\n")
        f.write(f"{move_num},{final_depth},{time_spent:.4f}\n")

# This function alpha beta is the logic behind the alpha beta algorithm. It utilizes the minmax algo.
def alpha_beta(board, depth, alpha, beta, maximizing):
    # We start by getting all possible valid moves through the get_valid_moves function
    valid_moves = get_valid_moves(board)
    # We also get the terminal state by checking if either the agent or human have won or
    # we have no more valid moves.
    terminal = check_win(board, AGENT) or check_win(board, HUMAN) or len(valid_moves) == 0

    # We then check if a terminal state has been reached or the depth limit has been reached.
    # We do this by verifying if either the agent or the human have won.
    if depth == 0 or terminal:
        if terminal:
            if check_win(board, AGENT): 
                return (None, 1000000)
            if check_win(board, HUMAN): 
                return (None, -1000000)
            return (None, 0)
        return (None, score_position(board, AGENT))
    
    # This is the key part of the agent's algorithm. The goal is to simulate all possible
    # moves and choose the one results in the highest possible score.
    # At the beginning the agent starts by setting the best found value to negative infinity.
    # Makes the first valid move to become the best move. The agent iterates through every
    # available column, creates a copy of the current board and drop its piece there. We then
    # call this function again but set maximizing equal to false, which means it is the human's
    # turn.
    if maximizing:
        v, col = -np.inf, np.random.choice(valid_moves)
        for m in valid_moves:
            b_copy = board.copy()
            drop_piece(b_copy, m, AGENT)
            score = alpha_beta(b_copy, depth-1, alpha, beta, False)[1]
            # If the deeper search is higher than the current calue, the agent updates its target.
            if score > v: 
                v, col = score, m
            # The agent updates alpha which is the floor of the score. 
            alpha = max(alpha, v)
            # This line is the pruning. If the agent's guaranteed score becomes equal to or 
            # greater than what the Human is willing to allow so there is no point looking at
            # any other column.
            if alpha >= beta:
                break
        return col, v
    # This section is simulating the human's turn. We want the agent to be able to simulate the
    # human's play so it can play its best move even if the human plays theirs.
    else:
        v, col = np.inf, np.random.choice(valid_moves)
        for m in valid_moves:
            b_copy = board.copy()
            drop_piece(b_copy, m, HUMAN)
            score = alpha_beta(b_copy, depth-1, alpha, beta, True)[1]
            if score < v:
                v, col = score, m
            beta = min(beta, v)
            if alpha >= beta:
                break
        return col, v

# We want to be able to keep an account of what each of the mcts algorithm do at each round of play.
def record_ab_stats(move_num, depth, elapsed_time, score, log_path="ab_depth_timeline.csv"):
    """
    Overwrites the log file to show only the current move's depth progression.
    """
    # Use "a" if it's the first depth of the move, but we will handle the 
    # "erasing" logic in the agent before the loop starts.
    with open(log_path, "a") as f:
        # Format: Move (5 chars), Depth (10 chars), Time (15 chars), Score (10 chars)
        row = f"Move: {move_num:<5} | Depth: {depth:<8} | Time: {elapsed_time:<10.4f} | Score: {score:<8}\n"
        f.write(row)


# This function is the director of the entire Alpha beta pruning process. We will manage the 
# timer and coordinate how long the iterative deepening will occur. It will also help control
# how we long the various depths the algorithm reaches every time it does a move.
def alpha_beta_agent(board, log_path="ab_depth_timeline.txt"):
    # We get the start time, the fallback  move, current move number and final depth reached
    start = time.time()
    best_col = get_valid_moves(board)[0]
    current_move_num = np.count_nonzero(board) + 1
    final_reached_depth = 0

    #  We use iterative deepening where the loop runs still we reach the time limit.
    for d in range(1, 10):
        # Timer check
        if time.time() - start > TIMEOUT - 0.2:
            break
            
        # Run the search algo
        col, score = alpha_beta(board, d, -np.inf, np.inf, True)
            
        # If the search finished, update our best move and the depth counter
        if col is not None:
            best_col = col
            final_reached_depth = d
            
            # Log each depth as it completes (Internal Logging)
            elapsed = time.time() - start
            record_ab_stats(current_move_num, d, elapsed, score, log_path)

    # Final terminal print so you can see it while playing
    print(f" > Alpha-Beta: Reached Depth {final_reached_depth} in {time.time()-start:.2f}s")
    
    return best_col
 

# ------- MCTS LOGIC -------
# We use a class as a container for the building block of the search tree.
# We initiate the board state, parent state, specific move, total score from
# simulations, number of times this node has been simulated, list of 
# nodes representing future moves and moves not yet addedd to the tree.
class MCTSNode:
    def __init__(self, board, parent=None, move=None):
        self.board, self.parent, self.move = board, parent, move
        self.wins, self.visits, self.children = 0, 0, []
        self.untried_moves = get_valid_moves(board)

# This option "Option 1": Random Playout is the first reasoning logic for the mcts agent.
def random_playout(board, turn):
    curr_b, curr_p = board.copy(), turn
    # Make it an infinite loop
    while True:
        # We get the valid moves, use the length of valid moves to determine
        # a draw.
        moves = get_valid_moves(curr_b)
        if len(moves) == 0: return 0.5 # Draw
        
        # We choose a random move from the list of moves and pass it on.
        m = moves[np.random.randint(len(moves))]
        drop_piece(curr_b, m, curr_p)
        
        # After the move we check if the current player won. 
        if check_win(curr_b, curr_p):
            if curr_p == AGENT:
                return 1 
            else:
                return 0
            
        # We are identifying the opponent.
        if curr_p == AGENT:
            opp = HUMAN
        else:
            opp = AGENT

        
# This function "Smart Playout" is the second option for the reasoning logic for the mcts agent.
def smart_playout(board, turn):
    # we make a copy of the board and the turn.
    curr_b, curr_p = board.copy(), turn
    # The loop helps us to be able to go through and play the game from the 
    # current position all the way to the end.
    while True:
        moves = get_valid_moves(curr_b)
        # If there are no moves, then the board is full and so it is a draw.
        if len(moves) == 0:
            return 0.5
        # We are identifying the opponent.
        if curr_p == AGENT:
            opp = HUMAN
        else:
            opp = AGENT
        
        best_m = None

        # Proirity 1: We check if we can win now. The for loop goes through all
        # the moves in the list and checks if taking any of those moves gets the
        # agent to win. if the agent can win, the function breaks.
        for m in moves:
            b = curr_b.copy()
            drop_piece(b, m, curr_p)
            if check_win(b, curr_p):
                best_m = m 
                break
        # If there is no best move, the for loop will go through all the possible
        # moves and checks if taking that move gives the opponent and opportunity
        # to win 
        if best_m is None:
            for m in moves:
                b = curr_b.copy()
                drop_piece(b, m, opp)
                if check_win(b, opp): 
                    best_m = m
                    break
        # If there is no best move, then m becomes the best move, else we will choose
        # a random move from the list of moves
        if best_m is not None:
            m = best_m  
        else:
            # Randomly select from the list of valid moves.
            random_index = np.random.randint(len(moves))
            m = moves[random_index]
        
        # We will execute the move in the simulation
        drop_piece(curr_b, m, curr_p)
        # IF the game is over, we will check who won.
        if check_win(curr_b, curr_p): 
            if curr_p == AGENT:
                return 1 
            else:
                return 0
        # We switch turns and the simulation continues
        curr_p = opp

# We want to be able to keep an account of what each of the mcts algorithm do at each round of play.
def mcts_log_full_tree(node, file, indent=0):
    """
    Recursively walks through the MCTS tree and logs stats for every node.
    """
    prefix = "  " * indent
    # Format: [Move in Column X] Wins: W / Visits: V (WinRate%)
    move_info = f"Col {node.move}" if node.move is not None else "ROOT"
    win_rate = (node.wins / node.visits * 100) if node.visits > 0 else 0
    
    file.write(f"{prefix}{move_info} | Wins: {node.wins:.1f} | Visits: {node.visits} | {win_rate:.1f}%\n")
    # We log for every child of the node as well.
    # So the function is recursively called until no child is left in the list.
    for child in node.children:
        mcts_log_full_tree(child, file, indent + 1)


# This function is the director of the entire Monte Carlo process. We will manage the 
# timer and coordinate the four stages which are selection, expansion, simulation and
# back-propagation thousands of times to build a statistical map of the best move.
def mcts_agent(board, playout_mode="SMART", log_path=None):
    # We use the class to get the root node and also get the start time.
    root, start = MCTSNode(board), time.time()

    current_move_count = np.count_nonzero(board) + 1
    # ------- STAGE A: SELECTION -------
    # Since we do not want the human to wait for too long, we use a time limit for how
    # long the agent can "think". This can allow the loop to run 5,000 to 15,0000 or even
    # 20,000 times.
    while time.time() - start < TIMEOUT:
        # We start at the root and use the 
        node = root
        # The while loop means if the node has fully been expanded meaning no untried moves and
        # the node is not a terminal node, the agent has already mapped the section out
        # and will need to use the UCB1 formula to pick which child to visit next.
        while not node.untried_moves and node.children:
            # "c.wins/c.visits" is the exploitation part and "1.41 * np.sqrt(np.log(node.visits)/c.visits)" 
            # is the exploration part
            node = max(node.children, key=lambda c: (c.wins/c.visits) + 1.41 * np.sqrt(np.log(node.visits)/c.visits))
        # ------- STAGE B: EXPANSION ------
        # If the node has untried moves, the node is popped out of the list of untried moves,
        # a copy of the board is made, a piece is dropped and the children are attached
        # to the tree or in other words appended to the children's list of the node.
        if node.untried_moves:
            m = node.untried_moves.pop(np.random.randint(len(node.untried_moves)))
            b = node.board.copy()
            drop_piece(b, m, AGENT)
            child = MCTSNode(b, parent=node, move=m)
            node.children.append(child)
            node = child
        # ------- STAGE C: SIMULATION (PLAYOUT) -------
        #  We call either the random playout function or the smart_playout function to run the simulation.
        if playout_mode == "SMART":
            result = smart_playout(node.board, HUMAN)
        else:
            result = random_playout(node.board, HUMAN)
        # ------- STAGE D: BACK-PROPAGATION -------
        # The result of the game is sent back up to update the entire tree for learning purposes
        while node:
            node.visits += 1
            node.wins += result
            node = node.parent

    # --- LOGGING TO THE SPECIFIC GAME FILE---
    if log_path:
        with open(log_path, "a") as f: # Append mode
            f.write(f"\n{'='*40}\n")
            f.write(f"MOVE {current_move_count} | Playout: {playout_mode} | Sims: {root.visits}\n")
            f.write(f"{'='*40}\n")
            mcts_log_full_tree(root, f)
    
    print(f" > {playout_mode} log saved to: {log_path}")

    # We want to print the log file to the terminal
    if current_move_count == 30 and log_path:
        print(f"\n[!] REACHED MOVE 30: DISPLAYING LOG FOR {playout_mode}")
        print("-" * 50)
        try:
            with open(log_path, "r") as f:
                # Dumps the entire file content to the screen
                print(f.read())
        except:
            print("Log file not found yet.")
        print("-" * 50)
        input("Press Enter to continue playing...")
   
    # Once the timer runs out, the agent stops simulating and picks the node with the most visits.
    # Why the most visit is because it survived the UCB1 formula's scrutiny over thousands of iterations.
    return max(root.children, key=lambda c: c.visits).move


# --- GAME ENGINE ---
def play_game(mode):
    # We create the board
    board = create_board()
    print(f"\n--- STARTING GAME: {mode} ---")

    game_log_path = None

    # Define paths for the three algorithms
    if mode == "MCTS-SMART":
        game_log_path = "mcts_smart_log.txt"
    elif mode == "MCTS-RANDOM":
        game_log_path = "mcts_random_log.txt"
    elif mode == "ALPHA-BETA":
        with open("ab_depth_timeline.txt", "w") as f:
            f.write(f"{'='*60}\n")
            f.write(f" ALPHA-BETA SEARCH LOG \n")
            f.write(f"{'='*60}\n")
            # Column Labels
            f.write(f"{'Move':<11} | {'Depth':<8} | {'Time Taken':<12}(s) | {'Score':<8}\n")
            f.write(f"{'='*60}\n")

    # CLEAR THE FILE: Opening in "w" mode wipes previous contents
    if game_log_path:
        with open(game_log_path, "w") as f:
            f.write(f"--- STARTING NEW {mode} SESSION ---\n")


    print(f"\n--- STARTING GAME: {mode} ---")

    # We make the game run in an infinite loop and only stop if the code hits a break.
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"MODE: {mode}\n", board)
        # We accept the human input and validate it, that is why we use the try/except block.
        try:
            c = int(input("Enter between 0-6 for the column: "))
            if not drop_piece(board, c, HUMAN):
                 continue
        except ValueError:
            continue
        # After each users play, we check if any user has won or if there are no valid moves
        # left because that is what the whole game is about.
        if check_win(board, HUMAN): 
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"------- TERMINAL STATE: {mode} -------")
            print(board)
            print("\nRESULT: HUMAN PLAYER (2) WINS!")
            break

        if not get_valid_moves(board):
            print(f"------- TERMINAL STATE: {mode} -------")
            print(board, "\nRESULT: DRAW!")
            break

        # We are now going to the agents processing.
        print("Agent is thinking...")

        # If we are running the ab testing then we will call the Alpha-beta mode.
        if mode == "ALPHA-BETA":
            # Call the new agent function
            best_col = alpha_beta_agent(board)
        # If we are running the mcts algo, then we will run the mcts agent using either the 
        # smart or the random algo.
        elif mode == "MCTS-SMART":
            best_col = mcts_agent(board, playout_mode="SMART", log_path=game_log_path)
        elif mode == "MCTS-RANDOM":
            best_col = mcts_agent(board, playout_mode="RANDOM", log_path=game_log_path)
        
        # We accepted the agents best move and then check if the agent wins. If the agent 
        # wins the code breaks if not the loop continues.
        drop_piece(board, best_col, AGENT)
        if check_win(board, AGENT):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"------- TERMINAL STATE: {mode} -------")
            print(board)
            print("\nRESULT: AGENT PLAYER (1) WINS!")
            break

if __name__ == "__main__":
    # Part 1: Alpha-Beta
    ##input("\nAlpha-Beta is finished. Press Enter to start MCTS-SMART...")
    
    # Part 2: MCTS with Random Playouts (Option 1)
    ##play_game("MCTS-RANDOM")
    #input("\nMCTS-RANDOM is finished. Press Enter to start MCTS-RANDOM...")
    
    # Part 3: MCTS with Smart Playouts (Option 2)
    play_game("MCTS-SMART")
    