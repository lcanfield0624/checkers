import os
from re import A
import pygame
# from msvcrt import kbhit
from operator import add
import time


pygame.init()
clock = pygame.time.Clock()


global white, black, red, gray
white = (255,255,255)
black = (0, 0, 0)
red = (255, 0, 0)
gray = (127,127,127)


# importing input keys
from pygame.locals import(
  K_UP,
  K_DOWN,
  K_RIGHT,
  K_LEFT,
  K_ESCAPE,
  K_1,
  K_2,
  K_3,
  KEYDOWN,
  MOUSEBUTTONDOWN,
  MOUSEMOTION,
  QUIT
)



# game window
window = pygame.display.set_mode((1400,900)) #, pygame.FULLSCREEN)
# fill window background white


window.fill(white)
pygame.display.update()


# set font
sourceFileDir = os.path.dirname(os.path.abspath(__file__))
fontPath = os.path.join(sourceFileDir, 'MYRIADPRO-REGULAR.OTF')




# piece class to give checkers certain attributes
class piece:
  def __init__(self, color, king, life, canmove, movelist, canjump, jumpdict, square):
    self.color = color # black or white
    self.king = king # king or pawn
    self.life = life # alive or dead
    self.canmove = canmove # True or False (True until proven false)
    self.movelist = movelist # list of moves available to the piece
    self.canjump = canjump # True or False (True until proven false)
    self.jumpdict = jumpdict # list of jumps available to the piece
    self.square = square # location: from rows and columns in square functions




def draw_board():
  white = (255,255,255)
  black = (0, 0, 0)
  red = (255, 0, 0)

  width, height = 100, 100 # of checker square
  thickness = 0

    # starting positions for drawing the board
  board_x = 100
  board_y = 0

  # set bg to blurred image
  sourceFileDir = os.path.dirname(os.path.abspath(__file__))
  ImgPath = os.path.join(sourceFileDir, 'blur_bg2.jpg')
  bg = pygame.image.load(ImgPath)
  window.blit(bg,(0,0)) 

  # drawing the checkerboard (without numbers or letters)
  for n in range(4):
    for n in range(4):
      pygame.draw.rect(window, red, (board_x, board_y, width, height),thickness)
      board_x += 100
      pygame.draw.rect(window, black, (board_x, board_y, width, height),thickness)
      board_x += 100
    board_x = 100
    board_y += 100
    for n in range(4):
      pygame.draw.rect(window, black, (board_x, board_y, width, height),thickness)
      board_x += 100
      pygame.draw.rect(window, red, (board_x, board_y, width, height),thickness)
      board_x += 100
    board_x = 100
    board_y += 100

  # adding letters and numbers on side
  numbers = ['8','7','6','5','4','3','2','1',]
  letters = ['a','b','c','d','e','f','g','h']
    # set font size
  font = pygame.font.Font(fontPath, 50) 
  
  # draw numbers
  i = 0
    # starting positions for drawing the numbers
  numbers_x = 40
  numbers_y = 35
  for c in range(8):
    text = font.render(numbers[i], True, black)
    i += 1
    window.blit(text, (numbers_x, numbers_y))
    numbers_y += 100

  # draw letters
  i = 0
    # starting positions for drawing the letters
  letters_x = 140
  letters_y = 830
  for r in range(8):
    text = font.render(letters[i], True, black)
    i += 1
    window.blit(text, (letters_x, letters_y))
    letters_x += 100

  # draw key on right
  font = pygame.font.Font(fontPath, 25)
  text = font.render('[esc] Return to Menu', True, black)
  window.blit(text, (1050, 30))

  pygame.display.update()




def draw_pieces():
  global blacksquares, wpieces, bpieces

  blacksquares = dict()
  columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
  rows = ['8', '7', '6', '5', '4', '3', '2', '1']

  wpieces = []
  bpieces = []

  # draws white checker pieces and puts the squares the checkers are on into a dictionary with the key being the square and the value being the coordinate
  i = 0
    #starting position for drawing white pieces
  white_x = [250, 150, 250]
  white_y = 50

  for n in (white_x):
    for n in range(4):
      pygame.draw.circle(window, white, (white_x[i], white_y), 40, 0)
      pygame.draw.circle(window, gray, (white_x[i], white_y), 36, 2)

      if i == 1:
        blacksquares[columns[2 * n] + rows[i]] = [white_x[i], white_y]

        #creates all white piece objects and assigns their starting attributes
        
        wpieces.append(piece(color = 'w', king = False, life = True, canmove = False, movelist = [], canjump = False, jumpdict = dict(), square = columns[2 * n] + rows[i]))
        
      else:
        blacksquares[columns[2 * n + 1] + rows[i]] = [white_x[i], white_y]

        #creates all white piece objects and assigns their starting attributes
        wpieces.append(piece(color = 'w', king = False, life = True, canmove = False, movelist = [], canjump = False, jumpdict = dict(), square = columns[2 * n + 1] + rows[i]))
        
      white_x[i] += 200
    white_y += 100
    i += 1

  # draws black checker pieces and puts the squares the checkers are on into a dictionary with the key being the square and the value being the coordinate
  i = 0
    # starting position for drawing black pieces
  black_x = [150, 250, 150]
  black_y = 550
  
  for n in (black_x):
    for n in range(4):
      pygame.draw.circle(window, white, (black_x[i], black_y), 40, 4)

      if i == 1:
        blacksquares[columns[2 * n + 1] + rows[i+5]] = [black_x[i], black_y]

        #creates all black piece objects and assigns their starting attributes
        bpieces.append(piece(color = 'b', king = False, life = True, canmove = False, movelist = [], canjump = False, jumpdict = dict(), square = columns[2 * n + 1] + (str(int(rows[i]) - 5))))

      
      else:
        blacksquares[columns[2 * n] + rows[i+5]] = [black_x[i], black_y]

        #creates all black piece objects and assigns their starting attributes
        bpieces.append(piece(color = 'b', king = False, life = True, canmove = False, movelist = [], canjump = False, jumpdict = dict(), square = columns[2 * n] + (str(int(rows[i]) - 5))))

      black_x[i] += 200
    black_y += 100
    i += 1

  # creates black squares that checkers are not on and adds them to the dictionary with their coordinates
  blacksquares['a5'], blacksquares['c5'], blacksquares['e5'], blacksquares['g5'], blacksquares['b4'], blacksquares['d4'], blacksquares['f4'], blacksquares['h4'] = [150, 350], [350, 350], [550, 350], [750, 350], [250, 450], [450, 450], [650, 450], [850, 450]

  pygame.display.update()




def draw_rules():
  # set background to image of rules
  sourceFileDir = os.path.dirname(os.path.abspath(__file__))
  ImgPath = os.path.join(sourceFileDir, 'checkers_rules.jpg')
  bg = pygame.image.load(ImgPath)
  window.blit(bg,(0,0)) 
  
  font = pygame.font.Font(fontPath, 25)
  text = font.render('[esc] Return to Menu', True, black)
  window.blit(text, (1150, 30))

  pygame.display.update()

  next = True
  while next:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                menu()  




def menu():
  # set background to image of menu
  sourceFileDir = os.path.dirname(os.path.abspath(__file__))

  ImgPath = os.path.join(sourceFileDir, 'menu_norm.jpg')
  bg = pygame.image.load(ImgPath)
  window.blit(bg,(0,0)) 
  pygame.display.update() 


  next = True
  # when menu is open, loop determines next event
  while next:
    for event in pygame.event.get(): 
        if event.type == pygame.KEYDOWN:            
            if event.key == K_3: # quit game
                pygame.quit()
        



        menu_click = False
        if event.type == pygame.MOUSEMOTION:
            while not menu_click:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEMOTION: 
                        pass

                    if event.type == pygame.KEYDOWN: # if key pressed
                        if event.key == pygame.K_3:
                            pygame.quit()
                    
                    if event.type == pygame.QUIT: # if x pressed
                        run = False
                        pygame.quit()


                mouse_x, mouse_y = pygame.mouse.get_pos()


                # play button hover
                if 450 < mouse_x < 990 and 420 < mouse_y < 525:
                    ImgPath = os.path.join(sourceFileDir, 'menu_play.jpg')
                    play = pygame.image.load(ImgPath)
                    window.blit(play,(0,0)) 
                    pygame.display.update()
                    while 450 < mouse_x < 990 and 420 < mouse_y < 525:
                        for event in pygame.event.get():  
                            if event.type == pygame.KEYDOWN:                                
                                if event.key == K_3: # quit game
                                    pygame.quit()
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            menu_click = True
                            draw_board()
                            draw_pieces()
                            gameplay()


                        mouse_x, mouse_y = pygame.mouse.get_pos()
                    ImgPath = os.path.join(sourceFileDir, 'menu_norm.jpg')
                    bg = pygame.image.load(ImgPath)
                    window.blit(bg,(0,0)) 
                    pygame.display.update() 
                    

                # rules button hover
                if  455 < mouse_x < 990 and 555 < mouse_y < 655:
                    ImgPath = os.path.join(sourceFileDir, 'menu_rules.jpg')
                    rules = pygame.image.load(ImgPath)
                    window.blit(rules,(0,0))
                    pygame.display.update()
                    while 455 < mouse_x < 990 and 555 < mouse_y < 655:
                        for event in pygame.event.get():  
                            if event.type == pygame.KEYDOWN:
                                if event.key == K_3: # quit game
                                    pygame.quit()
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            menu_click = True
                            draw_rules()
                        

                        mouse_x, mouse_y = pygame.mouse.get_pos()


                    ImgPath = os.path.join(sourceFileDir, 'menu_norm.jpg')
                    bg = pygame.image.load(ImgPath)
                    window.blit(bg,(0,0)) 
                    pygame.display.update() 


                # quit button hover
                if 455 < mouse_x < 990 and 685 < mouse_y < 790:
                    ImgPath = os.path.join(sourceFileDir, 'menu_quit.jpg')
                    quit_game = pygame.image.load(ImgPath)
                    window.blit(quit_game,(0,0))
                    pygame.display.update()
                    while 455 < mouse_x < 990 and 685 < mouse_y < 790:
                        for event in pygame.event.get():  
                            if event.type == pygame.KEYDOWN:
                                if event.key == K_3: # quit game
                                    pygame.quit()
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            menu_click = True
                            pygame.quit()
                        mouse_x, mouse_y = pygame.mouse.get_pos()


                    ImgPath = os.path.join(sourceFileDir, 'menu_norm.jpg')
                    bg = pygame.image.load(ImgPath)
                    window.blit(bg,(0,0)) 
                    pygame.display.update() 
            

        if event.type == pygame.QUIT: # quit game
            pygame.quit()









# function to return the key (square) given its corresponding value (coordinates) and the dictionary you are finding from
def coordstosquare(des_sqr_coords:list, blacksquares: dict):
    for square, coords in blacksquares.items():
        if des_sqr_coords == coords:
            return square
            break





# checks if a singular piece can move, returns a possible captures list and moves list for the piece, and whether jumps need to be forced this turn
# ex. movability(currentpiece, currentpiece.color, bpieces (maybe make these list names automatic somehow))

def movability(currentpiece, sameteampiecelist, oppteampiecelist):
    currentcoords = blacksquares.get(currentpiece.square) # gets current coordinates of square of checker
    oppblock = False # tells if move is blocked by opposite colored piece, must be proven true
    currentpiece.movelist.clear() # resetting the movelist and jumpdict
    currentpiece.jumpdict.clear()
    currentpiece.canmove = True # resetting canmove and canjump (True until proven False)
    currentpiece.canjump = True

    # checking movability for individual KING piece in all 4 directions
    if currentpiece.king == True:

        # BOTTOM RIGHT SQUARE
        if currentpiece.canmove == True: # canmove is true until proven False, which is done with this function
            if currentcoords[0] > 800 or currentcoords[1] > 700: # CHECKS IF MOVE (AND JUMP) GOES OFF THE BOARD
                currentpiece.canmove = False # piece cannot move off the board
                currentpiece.canjump = False # piece cannot jump off the board
        
        if currentpiece.canmove == True: # canjump too, but doesn't matter because both are together at this point
            for i in sameteampiecelist: # cycles through the coords of each white piece
                testcoords = blacksquares.get(i.square) # putting the square (ex. 'a1') through the dictionary to get the coordinates and storing them
                if testcoords == [currentcoords[0] + 100, currentcoords[1] + 100]: # CHECKS IF MOVE IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canmove = False # cannot move onto another white (same color) piece
                    currentpiece.canjump = False # cannot jump over another white (same color) piece
                    break

        if currentpiece.canjump == True: # still doesnt matter whether canjump or canmove    
            if currentcoords[0] > 700 or currentcoords[1] > 600: # CHECKS IF JUMP GOES OFF BOARD
                currentpiece.canjump = False # cannot jump off board

        if currentpiece.canjump == True:
            for i in oppteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] + 200, currentcoords[1] + 200]: # TESTS IF JUMP IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                    currentpiece.canjump = False
                    break

        if currentpiece.canjump == True:
            for i in sameteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] + 200, currentcoords[1] + 200]: # TESTS IF JUMP IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canjump = False
                    break 

        for i in oppteampiecelist:      
            testcoords = blacksquares.get(i.square) 
            if testcoords == [currentcoords[0] + 100, currentcoords[1] + 100]: # CHECKS IF MOVE IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                currentpiece.canmove = False
                oppblock = True
                jumpedpiecesquare = i.square
                break

        if oppblock == False: # CHECKS IF MOVE IS BLOCKED BY (OPPOSITE TEAM) PIECE
            currentpiece.canjump = False
        oppblock = False # resetting oppblock for next checks


        if currentpiece.canmove == True:
            newmove = coordstosquare([currentcoords[0] + 100, currentcoords[1] + 100], blacksquares)
            currentpiece.movelist.append(newmove)
        currentpiece.canmove = True # resetting canmove to True
        
        if currentpiece.canjump == True:
            newjump = coordstosquare([currentcoords[0] + 200, currentcoords[1] + 200], blacksquares)
            currentpiece.jumpdict.update({newjump: jumpedpiecesquare})
        currentpiece.canjump = True # resetting canjump to True


    


        # TOP RIGHT SQUARE
        if currentpiece.canmove == True: # canmove is true until proven False, which is done with this function
            if currentcoords[0] > 800 or currentcoords[1] < 100: # CHECKS IF MOVE (AND JUMP) GOES OFF THE BOARD
                currentpiece.canmove = False # piece cannot move off the board
                currentpiece.canjump = False # piece cannot jump off the board
        
        if currentpiece.canmove == True: # canjump too, but doesn't matter because both are together at this point
            for i in sameteampiecelist: # cycles through the coords of each white piece
                testcoords = blacksquares.get(i.square) # putting the square (ex. 'a1') through the dictionary to get the coordinates and storing them
                if testcoords == [currentcoords[0] + 100, currentcoords[1] - 100]: # CHECKS IF MOVE IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canmove = False # cannot move onto another white (same color) piece
                    currentpiece.canjump = False # cannot jump over another white (same color) piece
                    break

        if currentpiece.canjump == True: # still doesnt matter whether canjump or canmove    
            if currentcoords[0] > 700 or currentcoords[1] < 200: # CHECKS IF JUMP GOES OFF BOARD
                currentpiece.canjump = False # cannot jump off board

        if currentpiece.canjump == True:
            for i in oppteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] + 200, currentcoords[1] - 200]: # TESTS IF JUMP IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                    currentpiece.canjump = False
                    break

        if currentpiece.canjump == True:
            for i in sameteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] + 200, currentcoords[1] - 200]: # TESTS IF JUMP IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canjump = False
                    break 

        for i in oppteampiecelist:      
            testcoords = blacksquares.get(i.square) 
            if testcoords == [currentcoords[0] + 100, currentcoords[1] - 100]: # CHECKS IF MOVE IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                currentpiece.canmove = False
                oppblock = True
                jumpedpiecesquare = i.square
                break

        if oppblock == False: # CHECKS IF MOVE IS BLOCKED BY (OPPOSITE TEAM) PIECE
            currentpiece.canjump = False
        oppblock = False # resetting oppblock for next checks


        if currentpiece.canmove == True:
            newmove = coordstosquare([currentcoords[0] + 100, currentcoords[1] - 100], blacksquares)
            currentpiece.movelist.append(newmove)
        currentpiece.canmove = True # resetting canmove to True
        
        if currentpiece.canjump == True:
            newjump = coordstosquare([currentcoords[0] + 200, currentcoords[1] - 200], blacksquares)
            currentpiece.jumpdict.update({newjump: jumpedpiecesquare})
        currentpiece.canjump = True # resetting canjump to True  
        




        # BOTTOM LEFT SQUARE
        if currentpiece.canmove == True: # canmove is true until proven False, which is done with this function
            if currentcoords[0] < 200 or currentcoords[1] > 700: # CHECKS IF MOVE (AND JUMP) GOES OFF THE BOARD
                currentpiece.canmove = False # piece cannot move off the board
                currentpiece.canjump = False # piece cannot jump off the board
        
        if currentpiece.canmove == True: # canjump too, but doesn't matter because both are together at this point
            for i in sameteampiecelist: # cycles through the coords of each white piece
                testcoords = blacksquares.get(i.square) # putting the square (ex. 'a1') through the dictionary to get the coordinates and storing them
                if testcoords == [currentcoords[0] - 100, currentcoords[1] + 100]: # CHECKS IF MOVE IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canmove = False # cannot move onto another white (same color) piece
                    currentpiece.canjump = False # cannot jump over another white (same color) piece
                    break

        if currentpiece.canjump == True: # still doesnt matter whether canjump or canmove    
            if currentcoords[0] < 300 or currentcoords[1] > 600: # CHECKS IF JUMP GOES OFF BOARD
                currentpiece.canjump = False # cannot jump off board

        if currentpiece.canjump == True:
            for i in oppteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] - 200, currentcoords[1] + 200]: # TESTS IF JUMP IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                    currentpiece.canjump = False
                    break

        if currentpiece.canjump == True:
            for i in sameteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] - 200, currentcoords[1] + 200]: # TESTS IF JUMP IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canjump = False
                    break 

        for i in oppteampiecelist:      
            testcoords = blacksquares.get(i.square) 
            if testcoords == [currentcoords[0] - 100, currentcoords[1] + 100]: # CHECKS IF MOVE IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                currentpiece.canmove = False
                oppblock = True
                jumpedpiecesquare = i.square
                break

        if oppblock == False: # CHECKS IF MOVE IS BLOCKED BY (OPPOSITE TEAM) PIECE
            currentpiece.canjump = False
        oppblock = False # resetting oppblock for next checks


        if currentpiece.canmove == True:
            newmove = coordstosquare([currentcoords[0] - 100, currentcoords[1] + 100], blacksquares)
            currentpiece.movelist.append(newmove)
        currentpiece.canmove = True # resetting canmove to True
        
        if currentpiece.canjump == True:
            newjump = coordstosquare([currentcoords[0] - 200, currentcoords[1] + 200], blacksquares)
            currentpiece.jumpdict.update({newjump: jumpedpiecesquare})
        currentpiece.canjump = True # resetting canjump to True





        # TOP LEFT SQUARE
        if currentpiece.canmove == True: # canmove is true until proven False, which is done with this function
            if currentcoords[0] < 200 or currentcoords[1] < 100: # CHECKS IF MOVE (AND JUMP) GOES OFF THE BOARD
                currentpiece.canmove = False # piece cannot move off the board
                currentpiece.canjump = False # piece cannot jump off the board
        
        if currentpiece.canmove == True: # canjump too, but doesn't matter because both are together at this point
            for i in sameteampiecelist: # cycles through the coords of each white piece
                testcoords = blacksquares.get(i.square) # putting the square (ex. 'a1') through the dictionary to get the coordinates and storing them
                if testcoords == [currentcoords[0] - 100, currentcoords[1] - 100]: # CHECKS IF MOVE IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canmove = False # cannot move onto another white (same color) piece
                    currentpiece.canjump = False # cannot jump over another white (same color) piece
                    break

        if currentpiece.canjump == True: # still doesnt matter whether canjump or canmove    
            if currentcoords[0] < 300 or currentcoords[1] < 200: # CHECKS IF JUMP GOES OFF BOARD
                currentpiece.canjump = False # cannot jump off board

        if currentpiece.canjump == True:
            for i in oppteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] - 200, currentcoords[1] - 200]: # TESTS IF JUMP IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                    currentpiece.canjump = False
                    break

        if currentpiece.canjump == True:
            for i in sameteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] - 200, currentcoords[1] - 200]: # TESTS IF JUMP IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canjump = False
                    break 

        for i in oppteampiecelist:      
            testcoords = blacksquares.get(i.square) 
            if testcoords == [currentcoords[0] - 100, currentcoords[1] - 100]: # CHECKS IF MOVE IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                currentpiece.canmove = False
                oppblock = True
                jumpedpiecesquare = i.square
                break

        if oppblock == False: # CHECKS IF MOVE IS BLOCKED BY (OPPOSITE TEAM) PIECE
            currentpiece.canjump = False
        oppblock = False # resetting oppblock for next checks


        if currentpiece.canmove == True:
            newmove = coordstosquare([currentcoords[0] - 100, currentcoords[1] - 100], blacksquares)
            currentpiece.movelist.append(newmove)
        currentpiece.canmove = True # resetting canmove to True
        
        if currentpiece.canjump == True:
            newjump = coordstosquare([currentcoords[0] - 200, currentcoords[1] - 200], blacksquares)
            currentpiece.jumpdict.update({newjump: jumpedpiecesquare})
        currentpiece.canjump = True # resetting canjump to True




    # checking movability for individual white pawn piece (only downward directions)
    elif currentpiece.color == "w":
       
       # BOTTOM RIGHT SQUARE
        if currentpiece.canmove == True: # canmove is true until proven False, which is done with this function
            if currentcoords[0] > 800 or currentcoords[1] > 700: # CHECKS IF MOVE (AND JUMP) GOES OFF THE BOARD
                currentpiece.canmove = False # piece cannot move off the board
                currentpiece.canjump = False # piece cannot jump off the board
        
        if currentpiece.canmove == True: # canjump too, but doesn't matter because both are together at this point
            for i in sameteampiecelist: # cycles through the coords of each white piece
                testcoords = blacksquares.get(i.square) # putting the square (ex. 'a1') through the dictionary to get the coordinates and storing them
                if testcoords == [currentcoords[0] + 100, currentcoords[1] + 100]: # CHECKS IF MOVE IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canmove = False # cannot move onto another white (same color) piece
                    currentpiece.canjump = False # cannot jump over another white (same color) piece
                    break

        if currentpiece.canjump == True: # still doesnt matter whether canjump or canmove    
            if currentcoords[0] > 700 or currentcoords[1] > 600: # CHECKS IF JUMP GOES OFF BOARD
                currentpiece.canjump = False # cannot jump off board

        if currentpiece.canjump == True:
            for i in oppteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] + 200, currentcoords[1] + 200]: # TESTS IF JUMP IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                    currentpiece.canjump = False
                    break

        if currentpiece.canjump == True:
            for i in sameteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] + 200, currentcoords[1] + 200]: # TESTS IF JUMP IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canjump = False
                    break 

        for i in oppteampiecelist:      
            testcoords = blacksquares.get(i.square) 
            if testcoords == [currentcoords[0] + 100, currentcoords[1] + 100]: # CHECKS IF MOVE IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                currentpiece.canmove = False
                oppblock = True
                jumpedpiecesquare = i.square
                break

        if oppblock == False: # CHECKS IF MOVE IS BLOCKED BY (OPPOSITE TEAM) PIECE
            currentpiece.canjump = False
        oppblock = False # resetting oppblock for next checks


        if currentpiece.canmove == True:
            newmove = coordstosquare([currentcoords[0] + 100, currentcoords[1] + 100], blacksquares)
            currentpiece.movelist.append(newmove)
        currentpiece.canmove = True # resetting canmove to True
        
        if currentpiece.canjump == True:
            newjump = coordstosquare([currentcoords[0] + 200, currentcoords[1] + 200], blacksquares)
            currentpiece.jumpdict.update({newjump: jumpedpiecesquare})
        currentpiece.canjump = True # resetting canjump to True




        # BOTTOM LEFT SQUARE
        if currentpiece.canmove == True: # canmove is true until proven False, which is done with this function
            if currentcoords[0] < 200 or currentcoords[1] > 700: # CHECKS IF MOVE (AND JUMP) GOES OFF THE BOARD
                currentpiece.canmove = False # piece cannot move off the board
                currentpiece.canjump = False # piece cannot jump off the board
        
        if currentpiece.canmove == True: # canjump too, but doesn't matter because both are together at this point
            for i in sameteampiecelist: # cycles through the coords of each white piece
                testcoords = blacksquares.get(i.square) # putting the square (ex. 'a1') through the dictionary to get the coordinates and storing them
                if testcoords == [currentcoords[0] - 100, currentcoords[1] + 100]: # CHECKS IF MOVE IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canmove = False # cannot move onto another white (same color) piece
                    currentpiece.canjump = False # cannot jump over another white (same color) piece
                    break

        if currentpiece.canjump == True: # still doesnt matter whether canjump or canmove    
            if currentcoords[0] < 300 or currentcoords[1] > 600: # CHECKS IF JUMP GOES OFF BOARD
                currentpiece.canjump = False # cannot jump off board

        if currentpiece.canjump == True:
            for i in oppteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] - 200, currentcoords[1] + 200]: # TESTS IF JUMP IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                    currentpiece.canjump = False
                    break

        if currentpiece.canjump == True:
            for i in sameteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] - 200, currentcoords[1] + 200]: # TESTS IF JUMP IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canjump = False
                    break 

        for i in oppteampiecelist:      
            testcoords = blacksquares.get(i.square) 
            if testcoords == [currentcoords[0] - 100, currentcoords[1] + 100]: # CHECKS IF MOVE IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                currentpiece.canmove = False
                oppblock = True
                jumpedpiecesquare = i.square
                break

        if oppblock == False: # CHECKS IF MOVE IS BLOCKED BY (OPPOSITE TEAM) PIECE
            currentpiece.canjump = False
        oppblock = False # resetting oppblock for next checks


        if currentpiece.canmove == True:
            newmove = coordstosquare([currentcoords[0] - 100, currentcoords[1] + 100], blacksquares)
            currentpiece.movelist.append(newmove)
        currentpiece.canmove = True # resetting canmove to True
        
        if currentpiece.canjump == True:
            newjump = coordstosquare([currentcoords[0] - 200, currentcoords[1] + 200], blacksquares)
            currentpiece.jumpdict.update({newjump: jumpedpiecesquare})
        currentpiece.canjump = True # resetting canjump to True





    # checking movability for individual black pawn piece (only upward directions)
    elif currentpiece.color == "b":

        # TOP RIGHT SQUARE
        if currentpiece.canmove == True: # canmove is true until proven False, which is done with this function
            if currentcoords[0] > 800 or currentcoords[1] < 100: # CHECKS IF MOVE (AND JUMP) GOES OFF THE BOARD
                currentpiece.canmove = False # piece cannot move off the board
                currentpiece.canjump = False # piece cannot jump off the board
        
        if currentpiece.canmove == True: # canjump too, but doesn't matter because both are together at this point
            for i in sameteampiecelist: # cycles through the coords of each white piece
                testcoords = blacksquares.get(i.square) # putting the square (ex. 'a1') through the dictionary to get the coordinates and storing them
                if testcoords == [currentcoords[0] + 100, currentcoords[1] - 100]: # CHECKS IF MOVE IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canmove = False # cannot move onto another white (same color) piece
                    currentpiece.canjump = False # cannot jump over another white (same color) piece
                    break

        if currentpiece.canjump == True: # still doesnt matter whether canjump or canmove    
            if currentcoords[0] > 700 or currentcoords[1] < 200: # CHECKS IF JUMP GOES OFF BOARD
                currentpiece.canjump = False # cannot jump off board

        if currentpiece.canjump == True:
            for i in oppteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] + 200, currentcoords[1] - 200]: # TESTS IF JUMP IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                    currentpiece.canjump = False
                    break

        if currentpiece.canjump == True:
            for i in sameteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] + 200, currentcoords[1] - 200]: # TESTS IF JUMP IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canjump = False
                    break 

        for i in oppteampiecelist:      
            testcoords = blacksquares.get(i.square) 
            if testcoords == [currentcoords[0] + 100, currentcoords[1] - 100]: # CHECKS IF MOVE IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                currentpiece.canmove = False
                oppblock = True
                jumpedpiecesquare = i.square
                break

        if oppblock == False: # CHECKS IF MOVE IS BLOCKED BY (OPPOSITE TEAM) PIECE
            currentpiece.canjump = False
        oppblock = False # resetting oppblock for next checks


        if currentpiece.canmove == True:
            newmove = coordstosquare([currentcoords[0] + 100, currentcoords[1] - 100], blacksquares)
            currentpiece.movelist.append(newmove)
        currentpiece.canmove = True # resetting canmove to True
        
        if currentpiece.canjump == True:
            newjump = coordstosquare([currentcoords[0] + 200, currentcoords[1] - 200], blacksquares)
            currentpiece.jumpdict.update({newjump: jumpedpiecesquare})
        currentpiece.canjump = True # resetting canjump to True




        # TOP LEFT SQUARE
        if currentpiece.canmove == True: # canmove is true until proven False, which is done with this function
            if currentcoords[0] < 200 or currentcoords[1] < 100: # CHECKS IF MOVE (AND JUMP) GOES OFF THE BOARD
                currentpiece.canmove = False # piece cannot move off the board
                currentpiece.canjump = False # piece cannot jump off the board
        
        if currentpiece.canmove == True: # canjump too, but doesn't matter because both are together at this point
            for i in sameteampiecelist: # cycles through the coords of each white piece
                testcoords = blacksquares.get(i.square) # putting the square (ex. 'a1') through the dictionary to get the coordinates and storing them
                if testcoords == [currentcoords[0] - 100, currentcoords[1] - 100]: # CHECKS IF MOVE IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canmove = False # cannot move onto another white (same color) piece
                    currentpiece.canjump = False # cannot jump over another white (same color) piece
                    break

        if currentpiece.canjump == True: # still doesnt matter whether canjump or canmove    
            if currentcoords[0] < 300 or currentcoords[1] < 200: # CHECKS IF JUMP GOES OFF BOARD
                currentpiece.canjump = False # cannot jump off board

        if currentpiece.canjump == True:
            for i in oppteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] - 200, currentcoords[1] - 200]: # TESTS IF JUMP IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                    currentpiece.canjump = False
                    break

        if currentpiece.canjump == True:
            for i in sameteampiecelist:
                testcoords = blacksquares.get(i.square)
                if testcoords == [currentcoords[0] - 200, currentcoords[1] - 200]: # TESTS IF JUMP IS BLOCKED BY WHITE (SAME TEAM) PIECE
                    currentpiece.canjump = False
                    break 

        for i in oppteampiecelist:      
            testcoords = blacksquares.get(i.square) 
            if testcoords == [currentcoords[0] - 100, currentcoords[1] - 100]: # CHECKS IF MOVE IS BLOCKED BY BLACK (OPPOSITE TEAM) PIECE
                currentpiece.canmove = False
                oppblock = True
                jumpedpiecesquare = i.square
                break

        if oppblock == False: # CHECKS IF MOVE IS BLOCKED BY (OPPOSITE TEAM) PIECE
            currentpiece.canjump = False
        oppblock = False # resetting oppblock for next checks


        if currentpiece.canmove == True:
            newmove = coordstosquare([currentcoords[0] - 100, currentcoords[1] - 100], blacksquares)
            currentpiece.movelist.append(newmove)
        currentpiece.canmove = True # resetting canmove to True
        
        if currentpiece.canjump == True:
            newjump = coordstosquare([currentcoords[0] - 200, currentcoords[1] - 200], blacksquares)
            currentpiece.jumpdict.update({newjump: jumpedpiecesquare})
        currentpiece.canjump = True # resetting canjump to True
    
    
    # need to return something that shows there is a jump that must be forced (force means must force the jump)
    if len(currentpiece.jumpdict) > 0:
        currentpiece.canjump = True
        currentpiece.canmove = False
        return "force"
    elif len(currentpiece.movelist) > 0:
        currentpiece.canmove = True
        currentpiece.canjump = False
        return "dontforce"
    else:
        currentpiece.canmove = False
        currentpiece.canjump = False
        return "dontforce"
        



# finds current cursor location at all times to determine what square it is on (returns square the cursor is on)
def squarecursorlocation():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for square in blacksquares:
        squarecentercoords = blacksquares.get(square)
        if squarecentercoords[0] - 50 < mouse_x < squarecentercoords[0] + 50 and squarecentercoords[1] - 50 < mouse_y < squarecentercoords[1] + 50: #checks if cursor is on a given square
            mousesquare = square # stores the square the cursor is on into a variable
            return mousesquare
             








#VISUAL STUFF


# draws king symbol, **not circle underneath
def draw_king(square_name):
    # uses image of a crown and puts it on the piece if king
    king_image = pygame.image.load('crownred.png')
    coordslist = blacksquares.get(square_name) # returns coords list from desired square
    
    # sets coordinate to display crown image from
    king_x = coordslist[0] -25
    king_y = coordslist[1] -18

    window.blit(king_image, (king_x, king_y))
    pygame.display.update()


# draws transparent yellow highlight circle
def highlight(square_name):
    highlight = pygame.image.load('highlight.png')
    coordslist = blacksquares.get(square_name) # returns coords list from desired square
    
    highlight_x = coordslist[0] - 40
    highlight_y = coordslist[1] - 40

    window.blit(highlight, (highlight_x, highlight_y))
    pygame.display.update()


# draws transparent blue highlight circle
def highlight_blue(square_name):
    highlight = pygame.image.load('highlight_blue.png')
    coordslist = blacksquares.get(square_name) # returns coords list from desired square
    
    highlight_x = coordslist[0] - 40
    highlight_y = coordslist[1] - 40

    window.blit(highlight, (highlight_x, highlight_y))
    pygame.display.update()


#Function for redrawing board and pieces after a move
def redraw():
    white = (255,255,255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    gray = (127,127,127)

    width, height = 100, 100 # of checker square
    thickness = 0

    # starting positions for drawing the board
    board_x = 100
    board_y = 0

    # drawing the checkerboard (without numbers or letters)
    for n in range(4):
        for n in range(4):
            pygame.draw.rect(window, red, (board_x, board_y, width, height),thickness)
            board_x += 100
            pygame.draw.rect(window, black, (board_x, board_y, width, height),thickness)
            board_x += 100
        board_x = 100
        board_y += 100
        for n in range(4):
            pygame.draw.rect(window, black, (board_x, board_y, width, height),thickness)
            board_x += 100
            pygame.draw.rect(window, red, (board_x, board_y, width, height),thickness)
            board_x += 100
        board_x = 100
        board_y += 100


    # redraw white pieces
    for whitechecker in wpieces:
        wcoords = blacksquares.get(whitechecker.square) # -> list of coords [x,y]
        pygame.draw.circle(window, white, (wcoords[0], wcoords[1]), 40, 0)
        pygame.draw.circle(window, gray, (wcoords[0], wcoords[1]), 36, 2)
        if whitechecker.king == True:
            draw_king(whitechecker.square)


    # redraw black pieces
    for blackchecker in bpieces:
        bcoords = blacksquares.get(blackchecker.square) # -> list of coords [x,y]
        pygame.draw.circle(window, white, (bcoords[0], bcoords[1]), 40, 4) 
        if blackchecker.king == True:
            draw_king(blackchecker.square)

    pygame.display.update()


        














# main gameplay function
def gameplay():
       
    # starting values and constants:
    playing = True
    bwin = False
    wwin = False
    piecemoved = False
    pieceselected = False
    blackpiececapturedlastturn = ""
    whitepiececapturedlastturn = ""
    blackpiecedidcapturelastturn = False
    whitepiecedidcapturelastturn = False



    while playing:
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        menu()
                if event.type == pygame.MOUSEMOTION:
                    run = False
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

        # black turn start:
        piecemoved = False
        pieceselected = False
        

        if blackpiecedidcapturelastturn == True: #if black's piece captured last turn (and has another capture)
            blackpiecedidcapturelastturn = False #resetting value
            bpieces.remove(blackpiececapturedlastturn)
            for checker in bpieces:
                checker.movelist.clear()
                checker.canmove = False
                checker.jumpdict.clear()
                checker.canjump = False
            bpieces.append(blackpiececapturedlastturn)
            blackpiececapturedlastturn.movelist.clear()
        else:
            for checker in bpieces: # scans movability of all black checkers
                ifforce = movability(checker, bpieces, wpieces)
                if ifforce == "force":
                    break # stops loop if jump is detected (for forced jump purposes)

            if ifforce == "force":
                ifforce = "dontforce" # resetting ifforce
                for checker in bpieces: # forced jump loop
                    movability(checker, bpieces, wpieces)
                    checker.movelist.clear()  # clears all moves because jumps need to be forced
                    checker.canmove = False            
        if whitepiecedidcapturelastturn == True:
            movability(whitepiececapturedlastturn, wpieces, bpieces) 
            if len(whitepiececapturedlastturn.jumpdict) > 0:
                pass


    
            else:
                blur_bg2 = pygame.image.load('blur_bg2.jpg')
                window.blit(blur_bg2, (0,0))
                bmove_img = pygame.image.load('blacks_move.png')
                window.blit(bmove_img, (0,0))
                redraw()
                pygame.display.update()

                whitepiecedidcapturelastturn = False

                if len(bpieces) < 1:
                    wwin_img = pygame.image.load('white_wins.png')
                    window.blit(wwin_img, (0,0))
                    pygame.display.update()
               
                # unmovablecheckerlist = [] #resetting the list
                # for checker in bpieces:
                #     if len(checker.movelist) + len(checker.jumpdict) < 1: #checking if any checker can move (win condition)
                #         unmovablecheckerlist.append(checker)
                #     else:
                #         break
                #     if len(unmovablecheckerlist) == len(bpieces):
                        # playing = False
                        # wwin_img = pygame.image.load('white_wins.png')
                        # window.blit(wwin_img, (0,0))
                        # pygame.display.update()
        
        
                if playing == True:
                    while piecemoved == False: # loop for selecting a piece
                        run = True
                        while run:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        run = False
                                        menu()
                                if event.type == pygame.MOUSEMOTION:
                                    run = False
                                if event.type == pygame.QUIT:
                                    run = False
                                    pygame.quit()
                        for piece in bpieces:
                            if piece.square == squarecursorlocation() and (piece.canmove or piece.canjump): # checking if piece location equals the cursor location, and if the piece has a move or jump
                                highlight(piece.square) # highlights checker the cursor is hovering over if it isnt already selected (clicked_)
                                while piece.square == squarecursorlocation(): #keeps checking if cursor is still on the piece
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button is clicked
                                            redraw()
                                            pieceselected = True
                                            currentmovehighlightpiece = piece
                                            highlight(currentmovehighlightpiece.square)
                                            for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                                highlight(squaremove)
                                            for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                                highlight(squarejump)
                                            break #breaks out of pygame.event loop after piece is selected (necessary??)
                                redraw() # redraws, then redraws the selected piece and its moves (after cursor goes off of piece)
                                if pieceselected:
                                    highlight(currentmovehighlightpiece.square)
                                    for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                        highlight(squaremove)
                                    for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                        highlight(squarejump)
                        
                        
                        if pieceselected:                      
                            for square in currentmovehighlightpiece.movelist: #checking through movelist of selected piece
                                if square == squarecursorlocation():
                                    highlight_blue(square)
                                    while square == squarecursorlocation():
                                        for event in pygame.event.get():
                                            if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button is clicked (MOVE IS MADE)
                                                currentmovehighlightpiece.square = squarecursorlocation() #moves piece
                                                piecemoved = True
                                                pieceselected = False    #ENDS BLACK TURN
                                                if "8" in squarecursorlocation():
                                                    currentmovehighlightpiece.king = True
                                                redraw()
                                                #break                                
                                    redraw()
                                    if pieceselected:
                                        highlight(currentmovehighlightpiece.square)
                                        for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                            highlight(squaremove)
                                        for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                            highlight(squarejump)

                            if piecemoved == False: #so after move it doesnt go through jumps        
                                for square in currentmovehighlightpiece.jumpdict: #checking through jumpdict of selected piece
                                    if square == squarecursorlocation():
                                        highlight_blue(square)
                                        while square == squarecursorlocation():
                                            for event in pygame.event.get():
                                                if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button is clicked
                                                    currentmovehighlightpiece.square = squarecursorlocation() #jumps piece
                                                    piecemoved = True
                                                    pieceselected = False    #ENDS BLACK TURN
                                                    if "8" in squarecursorlocation():
                                                        currentmovehighlightpiece.king = True
                                                    killedcheckersquare = currentmovehighlightpiece.jumpdict.get(currentmovehighlightpiece.square) #finds the square the checker jumped (which an opponent piece is on)
                                                    for checker in wpieces: #finds killed checker and removes it
                                                        if checker.square == killedcheckersquare:
                                                            wpieces.remove(checker)
                                                            break
                                                    redraw()
                                                    blackpiececapturedlastturn = currentmovehighlightpiece
                                                    blackpiecedidcapturelastturn = True

                                                    
                                        redraw()
                                        if pieceselected:
                                            highlight(currentmovehighlightpiece.square)
                                            for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                                highlight(squaremove)
                                            for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                                highlight(squarejump)
        else:
            blur_bg2 = pygame.image.load('blur_bg2.jpg')
            window.blit(blur_bg2, (0,0))
            bmove_img = pygame.image.load('blacks_move.png')
            window.blit(bmove_img, (0,0))
            redraw()
            pygame.display.update()

            
            whitepiecedidcapturelastturn = False
            if len(bpieces) < 1:
                wwin_img = pygame.image.load('white_wins.png')
                window.blit(wwin_img, (0,0))
                pygame.display.update()
            # unmovablecheckerlist = [] #resetting the list
            # for checker in bpieces:
            #     if len(checker.movelist) + len(checker.jumpdict) < 1: #checking if any checker can move (win condition)
            #         unmovablecheckerlist.append(checker)
            #     else:
            #         break
            #     if len(unmovablecheckerlist) == len(bpieces):
            #         playing = False
            #         wwin_img = pygame.image.load('white_wins.png')
            #         window.blit(wwin_img, (0,0))
            #         pygame.display.update()
    
    
            if playing == True:
                while piecemoved == False: # loop for selecting a piece
                    run = True
                    while run:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    run = False
                                    menu()
                            if event.type == pygame.MOUSEMOTION:
                                run = False
                            if event.type == pygame.QUIT:
                                run = False
                                pygame.quit()
                    for piece in bpieces:
                        if piece.square == squarecursorlocation() and (piece.canmove or piece.canjump): # checking if piece location equals the cursor location, and if the piece has a move or jump
                            highlight(piece.square) # highlights checker the cursor is hovering over if it isnt already selected (clicked_)
                            while piece.square == squarecursorlocation(): #keeps checking if cursor is still on the piece
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button is clicked
                                        redraw()
                                        pieceselected = True
                                        currentmovehighlightpiece = piece
                                        highlight(currentmovehighlightpiece.square)
                                        for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                            highlight(squaremove)
                                        for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                            highlight(squarejump)
                                        break #breaks out of pygame.event loop after piece is selected (necessary??)
                            redraw() # redraws, then redraws the selected piece and its moves (after cursor goes off of piece)
                            if pieceselected:
                                highlight(currentmovehighlightpiece.square)
                                for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                    highlight(squaremove)
                                for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                    highlight(squarejump)
                    
                    
                    if pieceselected:                      
                        for square in currentmovehighlightpiece.movelist: #checking through movelist of selected piece
                            if square == squarecursorlocation():
                                highlight_blue(square)
                                while square == squarecursorlocation():
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button is clicked (MOVE IS MADE)
                                            currentmovehighlightpiece.square = squarecursorlocation() #moves piece
                                            piecemoved = True
                                            pieceselected = False    #ENDS BLACK TURN
                                            if "8" in squarecursorlocation():
                                                currentmovehighlightpiece.king = True
                                            redraw()
                                            #break                                
                                redraw()
                                if pieceselected:
                                    highlight(currentmovehighlightpiece.square)
                                    for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                        highlight(squaremove)
                                    for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                        highlight(squarejump)

                        if piecemoved == False: #so after move it doesnt go through jumps        
                            for square in currentmovehighlightpiece.jumpdict: #checking through jumpdict of selected piece
                                if square == squarecursorlocation():
                                    highlight_blue(square)
                                    while square == squarecursorlocation():
                                        for event in pygame.event.get():
                                            if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button is clicked
                                                currentmovehighlightpiece.square = squarecursorlocation() #jumps piece
                                                piecemoved = True
                                                pieceselected = False    #ENDS BLACK TURN
                                                if "8" in squarecursorlocation():
                                                    currentmovehighlightpiece.king = True
                                                killedcheckersquare = currentmovehighlightpiece.jumpdict.get(currentmovehighlightpiece.square) #finds the square the checker jumped (which an opponent piece is on)
                                                for checker in wpieces: #finds killed checker and removes it
                                                    if checker.square == killedcheckersquare:
                                                        wpieces.remove(checker)
                                                        break
                                                redraw()
                                                blackpiececapturedlastturn = currentmovehighlightpiece
                                                blackpiecedidcapturelastturn = True

                                                
                                    redraw()
                                    if pieceselected:
                                        highlight(currentmovehighlightpiece.square)
                                        for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                            highlight(squaremove)
                                        for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                            highlight(squarejump)
                

        # white turn start:
        piecemoved = False
        pieceselected = False

        if whitepiecedidcapturelastturn == True: #if white's piece captured last turn (and has another capture)
            whitepiecedidcapturelastturn = False #resetting value
            wpieces.remove(whitepiececapturedlastturn)
            for checker in wpieces:
                checker.movelist.clear()
                checker.canmove = False
                checker.jumpdict.clear()
                checker.canjump = False
            wpieces.append(whitepiececapturedlastturn)
            whitepiececapturedlastturn.movelist.clear()
        else:
            for checker in wpieces: # scans movability of all white checkers
                ifforce = movability(checker, wpieces, bpieces)
                if ifforce == "force": 
                    break # stops loop if jump is detected (for forced jump purposes)
            
            if ifforce == "force":
                ifforce = "dontforce" # resetting ifforce
                for checker in wpieces: # forced jump loop
                    movability(checker, wpieces, bpieces)
                    checker.movelist.clear()  # clears all moves because jumps need to be forced
                    checker.canmove = False
        
        
        if blackpiecedidcapturelastturn == True:
            movability(blackpiececapturedlastturn, bpieces, wpieces) 
            if len(blackpiececapturedlastturn.jumpdict) > 0:
                pass
            else:
                blur_bg2 = pygame.image.load('blur_bg2.jpg')
                window.blit(blur_bg2, (0,0))
                wmove_img = pygame.image.load('whites_move.png')
                window.blit(wmove_img, (0,0))
                redraw()
                pygame.display.update()

                blackpiecedidcapturelastturn = False

                if len(wpieces) < 1:
                    bwin_img = pygame.image.load('black_wins.png')
                    window.blit(bwin_img, (0,0))
                    pygame.display.update()
                # unmovablecheckerlist = [] #resetting the list
                # for checker in wpieces:
                #     if len(checker.movelist) + len(checker.jumpdict) < 1: #checking if any checker can move (win condition)
                #         unmovablecheckerlist.append(checker)
                #     else:
                #         break
                #     if len(unmovablecheckerlist) == len(wpieces):
                #         playing = False
                #         bwin_img = pygame.image.load('black_wins.png')
                #         window.blit(bwin_img, (0,0))
                #         pygame.display.update()
                
                
                if playing == True:
                    while piecemoved == False: # loop for selecting a piece
                        run = True
                        while run:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        run = False
                                        menu()
                                if event.type == pygame.MOUSEMOTION:
                                    run = False
                                if event.type == pygame.QUIT:
                                    run = False
                                    pygame.quit()
                        for piece in wpieces:
                            if piece.square == squarecursorlocation() and (piece.canmove or piece.canjump): # checking if piece location equals the cursor location, and if the piece has a move or jump
                                highlight(piece.square) # highlights checker the cursor is hovering over if it isnt already selected (clicked_)
                                while piece.square == squarecursorlocation(): #keeps checking if cursor is still on the piece
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button is clicked
                                            redraw()
                                            pieceselected = True
                                            currentmovehighlightpiece = piece
                                            highlight(currentmovehighlightpiece.square)
                                            for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                                highlight(squaremove)
                                            for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                                highlight(squarejump)
                                            break #breaks out of pygame.event loop after piece is selected (necessary??)
                                redraw() # redraws, then redraws the selected piece and its moves (after cursor goes off of piece)
                                if pieceselected:
                                    highlight(currentmovehighlightpiece.square)
                                    for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                        highlight(squaremove)
                                    for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                        highlight(squarejump)
                        
                        
                        if pieceselected:                      
                            for square in currentmovehighlightpiece.movelist: #checking through movelist of selected piece
                                if square == squarecursorlocation():
                                    highlight_blue(square)
                                    while square == squarecursorlocation():
                                        for event in pygame.event.get():
                                            if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button is clicked (MOVE IS MADE)
                                                currentmovehighlightpiece.square = squarecursorlocation() #moves piece
                                                piecemoved = True
                                                pieceselected = False    #ENDS WHITE TURN
                                                if "1" in squarecursorlocation():
                                                    currentmovehighlightpiece.king = True
                                                redraw()
                                                #break                                
                                    redraw()
                                    if pieceselected:
                                        highlight(currentmovehighlightpiece.square)
                                        for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                            highlight(squaremove)
                                        for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                            highlight(squarejump)

                            if piecemoved == False: #so after move it doesnt go through jumps        
                                for square in currentmovehighlightpiece.jumpdict: #checking through jumpdict of selected piece
                                    if square == squarecursorlocation():
                                        highlight_blue(square)
                                        while square == squarecursorlocation():
                                            for event in pygame.event.get():
                                                if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button is clicked
                                                    currentmovehighlightpiece.square = squarecursorlocation() #jumps piece
                                                    piecemoved = True
                                                    pieceselected = False    #ENDS BLACK TURN
                                                    if "1" in squarecursorlocation():
                                                        currentmovehighlightpiece.king = True
                                                    killedcheckersquare = currentmovehighlightpiece.jumpdict.get(currentmovehighlightpiece.square) #finds the square the checker jumped (which an opponent piece is on)
                                                    for checker in bpieces:
                                                        if checker.square == killedcheckersquare:
                                                            bpieces.remove(checker)
                                                            break
                                                    redraw()
                                                    whitepiececapturedlastturn = currentmovehighlightpiece
                                                    whitepiecedidcapturelastturn = True
                                                    
                                        redraw()
                                        if pieceselected:
                                            highlight(currentmovehighlightpiece.square)
                                            for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                                highlight(squaremove)
                                            for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                                highlight(squarejump)
        else:
            blur_bg2 = pygame.image.load('blur_bg2.jpg')
            window.blit(blur_bg2, (0,0))
            wmove_img = pygame.image.load('whites_move.png')
            window.blit(wmove_img, (0,0))
            redraw()
            pygame.display.update()
            

            blackpiecedidcapturelastturn = False

            if len(wpieces) < 1:
                bwin_img = pygame.image.load('black_wins.png')
                window.blit(bwin_img, (0,0))
                pygame.display.update()
            # unmovablecheckerlist = [] #resetting the list
            # for checker in wpieces:
            #     if len(checker.movelist) + len(checker.jumpdict) < 1: #checking if any checker can move (win condition)
            #         unmovablecheckerlist.append(checker)
            #     else:
            #         break
            #     if len(unmovablecheckerlist) == len(wpieces):
            #         playing = False
            #         bwin_img = pygame.image.load('black_wins.png')
            #         window.blit(bwin_img, (0,0))
            #         pygame.display.update()
            
            
            if playing == True:
                while piecemoved == False: # loop for selecting a piece
                    run = True
                    while run:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    run = False
                                    menu()
                            if event.type == pygame.MOUSEMOTION:
                                run = False
                            if event.type == pygame.QUIT:
                                run = False
                                pygame.quit()
                    for piece in wpieces:
                        if piece.square == squarecursorlocation() and (piece.canmove or piece.canjump): # checking if piece location equals the cursor location, and if the piece has a move or jump
                            highlight(piece.square) # highlights checker the cursor is hovering over if it isnt already selected (clicked_)
                            while piece.square == squarecursorlocation(): #keeps checking if cursor is still on the piece
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button is clicked
                                        redraw()
                                        pieceselected = True
                                        currentmovehighlightpiece = piece
                                        highlight(currentmovehighlightpiece.square)
                                        for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                            highlight(squaremove)
                                        for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                            highlight(squarejump)
                                        break #breaks out of pygame.event loop after piece is selected (necessary??)
                            redraw() # redraws, then redraws the selected piece and its moves (after cursor goes off of piece)
                            if pieceselected:
                                highlight(currentmovehighlightpiece.square)
                                for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                    highlight(squaremove)
                                for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                    highlight(squarejump)
                    
                    
                    if pieceselected:                      
                        for square in currentmovehighlightpiece.movelist: #checking through movelist of selected piece
                            if square == squarecursorlocation():
                                highlight_blue(square)
                                while square == squarecursorlocation():
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button is clicked (MOVE IS MADE)
                                            currentmovehighlightpiece.square = squarecursorlocation() #moves piece
                                            piecemoved = True
                                            pieceselected = False    #ENDS WHITE TURN
                                            if "1" in squarecursorlocation():
                                                currentmovehighlightpiece.king = True
                                            redraw()
                                            #break                                
                                redraw()
                                if pieceselected:
                                    highlight(currentmovehighlightpiece.square)
                                    for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                        highlight(squaremove)
                                    for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                        highlight(squarejump)

                        if piecemoved == False: #so after move it doesnt go through jumps        
                            for square in currentmovehighlightpiece.jumpdict: #checking through jumpdict of selected piece
                                if square == squarecursorlocation():
                                    highlight_blue(square)
                                    while square == squarecursorlocation():
                                        for event in pygame.event.get():
                                            if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button is clicked
                                                currentmovehighlightpiece.square = squarecursorlocation() #jumps piece
                                                piecemoved = True
                                                pieceselected = False    #ENDS BLACK TURN
                                                if "1" in squarecursorlocation():
                                                    currentmovehighlightpiece.king = True
                                                killedcheckersquare = currentmovehighlightpiece.jumpdict.get(currentmovehighlightpiece.square) #finds the square the checker jumped (which an opponent piece is on)
                                                for checker in bpieces:
                                                    if checker.square == killedcheckersquare:
                                                        bpieces.remove(checker)
                                                        break
                                                redraw()
                                                whitepiececapturedlastturn = currentmovehighlightpiece
                                                whitepiecedidcapturelastturn = True
                        
                                                
                                    redraw()
                                    if pieceselected:
                                        highlight(currentmovehighlightpiece.square)
                                        for squaremove in currentmovehighlightpiece.movelist: # iterate through movelist and highlight possible moves
                                            highlight(squaremove)
                                        for squarejump in currentmovehighlightpiece.jumpdict: # iterate through jumpdict and highlight possible jumps
                                            highlight(squarejump)                










menu()



# closing window, quitting game and returning to menu
# for next event while not on menu screen
running = True
while running:
  clock.tick(60) # program will not run faster than 60fps

  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        window.fill(white)
        menu()
    elif event.type == pygame.QUIT:
      running = False
pygame.quit()
