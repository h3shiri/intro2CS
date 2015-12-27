import copy
# reading the links from a given file.
def read_article_links(file_name):
    res = []
    file = open(file_name, 'r')
    text = file.read()
    links = text.split('\t')
    # appending all the links one by one
    while len(links) >= 2:
        node1 = links.pop(0)
        node2 = links.pop(0)
        edge = (node1, node2)
        res.append(edge)
    return res

class Article:
    """docstring for Article"""
    def __init__(self, name):
        self.__name = name
        #figured out this collections
        self.collection = []

    # Retrurn the name of the article
    def get_name(self):
        return self.__name
    # Add a neighbor to the collection
    def add_neighbor(self, neighbor):
        self.collection.append(neighbor)
    # Return the collection list (neighbors)
    def get_neighbors(self):
        res = copy.deepcopy(self.collection)
        return res
    # Represent an Article format
    def __repr__(self):
        r1 = self.get_name()
        r2 = self.get_neighbors()
        res = str(r1, r2)
        print(res)
    # Return the number of neighbors
    def __len__(self):
        res = len(self.get_neighbors())
        return res
    # Determine whether an article is an outgoing neighbor
    def __contains__(self, article):
        res = article in self.collection
        return res