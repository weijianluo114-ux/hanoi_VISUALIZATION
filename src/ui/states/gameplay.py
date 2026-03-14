import pygame     #游戏包

# 导入自定义组件
from ..components import tower_m
from ..components import disk_m
from ...solution import solution_m

class gameplay(object):
    """docstring for gameplay."""
    def __init__(self, screen, font, num_disks, num_towers, first_ticks):
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
        self.time_str = '0.00'      #需要显示的时间数
        self.implication_str = ''   #对应要显示的提示文字
        self.solution1 = solution_m.solution()
        self.solution_start = 0         #解题开始标志位
        self.solution_total_step = 0      #记录解题总步骤
        self.solution_step = 0      #记录解题步骤
        self.total_ticks = 0        #记录总程序运行时间
        self.first_ticks = first_ticks  #记录最初时的时间戳
        self.move_step = 0      #移动盘子时记录状态机的参数
        self.solution_speed = 200   #解题速度设置，越小越快
        
        
        
        # 初始化所有柱子(根据柱子的数量添加)
        self.towers = []
        for tower_x in range(self.num_towers):
            x_center = ((tower_x+1)*(self.width))/(self.num_towers+1)
            tower = tower_m.Tower(self.screen_surface, x_center, 700, 20, 400, 240, 40, self.num_disks, tower_x, )
            self.towers.append(tower)

        # 初始化所有盘子
        self.disks = []
        disk_font = pygame.font.SysFont('SimHei', 15)   #序号字体
        for disk_size in range(self.num_disks, 0, -1):  # disk_size 从 self.num_disks 递减到 1
            disk_color = (100, 200, 255 - disk_size * (200/self.num_disks))   # 示例：颜色随大小变化（蓝色调）
            disk = disk_m.Disk(disk_size, disk_color, disk_font, height=30)
            self.disks.append(disk)
        
        # 将所有盘子加到第一根柱子（索引0）
        for disk in self.disks:
            self.towers[0].add_disk(disk)
        
        #用于存放查看提示的矩形
        self.solution_rect = pygame.Rect(0, 0, 150, 50)     
        self.solution_rect.center = (self.width-150, 50)
    
    def handle_events(self, event, mouse_pos):
        #处理解题问题
        # 处理游戏中的键盘事件，按 ESC 返回菜单
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 0   # 返回主菜单状态 MENU
        # 原有的空格、数字键处理...
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:      #按下左键
                if self.solution_rect.collidepoint(mouse_pos): #检测是否在第一个矩形中，如果是则开始解题
                    if self.solution_start == 0:
                        self.solution_start = 1
                        self.solution_total_step = self.solution1.get_classical_num(self.num_disks)
                        print(self.solution_total_step)
                        self.solution1.clear_solution_dict()
                        self.solution1.recursion(self.num_disks, 0, 1, 2)   #获得答案
                        print(f'答案为：{self.solution1.solution_dict}')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:     #选中第一根柱子
                self.selected_tower = 0
            elif event.key == pygame.K_2:   #选中第二根柱子
                self.selected_tower = 1
            elif event.key == pygame.K_3:   #选中第三根柱子
                self.selected_tower = 2
            elif event.key == pygame.K_SPACE:
                self.move_disks()
            
        return self.win_detect()

    #自动更新并执行
    def solution_update(self):
        if self.solution_start:
            self.solution_untie()

    #定义一个解包解题元组并执行相应操作的方法
    def solution_untie(self):
        current_time = self.total_ticks     #记录上一次的时间
        # print(f'当前时间{current_time}')
        # print(f'上一次的时间{self.first_ticks}')
        if (current_time - self.first_ticks) >= self.solution_speed:
            self.first_ticks = current_time
            if self.solution_step < self.solution_total_step:
                disk_size, origin_tower, taget_tower = self.solution1.solution_dict[self.solution_step]
                #这里可以分三步进行
                #如果进行到第二步则将其转变为状态False并移动
                if self.move_step == 0:
                    self.move_step = 1
                    self.selected_tower = origin_tower  #先将当前盘子拿起来
                    self.move_disks()
                #如果进行到第一步则将其转变为状态True并移动    
                elif self.move_step == 1:
                    self.move_step = 2
                    self.selected_tower = taget_tower
                elif self.move_step == 2:
                    self.move_step = 0
                    self.solution_step += 1
                    print(f'第{self.solution_step}步')
                    self.move_disks()
            elif self.solution_step == self.solution_total_step:    #结束解题
                self.solution_step = 0      #将步骤也清0
                self.solution_start = 0     #将参数置0


    #定义一个移动盘子的方法
    def move_disks(self):
        if self.holding_disk is None:
            # 尝试从当前选中柱子上拿起最上面的盘子
            disk = self.towers[self.selected_tower].remove_disk()
            if disk is not None:
                self.holding_disk = disk
                # 拿起后立即将盘子显示在柱子上方（y=100）
                tower_x = self.towers[self.selected_tower].x
                self.holding_disk.rect.center = (tower_x, self.holding_disk_height)
                print(f"拿起了盘子 {disk.size}")
                self.implication_str = f"拿起了盘子 {disk.size}"
            else:
                print("柱子上没有盘子可拿")
                self.implication_str = "柱子上没有盘子可拿"
        else:
            # 尝试将手中的盘子放到当前选中柱子上
            if self.towers[self.selected_tower].add_disk(self.holding_disk):
                print(f"移动盘子 {self.holding_disk.size} 到柱子 {self.selected_tower+1}")
                self.implication_str = f"移动盘子 {self.holding_disk.size} 到柱子 {self.selected_tower+1}"
                self.holding_disk = None
            else:
                print("无法放置")
                self.implication_str = "无法放置"            

    #定义一个绘制盘子的方法
    def draw_holding_disk(self):
        # 绘制手中盘子
        if self.holding_disk:
            # 获取当前选中柱子的中心x坐标
            tower_x = self.towers[self.selected_tower].x
            # 设置盘子的位置：x为柱子中心，y固定为100
            self.holding_disk.rect.center = (tower_x, self.holding_disk_height)
            self.holding_disk.draw(self.screen_surface)     #绘制

    #定义一个刷新盘子的方法
    def reset(self):
        #清空所有柱子的盘子
        for tower in self.towers:
            tower.disks = []
        # 将所有盘子加到第一根柱子（索引0）
        for disk in self.disks:
            self.towers[0].add_disk(disk)

    #检测获胜方法
    def win_detect(self):
        last_tower = self.towers[-1]
        if len(last_tower.disks) == self.num_disks:
            return 5
        return 1    #1为游玩态
        
    #时间累计方法
    def time_accumulate(self, start_ticks):
        #首先检测获胜
        if self.win_detect() == 5:
            return self.time_str
        #未获得胜利的时候继续计时
        elif self.win_detect() == 1:
            # 计算已经过的秒数
            elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000.0
            # 格式化为小数点后两位
            self.time_str = f"{elapsed_seconds:.2f}"
            return self.time_str
        else:
            return '0.00'

    #绘制对应屏幕方法
    def draw(self):
        self.screen_surface.fill((255,255,255))     #清屏
        #绘制柱子
        for tower in self.towers:
            tower.draw(self.screen_surface)
        
        # # 绘制手中盘子
        self.draw_holding_disk()

        #绘制时间
        # 渲染文本
        time_text = self.game_font.render(self.time_str, True, (0, 0, 0))
        # 绘制到屏幕
        self.screen_surface.blit(time_text, (10, 10))
        
        #绘制提示
        font = pygame.font.SysFont('SimHei', 20)    #字体类
        # 渲染文本
        str = font.render(self.implication_str, True, (60, 40, 60))
        str_rect = str.get_rect()
        str_rect.center = (self.width/2, 50)
        # 绘制到屏幕
        self.screen_surface.blit(str, str_rect)
        
        #绘制查看解题提示的矩形
        pygame.draw.rect(self.screen_surface, (100, 150, 50), self.solution_rect, border_radius=2)
        pygame.draw.rect(self.screen_surface, (0, 0, 0), self.solution_rect, 2, border_radius=2)     #边框
        font = pygame.font.SysFont('SimHei', 20)    #字体类
        # 渲染文本
        str = font.render('查看步骤', True, (40, 40, 60))
        str_rect = str.get_rect()
        str_rect.center = self.solution_rect.center
        # 绘制到屏幕
        self.screen_surface.blit(str, str_rect)
    

