import pygame     #游戏包

# 导入自定义组件
from ..components import tower_m
from ..components import disk_m
from ...solution import solution_m
from ..components.get_graph import build_state_graph

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
        self.solution_speed = 250   #解题速度设置，越小越快
        
        self.right_ratio = 3/5  #分屏比例
        self.left_ratio = 1.0 - self.right_ratio
        
        self.disk_states = [0 for i in range(num_disks)]    #初始化所有盘子的状态，0表示第0个柱子，索引代表第几个盘子
        
        # 在 __init__ 末尾，建立状态图后面，添加：
        self.graph_initialized = False   # 标志：是否已构建布局
        self.path_to_target = []   # 存储最短路径的状态序列，格式 [(0,0,0), ..., (2,2,2)]
        self.graph_surface = None        # 预渲染的状态图表面
        self.graph_positions = None      # 所有状态的位置字典
        self.graph_left = 0
        self.graph_top = 0
        
        self.pending_victory = False   # 胜利延迟一帧标志
        
        # 初始化所有柱子(根据柱子的数量添加)
        self.towers = []
        for tower_x in range(self.num_towers):
            x_center = ((tower_x+1)*(self.width*(self.right_ratio)))/(self.num_towers+1)
            tower = tower_m.Tower(self.screen_surface, x_center, 900, 20, 400, 240, 40, self.num_disks, tower_x, )
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
        
        # 建立状态图
        self.graph = build_state_graph(self.num_disks)
        # ★ 同步初始状态
        self.update_disk_states()
        # print(f"初始状态: {self.disk_states}")
    
    def handle_events(self, event, mouse_pos):
        #处理解题问题
        # 处理游戏中的键盘事件，按 ESC 返回菜单
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # ★ 重置所有状态
            self.reset()
            self.solution_start = 0
            self.solution_step = 0
            self.move_step = 0
            self.holding_disk = None
            self.implication_str = ''
            return 0   # 返回主菜单状态 MENU
        # 原有的空格、数字键处理...
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:      #按下左键
                if self.solution_rect.collidepoint(mouse_pos): #检测是否在第一个矩形中，如果是则开始解题
                    if self.solution_start == 0:
                        # ★ 重置游戏到初始状态
                        self.reset()
                        # ★ 重置解题相关参数
                        self.solution_step = 0
                        self.move_step = 0
                        self.solution_start = 1
                        self.solution_total_step = self.solution1.get_classical_num(self.num_disks)
                        print(self.solution_total_step)
                        # ★ 重置计时器，让第一步立即执行
                        self.first_ticks = self.total_ticks - self.solution_speed
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
        return 1

    def update_disk_states(self):
        """根据当前所有柱子上的盘子，更新 disk_states"""
        # 重置为 -1（确保能看到未正确设置的情况）
        self.disk_states = [-1] * self.num_disks
        for tower_idx, tower in enumerate(self.towers):
            for disk in tower.disks:
                # disk.size 范围 [1, num_disks]，减1转为0-based索引
                self.disk_states[disk.size - 1] = tower_idx
        # 盘子放下后，自动计算到目标的最短路径
        self.find_shortest_path_bfs()

    #自动更新并执行
    def update(self):
        if self.solution_start:
            self.solution_untie()
        return self.win_detect()

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
                self.move_step = 0          # ★ 复位移动状态机


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
                # ★ 只有放下盘子后才更新状态
                self.update_disk_states()
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
        # ★ 重置后同步
        self.update_disk_states()
        
        # ★ 只在第一次进入 GAMEPLAY 时构建状态图
        if not self.graph_initialized:
            self.build_graph_layout()
            self.graph_initialized = True

    def win_detect(self):
        last_tower = self.towers[-1]
        if len(last_tower.disks) == self.num_disks:
            if not self.pending_victory:
                # 第一次检测到全部归位 → 标记但不判定，确保这一帧先 draw
                self.pending_victory = True
                return 1    # 依然返回游玩态
            return 5        # 下一帧才真正判定胜利
        self.pending_victory = False
        return 1            # 1为游玩态
        
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

    def compute_sierpinski_position(self, state, corners, level, prev_disk=None):
        """
        递归计算汉诺塔状态在谢尔宾斯基三角形中的唯一位置
        state: tuple, (d0, d1, ..., d_{n-1})，d0是最小盘子
        corners: (left, right, top) — left=tower0, right=tower2, top=tower1
        level: 还有多少层需要细分（从 n 递减到 0）
        flip: 是否在本次递归中先进行水平翻转（偶数层递归为 True）
        prev_disk: 上一层的 disk 值，决定了翻转轴通过哪个顶点
        """
        left, right, top = corners

        if level == 0:
            # 所有盘子都处理完，返回当前子三角形的重心
            return ((left[0] + right[0] + top[0]) / 3.0,
                    (left[1] + right[1] + top[1]) / 3.0)

        # ── 偶数层递归：先水平翻转整个三角形 ──
        if prev_disk is not None:
            # 以"进入的子三角形的顶点"与"中心"的连线为轴进行水平翻转，
            # 等价于交换除 prev_disk 对应顶点外的另外两个顶点
            if prev_disk == 0:          # 轴通过左顶点 → 交换右顶点和上顶点
                right, top = top, right
            elif prev_disk == 1:        # 轴通过上顶点 → 交换左顶点和右顶点
                left, right = right, left
            else:                       # 轴通过右顶点 → 交换左顶点和上顶点
                left, top = top, left

        # state[-1] 是当前层要处理的盘子（从大到小）
        disk = state[-1]

        # 三条边的中点
        mid_bottom = ((left[0] + right[0]) / 2.0, (left[1] + right[1]) / 2.0)
        mid_left   = ((left[0] + top[0]) / 2.0,   (left[1] + top[1]) / 2.0)
        mid_right  = ((right[0] + top[0]) / 2.0,  (right[1] + top[1]) / 2.0)

        if disk == 0:   # 左下子三角形
            new_corners = (left, mid_bottom, mid_left)
        elif disk == 1: # 顶部子三角形
            new_corners = (mid_left, mid_right, top)
        else:           # 右下子三角形
            new_corners = (mid_bottom, right, mid_right)

        # 递归：flip 取反，并传递当前 disk 作为下一层的 prev_disk
        return self.compute_sierpinski_position(
            state[:-1], new_corners, level - 1, disk
        )
    
    def build_graph_layout(self):
        """构建状态图布局并预渲染到表面（仅调用一次）"""
        n = self.num_disks

        # 右侧绘制区域
        graph_left = int(self.width * self.right_ratio)
        graph_right = self.width
        graph_top = 0
        graph_bottom = self.height
        graph_width = graph_right - graph_left
        graph_height = graph_bottom - graph_top

        # 正立三角形的三个顶点
        margin = 0
        cx = graph_width / 2
        cy = graph_height / 2
        tri_radius = min(graph_width, graph_height) / 2 - margin

        # left=tower0(左下), right=tower2(右下), top=tower1(顶部)
        left = (cx - tri_radius * 0.866, cy + tri_radius * 0.5)
        right = (cx + tri_radius * 0.866, cy + tri_radius * 0.5)
        top = (cx, cy - tri_radius)

        corners = (left, right, top)

        # 计算所有状态的位置
        all_states = list(self.graph.keys())
        self.graph_positions = {}
        for state in all_states:
            self.graph_positions[state] = self.compute_sierpinski_position(state, corners, n)

        # 创建表面并预绘制
        self.graph_surface = pygame.Surface((graph_width, graph_height), pygame.SRCALPHA)
        self.graph_surface.fill((245, 245, 245))

        # 绘制所有边（无向图，state < neighbor 避免重复）
        for state, neighbors in self.graph.items():
            p1 = self.graph_positions[state]
            for neighbor in neighbors:
                if state < neighbor:  # 每条边只画一次
                    p2 = self.graph_positions[neighbor]
                    pygame.draw.line(self.graph_surface, (180, 180, 180), p1, p2, 2)

        # ★ 调试：打印所有状态及其坐标
        # print(f"=== 共 {len(all_states)} 个状态 ===")
        # for state, pos in sorted(self.graph_positions.items()):
        #     print(f"状态 {''.join(str(d) for d in state)} → ({pos[0]:.2f}, {pos[1]:.2f})")

        # 绘制所有节点圆和文字
        # node_radius = 16
        # font_size = 13
        
        node_radius = min((max(8, int(128 / (2 ** (n - 1))))),(50))
        font_size = min((max(6, int(96 / (2 ** (n - 1))))),(38))   # 字号同步缩小
        font = pygame.font.SysFont('SimHei', font_size)
        for state, pos in self.graph_positions.items():
            # 画圆
            pygame.draw.circle(self.graph_surface, (100, 130, 200),
                            (int(pos[0]), int(pos[1])), node_radius)
            # 绘制状态文字（如 "000"、"210"）
            text_str = ''.join(str(d) for d in state)
            text_surf = font.render(text_str, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(int(pos[0]), int(pos[1])))
            self.graph_surface.blit(text_surf, text_rect)

        self.graph_left = graph_left
        self.graph_top = graph_top
        self.graph_node_radius = node_radius
        print(f"状态图已生成，共 {len(all_states)} 个状态")


    def draw_current_state_on_graph(self):
        """在状态图上高亮当前盘子的状态"""
        current_state = tuple(self.disk_states)
        if current_state in self.graph_positions:
            pos = self.graph_positions[current_state]
            screen_x = int(pos[0] + self.graph_left)
            screen_y = int(pos[1] + self.graph_top)
            r = self.graph_node_radius + 3
            # 红色高亮圆圈
            pygame.draw.circle(self.screen_surface, (255, 50, 50), (screen_x, screen_y), r)
            pygame.draw.circle(self.screen_surface, (255, 0, 0), (screen_x, screen_y), r - 2)
            # ★ 高亮文字字体随 node_radius 动态变化（比普通节点文字大 2 号）
            highlight_font_size = max(8, self.graph_node_radius - 2)
            font = pygame.font.SysFont('SimHei', highlight_font_size)
            text_str = ''.join(str(d) for d in current_state)
            text_surf = font.render(text_str, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(screen_x, screen_y))
            self.screen_surface.blit(text_surf, text_rect)

    def draw_shortest_path(self):
        """在状态图上用黄色高亮最短路径的边和节点"""
        if not self.path_to_target or len(self.path_to_target) < 2:
            return

        # --- 绘制黄色连线 ---
        for i in range(len(self.path_to_target) - 1):
            p1 = self.graph_positions[self.path_to_target[i]]
            p2 = self.graph_positions[self.path_to_target[i + 1]]
            screen_p1 = (int(p1[0] + self.graph_left), int(p1[1] + self.graph_top))
            screen_p2 = (int(p2[0] + self.graph_left), int(p2[1] + self.graph_top))
            pygame.draw.line(self.screen_surface, (255, 235, 120), screen_p1, screen_p2, 5)

        # --- 绘制黄色节点圆 + 文字（只画一次！）---
        label_font = pygame.font.SysFont('SimHei', max(8, self.graph_node_radius - 2))
        for i, state in enumerate(self.path_to_target):
            if i == 0:      # 起点保留红色高亮
                continue
            pos = self.graph_positions[state]
            screen_x = int(pos[0] + self.graph_left)
            screen_y = int(pos[1] + self.graph_top)
            r = self.graph_node_radius + 2

            # 浅黄圆
            pygame.draw.circle(self.screen_surface, (255, 230, 100), (screen_x, screen_y), r)
            pygame.draw.circle(self.screen_surface, (255, 245, 180), (screen_x, screen_y), r - 2)

            # 文字用深色，在浅黄底上才看得清
            text_str = ''.join(str(d) for d in state)
            text_surf = label_font.render(text_str, True, (60, 60, 60))
            text_rect = text_surf.get_rect(center=(screen_x, screen_y))
            self.screen_surface.blit(text_surf, text_rect)

    def find_shortest_path_bfs(self):
        """BFS 查找当前 disk_states 到目标 (全在2号柱) 的最短路径"""
        target = tuple([2] * self.num_disks)
        start = tuple(self.disk_states)

        if start == target:
            self.path_to_target = [start]
            return

        visited = {start}
        queue = [(start, [start])]          # (当前状态, 到该状态的路径)

        while queue:
            current, path = queue.pop(0)
            for neighbor in self.graph[current]:   # 遍历所有可达邻居
                if neighbor == target:
                    self.path_to_target = path + [neighbor]
                    return
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        # 理论上汉诺塔图是连通的，不会走到这里
        self.path_to_target = []
    
    #绘制对应屏幕方法
    def draw(self):
        self.screen_surface.fill((255,255,255))     #清屏
        #绘制柱子
        for tower in self.towers:
            tower.draw(self.screen_surface)
        
        # # 绘制手中盘子
        self.draw_holding_disk()

        # ★ 绘制右侧状态图
        if self.graph_surface:
            self.screen_surface.blit(self.graph_surface, (self.graph_left, self.graph_top))
            self.draw_shortest_path()              # ← 先画路径（在底层）
            self.draw_current_state_on_graph()

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
    

