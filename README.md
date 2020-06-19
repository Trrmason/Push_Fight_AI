# B351_Team25
<h1> B351 final project over push fight </h1>

There are multiple files for our project.

1. game.py              | This is the functionality of the Push Fight game with comments explaining the directions and code
2. player.py            | This is the implementation of MCTS. This file also has Three players, MCTSPlayer, ModelPlayer, and UserPlayer.
3. testing.py           | This file was used for different tests, but mainly was used for generating data by calling player.py's simulate_game function.
4. model.py             | This file was used for training and testing GBR. Things are commented out and switched due to trying to figure out the best configuration.
5. game_data.csv        | This file was used to store the game board states with their win percentage for GBR.
6. player_1_model.pkl   | This file is the dumped/saved trained model for player 1 using joblib
7. player_1.1_model.pk1 | The same as player_1_model.pkl, but trained without dropping duplicate states. Saw better results with this model.
8. player_2_model.pk1   | Same as #6 but player_2.
9. player_2.1_model.pk1 | Same as #7 but player_2.
10. game_play.py        | This file is used for simulating game play and user game play
__________________________________________________________________________________________________________________________________________________________
Finally to run the program      
To run the already configured simulation just run the file game_play.py    
To change settings Directions:    
For ModelPlayer, you can change to player #1 by setting player to -1 or player #2 by setting player to 1   
For MCTSPlayer, the player settings are the same as above, but you can change num_sim to any number for more MCTS simulation for a move     
For UserPlayer, you can change the player setting like above.   
To enter the players into a game use play_game(player#1, player#2)   
To simulate a game multiple times use play_game(player#1, player#2, num_sims = #)   
       
game_data.csv has over 500,000 boards saved so we didn't want to push the whole file. So it's just a sample of 5,000 boards   
If you would like the whole file please contact our team.    
You can download any needed dependencies with requirements.txt
