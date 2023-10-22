from init import *



while settings_.running:


    # FPS
    settings_.clock.tick(settings_.FPS)


    # Обработчик событий
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            settings_.running = False

        # Управление

        # Получение нажатых клавиш
        k_pressed = pygame.key.get_pressed()

        settings_.k_control.creature_control(settings_.c_viewer.target, k_pressed, event)
        settings__.k_control.creature_control(settings_.available_viewers[0].target, k_pressed, event)
        settings_.k_control.control(k_pressed, event)


    # Обновления спрайтов
    tangiables_sprites = tangiables.sprites()

    players.update(viewer=settings_.c_viewer, tangiables=tangiables_sprites)
    bariers.update(viewer=settings_.c_viewer)


    # Отрисовка

    # Слой заднего фона
    settings_.screen.fill((255,255,255))
    settings_.screen.blit(bg_map, (0 - settings_.c_viewer.delta_x, 0 - settings_.c_viewer.delta_y))

    # Слой малого окружения
    bariers.draw(settings_.screen)

    # Слой существ
    players.draw(settings_.screen)


    # Вывод отрисованного кадра
    pygame.display.flip()


# Выход
pygame.quit()
    