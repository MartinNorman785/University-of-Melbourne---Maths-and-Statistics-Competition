import random
class Player: 
    def __init__(self, name): 
        self.name = name 
        self.total = 0 
        self.score = 0
    def draw(self):
        return random.uniform(0, 1)

    def take_turn(self, opponent_score=None):
        print(f"\n{self.name}'s Turn")
        self.total = self.draw()
        print(f"Initial draw: {self.total:.3f}")

        while True:
            if self.total > 1:
                self.total = 0
                print(f"{self.name} busted! Final score: 0")
                break

            print(f"Current total: {self.total:.3f}")
            print(f"Current score: {self.score:.3f}")
        
            action = input("Choose action - 'play' to draw again, 'pass' to end turn: ").strip().lower()
            if action == "pass":
                print(f"{self.name} passes with score: {self.total:.3f}")
                self.score += self.total
                break
            elif action == "play":
                new_draw = self.draw()
                print(f"Drew: {new_draw:.3f}")
                self.total += new_draw
            else:
                print("Invalid input. Please type 'play' or 'pass'.")
            print()
 
class Game: 
    def __init__(self, num_rounds=1): 
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.rounds = num_rounds
    def play(self):
        for _ in range(self.rounds):
            self.player1.take_turn()
            self.player2.take_turn(opponent_score=self.player1.score)

        print("\nGame Over!")
        print(f"Player 1 score: {self.player1.score:.3f}")
        print(f"Player 2 score: {self.player2.score:.3f}")

        if self.player1.score > self.player2.score:
            print("Player 1 wins!")
        elif self.player2.score > self.player1.score:
            print("Player 2 wins!")
        else:
            print("It's a tie!")
        print()
 
Game(1).play()
