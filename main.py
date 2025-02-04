import pygame
import sys
import sqlite3

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)

pygame.mixer.music.load("calm_music.mp3")
pygame.mixer.music.set_volume(0.5)

music_enabled = True

player1_name = ""
player2_name = ""

board = [["", "", ""], ["", "", ""], ["", "", ""]]
current_player = "X"
game_over = False
winner = None

animation_data = {}


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def get_records_from_db():
    """Получает данные из SQL-таблицы"""
    conn = sqlite3.connect('records.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, wins, draws, losses FROM records")
    records = cursor.fetchall()
    conn.close()
    return records


def draw_table(surface, records, x, y, cell_width, cell_height):
    """Отрисовывает таблицу с данными"""
    headers = ["Имя", "Победы", "Ничьи", "Поражения"]
    for i, header in enumerate(headers):
        draw_text(header, small_font, BLACK, surface, x + i * cell_width + cell_width // 2, y - 30)

    for row, record in enumerate(records):
        for col, value in enumerate(record):
            draw_text(str(value), small_font, BLACK, surface, x + col * cell_width + cell_width // 2,
                      y + row * cell_height)


def update_record(name, result):
    """Обновляет запись в таблице records"""
    conn = sqlite3.connect('records.db')
    cursor = conn.cursor()

    cursor.execute("SELECT wins, draws, losses FROM records WHERE name = ?", (name,))
    record = cursor.fetchone()

    if record:
        wins, draws, losses = record
        if result == "win":
            wins += 1
        elif result == "draw":
            draws += 1
        elif result == "loss":
            losses += 1
        cursor.execute(
            "UPDATE records SET wins = ?, draws = ?, losses = ? WHERE name = ?",
            (wins, draws, losses, name)
        )
    else:
        if result == "win":
            wins = 1
        else:
            wins = 0
        if result == "draw":
            draws = 1
        else:
            draws = 0
        if result == "loss":
            losses = 1
        else:
            losses = 0
        cursor.execute(
            "INSERT INTO records (name, wins, draws, losses) VALUES (?, ?, ?, ?)",
            (name, wins, draws, losses)
        )

    conn.commit()
    conn.close()


def records_screen():
    """Экран рекордов"""
    records = get_records_from_db()
    while True:
        screen.fill(WHITE)
        draw_text("Рекорды", font, BLACK, screen, WIDTH // 2, 50)

        sort_records = sorted(records, key=lambda x: (-x[1], -x[2], x[3]))

        draw_table(screen, sort_records, 70, 150, 165, 50)

        back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
        pygame.draw.rect(screen, GRAY, back_button)
        draw_text("Назад", small_font, BLACK, screen, back_button.centerx, back_button.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_button.collidepoint(event.pos):
                        return

        pygame.display.flip()


def settings_screen():
    """Экран настроек"""
    global music_enabled
    while True:
        screen.fill(WHITE)
        draw_text("Настройки", font, BLACK, screen, WIDTH // 2, 50)

        music_button = pygame.Rect(WIDTH // 2 - 125, 200, 250, 50)
        pygame.draw.rect(screen, GRAY, music_button)
        music_text = "Музыка: Вкл" if music_enabled else "Музыка: Выкл"
        draw_text(music_text, small_font, BLACK, screen, music_button.centerx, music_button.centery)

        back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
        pygame.draw.rect(screen, GRAY, back_button)
        draw_text("Назад", small_font, BLACK, screen, back_button.centerx, back_button.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if music_button.collidepoint(event.pos):
                        music_enabled = not music_enabled
                        if music_enabled:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                    elif back_button.collidepoint(event.pos):
                        return

        pygame.display.flip()


def input_name_screen():
    """Экран для ввода имен игроков"""
    global player1_name, player2_name
    input_box1 = pygame.Rect(WIDTH // 2 - 100, 150, 200, 50)
    input_box2 = pygame.Rect(WIDTH // 2 - 100, 250, 200, 50)
    active1 = False
    active2 = False
    color_inactive = GRAY
    color_active = BLUE
    color1 = color_inactive
    color2 = color_inactive
    text1 = player1_name
    text2 = player2_name

    while True:
        screen.fill(WHITE)
        draw_text("Введите имена игроков", font, BLACK, screen, WIDTH // 2, 50)

        pygame.draw.rect(screen, color1, input_box1, 2)
        pygame.draw.rect(screen, color2, input_box2, 2)
        draw_text(text1, small_font, BLACK, screen, input_box1.centerx, input_box1.centery)
        draw_text(text2, small_font, BLACK, screen, input_box2.centerx, input_box2.centery)

        play_button = pygame.Rect(WIDTH // 2 - 100, 350, 200, 50)
        pygame.draw.rect(screen, GRAY, play_button)
        draw_text("Играть", small_font, BLACK, screen, play_button.centerx, play_button.centery)

        back_button = pygame.Rect(WIDTH // 2 - 100, 450, 200, 50)
        pygame.draw.rect(screen, GRAY, back_button)
        draw_text("Назад", small_font, BLACK, screen, back_button.centerx, back_button.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if input_box1.collidepoint(event.pos):
                        active1 = True
                        active2 = False
                        color1 = color_active
                        color2 = color_inactive
                    elif input_box2.collidepoint(event.pos):
                        active1 = False
                        active2 = True
                        color1 = color_inactive
                        color2 = color_active
                    elif play_button.collidepoint(event.pos):
                        player1_name = text1
                        player2_name = text2
                        print(f"Игрок 1: {player1_name}, Игрок 2: {player2_name}")
                        tic_tac_toe_screen()
                    elif back_button.collidepoint(event.pos):
                        return
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                elif active2:
                    if event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode

        pygame.display.flip()


def check_winner(board):
    """Проверяет, есть ли победитель"""
    for row in board:
        if row[0] == row[1] == row[2] != "":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    if all(cell != "" for row in board for cell in row):
        return "Ничья"
    return None


def tic_tac_toe_screen():
    """Экран игры в крестики-нолики"""
    global board, current_player, game_over, winner, animation_data
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    current_player = "X"
    game_over = False
    winner = None
    animation_data = {}
    bul_tr = True

    while True:
        screen.fill(WHITE)
        draw_text(f"Ход: {player1_name if current_player == 'X' else player2_name}",
                  font, BLACK, screen, WIDTH // 2, 50)

        for row in range(3):
            for col in range(3):
                pygame.draw.rect(screen, GRAY, (120 + col * 100, 130 + row * 100, 100, 100), 2)
                if board[row][col] == "X":
                    if (row, col) not in animation_data:
                        animation_data[(row, col)] = {"size": 0, "max_size": 74}
                    size = animation_data[(row, col)]["size"]
                    if size < animation_data[(row, col)]["max_size"]:
                        size += 2
                        animation_data[(row, col)]["size"] = size
                    animated_font = pygame.font.Font(None, int(size))
                    draw_text("X", animated_font, BLACK, screen, 170 + col * 100, 180 + row * 100)
                elif board[row][col] == "O":
                    if (row, col) not in animation_data:
                        animation_data[(row, col)] = {"size": 0, "max_size": 74}
                    size = animation_data[(row, col)]["size"]
                    if size < animation_data[(row, col)]["max_size"]:
                        size += 2
                        animation_data[(row, col)]["size"] = size
                    animated_font = pygame.font.Font(None, int(size))
                    draw_text("O", animated_font, BLACK, screen, 170 + col * 100, 180 + row * 100)

        restart_button = pygame.Rect(130, 500, 230, 50)
        pygame.draw.rect(screen, GRAY, restart_button)
        draw_text("Перезапуск", small_font, BLACK, screen, restart_button.centerx, restart_button.centery)

        home_button = pygame.Rect(450, 500, 230, 50)
        pygame.draw.rect(screen, GRAY, home_button)
        draw_text("Назад", small_font, BLACK, screen, home_button.centerx, home_button.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not game_over:
                        for row in range(3):
                            for col in range(3):
                                if 120 + col * 100 < event.pos[0] < 220 + col * 100 and \
                                        130 + row * 100 < event.pos[1] < 230 + row * 100:
                                    if board[row][col] == "":
                                        board[row][col] = current_player
                                        winner = check_winner(board)
                                        if winner:
                                            game_over = True
                                        else:
                                            current_player = "O" if current_player == "X" else "X"
                    if restart_button.collidepoint(event.pos):
                        board = [["", "", ""], ["", "", ""], ["", "", ""]]
                        current_player = "X"
                        game_over = False
                        winner = None
                        animation_data = {}
                        bul_tr = True
                    elif home_button.collidepoint(event.pos):
                        return

        if game_over:
            if winner == "Ничья":
                draw_text("Ничья!", font, BLACK, screen, 600, 250)
                if bul_tr:
                    update_record(player1_name, "draw")
                    update_record(player2_name, "draw")
                bul_tr = False
            else:
                winner_name = player1_name if winner == "X" else player2_name
                loser_name = player2_name if winner == "X" else player1_name
                draw_text("Победитель:", font, BLACK, screen, 610, 190)
                draw_text(f"{winner_name}", font, BLACK, screen, 610, 260)
                if bul_tr:
                    update_record(winner_name, "win")
                    update_record(loser_name, "loss")
                bul_tr = False

        pygame.display.flip()


def main_menu():
    """Главное меню"""
    global music_enabled
    if music_enabled:
        pygame.mixer.music.play(-1)

    while True:
        screen.fill(WHITE)
        draw_text("Главное Меню", font, BLACK, screen, WIDTH // 2, 100)

        buttons = [
            (pygame.Rect(WIDTH // 2 - 100, 150, 200, 50), "Играть"),
            (pygame.Rect(WIDTH // 2 - 100, 250, 200, 50), "Настройки"),
            (pygame.Rect(WIDTH // 2 - 100, 350, 200, 50), "Рекорды"),
            (pygame.Rect(WIDTH // 2 - 100, 450, 200, 50), "Выход"),
        ]

        for button, text in buttons:
            pygame.draw.rect(screen, GRAY, button)
            draw_text(text, small_font, BLACK, screen, button.centerx, button.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, (button, text) in enumerate(buttons):
                        if button.collidepoint(event.pos):
                            if i == 0:
                                input_name_screen()
                            elif i == 1:
                                settings_screen()
                            elif i == 2:
                                records_screen()
                            elif i == 3:
                                pygame.quit()
                                sys.exit()

        pygame.display.flip()


if __name__ == "__main__":
    conn = sqlite3.connect('records.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                name TEXT PRIMARY KEY,
                wins INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0
            )
        ''')
    conn.commit()
    conn.close()

    main_menu()
