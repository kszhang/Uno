# Uno
# Raiden van Bronkhorst, Bryan Mendes, Kevin Zhang

import random

# Gamestate
class Game:
  names = ["Bryan", "Raiden", "Erik", "Frank"]

  def __init__(self):
    self.pile = []
    self.deck = Deck()

    # botList = ???


    # Start looping at this part for i in botList
    self.players = []
    self.nPlayers = len(self.names)

    for i in range(self.nPlayers):
      self.players.append(Player(self.names[i], i))
    # append a specific bot
    random.shuffle(self.deck.cards)

    # Distribute cards to players
    for n in range(7):
      for i in range(self.nPlayers):
        self.players[i].hand.append(self.deck.pop())
        
    # Starting card 
    self.pile.insert(0, self.deck.pop())
    # Do this a lot to find winrate
    # Game loop
    self.gameloop()

  def recycle(self):
    self.deck.cards = self.pile[0:len(self.pile)-1];
    self.pile = [self.pile[len(self.pile) - 1]]
    # Reset wildcard color
    for i in range(len(self.deck.cards)):
      if (self.deck.cards[i].rank >= 13):
        self.deck.cards[i].color = 'w'
    # Reshuffle
    random.shuffle(self.deck.cards)

  def gameloop(self):    
    won = False
    turn = 0
    direction = 1
    toDraw = 0
    actionPerformed = False
    while (not won):
      if (toDraw):
        # print(self.players[turn].name + " drawing " + str(toDraw))
        for i in range(toDraw):
          self.players[turn].hand.append(self.deck.pop())
          if (len(self.deck.cards) == 0):
            self.recycle() 
            
        turn = (turn + direction) % self.nPlayers
        toDraw = 0
        continue

      # Recycle if needed
      if (len(self.deck.cards) == 0):
        self.recycle()

      lastPlayed = self.pile[len(self.pile) - 1]
      if (lastPlayed.rank > 9 and not actionPerformed):
        if (lastPlayed.rank == 10):
          turn = (turn + direction) % self.nPlayers
        elif (lastPlayed.rank == 11):
          direction = -1 * direction
          turn = (turn + 2 * direction) % self.nPlayers
        elif (lastPlayed.rank == 12):
          toDraw = 2
          turn = (turn + direction) % self.nPlayers
        else:
          toDraw = 4
          turn = (turn + direction) % self.nPlayers
        actionPerformed = True
        continue
        
      # Give other players number of cards
      # set an "if" statement to check if the player is the 5th one to give different paramaters
      decision = self.players[turn].takeTurn(self.legalMoves(self.players[turn].hand), self.players[turn].hand, self.pile, direction, turn, len(self.players[0].hand), len(self.players[1].hand), len(self.players[2].hand), len(self.players[3].hand))
      if (decision < 0):
        # Draw from deck
        self.players[turn].hand.append(self.deck.pop())
      else:
        # Play a card
        if (self.players[turn].hand[decision].color == 'w'):
          # Choose a color
          self.players[turn].hand[decision].color = 'r'

        if (self.players[turn].hand[decision].rank > 9):
          actionPerformed = False

        self.pile.append(self.players[turn].hand[decision])
        self.players[turn].hand.pop(decision)

        lastPlayed = self.pile[len(self.pile) - 1]
        # print(self.players[turn].name + " played " + lastPlayed.color + str(lastPlayed.rank))

        if (not self.players[turn].hand):
          won = True
          print(self.players[turn].name + " Won")

      turn = (turn + direction) % self.nPlayers

  # Return indices in hand which are legal
  def legalMoves(self, hand):
    lastPlayed = self.pile[len(self.pile) - 1]
    legal = []
    for i in range(len(hand)):
      if (hand[i].color == lastPlayed.color or hand[i].rank == lastPlayed.rank or hand[i].color == 'w'):
        legal.append(i)
    return legal
    
# Player
class Player:
  hand = []
  def __init__(self, name, number):
    self.name = name
    self.number = number
    
    #Method for hard coded bot
  def hchoose(self, legalMoves, hand, pile, direction, currplayer, player1, player2, player3, player4):
    if (not pile):
      return -1
    else:
      toMove = legalMoves[0]
      nextPlayer = currplayer + direction
      nextHand = 0
      if (nextPlayer == 0):
        nextHand = player1
      elif (nextPlayer == 1):
        nextHand = player2
      elif (nextPlayer == 2):
        nextHand = player3
      else:
        nextHand = player4
      if nextHand < 4:
        for x in legalMoves:
          if hand[x].rank > 9:
            toMove = x
            return toMove
      else:
        # Counting colors in hand to find a card that can switch to ta better color
        topColor = pile[len(pile) - 1].color
        redCards = 0
        yellowCards = 0
        greenCards = 0
        blueCards = 0
        maxCount = 0
        # If there's nothing but a wildcard, play it
        maxColor = "w"
        for x in hand:
          if x.color == "r":
            redCards += 1
            if redCards > maxCount:
              maxCount = redCards
              maxColor = "r"
          elif x.color == "y":
            yellowCards += 1
            if yellowCards > maxCount:
              maxCount = yellowCards
              maxColor = "y"
          elif x.color == "g":
            greenCards += 1
            if yellowCards > maxCount:
              maxCount = yellowCards
              maxColor = "g"
          elif x.color == "b":
            blueCards += 1
            if blueCards > maxCount:
              maxCount = blueCards
              maxColor = "b"
          else:
            # do nothing
            maxCount = maxCount

        for x in legalMoves:
          if hand[x].color == maxColor:
            toMove = x
            return toMove

        # If there's no number to switch to a better color with....
        
        # do somthing with most frequent color info

      return toMove
      # return legalMoves[0]

  # Returns -1 for draw, >= 0 index in hand to play
  def takeTurn(self, legalMoves, hand, pile, direction, currplayer, player1, player2, player3, player4):
    if (not legalMoves):
      return -1
    else:
      # Make decision
      answer = self.hchoose(legalMoves, hand, pile, direction, currplayer, player1, player2, player3, player4)
      return answer
  

class Bot(Player):
  def __init__(self, name, number, CNA):
    Player.__init__(self, name, number)
    self.CarValues = CNA
    self.winRate


  def takeTurn(self, legalMoves):
    return legalMoves[0]

class Population:
  def __init__():
    self.botList = []

# Card
class Card:
  def __init__(self, color, rank):
    # rank 0-9, 10:skip, 11:reverse, 12:+2, 13:w, 14:w+4
    # color: r, y, g, b, w
    self.color = color
    self.rank = rank

# Deck
class Deck:
  cards = []
  def __init__(self):
    for color in ['r', 'y', 'g', 'b']:
      for rank in range(1, 13): # 1-9, 10, 11, 12
        self.cards.append(Card(color, rank))
        self.cards.append(Card(color, rank))
      self.cards.append(Card(color, 0))
      self.cards.append(Card('w', 13))
      self.cards.append(Card('w', 14))

  def pop(self):
    return self.cards.pop()
    
if __name__ == "__main__":
  # add command line stuff into here
  Game()
