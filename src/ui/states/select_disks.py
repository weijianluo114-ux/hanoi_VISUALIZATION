import pygame

class select_disks(object):
    """盘子数量选择界面"""
    def __init__(self, screen):
        self.selected_number = None   # 记录选中的数字
        self.screen_surface = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font = pygame.font.SysFont('SimHei', 72)       # 大数字
        self.title_font = pygame.font.SysFont('SimHei', 42)  # 标题
        self.info_font = pygame.font.SysFont('SimHei', 24)   # 提示文字

        # 背景图（与菜单共用）
        self.background = pygame.image.load(r'assets\16_9.png')

        # === 计算 2×2 网格位置 ===
        self.cell_size = 130          # 格子边长
        self.cell_gap = 50            # 格子间距
        self.grid_width = 2 * self.cell_size + self.cell_gap
        self.grid_height = 2 * self.cell_size + self.cell_gap
        self.grid_left = (self.width - self.grid_width) // 2
        self.grid_top = (self.height - self.grid_height) // 2

        # === 初始化 4 个格子 ===
        # 颜色方案：按 1~4 分别用红、绿、蓝、金色
        self.color_scheme = [
            (220, 80, 80),    # 1 - 红色
            (80, 190, 80),    # 2 - 绿色
            (70, 130, 220),   # 3 - 蓝色
            (230, 180, 50),   # 4 - 金色
        ]

        self.cells = []
        for i in range(4):
            number = i + 1
            col = i % 2
            row = i // 2
            x = self.grid_left + col * (self.cell_size + self.cell_gap)
            y = self.grid_top + row * (self.cell_size + self.cell_gap)

            rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            base_color = self.color_scheme[i]
            hover_color = tuple(min(c + 50, 255) for c in base_color)

            text = self.font.render(str(number), True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)

            self.cells.append({
                'rect': rect,
                'number': number,
                'text': text,
                'text_rect': text_rect,
                'base_color': base_color,
                'hover_color': hover_color,
                'is_hovered': False,
            })

        # === 标题文字 ===
        self.title_text = self.title_font.render("请选择盘子数量", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(
            center=(self.width // 2, self.grid_top - 70)
        )

        # === 底部提示 ===
        self.info_text = self.info_font.render("点击数字开始游戏", True, (200, 200, 200))
        self.info_rect = self.info_text.get_rect(
            center=(self.width // 2, self.grid_top + self.grid_height + 60)
        )

    def handle_events(self, event, mouse_pos):
        """返回 True 表示已选择，False/None 表示未选择"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for cell in self.cells:
                if cell['rect'].collidepoint(mouse_pos):
                    self.selected_number = cell['number']   # ← 存到属性
                    return True
        return False

    def update(self, mouse_pos):
        """更新悬停状态"""
        for cell in self.cells:
            cell['is_hovered'] = cell['rect'].collidepoint(mouse_pos)

    def draw(self):
        """绘制界面"""
        # 1. 绘制背景
        self.screen_surface.blit(self.background, (0, 0))

        # 2. 半透明蒙版（让文字更清晰）
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen_surface.blit(overlay, (0, 0))

        # 3. 绘制标题
        self.screen_surface.blit(self.title_text, self.title_rect)

        # 4. 绘制 4 个格子
        for cell in self.cells:
            color = cell['hover_color'] if cell['is_hovered'] else cell['base_color']
            rect = cell['rect']

            # 圆角矩形背景
            pygame.draw.rect(self.screen_surface, color, rect, border_radius=18)
            # 白色边框
            pygame.draw.rect(self.screen_surface, (255, 255, 255), rect, 3, border_radius=18)
            # 数字
            self.screen_surface.blit(cell['text'], cell['text_rect'])

        # 5. 绘制底部提示
        self.screen_surface.blit(self.info_text, self.info_rect)