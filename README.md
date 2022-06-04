# Chess game

(To be updated)
A desktop-based chess game. GUI made with python's tkinter library. 

## Usage

To see the application in action, run the `main.py` file.

`flip board` changes the orientation of the board.

`new game` builds a new game instance.

You can play against a very unintelligent computer that makes the most random moves. You can also play against yourself (i.e., playing as both black and white). To do this, comment out `self.get_computer_move()` in the last line of the `handle_second_click` method of `board.py`. Currently, computer plays as black. You can change this to white by passing `"white"` and `self.white_active_pieces` when initializing `Computer` in the last line of the `reset_labels` method in `board.py`.

## Some current issues
- There's cleanup to be done on the code.
- Checkmates and stalemates are only printed to the terminal for now. So you won't see it on the board (apart from the fact that you won't be able to move any piece unless you restart the game).
- There's as of yet no ability to undo a move.
- You can't yet play against a human opponent on another machine.
