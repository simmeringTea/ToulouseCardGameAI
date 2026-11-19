import random
from enum import Enum
import time
import math

# OG code, always move 1,2,3 to back: 9.6% (1000000 tests)
# AI with first 2 moves, depth 5: 13.36% (10000 tests) (0.003 sec/test)
# AI with first 2 moves, depth 10: 22.27% (10000 tests) (0.03 sec/test)
# AI with first 2 moves, depth 15: 30.47% (10000 tests) (0.3 sec/test)
# AI with first 2 moves, depth 20: 38.1% (1000 tests) (3 sec/test)
# AI with first 2 moves, depth 25: 43.0% % (100 tests) (32 sec/test)

#                                                                   after always moving 1s to back of river
# AI with all 4 moves, depth 1: 3.54% (100000) (0.001 sec/test)      7.66% (100000) (0.001 sec/test)
# AI with all 4 moves, depth 2: 15.99% (100000) (0.002 sec/test)    34.78% (100000) (0.002 sec/test)
# AI with all 4 moves, depth 3: 28.45% (100000) (0.008 sec/test)    61.79% (100000) (0.006 sec/test)
# AI with all 4 moves, depth 4: 44.27% (10000) (0.026 sec/test)     79.98% (100000) (0.020 sec/test)
# AI with all 4 moves, depth 5: 59.97% (10000) (0.093 sec/test)     85.76% (100000) (0.063 sec/test)
# AI with all 4 moves, depth 6: 71.82% (10000) (0.325 sec/test)     86.54% (10000)  (0.217 sec/test)
# AI with all 4 moves, depth 7: 80.22% (10000) (1.154 sec/test)     84.8 % (10000)  (0.751 sec/test)
# AI with all 4 moves, depth 8: 84.8% (1000)  (3.983 sec/test)      80.02% (10000)  (2.499 sec/test)
# AI with all 4 moves, depth 9: 85.9% (1000)   (14.965 sec/test)
#                                                                                       moved loop check to first check
# Same moves, depth 1, after detecting complete loops:  7.74% (100000) (0.001 sec/test)  8.79% (100000) (0.001)
# Same moves, depth 2, after detecting complete loops: 39.82% (100000) (0.002 sec/test) 42.85% (100000) (0.002)
# Same moves, depth 3, after detecting complete loops: 69.74% (100000) (0.005 sec/test) 70.25% (100000) (0.005)
# Same moves, depth 4, after detecting complete loops: 89.47% (10000)  (0.015 sec/test) 88.74% (100000) (0.014)
# Same moves, depth 5, after detecting complete loops: 95.53% (10000)  (0.042 sec/test) 95.64% (100000) (0.042)
# Same moves, depth 6, after detecting complete loops: 98.26% (10000)  (0.139 sec/test) 98.23% (100000) (0.145)
# Same moves, depth 7, after detecting complete loops:                                  98.7 % (10000)  (0.524)
# Same moves, depth 8, after detecting complete loops:                                  98.39% (10000)  (1.889)
#
# No canal, depth 5:  16.69% (100000) (0.002 sec/test)
# No canal, depth 10: 25.79% (10000)  (0.012 sec/test)
# No canal, depth 15: 31.62% (10000)  (0.071 sec/test)
# No canal, depth 20:
#                                                      fixed loops for good and added lose case to heuristic
# Same moves, depth 1, after detecting complete loops:  9.34% (100000) (0.001 sec/test)
# Same moves, depth 2, after detecting complete loops: 44.00% (100000) (0.002 sec/test)
# Same moves, depth 3, after detecting complete loops: 70.91% (100000) (0.005 sec/test)
# Same moves, depth 4, after detecting complete loops: 89.40% (100000) (0.011 sec/test)
# Same moves, depth 5, after detecting complete loops: 96.25% (100000) (0.028 sec/test)
# Same moves, depth 6, after detecting complete loops: 98.83% (100000) (0.070 sec/test)
# Same moves, depth 7, after detecting complete loops: 99.55% (100000) (0.173 sec/test)
# Same moves, depth 8, after detecting complete loops: 99.83% (100000) (0.416 sec/test)
# Same moves, depth 9, after detecting complete loops: 99.97% (20000)  (1.019 sec/test)
# Same moves, depth 10, after detecting complete loops:99.97% (10000)  (2.384 sec/test)
# Same moves, depth 11, after detecting complete loops:100.0% (20000)  (5.789 sec/test)
#
# No canal, depth 5:  16.90% (100000) (0.002 sec/test)
# No canal, depth 10: 25.09% (10000)  (0.011 sec/test)
# No canal, depth 15: 31.40% (10000)  (0.057 sec/test)
# No canal, depth 20: 35.24% (10000)  (0.296 sec/test)
#
# depth 8,  run losses through depth 13: 100% (10000)
# depth 9,  run losses through depth 13: 100% (20000)
# depth 10, run losses through depth 13: 100% (10000)
#
#
# Same moves, depth 3, after removing empty river win condition: 70.53% (100000)
# Same moves, depth 4, after removing empty river win condition: 88.94% (10000)
# Same moves, depth 5, after removing empty river win condition: 96.38% (10000)
# Same moves, depth 6, after removing empty river win condition: 98.92% (10000)
#
# Same moves, depth  1, after enforcing all 4 aces to win:  2.32% (100000)
# Same moves, depth  2, after enforcing all 4 aces to win: 24.89% (100000)
# Same moves, depth  3, after enforcing all 4 aces to win: 51.52% (100000)
# Same moves, depth  4, after enforcing all 4 aces to win: 73.40% (10000)
# Same moves, depth  5, after enforcing all 4 aces to win: 83.85% (10000)
# Same moves, depth  6, after enforcing all 4 aces to win: 90.80% (10000)
# Same moves, depth  7, after enforcing all 4 aces to win: 94.03% (10000)
# Same moves, depth  8, after enforcing all 4 aces to win: 95.91% (10000)
# Same moves, depth  9, after enforcing all 4 aces to win: 97.68% (10000) (2.421 sec/test) (post PC upgrade)
# Same moves, depth 10, after enforcing all 4 aces to win: 97.80% (1000)
masterDeck = []
numTests = 1000
searchDepth = 6
numSuccess = 0

printStuff = False

class Move(Enum):
    NONE = 0,
    RIVER_TO_RIVER = 1
    DECK_TO_RIVER  = 2
    DECK_TO_CANAL  = 3
    CANAL_TO_RIVER = 4

class GameState:

    deck = []
    river = []
    canal = []

    def __init__(self, prevState=0, move=Move.NONE):
        if prevState == 0:
            self.deck = []
            self.river = []
            self.canal = []
            for i in range(13):
                for j in range(4):
                    self.deck.append(i + 1)
            random.shuffle(self.deck)
            self.river = self.deck[:5]
            self.deck = self.deck[5:]
        else:
            self.deck = prevState.deck[:]
            self.river = prevState.river[:]
            self.canal = prevState.canal[:]

            if move == Move.RIVER_TO_RIVER:
                self.riverToRiver()
            elif move == Move.DECK_TO_RIVER:
                self.deckToRiver()
            elif move == Move.DECK_TO_CANAL:
                self.deckToCanal()
            elif move == Move.CANAL_TO_RIVER:
                self.canalToRiver()

        if len(self.river) > 0 and self.river[0] == 1 and self.river.count(1) != len(self.river):
            while self.river[0] == 1:
                self.river.append(1)
                self.river = self.river[1:]

        return

    def __eq__(self, other):
        if isinstance(other, GameState):
            return self.river == other.river and self.canal == other.canal and self.deck == other.deck
        return False

    def __str__(self):
        return "Canal: " + str(self.canal) + "\nRiver: " + str(self.river) + "\nDeck: " + str(self.deck)

    # Only way this is different than before is we only move one to the back, not all consecutive
    # could effect results for the better or worse
    def riverToRiver(self):
        if len(self.river) > 0:
            if self.river[0] == 1 or self.river[0] == 2 or self.river[0] == 3:
                self.river.append(self.river[0])
                self.river = self.river[1:]

        return

    def deckToRiver(self):
        if len(self.river) == 0:
            self.river.append(self.deck[0])
        elif self.deck[0] == self.river[0] and self.deck[0] != 1: # Aces can't cancel out
            if len(self.river) > 1:
                if self.river[1] != 1:
                    self.river = self.river[2:]
                else:
                    cardId = 2
                    while cardId < len(self.river) and self.river[cardId] == 1:
                        cardId += 1
                    if cardId < len(self.river):
                        self.river = self.river[:cardId] + self.river[cardId+1:]
                    self.river = self.river[1:]
            else:
                self.river = []
        elif self.deck[0] < self.river[0]:
            self.river = self.river[1:]
            self.river.append(self.deck[0])
        else:
            self.river.append(self.deck[0])

        self.deck = self.deck[1:]

    def deckToCanal(self):
        self.canal.append(self.deck[0])
        self.deck = self.deck[1:]

    def canalToRiver(self):
        if len(self.river) == 0:
            self.river.append(self.canal[0])
        elif self.canal[0] == self.river[0] and self.canal[0] != 1: # Aces can't cancel out
            if len(self.river) > 1:
                if self.river[1] != 1:
                    self.river = self.river[2:]
                else:
                    cardId = 2
                    while cardId < len(self.river) and self.river[cardId] == 1:
                        cardId += 1
                    if cardId < len(self.river):
                        self.river = self.river[:cardId] + self.river[cardId+1:]
                    self.river = self.river[1:]
            else:
                self.river = []
        elif self.canal[0] < self.river[0]:
            self.river = self.river[1:]
            self.river.append(self.canal[0])
        else:
            self.river.append(self.canal[0])

        self.canal = self.canal[1:]

# TODO: Long term - Change to create node tree with states/heuristic value in each node - enables
#  more optimization and loop detection
class AIAgent:

    maxSearchDepth = 0

    def __init__(self, searchDepth):
        self.maxSearchDepth = searchDepth

        return

    # Higher value is better
    def heuristic(self, gameState):
        result = -1
        if len(gameState.canal) == 0:
            if len(gameState.deck) == 0:  # end of game because we can't remove more cards
                if gameState.river.count(1) < len(gameState.river):  # we lost
                    result = 0
                else:  # we won at the very end
                    result = 101
            elif (len(gameState.river) == 4) and (gameState.river[0] == 1): # length of river used to be > 0
                if gameState.river.count(gameState.river[0]) == len(gameState.river):
                    result = 101  # Winning situation
            #elif len(gameState.river) == 0:
            #    result = 101  # Potential winning situation, include for now since we did before

        if result == -1:
            result = 100 - (len(gameState.river) + len(gameState.canal)) + gameState.river.count(1)  # TODO: Add 1s in canal as well?

        return result

    def stateSearch(self, gameState, depth, prevState=0):
        rating = -1
        nextMove = Move.NONE

        currHeuristic = self.heuristic(gameState)
        if gameState == prevState:  # Got into a loop, return bad heuristic
            rating = -1
        elif depth == self.maxSearchDepth or currHeuristic == 101 or currHeuristic == 0:  # We hit max depth or won
            rating = currHeuristic
        else:
            tempResult = 0
            if len(gameState.deck) > 0:
                tempResult = self.stateSearch(GameState(gameState, Move.DECK_TO_RIVER), depth + 1)
                if tempResult[0] > rating:
                    rating = tempResult[0]
                    nextMove = Move.DECK_TO_RIVER
                tempResult = self.stateSearch(GameState(gameState, Move.DECK_TO_CANAL), depth + 1)
                if tempResult[0] > rating:
                    rating = tempResult[0]
                    nextMove = Move.DECK_TO_CANAL
            if (len(gameState.river) > 0) and (len(gameState.deck) > 0 or len(gameState.canal) > 0) and (gameState.river[0] == 1 or gameState.river[0] == 2 or gameState.river[0] == 3):
                passState = prevState  # Pass on initial game state in river to river chain to detect loops
                if passState == 0:
                    passState = gameState
                tempResult = self.stateSearch(GameState(gameState, Move.RIVER_TO_RIVER), depth + 1, passState)
                if tempResult[0] > rating:
                    rating = tempResult[0]
                    nextMove = Move.RIVER_TO_RIVER
            if len(gameState.canal) > 0:
                tempResult = self.stateSearch(GameState(gameState, Move.CANAL_TO_RIVER), depth + 1)
                if tempResult[0] > rating:
                    rating = tempResult[0]
                    nextMove = Move.CANAL_TO_RIVER
            # ADD ADDITIONAL MOVES HERE
            if nextMove == Move.NONE: # No moves were valid, return value of current state
                rating = self.heuristic(gameState)

        return rating, nextMove

    def simulate(self, game=None, printInfo=False):
        if game == None:
            game = GameState()
        gameWon = False
        gameDone = False
        prevStater2r = 0
        rating, move = 0, Move.NONE

        while not gameDone:
            rating, move = self.stateSearch(game, 0, prevStater2r)

            if rating == 101:
                gameDone = True
                gameWon  = True
            elif rating == 0:
                gameDone = True
            else:
                if printInfo:
                    print(rating)
                    print(move)
                    print(game)
                if move == Move.RIVER_TO_RIVER:
                    if prevStater2r == 0:
                        prevStater2r = game
                    #if len(prevMoves) > 12:
                    #    if prevMoves[-12:].count(Move.RIVER_TO_RIVER) == 12:
                    #        print("Break!")
                    #        for i in prevStates:
                    #            print("_____")
                    #            print(i)
                    #        if len(game.deck) > 0:
                    #            move = Move.DECK_TO_RIVER
                    #        else:
                    #            gameDone = True
                else:
                    prevStater2r = 0

                #prevMoves.append(move)
                game = GameState(game, move)
        if printInfo:
            print("Final State:")
            print(game)
        return gameWon


print("Beginning Simulation...")

def printOut(str):
    if printStuff:
        print(str)


ai = AIAgent(searchDepth)

currTimeSum = 0
startTime = 0

testsHundreth = numTests / 100
nextHundreth = testsHundreth
hundrethsDone = 0
tenthsDone = 0

lostGames = []

for t in range(numTests):
    gameSim = GameState()
    gameCopy = GameState(gameSim)
    startTime = time.time()
    if ai.simulate(gameSim, printStuff) == True:
        numSuccess += 1
        #print("Win!")
    else:
        lostGames.append(gameCopy)
        #print("Loss")
    currTimeSum += (time.time() - startTime)

    if t >= nextHundreth:
        while t >= nextHundreth:
            hundrethsDone += 1
            nextHundreth += testsHundreth
        if hundrethsDone >= tenthsDone + 10:
            while hundrethsDone >= tenthsDone + 10:
                tenthsDone += 10
            print()
            avgTimePerTest = currTimeSum / t
            minutesLeft = (avgTimePerTest * (numTests - t)) / 60
            if minutesLeft > 60:
                expectedRemainingHr = "{:.2f}".format(minutesLeft / 60)
                print(str(tenthsDone) + "% complete, " + expectedRemainingHr + " hours remaining")
            elif minutesLeft < 1:
                expectedRemainingSec = "{:.2f}".format(minutesLeft * 60)
                print(str(tenthsDone) + "% complete, " + expectedRemainingSec + " seconds remaining")
            else:
                expectedRemainingMin = "{:.2f}".format(minutesLeft)
                print(str(tenthsDone) + "% complete, " + expectedRemainingMin + " minutes remaining")
        else:
            print(".", end='')


print()
print("Number of Tests:     ", numTests)
print("Number of Successes: ", numSuccess)
print("Success Rate:        ", (numSuccess/numTests) * 100, "%")
print("Total Time Spent:    " + "{:.2f}".format(currTimeSum/60) + " minutes")
print("Average Test Time:   " + "{:.3f}".format(currTimeSum/numTests) + " seconds")
print()
#print("Lost Games:")
#
#for i in lostGames:
#    print(i)


#deepAI = AIAgent(13)
#newWins = 0
#for i in lostGames:
#    if deepAI.simulate(i) == True:
#        newWins += 1

#print()
#print("Additional Wins from DeepAI: ", newWins)












def old():
    for i in range(13):
        for j in range(4):
            masterDeck.append(i+1)

    for t in range(numTests):
        deck = masterDeck[:]
        random.shuffle(deck)

        hand = deck[:5]
        deck = deck[5:]

        printOut(deck)
        printOut(hand)
        printOut("\n")

        #should eventually change this logic of moving 1, 2, and 3 to back to include option of if next card drawn can
        #match or replace one of them, do that (might need to put rotation logic into draw card logic)
        for i in deck:
            #handle aces, twos, or threes being in the front of the hand
            if len(hand) > 0 and (hand[0] == 1 or hand[0] == 2 or hand[0] == 3):

                loopFrontToBack = False

                if i < 4:
                    j = 0
                    while j < len(hand) and hand[j] < 4:
                        j += 1
                    leadingSmalls = hand[:]
                    if j < len(hand):
                        leadingSmalls = hand[:j]
                    if i in leadingSmalls and i != 1:
                        while hand[0] != i:
                            hand.append(hand[0])
                            hand = hand[1:]
                    elif max(leadingSmalls) > i:
                        if i + 1 in leadingSmalls:
                            while hand[0] != i + 1:
                                hand.append(hand[0])
                                hand = hand[1:]
                        else:
                            while hand[0] != max(leadingSmalls):
                                hand.append(hand[0])
                                hand = hand[1:]
                    else:
                        loopFrontToBack = True
                else:
                    loopFrontToBack = True

                if loopFrontToBack:
                    copy = hand[:]
                    copy.sort(reverse=True)
                    if (copy[0] > 3):
                        while hand[0] == 1 or hand[0] == 2 or hand[0] == 3:
                            hand.append(hand[0])
                            hand = hand[1:]
                    elif (copy[0] == 3):
                        while hand[0] == 1 or hand[0] == 2:
                            hand.append(hand[0])
                            hand = hand[1:]
                    elif (copy[0] == 2):
                        while hand[0] == 1:
                            hand.append(hand[0])
                            hand = hand[1:]
                    else:
                        break
                    printOut(hand)

            printOut(i)
            #"Draw" card and do appropriate action
            if len(hand) == 0:
                hand.append(i)
            elif i == hand[0]:
                if len(hand) > 1:
                    if hand[1] != 1:
                        hand = hand[2:]
                    elif len(hand) == 2:
                        hand = hand[1:]
                    else:
                        cardId = 2
                        while cardId < len(hand) and hand[cardId] == 1:
                            cardId += 1
                        if cardId < len(hand):
                            hand = hand[:cardId] + hand[cardId+1:]
                        hand = hand[1:]
                else:
                    hand = []
            elif i < hand[0]:
                hand = hand[1:]
                hand.append(i)
            else:
                hand.append(i)
            printOut(hand)

        #hand.sort(reverse=True)
        #if len(hand) == 0 or hand[0] == 1:
            #numSuccess += 1