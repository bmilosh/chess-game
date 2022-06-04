import tkinter as tk

from PIL import Image, ImageTk

from model.checkmate_checker import CheckmateChecker
from model.computer import Computer
from model.legal_moves_getter import LegalMovesGetter
from model.pieces.bishop import Bishop
from model.pieces.king import King
from model.pieces.knight import Knight
from model.pieces.pawn import Pawn
from model.pieces.queen import Queen
from model.pieces.rook import Rook
from model.square_validator import SquareValidator

SQUARE_RATIO = 1 / 8


class Board(tk.Frame):
    # Colours
    board_colours1 = ["#4a390a", "#ebd086"]  # 918051
    board_colours = ["#4f462c", "#ebd086"]
    available_moves_colours = ["#cee0d3", "#cae8d2"]
    focus_colour = "#ebd086"
    clicked_or_released_colour = ["#ded3b1", "#d9d2bf"]
    clicked_colour = "#818399"
    moved_colours = []
    pcs = {
        "R": "♜",
        "N": "♞",
        "B": "♝",
        "Q": "♛",
        "K": "♚",
        "P": "♟",
        "r": "♖",
        "n": "♘",
        "b": "♗",
        "q": "♕",
        "k": "♔",
        "p": "♙",
        ".": "·",
    }

    files = ["a", "b", "c", "d", "e", "f", "g", "h"]  # list('abcdefgh')

    # Square validator
    sqv = SquareValidator()

    ################################################
    ################ Init methods ##################
    ################################################

    def __init__(self, parent: tk.Tk):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.configure(
            bg="white",
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
        )
        self.place(relx=0.25, rely=0.0, relwidth=0.5, relheight=0.75)
        self.temp_children = {}
        self.temp_board = []
        self.white_active_pieces = []
        self.black_active_pieces = []

        self.img_dict = {
            "black pawn": ImageTk.PhotoImage(Image.open(".\images\\black_pawn.png")),
            "black rook": ImageTk.PhotoImage(Image.open(".\images\\black_rook.png")),
            "black knight": ImageTk.PhotoImage(
                Image.open(".\images\\black_knight.png")
            ),
            "black bishop": ImageTk.PhotoImage(
                Image.open(".\images\\black_bishop.png")
            ),
            "black queen": ImageTk.PhotoImage(Image.open(".\images\\black_queen.png")),
            "black king": ImageTk.PhotoImage(Image.open(".\images\\black_king.png")),
            "white pawn": ImageTk.PhotoImage(Image.open(".\images\\white_pawn.png")),
            "white rook": ImageTk.PhotoImage(Image.open(".\images\\white_rook.png")),
            "white knight": ImageTk.PhotoImage(
                Image.open(".\images\\white_knight.png")
            ),
            "white bishop": ImageTk.PhotoImage(
                Image.open(".\images\\white_bishop.png")
            ),
            "white queen": ImageTk.PhotoImage(Image.open(".\images\\white_queen.png")),
            "white king": ImageTk.PhotoImage(Image.open(".\images\\white_king.png")),
            0: "",
        }

        self.tk_focusFollowsMouse()
        self.reset_variables()

    def reset_variables(self):
        self.board = [[0] * 8 for _ in range(8)]
        self.previous_move = []
        self.legal_moves = []
        self.moving_img = ""
        self.moving_label: tk.Label = None
        self.last_move_by = 0
        self.last_moved_pawn: Pawn = None
        self.flipped = False
        self.castling_options = {
            "white king": True,
            "black king": True,
            (0, 0): True,
            (0, 7): True,
            (7, 0): True,
            (7, 7): True,
        }

        # First entry is tuple representing current position of black king
        # Second entry is tuple representing current position of black king
        # For example, starting positions will be [(7,4), (0,4)]
        self.kings_positions = [0, 0]

        self.king_under_check = [False, False]  # [black_king, white_king]
        self.kings_widgets: list[tk.Label] = [0, 0]  # [black_king, white_king]
        self.checking_pieces = {"black": [], "white": []}
        self.reset_labels()

    def reset_labels(self):
        if self.temp_board:
            self.board = [list(itm) for itm in self.temp_board]
            self.white_active_pieces = list(self.temp_wap)
            self.black_active_pieces = list(self.temp_bap)
            self.children = {k: v for k, v in self.temp_children.items()}
            self.kings_positions = [(7, 4), (0, 4)]
            self.kings_widgets: list[tk.Label] = [
                self.children["!label61"],
                self.children["!label5"],
            ]
            self.reconfigure_labels()
            for r in range(8):
                for f in range(8):
                    # Reset piece rank and file attributes
                    if self.board[r][f]:
                        self.board[r][f].rank, self.board[r][f].file = r, f
                    # Reset castling priviledges
                    if (r, f) in [(0, 0), (0, 7), (7, 0), (7, 7), (0, 4), (7, 4)]:
                        self.board[r][f].can_castle = True
        else:
            self._add_labels()

        self.mate_checker = CheckmateChecker()
        self.computer = Computer("black", self.black_active_pieces)

    def reconfigure_labels(self):
        for r in range(8):
            for f in range(8):
                name = self.get_label_from_rank_and_file(r, f)
                try:
                    img_key = self.board[r][f].colour + " " + self.board[r][f].name
                except AttributeError:
                    img_key = 0
                col = self.board_colours[(r + f) % 2]
                self.children[name].configure(bg=col, image=self.img_dict[img_key])

    ################################################
    ################ Setter methods ################
    ################################################

    def update_active_pieces(
        self, rank, file, promoted_piece=None, rank_from=None, file_from=None
    ):
        """
        Called before updating the board.
        Only called when the move is legal."""
        p = self.board[rank][file]
        if p and promoted_piece is None:
            active_pieces = self.get_active_pieces(p.colour, True)
            active_pieces.remove(p)
        if promoted_piece is not None:
            print(f"we're promoting?? {promoted_piece=}")
            active_pieces = self.get_active_pieces(promoted_piece.colour, True)
            active_pieces.append(promoted_piece)
            active_pieces.remove(self.board[rank_from][file_from])

    def update_board(
        self, w: tk.Widget, rank, file, rank_from, file_from, last_moved_piece
    ):
        if (
            self.last_moved_pawn is not None
            and last_moved_piece.name == "pawn"
            and rank_from == self.last_moved_pawn.rank
            and abs(self.last_moved_pawn.file - file_from) == 1
            and file == self.last_moved_pawn.file
            and abs(rank - self.last_moved_pawn.rank) == 1
        ):
            # Last move was an en passant. Hence, we make sure to
            # remove the "captured" piece from display and also from
            # the list representation of the board.
            # For this to work correctly, it is essential that it is
            # done before calling the update_last_moved_pawn method.
            passanted_lab = self.get_label_from_rank_and_file(
                self.last_moved_pawn.rank, self.last_moved_pawn.file
            )
            passanted_wid = self.children[passanted_lab]
            passanted_wid.configure(image="")
            self.board[self.last_moved_pawn.rank][self.last_moved_pawn.file] = 0

        if rank in [0, 7] and last_moved_piece.name == "pawn":
            # Handles promotion (to queen for now)
            # last_moved_piece.colour + '_queen'
            last_moved_piece = Queen(colour=last_moved_piece.colour)
            last_moved_piece.rank, last_moved_piece.file = rank, file
            self.update_active_pieces(
                rank,
                file,
                promoted_piece=last_moved_piece,
                rank_from=rank_from,
                file_from=file_from,
            )
            img_key = f"{last_moved_piece.colour} queen"
            w.configure(image=self.img_dict[img_key])  # ,
            # bg=self.clicked_or_released_colour[(rank+file) % 2])
        else:
            w.configure(image=self.moving_img)  # ,
            # bg=self.clicked_or_released_colour[(rank+file) % 2])
        self.board[rank][file] = last_moved_piece
        self.moving_label.configure(image="")
        self.board[rank_from][file_from] = 0

    def update_castling_options(
        self, sq_frm_rnk, sq_frm_fil, sq_to_rnk, sq_to_fil, last_moved_piece
    ):
        """
        Called only if the move is valid"""
        if last_moved_piece.name == "king":
            # Works as long as the castling rights are correctly updated
            r_diff = sq_frm_rnk - sq_to_rnk
            f_diff = sq_frm_fil - sq_to_fil
            if abs(r_diff) == 0 and abs(f_diff) == 2:
                # we're castling, and the move has already been validated to be correct,
                # so we need to display this move on the board
                self.display_castle(sq_frm_rnk, sq_to_fil, f_diff, last_moved_piece)
            else:
                last_moved_piece.can_castle = False

    def update_previous_move_list(self, w: tk.Widget):
        self.previous_move.append(w)
        end = 2 if len(self.previous_move) == 4 else 0
        for i in range(end):
            # Restore their original colour
            self.restore_label_colour(self.previous_move[i])
        for j in range(end, len(self.previous_move)):
            # Give it a clicked_or_released colour
            self.restore_label_colour(self.previous_move[j], previous=True)
        self.previous_move = self.previous_move[end:]

    def update_king_position(self, last_moved_piece: str, new_position: tuple, widget):
        if last_moved_piece.name == "king":
            king_idx = 0 if last_moved_piece.colour == "black" else 1
            # Assumes that the previous king move was valid.
            self.restore_label_colour(self.kings_widgets[king_idx], True)
            self.kings_positions[king_idx] = new_position
            self.kings_widgets[king_idx] = widget

    def update_last_moved_pawn(self, last_moved_piece):
        if isinstance(last_moved_piece, Pawn):
            self.last_moved_pawn = last_moved_piece
        else:
            self.last_moved_pawn = None

    def do_updates(self, w: tk.Widget, rank_to, file_to, rank_from, file_from, entry):
        """
        The order in which these updates are done is important.
        In some cases, an update works on the assumption that
        a particular update has not yet been carried out.
        Hence, changing this order could result in a malfunction.
        """
        self.update_active_pieces(rank_to, file_to)
        self.update_board(w, rank_to, file_to, rank_from, file_from, entry)
        self.update_castling_options(rank_from, file_from, rank_to, file_to, entry)
        self.update_previous_move_list(w)
        self.update_king_position(entry, (rank_to, file_to), w)
        self.update_last_moved_pawn(entry)

    ################################################
    ################ Getter methods ################
    ################################################

    def get_active_pieces(self, colour, same_colour=False):
        if same_colour:
            return (
                self.black_active_pieces
                if colour == "black"
                else self.white_active_pieces
            )
        return (
            self.black_active_pieces if colour == "white" else self.white_active_pieces
        )

    def get_legal_moves(self, board_entry):
        active_pieces = self.get_active_pieces(board_entry.colour)
        self.legal_moves = board_entry.get_legal_moves(
            self.kings_positions,
            self.checking_pieces,
            self.board,
            flipped=self.flipped,
            king_under_check=self.king_under_check,
            opp_active_pieces=active_pieces,
            last_moved_pawn=self.last_moved_pawn,
        )

    def get_rank_and_file_from_label(self, name: int):
        try:
            num = int(name[name.rfind("l") + 1 :])
        except ValueError:
            num = 1
        num -= 1
        rank = (num // 8) % 8
        file = (num - (rank * 8)) % 8
        return rank, file

    def get_label_from_rank_and_file(self, rank, file) -> str:
        if not rank and not file:
            return "!label"
        return f"!label{(rank*8) + file + 1}"

    def get_computer_move(self):
        move = self.computer.make_move(
            self.kings_positions,
            self.checking_pieces,
            self.board,
            self.flipped,
            self.king_under_check,
            self.white_active_pieces,
        )
        if move:
            print(f"Valid computer move: {move = }")
            self.show_computer_move(move)
        else:
            print(f"Invalid computer move: {move = }")

    #################################################
    ################ Show-er methods ################
    #################################################

    def show_computer_move(self, move: tuple):
        piece, new_pos = move
        old_lab = self.get_label_from_rank_and_file(piece.rank, piece.file)
        new_lab = self.get_label_from_rank_and_file(*new_pos)
        n = piece.colour + " " + piece.name

        self.moving_img = self.img_dict[n]
        self.moving_label = self.children[old_lab]

        old_widget = self.children[old_lab]
        self.previous_move.append(old_widget)
        # old_widget.configure(image='')
        new_widget = self.children[new_lab]
        # new_widget.configure(image=img)
        # self.board[piece.rank][piece.file] = 0
        # self.board[new_pos[0]][new_pos[1]] = piece

        self.do_updates(new_widget, *new_pos, piece.rank, piece.file, piece)

        self.show_checked_king()
        self.show_unchecked_king()

        piece.rank, piece.file = new_pos

        self.last_move_by ^= 1
        self.moving_img = ""
        self.moving_label = None

    def show_legal_moves(self):
        for r, f in self.legal_moves:
            lab = self.get_label_from_rank_and_file(r, f)
            w = self.children[lab]
            w.configure(bg=self.available_moves_colours[(r + f) % 2])

    def unshow_legal_moves(self):
        for r, f in self.legal_moves:
            lab = self.get_label_from_rank_and_file(r, f)
            w = self.children[lab]
            if w in self.previous_move:
                self.restore_label_colour(w, True)
            else:
                self.restore_label_colour(w)

    def show_mate(self, king: King, active_pieces: list, colour):
        opp_active_pieces = self.get_active_pieces(colour)
        mate = self.mate_checker.is_checkmate(
            king,
            self.checking_pieces,
            active_pieces,
            self.kings_positions,
            self.king_under_check,
            colour,
            self.board,
            opp_active_pieces,
            self.flipped,
            self.last_moved_pawn,
        )
        if mate:
            print(
                "**************** There's a checkmate on the board!!! ****************"
            )

    def show_checked_king(self):
        # if self.king_under_check[self.last_move_by]:
        #     col = "white" if self.last_move_by else "black"
        #     ap = self.get_active_pieces(col, True)
        #     king = self.board[self.kings_positions[self.last_move_by][0]][
        #         self.kings_positions[self.last_move_by][1]
        #     ]
        #     self.show_mate(king, ap, col)
        #     w = self.kings_widgets[self.last_move_by]
        #     w.configure(bg="red")
        #     print(w, "is under check")
        if self.king_under_check[0]:
            king = self.board[self.kings_positions[0][0]][self.kings_positions[0][1]]
            self.show_mate(king, self.black_active_pieces, "black")
            w = self.kings_widgets[0]
            w.configure(bg="red")
            print(w, "is under check")
        if self.king_under_check[1]:
            king = self.board[self.kings_positions[1][0]][self.kings_positions[1][1]]
            self.show_mate(king, self.white_active_pieces, "white")
            w = self.kings_widgets[1]
            w.configure(bg="red")
            print(w, "is under check")

    def show_unchecked_king(self):
        if not self.king_under_check[self.last_move_by ^ 1]:
            self.restore_label_colour(self.kings_widgets[self.last_move_by ^ 1])

    def display_castle(self, sq_frm_rnk, sq_to_fil, f_diff, last_moved_piece):
        new_rook_file, file = (sq_to_fil + 1, 0) if f_diff > 0 else (sq_to_fil - 1, 7)
        old_rook_lab = self.get_label_from_rank_and_file(sq_frm_rnk, file)
        new_rook_lab = self.get_label_from_rank_and_file(sq_frm_rnk, new_rook_file)
        rook = last_moved_piece.colour + " rook"
        self.children[old_rook_lab].configure(image="")
        self.children[new_rook_lab].configure(image=self.img_dict[rook])
        self.board[sq_frm_rnk][new_rook_file], self.board[sq_frm_rnk][file] = (
            self.board[sq_frm_rnk][file],
            0,
        )
        self.board[sq_frm_rnk][new_rook_file].can_castle = False
        self.board[sq_frm_rnk][new_rook_file].file = new_rook_file
        last_moved_piece.can_castle = False

    ################################################
    ################ Click handlers ################
    ################################################

    def single_click(self, event: tk.Event):
        w = event.widget
        n = str(w)
        rank, file = self.get_rank_and_file_from_label(n)
        if self.moving_label is None:
            self.handle_first_click(rank, file, w)
        else:
            self.handle_second_click(rank, file, w)

    def handle_first_click(self, rank, file, w):
        try:
            p = self.board[rank][file]
            self.moving_img = self.img_dict[f"{p.colour} {p.name}"]
        except AttributeError:
            pass
        if not self.moving_img:
            pass
        else:
            if not self.board[rank][file] or (
                (self.board[rank][file].colour == "black" and self.last_move_by != 1)
                or (self.board[rank][file].colour == "white" and self.last_move_by != 0)
            ):
                # self.unshow_legal_moves()
                self.legal_moves.clear()
            else:
                self.get_legal_moves(p)
                self.show_legal_moves()
                w.configure(bg=self.clicked_colour)
                self.previous_move.append(w)
                self.moving_label = w

    def handle_second_click(self, rank, file, w):
        r2, f2 = self.get_rank_and_file_from_label(str(self.moving_label))
        square_from = self.files[f2] + str(r2 + 1)
        square_to = f"{self.files[file]}{rank+1}"
        entry = self.board[r2][f2]
        move_valid = self.verify_move(entry, square_from, square_to)
        if not move_valid:
            # print(
            #     f"Invalid move: {entry=},{rank=},{file=},{r2=},{f2=},{self.board[rank][file]}")
            if self.previous_move:
                self.previous_move.pop()
            self.restore_label_colour(self.moving_label)
            self.unshow_legal_moves()
            self.legal_moves.clear()
            self.handle_first_click(rank, file, w)

        else:
            # print(
            #     f"Valid move: {entry=},{rank=},{file=},{r2=},{f2=},{self.board[rank][file]}")
            self.do_updates(w, rank, file, r2, f2, entry)
            self.show_checked_king()
            self.show_unchecked_king()
            self.last_move_by ^= 1
            ##########
            # Doing this here in case we eventually bypass the move methods
            # of the pieces. If so, will also need to update checks differently.
            entry.rank, entry.file = rank, file

            self.moving_label: tk.Label = None
            self.moving_img = ""
            self.unshow_legal_moves()
            self.legal_moves.clear()

            # # Toggle this to play against the computer
            # self.get_computer_move()

    ################################################
    ################ Focus handlers ################
    ################################################

    def enter_focus(self, event: tk.Event):
        w = event.widget
        r, f = self.get_rank_and_file_from_label(str(w))
        if (
            w.master == self
            and w not in self.previous_move
            and (r, f) not in self.legal_moves
        ):
            if (
                w not in self.kings_widgets
                or not self.king_under_check[self.kings_widgets.index(w)]
            ):
                w.configure(bg="#a7aac4")

    def leave_focus(self, event: tk.Event):
        w = event.widget
        r, f = self.get_rank_and_file_from_label(str(w))
        if (
            w.master == self
            and w not in self.previous_move
            and (r, f) not in self.legal_moves
        ):
            if (
                w not in self.kings_widgets
                or not self.king_under_check[self.kings_widgets.index(w)]
            ):
                self.restore_label_colour(w)

    ########################################
    ################ Others ################
    ########################################

    def verify_move(self, board_entry: str, square_from: str, square_to: str):
        ap = self.get_active_pieces(board_entry.colour)
        return board_entry.move(
            square_from,
            square_to,
            self.kings_positions,
            self.king_under_check,
            self.board,
            self.sqv,
            flipped=self.flipped,
            checking_pieces=self.checking_pieces,
            last_moved_pawn=self.last_moved_pawn,
            opp_active_pieces=ap,
            queen_move=None,
        )

    def restore_label_colour(self, w: tk.Label, previous=False):
        n = str(w)
        r, f = self.get_rank_and_file_from_label(n)
        if (
            w in self.kings_widgets
            and self.king_under_check[self.kings_widgets.index(w)]
        ):
            self.show_checked_king()
        elif w in self.previous_move and previous:
            w.configure(bg=self.clicked_or_released_colour[(r + f) % 2])
        else:
            w.configure(bg=self.board_colours[(r + f) % 2])

    def _add_labels(self):
        # self.bind_class('Label', '<Double-Button-1>', self.double_click)
        self.bind_class("Label", "<Button-1>", self.single_click)
        self.bind_class("Label", "<Enter>", self.enter_focus)
        self.bind_class("Label", "<Leave>", self.leave_focus)
        prev_colour = 0
        for rank in range(7, -1, -1):
            for file in range(8):
                cell = tk.Label(
                    self,
                    bg=self.board_colours[prev_colour],
                    takefocus=1,
                    compound="top",
                )

                # pawns
                if rank == 1:
                    self.board[7 - rank][file] = Pawn(colour="black")
                elif rank == 6:
                    self.board[7 - rank][file] = Pawn(colour="white")
                # rooks
                elif (rank, file) in [(0, 0), (0, 7)]:
                    self.board[7 - rank][file] = Rook(colour="black")
                elif (rank, file) in [(7, 0), (7, 7)]:
                    self.board[7 - rank][file] = Rook(colour="white")
                # knights
                elif (rank, file) in [(0, 1), (0, 6)]:
                    self.board[7 - rank][file] = Knight(colour="black")
                elif (rank, file) in [(7, 1), (7, 6)]:
                    self.board[7 - rank][file] = Knight(colour="white")
                # bishops
                elif (rank, file) in [(0, 2), (0, 5)]:
                    self.board[7 - rank][file] = Bishop(colour="black")
                elif (rank, file) in [(7, 2), (7, 5)]:
                    self.board[7 - rank][file] = Bishop(colour="white")
                # queens
                elif (rank, file) == (0, 3):
                    self.board[7 - rank][file] = Queen(colour="black")
                elif (rank, file) == (7, 3):
                    self.board[7 - rank][file] = Queen(colour="white")
                # kings
                elif (rank, file) == (0, 4):
                    self.board[7 - rank][file] = King(colour="black")
                    self.kings_positions[0] = (7, 4)
                    self.kings_widgets[0] = cell
                elif (rank, file) == (7, 4):
                    self.board[7 - rank][file] = King(colour="white")
                    self.kings_positions[1] = (0, 4)
                    self.kings_widgets[1] = cell

                if self.board[7 - rank][file]:
                    img_name = (
                        self.board[7 - rank][file].colour
                        + " "
                        + self.board[7 - rank][file].name
                    )
                    cell.configure(image=self.img_dict[img_name])
                    self.board[7 - rank][file].rank, self.board[7 - rank][file].file = (
                        7 - rank,
                        file,
                    )
                    if (
                        self.board[7 - rank][file].colour == "white"
                        and self.board[7 - rank][file] not in self.white_active_pieces
                    ):
                        self.white_active_pieces.append(self.board[7 - rank][file])
                    elif (
                        self.board[7 - rank][file].colour == "black"
                        and self.board[7 - rank][file] not in self.black_active_pieces
                    ):
                        self.black_active_pieces.append(self.board[7 - rank][file])

                cell.place(
                    relx=file * SQUARE_RATIO,
                    rely=rank * SQUARE_RATIO,
                    relheight=SQUARE_RATIO,
                    relwidth=SQUARE_RATIO,
                )
                if file < 7:
                    prev_colour = prev_colour ^ 1

        self.temp_children = {k: v for k, v in self.children.items()}
        self.temp_board = [list(itm) for itm in self.board]
        self.temp_wap = list(self.white_active_pieces)
        self.temp_bap = list(self.black_active_pieces)
