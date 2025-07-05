import tkinter as tk

root = tk.Tk()
root.title("Tic-Tac-Toe - With Timer")
root.geometry("450x600")
root.configure(bg="#222831")
root.resizable(False, False)

FONT = ("Comic Sans MS", 22, "bold")
LABEL_FONT = ("Helvetica", 14, "bold")
PLAYER_X_COLOR = "#00adb5"
PLAYER_O_COLOR = "#ff5722"

board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
player1_name = "Player X"
player2_name = "Player O"
player1_score = 0
player2_score = 0
current_player = "X"
time_left = 10
timer_running = False

def start_game():
    global player1_name, player2_name
    player1_name = entry1.get() or "Player X"
    player2_name = entry2.get() or "Player O"
    name_frame.destroy()
    setup_board()
    update_status()
    start_timer()

def start_timer():
    global time_left, timer_running
    time_left = 10
    timer_running = True
    update_timer()

def update_timer():
    global time_left, timer_running
    if time_left > 0 and timer_running:
        timer_label.config(text=f"⏱️ {time_left} sec")
        time_left -= 1
        root.after(1000, update_timer)
    elif timer_running:
        handle_time_out()

def handle_time_out():
    global player1_score, player2_score, timer_running
    timer_running = False
    if current_player == "X":
        player2_score += 1
        winner = player2_name
        loser = player1_name
    else:
        player1_score += 1
        winner = player1_name
        loser = player2_name
    update_score()
    show_result(f"⏳ Time's up! {loser} lost. {winner} wins!")

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return True
        if board[0][i] == board[1][i] == board[2][i] != "":
            return True
    if board[0][0] == board[1][1] == board[2][2] != "":
        return True
    if board[0][2] == board[1][1] == board[2][0] != "":
        return True
    return False

def is_draw():
    return all(cell != "" for row in board for cell in row)

def on_click(i, j):
    global current_player, player1_score, player2_score, timer_running

    if board[i][j] == "":
        board[i][j] = current_player
        buttons[i][j].config(
            text=current_player,
            fg=PLAYER_X_COLOR if current_player == "X" else PLAYER_O_COLOR,
            state="disabled"
        )

        if check_winner():
            winner = player1_name if current_player == "X" else player2_name
            if current_player == "X":
                player1_score += 1
            else:
                player2_score += 1
            update_score()
            show_result(f"🏆 {winner} wins!")
        elif is_draw():
            show_result("😅 It's a draw!")
        else:
            current_player = "O" if current_player == "X" else "X"
            update_status()
            start_timer()

def update_status():
    name = player1_name if current_player == "X" else player2_name
    status_label.config(text=f"{name}'s turn ({current_player})")

def show_result(message):
    global timer_running
    timer_running = False
    status_label.config(text=message)
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state="disabled")
    button_frame.pack(pady=10)
    restart_button.pack(side="left", padx=10)
    quit_button.pack(side="right", padx=10)

def reset_game():
    global board, current_player, timer_running
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    timer_running = False
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state="normal")
    update_status()
    timer_label.config(text="")
    button_frame.pack_forget()
    restart_button.pack_forget()
    quit_button.pack_forget()
    start_timer()

def quit_game():
    root.destroy()

def update_score():
    score_label.config(text=f"{player1_name}: {player1_score}    |    {player2_name}: {player2_score}")

def setup_board():
    update_score()
    score_label.pack(pady=(10, 0))
    timer_label.pack(pady=(5, 0))
    for i in range(3):
        for j in range(3):
            btn = tk.Button(game_frame, text="", width=5, height=2, font=FONT,
                            bg="#eeeeee", activebackground="#00adb5",
                            command=lambda i=i, j=j: on_click(i, j))
            btn.grid(row=i, column=j, padx=5, pady=5)
            buttons[i][j] = btn
    game_frame.pack(pady=20)
    status_label.pack(pady=(10, 0))

name_frame = tk.Frame(root, bg="#222831")
tk.Label(name_frame, text="🎮 Enter Player Names", font=("Arial", 16, "bold"), fg="white", bg="#222831").pack(pady=10)
tk.Label(name_frame, text="Player X:", font=LABEL_FONT, fg="white", bg="#222831").pack()
entry1 = tk.Entry(name_frame, font=LABEL_FONT, justify="center")
entry1.pack(pady=5)
tk.Label(name_frame, text="Player O:", font=LABEL_FONT, fg="white", bg="#222831").pack()
entry2 = tk.Entry(name_frame, font=LABEL_FONT, justify="center")
entry2.pack(pady=5)
tk.Button(name_frame, text="Start Game", font=("Arial", 14, "bold"), bg="#00adb5", fg="white", command=start_game).pack(pady=15)
name_frame.pack(pady=80)

score_label = tk.Label(root, text="", font=LABEL_FONT, fg="white", bg="#222831")
timer_label = tk.Label(root, text="", font=("Helvetica", 14, "bold"), fg="#00ffcc", bg="#222831")
game_frame = tk.Frame(root, bg="#222831")
status_label = tk.Label(root, text="", font=("Arial", 14), fg="#eeeeee", bg="#222831")

button_frame = tk.Frame(root, bg="#222831")
restart_button = tk.Button(button_frame, text="🔁 Play Again", font=("Helvetica", 16, "bold"),
                           bg="#393e46", fg="white", width=12, height=2, bd=3, relief="raised", command=reset_game)
quit_button = tk.Button(button_frame, text="❌ Quit", font=("Helvetica", 16, "bold"),
                        bg="#ff4d4d", fg="white", width=12, height=2, bd=3, relief="raised", command=quit_game)

root.mainloop()
