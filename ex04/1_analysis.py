import networkx as nx
import sys
import collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def nodelabel(label_filename):
    f = open(label_filename, "r")
    line = f.readline()
    label_data = dict()
    while line:
        num, name = line.split()
        label_data[num] = name
        line = f.readline()
    f.close()
    return label_data

def read_and_relabel(graph_filename, label_filename):
    G = nx.read_edgelist(graph_filename, create_using=nx.DiGraph())
    G = nx.relabel_nodes(G, mapping=nodelabel(label_filename))
    return G

def basic_data(G):
    print("\n########### Basic Graph Data ###########")
    print("- Number of nodes:", nx.number_of_nodes(G))
    print("- Number of edges:", nx.number_of_edges(G))
    if nx.is_strongly_connected(G):
        print("- Given graph is strongly connected.")
        print("- Diameter:", nx.diameter(G))
    else:
        print("- Given graph is not strongly connected.")
    return 0

def shortestpath_data(G, sourcename, targetname):
    print("\n########### ex01 ###########")
    source2target = nx.shortest_path(G, source=sourcename, target=targetname)
    print("- Shortest path from %s to %s:" % (sourcename, targetname), source2target, ", %d hops" % (len(source2target)-1))


# [fuction for properties]
# Degree distribution
def degree_dist(G):
    x = list(collections.Counter(dict(G.degree()).values()).keys())
    y = list(collections.Counter(dict(G.degree()).values()).values())
    y = list(map(lambda e: e/nx.number_of_nodes(G), y))
    return x, y

# Closeness centrality
def closeness_centrality(G):
    close_cent_list = sorted(dict(nx.closeness_centrality(G)).values())
    N = G.number_of_nodes()
    if (len(close_cent_list) != N):
        raise Exception("[error] number of nodes is weird !!")
    close_cent = dict()
    for i in range(0, N):
        close_cent[i] = close_cent_list[i]
    return close_cent

def plot(x, y, xlabel, ylabel, title, figname, type="scatter", xlog=True, ylog=True):
    fig, ax = plt.subplots()
    plt.title(title)
    plt.scatter(x, y, s=0.8, color='r')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.savefig(figname, dpi=500)
    return 0


##### Main Process
graph_filename = sys.argv[1]
label_filename = sys.argv[2]
G = read_and_relabel(graph_filename, label_filename)
basic_data(G)
shortestpath_data(G, "jacob", "andy")
print("\n")

x, y = degree_dist(G)
plot(x,y,"node degree k","degree distribution p(k)","Degree Distribution","01_degree_distribution.png")
# plot(x,y,"node degree k","degree distribution p(k)","Degree Distribution","02_degree_distribution.png")
