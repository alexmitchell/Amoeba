from vecrec import Vector

def pass_function(*args_to_be_ignored):
    pass

class Node:
    id = 0
    def __init__(self, position, draw_dot_function=pass_function, state='inactive'):
        self.id = Node.id
        Node.id += 1

        self.position = position
        self.state = state
        self.draw_dot_function = draw_dot_function

        self.left_node = None
        self.right_node = None

    def draw(self):
        x, y = self.position.tuple
        self.draw_dot_function(x, y, self.state)

