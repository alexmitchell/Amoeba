from vecrec import Vector
from node import Node

class Shape:
    def __init__(self, center_x, center_y, draw_dot_function, length_scale):
        self.draw_dot_function = draw_dot_function
        self.length_scale = length_scale

        self.max_link_length = 4.5 * length_scale
        self.min_link_length = 1.5 * length_scale
        self.std_link_length = (self.max_link_length + self.min_link_length)/2
        self.init_center = Vector(center_x, center_y)

        self.perimeter_nodes = []
        self.active_nodes = []
        self.number_to_activate = 4

    # Setup
    def generate_init_box(self, nx, ny):
        """ Create a nx by ny box of dots as the initial shape. The
        distance between nodes is set by self.length_scale. The nodes
        will be added to self.perimeter_nodes in sequence. (ie. 
        perimeter_node[0] is left of perimeter_node[1] and so on...) """
        center = self.init_center
        dx = Vector(self.std_link_length, 0)
        dy = Vector(0, self.std_link_length)

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
        x,y = position.tuple
        position.x = round(x)
        position.y = round(y)
        node = Node(position, draw_function)
        self.perimeter_nodes.append(node)
        return node

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
            


    # Node activation methods
    def activate_closest_nodes(self, click):
        n_activate = self.number_to_activate
        candidate_magnitudes = {}

        # Make sure the activation list is empty
        self.deactivate_nodes()

        # Find the closest nodes to the mouse click!
        for node in self.perimeter_nodes:
            distance = click - node.position
            node_magnitude = distance.magnitude_squared

            # Candidates list is empty, add the node to the activation 
            # list.
            if not self.active_nodes:
                self.active_nodes.append(node)
                candidate_magnitudes[node] = node_magnitude
                continue

            # Place the new node on the activation list if the distance 
            # is short enough.
            self.add_activation_candidate(node, node_magnitude, candidate_magnitudes)

            # Trim the activation list if necessary.
            if len(self.active_nodes) > n_activate:
                # The activation list is too long, remove the last 
                # (farthest) candidate from the list.
                try:
                    last = self.active_nodes.pop()
                    del candidate_magnitudes[last]
                except KeyError:
                    ids = [pnode.id for pnode in self.active_nodes]
                    print("Active nodes list too long (",len(self.active_nodes), ")")
                    print(" list = ", ids)
                    print(" list = ", self.active_nodes)
                    print(" mags = ", candidate_magnitudes)
                    print(" popped: ", last)
                    raise KeyError
        
        # Clean up activation list
        self.clean_activation_list()

        # Activate the nodes
        for node in self.active_nodes:
            node.activate()
                
    def add_activation_candidate(self, node, node_magnitude, candidate_magnitudes):
        """ Place the new node on the activation list if the distance is 
         short enough. If the node is farther than all the candidates in 
         the activation list and the activation list is full, ignore the 
         node. """
        n_activate = self.number_to_activate
        for i in range(n_activate):

            # Activation list is not full, add the new node to the list
            if i == len(self.active_nodes):
                # Reached the end of the activation list but the list 
                # needs more nodes. Implies that this node is now the 
                # farthest away candidate on the self.active_nodes 
                # list.
                self.active_nodes.append(node)
                candidate_magnitudes[node] = node_magnitude
                break
                
            # Activation list is full. Either insert the node in the 
            # activation list or throw it away.
            candidate = self.active_nodes[i]
            candidate_mag = candidate_magnitudes[candidate]

            if node_magnitude < candidate_mag:
                # The node is closer than the current candidate.  
                # Insert the node at this index in the candidate list, 
                # eventually pushing another candidate off the 
                # activation list.
                self.active_nodes.insert(i, node)
                candidate_magnitudes[node] = node_magnitude
                break
            else:
                # The node is farther away than the current candidate.  
                # Keep moving down the activation list. If this is the 
                # last iteration of the for loop, then the new node is 
                # being ignored.
                pass

    def clean_activation_list(self):
        """ Clean up the activation list by changing which nodes are
        selected. In its current form, this function searches for gaps of
        one node and adds that node to the activation list. This function
        can become much more complicated in the future. """

        for node in self.perimeter_nodes:
            # Skip node if it is already on the activation list
            if node in self.active_nodes:
                continue

            # If the left and right node will both be activated, then 
            # activate this node. This prevents a gap of one unselected 
            # node mucking things up.
            left = node.left_node in self.active_nodes
            right = node.right_node in self.active_nodes
            if left and right:
                self.active_nodes.append(node)

    def deactivate_nodes(self):
        for node in self.active_nodes:
            node.deactivate()
        self.active_nodes = []


    # Gui methods
    def draw(self):
        for node in self.perimeter_nodes:
            node.draw()
    
    def move_active_nodes(self, delta):
        # Move the active nodes
        for node in self.active_nodes:
            node.move(delta)

        # Check the link lengths, split or destroy as necessary
        for node in self.active_nodes:
            for adjacent in node.left_node, node.right_node:
                link = node.position - adjacent.position
                length = link.magnitude

                if length > self.max_link_length:
                    # Split the link
                    self.split_link(node, adjacent)
                elif length < self.min_link_length:
                    # Remove adjacent
                    self.remove_node(adjacent)

    def split_link(self, node_a, node_b):
        link = node_a.position - node_b.position
        position = link / 2 + node_b.position

        node = self.create_perimeter_node(position)
        
        if node_a.left_node is node_b:
            node.right_node = node_a
            node.left_node = node_b

            node_a.left_node = node
            node_b.right_node = node

        elif node_a.right_node is node_b:
            node.right_node = node_b
            node.left_node  = node_a

            node_a.right_node = node
            node_b.left_node  = node

        else:
            print("New node did not link properly.")
            raise

    def remove_node(self, node):
        left = node.left_node
        right = node.right_node

        if left.left_node is right:
            print("Cannot have fewer than 3 nodes (less than a triangle).")
        else:
            left.right_node = right
            right.left_node = left
            self.perimeter_nodes.remove(node)
            
