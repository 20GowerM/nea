import random

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

#Standard deck using Fisher-Yates shuffle.
class Deck:

    def __init__(self):
        self.cards = [(rank, suit) for suit in SUITS for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        # Fisher-Yates: walk backwards, swapping each card with a random earlier one
        for i in range(len(self.cards) - 1, 0, -1):
            j = random.randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def draw(self):
        return self.cards.pop()

#Holds the cards for both the dealer and player, and calculates their value.
class Hand:

    def __init__(self, cards=None):
        self.cards = cards if cards else []

    def add(self, card):
        self.cards.append(card)

    def value(self):
        total = 0
        aces = 0
        for rank, _ in self.cards:
            if rank == "A":
                total += 11
                aces += 1
            elif rank in ("J", "Q", "K"):
                total += 10
            else:
                total += int(rank)
        #Aces count as 11, but if the player will bust they count as 1 instead.
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def is_bust(self):
        return self.value() > 21

    def can_split(self):
        return len(self.cards) == 2 and self.cards[0][0] == self.cards[1][0]

    def __str__(self):
        cards = ", ".join(f"{rank} of {suit}" for rank, suit in self.cards)
        return f"{cards} (value {self.value()})"

#Keep asking until the player enters an option.
def get_choice(options):
    while True:
        choice = input(f"Choose an action ({' / '.join(options)}): ").strip().lower()
        if choice in options:
            return choice
        print("Invalid choice, please try again.")

#The player's turn, which consists of hitting, standing, doubling down, or splitting. If the player splits, they will play each hand in turn.
def player_turn(hand, deck):
    finished = []
    to_play = [hand]

    while to_play:
        current = to_play.pop(0)

        while True:
            print(f"\nYour hand: {current}")

            if current.is_bust():
                print("Bust!")
                break
            if current.value() == 21:
                print("21!")
                break

            options = ["hit", "stand"]
            if len(current.cards) == 2:
                options.append("double")
            if current.can_split():
                options.append("split")

            choice = get_choice(options)

            if choice == "hit":
                current.add(deck.draw())
            elif choice == "stand":
                break
            elif choice == "double":
                current.add(deck.draw())
                print(f"You drew one card: {current}")
                break
            elif choice == "split":
                new_hand = Hand([current.cards.pop()])
                current.add(deck.draw())
                new_hand.add(deck.draw())
                to_play.append(new_hand)
                print("Hand split into two hands. Playing the first hand now.")

        finished.append(current)

    return finished

#Dealer hits up to 17, then stands.
def dealer_turn(dealer, deck):
    """Dealer hits until reaching 17 or more, then stands."""
    while dealer.value() < 17:
        dealer.add(deck.draw())

#Calculates the winner based on hand values.
def determine_winner(player_hand, dealer_hand):
    player_value = player_hand.value()
    dealer_value = dealer_hand.value()

    if player_value > 21:
        return "lose"
    if dealer_value > 21:
        return "win"
    if player_value > dealer_value:
        return "win"
    if player_value < dealer_value:
        return "lose"
    return "draw"


def play_round():
    deck = Deck()
    player = Hand()
    dealer = Hand()

    for _ in range(2):
        player.add(deck.draw())
        dealer.add(deck.draw())

    print("\n" + "=" * 40)
    print(f"Dealer shows: {dealer.cards[0][0]} of {dealer.cards[0][1]}")

    player_hands = player_turn(player, deck)

    #If the player went bust, the dealer doesn't need to play.
    if any(not h.is_bust() for h in player_hands):
        dealer_turn(dealer, deck)

    print("\n" + "-" * 40)
    print(f"Dealer's hand: {dealer}")

    for i, hand in enumerate(player_hands, start=1):
        label = f"Hand {i}" if len(player_hands) > 1 else "Your hand"
        result = determine_winner(hand, dealer)
        message = {"win": "You win!", "lose": "You lose.", "draw": "It's a draw."}[result]
        print(f"{label}: {hand} -> {message}")

#Starts and loops the system until the player chooses to stop playing.
def main():
    print("Welcome to Blackjack!")
    while True:
        play_round()
        again = input("\nPlay another round? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()