import pygame     #游戏包
import sys  #用于退出系统

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))   # 将 your_project 加入路径

# 导入自定义组件
from components import tower_m
from components import disk_m

# 参数
# width, height = 1280, 720
# num_disks = 4       #盘子的数量

class gameplay(object):
    """docstring for gameplay."""
    def __init__(self, screen, font, num_disks):
        super(gameplay, self).__init__()
        self.screen_surface = screen
        self.game_font = font
        self.selected_tower = 0      # 初始选中第一根柱子
        self.holding_disk = None     # 手中没有盘子
        self.num_disks = num_disks
        self.anim_disk = None
        
        # 柱子类
        self.towers = [
            tower_m.Tower(320, 700, 20, 400, 240, 40, self.num_disks),
            tower_m.Tower(640, 700, 20, 400, 240, 40, self.num_disks),
            tower_m.Tower(960, 700, 20, 400, 240, 40, self.num_disks)
        ]

        # 盘子类
        self.disks = []
        disk_font = pygame.font.SysFont('SimHei', 15)   #序号字体
        for disk_size in range(self.num_disks, 0, -1):  # disk_size 从 self.num_disks 递减到 1
            disk_color = (100, 200, 255 - disk_size * (200/self.num_disks))   # 示例：颜色随大小变化（蓝色调）
            disk = disk_m.Disk(disk_size, disk_color, disk_font, height=30)
            self.disks.append(disk)
        
        # 将所有盘子加到第一根柱子（索引0）
        for disk in self.disks:
            self.towers[0].add_disk(disk)
    
    def handle_events(self, event):
        # 处理游戏中的键盘事件，按 ESC 返回菜单
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 0   # 返回主菜单状态 MENU
        # 原有的空格、数字键处理...
        elif self.anim_disk is not None:
            # 动画期间忽略所有操作（除了退出）
            return 1  # 或直接跳过事件处理
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:     #选中第一根柱子
                selected_tower = 0
            elif event.key == pygame.K_2:   #选中第二根柱子
                selected_tower = 1
            elif event.key == pygame.K_3:   #选中第三根柱子
                selected_tower = 2
            elif event.key == pygame.K_SPACE:
                if self.holding_disk is None:
                    # 尝试从当前选中柱子上拿起最上面的盘子
                    disk = self.towers[self.selected_tower].remove_disk()
                    if disk is not None:
                        self.holding_disk = disk
                        # 拿起后立即将盘子显示在柱子上方（y=100）
                        tower_x = self.towers[self.selected_tower].x
                        self.holding_disk.rect.center = (tower_x, 100)
                        print(f"拿起了盘子 {disk.size}")
                    else:
                        print("柱子上没有盘子可拿")
                else:
                    # 尝试将手中的盘子放到当前选中柱子上
                    if self.towers[self.selected_tower].can_add_disk(self.holding_disk):
                        # 开始动画：记录起始位置（当前空中位置）和目标位置（目标柱顶部）
                        self.anim_disk = self.holding_disk
                        anim_start_pos = self.holding_disk.rect.center
                        # 计算目标柱顶部中心坐标
                        target_tower = self.towers[self.selected_tower]
                        target_x = target_tower.x
                        target_y = target_tower.y - target_tower.base_height - (len(target_tower.disks)) * self.anim_disk.height
                        anim_end_pos = (target_x, target_y)
                        # 初始化进度
                        anim_progress = 0.0
                        # 清空手中盘子，准备动画
                        self.holding_disk = None
                        print(f"开始移动盘子 {self.anim_disk.size} 到柱子 {self.selected_tower+1}")
                    else:
                        print("不能放在这里，规则不允许")
        # 注意：可能需要访问全局变量（如 holding_disk），可以在函数内部修改它们
        return None

    def update(self):
        anim_progress = 0.0        # 动画进度 0~1
        anim_speed = 0.06          # 每帧进度增量（控制动画速度）
        anim_start_pos = (0, 0)    # 起始位置（屏幕坐标）
        anim_end_pos = (0, 0)      # 结束位置（屏幕坐标）
        # 动画更新逻辑（原有的动画进度更新）
        if self.anim_disk is not None:
            anim_progress += anim_speed
            if anim_progress >= 1.0:
                anim_progress = 1.0
                # 动画完成：将盘子放入目标柱子
                self.towers[self.selected_tower].add_disk(self.anim_disk)  # 注意：目标柱子是当前选中的
                self.anim_disk = None
            else:
                # 根据进度插值计算当前帧的位置
                print(anim_start_pos, ' ', anim_end_pos, ' ', anim_progress)
                current_x = anim_start_pos[0] + (anim_end_pos[0] - anim_start_pos[0]) * anim_progress
                current_y = anim_start_pos[1] + (anim_end_pos[1] - anim_start_pos[1]) * anim_progress
                self.anim_disk.rect.center = (current_x, current_y)

        if self.anim_disk:
            self.anim_disk.draw(self.screen_surface)


    def draw(self):
        
        self.screen_surface.fill((255,255,255))     #清屏
        for tower in self.towers:
            tower.draw(self.screen_surface)
        # 绘制手中盘子和动画盘子...
        for tower_m in self.towers:
            tower_m.draw(self.screen_surface)
        
        if self.anim_disk:
            self.anim_disk.draw(self.screen_surface)
        
        if self.holding_disk:
            # 获取当前选中柱子的中心x坐标
            tower_x = self.towers[self.selected_tower].x
            # 设置盘子的位置：x为柱子中心，y固定为100
            self.holding_disk.rect.center = (tower_x, 100)
            self.holding_disk.draw(self.screen_surface)
    

