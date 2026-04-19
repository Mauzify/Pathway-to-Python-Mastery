# Pathway-to-Python-Mastery
Learning how to fully master python & purpose

Learning how to fully master python, understand basic functions to highly complex projects including NumPY, Cuda, PY-Torch, and other libraries. 
As I learn python, this will help build my portfolio, get deeper in IT Infrastructure and software development. 

As of right now, I'm current learning the basics of workflow, as functions, defines, if/elif/else, loops, ValueError excepts, etc.



For my PasswordGenerator.py script, this picture will explain length security.
<img width="622" height="658" alt="Screenshot 2026-04-18 110123" src="https://github.com/user-attachments/assets/13d06dd9-1311-4d6d-bc7c-89bc519a295a" />
This is a example of why it is important to have a strong, secure password. - DESMOS GRAPHING CALCULATOR

for my Chess Python script, this is where it gets interesting, after over 3.5-4~ hours of work, I managed to learn new mechanics and libraries. With the help of google you can do anything.

The Chess program has over 2+ difficulties for those who want a good, basic and simple TTY chess engine that can reach ELO up to 900-1000+, its fairly competitive for the average joe. 

in terms of the MINIMAX Algorithm used to determine the score in a zero sum game after a certain number of moves, the best play according to an evaluation function, the algorithm can be explained move sequences with length one are examined, the side to move (max player) can simply look at the evaluation after playing all possible moves. THe move with the best evaluation is chosen. But for a two-ply search, when the opponet also moves, things become more complicated. The opponet (min player) also chooses the move that gets the best score. Therefore, the score of each move is now the score of the worst that the opponent can do.
Sorce: Chess Programming WiKi-CPW \ MINIMAX Algorithm

For Example as shown:
int maxi( int depth ) {
    if ( depth == 0 ) return evaluate();
    int max = -oo;
    for ( all moves) {
        score = mini( depth - 1 );
        if( score > max )
            max = score;
    }
    return max;
}

Here's the math :)
<img width="774" height="756" alt="Screenshot 2026-04-18 234411" src="https://github.com/user-attachments/assets/364c65be-94ca-4546-950d-ba30b1498be3" />

Usually the Negamax algorithm is used for simplicity. This means that the evaluation of a position is equivalent to the negation of the evaluation from the opponent's viewpoint. This is because of the zero-sum property of chess: one side's win is the other side's loss.

<img width="636" height="448" alt="Screenshot 2026-04-18 225048" src="https://github.com/user-attachments/assets/e9b6f577-dab6-4147-9eaf-f0e57752e58f" />
Here's some gameplay of ThePythonChess.py :) (OLD - ARCHIVED)

https://github.com/user-attachments/assets/8567ada8-2c26-4198-a188-2962682c0cd5
(Video Example, Updated 4/19/2026 - 11:18 AM CST)
