
# reading the links from a given file.
def read_article_links(file_name):
    res = []
    file = open(file_name, 'r')
    text = file.read()
    links = text.split('\t')
    # appending all the links one by one
    while len(links) > 0:
        node1 = links.pop(0)
        node2 = links.pop(0)
        edge = (node1, node2)
        res.append(edge)
    return res
    