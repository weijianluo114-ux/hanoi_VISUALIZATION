import pygame

class menu(object):
    def __init__(self, screen):
        self.screen_surface = screen
        self.font = pygame.font.SysFont('SimHei', 28)
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.image = pygame.image.load(r'assets\16_9.png')

        self.text = ['开始', '排行榜', '设置', '关于']
        self.text_render = []
        self.base_rects = []       # 基础矩形（未放大时）
        self.text_rect_list = []

        for i in range(4):
            self.text_render.append(self.font.render(self.text[i], True, (0, 0, 0)))

        # 初始化矩形位置
        rect_temp = pygame.Rect(0, 0, 300, 70)
        rect_temp.centerx = self.width / 2
        for y_num in range(4):
            y_bottom = self.height - 100 - y_num * 100
            rect_temp.centery = y_bottom
            self.base_rects.append(rect_temp.copy())

            text_rect = self.text_render[-1 - y_num].get_rect()
            text_rect.centerx = rect_temp.centerx
            text_rect.centery = y_bottom
            self.text_rect_list.append(text_rect)

    def handle_events(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # base_rects[3]=开始(顶), [2]=排行榜, [1]=设置, [0]=关于(底)
            if self.base_rects[3].collidepoint(mouse_pos):
                return 6          # 选择盘子数量
            elif self.base_rects[2].collidepoint(mouse_pos):
                return 2          # LEADERBOARD
            elif self.base_rects[1].collidepoint(mouse_pos):
                return 3          # SETTINGS
            elif self.base_rects[0].collidepoint(mouse_pos):
                return 4          # ABOUT
        return None

    def draw(self):
        self.screen_surface.blit(self.image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        hover_index = None
        for i, rect in enumerate(self.base_rects):
            if rect.collidepoint(mouse_pos):
                hover_index = i
                break

        for y_num in range(4):
            rect = self.base_rects[y_num]
            is_hover = (y_num == hover_index)

            if is_hover:
                # 悬停：放大 + 变色
                scale_w, scale_h = 340, 82
                big_rect = pygame.Rect(0, 0, scale_w, scale_h)
                big_rect.center = rect.center
                color = (255, 160, 60)
                border_color = (200, 100, 20)
                shadow_offset = 6

                # 阴影
                shadow_rect = big_rect.copy()
                shadow_rect.x += shadow_offset
                shadow_rect.y += shadow_offset
                pygame.draw.rect(self.screen_surface, (80, 40, 10, 60),
                                 shadow_rect, border_radius=12)
                # 主矩形
                pygame.draw.rect(self.screen_surface, color, big_rect, border_radius=12)
                pygame.draw.rect(self.screen_surface, border_color, big_rect, 3, border_radius=12)

                # 文字居中于放大后的矩形
                text_surf = self.text_render[-1 - y_num]
                text_rect = text_surf.get_rect(center=big_rect.center)
                self.screen_surface.blit(text_surf, text_rect)
            else:
                # 普通状态
                base_color = (200, 100, 50)
                pygame.draw.rect(self.screen_surface, base_color, rect, border_radius=10)
                pygame.draw.rect(self.screen_surface, (0, 0, 0), rect, 1, border_radius=10)
                self.screen_surface.blit(self.text_render[-1 - y_num], self.text_rect_list[y_num])