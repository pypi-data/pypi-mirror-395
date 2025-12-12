import copy
from PipeGraphPy.constants import MODULES   # , JUPYTER_TYPE
try:
    from prettytable import PrettyTable
except Exception as e:
    print(e)
    PrettyTable = None
from PipeGraphPy.config import settings

# from PipeGraphPy.plot.plt_draw import ChartNode, ChartGraph, ChartArrow

default_str = "--"
replace_str = "="
stop_str = "|"
connect_str = " --> "


def get_all_node(all_pipline):
    """获取有序的所有节点列表"""
    # 所有节点
    all_nodes = []
    _ = [all_nodes.extend(i) for i in all_pipline]
    # 去重
    all_nodes = list(set(all_nodes))
    # 排序
    for i in range(len(all_pipline)):
        indexs = [all_nodes.index(j) for j in all_pipline[i]]
        indexs_sort = sorted(indexs)
        copy_nodes = copy.deepcopy(all_nodes)
        for n, i in enumerate(indexs_sort):
            all_nodes[i] = copy_nodes[indexs[n]]
    return all_nodes


def get_one_head_pipline_list(graph, head):
    """获取一个头节点下所有节点走向列表

    Args:
        head (Node): 头节点

    Returns:
        list(list[Node]): 走向列表
    """

    pipline_list = list()
    pipline = list()

    def _iter_children(node):
        pipline.append(node)
        if not graph.a.source_nodes_group.get(node):
            pipline_list.append(copy.deepcopy(pipline))
            return
        for i in graph.a.source_nodes_group[node]:
            _iter_children(i)
            pipline.pop()

    _iter_children(head)
    return pipline_list


def get_head_cls(graph):
    """由头节点开头的子节点集合的个数"""
    head_child_set_list = list()  # 由头节点开头的子节点集合的个数
    for head in graph.a.start_nodes:
        node_set = set()
        for child in graph.a._iter_children(head):
            node_set.add(str(child))
        head_child_set_list.append([[head], node_set])
    for i in range(len(head_child_set_list), 1, -1):
        for j in range(i - 1):
            if head_child_set_list[i - 1][1] & head_child_set_list[j][1]:
                head_child_set_list[j][0].extend(head_child_set_list[i - 1][0])
                head_child_set_list[i - 1] = []
                break
    return [i[0] for i in head_child_set_list if i]


def merge_same_node(gpl):
    """把相同的节点合并"""
    # 循环所有节点
    length = len(gpl[0])
    for i in range(length):
        # 统计相等的行
        line_idx = [idx for idx, j in enumerate(gpl) if j[i] != default_str]
        mid_idx = int((line_idx[0] + line_idx[-1]) / 2)
        for idx in range(line_idx[0], line_idx[-1] + 1):
            if idx == mid_idx:
                gpl[idx][i] = gpl[line_idx[-1]][i]
            elif gpl[idx][i] == default_str:  # 变更中间的default_str 为 stop_str
                gpl[idx][i] = stop_str
            else:
                gpl[idx][i] = replace_str
    return gpl


def compress2right(gpl):
    """向右压缩"""
    length = len(gpl[0])
    # 长度小于3直接返回, 不需要做处理
    if length < 3:
        return gpl
    # 从倒数第二个至第一个循环, 逐列向右压缩
    for i in range(length - 2, 0, -1):
        # 统计相等的行
        line_idx = [idx for idx, j in enumerate(gpl) if j[i] != default_str]

        # 相等的中间行和最靠后的全为default_str的位置对换
        for j in range(i + 1, length):
            if all([gpl[k][j] == default_str for k in line_idx]):
                if j < length - 1:
                    continue
                else:
                    for k in line_idx:
                        gpl[k][i], gpl[k][j] = gpl[k][j], gpl[k][i]
                    break
            else:
                for k in line_idx:
                    gpl[k][i], gpl[k][j - 1] = gpl[k][j - 1], gpl[k][i]
                break
    # 去除全是default_str的列
    # adsi:all_default_str_idx
    adsi = list()
    for i in range(length):
        if all([j[i] == default_str for j in gpl]):
            adsi.append(i)
    if adsi:
        for i in gpl:
            i[adsi[0] : adsi[-1] + 1] = []
    return gpl


def compress2left(gpl):
    """向左压缩"""
    length = len(gpl[0])
    # 长度小于3直接返回, 不需要做处理
    if length < 3:
        return gpl
    for i in range(2, length):
        for j in range(len(gpl)):
            if isinstance(gpl[j][i], str):
                continue
            for k in range(i - 1, -1, -1):
                if gpl[j][k] == default_str:
                    continue
                else:
                    if k + 1 == i:
                        break
                    gpl[j][k + 1], gpl[j][i] = gpl[j][i], gpl[j][k + 1]
                    break
    return gpl


def node_layout(graph, heads):
    """节点布局，各节点放在合适的位置

    Args:
        heads ([list(Node)]): 头节点
    """

    # 所有节点走向列表
    all_pipline = list()
    for i in heads:
        all_pipline.extend(get_one_head_pipline_list(graph, i))

    # 有序的所有节点
    all_node = get_all_node(all_pipline)

    # 所有pipline节点按照all_node定位,使所有pipline等长,不存在的节点补default_str
    same_len_pipline = list()
    for i in all_pipline:
        _lst = [default_str] * len(all_node)
        for j in i:
            _lst[all_node.index(j)] = j
        same_len_pipline.append(_lst)

    # 合并重名列
    merge_pipline = merge_same_node(same_len_pipline)

    # 向右压缩
    compress_right_gpl = compress2right(merge_pipline)

    # 向左压缩
    compress_left_gpl = compress2left(compress_right_gpl)

    return compress_left_gpl


def plot_by_pt(graph):
    """通过pt展示图"""
    # 分图，有可能是多张图, 把同一图的头节点，分到一个列表中
    all_graph_node = list()
    heads_cls = get_head_cls(graph)
    for num, heads in enumerate(heads_cls):
        # 节点排布
        layout_node = node_layout(graph, heads)

        if len(layout_node) > len(all_graph_node):
            layout_node, all_graph_node = all_graph_node, layout_node

        # 所有图的节点合并
        default_lst = [default_str] * len(all_graph_node[0])
        for i in layout_node:
            c_lst = copy.copy(default_lst)
            c_lst[: len(i)] = i
            all_graph_node.append(c_lst)
    # 节点标号
    node2tag = dict()
    num = 1
    for i in all_graph_node:
        for j in i:
            if not isinstance(j, str):
                node2tag[j] = num
                num += 1

    # 连接边
    node2nodes = dict()
    for k, v in graph.a.source_nodes_group.items():
        node2nodes[graph.a.nodes_dict[k]] = [graph.a.nodes_dict[i] for i in v]

    # 节点转字符
    for i in range(len(all_graph_node)):
        for j in range(len(all_graph_node[i])):
            if not isinstance(all_graph_node[i][j], str):
                if node2nodes.get(all_graph_node[i][j]):
                    all_graph_node[i][j] = "(%s)%s-->%s" % (
                        node2tag[all_graph_node[i][j]],
                        str(all_graph_node[i][j]),
                        ",".join(
                            [str(node2tag[k]) for k in node2nodes[all_graph_node[i][j]]]
                        ),
                    )
                else:
                    all_graph_node[i][j] = "(%s)%s" % (
                        node2tag[all_graph_node[i][j]],
                        str(all_graph_node[i][j]),
                    )
            else:
                all_graph_node[i][j] = ""

    # 打印显示
    pt = PrettyTable()
    pt.header = False
    for i in all_graph_node:
        pt.add_row(i)
    print(pt)
    return pt


def plot_by_jupyter(graph, just_build=False, load_javascript=False):
    from pyecharts.globals import CurrentConfig

    if settings.JUPYTER_TYPE not in JUPYTER_TYPE.values():
        raise Exception("JUPYTER_TYPE设置错误")
    CurrentConfig.NOTEBOOK_TYPE = settings.JUPYTER_TYPE

    from pyecharts import options as opts
    from pyecharts.charts import Graph

    nodes = list()
    links = list()
    x_span = 160
    y_span = 50
    # merge_px = 100
    max_width = 900
    max_height = 500
    sum_x, sum_y = 0, 0
    merge = 100
    init_edge = 50

    # 分图，有可能是多张图, 把同一图的头节点，分到一个列表中
    heads_cls = get_head_cls(graph)
    nodes.append(opts.GraphNode(x=init_edge, y=init_edge, symbol_size=1, is_fixed=True))
    for heads in heads_cls:
        # 节点排布
        layout_node = node_layout(graph, heads)
        # 增加节点
        for y_idx, i in enumerate(layout_node):
            for x_idx, j in enumerate(i):
                if not isinstance(j, str):
                    nodes.append(
                        opts.GraphNode(
                            name=str(j),
                            x=x_idx * x_span + merge,
                            y=y_idx * y_span + sum_y + merge,
                            is_fixed=True,
                        )
                    )
        sum_y += len(layout_node) * y_span + merge
        this_width = len(layout_node[0]) * x_span + merge
        if this_width > sum_x:
            sum_x = this_width
    nodes.append(
        opts.GraphNode(
            x=sum_x + init_edge, y=sum_y + init_edge, symbol_size=1, is_fixed=True
        )
    )
    sum_x = sum_x + merge
    sum_y = sum_y + merge

    # 生成连线
    edges_tuple = [
        (
            graph.a.nodes_dict[i.info["source_id"]],
            graph.a.nodes_dict[i.info["target_id"]],
        )
        for i in graph.edges
    ]

    for i in edges_tuple:
        links.append(opts.GraphLink(source=str(i[0]), target=str(i[1])))

    # 画图
    width = "%spx" % (max_width if sum_x > max_width else sum_x)
    height = "%spx" % (max_height if sum_y > max_height else sum_y)

    charts_graph = (
        Graph(init_opts=opts.InitOpts(width=width, height=height))
        .add(
            "",
            nodes,
            links,
            symbol_size=30,
            layout="none",
            edge_symbol=["circle", "arrow"],
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=str(graph)))
    )
    if just_build:
        if load_javascript:
            charts_graph.load_javascript()
        return charts_graph
    return charts_graph.render_notebook()


# def draw_by_plt(graph):
#     nodes = list()
#     edges = list()
#     x_span = 16
#     y_span = 5
#     sum_x, sum_y = 0, 0

#     # 分图，有可能是多张图, 把同一图的头节点，分到一个列表中
#     heads_cls = get_head_cls(graph)
#     for heads in heads_cls:
#         # 节点排布
#         layout_node = node_layout(heads)
#         # 增加节点
#         for y_idx, i in enumerate(layout_node):
#             for x_idx, j in enumerate(i):
#                 if not isinstance(j, str):
#                     nodes.append(
#                         ChartNode(
#                             x=x_idx * x_span + int(x_span / 2),
#                             y=y_idx * y_span + int(y_span / 2) + sum_y,
#                             name=str(j),
#                         )
#                     )
#         sum_y += len(layout_node) * y_span
#         this_width = len(layout_node[0]) * x_span
#         if this_width > sum_x:
#             sum_x = this_width

#     # 生成连线
#     edges_tuple = [
#         (
#             graph.a.nodes_dict[i.info["source_id"]],
#             graph.a.nodes_dict[i.info["target_id"]],
#         )
#         for i in graph.edges
#     ]
#     nodes_dict = {i.name: i for i in nodes}

#     for i in edges_tuple:
#         edges.append(
#             ChartArrow(start_node=nodes_dict[str(i[0])], end_node=nodes_dict[str(i[1])])
#         )

#     # 画图
#     chart_graph = ChartGraph(nodes, edges, dict(xlim=(0, sum_x), ylim=(0, sum_y)))
#     chart_graph.plot(sum_x, sum_y)


# def draw_graph(graph, load_javascript=False):
#     """显示图

#     Args:
#         graph (Graph): 要显示的图

#     Returns:
#         object: 经过处理后的图
#     """
#     if not settings.ISJUPYTER:
#         return draw_by_pt(graph)
#     else:
#         return draw_by_jupyter(graph, load_javascript)
#         # return draw_by_plt(graph)


def draw_test(just_build=False):
    from pyecharts.globals import CurrentConfig, NotebookType

    CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB

    from pyecharts import options as opts
    from pyecharts.charts import Graph

    nodes = [
        opts.GraphNode(name="结点1", symbol_size=10),
        opts.GraphNode(name="结点2", symbol_size=20),
        opts.GraphNode(name="结点3", symbol_size=30),
        opts.GraphNode(name="结点4", symbol_size=40),
        opts.GraphNode(name="结点5", symbol_size=50),
    ]
    links = [
        opts.GraphLink(source="结点1", target="结点2"),
        opts.GraphLink(source="结点2", target="结点3"),
        opts.GraphLink(source="结点3", target="结点4"),
        opts.GraphLink(source="结点4", target="结点5"),
        opts.GraphLink(source="结点5", target="结点1"),
    ]
    c = (
        Graph()
        .add("", nodes, links, repulsion=4000)
        .set_global_opts(title_opts=opts.TitleOpts(title="Graph-GraphNode-GraphLink"))
    )
    if not just_build:
        c.load_javascript()
    return c
