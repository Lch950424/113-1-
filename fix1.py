# 顯示遊戲畫面
def draw_game():
    screen.fill(BLACK)

    # 如果血量歸零，顯示 Game Over 並停止遊戲
    if current_health <= 0:
        font = pygame.font.SysFont(None, 50)
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        return True  # 結束遊戲

    # 改變玩家顏色為無敵顏色
    player_color = GREEN if not invincible else INVINCIBLE_COLOR

    # 畫玩家
    pygame.draw.rect(screen, player_color, player_rect)

    # 畫敵人
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # 畫子彈
    for bullet in bullets:
        pygame.draw.rect(screen, BLUE, bullet['rect'])

    # 顯示血量
    health_bar_width = 200
    health_bar_height = 20
    health_bar_x = 10
    health_bar_y = 10
    pygame.draw.rect(screen, WHITE, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, HEALTH_COLOR, (health_bar_x, health_bar_y, (current_health / MAX_HEALTH) * health_bar_width, health_bar_height))

    # 顯示血量數字
    font = pygame.font.SysFont(None, 30)
    health_text = font.render(f"HP: {current_health}", True, WHITE)
    screen.blit(health_text, (health_bar_x + health_bar_width + 10, health_bar_y))

    pygame.display.flip()
    return False  # 遊戲繼續進行
