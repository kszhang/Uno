# Uno
# Raiden van Bronkhorst, Bryan Mendes, Kevin Zhang

import random

# Gamestate
class Game:
  names = ["Bryan", "Raiden", "Erik", "Frank"]

  def __init__(self):
    self.pile = []
    self.deck = Deck()
    self.players = []
    self.nPlayers = len(self.names)

    for i in range(self.nPlayers):
      self.players.append(Player(self.names[i], i))

    random.shuffle(self.deck.cards)

    # Distribute cards to players
    for n in range(7):
      for i in range(self.nPlayers):
        self.players[i].hand.append(self.deck.pop())
        
    # Starting card 
    self.pile.insert(0, self.deck.pop())

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
        print(self.players[turn].name + " drawing " + str(toDraw))
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
        
      decision = self.players[turn].takeTurn(self.legalMoves(self.players[turn].hand))
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
        print(self.players[turn].name + " played " + lastPlayed.color + str(lastPlayed.rank))

        if (not self.players[turn].hand):
          won = True

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
    
  # Returns -1 for draw, >= 0 index in hand to play
  def takeTurn(self, legalMoves):
    if (not legalMoves):
      return -1
    else:
      # Make decision
      return legalMoves[0]
  
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
  Game()
