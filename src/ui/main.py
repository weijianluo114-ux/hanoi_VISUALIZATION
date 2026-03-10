import pygame
import sys

# 从状态文件中调取不同界面状态
from .states import leaderboard, settings, about
from .states.gameplay import gameplay
from .states.menu import menu

# 游戏状态常量
MENU = 0
GAMEPLAY = 1
LEADERBOARD = 2
SETTINGS = 3
ABOUT = 4

# 各种参数
width, height = 1280, 720
num_disks = 2       #盘子的数量
num_towers = 3       #柱子的数量
start_time_flag = 0.0     #开始计时的标志参数

def main():
    global start_time_flag, start_ticks
    
    pygame.init()   #初始化pygame
    screen = pygame.display.set_mode((width, height))   #屏幕类
    clock = pygame.time.Clock()     #时钟类
    font = pygame.font.SysFont('SimHei', 36)    #字体类
    pygame.display.set_caption("汉诺塔小游戏")  #设置窗口说明
    
    # 初始化当前状态
    current_state = MENU
    
    # 初始化各个界面（传入共享资源，如screen, font）
    s_menu = menu(screen)
    s_gameplay = gameplay(screen, font, num_disks, num_towers)   # 游戏界面初始化（创建柱子、盘子等）
    # leaderboard.init(screen, font)
    # settings.init(screen, font)
    # about.init(screen, font)
    
    running = True
    while running:
        #获取鼠标位置
        mouse_pos = pygame.mouse.get_pos()
        
        # 事件处理：根据当前状态调用对应模块的handle_events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif current_state == MENU:
                new_state = s_menu.handle_events(event, mouse_pos)
                if new_state is not None:
                    current_state = new_state
                if new_state == GAMEPLAY and start_time_flag == 0:
                    start_time_flag = 1
                    start_ticks = pygame.time.get_ticks()
            elif current_state == GAMEPLAY:
                new_state = s_gameplay.handle_events(event)
                if new_state is not None:
                    current_state = new_state
            # 其他状态类似...
        
        # 更新逻辑（如果需要，例如动画）

        # 绘制
        if current_state == MENU:
            s_menu.draw()
        elif current_state == GAMEPLAY:
            s_gameplay.time_accumulate(start_ticks)
            s_gameplay.draw()
            
        # ...
        
        #设置帧率为60帧
        pygame.display.flip()
        clock.tick(60)
    
    # 当程序不跑时会停止并退出
    pygame.quit()
    # 退出程序
    sys.exit()

if __name__ == "__main__":
    main()




