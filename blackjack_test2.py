# from blackjackpack import card
# from deck import Deck
# from card import Card
# from hand import Hand
# from chips import Chips
# from end_of_game import player_busts
# from end_of_game import player_wins
# from end_of_game import dealer_busts
# from end_of_game import dealer_wins
# from end_of_game import push

# import take_bet
# import show_cards
# import hit_or_stand
# import hit


import random
# from card import Card

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

# deck object used to deal cards and shuffle the deck


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.deck.append(card)

    def __str__(self):
        deck_string = ''
        for i in self.deck:
            deck_string = deck_string + ', ' + str(i)
        return deck_string

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):  # dealing the last card from deck
        return self.deck.pop()

# hand object used to evaluate cards and adjust the value in case there is an ace


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
        # self.adjusted_value = 0

    def add_card(self, card):
        self.cards.append(card.rank + ' of ' + card.suit)
        self.value = self.value + values[card.rank]
        if card.rank == "Ace":
            self.aces = self.aces + 1

    def adjust_for_ace(self):
        # case1: ace gets value of one if total unadjusted value is >21; the rest of cards get left untouched
        if self.value > 21 and self.aces >= 1:
            non_ace_card_value = self.value - (11 * self.aces)
            if non_ace_card_value == 0:
                adjusted_value = 11 + 1 * (self.aces - 1)
                return adjusted_value
            difference = 21 - non_ace_card_value
            ratio = difference / 11
            if self.aces > ratio:
                adjusted_value = self.value - self.aces * 10
        else:
            adjusted_value = self.value
        return adjusted_value

# chips class used to calculate resulting chip balance


class Chips:

    def __init__(self, total, bet):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = bet

    def win_bet(self):
        self.total = self.total + self.bet*2

    def lose_bet(self):
        self.total = self.total - self.bet

# card class used to create name of a card based on suit and rank


class Card:

    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

# evaluating win/lose scenarios and generating an end of the game


def player_busts(player, dealer, chips):
    print(f"\nPlayer's Hand Value: {player.adjust_for_ace()} Player Busts!")
    chips.lose_bet()
    print(f"Remaining chips value: {chips.total}")


def player_wins(player, chips):
    print(f"\nPlayer's Hand Value: {player.adjust_for_ace()} Player Wins!")
    chips.win_bet()
    print(f"Remaining chips value: {chips.total}")


def dealer_busts(dealer, chips):
    print(f"\nDealer's Hand Value: {dealer.adjust_for_ace()} Dealer Busts!")
    chips.win_bet()
    print(f"Remaining chips value: {chips.total}")


def dealer_wins(dealer, chips):
    print(f"\nDealer's Hand Value: {dealer.adjust_for_ace()} Dealer Wins!")
    chips.lose_bet()
    print(f"Remaining chips value: {chips.total}")


def push(player, dealer, chips):
    print(f"\nDealer's Hand Value: {dealer.adjust_for_ace()} .")
    print(f"Player's Hand Value: {player.adjust_for_ace()} .")
    print(f"Nobody wins!")
    print(f"Remaining chips value: {chips.total}")


# function used to receive bids which dont exceed chip value
def take_bet():

    while True:
        try:
            bet = int(input("Please enter in a bid. "))
            current_chips = Chips(total, bet)
            if bet > current_chips.total:
                print("Not enough chips for this bid! Try again.", bet)
                continue
            elif bet < 0:
                print("Not a valid bid value, try again", bet)
                continue
        except ValueError:
            print("Not a number, try again.")
            continue
        else:
            print("Thank you")
            break
    return bet

# show all of player's cards and some of dealer's cards


def show_some(player, dealer):
    print("\nDealer's Cards:")
    print("<First card is hidden.>")
    print(dealer.cards[1])
    print("\nPlayer's Cards:")
    print(player.cards)
    # print(f"Value: {player.value}")
    print(f"Value: {player.adjust_for_ace()}")

# show both dealers and players cards


def show_all(player, dealer):
    print("\nDealer's Cards:")
    print(dealer.cards)
    # print(f"Value: {dealer.value}")
    print(f"Value: {dealer.adjust_for_ace()}")
    print("\nPlayer's Cards:")
    print(player.cards)
    # print(f"Value: {player.value}")
    print(f"Value: {player.adjust_for_ace()}")

# function used to either add more cards to the player's hand or not


def hit_or_stand(deck, hand):
    global playing

    while True and hand.value < 21:
        choice = input("Would you like to Hit or Stand? ")

        if choice.lower() == "hit":
            # to control an upcoming while loop
            hit(deck, hand)
            break

        elif choice.lower() == "stand":
            playing = False
            break

        else:
            print("Please try again.")
            continue

# function used to add card from the deck and into the hand


def hit(deck, hand):

    # dealing one card off the deck
    dealt_card = deck.deal()

    # adding it to the hand
    hand.add_card(dealt_card)

    if hand.aces > 0:
        hand.adjust_for_ace()

# game


playing = True
total = 100

while True:
    print("\nWelcome to the Game of Black Jack! \n")
    deck = Deck()
    dealer = Hand()
    player = Hand()

    deck.shuffle()
    dealer.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    player.add_card(deck.deal())

    # Prompt the Player for their bet
    print(f"Remaining chips: {total}")
    bet = take_bet()

    # Set up the Player's chips
    chips = Chips(total, bet)

    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)

    while playing:  # recall this variable from our hit_or_stand function
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player)

        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)

        # If player's hand exceeds 21, run player_busts() and break out of loop

        if player.adjust_for_ace() > 21:
            player_busts(player, dealer, chips)
            break
       # playing = False

        elif player.adjust_for_ace() == 21:
            player_wins(player, chips)
            break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        elif player.adjust_for_ace() < 21:
            while dealer.adjust_for_ace() <= 17:
                hit(deck, dealer)
                print("<Dealer gets one more card>")

                # Show all cards
                show_all(player, dealer)

                # Run different winning scenarios
                # Inform Player of their chips total

                if dealer.adjust_for_ace() < 21 and dealer.adjust_for_ace() > 17:
                    if dealer.adjust_for_ace() > player.adjust_for_ace():
                        dealer_wins(dealer, chips)
                        break
                    elif dealer.adjust_for_ace() < player.adjust_for_ace():
                        player_wins(player, chips)
                        break
                    else:
                        push(player, dealer, chips)
                        break
                    break
                elif dealer.adjust_for_ace() > 21:
                    dealer_busts(dealer, chips)
                    break
                elif dealer.adjust_for_ace() == 21:
                    dealer_wins(dealer, chips)
                    break
                continue
        elif player.adjust_for_ace() < 21 and dealer.adjust_for_ace() > 17:
            if dealer.adjust_for_ace() > player.adjust_for_ace():
                dealer_wins(dealer, chips)
                break
            elif dealer.adjust_for_ace() < player.adjust_for_ace():
                player_wins(player, chips)
                break
            elif push(player, dealer, chips):
                print("Nobody wins!")
                break
            else:
                print("Scenario you did not catch!")

        else:
            print("Scenario you did not catch!")
        break

    if chips.total == 0:
        print("\nNo more chips! Game Over")
        break
    else:
        # Ask to play again
        print("Dealer Value was: ", dealer.adjust_for_ace())
        play_again = input("\nWould you like to play again?: Yes/No ")
        if play_again.lower() == 'yes':
            playing = True
            total = chips.total
            continue
        elif play_again.lower() == 'no':
            playing = False
            break
        else:
            print("Please try again.")
            continue
        break
