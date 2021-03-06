import tkinter as tk

from model.board import Board
from model.board_ranks_and_files import BoardFiles, BoardRanks

HEIGHT = 3840
WIDTH = 2160


class MainBody(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Michael's Chess")
        self.configure(bg="#ada99e", height=HEIGHT, width=WIDTH)  # 4a390a
        self.board = Board(self)
        self.board_ranks = BoardRanks(self)
        self.board_ranks.display_ranks()
        self.board_files = BoardFiles(self)
        self.board_files.display_files()
        self.add_buttons()

    def get_image(self, piece_name):
        try:
            return self.board.img_dict[piece_name]
        except KeyError:
            return ""

    def get_number_of_label(self, name: str):
        try:
            return int(name[name.rfind("l") + 1 :])
        except ValueError:
            return 1

    def update_piece_attrs(self, i, j):
        if self.board.board[i][j]:
            self.board.board[i][j].rank, self.board.board[i][j].file = i, j
        if self.board.board[7 - i][7 - j]:
            self.board.board[7 - i][7 - j].rank, self.board.board[7 - i][7 - j].file = (
                7 - i,
                7 - j,
            )

    def flip_command(self):
        for i in range(4):
            d = i if not self.board.flipped else 7 - i
            rank1 = "!label" if not i else f"!label{i+1}"
            rank2 = f"!label{8 - i}"
            self.board_files.children[rank1].configure(
                text=self.board_files.ranks[7 - d]
            )
            self.board_files.children[rank2].configure(text=self.board_files.ranks[d])

            self.board_ranks.children[rank1].configure(text=str(d + 1))
            self.board_ranks.children[rank2].configure(text=str(7 - d + 1))
            for j in range(8):
                self.board.board[i][j], self.board.board[7 - i][7 - j] = (
                    self.board.board[7 - i][7 - j],
                    self.board.board[i][j],
                )
                self.update_piece_attrs(i, j)
                if i or j:
                    first = f"!label{(i * 8) + j + 1}"
                else:
                    first = "!label"
                second = f"!label{((7 - i) * 8) + 7 - j + 1}"
                first_piece = self.board.board[i][j]
                k1 = (
                    first_piece
                    if not first_piece
                    else f"{first_piece.colour} {first_piece.name}"
                )
                second_piece = self.board.board[7 - i][7 - j]
                k2 = (
                    second_piece
                    if not second_piece
                    else f"{second_piece.colour} {second_piece.name}"
                )

                self.board.children[first].configure(image=self.get_image(k1))
                self.board.children[second].configure(image=self.get_image(k2))
        self.board.flipped ^= 1
        self.update_king_widget_and_positions()
        self.update_colours_for_previous_moves()
        self.update_legal_moves()

    def update_legal_moves(self):
        self.board.unshow_legal_moves()
        if self.board.legal_moves:
            self.board.legal_moves = [(7 - r, 7 - f) for r, f in self.board.legal_moves]
            self.board.previous_move[-1].legal_moves = self.board.legal_moves
            new_lab_num = 65 - self.get_number_of_label(str(self.board.moving_label))
            new_lab = f"!label{new_lab_num}" if new_lab_num > 1 else "!label"
            self.board.moving_label = self.board.children[new_lab]
        self.board.show_legal_moves()

    def update_colours_for_previous_moves(self):
        new_prev_move = []
        for w in self.board.previous_move:
            self.board.restore_label_colour(w)
            move_no = self.get_number_of_label(str(w))
            r, f = self.board.get_rank_and_file_from_label(str(w))
            new_m = "" if move_no == 64 else str(65 - move_no)
            self.board.children[f"!label{new_m}"].configure(
                bg=self.board.clicked_or_released_colour[(r + f) % 2]
            )
            new_prev_move.append(self.board.children[f"!label{new_m}"])
        self.board.previous_move = new_prev_move

    def update_king_widget_and_positions(self):
        self.board.kings_positions = [
            (7 - itm[0], 7 - itm[1]) for itm in self.board.kings_positions
        ]
        b_ki_no = self.get_number_of_label(str(self.board.kings_widgets[0]))
        w_ki_no = self.get_number_of_label(str(self.board.kings_widgets[1]))
        new_b_ki_no = "" if b_ki_no == 64 else str(65 - b_ki_no)
        new_w_ki_no = "" if w_ki_no == 64 else str(65 - w_ki_no)
        self.board.kings_widgets = [
            self.board.children[f"!label{new_b_ki_no}"],
            self.board.children[f"!label{new_w_ki_no}"],
        ]

    def new_game_command(self):
        self.board.reset_variables()
        self.board_ranks.reset_variables()
        self.board_files.reset_variables()

    def add_buttons(self):
        flip_button = tk.Button(
            self,
            text="Flip board",
            font=("Arial", 12),
            command=self.flip_command,
            bg="#c7655d",
            activebackground="#69605f",
        )
        flip_button.place(relx=0.8, rely=0.2, relheight=0.05, relwidth=0.1)

        new_game_button = tk.Button(
            self,
            text="New Game",
            font=("Arial", 12),
            command=self.new_game_command,
            bg="#c7655d",
            activebackground="#69605f",
        )
        new_game_button.place(relx=0.8, rely=0.26, relheight=0.05, relwidth=0.1)

    def play(self):
        self.mainloop()
