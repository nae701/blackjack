import random
import sys

# define the card ranks, and suits
ranks = list(range(2, 11)) + ['J', 'Q', 'K', 'A']
suits = ['SPADE', 'HEART', 'DIAMOND', 'CLUB']


def get_deck():
    """Return a new deck of cards."""
    return [[rank, suit] for rank in ranks for suit in suits]


def get_value(card, total):
    """Return the value of a card in blackjack"""
    if card[0] in range(2, 11):
        return card[0]
    if card[0] == "J" or card[0] == "Q" or card[0] == "K":
        return 10
    if card[0] == "A" and total < 11:
        return 11
    else:
        return 1


def is_soft(hand):
    """Return whether a hand is soft or hard based on if there is an ace"""
    for card in hand:
        if card[0] == "A":
            return True
    return False


def num_ace(hand):
    """Returns the number of aces in a hand"""
    aces = 0
    for card in hand:
        if card[0] == "A":
            aces += 1
    return aces


def dealer_game(hand, hit, score_hit, total, number_ace):
    """Executes the recursive game logic for the dealer and returns their score"""
    score_initial = get_value(hand[0], total) + get_value(hand[1], total)
    score = score_initial + score_hit
    print("DEALER:" + str(hand), '\n')
    print("Dealer's score: " + str(score), '\n')

    # Dealer must hit if below 17
    if score < 17:
        hand.append(deck.pop())
        hit += 1
        score_hit = score_hit + get_value(hand[1 + hit], score)
        return dealer_game(hand, hit, score_hit, score, number_ace)

    # Checks if dealer has a soft hand and can continue
    elif score > 21:
        if number_ace > 0:
            if num_ace([hand[1 + hit]]) > 0:
                number_ace += 1
            return dealer_game(hand, hit, score_hit, score, number_ace - 1)

        print("DEALER BUSTS.\n")
        return 1

    elif score == 21:
        return score

    else:
        return score


def player_game(hand, hit, score_hit, total, number_ace):
    """Executes the recursive game logic for the player and returns their score"""
    score_initial = get_value(hand[0], total) + get_value(hand[1], total)
    score = score_initial + score_hit
    print("PLAYER:" + str(hand), '\n')
    print("Player's score: " + str(score), '\n')
    player_choice = input("Would you like to 'HIT' or 'STAY': \n")

    if player_choice.lower() == "stay":
        return score

    # Adds a card to player's hand and determines new score
    elif player_choice.lower() == 'hit':
        hand.append(deck.pop())
        hit += 1
        score_hit = score_hit + get_value(hand[1 + hit], score)
        score = score_initial + score_hit

        # Check if player busts or can continue with ace as 1 now
        if score > 21:
            if number_ace > 0:
                if num_ace([hand[1 + hit]]) > 0:
                    number_ace += 1
                return player_game(hand, hit, score_hit, score, number_ace - 1)

            print("PLAYER:" + str(hand), '\n')
            print("Player's score: " + str(score), '\n')
            print("YOU BUST.\n")
            return 0

        elif score == 21:
            return score

        return player_game(hand, hit, score_hit, score_hit, number_ace)

    else:
        print("Choose to either 'HIT' or 'STAY'.\n")
        return player_game(hand, hit, score_hit, score, number_ace)


def wager_amount(total):
    """Returns the wager the user would like to place"""
    wage = float(input("How much would you like to wager? (To exit enter 0)\n"))
    if wage < 0 or wage > total:
        print("You cannot wager that amount!\n")
        wager_amount(total)

    return wage


if __name__ == '__main__':

    money = 100
    keep_playing = True

    while keep_playing:

        # get a deck of cards, and randomly shuffle it
        deck = get_deck()
        random.shuffle(deck)

        wager = wager_amount(money)

        # Checks if player wants to quit
        if wager == 0:
            sys.exit()

        # Deals each hand, removing the cards from the deck
        dealer_hand = [deck.pop(), deck.pop()]
        player_hand = [deck.pop(), deck.pop()]

        print("DEALER:" + str(dealer_hand[0]), '\n')

        player_score = player_game(player_hand, 0, 0, 0, num_ace(player_hand))
        dealer_score = dealer_game(dealer_hand, 0, 0, 0, num_ace(dealer_hand))

        player_score_initial = get_value(player_hand[0], 0) + get_value(player_hand[1], 0)
        dealer_score_initial = get_value(dealer_hand[0], 0) + get_value(dealer_hand[1], 0)

        # Prints out game's outcome and money won/lost
        if player_score > dealer_score:
            if player_score_initial == 21:
                money = money + 1.5 * wager
                print("You have BLACKJACK!")
                print("Money: " + str(money))
            else:
                money = money + wager
                print("You win!")
                print("Money: " + str(money))
        elif player_score == dealer_score:
            if player_score_initial == 21:
                print("You and Dealer both have BLACKJACK! It is a push.")
                print("Money: " + str(money))
            else:
                print("It is a push.")
                print("Money: " + str(money))
        else:
            if dealer_score_initial == 21:
                money = money - wager
                print("Dealer has BLACKJACK!")
                print("Money: " + str(money))
            else:
                money = money - wager
                print("Dealer wins.")
                print("Money: " + str(money))
