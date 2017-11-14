import requests
import igraph
import numpy as np
import time
import datetime
from vk_api import get_friends
from pprint import pprint as pp
from igraph import Graph, plot


def get_network(users_ids, as_edgelist=True):
    edges = []
    matrix = [[0 for j in range(len(users_ids))]
              for i in range(len(users_ids))]

    for i, user_id in enumerate(users_ids):
        date1 = datetime.datetime.now()
        response = get_friends(user_id)
        if response.get('error'):
            continue
        friends_list = response['response']['items']
        for j in range(i + 1, len(users_ids)):
            if users_ids[j] in friends_list:
                if as_edgelist:
                    edges.append((i, j))
                else:
                    matrix[i][j] = matrix[j][i] = 1
        date2 = datetime.datetime.now()
        time.sleep(max(0, 0.33334 - (date2 - date1).total_seconds()))
        print("slept for", max(0, 0.33334 - (date2 - date1).total_seconds()))

    if as_edgelist:
        return edges
    else:
        return matrix


if __name__ == '__main__':
    response = get_friends(145458606)
    friends_list = response.get('response').get('items')

    vertices = [i for i in range(len(friends_list))]
    edges = get_network(friends_list)

    g = Graph(vertex_attrs={"label": vertices},
              edges=edges, directed=False)
    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**3,
        repulserad=N**3)

    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    plot(g, **visual_style)
