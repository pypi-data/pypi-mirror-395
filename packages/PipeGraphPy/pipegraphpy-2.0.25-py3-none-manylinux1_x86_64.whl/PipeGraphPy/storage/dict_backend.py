from collections import defaultdict


class ParamsPool:
    """传参池"""

    def __init__(self, graph_id, object_id):
        self.graph_id = graph_id
        self.object_id = object_id
        self.all_params = dict()

    def __bool__(self):
        return self.all_params

    def __str__(self):
        return str(list(self.all_params.keys()))

    def add_params(self, id, anchor, data):
        """添加传参值"""
        if self.get_params(id, anchor):
            raise Exception("此参数已经存在")
        self.all_params[(id, anchor)] = data

    def get_params(self, id, anchor):
        """获取传参值"""
        return self.all_params.get((id, anchor))

    def get_params_by_node(self, node, anchor):
        """通过节点获取传参值"""
        return self.get_params(node.id, int(str(anchor)))

    def add_params_by_node(self, node, anchor, data):
        """通过节点添加传参"""
        self.add_params(node.id, anchor, data)

    def add_params_by_list(self, node, data_list):
        """通过数据列表添加传参"""
        for idx, data in enumerate(data_list):
            anchor = node.outidx_to_outanchor(idx)
            self.add_params_by_node(node, anchor, data)

    def is_end(self, node):
        """判断节点是否已运行完"""
        return (
            True
            if self.get_params_by_node(node, node.anchors[1][0].anc) is not None
            else False
        )

    def is_all_fathers_end(self, node):
        """循环父节点判断父节点是否已结束"""
        return all([self.is_end(i) for i in node.fathers])

    # def save_one(self, graph_id, node, anchor):
    #     '''将单个数据保存'''
    #     data = self.get_params_by_node(node, anchor)
    #     if not data:
    #         raise Exception('未找到模块输出数据')
    #     store.save_params(graph_id, node, anchor, data)

    # def save_all(self, graph_id):
    #     '''将所有数据保存'''
    #     for (node, anchor), data in self.all_params.items():
    #         store.save_params(graph_id, node, anchor, data)

    def gen_pass_params(self, node, nodes_group):
        """生成节点要传入的参数"""
        if not self.is_all_fathers_end(node):
            raise Exception("节点%s的父节点还有未运行完的节点" % node)
        # edges_info = EdgesTB.find(graph_id=self.graph_id)
        # nodes_info = NodesTB.find(graph_id=self.graph_id)
        # nodes_info_dict = {i['id']: i for i in nodes_info}
        # nodes_group_dict = gen_nodes_group_dict(edges_info, nodes_info_dict)
        input_output_dict = defaultdict(list)
        input_output_list = list()
        # 循环所有父节点, 组合node和anchor值
        for n in node.fathers:
            output_anchor, input_anchor = nodes_group[(n.id, node.id)]
            input_output_list.extend(
                zip(list(input_anchor), [(n, int(i)) for i in output_anchor])
            )

        for i, o in input_output_list:
            input_output_dict[int(i)].append(o)

        # 根据node和anchor获取节点,识别列表，把接口是列表类型的数据放入一个列表中
        input_params_list = list()
        for k, v in input_output_dict.items():
            if len(v) > 1:
                input_params_list.append((k, [self.get_params_by_node(*i) for i in v]))
            elif len(v) == 1:
                input_params_list.append((k, self.get_params_by_node(*v[0])))
            else:
                raise Exception("传参错误")
        # 参数排序
        input_params_list.sort(key=lambda x: x[0])
        arg = [i[1] for i in input_params_list]
        # 当list输入为1个元素时要转成list
        for i, item in enumerate(node.INPUT):
            if item.startswith("list") and not isinstance(arg[i], list):
                arg[i] = [arg[i]]
        return arg
