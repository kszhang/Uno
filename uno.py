# Uno
# Raiden van Bronkhorst, Bryan Mendes, Kevin Zhang

import random
import thread
from collections import Counter

# Gamestate
class Game:
  names = ["Bryan", "Raiden", "Alan"]

  def __init__(self, popOfBots):
    self.pile = []
    self.deck = Deck()
    self.Population = popOfBots
    for x in range(1,10):
      print("Playing Generation: " + str(x))
      self.playGame()
      self.Population.replicateFittest()

  def playGame(self):
    avgTotal = 0
    for k in self.Population.botList:
      k.wins = 0
      # Start looping at this part for i in botList
      self.players = []
      self.nPlayers = len(self.names)

      # do hard coded bots
      for i in range(self.nPlayers):
        self.players.append(Player(self.names[i], i))

      # add the Learning Bot
      self.players.append(k)
      self.nPlayers = len(self.players)
      # Now loop the game.
      for j in range(1,100):
        self.pile = []
        self.deck = Deck()
        random.shuffle(self.deck.cards)

        # Clear player hands
        for i in range(self.nPlayers):
          self.players[i].hand = []

        # Distribute cards to players
        for n in range(7):
          for i in range(self.nPlayers):
            self.players[i].hand.append(self.deck.pop())
            
        # Starting card 
        self.pile.insert(0, self.deck.pop())
        # Do this a lot to find winrate
        # Game loop
        winner = self.gameloop()
        if winner == k.name:
          k.wins += 1
      avgTotal += k.wins
      print(k.name + ' won ' + str(k.wins) + ' out of 100')
    avgTotal = avgTotal / len(self.Population.botList)
    print(str(avgTotal) + "% win average")



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
      decision = 0
      if turn == 3:
        decision = self.players[turn].takeTurn(self.legalMoves(self.players[turn].hand))
      else:
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
          # print(self.players[turn].name + " Won")
          return self.players[turn].name

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

      top = pile[len(pile) - 1]
      if top.rank == 12 or top.rank == 14:
        for x in legalMoves:
          if hand[x].rank == 12 and hand[x].rank == 14:
            toMove = x
            return toMove
      
      elif nextHand < 3:
        for x in legalMoves:
          if hand[x].rank > 9:
            toMove = x
            return toMove
      
      else:
        # Counting colors in hand to find a card that can switch to ta better color
        topColor = top.color
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
  hand = []
  def __init__(self, name, number, CNA):
    Player.__init__(self, name, number)
    self.Weights = Counter()
    self.CardValues = CNA
    self.wins = 0
    for color in ['r', 'y', 'g', 'b']:
      for rank in range(0, 13): # 1-9, 10, 11, 12
        insert = color + str(rank);
        self.Weights[insert] += 1
    self.Weights["w13"] += 1
    self.Weights["w14"] += 1

  def takeTurn(self, legalMoves):
    if (not legalMoves):
      return -1
    else:
      poolChoose = []
      juryRig = 0
      for i in legalMoves:
        toTrack = self.hand[i].color + str(self.hand[i].rank)
        numTrack = self.Weights[toTrack]
        for x in range(0,numTrack):
          poolChoose.append(juryRig)
        juryRig += 1

      choicePlace = random.randrange(len(poolChoose))
      choice = poolChoose[choicePlace]
      return legalMoves[choice]

  def mutate(self):
    mutMax = 5
    mutMin = 1
    mutChan = 0.2
    for i in self.Weights:
      toBe = random.random()
      if toBe < mutChan:
        toBy = random.randrange(mutMin, mutMax)
        self.Weights[i] += toBy

class Population:
  Generations = 0
  def __init__(self, bots):
    self.botList = bots
    for x in self.botList:
      x.mutate()

  def replicateFittest(self):
    numToLive = int(len(self.botList)/10) + 1
    TopDogs = []
    for x in range(1,3):
      topWin = self.botList[0]
      for i in self.botList:
        if topWin.wins < i.wins:
          topWin = i
      TopDogs.append(i)
      self.botList.remove(i)
    numToDupe = int(len(self.botList)/numToLive) + 1
    self.botList = []
    numName = 1
    for i in TopDogs:
      i.wins = 0
      for x in range(0,numToDupe):
        newbot = "Kevin-Jr-" + str(numName)
        newRep = Bot(newbot, 3, i.CardValues)
        newRep.mutate()
        self.botList.append(newRep)
        numName += 1
      

    

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
  initPop = []
  for x in range(1,11):
    botName = "Kevin-Jr-" + str(x)
    DNA = []
    initPop.append(Bot(botName, 3, DNA))

  botPop = Population(initPop)
  Game(botPop)
