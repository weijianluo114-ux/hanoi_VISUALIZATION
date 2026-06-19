import itertools  # 导入 itertools 库，用于生成笛卡尔积（所有可能的状态组合）

def get_next_states(state):
    """
    state: tuple of length n, each element 0/1/2
    returns list of new states reachable by one legal move
    """
    n = len(state)                         # 获取盘子总数 n
    next_states = []                       # 初始化下一个状态的列表
    # 对于每个盘子，判断它是否在所在柱子的顶部
    for disk in range(n):                  # 遍历每个盘子（从最小的 0 到最大的 n-1）
        src = state[disk]                  # 获取当前盘子所在的柱子编号 (0/1/2)
        # 检查该盘子是否是源柱子的顶部（即没有比它小的盘子在同一个柱子上）
        is_top = True                      # 先假设当前盘子位于柱子顶部
        for smaller in range(disk):        # 遍历所有比当前盘子小的盘子
            if state[smaller] == src:      # 如果有更小的盘子在同一个柱子上
                is_top = False             # 则当前盘子不在顶部
                break                      # 退出内层循环
        if not is_top:                     # 如果当前盘子不在顶部
            continue                       # 跳过，不能移动这个盘子
        # 尝试移动到另外两个柱子
        for dst in range(3):               # 遍历三个柱子 (0, 1, 2) 作为目标
            if dst == src:                 # 如果目标柱子就是当前所在的柱子
                continue                   # 跳过，无需移动
            # 检查目标柱子是否允许放置（没有比它小的盘子）
            can_place = True               # 先假设可以放置
            for smaller in range(disk):    # 遍历所有比当前盘子小的盘子
                if state[smaller] == dst:  # 如果有更小的盘子已经在目标柱子上
                    can_place = False      # 则不能放置（大盘不能压小盘）
                    break                  # 退出内层循环
            if can_place:                  # 如果可以放置
                new_state = list(state)    # 将当前状态元组转为列表以修改
                new_state[disk] = dst      # 将当前盘子移动到目标柱子
                next_states.append(tuple(new_state))  # 将新状态转为元组加入列表
    return next_states                     # 返回所有可达的下一个状态列表

def build_state_graph(n):
    """生成所有状态和邻接表"""
    all_states = [tuple(p) for p in itertools.product([0,1,2], repeat=n)]  # 生成所有 3^n 种状态
    graph = {}                             # 初始化空字典，用于存储邻接表
    for state in all_states:               # 遍历每一个状态
        graph[state] = get_next_states(state)  # 计算该状态的下一步可达状态并存入字典
    return graph                           # 返回完整的状态图（邻接表）

if __name__ == "__main__":
    graph = build_state_graph(3)
    print(graph)