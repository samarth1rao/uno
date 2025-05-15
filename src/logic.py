# Uno Logic

import random

def buildDeck():
    colours = ["Red", "Green", "Blue", "Yellow"]
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    actions = ["Skip", "Reverse", "Draw2", "Skip", "Reverse", "Draw2"]   
    wilds = ["Wild", "Wild", "Wild", "Wild", "WildDraw4", "WildDraw4", "WildDraw4", "WildDraw4"]
    
    deck = []
    for colour in colours:
        for num in numbers:
            deck.append((colour, str(num)))
        for action in actions:
            deck.append((colour, action))
    for wild in wilds:
        deck.append(("Wild", wild))
    return deck

class UnoGame:
    def __init__(self, numPlayers):
        self.deck = buildDeck()
        random.shuffle(self.deck)

        self.discardPile = []
        self.currentColour = None
        self.players={}
        for i in range(numPlayers):
            name=f"Player {i+1}"
            self.players[name]=[]
        self.current = 0

        self.direction=1

        self.draw_pile = 0

        for i in range(7):
            for player in self.players:
                self.players[player].append(self.deck.pop())

        while True:
            openCard = self.deck.pop()
            if openCard[1] not in ["Wild", "WildDraw4"]:
                self.discardPile.append(openCard)
                self.currentColour = openCard[0]
                break
            else:
                self.deck.insert(0, openCard)

    def draw_card(self, player):
        if not self.deck:
            self.reshuffle() 
        card = self.deck.pop()
        self.players[player].append(card)
        return card
    
    def reshuffle(self):
        openCard = self.discardPile[-1]
        self.deck = self.discardPile[:-1]
        random.shuffle(self.deck)
        self.discardPile = [openCard]

    def isValid(self, card, player):
        openColour, openNumber  = self.discardPile[-1]
        nColour, nNumber = card
        if nColour == openColour or nNumber == openNumber or nColour == "Wild":
            return True
        else:
            return False
        
    def throwCard(self, card, player, wildColour=None):
        if card not in self.players[player]:
            return False
        if not self.isValid(card, player):
            return False
        
        self.players[player].remove(card)
        self.discardPile.append(card)

        if card[1] == "Skip":
            self.current = (self.current + self.direction) % len(self.players)
        elif card[1] == "Reverse":
            self.direction = (-1)*self.direction
        elif card[1] == "Draw2":
            self.draw_pile += 2
        elif card[1] == "WildDraw4":
            self.draw_pile += 4
            if wildColour:
                self.currentColour = wildColour
        elif card[1] == "Wild":
            if wildColour:
                self.currentColour = wildColour

        if card[1] not in ["Draw2", "WildDraw4"]:
            self.current = (self.current + self.direction) % len(self.players)
        return True
    

# Test script

game = UnoGame(2)
print("Top card:", game.discardPile[-1])
print("Player 1 hand:", game.players["Player 1"])

# Simulate a move
player = "Player 1"
card = game.players[player][0]
if game.isValid(card, player):
    game.throwCard(card, player)
    print(f"{player} played {card}")
    print("New top card:", game.discardPile[-1])