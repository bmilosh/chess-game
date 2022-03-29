
import tkinter as tk

from PIL import Image, ImageTk

from model.board_ranks_and_files import BoardFiles, BoardRanks
from model.pieces import *
from model.square_validator import SquareValidator

SQUARE_RATIO = 1/8


class Board(tk.Frame):
    # Colours
    board_colours = ['#4a390a', '#ebd086']
    focus_colour = '#ebd086'
    clicked_or_released_colour = '#818399'

    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']  # list('abcdefgh')

    # Pieces
    pawn = Pawn()
    rook = Rook()
    knight = Knight()
    bishop = Bishop()
    queen = Queen()
    king = King()

    # Square validator
    sqv = SquareValidator()

    def __init__(self, parent: tk.Tk):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.configure(bg='white', highlightbackground="black",
                       highlightcolor="black", highlightthickness=1)
        self.place(relx=0.25, rely=0.0,
                   relwidth=0.5, relheight=0.75)
        self.board = [[0] * 8 for _ in range(8)]
        self.previous_move = []
        self.moving_img = ''
        self.moving_label: tk.Label = None
        self.last_move_by = 0
        self.flipped = False

        # First entry is tuple representing current position of black king
        # Second entry is tuple representing current position of black king
        # For example, starting positions will be [(7,4), (0,4)]
        self.kings_positions = [0, 0]

        self.king_under_check = [False, False]  # [black_king, white_king]
        self.kings_widgets: list[tk.Label] = [0, 0]  # [black_king, white_king]
        self.checking_pieces = {'b_ki': list[tk.Widget],
                                'w_ki': list[tk.Widget]}

        # self.black_queen_image = ImageTk.PhotoImage(Image.open('.\images\\black_queen.png'))
        # self.black_king_image = ImageTk.PhotoImage(Image.open('.\images\\black_king.png'))
        # self.black_rook_image = ImageTk.PhotoImage(Image.open('.\images\\black_rook.png'))
        # self.black_bishop_image = ImageTk.PhotoImage(Image.open('.\images\\black_bishop.png'))
        # self.black_knight_image = ImageTk.PhotoImage(Image.open('.\images\\black_knight.png'))
        # self.black_pawn_image = ImageTk.PhotoImage(Image.open('.\images\\black_pawn.png'))

        # self.white_queen_image = ImageTk.PhotoImage(Image.open('.\images\\white_queen.png'))
        # self.white_king_image = ImageTk.PhotoImage(Image.open('.\images\\white_king.png'))
        # self.white_rook_image = ImageTk.PhotoImage(Image.open('.\images\\white_rook.png'))
        # self.white_bishop_image = ImageTk.PhotoImage(Image.open('.\images\\white_bishop.png'))
        # self.white_knight_image = ImageTk.PhotoImage(Image.open('.\images\\white_knight.png'))
        # self.white_pawn_image = ImageTk.PhotoImage(Image.open('.\images\\white_pawn.png'))

        self.img_dict = {'b_pa': ImageTk.PhotoImage(Image.open('.\images\\black_pawn.png')),
                         'b_ro': ImageTk.PhotoImage(Image.open('.\images\\black_rook.png')),
                         'b_kn': ImageTk.PhotoImage(Image.open('.\images\\black_knight.png')),
                         'b_bi': ImageTk.PhotoImage(Image.open('.\images\\black_bishop.png')),
                         'b_qu': ImageTk.PhotoImage(Image.open('.\images\\black_queen.png')),
                         'b_ki': ImageTk.PhotoImage(Image.open('.\images\\black_king.png')),
                         'w_pa': ImageTk.PhotoImage(Image.open('.\images\\white_pawn.png')),
                         'w_ro': ImageTk.PhotoImage(Image.open('.\images\\white_rook.png')),
                         'w_kn': ImageTk.PhotoImage(Image.open('.\images\\white_knight.png')),
                         'w_bi': ImageTk.PhotoImage(Image.open('.\images\\white_bishop.png')),
                         'w_qu': ImageTk.PhotoImage(Image.open('.\images\\white_queen.png')),
                         'w_ki': ImageTk.PhotoImage(Image.open('.\images\\white_king.png'))}

        self.tk_focusFollowsMouse()

        self._add_labels()

    def verify_move(self, board_entry: str, square_from: str, square_to: str):
        piece_name = board_entry[2:]
        # if (board_entry[0] == 'b' and self.last_move_by != 1 or
        #         board_entry[0] == 'w' and self.last_move_by != 0):
        #     return False
        if piece_name == 'pa':
            return self.pawn.move(square_from, square_to, self.kings_positions, self.king_under_check, self.board, self.sqv, self.flipped)
        elif piece_name == 'ro':
            return self.rook.move(square_from, square_to, self.kings_positions, self.king_under_check, self.board, self.sqv)
        elif piece_name == 'kn':
            return self.knight.move(square_from, square_to, self.kings_positions, self.king_under_check, self.board, self.sqv)
        elif piece_name == 'bi':
            return self.bishop.move(square_from, square_to, self.kings_positions, self.king_under_check, self.board, self.sqv)
        elif piece_name == 'qu':
            return self.queen.move(square_from, square_to, self.kings_positions, self.king_under_check, self.board, self.sqv)
        elif piece_name == 'ki':
            return self.king.move(square_from, square_to, self.kings_positions, self.king_under_check, self.board, self.sqv)
        else:
            raise ValueError(f"Tried to move unknown piece: {piece_name}.")

    def get_rank_and_file_from_label(self, name: int):
        num = int(name[name.rfind('l')+1:])
        num = num if not num else num - 1
        rank = num // 8
        file = num - (rank * 8)
        return rank, file

    # def get_number_of_label(self, name: str):
    #     try:
    #         return int(name[name.rfind('l')+1:])
    #     except ValueError:
    #         return 1

    def update_previous_move_list(self, w: tk.Widget):
        if len(self.previous_move) == 3:
            for i in range(2):
                self.restore_label_colour(self.previous_move[i])
            self.previous_move = [self.previous_move[2]]
        self.previous_move.append(w)

    def update_king_position(self, last_moved_piece: str, new_position: tuple, widget):
        if last_moved_piece.endswith('ki'):
            if last_moved_piece.startswith('b'):
                self.kings_positions[0] = new_position
                self.kings_widgets[0] = widget
            else:
                self.kings_positions[1] = new_position
                self.kings_widgets[1] = widget

    def show_checked_king(self):
        if self.king_under_check[0]:
            w = self.kings_widgets[0]
            w.configure(bg="red")
            print(w)
        if self.king_under_check[1]:
            w = self.kings_widgets[1]
            w.configure(bg="red")
            print(w)

    def single_click(self, event: tk.Event):
        w = event.widget
        n = str(w)
        rank, file = self.get_rank_and_file_from_label(n)
        # First click
        if self.moving_label is None:

            try:
                self.moving_img = self.img_dict[self.board[rank][file]]
            except KeyError:
                pass
            else:
                if ((self.board[rank][file][0] == 'b' and self.last_move_by != 1) or
                        (self.board[rank][file][0] == 'w' and self.last_move_by != 0)):
                    pass
                else:
                    w.configure(bg=self.clicked_or_released_colour)
                    # self.clicked = True
                    self.previous_move.append(w)
                    self.moving_label = w
        # Second click
        else:
            r2, f2 = self.get_rank_and_file_from_label(str(self.moving_label))
            square_from = self.files[f2] + str(r2+1)
            square_to = f"{self.files[file]}{rank+1}"
            entry = self.board[r2][f2]
            move_valid = self.verify_move(entry, square_from, square_to)
            # if entry[0] == 'b':
            #     move_valid = self.verify_move(entry, self.black_king_position, square_from, square_to)
            # else:
            #     move_valid = self.verify_move(entry, self.white_king_position, square_from, square_to)
            if not move_valid:
                print(
                    f"Invalid move: {entry=},{rank=},{file=},{r2=},{f2=},{self.board[rank][file]}")
                self.previous_move.pop()
                self.restore_label_colour(self.moving_label)
            else:
                print(
                    f"Valid move: {entry=},{rank=},{file=},{r2=},{f2=},{self.board[rank][file]}")
                w.configure(image=self.moving_img,
                            bg=self.clicked_or_released_colour)
                self.board[rank][file] = entry
                self.moving_label.configure(image='')
                self.board[r2][f2] = 0
                # self.clicked = True
                self.update_previous_move_list(w)
                self.update_king_position(entry, (rank, file), w)
                if sum(self.king_under_check):
                    self.show_checked_king()
                self.last_move_by ^= 1
            self.moving_label: tk.Label = None
            self.moving_img = ''

    def restore_label_colour(self, w: tk.Label):
        n = str(w)
        r, f = self.get_rank_and_file_from_label(n)
        w.configure(bg=self.board_colours[(r+f) % 2])

    def enter_focus(self, event: tk.Event):
        w = event.widget
        if w.master == self and w not in self.previous_move:
            if w not in self.kings_widgets or not self.king_under_check[self.kings_widgets.index(w)]:
                # print(f"not a king {str(w)}")
                w.configure(bg='#a7aac4')
            # elif not self.king_under_check[self.kings_widgets.index(w)]:
            #     print(f"a king but not under check {self.king_under_check=}")
            #     w.configure(bg='#a7aac4')

    def leave_focus(self, event: tk.Event):
        w = event.widget
        if w.master == self and w not in self.previous_move:
            if w not in self.kings_widgets or not self.king_under_check[self.kings_widgets.index(w)]:
                self.restore_label_colour(w)

    def _add_labels(self):
        # self.bind_class('Label', '<Double-Button-1>', self.double_click)
        self.bind_class('Label', '<Button-1>', self.single_click)
        self.bind_class('Label', '<Enter>', self.enter_focus)
        self.bind_class('Label', '<Leave>', self.leave_focus)
        prev_colour = 0
        for rank in range(7, -1, -1):
            for file in range(8):
                cell = tk.Label(self, bg=self.board_colours[prev_colour], takefocus=1,
                                compound='top')

                # pawns
                if rank == 1:
                    cell.configure(image=self.img_dict['b_pa'])
                    self.board[7-rank] = ['b_pa'] * 8
                elif rank == 6:
                    cell.configure(image=self.img_dict['w_pa'])
                    self.board[7-rank] = ['w_pa'] * 8
                # rooks
                elif (rank, file) in [(0, 0), (0, 7)]:
                    cell.configure(image=self.img_dict['b_ro'])
                    self.board[7-rank][file] = 'b_ro'
                elif (rank, file) in [(7, 0), (7, 7)]:
                    cell.configure(image=self.img_dict['w_ro'])
                    self.board[7-rank][file] = 'w_ro'
                # knights
                elif (rank, file) in [(0, 1), (0, 6)]:
                    cell.configure(image=self.img_dict['b_kn'])
                    self.board[7-rank][file] = 'b_kn'
                elif (rank, file) in [(7, 1), (7, 6)]:
                    cell.configure(image=self.img_dict['w_kn'])
                    self.board[7-rank][file] = 'w_kn'
                # bishops
                elif (rank, file) in [(0, 2), (0, 5)]:
                    cell.configure(image=self.img_dict['b_bi'])
                    self.board[7-rank][7-file] = 'b_bi'
                elif (rank, file) in [(7, 2), (7, 5)]:
                    cell.configure(image=self.img_dict['w_bi'])
                    self.board[7-rank][7-file] = 'w_bi'
                # queens
                elif (rank, file) == (0, 3):
                    cell.configure(image=self.img_dict['b_qu'])
                    self.board[7-rank][file] = 'b_qu'
                elif (rank, file) == (7, 3):
                    cell.configure(image=self.img_dict['w_qu'])
                    self.board[7-rank][file] = 'w_qu'
                # kings
                elif (rank, file) == (0, 4):
                    cell.configure(image=self.img_dict['b_ki'])
                    self.board[7-rank][file] = 'b_ki'
                    self.kings_positions[0] = (7, 4)
                    self.kings_widgets[0] = cell
                elif (rank, file) == (7, 4):
                    cell.configure(image=self.img_dict['w_ki'])
                    self.board[7-rank][file] = 'w_ki'
                    self.kings_positions[1] = (0, 4)
                    self.kings_widgets[1] = cell

                cell.place(relx=file * SQUARE_RATIO, rely=rank * SQUARE_RATIO,
                           relheight=SQUARE_RATIO, relwidth=SQUARE_RATIO)
                if file < 7:
                    prev_colour = prev_colour ^ 1

        # print(*self.board[0], sep='\n')
