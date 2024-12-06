from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A can be either a knight and a knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # If A is a Knight, Sentence is true
    Implication(AKnight, And(AKnight, AKnave)),
    # If A is a Knave, Sentence is false
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Either A and B are Knights or Knaves, but not both
    And(And(Or(AKnight, AKnave), Or(BKnight, BKnave)), Not(
        And(AKnight, AKnave)), Not(And(BKnight, BKnave))),
    # A and B can either be both knights, both knaves, or one of each
    Or(And(AKnight, BKnight), And(AKnave, BKnave), And(AKnight, BKnave), And(AKnave, BKnight)),
    # If A is a Knight, Sentence is true
    Implication(AKnight, And(AKnave, BKnave)),
    # If A is a Knave, Sentence is false
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Either A and B are Knights or Knaves, but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # Either they are the same kind or they are of different kinds
    Or(Or(And(AKnight, BKnight), And(AKnave, BKnave)),
       Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # If A is a Knight, they are of the same kind
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    # If A is a Knave, they are of different kinds
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # If B is a Knight, they are of different kind
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # If B is a Knave, they are of the same kinds
    Implication(BKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),
    # They cannot both be same and different kinds
    Implication(Or(And(AKnight, BKnight), And(AKnave, BKnave)),
                Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))),
    Implication(Or(And(AKnight, BKnave), And(AKnave, BKnight)),
                Not(Or(And(AKnight, BKnight), And(AKnave, BKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Either A, B and C are Knights or Knaves, but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
    # A is a Knight if and only if "I am a Knight" is true
    # A is a Knight if and only if "I am a Knave" is true
    Or(Biconditional(AKnight, AKnight), Biconditional(AKnight, AKnave)),
    # B is a Knight if and only if "A said 'I am a Knave'" is true
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    # Either C is a Knave or not
    Or(CKnave, CKnight),
    # Either A is a Knight or not
    Or(AKnight, AKnave),
    # If B is a Knight, A said he is a Knave and C is a Knave
    Implication(BKnight, CKnave),
    # If B is a Knave, A said he is a Knight and C is a Knight
    Implication(BKnave, CKnight),
    # If C is a Knight, A is a Knight
    Implication(CKnight, AKnight),
    # If C is a Knave, A is a Knave
    Implication(CKnave, AKnave),
    # B and C cannot both be Knights
    Not(And(BKnight, CKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2)
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
