import pygame

class Disk:
    def __init__(self, size, color, font, height=20):
        self.size = size
        self.color = color
        self.height = height
        self.width = size * 20 + 100   # 根据大小设定宽度
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.font = font  # 保存字体引用

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=3)
        pygame.draw.rect(screen, (0,0,0), self.rect, 2, border_radius=3)   # 黑色边框
        
        # 使用外部传入的字体绘制序号
        text = self.font.render(str(self.size), True, (255, 255, 255))   # 序号字体颜色为白色
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)