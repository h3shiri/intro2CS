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

class WikiNetwork:

    def __init__(self, link_list = []):
        self.__network = dict()
        self.update_network(link_list)
        
    def update_network(self, link_list = []):
        for link in link_list:
            source = link[0]
            target = link[1]
            if source not in self.__network.keys():
                self.__network[source] = Article(source)

            if target not in self.__network.keys():
                self.__network[target] = Article(target)

            self.__network[source].add_neighbor(self.__network[target])

    def get_articles(self):
        return self.__network.values()

    def get_titles(self):
        return self.__network.keys()

    def __contains__(self, article_name):
        return (article_name in self.get_titles())

    def __len__(self, article_name):
        return self.__network.len()

    def __repr__(self):
        return str(self.__network)

    def __getitem__(self, article_name):
        if article_name not in self.get_titles():
            raise KeyError(article_name)
        return self.__network[article_name]

    def page_rank(self, iters, d=0.9):
        # We create a dictionary that contains, for each title, it's page rank number
        ranks = dict()
        
        # Create all titles in dictionary and set their ranks to 1
        for title in self.get_titles():
            ranks[title] = 1

        # Here are the iterations
        for i in range(iters):

            # Create the new ranks dictionary. We want this to be separate so that by changing the ranks
            # we don't affect the old values.
            newRanks = dict()
            for title in self.get_titles():
                newRanks[title] = 1 - d

            # Update the page ranks
            for title, rank in ranks.items():
                for neighbor in self[title].get_neighbors():
                    newRanks[neighbor.get_name()] += ranks[title]/len(self[title].get_neighbors())

            ranks = copy.deepcopy(newRanks)

        sortedByTitle = sorted(ranks.items(), key=lambda a: a[0])
        sortedByRank = sorted(sortedByTitle, key=lambda a: a[1], reverse=True)

        # print(sortedByRank)

        return [ titleAndRankTuple[0] for titleAndRankTuple in sortedByRank ]

#TODO: remove tests later on
network = WikiNetwork(read_article_links('links.txt'));
print('Hello!')
print(network.page_rank(3))