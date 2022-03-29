import tkinter as tk

from model.board import Board
from model.board_ranks_and_files import BoardFiles, BoardRanks

HEIGHT = 3840
WIDTH = 2160


class MainBody(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Michael's Chess")
        self.configure(bg='#ada99e', height=HEIGHT, width=WIDTH)  # 4a390a
        self.board = Board(self)
        self.board_ranks = BoardRanks(self)
        self.board_ranks.display_ranks()
        self.board_files = BoardFiles(self)
        self.add_button()

    def get_image(self, piece_name):
        try:
            return self.board.img_dict[piece_name]
        except KeyError:
            return ''

    def get_number_of_label(self, name: str):
        try:
            return int(name[name.rfind('l')+1:])
        except ValueError:
            return 1

    def flip_command(self):
        for i in range(4):
            d = i if not self.board.flipped else 7-i
            rank1 = '!label' if not i else f"!label{i+1}"
            rank2 = f'!label{8 - i}'
            self.board_ranks.children[rank1].configure(
                text=self.board_ranks.ranks[7-d])
            self.board_ranks.children[rank2].configure(
                text=self.board_ranks.ranks[d])

            self.board_files.children[rank1].configure(text=str(d+1))
            self.board_files.children[rank2].configure(text=str(7-d+1))
            for j in range(8):
                self.board.board[i][j], self.board.board[7-i][7 -
                                                              j] = self.board.board[7-i][7-j], self.board.board[i][j]
                if i or j:
                    first = f'!label{(i * 8) + j + 1}'
                else:
                    first = '!label'
                second = f'!label{((7 - i) * 8) + 7 - j + 1}'

                self.board.children[first].configure(
                    image=self.get_image(self.board.board[i][j]))
                self.board.children[second].configure(
                    image=self.get_image(self.board.board[7-i][7-j]))
        self.board.flipped ^= 1
        self.update_king_widget_and_positions()
        self.update_colours_for_previous_moves()

    def update_colours_for_previous_moves(self):
        new_prev_move = []
        for w in self.board.previous_move:
            self.board.restore_label_colour(w)
            move_no = self.get_number_of_label(str(w))
            new_m = '' if move_no == 64 else str(65-move_no)
            self.board.children[f"!label{new_m}"].configure(
                bg=self.board.clicked_or_released_colour)
            new_prev_move.append(self.board.children[f"!label{new_m}"])
        self.board.previous_move = new_prev_move

    def update_king_widget_and_positions(self):
        self.board.kings_positions = [
            (7 - itm[0], 7 - itm[1]) for itm in self.board.kings_positions]
        b_ki_no = self.get_number_of_label(str(self.board.kings_widgets[0]))
        w_ki_no = self.get_number_of_label(str(self.board.kings_widgets[1]))
        new_b_ki_no = '' if b_ki_no == 64 else str(65-b_ki_no)
        new_w_ki_no = '' if w_ki_no == 64 else str(65-w_ki_no)
        self.board.kings_widgets = [
            self.board.children[f"!label{new_b_ki_no}"], self.board.children[f"!label{new_w_ki_no}"]]

    def add_button(self):
        flip_button = tk.Button(self, text='Flip board', font=(
            'Arial', 12), command=self.flip_command, bg='#c7655d', activebackground='#69605f')
        flip_button.place(relx=0.8, rely=0.2, relheight=0.05, relwidth=0.1)

    def play(self):
        self.mainloop()
