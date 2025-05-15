# Uno

import random
from pyfiglet import Figlet

def buildDeck():
    colours = ["Red", "Green", "Blue", "Yellow"]
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    actions = ["Skip", "Reverse", "Draw2"] * 2   
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
        self.currentPlayer = 0  

        self.direction=1
        self.drawPile = 0

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

    def drawCard(self, player):
        if not self.deck:
            self.reshuffle() 
        card = self.deck.pop()
        self.players[player].append(card)
        return card
    
    def reshuffle(self):
        if len(self.discardPile) > 1:  # not working w/o, idk why
            openCard = self.discardPile[-1]
            self.deck = self.discardPile[:-1]
            random.shuffle(self.deck)
            self.discardPile = [openCard]

    def isValid(self, card, player):
        colour = self.currentColour if self.currentColour else self.discardPile[-1][0]
        nColour, nNumber = card
        return nColour == colour or nNumber == self.discardPile[-1][1] or nColour == "Wild"

    def playCard(self, card, player, wildColour=None):
        if card not in self.players[player]:
            return False
        if not self.isValid(card, player):
            return False
        
        self.players[player].remove(card)
        self.discardPile.append(card)

        if card[1] == "Skip":
            self.currentPlayer = (self.currentPlayer + self.direction) % len(self.players)
        elif card[1] == "Reverse":
            self.direction = -1 * self.direction
        elif card[1] == "Draw2":
            self.drawPile += 2
        elif card[1] == "WildDraw4":
            self.drawPile += 4
            if wildColour:
                self.currentColour = wildColour
        elif card[1] == "Wild":
            if wildColour:
                self.currentColour = wildColour

        if card[1] not in ["Draw2", "WildDraw4"]:
            self.currentPlayer = (self.currentPlayer + self.direction) % len(self.players)
        return True

class UnoCLI:
    def __init__(self, numPlayers):
        self.game = UnoGame(numPlayers)
        self.currentPlayer = "Player 1"

    def gameStart(self):
        while True:
            print(f"\n{self.currentPlayer}'s turn")
            print("Top Card: ", self.game.discardPile[-1])
            print("Your Hand: ", self.game.players[self.currentPlayer])

            cmd = input("> ").strip().lower()
            turnEnded = False
            
            if cmd == "uno hand":
                print("Your Hand: ", self.game.players[self.currentPlayer])

            elif cmd == "uno draw":
                card = self.game.drawCard(self.currentPlayer)
                print("You drew: ", card)
                print("Your Hand: ", self.game.players[self.currentPlayer])
                if any(self.game.isValid(c, self.currentPlayer) for c in self.game.players[self.currentPlayer]):
                    print("You must play a card if possible")
                else:
                    turnEnded = True
                    
            elif cmd == "uno help":
                italic = Figlet(font='slant')
                print("To see the top card, type ", italic.renderText('uno top card'))
                print("To see your hand, type ", italic.renderText('uno hand'))
                print("You are supposed to discard a card from your current hand, onto the discard pile.")
                print("This card must either have the same colour or number as the top card")
                print("To play a card, type ", italic.renderText('uno play red7'), " or ", italic.renderText('uno play WildDraw4'), " or the such.")
                print("If you do not have a matching card, you must draw a card from the deck. Type ", italic.renderText('uno draw'))
            
            elif cmd.startswith("uno play"):
                parts = cmd.split()
                if len(parts) < 3:
                    italic = Figlet(font='slant')
                    print("Invalid command format, must be like ", italic.renderText('uno play red7'))
                    continue
                    
                cardString = parts[2]
                wildColour = None
                if "wild" in cardString.lower():
                    wildColour = input("Choose color (Red/Green/Blue/Yellow): ").capitalize()
                    cardString = "Wild"
                    
                colour = cardString[:-1].capitalize()
                number = cardString[-1:].upper()
                card = (colour, number)
                
                if self.game.playCard(card, self.currentPlayer, wildColour):
                    print(f"Played {card}")
                    turnEnded = True
                else:
                    print("Invalid move")
            
            else:
                print("UNKNOWN COMMAND")
                italic = Figlet(font='slant')
                print("To see the top card, type ", italic.renderText('uno top card'))
                print("To see your hand, type ", italic.renderText('uno hand'))
                print("To play a card, type ", italic.renderText('uno play red7'), " or ", italic.renderText('uno play WildDraw4'), " or the such.")
                print("If you do not have a matching card, you must draw a card from the deck. Type ", italic.renderText('uno draw'))
                print("For more help type", italic.renderText('uno help'))

            if turnEnded == True:
                nextPlayer = (int(self.currentPlayer[-1]) % len(self.game.players)) + 1
                self.currentPlayer = f"Player {nextPlayer}"

cli = UnoCLI(2)
cli.gameStart()