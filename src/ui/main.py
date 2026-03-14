import pygame
import sys

# 从状态文件中调取不同界面状态
from .states import leaderboard, settings, about
from .states.gameplay import gameplay
from .states.menu import menu
from .states.win import win

# 游戏状态常量
MENU = 0
GAMEPLAY = 1
LEADERBOARD = 2
SETTINGS = 3
ABOUT = 4
WIN = 5

# 各种参数
width, height = 1280, 720
num_disks = 4       #盘子的数量
num_towers = 3       #柱子的数量
game_start = 1
start_ticks = 0
first_ticks = pygame.time.get_ticks()

def main():
    global start_ticks, win_time, game_start
    
    pygame.init()   #初始化pygame
    screen = pygame.display.set_mode((width, height))   #屏幕类
    clock = pygame.time.Clock()     #时钟类
    font = pygame.font.SysFont('SimHei', 36)    #字体类
    pygame.display.set_caption("汉诺塔小游戏")  #设置窗口说明
    
    # 初始化混音器
    # 设置音频缓冲区大小为 4096 字节
    pygame.mixer.init(buffer=4096)
    
    # 初始化当前状态
    current_state = MENU
    
    # 初始化各个界面（传入共享资源，如screen, font）
    s_menu = menu(screen)
    s_gameplay = gameplay(screen, font, num_disks, num_towers, first_ticks)   # 游戏界面初始化（创建柱子、盘子等）
    s_win = win(screen)
    # leaderboard.init(screen, font)
    # settings.init(screen, font)
    # about.init(screen, font)
    
    #插入音乐
    sound = None
    music = None
    try:
        # 尝试加载音频文件
        sound = pygame.mixer.Sound(r"assets\真夜中的汉诺塔.mp3")
        pygame.mixer.music.load(r"assets\真夜中的汉诺塔.mp3")
        print("音频加载成功！")
        sound.play()
        pygame.mixer.music.play(loops=-1)  # 无限循环
    except Exception as e:
        # 如果加载失败，使用模拟的音频
        print(f"无法加载音频文件：{e}")
    
    running = True
    while running:
        #获取鼠标位置
        mouse_pos = pygame.mouse.get_pos()
        s_gameplay.total_ticks = pygame.time.get_ticks()
        
        # 事件处理：根据当前状态调用对应模块的handle_events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #菜单栏状态
            elif current_state == MENU:
                new_state = s_menu.handle_events(event, mouse_pos)
                if new_state is not None:
                    current_state = new_state
            #游玩状态        
            elif current_state == GAMEPLAY:                    
                new_state = s_gameplay.handle_events(event, mouse_pos)
                if new_state is not None:
                    current_state = new_state
            #获胜状态
            elif current_state == WIN:
                new_state = s_win.handle_events(event, mouse_pos)
                if new_state is not None:
                    current_state = new_state
            # 其他状态类似...
        
        # 更新逻辑（如果需要，例如动画）
        if current_state == MENU:
            game_start = 1  #处于其它状态时，随时准备游戏
        elif current_state == GAMEPLAY:
            #判断是否是进入这个状态的那一刻
            if game_start == 1: #进入游戏时将该标志位清0
                start_ticks = pygame.time.get_ticks()
                s_gameplay.reset()
                game_start = 0
            
            #这里必须要有这个状态更新
            new_state = s_gameplay.update()     #解题更新，并且更新状态
            if new_state is not None:
                current_state = new_state
            s_win.time_str = s_gameplay.time_accumulate(start_ticks)
        elif current_state == WIN:
            game_start = 1  #处于其它状态时，随时准备游戏
            
        # 绘制
        if current_state == MENU:
            s_menu.draw()
        elif current_state == GAMEPLAY:
            s_gameplay.draw()
        elif current_state == WIN:
            s_win.draw()
        
        # print(current_state)
        
        #设置帧率为60帧
        pygame.display.flip()
        clock.tick(60)
    
    # 当程序不跑时会停止并退出
    pygame.quit()
    # 退出程序
    sys.exit()

if __name__ == "__main__":
    main()




