import random
import pickle

class TicTacToeAI:
    def __init__(self, player_char, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.999, load_q=True):
        self.player_char = player_char # Thats X or O
        self.q_table = {} # Saves the board tuple
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.history = [] # Saves the state and action for every game
        
        if load_q:
            self.load_q_table()
    
    def get_board_key(self, board):
        # Convert the board to tupel
        # Replace the "" with ' ' so the MLA can read it 
        normalized_board = []
        for row in board:
            normalized_row = []
            for cell in row:
                normalized_row.append(cell if cell != "" else ' ')
            normalized_board.append(tuple(normalized_row))
        return tuple(normalized_board)
    
    def get_available_moves(self, board, is_training):
        moves = []
        if is_training:
            print("getting moves while training...")
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        moves.append((r, c))
        else:
            print("getting moves in non-training mode")
            for r in range(3):
                for c in range(3):
                    if board[r][c] == '':
                        moves.append((r, c))
        return moves    

    def choose_action(self, board, is_training=True, load_q=True):
        print("choose_action called")
        board_key = self.get_board_key(board)
        print(f"Board key: {board_key}")
        available_moves = self.get_available_moves(board, is_training=is_training)
        print(f"Available moves: {available_moves}")
        
        if not available_moves:
            print("No available moves.")
            return None 
        
        if board_key not in self.q_table:
            self.q_table[board_key] = {move: 0.0 for move in available_moves}
            print(f"DEBUG: New state added to Q-table. Current Q-table size: {len(self.q_table)}")
        
        # Exploration (random choice) against Exploitation (best known move)
        if is_training and random.uniform(0, 1) < self.exploration_rate:
            print(f"Exploring: exploration_rate={self.exploration_rate}")
            move = random.choice(available_moves)
            print(f"Randomly chosen move: {move}")
        else:
            print("Exploiting known Q-values.")
            q_values_for_state = self.q_table[board_key]
            print(f"Q-values for state: {q_values_for_state}")
            
            # Delete not possible moves
            valid_q_values = {move: q_values_for_state.get(move, 0.0) for move in available_moves}
            print(f"Valid Q-values: {valid_q_values}")

            if not valid_q_values:
                print("No valid Q-values, choosing random move.")
                move = random.choice(available_moves)
            else:
                max_q_value = -float('inf')
                best_moves = []
                
                for move_coords, q_value in valid_q_values.items():
                    print(f"Checking move {move_coords} with Q-value {q_value}")
                    if q_value > max_q_value:
                        max_q_value = q_value
                        best_moves = [move_coords]
                    elif q_value == max_q_value:
                        best_moves.append(move_coords)
                
                print(f"Best moves: {best_moves} with Q-value: {max_q_value}")
                move = random.choice(best_moves)
                print(f"Chosen best move: {move}")
        
        if is_training:
            print(f"Appending to history: ({board_key}, {move})")
            self.history.append((board_key, move))
        
        print(f"Returning move: {move}")
        return move
    
    def update_q_table(self, reward, final_board_state):
        next_state_max_q_value = 0.0 
        
        for state, action in reversed(self.history):
            if state not in self.q_table:
                self.q_table[state] = {}
            if action not in self.q_table[state]:
                self.q_table[state][action] = 0.0

            current_q_value = self.q_table[state][action]

            # Rewards stuff
            target_q = reward + self.discount_factor * next_state_max_q_value
            
            # Uhm, not describing that shit
            self.q_table[state][action] = (1 - self.learning_rate) * current_q_value + \
                                            self.learning_rate * target_q
            
            next_state_max_q_value = self.q_table[state][action] 
        
        self.exploration_rate *= self.exploration_decay
    
    def clear_history(self):
        self.history = []
    
    def save_q_table(self, filename="q_table.pkl"):
        # Saves the Q-Table in a file
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f"Q-Table saved in {filename}")
    
    def load_q_table(self, filename="q_table.pkl"):
        # Loads the Q-Table out of the file
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
            
            print(f"Q-Table load from {filename}. Total Values: {len(self.q_table)}")
            
        except FileNotFoundError:
            print(f"Couldn't find Q-Table {filename}, starting with empty table...")
            
        except Exception as e:
            print(f"Error while loading Q-Table: {e}. Starting with empty table...")