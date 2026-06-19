
class solution(object):
    def __init__(self) -> None:
        self.solution_dict = []     #空列表，用于存储解题元组(盘子, 所在的柱子, 要移动到的柱子)
        pass


    #清除解题元组列表
    def clear_solution_dict(self):
        self.solution_dict = []
    
    #获取经典汉诺塔需要的最少移动次数
    def get_classical_num(self, num_disk):
        return 2**num_disk-1
        
    #递归函数实现汉诺塔排序
    def recursion(self, num_disk, origin, temp, target):
        if num_disk == 1:
            self.solution_dict.append((num_disk, origin, target))  #将解决过程移动到该列表中
            # print(f'盘子{num_disk}从柱子{origin}到柱子{target}')
            return
        
        self.recursion(num_disk-1, origin, target, temp)     #将此时该柱子最底下的盘子的上面那个移动到目标柱
        # print(f'盘子{num_disk}从柱子{origin}到柱子{target}')             #将最底下那个盘子移动到临时柱子
        self.solution_dict.append((num_disk, origin, target))   #将解决过程移动到该列表中
        self.recursion(num_disk-1, temp, origin, target)     #将剩下的盘子移动到目标柱

    def generate_state_sequence(self, num_disks, origin=0, temp=1, target=2):
        """
        生成解题过程的状态序列
        返回: [(s0), (s1), (s2), ...] 
            每个 s 是 (disk0_tower, disk1_tower, ..., disk{n-1}_tower) 的元组形式
        """
        # 先清空并重新生成 solution_dict
        self.clear_solution_dict()
        self.recursion(num_disks, origin, temp, target)
        
        # 从初始状态开始（所有盘子都在 origin 柱子上）
        state = [origin] * num_disks
        states = [tuple(state)]
        
        # 遍历每一步，更新状态
        for disk_size, origin_tower, target_tower in self.solution_dict:
            # disk_size 范围 [1, num_disks]，减1得到0-based索引
            state[disk_size - 1] = target_tower
            states.append(tuple(state))
        
        return states


if __name__ == '__main__':
    #以下为测试的程序
    solution1 = solution()
    solution1.recursion(3, 1, 2, 3)
    print(solution1.solution_dict)