import tkinter as tk

SQUARE_RATIO = 1/8


class BoardRanks(tk.Frame):
    def __init__(self, parent: tk.Tk):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.place(relx=0.225, rely=0.0, relheight=0.75, relwidth=0.025)
        self.temp_children = {}

    def display_ranks(self):
        for x in range(8):
            cell = tk.Label(self, bg='#4a390a', text=str(8-x),
                            font=('Arial', 10, 'italic'))
            cell.place(relheight=SQUARE_RATIO,
                       relwidth=1.0, rely=x*SQUARE_RATIO)
        self.temp_children = self.children
    
    def reset_variables(self):
        if self.temp_children:
            self.children = self.temp_children
            for i in range(8):
                name = '!label' if not i else f'!label{i+1}'
                self.children[name].configure(bg='#4a390a', text=str(8-i),
                            font=('Arial', 10, 'italic'))
        else:
            self.display_ranks()


class BoardFiles(tk.Frame):
    def __init__(self, parent: tk.Tk):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.place(relx=0.25, rely=0.75, relheight=0.025, relwidth=0.5)
        self.ranks = list('ABCDEFGH')
        self.temp_children = {}
        pcs = {'R':'♜', 'N':'♞', 'B':'♝', 'Q':'♛', 'K':'♚', 'P':'♟',
                  'r':'♖', 'n':'♘', 'b':'♗', 'q':'♕', 'k':'♔', 'p':'♙', '.':'·'}
        
    def display_files(self):
        for x in range(8):
            cell = tk.Label(self, bg='#4a390a', text=self.ranks[x])
            cell.place(relheight=1.0, relwidth=SQUARE_RATIO,
                       relx=x*SQUARE_RATIO)
        self.temp_children = self.children
    
    def reset_variables(self):
        if self.temp_children:
            self.children = self.temp_children
            for i in range(8):
                name = '!label' if not i else f'!label{i+1}'
                self.children[name].configure(bg='#4a390a', text=self.ranks[i]) 
        else:
            self.display_files()
