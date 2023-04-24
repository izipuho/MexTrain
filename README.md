# MexTrain
Home project for OOP learning on the base of Mexican train board game

## HOWTO:
1. **Demo**. You can just run start.py for demonstration. It will print whole game.
2. **Manual** dev-like. In py-console.
   1. import Game and Table.
   2. init table (tbl = Table(number or players))
   3. start first game round (gr = Game.Round(tbl, round number))
   4. init trails for each player (gr.init_trail(player number, 0 as difficulty))
   5. make turns (gr.turn(player number)) until the end.
   6. do aftermath (gr.aftermath()).
   7. start new round (3).

## TODOs:
- [x] Add Player class.
- [x] Add init move. 
* Add second-level difficulty. 
  - [x] Fix init trails.
  - [x] Add to turn.
- [x] Make interactivity.
- [ ] Add manual player.

### nice to have
- [ ] Add third-level difficulty. Graph-based.
