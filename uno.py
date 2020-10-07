# Uno
# Raiden van Bronkhorst, Bryan Mendes, Kevin Zhang

import random
import thread
from collections import Counter

# Gamestate
class Game:
  names = ["Bryan", "Raiden", "Alan"]

  def __init__(self, popOfBots):
    self.Population = popOfBots
    self.avgTotal = 0
    for x in range(1,100):
      print("Playing Generation: " + str(x))
      self.playGame()
      # self.Population.replicateFittest()
      self.Population.CrossSelection()
      self.Population.mutatePop(0.1)

  def playGame(self):
    self.avgTotal = 0
    for k in self.Population.botList:
      # Thread everything under here
      self.BotThread(k)
      # Sync this part
      self.avgTotal += k.wins
      # print(k.name + ' won ' + str(k.wins) + ' out of 100')
    self.avgTotal = self.avgTotal / len(self.Population.botList)
    print(str(self.avgTotal) + "% win average")

  
  def BotThread(self, Bot):
    players = []
    nPlayers = len(self.names)

    # do hard coded bots
    for i in range(nPlayers):
      players.append(Player(self.names[i], i))

    # add the Learning Bot
    players.append(Bot)
    nPlayers = len(players)
    # Now loop the game.
    for j in range(1,100):
      pile = []
      deck = Deck()
      random.shuffle(deck.cards)

      # Clear player hands
      for i in range(nPlayers):
        players[i].hand = []

      # Distribute cards to players
      for n in range(7):
        for i in range(nPlayers):
          players[i].hand.append(deck.pop())
            
      # Starting card 
      pile.insert(0, deck.pop())
      # Do this a lot to find winrate
      # Game loop
      winner = self.gameloop(players, pile, deck, nPlayers)
      if winner == Bot.name:
        Bot.wins += 1
    print(Bot.name + ' won ' + str(Bot.wins) + ' out of 100')


  def recycle(self, pile, deck):
    outPut = [[]]
    deck.cards = pile[0:len(pile)-1];
    pile1 = [pile[len(pile) - 1]]
    # Reset wildcard color
    for i in range(len(deck.cards)):
      if (deck.cards[i].rank >= 13):
        deck.cards[i].color = 'w'
    # Reshuffle
    random.shuffle(deck.cards)
    outPut.append(deck)
    outPut.append(pile1)
    return outPut

  def gameloop(self, players, pile, deck, nPlayers):    
    # Need a placeholder for recycling pile
    newDeck = [[]]
    won = False
    turn = 0
    direction = 1
    toDraw = 0
    actionPerformed = False
    while (not won):
      if (toDraw):
        # print(self.players[turn].name + " drawing " + str(toDraw))
        for i in range(toDraw):
          if (len(deck.cards) == 0):
            newDeck = self.recycle(pile, deck)
            deck = newDeck[0]
            pile = newDeck[1]
          players[turn].hand.append(deck.pop())
            
        turn = (turn + direction) % nPlayers
        toDraw = 0
        continue

      # Recycle if needed
      if (len(deck.cards) == 0):
        newDeck = self.recycle(pile, deck)
        deck = newDeck[0]
        pile = newDeck[1]

      lastPlayed = pile[len(pile) - 1]
      if (lastPlayed.rank > 9 and not actionPerformed):
        if (lastPlayed.rank == 10):
          turn = (turn + direction) % nPlayers
        elif (lastPlayed.rank == 11):
          direction = -1 * direction
          turn = (turn + 2 * direction) % nPlayers
        elif (lastPlayed.rank == 12):
          toDraw = 2
          turn = (turn + direction) % nPlayers
        else:
          toDraw = 4
          turn = (turn + direction) % nPlayers
        actionPerformed = True
        continue
        
      # Give other players number of cards
      # set an "if" statement to check if the player is the 5th one to give different paramaters
      decision = 0
      if turn == 3:
        decision = players[turn].takeTurn(self.legalMoves(players[turn].hand, pile))
      else:
        decision = players[turn].takeTurn(self.legalMoves(players[turn].hand, pile), players[turn].hand, pile, direction, turn, len(players[0].hand), len(players[1].hand), len(players[2].hand), len(players[3].hand))
      if (decision < 0):
        # Draw from deck
        players[turn].hand.append(deck.pop())
      else:
        # Play a card
        if (players[turn].hand[decision].color == 'w'):
          # Choose a color
          players[turn].hand[decision].color = 'r'

        if (players[turn].hand[decision].rank > 9):
          actionPerformed = False

        pile.append(players[turn].hand[decision])
        players[turn].hand.pop(decision)

        lastPlayed = pile[len(pile) - 1]
        # print(self.players[turn].name + " played " + lastPlayed.color + str(lastPlayed.rank))

        if (not players[turn].hand):
          won = True
          # print(self.players[turn].name + " Won")
          return players[turn].name

      turn = (turn + direction) % nPlayers

  # Return indices in hand which are legal
  def legalMoves(self, hand, pile):
    lastPlayed = pile[len(pile) - 1]
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
    # find fittest
    numToLive = int(len(self.botList)/5)
    TopDogs = []
    for x in range(1,numToLive):
      topWin = self.botList[0]
      for i in self.botList:
        if topWin.wins < i.wins:
          topWin = i
      TopDogs.append(i)
      self.botList.remove(i)
    # duplicate
    numToDupe = int(len(self.botList)/numToLive)
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
      
  def CrossSelection(self):
    # Do similar stratagy w/ choosing card, put down however many indexs equal to their number of wins and choose a random point a certin number of times
    Max = len(self.botList)
    indexPool = []
    newPop = []
    for x in range(0,Max):
      for y in range(0,self.botList[x].wins):
        indexPool.append(x)
    # Choose a certin number of bots, make sure it's even
    numBreeding = (int(len(self.botList)/5))*2
    # numBreeding = 4
    # How many children should each pair, and how to pair? just every 2? it would have to be even
    numToDupe = int(len(self.botList)/(numBreeding/2))
    # numToDupe = 5
    # choose bots randomly, take a index and referance it for the next round
    survivors = []
    for x in range(0,numBreeding):
      pointOfTake = random.randrange(len(indexPool))
      survivors.append(indexPool[pointOfTake])

    currId = 1
    for x in range(0,numBreeding, 2):
      # do a repeat to choose? pretty slow... maybe a random # compared to percentage
      # win1/win1+win2 put into percentage 0->1, if over choose other
      parent1 = self.botList[survivors[x]]
      parent2 = self.botList[survivors[x+1]]
      percent = parent1.wins / (parent1.wins + parent2.wins)
      # Go through every weight
      for y in range(0,numToDupe):
        # New weight
        WeightsToBe = Counter()
        for z in parent1.Weights:
          choice = random.random()
          if random < percent:
            WeightsToBe[z] = parent1.Weights[z]
          else:
            WeightsToBe[z] = parent2.Weights[z]
        # new Name
        newbot = "Kevin-Jr-" + str(currId)
        newRep = Bot(newbot, 3, WeightsToBe)
        if parent1 == parent2:
          newRep.mutate()
        newPop.append(newRep)
        currId += 1
    # Set botlist to new Population
    self.botList = newPop

  def mutatePop(self, Frac):
    for x in self.botList:
      shouldMutate = random.random()
      if shouldMutate < Frac:
        x.mutate()
    

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
  for x in range(1,101):
    botName = "Kevin-Jr-" + str(x)
    DNA = []
    initPop.append(Bot(botName, 3, DNA))

  botPop = Population(initPop)
  Game(botPop)
