# MexTrain
Home project for OOP learning on the base of Mexican train board game

## HOWTO:
1. **Demo**. You can just run start.py for demonstration. It will print whole game.
2. **Manual** dev-like. In py-console.
   1. import mextrain.
   2. init table (tbl = mextrain.Table(number or players))
   3. start first game round (gr = mextrain.GameRound(tbl, round number))
   4. init trails for each player (gr.init_trail(player number, 0 as difficulty))
   5. ~~start common trail: gr.turn(0) until someone puts tile to Table.trail.~~
   5. make turns (gr.turn(0 for difficulty)) until the end.
   6. do aftermath (gr.aftermath()).
   7. start new round.

## TODOs:
- [x] Add Player class. /add-player
- [ ] Add init move. Look for TODO. /fix-second-level-init-trail
* Add second-level difficulty. Look for TODO.
  - [ ] Fix init trails.
  - [ ] Add to turn.
- [ ] Make interactivity.

### nice to have
- [ ] Add third-level difficulty. Graph-based.
