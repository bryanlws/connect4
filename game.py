import random
import copy
import sys
import winsound

print("\t*****  *****  *    *  *    *  *****  *****  *****     *  ")
print("\t*      *   *  **   *  **   *  *      *        *      **  ")
print("\t*      *   *  * *  *  * *  *  *****  *        *     * *  ")
print("\t*      *   *  *  * *  *  * *  *      *        *    ***** ")
print("\t*      *   *  *   **  *   **  *      *        *       *  ")
print("\t*****  *****  *    *  *    *  *****  *****    *       *  \n")


#Background music
winsound.PlaySound("bgm.wav",winsound.SND_ASYNC | winsound.SND_ALIAS | winsound.SND_LOOP)


#Let's the player choose the difficulty for the game
print ("Please choose a difficulty:")
difficulty=int(input("Choose 1 for normal or 2 for advanced: "))
if difficulty == 1:
    columns = 7
    row = 6
    print('Get four-in-a-row to win!')
elif difficulty == 2:
    columns = 9
    row = 6
    print('Get five-in-a-row to win!')


def ChooseHumanChip():
    #Let's the player decide which chip they want to use.
    #Returns a list with th player's chip as the first item, and the computer's chip as the second.

    while True:
        userinput=input('Choose X or O:')
        if userinput.lower() == 'x':
            userinput='X'
            computerinput='O'

        elif userinput.lower() == 'o':
            userinput='O'
            computerinput='X'

     #The first element in the tuple is the player's chip while the second is the computer's chip.
        if userinput == 'X':
            return ['X', 'O']
        elif userinput == 'O':
            return ['O', 'X']
        
        if not userinput=='x'or'o'or'X'or'O':
            continue

def PlayerOrComputerFirst():
    #Let's the player choose whether they want to go first or second
    while True:
        whofirst=input('Choose to go first or second (type first or second):')
        if  whofirst.lower() == 'first':
            whofirst='First'
            return 'human'
        elif whofirst.lower() == 'second':
            whofirst='Second'
            return 'computer'
        if not whofirst == 'first' or 'second':

            continue
        

def GameBoard(board):
    #Code for the game board
    print()
    print(' ', end='')
    for x in range(1, columns + 1):
        print(' %s  ' % x, end='')
    print()

    print('+---+' + ('---+' * (columns - 1)))

    for y in range(row):
        print('|   |' + ('   |' * (columns - 1)))

        print('|', end='')
        for x in range(columns):
            print(' %s |' % board[x][y], end='')
        print()

        print('|   |' + ('   |' * (columns - 1)))

        print('+---+' + ('---+' * (columns - 1)))


def getNewBoard():
    board = []
    for x in range(columns):
        board.append([' '] * row)
    return board



def main():

    while True:
        attempts = 0
        humanChip, computerChip = ChooseHumanChip()
        turn = PlayerOrComputerFirst()
        print('The %s player will go first.' % (turn))
        mainBoard = getNewBoard()

        while True:
            if turn == 'human':
                GameBoard(mainBoard)
                move = HumanMove(mainBoard)
                MakeYourMove(mainBoard, humanChip, move)
                attempts += 1
                if isWinner(mainBoard, humanChip):
                    winner = 'human'
                    break
                turn = 'computer'
            else:
                GameBoard(mainBoard)
                move = ComputerMove(mainBoard, computerChip)
                MakeYourMove(mainBoard, computerChip, move)
                if isWinner(mainBoard, computerChip):
                    winner = 'computer'
                    break
                turn = 'human'

            if isBoardFull(mainBoard):
                winner = 'tie game'
                break

        GameBoard(mainBoard)
        print('Winner is: %s' % winner)
        if isWinner(mainBoard, humanChip):
            print('Total Attempts:', attempts)
            if attempts >= 15:
                print("You can do better")        
            elif (attempts >= 10) and (attempts <=14):
                print("Not too bad")
            elif(attempts <= 9):
                print("You have the talent")
        if not playAgain():
            break
          


def HumanMove(board):
    #Let's player decide which column to place their chip
    while True:
        print('Which column do you want to place your chip? (1-%s, or "quit" to quit game)' % (columns))
        move = input()
        if move.lower().startswith('q'):
            sys.exit()
        if not move.isdigit():
            continue
        move = int(move) - 1
        if CorrectMove(board, move):
            return move

def ComputerMove(board, computerChip):
    #Let's computer calculate the best possible move to make
    potentialMoves = getPotentialMoves(board, computerChip, 2)
    bestMoveScore = max([potentialMoves[i] for i in range(columns) if CorrectMove(board, i)])
    bestMoves = []
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveScore:
            bestMoves.append(i)
    return random.choice(bestMoves)


def getPotentialMoves(board, playerChip, lookAhead):
    if lookAhead == 0:
        return [0] * columns

    potentialMoves = []

    if playerChip == 'O':
        computerChip = 'X'
    else:
        computerChip = 'O'

    #Returns (best move, average condition of this state)
    if isBoardFull(board):
        return [0] * columns

    #Figure out the best move to make.
    potentialMoves = [0] * columns
    for playerMove in range(columns):
        DuplicateTheBoard = copy.deepcopy(board)
        if not CorrectMove(DuplicateTheBoard, playerMove):
            continue
        MakeYourMove(DuplicateTheBoard, playerChip, playerMove)
        if isWinner(DuplicateTheBoard, playerChip):
            potentialMoves[playerMove] = 1
            break
        else:
            #Follow other player's moves and determine best one
            if isBoardFull(DuplicateTheBoard):
                potentialMoves[playerMove] = 0
            else:
                for computerMove in range(columns):
                    DuplicateTheBoard2 = copy.deepcopy(DuplicateTheBoard)
                    if not CorrectMove(DuplicateTheBoard2, computerMove):
                        continue
                    MakeYourMove(DuplicateTheBoard2, computerChip, computerMove)
                    if isWinner(DuplicateTheBoard2, computerChip):
                        potentialMoves[playerMove] = -1
                        break
                    else:
                        results = getPotentialMoves(DuplicateTheBoard2, playerChip, lookAhead - 1)
                        potentialMoves[playerMove] += (sum(results) / columns) / columns
    return potentialMoves


def MakeYourMove(board, player, column):
    for y in range(row-1, -1, -1):
        if board[column][y] == ' ':
            board[column][y] = player
            
            return


def CorrectMove(board, move):
    if move < 0 or move >= (columns):
        return False

    if board[move][0] != ' ':
        return False

    return True


def isBoardFull(board):
    for x in range(columns):
        for y in range(row):
            if board[x][y] == ' ':
                return False
    return True


def isWinner(board, Chip):
    if difficulty == 1:
        #Check horizontal lines
        for y in range(row):
            for x in range(columns - 3):
                if board[x][y] == Chip and board[x+1][y] == Chip and board[x+2][y] == Chip and board[x+3][y] == Chip:
                    return True

    #Check vertical lines
        for x in range(columns):
            for y in range(row - 3):
                if board[x][y] == Chip and board[x][y+1] == Chip and board[x][y+2] == Chip and board[x][y+3] == Chip:
                    return True

    #Check / diagonal lines
        for x in range(columns - 3):
            for y in range(3, row):
                if board[x][y] == Chip and board[x+1][y-1] == Chip and board[x+2][y-2] == Chip and board[x+3][y-3] == Chip:
                    return True

    #Check \ diagonal lines
        for x in range(columns - 3):
            for y in range(row - 3):
                if board[x][y] == Chip and board[x+1][y+1] == Chip and board[x+2][y+2] == Chip and board[x+3][y+3] == Chip:
                    return True

        return False
    if difficulty == 2:
        for y in range (row):
            for x in range(columns - 4):
                if board [x][y] == Chip and board[x+1][y] == Chip and board[x+2][y] == Chip and board[x+3][y] == Chip and board [x+4][y]== Chip:
                    return True

        for x in range (columns):
            for y in range (row - 4):
                if board[x][y] == Chip and board[x][y+1] == Chip and board[x][y+2] == Chip and board[x][y+3] == Chip and board [x][y+3]==Chip:
                    return True
                
        for x in range(columns - 4):
            for y in range(3, row):
                if board[x][y] == Chip and board[x+1][y-1] == Chip and board[x+2][y-2] == Chip and board[x+3][y-3] == Chip and board [x+4][x-4]==Chip:
                    return True
        for x in range(columns - 4):
            for y in range(row - 4):
                if board[x][y] == Chip and board[x+1][y+1] == Chip and board[x+2][y+2] == Chip and board[x+3][y+3] == Chip and board [x+4][y+4]==Chip:
                    return True

        return False


    
def playAgain():
    #Returns True if the player wants to play again, else itreturns False.
    print('Play again? (yes or no)')
    return input().lower().startswith('y')




if __name__ == '__main__':
    main()
