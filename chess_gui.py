import tkinter as tk
from tkinter import messagebox
import chess
import chess.engine
import chess.pgn
import os
import time
import argparse
from PIL import Image, ImageTk
import threading
import concurrent.futures


class ChessGUI:
    def __init__(self, master, player_color):
        self.master = master
        master.title("Chess GUI")

        # Initialize chess board and engine
        self.board = chess.Board()
        self.engine_path = os.path.join(os.getcwd(), "RyanTrainer", "lc0.exe")
        if not os.path.exists(self.engine_path):
            messagebox.showerror("Error", f"Engine not found at {self.engine_path}")
            exit()

        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        self.engine.configure({"Threads": 3})  # Adjust as needed
        self.board_lock = threading.Lock() 

        # Initialize ThreadPoolExecutor with one worker thread
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        # Variables to track user interaction
        self.selected_square = None
        self.player_color = chess.WHITE if player_color.lower() == "white" else chess.BLACK
        self.board_flipped = self.player_color == chess.BLACK  # Flip board if player is black
        self.game_result = None  # Variable to store the game result

        # Create GUI elements
        self.create_widgets()

        # Now that self.canvas is initialized, we can update the board
        self.update_board()

        # If player is black, make the engine move immediately
        if self.player_color == chess.BLACK:
            self.master.after(100, self.engine_move)
            #threading.Thread(target=self.engine_move).start()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=512, height=512)
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Control frame
        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Resign buttons
        #self.resign_button = tk.Button(self.control_frame, text="Resign", command=self.player_resign)
        #self.resign_button.pack(pady=5)

        #self.engine_resign_button = tk.Button(self.control_frame, text="Force Engine to Resign", command=self.engine_resign)
        #self.engine_resign_button.pack(pady=5)

        # Reset Progress button
        self.reset_button = tk.Button(self.control_frame, text="Reset Progress", command=self.reset_progress)
        self.reset_button.pack(pady=5)

        # Show Progress button
        self.show_progress_button = tk.Button(self.control_frame, text="Show Progress", command=self.show_progress)
        self.show_progress_button.pack(pady=5)

        # Check if progression.png exists and games folder is not empty
        self.check_progress_availability()

    def check_progress_availability(self):
        # Path to progression.png
        self.progression_image_path = os.path.join(os.getcwd(), "progression.png")
        # Path to games folder
        self.games_folder = os.path.join(os.getcwd(), "RyanTrainer", "games")

        # Check if progression.png exists and games folder is not empty
        if os.path.exists(self.progression_image_path) and os.path.exists(self.games_folder):
            if os.listdir(self.games_folder):
                # Enable the Show Progress button
                self.show_progress_button.config(state=tk.NORMAL)
            else:
                # Disable the Show Progress button
                self.show_progress_button.config(state=tk.DISABLED)
        else:
            # Disable the Show Progress button
            self.show_progress_button.config(state=tk.DISABLED)

    def update_board(self):
        self.canvas.delete("all")
        colors = ["#F0D9B5", "#B58863"]  # Light and dark squares
        highlight_color = "#BACA2B"  # Color for highlighting the last move
        square_size = 64
        unicode_pieces = {
            'P': '\u265F', 'N': '\u265E', 'B': '\u265D',
            'R': '\u265C', 'Q': '\u265B', 'K': '\u265A',
            'p': '\u265F', 'n': '\u265E', 'b': '\u265D',
            'r': '\u265C', 'q': '\u265B', 'k': '\u265A',
        }

        # Get last move if it exists
        last_move = self.board.peek() if self.board.move_stack else None
        from_square = last_move.from_square if last_move else None
        to_square = last_move.to_square if last_move else None

        if self.board_flipped:
            rank_range = range(8)
            file_range = range(7, -1, -1)
        else:
            rank_range = range(7, -1, -1)
            file_range = range(8)

        for rank_index, rank in enumerate(rank_range):
            for file_index, file in enumerate(file_range):
                x1 = file_index * square_size
                y1 = rank_index * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size
                square = chess.square(file, rank)

                # Determine square color
                if square == from_square or square == to_square:
                    color = highlight_color  # Highlight squares involved in the last move
                else:
                    color = colors[(file + rank + 1) % 2]  # Normal square color

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="square")

                piece = self.board.piece_at(square)
                if piece:
                    symbol = piece.symbol()
                    unicode_char = unicode_pieces[symbol]
                    font_size = 40
                    piece_color = 'white' if piece.color == chess.WHITE else 'black'
                    self.canvas.create_text(x1 + square_size / 2, y1 + square_size / 2,
                                            text=unicode_char, font=("Arial", font_size),
                                            fill=piece_color, tags="piece")

        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")
        self.check_game_over()

    def on_canvas_click(self, event):
        if self.board.is_game_over():
            return  # Game is over

        if self.board.turn != self.player_color:
            return  # Not player's turn

        with self.board_lock:
            square_size = 64
            col = event.x // square_size
            row = event.y // square_size

            if self.board_flipped:
                file = 7 - col
                rank = row
            else:
                file = col
                rank = 7 - row

            square = chess.square(file, rank)

            if self.selected_square is None:
                piece = self.board.piece_at(square)
                if piece and piece.color == self.board.turn and piece.color == self.player_color:
                    self.selected_square = square
                    self.highlight_square(square)
            else:
                piece = self.board.piece_at(self.selected_square)
                move = chess.Move(self.selected_square, square)

                # Check for pawn promotion
                if piece and piece.piece_type == chess.PAWN:
                    target_rank = chess.square_rank(square)
                    if (piece.color == chess.WHITE and target_rank == 7) or \
                        (piece.color == chess.BLACK and target_rank == 0):
                        # Pawn promotion
                        promotion_piece_type = self.prompt_promotion()
                        if promotion_piece_type is None:
                            # User cancelled promotion
                            self.selected_square = None
                            self.update_board()
                            return
                        move = chess.Move(self.selected_square, square, promotion=promotion_piece_type)

                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.update_board()
                    self.selected_square = None
                    threading.Thread(target=self.engine_move).start()  # Use threading to call engine_move
                else:
                    self.selected_square = None
                    self.update_board()

    def highlight_square(self, square):
        square_size = 64
        file = chess.square_file(square)
        rank = chess.square_rank(square)

        if self.board_flipped:
            col = 7 - file
            row = rank
        else:
            col = file
            row = 7 - rank

        x1 = col * square_size
        y1 = row * square_size
        x2 = x1 + square_size
        y2 = y1 + square_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=3)

    def prompt_promotion(self):
        promotion_window = tk.Toplevel(self.master)
        promotion_window.title("Choose promotion piece")
        piece_var = tk.StringVar(value="q")

        tk.Label(promotion_window, text="Promote to:").pack()

        pieces = [("Queen", "q"), ("Rook", "r"), ("Bishop", "b"), ("Knight", "n")]
        for text, value in pieces:
            tk.Radiobutton(promotion_window, text=text, variable=piece_var, value=value).pack(anchor=tk.W)

        def on_ok():
            promotion_window.destroy()

        tk.Button(promotion_window, text="OK", command=on_ok).pack()

        promotion_window.grab_set()
        self.master.wait_window(promotion_window)

        piece = piece_var.get()
        if piece == 'q':
            return chess.QUEEN
        elif piece == 'r':
            return chess.ROOK
        elif piece == 'b':
            return chess.BISHOP
        elif piece == 'n':
            return chess.KNIGHT
        else:
            return None

    def engine_move(self):
        if self.board.is_game_over():
            return

        # This function will run in a separate thread
        def perform_engine_move():
            try:
                limit = chess.engine.Limit(depth=7, time=10)
                result = self.engine.play(self.board, limit)
                return result.move
            except chess.engine.EngineError as e:
                print(f"Engine error: {e}")
                return None


        # This function will be called on the main thread after the engine move is made
        def after_move(future):
            try:
                move = future.result()  # Get the result of the future
                with self.board_lock:  # Ensure thread safety when accessing the board
                    if move in self.board.legal_moves:  # Check if move is still legal
                        self.board.push(move)
                        self.update_board()
                    else:
                        print("Move is no longer legal. Skipping the engine move.")
            except Exception as e:
                print(f"Error handling engine move: {e}")

        # Acquire the lock before making an engine move
        with self.board_lock:
            future = self.executor.submit(perform_engine_move)
            future.add_done_callback(lambda f: self.master.after(0, after_move, f))



    def check_game_over(self):
        if self.board.is_checkmate():
            winner = "White" if self.board.turn == chess.BLACK else "Black"
            self.game_result = "1-0" if winner == "White" else "0-1"
            messagebox.showinfo("Game Over", f"Checkmate! {winner} wins.")
            self.save_game_automatic()
            self.on_closing()
        elif self.board.is_stalemate():
            self.game_result = "1/2-1/2"
            messagebox.showinfo("Game Over", "Stalemate!")
            self.save_game_automatic()
            self.on_closing()
        elif self.board.is_insufficient_material():
            self.game_result = "1/2-1/2"
            messagebox.showinfo("Game Over", "Draw due to insufficient material.")
            self.save_game_automatic()
            self.on_closing()
        elif self.board.can_claim_fifty_moves():
            self.game_result = "1/2-1/2"
            messagebox.showinfo("Game Over", "Draw by fifty-move rule.")
            self.save_game_automatic()
            self.on_closing()
        elif self.board.can_claim_threefold_repetition():
            self.game_result = "1/2-1/2"
            messagebox.showinfo("Game Over", "Draw by threefold repetition.")
            self.save_game_automatic()
            self.on_closing()

    def player_resign(self):
        winner = "Black" if self.player_color == chess.WHITE else "White"
        self.game_result = "0-1" if self.player_color == chess.WHITE else "1-0"
        messagebox.showinfo("Game Over", f"You have resigned. {winner} wins.")
        self.save_game_automatic()
        self.on_closing()

    def engine_resign(self):
        winner = "White" if self.player_color == chess.WHITE else "Black"
        self.game_result = "1-0" if self.player_color == chess.WHITE else "0-1"
        messagebox.showinfo("Game Over", f"Engine has resigned. {winner} wins.")
        self.save_game_automatic()
        self.on_closing()

    def save_game_automatic(self):
        # Determine the folder path
        games_folder = os.path.join(os.getcwd(), "RyanTrainer", "games")
        os.makedirs(games_folder, exist_ok=True)

        # Find the highest game index
        existing_files = [f for f in os.listdir(games_folder) if f.startswith("game_") and f.endswith(".pgn")]
        indices = [int(f[5:8]) for f in existing_files if f[5:8].isdigit()]
        next_index = max(indices) + 1 if indices else 0

        if next_index > 999:
            # Offer to archive the games
            answer = messagebox.askyesno("Game Limit Reached", "You have reached the 1000-game limit. Would you like to archive your games?")
            if answer:
                # Archive the games
                archive_folder_name = "archive_" + time.strftime("%Y_%m_%d_%H_%M_%S")
                archive_folder = os.path.join(os.getcwd(), "RyanTrainer", archive_folder_name)
                os.makedirs(archive_folder, exist_ok=True)
                for filename in existing_files:
                    src_path = os.path.join(games_folder, filename)
                    dst_path = os.path.join(archive_folder, filename)
                    os.rename(src_path, dst_path)
                messagebox.showinfo("Archive Games", f"Your games have been archived to {archive_folder}. Your progress has been reset.")
                # Reset next_index to 0
                next_index = 0
                # Update the Show Progress button
                self.check_progress_availability()
            else:
                messagebox.showinfo("Game Not Saved", "Your game was not saved. Please reset your progress to save new games.")
                return

        filename = f"game_{next_index:03d}.pgn"
        file_path = os.path.join(games_folder, filename)

        # Create PGN game
        game = chess.pgn.Game()
        node = game

        # Set up headers
        game.headers["Event"] = "?"
        game.headers["Site"] = "?"
        game.headers["Date"] = time.strftime("%Y.%m.%d")
        game.headers["Round"] = "1"

        # Determine who is white and who is black
        if self.player_color == chess.WHITE:
            game.headers["White"] = "Player"
            game.headers["Black"] = "Engine"
        else:
            game.headers["White"] = "Engine"
            game.headers["Black"] = "Player"

        # Set the result
        if self.game_result:
            game.headers["Result"] = self.game_result
        else:
            game.headers["Result"] = self.board.result()

        # Add moves to the game
        for move in self.board.move_stack:
            node = node.add_main_variation(move)

        # Save the game to a PGN file
        with open(file_path, 'w') as pgn_file:
            print(game, file=pgn_file)

        messagebox.showinfo("Save Game", f"Game automatically saved to {file_path}")
        self.game_result = None  # Reset the game result after saving

        # Update the Show Progress button
        self.check_progress_availability()

    def reset_progress(self):
        answer = messagebox.askyesno("Reset Progress", "Are you sure you want to reset your progress? This will delete all saved games.", icon='warning')
        if answer:
            games_folder = os.path.join(os.getcwd(), "RyanTrainer", "games")
            if os.path.exists(games_folder):
                # Delete all files in the games folder
                for filename in os.listdir(games_folder):
                    file_path = os.path.join(games_folder, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                messagebox.showinfo("Reset Progress", "Your progress has been reset.")
                # Update the Show Progress button
                self.check_progress_availability()
            else:
                messagebox.showinfo("Reset Progress", "No games found to delete.")
        else:
            messagebox.showinfo("Reset Progress", "Progress reset canceled.")

    def show_progress(self):
        # Open a new window to display the progression image
        try:
            progress_window = tk.Toplevel(self.master)
            progress_window.title("Progression")

            # Load the image
            image = Image.open(self.progression_image_path)
            photo = ImageTk.PhotoImage(image)

            # Create a label to display the image
            label = tk.Label(progress_window, image=photo)
            label.image = photo  # Keep a reference to prevent garbage collection
            label.pack()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display progression image: {e}")

    def on_closing(self):
        self.executor.shutdown(wait=False)
        self.engine.quit()
        self.master.destroy()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple Chess GUI')
    parser.add_argument('color', choices=['white', 'black'], help='Player color (white or black)')
    args = parser.parse_args()

    root = tk.Tk()
    gui = ChessGUI(root, args.color)
    root.protocol("WM_DELETE_WINDOW", gui.on_closing)
    root.mainloop()
