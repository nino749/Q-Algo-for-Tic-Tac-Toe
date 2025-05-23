import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Q_Algo import TicTacToeAI
import threading
import time

THEMES = [
    {
        "name": "Purple",
        "bg_color": "#ede7f6",
        "board_bg": "#ffffff",
        "line_color": "#7c4dff",
        "p1_color": "#7c4dff",
        "p2_color": "#3949ab",
        "txt_color": "#3a2a4d",
        "msg_bg": "#d1c4e9",
        "btn_bg": "#7c4dff",
        "btn_fg": "#ffffff",
        "btn_actv": "#412888",
        "icon": "🟣"
    },
    {
        "name": "Green",
        "bg_color": "#e8f5e9",
        "board_bg": "#ffffff",
        "line_color": "#43a047",
        "p1_color": "#43a047",
        "p2_color": "#1b5e20",
        "txt_color": "#1b2a1d",
        "msg_bg": "#c8e6c9",
        "btn_bg": "#43a047",
        "btn_fg": "#ffffff",
        "btn_actv": "#245a27",
        "icon": "🟢"
    },
    {
        "name": "Blue",
        "bg_color": "#e3f2fd",
        "board_bg": "#ffffff",
        "line_color": "#1976d2",
        "p1_color": "#1976d2",
        "p2_color": "#0288d1",
        "txt_color": "#0d223a",
        "msg_bg": "#bbdefb",
        "btn_bg": "#1976d2",
        "btn_fg": "#ffffff",
        "btn_actv": "#0d223a",
        "icon": "🔵"
    },
    {
        "name": "Red",
        "bg_color": "#ffebee",
        "board_bg": "#ffffff",
        "line_color": "#d32f2f",
        "p1_color": "#d32f2f",
        "p2_color": "#c62828",
        "txt_color": "#3d1a1a",
        "msg_bg": "#ffcdd2",
        "btn_bg": "#d32f2f",
        "btn_fg": "#ffffff",
        "btn_actv": "#a31515",
        "icon": "🔴"
    },
    {
        "name": "Orange",
        "bg_color": "#fff3e0",
        "board_bg": "#ffffff",
        "line_color": "#fb8c00",
        "p1_color": "#fb8c00",
        "p2_color": "#ef6c00",
        "txt_color": "#4e2e0e",
        "msg_bg": "#ffe0b2",
        "btn_bg": "#fb8c00",
        "btn_fg": "#ffffff",
        "btn_actv": "#b25a00",
        "icon": "🟠"
    },
    {
        "name": "Pink",
        "bg_color": "#fce4ec",
        "board_bg": "#ffffff",
        "line_color": "#d81b60",
        "p1_color": "#d81b60",
        "p2_color": "#ad1457",
        "txt_color": "#3a1a2a",
        "msg_bg": "#f8bbd0",
        "btn_bg": "#d81b60",
        "btn_fg": "#ffffff",
        "btn_actv": "#880e4f",
        "icon": "🌸"
    },
    {
        "name": "Yellow",
        "bg_color": "#fffde7",
        "board_bg": "#ffffff",
        "line_color": "#fbc02d",
        "p1_color": "#fbc02d",
        "p2_color": "#f9a825",
        "txt_color": "#ffffff",
        "msg_bg": "#fff9c4",
        "btn_bg": "#fbc02d",
        "btn_fg": "#ffffff",
        "btn_actv": "#a09502",
        "icon": "🟡"
    },
    {
        "name": "Aqua",
        "bg_color": "#e0f7fa",
        "board_bg": "#ffffff",
        "line_color": "#00bcd4",
        "p1_color": "#00bcd4",
        "p2_color": "#00838f",
        "txt_color": "#00363a",
        "msg_bg": "#b2ebf2",
        "btn_bg": "#00bcd4",
        "btn_fg": "#ffffff",
        "btn_actv": "#006064",
        "icon": "🟦"
    }
]

font = "Segoe UI"

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.theme_index = 0
        self.theme = THEMES[self.theme_index]
        master.title("Tic Tac Toe vs. AI")
        master.geometry("420x685")
        master.resizable(False, False)
        
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        
        # AI Stuff
        self.ai_player = "O" # AI playes as "O"
        self.ai = TicTacToeAI(player_char=self.ai_player, exploration_decay=0.9995, load_q=True)
        
        # Theme button
        self.theme_btn = tk.Button(
            master, text=self.theme["icon"], font=(font, 16),
            command=self.switch_theme, bg=self.theme["btn_bg"], fg=self.theme["btn_fg"],
            bd=0, relief="flat", padx=8, pady=2, cursor="hand2"
        )
        self.theme_btn.place(x=370, y=10)

        # Title label
        self.title_label = tk.Label(
            master, text="Tic Tac Toe", font=(font, 28, "bold"),
            bg=self.theme["bg_color"], fg=self.theme["line_color"]
        )
        self.title_label.pack(pady=(24, 8))
        
        # Message label
        self.message_label = tk.Label(
            master, text=f"Player {self.current_player} has to play",
            font=(font, 16), bg=self.theme["msg_bg"], fg=self.theme["txt_color"], bd=0, relief="flat",
            padx=10, pady=6
        )
        self.message_label.pack(pady=(0, 18))

        # Canvas frame for rounded border effect
        self.board_frame = tk.Frame(master, bg=self.theme["bg_color"], bd=0)
        self.board_frame.pack(pady=0)

        # Canvas
        self.canvas = tk.Canvas(
            self.board_frame, width=340, height=340,
            bg=self.theme["board_bg"], highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        # Restart button
        self.restart_btn = tk.Button(
            master, text="Play Again", command=self.reset_game,
            font=(font, 14, "bold"), bg=self.theme["btn_bg"], fg=self.theme["btn_fg"],
            activebackground=self.theme["btn_actv"], activeforeground=self.theme["btn_fg"],
            bd=0, relief="flat", padx=18, pady=8, cursor="hand2"
        )
        self.restart_btn.pack(pady=(20, 20))
        
        # Training button
        self.train_btn = tk.Button(
            master, text="Train AI", command=self.start_training,
            font=(font, 12), background=self.theme["btn_bg"], foreground=self.theme["btn_fg"],
            activebackground=self.theme["btn_actv"], activeforeground=self.theme["btn_fg"],
            bd=0, relief="flat", padx=12, pady=6, cursor="hand2"
        )
        self.train_btn.pack(pady=(5, 0))
        
        # Progress bar
        self.progress_var = tk.DoubleVar() # Var to save the progress
        self.progress_bar = ttk.Progressbar(
            master,
            orient="horizontal",
            length=300,
            mode="determinate", # Bc we know the progress 
            variable=self.progress_var
        )
        self.progress_bar.pack(pady=(10, 1))
        
        # Labels for the progressbar
        self.progress_label = tk.Label(
            master, text="", font=(font, 10),
            bg=self.theme["bg_color"], fg=self.theme["txt_color"]
        )
        self.progress_label.pack(pady=(5, 5))
        
        self.apply_theme()
        self.draw_board()

    def apply_theme(self):
        t = self.theme
        self.master.configure(bg=t["bg_color"])
        self.title_label.config(bg=t["bg_color"], fg=t["line_color"])
        self.message_label.config(bg=t["msg_bg"], fg=t["txt_color"])
        self.board_frame.config(bg=t["bg_color"])
        self.canvas.config(bg=t["board_bg"])
        self.restart_btn.config(bg=t["btn_bg"], fg=t["btn_fg"], activebackground=t["btn_actv"])
        self.theme_btn.config(bg=t["btn_bg"], fg=t["btn_fg"], text=t["icon"], activebackground=t["btn_actv"])
        self.progress_label.config(bg=t["bg_color"], fg=t["txt_color"])
        self.train_btn.config(bg=t["btn_bg"], fg=t["btn_fg"], activebackground=t["btn_actv"], activeforeground=t["btn_fg"])

        self.draw_board()

    def switch_theme(self):
        self.theme_index = (self.theme_index + 1) % len(THEMES)
        self.theme = THEMES[self.theme_index]
        self.apply_theme()

    def draw_board(self):
        t = self.theme
        self.canvas.delete("all")
        cell_size = 100
        offset = 20
        board_size = cell_size * 3

        self.canvas.create_rectangle(
            offset, offset, offset + board_size, offset + board_size,
            fill=t["board_bg"], outline=t["msg_bg"], width=3
        )

        for i in range(1, 3):
            self.canvas.create_line(
                offset, offset + i * cell_size,
                offset + board_size, offset + i * cell_size,
                width=6, fill=t["line_color"], capstyle=tk.ROUND
            )
            self.canvas.create_line(
                offset + i * cell_size, offset,
                offset + i * cell_size, offset + board_size,
                width=6, fill=t["line_color"], capstyle=tk.ROUND
            )

        for r in range(3):
            for c in range(3):
                player = self.board[r][c]
                if player:
                    x = offset + c * cell_size + cell_size // 2
                    y = offset + r * cell_size + cell_size // 2
                    if player == "X":
                        self.canvas.create_line(
                            x - 28, y - 28, x + 28, y + 28,
                            width=7, fill=t["p1_color"], capstyle=tk.ROUND
                        )
                        self.canvas.create_line(
                            x + 28, y - 28, x - 28, y + 28,
                            width=7, fill=t["p1_color"], capstyle=tk.ROUND
                        )
                    else:
                        self.canvas.create_oval(
                            x - 32, y - 32, x + 32, y + 32,
                            width=7, outline=t["p2_color"]
                        )

    def handle_click(self, event):
        if self.game_over:
            return
        cell_size = 100
        offset = 20
        col = (event.x - offset) // cell_size
        row = (event.y - offset) // cell_size
        
        # Human turn
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.draw_board()
            self.check_game_state()
            
            if not self.game_over:
                self.switch_player() # Switch to AI
                self.update_message()
                
                # Ai turn
                if self.current_player == self.ai_player:
                    # Delays the AI a bit, so the GUI dont block it
                    self.master.after(500, self.ai_make_move) # 500ms

    def start_training(self):
        # Deactivating the button
        self.train_btn.config(state=tk.DISABLED, text="Training...")
        self.message_label.config(text="Training the AI, pls wait UwU")
        
        # Progressbar
        self.progress_var.set(0) # Progress set to 0
        self.progress_label.config(text="0%") # Text set to 0%
        self.progress_bar.config(value=0) # Progressbar set to 0
        self.progress_bar.stop() # So that it doesn't run in 'indeterminate'
        
        # Start the training
        self.ai.exploration_rate = 1.0
        
        training_thread = threading.Thread(target=self._run_training_in_thread)
        training_thread.daemon = True
        training_thread.start()

    def _run_training_in_thread(self):
        # Ask user for number of games in the main thread
        def ask_num_games():
            import tkinter.simpledialog
            num_games = tkinter.simpledialog.askinteger(
                "AI Training", "Enter number of training games (avrg. per game: 2,4ms):",
                initialvalue=100000, minvalue=100, maxvalue=1000000, parent=self.master
            )
            return num_games

        from threading import Event
        self._num_games_event = Event()
        self._num_games = None

        def get_num_games():
            self._num_games = ask_num_games()
            self._num_games_event.set()

        # Ask for number of games in the main thread
        self.master.after(0, get_num_games)
        self._num_games_event.wait()

        num_games = self._num_games
        if num_games is None:
            # User cancelled, re-enable button
            self.master.after(0, lambda: self.train_btn.config(state=tk.NORMAL, text="Train AI"))
            self.master.after(0, lambda: self.message_label.config(text="Training cancelled."))
            return

        self.train_ai(num_games=num_games)
        self.master.after(0, self._training_completed)
        

    def _training_completed(self):
        self.train_btn.config(state=tk.NORMAL, text="Train AI")
        self.message_label.config(text="Training finished. Player X's turn")
        
        # Progressbar
        self.progress_var.set(0) # Progress set to 0
        self.progress_label.config(text="0%") # Text set to 0%
        self.progress_bar.config(value=0) # Progressbar set to 0
        self.progress_bar.stop() # So that it doesn't run in 'indeterminate'
        
        self.ai.exploration_rate = 0.0
        print("AI is now in the playing modus")
        
        self.reset_game()
    
    def ai_make_move(self):
        if self.game_over:
            return
        
        original_exploration_rate = self.ai.exploration_rate
        self.ai.exploration_rate = 0.0
        
        move = self.ai.choose_action(self.board, is_training=False) # is_training false, bc its no training
        
        self.ai.exploration_rate = original_exploration_rate
        
        if move:
            r, c = move
            self.board[r][c] = self.ai_player
            self.draw_board()
            self.check_game_state()
            
            if not self.game_over:
                self.switch_player()
                self.update_message()
                
        else:
            self.check_game_state()

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_game_state(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                self.end_game(self.board[i][0])
                return
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                self.end_game(self.board[0][i])
                return
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            self.end_game(self.board[0][0])
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            self.end_game(self.board[0][2])
            return
        if all(self.board[r][c] != "" for r in range(3) for c in range(3)):
            self.end_game("Draw")
            return

    def end_game(self, winner):
        self.game_over = True
        if winner == "Draw":
            self.message_label.config(text="Draw")
            messagebox.showinfo("Finished the game", "It ended in a draw")
        else:
            self.message_label.config(text=f"Player {winner} has won the game!")
            messagebox.showinfo("Finished the game", f"Player {winner} has won the game!")

    def update_message(self):
        if not self.game_over:
            self.message_label.config(text=f"Player {self.current_player} has to play")

    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.draw_board()
        self.update_message()
        
        # If AI is player 'X', it should make the first move
        if self.current_player == self.ai_player:
            self.master.after(500, self.ai_make_move) # Wait 500ms to not overload the GUI
        
    #---------------------------------------------
    # Train the AI
    # --------------------------------------------
    
    def train_ai(self, num_games):
        print(f"Starting AI training with {num_games} games...")

        opponent_ai = TicTacToeAI(player_char='X', exploration_rate=1.0, exploration_decay=0.999, load_q=False)
        self.ai.exploration_rate = 1.0 

        update_interval = max(1, num_games // 1000)
        print(f"Progress bar will update every {update_interval} games.")

        start_time = time.time()  # Start timer

        for i in range(num_games):
            temp_board = [[' ' for _ in range(3)] for _ in range(3)]
            current_training_player = 'X'

            self.ai.clear_history() 
            opponent_ai.clear_history()

            while True:
                if current_training_player == 'X':
                    move = opponent_ai.choose_action(temp_board, is_training=True, load_q=False)
                    if move:
                        temp_board[move[0]][move[1]] = 'X'
                else:  # The 'O' move
                    move = self.ai.choose_action(temp_board, is_training=True, load_q=True)
                    if move:
                        temp_board[move[0]][move[1]] = 'O'
                winner = self._check_game_state_ai(temp_board)
                if winner:
                    break

                current_training_player = 'O' if current_training_player == 'X' else 'X'

            # Rewards
            if winner == 'X':
                opponent_ai.update_q_table(1, temp_board)
                self.ai.update_q_table(-1, temp_board)
            elif winner == 'O':
                opponent_ai.update_q_table(-1, temp_board)
                self.ai.update_q_table(1, temp_board)
            else:  # if its a Draw
                opponent_ai.update_q_table(0.5, temp_board)
                self.ai.update_q_table(0.5, temp_board)

            if (i + 1) % update_interval == 0 or (i + 1) == num_games: 
                progress_percent = ((i + 1) / num_games) * 100
                self.master.after(0, self.update_progress_gui, progress_percent, i + 1, num_games)

            if (i + 1) % (num_games // 10) == 0:
                print(f"  {i+1}/{num_games} games trained. AI-Exploration: {self.ai.exploration_rate:.4f}")

        end_time = time.time()  # Stop timer
        elapsed = end_time - start_time
        print("AI-Training done!!")
        print(f"Training took {elapsed:.2f} seconds.")
        self.ai.save_q_table()
        
    # Function to update the progressbar
    def update_progress_gui(self, percent, current_game, total_games):
        self.progress_var.set(percent)
        self.progress_label.config(text=f"{percent:.1f}% ({current_game} / {total_games} games)")
        self.progress_bar.config(value=percent)

    def _check_game_state_ai(self, board):
        # Helping function
        # Returns the winner, 'X', 'O', 'Draw' or None

        # Check rows, columns
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != ' ': 
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != ' ': 
                return board[0][i]
            
        # Check diagonals     
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ': 
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ': 
            return board[0][2]
        
        # Check draw
        if all(board[r][c] != ' ' for r in range(3) for c in range(3)): 
            return 'Draw'
        
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()