
import random

# these lists are used to construct the deck

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

# deck object used to deal cards and shuffle the deck


class Deck:

    def __init__(self):
        self.deck = []
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

# card object used to create card names using rank and suit


class Card:

    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

# Hand object is used to accumulate cards, keep track of aces and adjust hand value for aces


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card.rank + ' of ' + card.suit)
        if card.rank != "Ace":
            self.value = self.value + card.value
            return self.value
        elif card.rank == "Ace":
            self.aces = self.aces + 1
            if (21 - self.value) >= 11:
                self.value = self.value + 11
                return self.value
            elif (21 - self.value) < 11:
                self.value = self.value + 1
                return self.value

# chips class used to calculate resulting chip balance in case of a win or a loss


class Chips:

    def __init__(self, total, bet):
        self.total = total
        self.bet = bet

    def win_bet(self):
        self.total = self.total + self.bet*2

    def lose_bet(self):
        self.total = self.total - self.bet

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

# evaluating win/lose scenarios at the end of the game


def player_busts(player, dealer, chips):
    print(f"\nPlayer's Hand Value: {player.value} Player Busts!")
    chips.lose_bet()
    print(f"Remaining chips value: {chips.total}")


def player_wins(player, chips):
    print(f"\nPlayer's Hand Value: {player.value} Player Wins!")
    chips.win_bet()
    print(f"Remaining chips value: {chips.total}")


def dealer_busts(dealer, chips):
    print(f"\nDealer's Hand Value: {dealer.value} Dealer Busts!")
    chips.win_bet()
    print(f"Remaining chips value: {chips.total}")


def dealer_wins(dealer, chips):
    print(f"\nDealer's Hand Value: {dealer.value} Dealer Wins!")
    chips.lose_bet()
    print(f"Remaining chips value: {chips.total}")


def push(player, dealer, chips):
    print(f"\nDealer's Hand Value: {dealer.value}.")
    print(f"Player's Hand Value: {player.value}.")
    print(f"Nobody wins!")
    print(f"Remaining chips value: {chips.total}")


# function requesting player input to either get one more card from the deck ie 'hit' or proceed with current hand ie 'stand'
def hit_or_stand(deck, hand):
    global playing

    while True and hand.value < 21:
        choice = input("Would you like to Hit or Stand? ")

        if choice.lower() == "hit":
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

    # if hand.aces > 0:
    #     hand.adjust_for_ace()

# show all of player's cards and some of dealer's cards


def show_some(player, dealer):
    print("\nDealer's Cards:")
    print("<First card is hidden.>")
    print(dealer.cards[1])
    print("\nPlayer's Cards:")
    print(player.cards)
    print(f"Value: {player.value}")
    # print(f"Value: {player.()}")

# show all of dealers and players cards


def show_all(player, dealer):
    print("\nDealer's Cards:")
    print(dealer.cards)
    print(f"Value: {dealer.value}")
    # print(f"Value: {dealer.adjust_for_ace()}")
    print("\nPlayer's Cards:")
    print(player.cards)
    print(f"Value: {player.value}")
    # print(f"Value: {player.adjust_for_ace()}")


def game_on():
    while True:
        play_again = input("\nWould you like to play again?: Yes/No ")
        if play_again.lower() == 'yes':
            print("Game On.")
            break
        elif play_again.lower() == 'no':
            print("Exiting the Game.")
            break
        else:
            print("Invalid input. Please try again.")
            continue
    return play_again.lower()


# putting together the pieces for the game
playing = True

# starting chip value
total = 100

while True:
    print("\nWelcome to the Game of Black Jack! \n")

    # Prompt the Player for their bet

    # Set up the Player's chips as a result of losing or winning bet
    print(f"Remaining chips: {total}")
    bet = take_bet()
    chips = Chips(total, bet)
    deck = Deck()

    # dealer keeps track of dealer's hand and player keeps track of player's hand
    dealer = Hand()
    player = Hand()

    # deck is shuffled and both player and dealer get two cards
    deck.shuffle()
    dealer.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    player.add_card(deck.deal())

    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)

    while playing:
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player)

        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)
        # If player's hand exceeds 21 break out of loop

        if player.value > 21:
            player_busts(player, dealer, chips)
            break

        # If player's hand = 21 break out of loop
        elif player.value == 21:
            player_wins(player, chips)
            break

# If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        elif player.value < 21 and dealer.value < 17:
            # start a while loop adding a card to dealer's hand while value is below 17
            while dealer.value <= 17:
                hit(deck, dealer)
                print("<Dealer gets one more card>")

                # Show all cards
                show_all(player, dealer)

                # different ending scenarios if player is below 21 and dealer does not need one more card
                if dealer.value < 21 and dealer.value > 17:
                    # print("Dealer Value adjusted for Ace <21 and >17 *4")
                    #       dealer.adjust_for_ace())

                    if dealer.value > player.value:
                        # print(
                        #     "Dealer value is greater than player value, between 17 and 21 *5")
                        #       dealer.adjust_for_ace(), ">", player.adjust_for_ace())
                        dealer_wins(dealer, chips)
                        break
                    elif dealer.value < player.value:
                        # print(
                        #     "Dealer value is less than player value, between 17 and 21 *6")
                        #       dealer.adjust_for_ace(), "<", player.adjust_for_ace())
                        player_wins(player, chips)
                        break
                    else:
                        push(player, dealer, chips)
                        # print(
                        #     "Dealer value is equal to player value, between 17 and 21 *7")
                        #       dealer.adjust_for_ace(), "=", player.adjust_for_ace())
                        break
                    break

                # ending scenario in case dealer's hand value exceeds 21
                elif dealer.value > 21:
                    # print("Dealer value is greater than 21 *8")
                    dealer_busts(dealer, chips)
                    break
                # ending scenario in case dealer's hand is 21
                elif dealer.value == 21:
                    # print("Dealer value equals 21 *9")
                    dealer_wins(dealer, chips)
                    break
        # ending scenarios for when neither player nor dealer have busted
        elif player.value < 21 and dealer.value > 17:
            if dealer.value > player.value:
                # print("Player value is less than dealer value, between 17 and 21 *10")
                dealer_wins(dealer, chips)
                break
            elif dealer.value < player.value:
                # print("Player value is greater than dealer value, between 17 and 21 *11")
                player_wins(player, chips)
                break
            elif dealer.value == player.value:
                push(player, dealer, chips)
                # print("Player value is the same as dealer value, between 17 and 21 *12")
                break
            # continue
        break

    # if the player has drawn down the chip balance to 0, Game Over!
    if chips.total == 0:
        print("\nNo more chips! Game Over")
        break
    else:
        # Ask to play again if there is a remaining chip balance
        play_again = game_on()
        if play_again == 'yes':
            total = chips.total
            playing = True
        elif play_again.lower() == 'no':
            total = chips.total
            playing = False
            break

# code backup
    # else:
    #     # Ask to play again if there is a remaining chip balance
    #     print("Dealer Value was: ", dealer.value)
    #     play_again = input("\nWould you like to play again?: Yes/No ")
    #     if play_again.lower() == 'yes':
    #         playing = True
    #         total = chips.total
    #         continue
    #     elif play_again.lower() == 'no':
    #         print("Thank you for playing!")
    #         playing = False
    #         total = chips.total
    #         break
    #     else:
    #         print("Invalid Input. Exiting the Game.")
    #     break
