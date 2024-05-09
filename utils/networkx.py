# -*- coding: utf-8 -*-
"""
Created on 2024/4/17
利用聊天数据，找出度最高的前N个，画出社交网络图
"""
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

node_num = 30


def get_data():
    """
    基础数据
    :return:
    """
    df = pd.read_csv(
        "数据-id.csv",
    )
    return df


def dfs_top(G):
    # 获取节点的度信息
    degreeView = G.degree()
    # 计算节点度的频率
    degree_counts = Counter(dict(degreeView))
    # 找到具有最高度的前10个节点
    max_degree_node = degree_counts.most_common(node_num)
    # 提取节点号
    nodes_filter = [i[0] for i in max_degree_node]

    print(nodes_filter)

    dfs_sequence = set()
    for index, start_node in enumerate(nodes_filter):
        # 执行深度优先搜索并生成节点序列
        dfs_sequence = dfs_sequence | set(nx.dfs_preorder_nodes(G, source=start_node))
        print(index, start_node, len(dfs_sequence))

    # 深度搜索， 指定某个节点，获取指定深度下的edges
    depth = 5
    # 假设 G 是您的原始 NetworkX 图对象
    nodes_of_interest = []  # 您感兴趣的节点列表
    for i in nodes_filter:
        edges = list(nx.dfs_edges(G, source=i, depth_limit=depth))
        nodes = [i[0] for i in edges]
        nodes_of_interest.extend(nodes)

    subgraph = G.subgraph(set(nodes_of_interest))
    plot_options = {"node_size": 10, "with_labels": False, "width": 0.15}
    nx.draw(subgraph, **plot_options)
    plt.show()


def show(G):
    # 设置节点位置布局
    pos = nx.spring_layout(G, iterations=15, seed=1721)
    # 创建图形和坐标轴
    fig, ax = plt.subplots(figsize=(15, 9))
    ax.axis("off")
    # 设置绘图选项
    plot_options = {"node_size": 10, "with_labels": False, "width": 0.15}
    nx.draw_networkx(G, pos=pos, ax=ax, **plot_options)
    # 显示图形
    plt.show()


def centrality(G):
    # 获取中心节点
    # 度中心性（Degree Centrality）
    degree_centrality = nx.degree_centrality(G)
    # 找到具有最高度中心性的节点
    most_central_node_by_degree = max(degree_centrality, key=degree_centrality.get)
    print(most_central_node_by_degree)
    # 所有节点的度中心性值
    print("Degree centrality values:")
    for node, centrality in degree_centrality.items():
        print(f"Node {node}: Degree Centrality {centrality}")
    return most_central_node_by_degree


def betweenness(G):
    # 介数中心性(Betweenness Centrality), 执行比较慢，需要10分钟左右
    betweenness_centrality = nx.centrality.betweenness_centrality(
        G
    )  # save results in a variable to use again
    most_central_node_by_betweenness = max(
        betweenness_centrality, key=betweenness_centrality.get
    )
    print(most_central_node_by_betweenness)


def closeness(G):
    # 接近中心性（Closeness Centrality）
    closeness_centrality = nx.closeness_centrality(G)
    most_central_node_by_closeness = max(
        closeness_centrality, key=closeness_centrality.get
    )
    print(most_central_node_by_closeness)


def eigenvector(G):
    # 特征向量中心性（Eigenvector Centrality）,可设置权重
    # eigenvector_centrality = nx.eigenvector_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G, weight="friendliness")
    most_central_node_by_eigenvector = max(
        eigenvector_centrality, key=eigenvector_centrality.get
    )
    print(most_central_node_by_eigenvector)


def bfs_top(G):
    # 广度优先
    # 使用 networkx 的 bfs_edges 函数进行广度优先搜索
    # 返回的是一个迭代器，包含所有邻接的边 (u, v)，其中 u 是起始节点，v 是在其之后访问的节点
    start_node = centrality(G)
    # 定义一个空字典来存储节点及其度数
    degree_counts = {}
    # 使用了  nx.bfs_edges()  方法执行广度优先搜索，并在搜索过程中记录每个节点的度数。
    # 然后使用  Counter  对度数进行计数排序，最后取出度数最高的前10个节点。这种方法是在广度优先搜索的过程中动态计算每个节点的度数，并最终找到度数最高的前10个节点。
    # # 使用 networkx 的 bfs_edges 函数进行广度优先搜索
    for source, target in nx.bfs_edges(G, start_node):
        degree_counts[source] = degree_counts.get(source, 0) + 1
        degree_counts[target] = degree_counts.get(target, 0) + 1
    #
    # # 使用 Counter 对字典进行计数排序，获取度数最高的节点及其度数
    degree_counts = Counter(degree_counts)
    #
    # # 取出度数最高的前10个节点（按度数降序排列）
    top_10_nodes_by_degree = [i[0] for i in degree_counts.most_common(node_num)]

    # TODO 使用了  nx.bfs_tree()  方法生成了一个广度优先搜索树，然后直接从搜索树中提取了前10个节点。这种方法是首先生成广度优先搜索树，然后从树中提取节点，而不是在搜索过程中动态计算节点的度数。
    # bfs_tree = nx.bfs_tree(G, source=start_node)
    # # 从广度优先搜索树中提取前10个节点
    # print(bfs_tree.nodes())
    # top_10_nodes_by_degree = list(bfs_tree.nodes())[:node_num]
    # degree_counts = Counter(dict(G.degree()))
    # top_10_nodes_by_degree = [node for node, _ in degree_counts.most_common(node_num)]
    print(top_10_nodes_by_degree)
    tmp = []
    # for node, _ in degree_counts.most_common(node_num):
    #     print(node, _)
    #     tmp.append({"role_id":node, "num": _})
    # pd.DataFrame(tmp).to_csv('1.csv', index=False)
    # 广度搜索
    depth = 3
    nodes_of_interest = []
    for i in top_10_nodes_by_degree:
        edges = list(nx.bfs_edges(G, source=i, depth_limit=depth))
        nodes = [j[0] for j in edges]
        # print(i, len(edges))
        nodes_of_interest.extend(nodes)
        tmp.append({"role_id": i, "num": len(edges)})
    pd.DataFrame(tmp).to_csv("1.csv", index=False)
    subgraph = G.subgraph(set(nodes_of_interest))
    plot_options = {"node_size": 10, "with_labels": False, "width": 0.15}
    nx.draw(subgraph, **plot_options)
    plt.show()


def run():
    df = get_data()
    G = nx.from_pandas_edgelist(
        df,
        "role_id",
        "to_role",
        edge_attr="friendliness",
    )
    bfs_top(G)
    # dfs_top(G)
    # centrality(G)


def property(G):
    # 节点数量
    print(G.number_of_nodes())
    # 连边数量
    print(G.number_of_edges())
