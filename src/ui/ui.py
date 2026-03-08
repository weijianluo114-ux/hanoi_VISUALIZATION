import pygame     #游戏包
import sys  #用于退出系统

from .components import tower_m
from .components import disk_m

# 参数
width, height = 1280, 720
num_disks = 4       #盘子的数量



#初始化pygam
pygame.init()

# 设置窗口大小和标题
# set_mode 函数参数：(width, height)，返回一个 Surface 对象
# 400x300 表示窗口宽度为 400 像素，高度为 300 像素
screen = pygame.display.set_mode((width, height))

# set_caption 函数设置窗口标题
pygame.display.set_caption("汉诺塔小游戏")

clock = pygame.time.Clock()     #帧率设置

# 设置字体
# font.SysFont 函数参数：字体名称，字体大小
# None 表示使用默认字体，36 表示字体大小为 36
font = pygame.font.SysFont('SimHei', 36)

# 柱子类
towers = [
    tower_m.Tower(320, 700, 20, 400, 240, 40, num_disks),
    tower_m.Tower(640, 700, 20, 400, 240, 40, num_disks),
    tower_m.Tower(960, 700, 20, 400, 240, 40, num_disks)
]

# 盘子类
disks = []
disk_font = pygame.font.SysFont('SimHei', 15)   #序号字体
for disk_size in range(num_disks, 0, -1):  # disk_size 从 num_disks 递减到 1
    disk_color = (100, 200, 255 - disk_size * (200/num_disks))   # 示例：颜色随大小变化（蓝色调）
    disk = disk_m.Disk(disk_size, disk_color, disk_font, height=30)
    disks.append(disk)

# 将所有盘子加到第一根柱子（索引0）
for disk in disks:
    towers[0].add_disk(disk)
    
selected_tower = 0      # 初始选中第一根柱子
holding_disk = None     # 手中没有盘子

# 添加矩形移动的动画
# 动画相关变量
anim_disk = None           # 当前正在移动的盘子对象
anim_progress = 0.0        # 动画进度 0~1
anim_speed = 0.06          # 每帧进度增量（控制动画速度）
anim_start_pos = (0, 0)    # 起始位置（屏幕坐标）
anim_end_pos = (0, 0)      # 结束位置（屏幕坐标）

# 游戏主循环
running = True
while running:
                     
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
            # 退出 pygame
            pygame.quit()
            # 退出程序
            sys.exit()
        elif anim_disk is not None:
            # 动画期间忽略所有操作（除了退出）
            continue  # 或直接跳过事件处理
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:     #选中第一根柱子
                selected_tower = 0
            elif event.key == pygame.K_2:   #选中第二根柱子
                selected_tower = 1
            elif event.key == pygame.K_3:   #选中第三根柱子
                selected_tower = 2
            elif event.key == pygame.K_SPACE:
                if holding_disk is None:
                    # 尝试从当前选中柱子上拿起最上面的盘子
                    disk = towers[selected_tower].remove_disk()
                    if disk is not None:
                        holding_disk = disk
                        # 拿起后立即将盘子显示在柱子上方（y=100）
                        tower_x = towers[selected_tower].x
                        holding_disk.rect.center = (tower_x, 100)
                        print(f"拿起了盘子 {disk.size}")
                    else:
                        print("柱子上没有盘子可拿")
                else:
                    # 尝试将手中的盘子放到当前选中柱子上
                    if towers[selected_tower].can_add_disk(holding_disk):
                        # 开始动画：记录起始位置（当前空中位置）和目标位置（目标柱顶部）
                        anim_disk = holding_disk
                        anim_start_pos = holding_disk.rect.center
                        # 计算目标柱顶部中心坐标
                        target_tower = towers[selected_tower]
                        target_x = target_tower.x
                        target_y = target_tower.y - target_tower.base_height - (len(target_tower.disks)) * anim_disk.height
                        anim_end_pos = (target_x, target_y)
                        # 初始化进度
                        anim_progress = 0.0
                        # 清空手中盘子，准备动画
                        holding_disk = None
                        print(f"开始移动盘子 {anim_disk.size} 到柱子 {selected_tower+1}")
                    else:
                        print("不能放在这里，规则不允许")
    
    # 更新动画进度
    if anim_disk is not None:
        anim_progress += anim_speed
        if anim_progress >= 1.0:
            anim_progress = 1.0
            # 动画完成：将盘子放入目标柱子
            towers[selected_tower].add_disk(anim_disk)  # 注意：目标柱子是当前选中的
            anim_disk = None
        else:
            # 根据进度插值计算当前帧的位置
            print(anim_start_pos, ' ', anim_end_pos, ' ', anim_progress)
            current_x = anim_start_pos[0] + (anim_end_pos[0] - anim_start_pos[0]) * anim_progress
            current_y = anim_start_pos[1] + (anim_end_pos[1] - anim_start_pos[1]) * anim_progress
            anim_disk.rect.center = (current_x, current_y)

    if anim_disk:
        anim_disk.draw(screen)
    
    screen.fill((255, 255, 255))  # 清屏
    for tower_m in towers:
        tower_m.draw(screen)
    
    if anim_disk:
        anim_disk.draw(screen)
    
    if holding_disk:
        # 获取当前选中柱子的中心x坐标
        tower_x = towers[selected_tower].x
        # 设置盘子的位置：x为柱子中心，y固定为100
        holding_disk.rect.center = (tower_x, 100)
        holding_disk.draw(screen)
    
    # 更新屏幕
    # flip 函数将绘制的内容显示到屏幕上
    pygame.display.flip()
    
    clock.tick(60)  # 限制帧率为 60 FPS
    # 可以获取实际帧率
    fps = clock.get_fps()
    # print(f"当前帧率：{fps:.2f} FPS")

