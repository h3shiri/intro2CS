import copy

# reading the links from a given file.
def read_article_links(file_name):
    """
    @param: file_name
    @return: list of tuples representing directed edges
    """
    res = []
    file = open(file_name, 'r')
    text = file.readlines()
    newText = [item.strip('\n') for item in text]
    multilinks = [item.split('\t') for item in newText]
    workingText = copy.deepcopy(multilinks)
    # Remove all the empty list items and garbage
    for item in copy.deepcopy(workingText):
        if len(item) <= 1:
            workingText.remove(item)
    while len(workingText) >= 1:
        link = workingText.pop(0)
        edge = (link[0],link[1])
        res.append(edge)
    return res

class Article:
    """
    Creating the article class
    """
    #Initialising the class
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
    """
    Creating a WikiNetwork class,
    simulating a graph with multiple articles
    """
    # Initialise the class
    def __init__(self, link_list=[]):
        self.__network = dict()
        self.update_network(link_list)

    # updating the network given a list of edges
    def update_network(self, link_list=[]):
        for link in link_list:
            source = link[0]
            target = link[1]
            if source not in self.__network.keys():
                self.__network[source] = Article(source)

            if target not in self.__network.keys():
                self.__network[target] = Article(target)
            # Make sure the edge does not already exist
            exists = False
            for article in self.__network[source].get_neighbors():
                if article.get_name() == target:
                    exists = True
                    break
            if not exists:
                self.__network[source].add_neighbor(self.__network[target])
    # Return a list of all the articles the network contains
    def get_articles(self):
        res = [article for article in self.__network.values()]
        return res

    # Return list of all the titles included in the network
    def get_titles(self):
        res = [str(title) for title in self.__network.keys()]
        return res
    # Return boolean whether a given title is is the wiki
    def __contains__(self, article_name):
        return (article_name in self.get_titles())

    # Return number of articles in the wiki
    def __len__(self):
        return len(self.__network.keys())

    # Create a repr of the network
    def __repr__(self):
        return str(self.__network)

    # Returns an Article object with the given title, raise exception in case it doesn't exist
    def __getitem__(self, article_name):
        if article_name not in self.get_titles():
            raise KeyError(article_name)
        return self.__network[article_name]

    # Implementation of the Larry Page algorithm
    def page_rank(self, iters, d=0.9):
        """
        @self: the WikiNetwork
        @iters: number of iterations
        @d: An important constant in the algorithm arithmetic
        @return: sorted list of titles by the Larry Page index and secondly lexicographically.
        """
        # We create a dictionary that contains, for each title, it's page rank number
        ranks = dict()
        # Create all titles in dictionary and set their ranks to 1
        for title in self.get_titles():
            ranks[title] = 1
        # Here are the iterations
        for i in range(iters):
            # New Separate independent dictionary derived from the previous one.
            newRanks = dict()
            # residue from all the article is always 1-d
            for title in self.get_titles():
                newRanks[title] = 1 - d

            # Update the page ranks
            for title in ranks.keys():
                neighbors = self.__network[title].get_neighbors()
                for neighbor in neighbors:
                    newRanks[neighbor.get_name()] += (d * (ranks[title]/len(neighbors)))
            ranks = copy.deepcopy(newRanks)
        # Sorting according to specs.
        sortedByTitle = sorted(ranks.items(), key=lambda a: a[0])
        sortedByRank = sorted(sortedByTitle, key=lambda a: a[1], reverse=True)

        return [titleAndRankTuple[0] for titleAndRankTuple in sortedByRank]

    # Soring the the articles by Jaccard_index and secondly by lexicography.
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
        yield article_name
        while len(current_neighbors) != 0:
            degree_N_index_copy = copy.deepcopy(incoming_N_dict_index)
            current_neighbors_dict = {}
            for neighbor in current_neighbors:
                neighborTitle = neighbor.get_name()
                current_neighbors_dict[neighborTitle] = degree_N_index_copy[neighborTitle]
            # Sort according to index and secondly by title
            sortedByTitle = sorted(current_neighbors_dict.items(), key=lambda a: a[0])
            sortedByNeighborsIndex = sorted(sortedByTitle, key=lambda a: a[1], reverse=True)
            nextNode = sortedByNeighborsIndex[0][0]
            current_neighbors = self.__network[nextNode].get_neighbors()
            yield nextNode
        
    # Assisting function returnning a community set of neighboors given a list of articles
    def community_neighboors(self, lst_of_articles = []):
        if len(lst_of_articles) == 0:
            empty_set = set()
            return empty_set
        res_set = set()
        for article in lst_of_articles:
            neighbors = article.get_neighbors()
            names = {neighbor.get_name() for neighbor in neighbors}
            res_set = res_set.union(names)
        return copy.deepcopy(res_set)

    def friends_by_depth(self, article_name, depth):
        res_set = set()
        # friend by distance zero
        res_set.add(article_name)
        # In case depth is zero return list containning only the article_name
        if article_name not in self.get_titles():
            return None
        if depth == 0:
            return [article_name]

        current_neighbors = self.__network[article_name].get_neighbors()
        names = {neighbor.get_name() for neighbor in current_neighbors}
        res_set = res_set.union(names)
        if depth == 1:
            return list(res_set)
        # Now we can run and preform a union several times with the set hence avoiding multiples
        for i in range((depth - 1)):
            new_neighbors_set = self.community_neighboors(current_neighbors)
            res_set = res_set.union(new_neighbors_set)
            current_neighbors = [self.__network[article] for article in new_neighbors_set]
        # Return the friends_set and convert to a list
        res = list(res_set)
        return res
