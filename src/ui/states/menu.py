import pygame     #游戏包

class menu(object):
    """_summary_

    Args:
        object (_type_): _description_
    """
    def __init__(self, screen):
        self.screen_surface = screen
        self.font = pygame.font.SysFont('SimHei', 28)    #字体类
        self.width = screen.get_width()     #获取屏幕的宽和高
        self.height = screen.get_height()
        self.text = ['开始', '排行榜', '设置', '关于']
        self.text_render = []
        self.image = pygame.image.load(r'assets\生成特定风格图片.bmp')
        self.select_rect = []
        self.text_rect_list = []

        for i in range(4):      #初始化菜单文字
            self.text_render.append(self.font.render(self.text[i], True, (0,0,0)))
            
        # 初始化矩形参数
        rect_temp = pygame.Rect(0, 0, 300, 70)
        rect_temp.centerx = self.width/2
        for y_num in range(4):
            #生成外框矩形参数
            y_bottom = self.height-100-y_num*100
            rect_temp.centery = y_bottom
            self.select_rect.append(rect_temp.copy())   #列表中的类是引用，需要创建一个新的对象

            # 生成文字参数
            text_rect = self.text_render[-1-y_num].get_rect()
            text_rect.centerx = rect_temp.centerx
            text_rect.centery = y_bottom
            self.text_rect_list.append(text_rect)
            
        
      
    def handle_events(self, event, mouse_pos):
        # 处理菜单中的鼠标按下事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:     #按下左键
                if self.select_rect[0].collidepoint(mouse_pos): #检测是否在第一个矩形中
                    return 1
            
        return None


    def draw(self):
        #生成背景图片
        self.screen_surface.blit(self.image, (0,0))
        
        for y_num in range(4):
            #生成矩形
            pygame.draw.rect(self.screen_surface, (200, 100, 50), self.select_rect[y_num], border_radius = 10)
            # print(self.select_rect)
            pygame.draw.rect(self.screen_surface, (0, 0, 0), self.select_rect[y_num], 1, border_radius = 10)
            
            # 生成文字
            self.screen_surface.blit(self.text_render[-1-y_num], self.text_rect_list[y_num])
            
        
            
        
    