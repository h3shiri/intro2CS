#TODO: add proper decomuentation to all the functions..etc
import copy
# reading the links from a given file.
def read_article_links(file_name):
    res = []
    file = open(file_name, 'r')
    text = file.readlines()
    newText = [item.strip('\n') for item in text]
    multilinks = [item.split('\t') for item in newText]
    workingText = copy.deepcopy(multilinks)
    while len(workingText) >= 1:
        line = workingText.pop()
        #removing garbage end of line
        line.pop()
        while len(line) >= 1:

            chainText = line.pop()
            link = chainText.split(" ")
            edge = (link[0],link[1])
            res.append(edge)
    return res

class Article:
    """docstring for Article"""
    def __init__(self, name):
        self.__name = name
        self.collection = []

    # Retrurn the name of the article
    def get_name(self):
        return self.__name
    # Add a neighbor to the collection
    def add_neighbor(self, neighbor):
        self.collection.append(neighbor)
    # Return the collection list (neighbors)
    def get_neighbors(self):
        #TODO: consider returning a copy
        res = self.collection
        return res
    # Represent an Article format
    def __repr__(self):
        r1 = self.get_name()
        neighbors = self.get_neighbors()
        neighbors_names = [neighbor.get_name() for neighbor in neighbors]
        return str((r1, neighbors_names))
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

        return [ titleAndRankTuple[0] for titleAndRankTuple in sortedByRank ]

    # TODO: test this function.
    def jaccard_index(self, article_name):
        jaccard_dictionary = {}
        # return None in case of no neighboors or non-existing title
        if article_name not in self.__network.keys():
            return None
        elif len(self.__network[article_name].get_neighbors()) == 0:
            return None

        # Define one group (list of articles) as the set of outgoing neighboors from article_name
        setArticlesB = self.__network[article_name].get_neighbors()
        # const set of articles names
        setB ={article.get_name() for article in setArticlesB}
        # Calculate jaccard_index one by one
        for articleA in self.__network.keys():
            setArticlesA = self.__network[articleA].get_neighbors()
            # in case of an article with no neighboors set index as zero
            if len(setArticlesA) == 0:
                jaccard_dictionary[articleA] = 0
                continue
            setA = {article.get_name() for article in setArticlesA}
            index = len(setA & setB)/len(setB.union(setA))
            jaccard_dictionary[articleA] = index

        sortedByTitle = sorted(jaccard_dictionary.items(), key=lambda a: a[0])
        sortedByJaccIndex = sorted(sortedByTitle, key=lambda a: a[1], reverse=True)

        return [ articleTitleAndIndexTuple[0] for articleTitleAndIndexTuple in sortedByJaccIndex ]

    def travel_path_iterator(self, article_name):
        if article_name not in self.get_titles():
            return iter([])
        # Pre calculate the incoming neighbors index for all the articles
        incoming_N_dict_index = {}
        for articleA in self.get_articles():
            # set initial counter
            titleA = articleA.get_name()
            incoming_N_dict_index[titleA] = 0
            for articleB in self.get_articles():
                if articleA in articleB.get_neighbors():
                    incoming_N_dict_index[titleA] += 1

        # Initialise the list of names by the traverse order
        res_list = []
        if incoming_N_dict_index[article_name] != 0:
            res_list.append(article_name)
        current_neighbors = self.__network[article_name].get_neighbors()
        # As long as we have outgoing neigbors continue to traverse
        while len(current_neighbors) != 0:
            current_neighbors_dict = {}
            for neighbor in current_neighbors:
                neighborTitle = neighbor.get_name()
                current_neighbors_dict[neighborTitle] = incoming_N_dict_index[neighborTitle]
            # Sort according to index and secondly by title
            sortedByTitle = sorted(current_neighbors_dict.items(), key=lambda a: a[0])
            sortedByNeighborsIndex = sorted(sortedByTitle, key=lambda a: a[1], reverse=True)
            nextNode = sortedByNeighborsIndex[0][0]
            # In case we made a full circut finish calculating the next node.
            if nextNode in res_list:
                break
            res_list.append(nextNode)
            current_neighbors = self.__network[nextNode].get_neighbors()
            #TODO: create fitting iterator that return appropriate stop iteration.
        res = iter(res_list)
        return res

# TODO: remove tests later on ,this one refrers to the silly links..
'''
network = WikiNetwork(read_article_links('links.txt'));
print('Hello!')
print(network.page_rank(3))
'''
'''
network = WikiNetwork(read_article_links('links2.txt'));
print(network.jaccard_index('Beer')[1])
'''

network = WikiNetwork(read_article_links('links.txt'));
iterator = network.travel_path_iterator('gisanu')
for i in range(3):
    print(iterator.next())


'''
print("processed network")
iterator = network.travel_path_iterator('Hitler')
i=0
for i in range(2):
    print(iterator.next())
'''
