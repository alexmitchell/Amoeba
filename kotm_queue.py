from collections import deque as Deque

class KOTMQueue (Deque):
    """ King of the Mountain Queue. If the queue is full, adding a
    new item will push one off the back. """

    def __init__(self, max_length):
        Deque.__init__(self, maxlen=max_length)
        self.length = 0
    
    def is_full(self):
        return self.length == self.maxlen

    def push(self, item):
        """ Put an item in the queue. If it is full, push an item
        off the other end and throw it away. """
        discarded = self.push_return(item)
    
    def push_return(self, item):
        """ Put an item in the queue. If it is full, push an item
        off the other end and return than item. """

        discarded = None
        if self.is_full():
            discarded = self.pop()
        else:
            self.length += 1
        self.appendleft(item)
        return discarded

    def clear(self):
        Deque.clear(self)
        self.length = 0

    def peek_all(self, youngest_first=False):
        """ Return a list of the elements in the queue without
        emptying the queue. """
        return [item for item in self]

    def peek(self, index):
        try:
            return self[index]
        except IndexError:
            return None

    def peek_front(self):
        return self.peek(0)

    def peek_back(self):
        return self.peek(-1)
