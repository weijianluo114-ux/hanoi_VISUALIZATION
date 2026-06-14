import itertools

def get_next_states(state):
    """
    state: tuple of length n, each element 0/1/2
    returns list of new states reachable by one legal move
    """
    n = len(state)
    next_states = []
    # 对于每个盘子，判断它是否在所在柱子的顶部
    for disk in range(n):
        src = state[disk]
        # 检查该盘子是否是源柱子的顶部（即没有比它小的盘子在同一个柱子上）
        is_top = True
        for smaller in range(disk):
            if state[smaller] == src:
                is_top = False
                break
        if not is_top:
            continue
        # 尝试移动到另外两个柱子
        for dst in range(3):
            if dst == src:
                continue
            # 检查目标柱子是否允许放置（没有比它小的盘子）
            can_place = True
            for smaller in range(disk):
                if state[smaller] == dst:
                    can_place = False
                    break
            if can_place:
                new_state = list(state)
                new_state[disk] = dst
                next_states.append(tuple(new_state))
    return next_states

def build_state_graph(n):
    """生成所有状态和邻接表"""
    all_states = [tuple(p) for p in itertools.product([0,1,2], repeat=n)]
    graph = {}
    for state in all_states:
        graph[state] = get_next_states(state)
    return graph