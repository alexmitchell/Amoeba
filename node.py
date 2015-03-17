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

    def set_left(self, node):
        self.left_node = node

    def set_right(self, node):
        self.right_node = node

    def draw(self):
        self.draw_dot_function(self)

    def activate(self):
        self.state='active'

    def deactivate(self):
        self.state='inactive'

    def move(self, delta):
        self.position += delta
