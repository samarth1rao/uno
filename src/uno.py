# Uno

import random
from pyfiglet import Figlet

def buildDeck():
    colours = ["Red", "Green", "Blue", "Yellow"]
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    actions = ["Skip", "Reverse", "Draw2"] * 2   
    wilds = ["Wild", "Wild", "Wild", "Wild", "draw4", "draw4", "draw4", "draw4"]
    
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
        self.currentPlayer = 0  

        self.direction=1
        self.drawPile = 0

        for i in range(7):
            for player in self.players:
                self.players[player].append(self.deck.pop())

        while True:
            openCard = self.deck.pop()
            if openCard[1] not in ["Wild", "draw4"]:  
                self.discardPile.append(openCard)
                self.currentColour = openCard[0]
                break
            else:
                self.deck.insert(0, openCard)

    def drawCard(self, player):
        if not self.deck:
            self.reshuffle() 
        card = self.deck.pop()
        self.players[player].append(card)
        return card
    
    def reshuffle(self):
        if len(self.discardPile) > 1:
            openCard = self.discardPile[-1]
            self.deck = self.discardPile[:-1]
            random.shuffle(self.deck)
            self.discardPile = [openCard]

    def isValid(self, card, player):
        vcolour = self.currentColour if self.currentColour else self.discardPile[-1][0]
        nColour, nNumber = card
        return nColour == vcolour or nNumber == self.discardPile[-1][1] or nColour == "Wild"

    def playCard(self, card, player, wildColour=None):
        if card not in self.players[player]:
            return False
        if not self.isValid(card, player):
            return False
        
        self.players[player].remove(card)
        self.discardPile.append(card)

        if card[1] == "Skip":
            self.currentPlayer = (self.currentPlayer + self.direction) % len(self.players)
            self.currentPlayer = (self.currentPlayer + self.direction) % len(self.players)
        elif card[1] == "Reverse":
            self.direction = -1 * self.direction
        elif card[1] == "Draw2":
            self.drawPile += 2
        elif card[1] == "draw4":
            self.drawPile += 4
            if wildColour:
                self.currentColour = wildColour
        elif card[1] == "Wild":
            if wildColour:
                self.currentColour = wildColour
        else:
            self.currentColour = None

        if card[1] not in ["Draw2", "draw4"] and card[1] != "Skip":
            self.currentPlayer = (self.currentPlayer + self.direction) % len(self.players)
        return True

class UnoCLI:
    def __init__(self, numPlayers):
        self.game = UnoGame(numPlayers)

    def gameStart(self):
        while True:
            players = list(self.game.players.keys())
            current_player = players[self.game.currentPlayer]
            print(f"\n{current_player}'s turn")
            print("Top Card: ", self.game.discardPile[-1])
            print("Your Hand: ", self.game.players[current_player])

            cmd = input("> ").strip().lower()
            turnEnded = False
            
            if cmd == "uno hand":
                print("Your Hand: ", self.game.players[current_player])

            elif cmd == "uno draw":
                card = self.game.drawCard(current_player)
                print("You drew: ", card)
                print("Your Hand: ", self.game.players[current_player])
                if any(self.game.isValid(c, current_player) for c in self.game.players[current_player]):
                    print("You must play a card if possible")
                else:
                    turnEnded = True

            elif cmd.startswith("uno play"):
                parts = cmd.split()
                if len(parts) < 3:
                    print("Invalid command format")
                    continue
                    
                cardString = parts[2]
                wildColour = None
                card = None

                if "wild" in cardString.lower():
                    wildColour = input("Choose color (Red/Green/Blue/Yellow): ").capitalize()
                    if "draw4" in cardString.lower():
                        card = ("Wild", "draw4")
                    else:
                        card = ("Wild", "Wild")
                else:
                    for i in range(1, len(cardString)):
                        if cardString[i].isalpha() and cardString[i].isupper():
                            continue
                        if cardString[i].isdigit() or cardString[i:].lower() in ["skip", "reverse", "draw2"]:
                            colour = cardString[:i].capitalize()
                            value = cardString[i:].capitalize()
                            card = (colour, value)
                            break
                    else:
                        print("Could not parse card properly. Try again.")
                        continue

                if card and self.game.playCard(card, current_player, wildColour):
                    print(f"Played {card}")
                    turnEnded = True
                else:
                    print("Invalid move")

cli = UnoCLI(5)
cli.gameStart()