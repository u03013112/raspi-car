import pygame
import pygame_gui

# 初始化pygame
pygame.init()

# 设置屏幕尺寸
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)

# 设置pygame_gui管理器
manager = pygame_gui.UIManager(screen_size)

# 创建按钮和标签
minus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 270), (50, 50)),
                                            text="-",
                                            manager=manager)

label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((410, 270), (80, 50)),
                                    text="0",
                                    manager=manager)

plus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 270), (50, 50)),
                                           text="+",
                                           manager=manager)

# 主循环
running = True
while running:
    time_delta = pygame.time.Clock().tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == minus_button:
                    label.set_text(str(int(label.text) - 1))
                elif event.ui_element == plus_button:
                    label.set_text(str(int(label.text) + 1))

        manager.process_events(event)

    manager.update(time_delta)

    screen.fill((255, 255, 255))
    manager.draw_ui(screen)

    pygame.display.update()

# 退出pygame
pygame.quit()
