# Bradley Titagwan
import numpy as np
import time
import os
import json
import matplotlib.pyplot as plt

"""
We are using a class so as to place the collection of the functions into a structured object.
We are also using a class because we need to keep track of several things simultaneously like
the board state, block size and metrics like the back track count.
"""

class SudokuSolver:
    def __init__(self, board_list):
        """
        Initialize the solver with the puzzle board.
        n: Total size (e.g., 9 for a 9x9 board)
        m: Block size (e.g., 3 for a 9x9 board)
        """
        self.n = len(board_list)
        self.m = int(self.n**0.5)
        self.initial_board = np.array(board_list)
        self.reset()

    def reset(self):
        """Resets the board and performance counters for a fresh comparison run."""
        self.board = self.initial_board.copy()
        self.backtracks = 0

    def get_neighbors(self, r, c):
        """
        Returns a set of coordinates for all cells in the same row, column, 
        and mxm block as the cell at (r, c).
        """
        neighbors = set()
        # Expand row neighbors: Scan every cell in the current row
        for i in range(self.n):
            neighbors.add((r, i))
        # Expand column neighbors: Scan every cell in the current column
        for i in range(self.n):
            neighbors.add((i, c))
        # Expand block neighbors: Find the top-left corner of the sub-grid
        # The (r // self.m) * self.m and the (c // self.m) * self.m are used to get 
        # mini blocks. It means we get the reminder of the rows divided by the block 
        # size and then multipy the answer by the block size and same for the columns
        sr, sc = (r // self.m) * self.m, (c // self.m) * self.m
        # We will loop through the rows in the block
        for i in range(sr, sr + self.m):
            # We will loop through the columns in the block
            for j in range(sc, sc + self.m):
                neighbors.add((i, j))
        # Remove the cell itself from the neighbor set
        neighbors.remove((r, c))
        return neighbors

    def is_valid(self, r, c, value):
        """
        Checks if 'value' can be placed at (r, c) without violating 
        Sudoku rules (Row, Column, and Block constraints).
        If the value is found in the row or column or even in the block
        of r, c then we know the move is not valid and so we return false.
        """
        # Row Check: Check if value exists in the current row
        for i in range(self.n):
            if self.board[r][i] == value:
                return False
        # Column Check: Check if value exists in the current column
        for i in range(self.n):
            if self.board[i][c] == value:
                return False
        # Block Check: Check if value exists in the specific mxm square
        sr, sc = (r // self.m) * self.m, (c // self.m) * self.m
        for i in range(sr, sr + self.m):
            for j in range(sc, sc + self.m):
                if self.board[i][j] == value:
                    return False
        return True

    def get_mrv_cell(self):
        """
        VARIABLE SELECTION: Minimum Remaining Values (MRV).
        Finds the empty square with the fewest legal numbers left.
        This helps fail early by tackling the most constrained cells first.
        """
        best_cell = None
        min_remaining = float('inf')  
        
        # Iterate through every cell on the board
        for r in range(self.n):
            for c in range(self.n):
                # If the cell is empty (0), we initiate the count = 0
                if self.board[r][c] == 0:
                    count = 0
                    # Check how many numbers are actually legal for this spot.
                    # For every number we increment the count by one.
                    for val in range(1, self.n + 1):
                        if self.is_valid(r, c, val):
                            count += 1
                    
                    # Track the cell with the smallest number of choices and make
                    # it the best cell. 
                    if count < min_remaining:
                        min_remaining = count
                        best_cell = (r, c)
        return best_cell

    def get_lcv_values(self, r, c):
        """
        VALUE SELECTION: Least Constraining Value (LCV).
        Returns a list of legal values for cell (r, c) sorted by how few 
        restrictions they place on neighboring empty cells.
        """
        # We initialize the valid values list, run a for loop to go through
        # all the values in range to see if they are valid.
        valid_values = []
        for v in range(1, self.n + 1):
            if self.is_valid(r, c, v):
                valid_values.append(v)
        
        # For each valid value, calculate its 'constraint score'
        value_constraints = []
        for val in valid_values:
            constraints = 0
            # Check every neighbor of the current cell
            for nr, nc in self.get_neighbors(r, c):
                # If the neighbor is empty, see if placing 'value' blocks a move there
                if self.board[nr][nc] == 0:
                    if not self.is_valid(nr, nc, val):
                        constraints += 1
            value_constraints.append((constraints, val))
        
        # Sort based on the lowest constraints (ascending order)
        value_constraints.sort()
        
        # We initialize the list sorted_values, go through all the items in value
        # constraints and add the values to the sorted values list. We return the list.
        sorted_values = []
        for item in value_constraints:
            sorted_values.append(item[1])
        return sorted_values

    def forward_check(self, r, c, value):
        """
        INFERENCE: Forward Checking.
        Checks if assigning 'value' to (r,c) would leave any neighboring 
        empty cell with zero valid moves.
        """
        # Temporarily place the value to check against neighbors
        self.board[r][c] = value
        
        # Go through all the neighbors of the value
        for nr, nc in self.get_neighbors(r, c):
            # If neighbor is zero then there is no value at that spot
            if self.board[nr][nc] == 0:
                has_option = False
                # Check if the neighbor still has at least one legal move, we break.
                for v in range(1, self.n + 1):
                    if self.is_valid(nr, nc, v):
                        has_option = True
                        break
                # If a neighbor has no options left, this move is a dead end
                if not has_option:
                    # We revert to the spot being zero.
                    self.board[r][c] = 0
                    return False

        # Cleanup  
        self.board[r][c] = 0
        return True

    def mac(self, r, c, value):
        """
        INFERENCE: Maintaining Arc Consistency (MAC).
        Uses the AC-3 logic to ensure that every assignment maintains 
        consistency across the entire board, not just immediate neighbors.
        """
        # Initialize the queue as a standard list of arcs
        # Each arc is a tuple: (neighbor_cell, current_cell)
        queue = []
        for nb in self.get_neighbors(r, c):
            queue.append((nb, (r, c)))

        # Create a local map of all currently possible values for every cell
        domains = {}
        for row in range(self.n):
            for col in range(self.n):
                # if the spot is not equal to zero, the we add those possible values
                # into the domain of that row and column
                if self.board[row][col] != 0:
                    domains[(row, col)] = [self.board[row][col]]
                # Else, we create a list possible and check all possible valid moves
                # of that value and add them to list possible then make the list
                # possible the domain.
                else:
                    possible = []
                    for v in range(1, self.n + 1):
                        if self.is_valid(row, col, v):
                            possible.append(v)
                    domains[(row, col)] = possible
        
        # Fix the value of the current cell
        domains[(r, c)] = [value]

        # Arc consistency propagation loop
        while len(queue) > 0:
            xi, xj = queue.pop(0)
            # The question comes into play if we remove a value from xi's domain because 
            # xj makes it impossible
            revised = False
            for x in domains[xi][:]:
                # Conflict: If xj's only choice is the same as x, xi can't use x
                if len(domains[xj]) == 1 and domains[xj][0] == x:
                    domains[xi].remove(x)
                    revised = True
            
            if revised:
                # If xi now has zero options, the whole board is inconsistent
                if len(domains[xi]) == 0:
                    return False
                # Propagate the change to all neighbors of xi
                for xk in self.get_neighbors(xi[0], xi[1]):
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def solve(self, var_mode="std", val_mode="std", inf_mode="none"):
        """
        The main recursive backtracking loop.
        var_mode: "std" (first empty) or "mrv"
        val_mode: "std" (1..n) or "lcv"
        inf_mode: "none", "fc" (Forward Checking), or "mac" (AC-3)
        """
        # STEP 1: SELECT VARIABLE (WHERE TO FILL)
        # We first initialize cell
        cell = None
        # Here we can choose from standard order or minimum remaining value.
        if var_mode == "mrv":
            cell = self.get_mrv_cell()
        else:
            # RANDOM SELECTION
            # np.argwhere returns an array of coordinates where the condition is True
            empty_cells = np.argwhere(self.board == 0)
            
            if empty_cells.size > 0:
                # Pick a random cellx from the list of empty coordinate pairs
                random_cell = empty_cells[np.random.choice(len(empty_cells))]
                # Extrct the cell coordinates from the tuple (r, c)
                cell = (random_cell[0], random_cell[1])

        # Base case: If no empty cells are left, puzzle is solved
        if cell is None:
            return True
        else:
            r, c = cell
        
        # STEP 2: SELECT VALUES (WHAT NUMBER TO TRY)
        # Here we can choose from standard order or least-constraining-value
        if val_mode == "lcv":
            values = self.get_lcv_values(r, c)
        else:
            values = []
            for v in range(1, self.n + 1):
                values.append(v)

        # STEP 3: TRY VALUES AND RECURSE
        for val in values:
            if self.is_valid(r, c, val):
                # Apply Inference (FC or MAC)
                can_proceed = True
                if inf_mode == "fc":
                    can_proceed = self.forward_check(r, c, val)
                elif inf_mode == "mac":
                    can_proceed = self.mac(r, c, val)
                
                if can_proceed:
                    # Make the assignment
                    self.board[r][c] = val
                    
                    # Recursive call
                    if self.solve(var_mode, val_mode, inf_mode):
                        return True
                    
                    # BACKTRACK: Undo the move and increment counter
                    self.board[r, c] = 0
                    self.backtracks += 1
                    
        return False


def optimal_solver(json_file):
        """
        The 'Optimal' configuration based on experimental data:
        - Variable Selection: MRV (Minimum Remaining Values)
        - Inference: Forward Checking (FC)
        - Value Selection: Standard Order
        
        This configuration maximizes pruning while maintaining a low 
        computational cost per node, typically resulting in 0 backtracks 
        for 9x9 puzzles.
        Prints the initial board at the start and the final board upon success.
        """
        # 1. Load the puzzle from the JSON file
        try:
            with open(json_file, 'r') as f:
                initial_grid = json.load(f)
        except FileNotFoundError:
            print(f"Error: {json_file} not found.")
            return

        # 2. Initialize the Solver Class to handle the board and metrics
        solve = SudokuSolver(initial_grid)
        solve.reset()

        # --- PRINT INITIAL STATE ---
        
        print("\n" + "="*40)
        print("--- OPTIMAL SOLVER: INITIAL STATE ---")
        print("="*40)
        for row in solve.board:
            print(" ".join(str(int(x)) if x != 0 else "." for x in row))
        print("="*40 + "\n")


        def recursive_solve():
            # SELECT VARIABLE: Use MRV to find the most constrained cell
            cell = solve.get_mrv_cell()

            # Base case: If no empty cells remain, the puzzle is solved
            if cell is None:
                return True
            
            r, c = cell

            # SELECT VALUES: Use LCV
            values = solve.get_lcv_values(r, c)

            # TRY VALUES WITH INFERENCE: Forward Checking is used.
            for val in values:
                # Check basic constraints
                if solve.is_valid(r, c, val):
                    
                    # Apply MAC inference
                    if solve.forward_check(r, c, val):
                        
                        # Make the assignment
                        solve.board[r][c] = val
                        
                        # Recursive step
                        if recursive_solve():
                            return True
                        
                        # BACKTRACK: If the path fails, undo and increment counter
                        solve.board[r][c] = 0
                        solve.backtracks += 1
        
        # 5. Execute and Time the Search
        start_time = time.time()
        success = recursive_solve()
        duration = time.time() - start_time
    
        # 6. Print Results
        if success:
            print("\n" + "="*40 + "\n--- FINAL STATE (SOLVED) ---\n" + "="*40)
            # Print the final state
            for row in solve.board:
                print(" ".join(str(int(x)) for x in row))
            print("="*40)
            print(f"Status: SUCCESS")
            print(f"Time:   {duration:.4f}s")
            print(f"Nodes:  {solve.backtracks} backtracks")
        else:
            print("\nStatus: FAILED - No solution found.")

        return success


def run_comparison(json_file):
    """
    Main execution function to benchmark the efficiency of different 
    Sudoku solving strategies and heuristics.
    """
    # 1. Load the puzzle from the JSON file
    try:
        with open(json_file, 'r') as f:
            initial_grid = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")
        return

    # --- PRINT INITIAL STATE ---
    print("\n" + "="*40)
    print("-------- SUDOKU INITIAL STATE --------")
    print("="*40)
    # Using a simple loop for a cleaner grid look than raw list of lists
    for row in initial_grid:
        print(" ".join(str(x) if x != 0 else "." for x in row))
    print("="*40 + "\n")

    # 2. EXPERIMENT DESIGN: Define combinations to test against each other.
    # We compare a "basic/random" strategy against a "heuristic" strategy 
    # for each of the three major decision points in the solver.
    
    test_cases = [
        {
            "label": "Variable Selection: Random vs MRV",
            "configs": [
                {"name": "Random Selection", "var": "std", "val": "std", "inf": "fc"},
                {"name": "MRV", "var": "mrv", "val": "std", "inf": "fc"}
            ]
        },
        {
            "label": "Inference: Forward Checking vs MAC",
            "configs": [
                {"name": "Forward Checking", "var": "mrv", "val": "std", "inf": "fc"},
                {"name": "MAC Heuristic", "var": "mrv", "val": "std", "inf": "mac"}
            ]
        },
        {
            "label": "Value Selection: Standard Order vs LCV",
            "configs": [
                {"name": "Standard Order", "var": "mrv", "val": "std", "inf": "fc"},
                {"name": "LCV ", "var": "mrv", "val": "lcv", "inf": "fc"}
            ]
        }
    ]

    # 

    
    # 3. INITIALIZE SOLVER: Load the initial grid into our SudokuSolver class
    solver = SudokuSolver(initial_grid)
    # Flag to ensure we only print the solved board once
    final_state_printed = False 

    # 4. RUN BENCHMARKS: Loop through the designed experiments
    for case in test_cases:
        names = []
        times = []
        backtracks = []

        
        for config in case['configs']:
            # IMPORTANT: Revert the board to its original state before every run 
            # and zero out the backtrack counter to ensure a fair test.
            solver.reset()
            
            # Start timer
            start_time = time.time()
            # Execute the recursive solve method with the specific configuration
            success = solver.solve(var_mode=config['var'], 
                                  val_mode=config['val'], 
                                  inf_mode=config['inf'])
            # Stop timer
            end_time = time.time()
            
            duration = end_time - start_time
            
            # --- PRINT FINAL STATE (Only once, on the first success) ---
            if success and not final_state_printed:
                print("\n" + "="*40)
                print("       SUDOKU FINAL STATE (SOLVED)")
                print("="*40)
                # Print the solved board
                for row in solver.board:
                    print(" ".join(str(int(x)) for x in row))
                print("="*40 + "\n")
                

                

                final_state_printed = True
            # Want to print the label for readability
            print(f"\n--- {case['label']} ---")
            # Print Table Header for readability and we also want to print it only once
            print(f"{'Search Engine Comparison':<40} | {'Time (s)':<10} | {'Backtracks':<10}")
            print("-" * 70)


            # Store data for the graphs
            names.append(config['name'])
            times.append(duration)
            backtracks.append(solver.backtracks)

            # Output results: Comparing speed (seconds) and search effort (backtracks)
            if success:
                print(f"{config['name']:<40} | {duration:>8.4f}s | {solver.backtracks:>10}")
            else:
                print(f"{config['name']:<40} | FAILED     | {solver.backtracks:>10}")

    # 5. PLOTTING: Create 2 graphs per category (Total 6)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(f'Performance Comparison: {case["label"]}', fontsize=14)

        # Graph: Execution Time
        ax1.bar(names, times, color=['skyblue', 'steelblue'])
        ax1.set_title(f'{case["label"]}: Time')
        ax1.set_ylabel('Seconds')

        # Graph: Backtracks
        ax2.bar(names, backtracks, color=['salmon', 'firebrick'])
        ax2.set_title(f'{case["label"]}: Backtracks')
        ax2.set_ylabel('Count')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()


if __name__ == "__main__":
    # Ensure your json file is named correctly here
    #run_comparison('sudoku.json')
    optimal_solver('sudoku.json')