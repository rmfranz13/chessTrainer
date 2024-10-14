# Chess Trainer 

Welcome to the chess trainer! There are 100 levels and you start off on level 0, which effectively represents pure random play. Winning a game moves you up 2 levels, losing a game moves you down 1 level, a draw moves you up 1 level. Level 100 is an unaltered version of Leela Chess Zero engine, which is far superhuman. Each "level" represents an amount of noise added to this super human network such that it roughly achieves a particular level of play. Every opponent is generated uniquely for the game at hand, so there are no guarantees about the sort of opponent you'll be facing, and that's the point. This includes playing strength. Winning a game doesn't guarantee your next opponent will be stronger, but on average it does mean you'll be facing a more Leela Chess Zero-like opponent (which tends to make it stronger). Because you move up 2 levels for a win and down 1 level for a loss, once you find your sweet spot you'll on average face off against slightly stronger opponents than yourself, which is how you naturally improve: you always have a shot of winning, your opponents won't be indestructable, but they'll tend to be a step ahead on the average. 

Since you're starting off on level 0, you'll start off with some very easy games. For me it takes around 20 easy games before the engine starts beating me. You'll notice it improving skills as you move up, although the skills might improve in a way that surprises you. Take note of what it seems surprisingly good at, because it's probably not an accident. If it seems like it's too good at check mate sequences given how terrible it's opening is, that's because check mate sequences are so deeply engrained in the super-human network that it's the last good strategy remaining after everything else has been flushed out. That's a major sign that you can improve your game by focussing on, say, checkmate sequences... or whatever it seems weirdly good at. And playing against this trainer is exactly how you can focus on those areas.

It turns out most humans, myself included (especially myself) are simply unaware of the universe of possible chess strategies. For instance, you'll never meet a decent human chess player who marches their king straight out into the center of the board and still beats you. Here, you may encounter such players. Here, it is possible to encounter any mathematically possible chess player, and you'll be playing mostly against the possible chess players that are slightly stronger than you. This trainer starts from nothing, pure random play, and builds up chess strategy in the correct order until it's superhuman, showing you at each step along the way exactly what it is you should be focussing on.

That is why this training program is designed as it is. There is no time limit, there are no take-backs, no analysis. There's just playing full games of chess, on a board, start to finish, the old fashioned way. Nobody knows the answers and mistakes have consequences.

There's no resigning either. The AI can't feel anything, so there's no sense in being respectful to it. The point here is learning chess and I think you'll find the engine can teach you something even in a hopelessly lost end game. That being said, you can always rage-quit by simply exiting out, but progress won't be made (or lost).

Subsequent games should be kicked off the same as this first game, but you won't see this message again.

You can view a graph of your progress with the "show progress" button once the chess GUI opens (you'll need a game under your belt to see anything). You can reset progress completely (and see this message again) with the "reset progress" button.
    
Good luck!

# Requirements: 

For now, this requires you have Python3 and git on a Windows machine. Typing "python" at the windows terminal should put you in an interactive python 3 session (powershell or cmd or 3rd party terminal such as might come with python or anaconda). Similarly "git" should be an accessible command from the same terminal.

You can get git for windows here: https://git-scm.com/downloads/win
And python for windows here: https://www.python.org/downloads/windows/

# Initial setup:
Simply clone this repo and pip install the dependencies (there's only 2: python-chess for the chess-playing logic and certain aspects of the chess GUI, and protobuf which is needed to read and apply noise to the network weights for each game).
```
git clone https://github.com/rmfranz13/chessTrainer.git
cd chessTrainer
pip install -r requirements.txt
```

# How to run:
Now each game will be kicked off simply by calling do_chess.py:
```
python do_chess.py
```

If all goes according to plan, you should be greeted with a welcome message (mostly the same info in this readme), clicking OK, you should see in the terminal the 13 layers of the neural network having noise applied, this may take a few seconds, then a GUI will pop up that randomly selects you to either play black or white. If black, the engine will immediately start playing (might take a minute to load the engine and calculate the move, but shouldn't take more than 10 seconds for subsequent moves). There is no timer and the only options you have besides playing chess moves is to resign or force the engine to resign. This is intended to remove unneeded complixity with options around search depth and thinking time. There are no take-backs, no analysis, no time limit for you. The point is simply to play chess. The games are saved, and you'll see a message indicating where, and you can look at them manually if desired, but the spirit of this trainer is simply to pit you against as many interesting opponents as possible, each opponent (once you find your approximate skill range) having something unique to teach you.

Once the game is over, either by checkmate, resignation, or one of the many possible draw conditions, it will automatically be saved and the window will close.

To play the next game simply re-run 
```
python do_chess.py
```

This time, the level of noise added to the network will be adjusted based on the result of your previous game, making for a better opponent if you won, or a worse opponent if you lost. This cycle repeats indefinitely, and a plot will open with each new game showing the progress you've made.

# How does it work?

I start off with a fully-trained network from leelaChess, this is called the "master" network. It's not literally a perfect chess-playing agent, but you can bet it's much stronger than you. I add a lot of noise to it so that it plays randomly, and then as you keep playing... winning and losing, the amount of noise gets adjusted each game, giving you players that are always unique and always about as far from perfect as you are. It will aim to win 2/3 of the games against you, and push you towards strategy more like that of the master network over time. That is... we are distilling the chess knowledge gained by leelaChess over millions of games into you the human. It just so happens that as you become more master-like in chess, you will become... more master-like in chess. This approach doesn't teach you what's good or bad chess strategy, it just pits you against an infinite number of unique opponents that drive you in the direction of being more like the master network.

You start off on level 0 representing pure random play. Winning a game moves you up 2 levels, losing a game moves you down 1 level, a draw moves you up 1 level. Each level up reduces the amount of noise added to the training network you'll play against in the next round, bringing that agent closer to the master network, causing feature's of master's playing style to become ever-more apparent. By the time you get to level 100, you're playing the un-altered master network and defeating it means you're likely superhuman at chess (there's some hardware dependence though). The agent playing against you is generated prior to each chess game, persists for the duration of the game, then disappears forever. In other words, whatever strategies you encounter as you play, you'll likely never see those exact strategies ever again, even if you keep playing around the same level. You're being exposed to all possible chess strategies that are roughly as far from master as you are. Some agents randomly like bishops better than rooks, or randomly prefer the left side of the board vs the right, or really like moving one particular piece a lot. It doesn't know what the relative worth of pieces are, it doesn't know the value of controlling the center or having rooks on open files or knights on outposts. These aspects of the strategy change with each new opponent, but as you get closer to level 100, getting to ever-increasing levels of play, you'll start to notice patterns in the noise, strategies that are successful, and these turn out to be what we might recognize as strategy. Because winning moves you up 2 levels, but losing moves you down 1 level, you will on average be playing against a slightly stronger opponent than yourself, which is how you improve. Unlike far-superhuman chess engines that tend to beat you into a risk-averse strategy where you're just trying to last as long as possible, the opponents you face here will not be indestructable, you'll always have a fighting chance. Additionally, it will not make intentionally stupid moves which is a common strategy to get standard chess engines to play at a certain level. It's always trying to win, even when the amount of noise added is such that it appears to be playing terribly. 

The first 10 to 20 games might feel absurdly easy, and you might question whether it's improving at all. Rest assured it is getting better with each level (on average), and rest assured you will not make it to level 100. You might see sparks of good strategy appear around level 20-30 only to then witness a needless queen sacrifice. The reason I included so many levels where it appears to be playing terribly is because there is signal in the noise on these levels... it may not be particularly good at the early levels but it isn't random. Perhaps the earliest improvement you'll notice is that it will start avoiding check mate for longer, rather than walking straight into it (even at the cost of random queen sacrifices)... it will make you chase the king around a little longer before you're able to ultimately check mate. It will also improve at putting pressure on your king and specifically directly attacks at your king, even though it may do a terrible job of this and end up throwing away the pieces it was attempting to attack your king with. Somewhere in the level 30 range, it'll start to become more adept at tactics, and understand that it ought to protect it's pieces and re-capture. It appears to start to care more about material, but this is only as a means of achieving the king-directed strategies it had come across earlier. This progression of skills isn't an accident, it's building up chess skills in a very logical way. The most important aspect of chess is to protect the king and attack your opponents king, and you'll notice the AI doing a better job of this even before it understands that a queen is more valuable than a pawn. By the time you get to level 70 (way above my level) it's playing recognizable openings to a deep level, not because it's memorized those openings but because it's good enough to "understand". The engine will teach you what's important for you to understand at your skill level, often through humiliating defeat and putting you in the weirdest positions you could never have dreamed of. If your head hurts, that means you're learning, and I have never met human opponents who could make my head hurt so much.

