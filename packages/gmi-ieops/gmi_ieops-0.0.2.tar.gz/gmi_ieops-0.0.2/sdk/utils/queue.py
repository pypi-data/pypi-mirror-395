CLOSE = "QUEUE.CLOSE"


class Node(object):

    def __init__(self, value=None, next_node=None):
        self.value = value
        self.next = next_node

    def set_value(self, value):
        self.value = value

    def set_next(self, next_node):
        self.next = next_node


class LinkQueue(object):

    def __init__(self):
        self.front = Node()  # 头节点
        self.rear = self.front  # 队列为空时，头节点=尾节点
        self.count = 0

    def __len__(self):
        return self.count

    def __str__(self):
        s = ''
        cursor = self.front
        while cursor != self.rear:
            cursor = cursor.next
            s += ' %s' % cursor.value
        return s

    def empty(self):
        return self.count == 0

    def put(self, value):
        node = Node(value)
        self.rear.next = node
        self.rear = node
        self.count += 1
        return True

    def close(self):
        node = Node(CLOSE)
        self.rear.next = node
        self.rear = node
        self.count += 1
        return True

    def get(self):
        if self.front == self.rear:
            return None
        p = self.front.next
        value = p.value
        self.front.next = p.next
        # 若队头为等于队尾，则尾节点指向头节点
        if self.rear == p:
            self.rear = self.front
        del p
        self.count -= 1
        return value
