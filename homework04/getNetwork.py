import requests
import igraph
import numpy as np
import time
from pprint import pprint as pp
from igraph import Graph, plot


DOMAIN = "https://api.vk.com/method"
ACCESS_TOKEN = "3c972e23c1f0119d2f7dc332c8857e4ddd102b483a3dfb4f82bba67fd3a840905c557a02c7811490a169e"

def get_network(users_ids, as_edgelist=True):

    vertices = [i for i in range(len(users_ids))]
    edges = []

    for i, user_id in enumerate(users_ids):
        query_params = {
            'domain': DOMAIN,
            'access_token': ACCESS_TOKEN,
            'user_id': user_id
        }
        query = "{domain}/friends.get?access_token={access_token}\
&user_id={user_id}&v=5.53".format(**query_params)
        response = requests.get(query)
        friends_list = response.json()['response']['items']
        for j in range(i + 1, len(users_ids)):
            if users_ids[j] in friends_list:
                edges.append((i, j))
        pp(response)
        time.sleep(0.3333)

    g = Graph(vertex_attrs={"label":vertices},
    edges=edges, directed=False)

    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**3,
        repulserad=N**3)

    # communities = g.community_edge_betweenness(directed=False)
    # clusters = communities.as_clustering()
    # pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    # g.vs['color'] = pal.get_many(clusters.membership)

    plot(g, **visual_style)
            


if __name__ == '__main__':
    get_network([52022332, # Еркежан
                 60355185, # Влад
                 52972873, # Паша
                 89253594, # Севиль
                 145458606, # Я
                 101425819, # Мадина
                 144772087, # Яна
                 56200185]) # Лиза
