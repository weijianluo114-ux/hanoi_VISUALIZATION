import pygame

class leaderboard(object):
    def __init__(self, screen, font):
        self.screen_surface = screen
        self.font = font
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.image = pygame.image.load(r'assets\16_9.png')

        self.info_text = font.render("敬请期待", True, (80, 80, 80))
        self.info_rect = self.info_text.get_rect(center=(self.width // 2, self.height // 2 - 40))

        self.back_text = pygame.font.SysFont('SimHei', 28).render("返回菜单", True, (0, 0, 0))
        self.back_rect = pygame.Rect(0, 0, 200, 60)
        self.back_rect.center = (self.width // 2, self.height // 2 + 60)
        self.back_text_rect = self.back_text.get_rect(center=self.back_rect.center)

    def handle_events(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_rect.collidepoint(mouse_pos):
                return 0
        return None

    def draw(self):
        self.screen_surface.blit(self.image, (0, 0))
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen_surface.blit(overlay, (0, 0))

        self.screen_surface.blit(self.info_text, self.info_rect)

        pygame.draw.rect(self.screen_surface, (180, 120, 60), self.back_rect, border_radius=8)
        pygame.draw.rect(self.screen_surface, (0, 0, 0), self.back_rect, 2, border_radius=8)
        self.screen_surface.blit(self.back_text, self.back_text_rect)