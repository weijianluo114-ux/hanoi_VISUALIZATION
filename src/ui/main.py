import pygame
import sys

# 从状态文件中调取不同界面状态
from states import menu, leaderboard, settings, about
from states.gameplay import gameplay

# 游戏状态常量
MENU = 0
GAMEPLAY = 1
LEADERBOARD = 2
SETTINGS = 3
ABOUT = 4

# 各种参数
width, height = 1280, 720
num_disks = 4       #盘子的数量

def main():
    pygame.init()   #初始化pygame
    screen = pygame.display.set_mode((width, height))   #屏幕类
    clock = pygame.time.Clock()     #时钟类
    font = pygame.font.SysFont('SimHei', 36)    #字体类
    pygame.display.set_caption("汉诺塔小游戏")  #设置窗口说明
    
    # 初始化当前状态
    current_state = GAMEPLAY
    
    # 初始化各个界面（传入共享资源，如screen, font）
    # menu.init(screen, font)
    s_gameplay = gameplay(screen, font, num_disks)   # 游戏界面初始化（创建柱子、盘子等）
    # leaderboard.init(screen, font)
    # settings.init(screen, font)
    # about.init(screen, font)
    
    running = True
    while running:
        # 事件处理：根据当前状态调用对应模块的handle_events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # elif current_state == MENU:
            #     new_state = menu.handle_events(event)
            #     if new_state is not None:
            #         current_state = new_state
            elif current_state == GAMEPLAY:
                new_state = s_gameplay.handle_events(event)
                if new_state is not None:
                    current_state = new_state
            # 其他状态类似...
        
        # 更新逻辑（如果需要，例如动画）
        if current_state == GAMEPLAY:
            s_gameplay.update()
        
        # 绘制
        if current_state == MENU:
            # menu.draw()
            pass
        elif current_state == GAMEPLAY:
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




