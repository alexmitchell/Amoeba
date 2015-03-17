from vecrec import Vector
from node import Node

class Shape:
    def __init__(self, center_x, center_y, draw_dot_function, length_scale):
        self.draw_dot_function = draw_dot_function
        self.length_scale = length_scale
        self.init_center = Vector(center_x, center_y)

        self.perimeter_nodes = []

    def generate_init_box(self, nx, ny):
        """ Create a nx by ny box of dots as the initial shape. The
        distance between nodes is set by self.length_scale. The nodes
        will be added to self.perimeter_nodes in sequence. (ie. 
        perimeter_node[0] is left of perimeter_node[1] and so on...) """
        center = self.init_center
        dx = 3 * Vector(self.length_scale, 0)
        dy = 3 * Vector(0, self.length_scale)

        # Calculate the bottom left corner of the box
        position = center - (nx-1) / 2 * dx - (ny-1) / 2 * dy

        # Create left edge (bottom left corner is made later)
        for i in range(ny-1):
            position += dy
            self.create_perimeter_node(position.copy())

        # Create top edge (top left corner is already made)
        for i in range(nx-1):
            position += dx
            self.create_perimeter_node(position.copy())

        # Create right edge (top right corner is already made)
        for i in range(ny-1):
            position -= dy
            self.create_perimeter_node(position.copy())

        # Create bottom edge (bottom right corner is already made)
        for i in range(nx-1):
            position -= dx
            self.create_perimeter_node(position.copy())

        self.link_perimeter_nodes()

    def create_perimeter_node(self, position):
        """ Create a new node and add it to self.perimeter_nodes. """
        draw_function = self.draw_dot_function
        node = Node(position, draw_function)
        self.perimeter_nodes.append(node)

    def link_perimeter_nodes(self):
        """ Link the perimeter nodes together. This function assumes
        the nodes are in order in the self.perimeter_nodes list. """
        first = None
        previous = None
        for node in self.perimeter_nodes:
            if first is None:
                first = node
                previous = node
                continue
            node.set_left(previous)
            previous.set_right(node)

            previous = node

        first.set_left(previous)
        previous.set_right(first)
            
    def draw(self):
        for node in self.perimeter_nodes:
            node.draw()
