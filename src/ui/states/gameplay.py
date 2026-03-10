import pygame     #游戏包

# 导入自定义组件
from ..components import tower_m
from ..components import disk_m

class gameplay(object):
    """docstring for gameplay."""
    def __init__(self, screen, font, num_disks, num_towers):
        super(gameplay, self).__init__()
        self.screen_surface = screen
        self.game_font = font
        self.selected_tower = 0      # 初始选中第一根柱子
        self.holding_disk = None     # 手中没有盘子
        self.num_disks = num_disks
        self.num_towers = num_towers
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.holding_disk_height = 180      #拿起的柱子的高度
        self.start_ticks = 0.0
        self.time_str = None
        self.time_continue = 1
        
        
        # 柱子类(根据柱子的数量添加)
        self.towers = []
        for tower_x in range(self.num_towers):
            x_center = ((tower_x+1)*(self.width))/(self.num_towers+1)
            tower = tower_m.Tower(self.screen_surface, x_center, 700, 20, 400, 240, 40, self.num_disks, tower_x, )
            self.towers.append(tower)

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:     #选中第一根柱子
                self.selected_tower = 0
            elif event.key == pygame.K_2:   #选中第二根柱子
                self.selected_tower = 1
            elif event.key == pygame.K_3:   #选中第三根柱子
                self.selected_tower = 2
            elif event.key == pygame.K_SPACE:
                if self.holding_disk is None:
                    # 尝试从当前选中柱子上拿起最上面的盘子
                    disk = self.towers[self.selected_tower].remove_disk()
                    if disk is not None:
                        self.holding_disk = disk
                        # 拿起后立即将盘子显示在柱子上方（y=100）
                        tower_x = self.towers[self.selected_tower].x
                        self.holding_disk.rect.center = (tower_x, self.holding_disk_height)
                        print(f"拿起了盘子 {disk.size}")
                    else:
                        print("柱子上没有盘子可拿")
                else:
                    # 尝试将手中的盘子放到当前选中柱子上
                    if self.towers[self.selected_tower].add_disk(self.holding_disk):
                        print(f"移动盘子 {self.holding_disk.size} 到柱子 {self.selected_tower+1}")
                        self.holding_disk = None
                    else:
                        print("不能放在这里，规则不允许")
        return None

    def win_detect(self):
        last_tower = self.towers[-1]
        if len(last_tower.disks) == self.num_disks:
            return 1
        return 0
        

    def time_accumulate(self, start_ticks):
        if self.win_detect():
            #将时间暂停
            self.time_continue = 0
        if self.time_continue == 1:
            # 计算已经过的秒数
            elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000.0
            # 格式化为小数点后两位
            self.time_str = f"{elapsed_seconds:.2f}"
        else:
            pass
        

    def draw(self):
        if self.win_detect():            
            self.screen_surface.fill((255,255,255))     #清屏
            # 渲染文本
            win_str = f'你过关！通关时间为:{self.time_str}s!'
            win_text = self.game_font.render(win_str, True, (0, 0, 0))
            # 绘制到屏幕
            win_text_rect = win_text.get_rect()
            # centerx 和 centery 分别设置矩形的中心 x 和 y 坐标
            win_text_rect.center = self.screen_surface.get_rect().center
            self.screen_surface.blit(win_text, win_text_rect)
        else:
            self.screen_surface.fill((255,255,255))     #清屏
            for tower in self.towers:
                tower.draw(self.screen_surface)
            
            # 绘制手中盘子
            if self.holding_disk:
                # 获取当前选中柱子的中心x坐标
                tower_x = self.towers[self.selected_tower].x
                # 设置盘子的位置：x为柱子中心，y固定为100
                self.holding_disk.rect.center = (tower_x, self.holding_disk_height)
                self.holding_disk.draw(self.screen_surface)     #绘制

            #绘制时间
            # 渲染文本
            time_text = self.game_font.render(self.time_str, True, (0, 0, 0))
            # 绘制到屏幕
            self.screen_surface.blit(time_text, (10, 10))
            
        
        
    

