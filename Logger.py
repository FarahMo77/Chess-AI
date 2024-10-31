from itertools import groupby

"""
code defines a metaclass called Singleton. A metaclass is a class that defines the behavior of other classes.
in this case, the Singleton metaclass ensures that only one instance of a class is created.
Here's how it works:
* The _instances class variable is a dictionary that keeps track of the instances of the class that have been created so far.
  It is defined as a class variable, so it is shared by all instances of the class.
* The __call__ method is called when an instance of the class is created. It takes the class (cls) as its first argument, 
  followed by any arguments (*args) and keyword arguments (**kwargs) that were passed to the class constructor.
* The if cls not in cls._instances line checks if an instance of the class has already been created. If not,
  it creates a new instance of the class using the super() function and stores it in the _instances dictionary.
* The return cls._instances[cls] line returns the instance of the class that was just created or retrieved from the _instances dictionary.
  By using this metaclass, any class that inherits from it will only ever have one instance created.
  This can be useful in situations where you want to ensure that there is only one instance of a class, such as a database connection or a configuration object.
"""


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



#A class that represents a board state with its array representation, depth, and evaluation.

class BoardRepr:
    """
     Initializes a new BoardRepr object with the given array representation, depth, and evaluation.
     Args:
        - array_repr (list): The array representation of the board state.
        - depth (int): The depth of the board state in the minimax tree.
        - evaluation (int): The evaluation score of the board state.
    """

    def __init__(self, array_repr, depth, evaluation):
        self.array_repr = array_repr
        self.depth = depth
        self.eval = evaluation

    """
    Returns an iterator over the array representation of the board state.
    Returns:
          - iterator: An iterator over the array representation of the board state.
    """

    def __iter__(self):
        return self.array_repr

    """
    Returns a string representation of the board state.
    Returns:
           - str: A string representation of the board state.
    """

    def __str__(self):
        return str(self.array_repr)

    """
    Returns the item at the given index in the array representation of the board state.
    Args:
        - item (int): The index of the item to return.
    Returns:
        - list: The item at the given index in the array representation of the board state.
    """

    def __getitem__(self, item):
        if item == len(self.array_repr) - 1:
            return self.array_repr[item] + [" depth:{}|eval:{}]\t".format(self.depth, self.eval)]
        return self.array_repr[item] + ["\t\t\t\t\t"]

    """
    Returns a string representation of the depth of the board state.
    Returns:
           - str: A string representation of the depth of the board state.
    """

    def __repr__(self):
        return str(self.depth)



#A class that logs the board states in the minimax tree to a file(minimax_tree.txt).
class Logger(metaclass=Singleton):
    log_file = 'minimax_tree.txt'

    # Initializes a new Logger object with an empty list of board states.
    def __init__(self):
        self.arr = []

    """
    Appends the given board state to the list of board states, sorted by depth.
    Args:
        - item (BoardRepr): The board state to append.
    """
    def append(self, item: BoardRepr):
        for idx, it in enumerate(self.arr):
            if it.depth == item.depth and idx < len(self.arr) - 1:
                if self.arr[idx + 1].depth < item.depth:
                    self.arr = self.arr[:idx] + [item] + self.arr[idx:]
                    return
        self.arr.append(item)

    # Clears the list of board states and deletes the log file.
    def clear(self):
        open(self.log_file, 'w').close()
        self.arr.clear()

    """
  * The with open(self.log_file, 'a', encoding='utf-8') as f: line opens the log file in append mode ('a') and 
    sets the encoding to UTF-8. The with statement ensures that the file is closed properly when the block is exited.
  * The for i, g in groupby(self.arr, key=lambda x: x.depth): line groups the board states in self.arr by their depth 
    attribute using the groupby function from the itertools module.This creates a sequence of (key, group) pairs,
    where key is the depth value and group is an iterator over the board states with that depth.
  * The board_repr = list((k for k in g)) line converts the group iterator to a list of BoardRepr objects.
  * The for idx, _ in enumerate(board_repr[0].array_repr): line loops over the rows of the board represented by the
    first BoardRepr object in board_repr.The _ variable is used to ignore the row index.
  * The for item in board_repr: line loops over the BoardRepr objects in board_repr.
  * The f.write(''.join(list(i for i in item[idx]))) line writes the characters in the idx-th column of the board for
    the current BoardRepr object to the log file.
  * The f.write("\n") line writes a newline character to the log file after each row of the board.
  * The f.write("\n") line writes an extra newline character to the log file after each group of board states with the same depth.
    Overall, this method writes the board states in self.arr to the log file in a tabular format, with each row representing a board
    state and each column representing a cell on the board. The board states are grouped by their depth,
    and an extra newline character is added between groups for readability.
    """
    def write(self):
        with open(self.log_file, 'a', encoding='utf-8') as f:
            for i, g in groupby(self.arr, key=lambda x: x.depth):
                board_repr = list((k for k in g))
                for idx, _ in enumerate(board_repr[0].array_repr):
                    for item in board_repr:
                        f.write(''.join(list(i for i in item[idx])))
                    f.write("\n")
                f.write("\n")
