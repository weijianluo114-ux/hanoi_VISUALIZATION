
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

    


if __name__ == '__main__':
    #以下为测试的程序
    solution1 = solution()
    solution1.recursion(3, 1, 2, 3)
    print(solution1.solution_dict)