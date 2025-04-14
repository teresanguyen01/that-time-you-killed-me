# That Time You Killed Me

## Table of Contents

- [Game Overview](#game-overview)

## Game Overview

That Time You Killed Me is a two-player game where players take turns playing as either the time traveler or the time cop. The game is played on a 5x5 grid, and players use cards to move their pieces and take actions. The goal of the game is to eliminate the opponent's time traveler while protecting your own.

### Setup

Each player chooses a color and takes the 7 pawns in their color and a focus token. There are 3 grids: past, present, future. The white player must place their pawn on the space 1 of each board and the black player places their pawn on space 1 as well.

The first player must place their focus token on the past board. The second player must place their focus token on the future board.

The game is played in rounds, with each player taking turns to play cards and move their pieces.

On your turn, you must:

1. choose 1 pawn
2. take 2 actions: move, push, squish, cause a paradox, etc. - can move down, up, left, right or 2 spaces
   - move 1 space
   - move 2 spaces
   - push 1 space
   - squish 1 space
   - cause a paradox (move to the past or future)
   - move to the focus token
3. shift focus token

### Board Representation

The game involves 3 4x4 boards: past, present, and future. Each board has a grid of spaces where players can move their pieces. The boards are represented as follows:

```
---------------------------------
                          black
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
|1| | | |   |2| | | |   |3| | | |
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
| | | | |   | | | | |   | | | | |
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
| | | | |   | | | | |   | | | | |
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
| | | |A|   | | | |B|   | | | |C|
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
  white
Turn: 1, Current player: white
```

The black player's starting pieces are represented by numbers in the top left corner of each board. The white player's pieces are represented by letters in the bottom right corner of each board. The focus token is represented by the term "white" or "black" on the board.

White is focused on the past and black is focused on the future.

### Move Representation

On a player's turn, they indicate through the CLI which piece they wish to move, which two directions they wish to move, and which era board they want to move their focus to for the next turn.

```

---------------------------------
                          black
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
|1| | | |   |2| | | |   |3| | | |
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
| | | | |   | | | | |   | | | | |
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
| | | | |   | | | | |   | | | | |
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
| | | |A|   | | | |B|   | | | |C|
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
  white
Turn: 1, Current player: white
Select a copy to move
A
Select the first direction to move ['n', 'e', 's', 'w', 'f', 'b']
n
Select the second direction to move ['n', 'e', 's', 'w', 'f', 'b']
f
Select the next era to focus on ['past', 'present', 'future']
present
Selected move: A,n,f,present
---------------------------------
                          black
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
|1| | | |   |2| | | |   |3| | | |
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
| | | | |   | | | | |   | | | | |
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
| | | | |   | | | |A|   | | | | |
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
| | | | |   | | | |B|   | | | |C|
+-+-+-+-+   +-+-+-+-+   +-+-+-+-+
              white
Turn: 2, Current player: black

```

### Requirements

1. **board setup and display**

   - construct the three 4x4 boards representing the past, present, and future.
   - print the boards to stdout at the start of the program

2. **human player interactions**

   - 2 human players via command line inputs
   - at the start of each turn, display the boards including the location of each players focus, the turn number, and the current player
   - a player is prompted to select a piece, two move directions, and the next board to focus on
   - invalid actions should not be allowed by the program
     - invalid piece selection -> print `Not a valid copy` and repeat the prompt
     - user selects a piece that is not theirs -> print `That is not your copy` and repeat the prompt
     - selects one of their pieces but not in the correct era -> print `Cannot select a copy from an inactive era` and repeat the prompt
     - enters a valid direction that the worker cannot move into -> print `Cannot move <direction>` (direction is user's selection) and repeat the prompt
     - enters an invalid era for their focus -> print `Not a valid era` and repeat the prompt
     - enters a currently active era -> print `Cannot select the current era` and repeat the prompt
   - after full move is completed, print the new line showing the worker, move direction, and next area of focus

3. **game end condition**:

   - at the start of a turn, check if the game has ended. If the current player has pieces in only one era board, then that player has lost and the other player has won
   - when the game ends, print `white has won` or `black has won` and ask if the user would like to play again
   - if the user selects yes, reset the game and start over
   - if the user responds with anything else, exit.

4. **enumerating possible moves**:

   - a piece may be unable to move:
     - this can happen if it is surrounded by friendly copies since we can't take a move that would directly cause a paradox
     - if a piece is only able to take one move, but another of that player's pieces in the same active era board can take 2, then the first one cannot be chosen
     - We don't want the player to get stuck having selected a piece that can't move, so whenever a piece is selected, we should check all the valid moves. If it can't move, then print `That copy cannot move` and repeat the prompt to select a different piece.
   - In the rare case that a piece can only make one move and it is the only available piece in the active board, then after the player selects the first move direction, the program should skip the prompt for a second move and go straight to selecting the next era to focus on.
   - If at the start of a player's turn, there are no pieces on the currently active board or the available pieces are unable to move, then both movement prompts are skipped. Print No copies to move then skip straight to the prompt for the next era board to focus on.

5. **random AI**:

- random computer player that will randomly choose a move from the set of allowed moves
- Two bots should be able to play against each other, in which case it will run through all the turns without prompting for additional input, until the game ends.

6. **heuristic ai**:

- Create a Heuristic computer player that will assess the available moves and choose the one it thinks is best based on a few criteria.

Criteria:

- _Era presence_: The number of era boards containing at least one of a player's pieces. Since we lose if we are only present in one era, we want to count how many era's we are occupying.
- _Piece advantage_. The number of pieces a player has across all boards, minus the number of pieces the opponent has. This helps the AI value plays that remove opposing pieces while also valuing bring out new pieces from the supply.
- _Supply_. The number of pieces available in a player's supply. This can be important because we can't move backwards in time once we run out. This needs to be balanced with having pieces on the board to work with.
- _Centrality_. The number of pieces a player has on spaces in the middle of the board (as opposed to the edges). Being on an edge is more dangerous and leaves less movement flexibility, so we want to value ending in the middle.
- _Focus_. The number of pieces a player controls in the current era they are focusing on. This helps decide which era to select next since we would rather not get stuck skipping a turn because the era chosen has no pieces to move.

### Undo and Redo

When enabled with the history command line argument, the game should give the options undo, redo, or next before every turn
Undo: roll back to the previous game state
Redo: reverses the most recent undo
Undo does nothing if at turn 1 and redo does nothing if it is already the latest turn.
After using undo, taking any new turn should invalidate any turns that could have been redone.
To continue taking turns as usual, the user should enter next.
To clarify, the AI players do not interact with this option. The choice of undo, redo, or next is a meta option presented to the user at every turn. You could have two AI players playing against each other and a human could observe step by step using the next command or undo/redo the AI turns.

### Design Patterns

**Composite**. May be useful for setting up the adjacency of spaces for valid moves, especially since moves can jump across boards.

**Abstract factory/factory method**. Useful for setting everything up in a modular way. If you do this well you can achieve some nice isolation between components making it easier to re-use the code for other similar games with different set ups. This may also be useful for resetting the game to start again.

**Decorator**. Could be a good way to add the the undo/redo/next interface on top of the basic CLI in a modular way.

**Strategy/Template method.** Both are good options for implementing the 3 types of players, human/random/heuristic. You could maybe consider State here too, but it's such a similar pattern that the difference in implementation may be mostly semantic.

**Command.** A good fit for representing move objects, especially since you will need to be able to generate moves without executing them right away. It can also help decouple some components from the board.

**Memento.** Very useful for undo/redo.

**Iterator.** It's not good enough just to use any for loop and claim that's using an iterator. However, you may find good uses for custom iterators over structures you've created.

**Observer.** This is a good pattern to use for the game state and the players. The game state should be able to notify the players when it changes, and the players should be able to observe the game state without being tightly coupled to it.
