import pygame

class Tower:
    """简单的柱子类，只负责绘制"""
    def __init__(self, x, y, pole_width, pole_height, base_width, base_height, max_disks, color=(176,196,222)):
        """
        :param x: 柱子底部中心点的 x 坐标
        :param y: 柱子底部（底座下沿）的 y 坐标
        :param pole_width: 柱子杆的宽度
        :param pole_height: 柱子杆的高度
        :param base_width: 底座的宽度
        :param base_height: 底座的高度
        :param color: 柱子杆的颜色，底座颜色可自行调整
        max_disks: 最多能放多少个盘子（用于计算盘子位置）
        """
        self.x = x
        self.y = y
        self.pole_width = pole_width
        self.pole_height = pole_height
        self.base_width = base_width
        self.base_height = base_height
        self.color = color          # 柱子杆颜色
        self.base_color = (255,182,193)  # 底座颜色（棕色），可根据需要修改
        self.max_disks = max_disks
        self.disks = []      # 存储当前柱子上的盘子对象（列表作为栈）

    def add_disk(self, disk):
        """将盘子放到柱子顶部"""
        if self.can_add_disk(disk):
            # 更新盘子的位置坐标（根据当前盘子数量计算 y）
            disk.rect.centerx = self.x
            disk.rect.bottom = self.y - self.base_height - (len(self.disks)) * disk.height  #应该先计算当前底部的盘子的位置再添加盘子
            self.disks.append(disk)     #将当前的盘子添加到该柱子上
            return True
        return False

    def remove_disk(self):
        """从柱子顶部移走盘子"""
        if self.disks:
            return self.disks.pop()
        return None

    def top_disk(self):
        """返回顶部盘子（不移除）"""
        return self.disks[-1] if self.disks else None

    def can_add_disk(self, disk):
        """判断能否放置盘子（比当前顶部盘子小或为空）"""
        # 无盘子，可以放置
        if not self.disks:
            return True
        # 有序号更大的盘子，可以放置
        return disk.size < self.disks[-1].size   # 假设 Disk 有 size 属性

    def draw(self, screen):
        
        """在指定的 screen 上绘制柱子"""
        # 绘制底座（一个扁矩形）
        base_rect = pygame.Rect(
            self.x - self.base_width // 2,
            self.y - self.base_height,
            self.base_width,
            self.base_height
        )
        pygame.draw.rect(screen, self.base_color, base_rect)

        # 绘制柱子杆（竖立矩形）
        pole_rect = pygame.Rect(
            self.x - self.pole_width // 2,
            self.y - self.base_height - self.pole_height,
            self.pole_width,
            self.pole_height
        )
        pygame.draw.rect(screen, self.color, pole_rect)
        
        
        # 绘制柱子杆顶部（圆形）
        pole_top = (self.x, self.y - self.base_height - self.pole_height)    #顶部
        pole_top_radius = self.pole_width // 2      #半径
        pygame.draw.circle(screen, self.color, pole_top, pole_top_radius)
        
        # 绘制盘子（可选：也可以由盘子自己绘制，但由 Tower 遍历调用更方便）
        for disk in self.disks:
            disk.draw(screen)