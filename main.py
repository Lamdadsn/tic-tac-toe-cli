# A simple tic-tac-toe game that offers choice of P-v-P or P-v-Machine (random).
# Player score is tallied as each game is concluded.
# Currently, when the Machine plays the player a simple random seletion is made for the machine.
# A future improvement would be to source and apply an ML model trained to play this game instead of using randint().
# Note: for the clear screen function to work, remember to ensure there is a TERM=xterm-color in Environment variables

import random
import os


GAME_LOGO = '''
 ____  __  ___    ____  __    ___    ____  __  ____ 
(_  _)(  )/ __)  (_  _)/ _\  / __)  (_  _)/  \(  __)
  )(   )(( (__     )( /    \( (__     )( (  O )) _) 
 (__) (__)\___)   (__)\_/\_/ \___)   (__) \__/(____)
 
 '''
X_TAKEN = False
O_TAKEN = False


class Player():
    def __init__(self):
        global X_TAKEN, O_TAKEN
        icon_set = False
        while not icon_set:
            if not X_TAKEN and not O_TAKEN:
                self.icon = input('P1, Choose X or O: ').upper()      # holds value of X or O
                if self.icon == 'X':
                    icon_set = True
                    X_TAKEN = True
                if self.icon == 'O':
                    icon_set = True
                    O_TAKEN = True
            elif not X_TAKEN:
                self.icon = 'X'
                icon_set = True
                X_TAKEN = True
            else:
                self.icon = 'O'
                icon_set = True
                O_TAKEN = True
        self.score = 0
        self.positions = []

    def select_tile(self, position):
        self.positions.append(position)


class GameBoard():
    def __init__(self):
        super().__init__()
        self.positions = [' ' for p in range(9)]
        self.win_combos = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [1, 5, 9],
            [3, 5, 7],
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9]
        ]
        self.ai_positions = []              # for when AI is using the board to play
        self.score = 0                      # to keep track of AI's score

    def show_board(self, num, gamers):
        """Shows the current board with player selections and checks for a game outcome by comparing with
        lists of winning combinations.
        Requires number of players (int) and the list containing the Player() instances.
        Returns a boolean value to indicate still_playing"""
        print('  -------------------')
        print('  |     |     |     |')
        print(f'  |  {self.positions[0]}  |  {self.positions[1]}  |  {self.positions[2]}  |')
        print('  |     |     |     |')
        print('  |-----|-----|-----|')
        print('  |     |     |     |')
        print(f'  |  {self.positions[3]}  |  {self.positions[4]}  |  {self.positions[5]}  |')
        print('  |     |     |     |')
        print('  |-----|-----|-----|')
        print('  |     |     |     |')
        print(f'  |  {self.positions[6]}  |  {self.positions[7]}  |  {self.positions[8]}  |')
        print('  |     |     |     |')
        print('  -------------------')

        sp = True
        game_status = self.check_finished(num, gamers)
        if game_status == 1:
            print('PLAYER 1 WINS!!')
            sp = False
        elif game_status == 2:
            print('PLAYER 2 WINS!!')
            sp = False
        elif game_status == 'm':
            print('A.I. WINS!!')
            sp = False
        elif game_status == 3:
            print('DRAW!!')
            sp = False
        # else game_status = 0 and still playing
        return sp

    def ai_selection(self, position):
        """Keep track of the selections made by the machine playing the game. Requires selected tile position"""
        self.ai_positions.append(position)

    def check_finished(self, num, players):
        # check player 1
        tally = 0
        for c_set in self.win_combos:
            for c in c_set:
                if c in players[0].positions:
                    tally += 1
                    if tally == 3:
                        players[0].score += 1
                        return 1                            # player 1 wins
            tally = 0
        if num == 2:                                        # check player 2
            tally = 0
            for c_set in self.win_combos:
                for c in c_set:
                    if c in players[1].positions:
                        tally += 1
                        if tally == 3:
                            players[1].score += 1
                            return 2                        # player 2 wins
                tally = 0
        else:                                               # check AI score
            tally = 0
            for c_set in self.win_combos:
                for c in c_set:
                    if c in self.ai_positions:
                        tally += 1
                        if tally == 3:
                            self.score += 1
                            return 'm'                        # machine (AI) wins
                tally = 0
        for i in range(9):
            if board.positions[i] == ' ':
                return 0                        # still playing
        return 3                                # draw


def get_choice(p_num, positions):
    """Displays currently available board tile positions and prompts for current player's choice.
    Requires number of players (int) and GameBoard.positions (list of strings) showing tiles occupied or blank.
    Returns int 1...9"""
    print('\n')
    display = [i+1 if positions[i] == ' ' else ' ' for i in range(0, 9)]  # only show available tiles at prompt
    print('-------------')
    print(f'| {display[0]} | {display[1]} | {display[2]} |')
    print('|---|---|---|')
    print(f'| {display[3]} | {display[4]} | {display[5]} |')
    print('|---|---|---|')
    print(f'| {display[6]} | {display[7]} | {display[8]} |')
    print('-------------')
    choice = 0
    while choice not in range(1, 10):
        choice = int(input(f'\nP{p_num} Choose an available tile number: '))
        if positions[choice-1] != ' ':
            print('That space has already been taken. Please try again')
            choice = 0
    os.system('clear')
    return choice


def ai_choice(positions):
    """Machine makes random selection from set of available tiles.
    Potential improvement would be to incorporate an AI function that uses an appropriately trained model.
    Requires GameBoard.positions (list of strings) showing tiles occupied or blank.
    Returns int 1...9"""
    choice = 0
    print("AI's turn!")
    while choice not in range(1, 10):
        choice = random.randint(1, 9)
        if positions[choice-1] != ' ':      # if space already taken
            choice = 0
    os.system('clear')
    return choice


def play_turn(n_players, p_num, game_board, gamers):
    """Play an individual player's turn.

    Requires:
    n_players: number of players (1 or 2)
    p_num: current player index (0 or 1)
    game_board: instance of GameBoard class
    gamers: list containing Player class instances.

    Returns: Boolean to indicate game outcome; to be used to exit playing loop"""
    position_played = get_choice(p_num + 1, game_board.positions)
    game_board.positions[position_played - 1] = players[p_num].icon
    players[p_num].select_tile(position_played)
    return game_board.show_board(n_players, gamers)


board = GameBoard()

os.system('clear')              # remember to ensure there is a TERM=xterm-color in environment variables
print(GAME_LOGO)
print("\nLet's play!!\n")
# Set number of players/gamers
num_players = 0
while num_players not in range(1,3):
    num_players = int(input("How many players?\n[1] - player vs machine\n[2] - player vs player\n:  "))
players = [Player() for p in range(num_players)]

still_playing = True
# Each loop execution is a pair of turns taken. Check for win occurs at end of each individual turn
while still_playing:                                        # 'X' goes first in this game
    if num_players == 2:
        if players[0].icon == 'X':                          # p1 of 2 goes first
            for p in range(0, 2):
                still_playing = play_turn(num_players, p, board, players)
                if not still_playing:
                    break
        else:                                               # p2 of 2 goes first
            for p in range(2, 0, -1):
                still_playing = play_turn(num_players, p-1, board, players)
                if not still_playing:
                    break
    else:                                                   # playing against machine
        if players[0].icon == 'X':                          # p1 goes first
            still_playing = play_turn(num_players, 0, board, players)
            if still_playing:                               # then machine
                posn_played = ai_choice(board.positions)
                board.positions[posn_played - 1] = 'O'      # assign player icon to the board
                board.ai_selection(posn_played)
                still_playing = board.show_board(num_players, players)
        else:
            posn_played = ai_choice(board.positions)        # machine is 'X' and goes first
            board.positions[posn_played - 1] = 'X'          # assign player icon to the board
            board.ai_selection(posn_played)
            still_playing = board.show_board(num_players, players)
            if still_playing:                               # p1 goes next
                still_playing = play_turn(num_players, 0, board, players)
# offer a re-match
    if not still_playing:
        if num_players == 1:
            print(f'\nSCORE:\n  P1: {players[0].score}\n  AI: {board.score}')
        else:
            print(f'\nSCORE:\n  P1: {players[0].score}\n  P2: {players[1].score}')
        keep_going = input('\nWould you like to play another game? (y) : ')
        if keep_going.lower() == 'y':                       # reset the board and players
            os.system('clear')
            for p in players:
                p.positions.clear()
            board.ai_positions.clear()
            board.positions.clear()
            for p in range(9):
                board.positions.append(' ')
            still_playing = True
        else:
            print("\nThanks for playing!")

