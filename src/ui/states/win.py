import pygame     #游戏包

class win(object):
    """_summary_

    Args:
        object (_type_): _description_
    """
    def __init__(self, screen):
        self.screen_surface = screen
        self.font = pygame.font.SysFont('SimHei', 28)    #字体类
        self.width = screen.get_width()     #获取屏幕的宽和高
        self.height = screen.get_height()
        self.image = pygame.image.load(r'assets\生成特定风格图片.bmp')
        self.time_str = '0.00'
        
        #标准化初始矩形和文字
        self.text = ['返回菜单', '重新开始']
        self.text_render = []
        self.select_rect = []
        self.text_rect_list = []

        for i in range(2):      #初始化获胜文字
            self.text_render.append(self.font.render(self.text[i], True, (0,0,0)))
            
        # 初始化矩形参数
        rect_temp = pygame.Rect(0, 0, 300, 70)
        rect_temp.centerx = self.width/2
        for x_num in range(2):
            #生成外框矩形参数
            y_bottom = self.height/2+110
            rect_temp.centery = y_bottom
            rect_temp.centerx = self.width/2-200+x_num*400
            self.select_rect.append(rect_temp.copy())   #列表中的类是引用，需要创建一个新的对象

            # 生成文字矩形参数
            text_rect = self.text_render[-1-x_num].get_rect()
            text_rect.centerx = rect_temp.centerx
            text_rect.centery = y_bottom
            self.text_rect_list.append(text_rect)
            
        
      
    def handle_events(self, event, mouse_pos):
        # 处理菜单中的鼠标按下事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:     #按下左键
                if self.select_rect[0].collidepoint(mouse_pos): #检测是否在第一个矩形中，重新开始游戏
                    return 1
                elif self.select_rect[1].collidepoint(mouse_pos): #检测是否在第二个矩形中，返回菜单
                    return 0
        return None


    def draw(self):
        # self.screen_surface.fill((255,255,255))     #清屏
        
        # 渲染文本
        win_str = f'你过关！时间:{self.time_str}s!'
        win_text = self.font.render(win_str, True, (0, 0, 0))
        # 绘制到屏幕
        win_text_rect = win_text.get_rect()
        # centerx 和 centery 分别设置矩形的中心 x 和 y 坐标
        win_text_rect.center = self.screen_surface.get_rect().center
        self.screen_surface.blit(win_text, win_text_rect)
        
        #绘制返回菜单和重新开始
        for x_num in range(2):
            #生成矩形
            pygame.draw.rect(self.screen_surface, (150, 99, 250), self.select_rect[x_num], border_radius = 10)  #内部矩形
            pygame.draw.rect(self.screen_surface, (0, 0, 0), self.select_rect[x_num], 1, border_radius = 10)    #边框
            
            # 生成文字
            self.screen_surface.blit(self.text_render[-1-x_num], self.text_rect_list[x_num])
            
        
            
        
    