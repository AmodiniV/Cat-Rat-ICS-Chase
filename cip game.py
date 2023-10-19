# importing all necessary libraries
import random
import tkinter
from tkinter import *
from functools import partial
from tkinter import messagebox
from copy import deepcopy
 
# sign variable to decide the turn of which player
sign = 0
count = 0     #number of days for attacker to succeed
 
# Creates an empty board
global board
board_size = 10
board = [[" " for _ in range(board_size)] for _ in range(board_size)]

attack_mat = [['Phishing', 'Insider Threat', 'SQLi/XSS on IT network'],
          ['Subnetting Attack', 'Credential Theft', 'Waterhole Attack'],
          ['Malware & Ransomware', 'DoS/DDoS', 'Supply Chain Attack']]

defend_mat =  [['Endpoint Protection', 'IDS & IPS', 'Input Validation/CSP'],
          ['Network Segmentation', 'MFA ', 'Vendor Risk Assessment'],
          ['IDS and IPS for ICS', 'ICS Firewall', 'Patch Management']]

attacks_tried = set()
defends_tried = set()
visit_set = set()

##how the system choses random security defense measure
def defender_values(j):
    while(1):
        x = random.randint(0, 2)
        if(j,x) not in defends_tried:
            defends_tried.add((j,x))
            return defend_mat[j][x]

## to check if security is already in place or not for an attacker move       
def check_condition(x,y):
    if (x,y) in defends_tried:
        box = messagebox.showinfo("Warning","Attack failed as {} in place".format(defend_mat[x][y]))
    else:
        box = messagebox.showinfo("Congrats","Attack succeeded at level:{}!".format(x+1))
        if(x == 2):
            box = messagebox.showinfo("Winner", "Attacker hacked the ICS system in {} days".format(count))

def attack_value(j):
    for v in range(len(attack_mat[j])):
        if (j,v) not in attacks_tried:
            attacks_tried.add((j,v))
            return attack_mat[j][v],v
        
## function when playing against another player
def get_text(i, j, gb, l1, l2):
    global sign
    global count
    def_flag = True
    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            #tmp = defender_values(j)
            board[i][j]= defender_values(j)
            def_flag = True
        else:
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j],v = attack_value(j)
            def_flag = False
            count += 1
        sign += 1
        if(def_flag):
            button[i][j].config(bg = 'blue',text=board[i][j])
        else:
            button[i][j].config(bg = 'red',text=board[i][j])
            check_condition(j,v)

##function when playing against pc 
def gameboard_pc(game_board,l1,l2):
    global button
    button = []
    global count
    count = 0
    for i in range(6):
        m = 3+i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_text_pc, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=6, width=20)
            button[i][j].grid(row=m, column=n)
    
    game_board.mainloop()

##continued function when playing against pc 
def get_text_pc(i, j, gb, l1, l2):
    global sign
    global count 
    def_flag = True
    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = defender_values(j)
            def_flag = True
        else:
            button[i][j].config(state=ACTIVE)
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j],v = attack_value(j)
            def_flag = False
            count += 1
        sign += 1
        if(def_flag):
            button[i][j].config(text=board[i][j],bg='blue')
        else:
            button[i][j].config(text=board[i][j],bg='red')
            check_condition(j,v)
        visit_set.add((i,j))
    x = True
    if(x):
        if sign % 2 == 0:
            for i in range(6):
                y1 = random.randint(0, 2)
                x1 = random.randint(0, 2)
                i += 1
                #button[x1][y1].config(state=DISABLED)
                if (x1,y1) not in visit_set:
                    get_text_pc(i,y1, gb, l1, l2)
                    break

## function when playing against another player
def gameboard_pl(game_board, l1, l2):
    global button
    button = []
    count = 0
    for i in range(6):
        m = 3+i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_text, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=6, width=20)
            button[i][j].grid(row=m, column=n)
    #print_missing_values()

    game_board.mainloop()

def withpc(game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.geometry("500x1500")
    game_board.title("CIP game")

    l3 = Button(game_board, text="Attacker Options", bg = 'yellow',width=20,command = partial(open_window,game_board))
    l3.grid(row=2, column=1)

    l1 = Button(game_board, text="Defender", width=20,bg = "blue")
    l1.grid(row=1, column=0)

    l2 = Button(game_board, text="Attacker",
                width=20, state=DISABLED,bg = "red")
    l2.grid(row=1, column=2)
    gameboard_pc(game_board,l1,l2)

## to display attacker options
def open_window(game_board):
    new_window = Toplevel(game_board)
    new_window.title("Options for Attacker")
    level1 = {"Phishing", "Insider Threat", "SQLi/XSS on IT network"}
    level2 = {'Subnetting Attack', 'Credential Theft', 'Waterhole Attack'}
    level3 = {'Malware & Ransomware', 'DoS/DDoS', 'Supply Chain Attack'}
    result_string = "\n-------\n"+"Level1\n" + '\n'.join([f'  {val}' for val in level1]) + "\n-------\n"+"\nLevel2\n" + '\n'.join([f'  {val}' for val in level2])+"\n-------\n"+"\nLevel3\n"+ '\n'.join([f' {val}' for val in level3])

    label = Label(new_window, text="Attacks list\n" + result_string)
    label.pack(padx=20, pady=20)

def withplayer(game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.geometry("500x1500")
    game_board.title("Cat-Rat ICS Chase")

    l3 = Button(game_board, text="Attacker Options", bg = 'yellow',width=20,command = partial(open_window,game_board))
    l3.grid(row=2, column=1)

    l1 = Button(game_board, text="Defender", width=20,bg = "blue")
    l1.grid(row=1, column=0)

    l2 = Button(game_board, text="Attacker",
                width=20, state=DISABLED,bg = "red")
    l2.grid(row=1, column=2)

    
    gameboard_pl(game_board,l1, l2)

##main game function
def play():
    menu = Tk()
    menu.geometry("500x500")
    menu.title("")
    wpc = partial(withpc, menu)
    wpl = partial(withplayer, menu)
 
    head = Button(menu, text="---Welcome to Cat-Rat ICS Chase---",
                  activeforeground='red',
                  activebackground="yellow", bg="red",
                  fg="yellow", width=500, font='summer', bd=5)
 
    B1 = Button(menu, text="Single Player", command=wpc,
                activeforeground='red',
                activebackground="yellow", bg="red",
                fg="yellow", width=500, font='summer', bd=5)
 
    B2 = Button(menu, text="Multi Player", command=wpl, activeforeground='red',
                activebackground="yellow", bg="red", fg="yellow",
                width=500, font='summer', bd=5)
 
    B3 = Button(menu, text="Exit", command=menu.quit, activeforeground='red',
                activebackground="yellow", bg="red", fg="yellow",
                width=500, font='summer', bd=5)
    head.pack(side='top')
    B1.pack(side='top')
    B2.pack(side='top')
    B3.pack(side='top')
    menu.mainloop()
 
 
# Call main function
if __name__ == '__main__':
    play()