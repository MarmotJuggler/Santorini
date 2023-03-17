#include <stdio.h>
#include <stdlib.h>

#define height 3
#define width 3

int startState[height][width][2];

void FindLocation(int position[height][width][2], int activePlayer, int *x, int *y){
    for (*x = 0; *x < height; (*x)++){
        for (*y = 0; *y < width; (*y)++){
            if (position[*x][*y][1] == activePlayer){
                return;
            }
        }
    }
}

int FindActivePlayer(int position[height][width][2]){
    int sum = 0;
    for (int x = 0; x < height; x++){
        for (int y = 0; y < width; y++){
            sum += position[x][y][0];
        }
    }
    if (sum % 2 == 0){
        return 1;
    }
    return 2;
}

void DoMove(int position[height][width][2], int *move, int newPosition[height][width][2]){
    int activePlayer = FindActivePlayer(position);
    int activePlayerLocationX, activePlayerLocationY;
    FindLocation(position, activePlayer, &activePlayerLocationX, &activePlayerLocationY);
    for (int x = 0; x < height; x++){
        for (int y = 0; y < width; y++){
            newPosition[x][y][0] = position[x][y][0];
            newPosition[x][y][1] = position[x][y][1];
        }
    }
    newPosition[move[0]][move[1]][1] = activePlayer;
    newPosition[activePlayerLocationX][activePlayerLocationY][1] = 0;
    newPosition[move[2]][move[3]][0] += 1;
}

void MoveDirections(int position[height][width][2], int availableMoves[8][2]) {
    int activePlayer = FindActivePlayer(position);
    int location[2];
    FindLocation(position, activePlayer, &location[0], &location[1]);
    //sides
    if (location[0]+1 < height && position[location[0]+1][location[1]][1] == 0 && position[location[0]+1][location[1]][0] < 4
    && (position[location[0]+1][location[1]][0] - position[location[0]][location[1]][0]) <= 1) { //bottom middle
        availableMoves[0][0] = +1;
        availableMoves[0][1] = 0;
    }
    if (location[0]-1 > -1 && position[location[0]-1][location[1]][1] == 0 && position[location[0]-1][location[1]][0] < 4
    && (position[location[0]-1][location[1]][0] - position[location[0]][location[1]][0]) <= 1) { //top middle
        availableMoves[1][0] = -1;
        availableMoves[1][1] = 0;
    }
    if (location[1]+1 < width && position[location[0]][location[1]+1][1] == 0 && position[location[0]][location[1]+1][0] < 4
    && (position[location[0]][location[1]+1][0] - position[location[0]][location[1]][0]) <= 1) { //right middle
        availableMoves[2][0] = 0;
        availableMoves[2][1] = +1;
    }
    if (location[1]-1 > -1 && position[location[0]][location[1]-1][1] == 0 && position[location[0]][location[1]-1][0] < 4
    && (position[location[0]][location[1]-1][0] - position[location[0]][location[1]][0]) <= 1) { //left middle
        availableMoves[3][0] = 0;
        availableMoves[3][1] = -1;
    }
    //corners
    if (location[0]+1 < height && location[1]+1 < width && position[location[0]+1][location[1]+1][1] == 0 && position[location[0]+1][location[1]+1][0] < 4
    && (position[location[0]+1][location[1]+1][0] - position[location[0]][location[1]][0]) <= 1) { //bottom right
        availableMoves[4][0] = +1;
        availableMoves[4][1] = +1;
    }
    if (location[0]-1 > -1 && location[1]-1 > -1 && position[location[0]-1][location[1]-1][1] == 0 && position[location[0]-1][location[1]-1][0] < 4
    && (position[location[0]-1][location[1]-1][0] - position[location[0]][location[1]][0]) <= 1) { //top left
        availableMoves[5][0] = -1;
        availableMoves[5][1] = -1;
    }
    if (location[0]+1 < height && location[1]-1 > -1 && position[location[0]+1][location[1]-1][1] == 0 && position[location[0]+1][location[1]-1][0] < 4
    && (position[location[0]+1][location[1]-1][0] - position[location[0]][location[1]][0]) <= 1) { //bottom left
        availableMoves[6][0] = +1;
        availableMoves[6][1] = -1;
    }
    if (location[0]-1 > -1 && location[1]+1 < width && position[location[0]-1][location[1]+1][1] == 0 && position[location[0]-1][location[1]+1][0] < 4
    && (position[location[0]-1][location[1]+1][0] - position[location[0]][location[1]][0]) <= 1) { //top right
        availableMoves[7][0] = -1;
        availableMoves[7][1] = +1;
    }
    return;
}

void GenerateMoves(int position[height][width][2], int availableMoves[8][2], int builds[8][8]) {
    int activePlayer = FindActivePlayer(position);
    int location[2];
    FindLocation(position, activePlayer, &location[0], &location[1]);
    int** moves = MoveDirections(position);
    int count = 0;
    for (int i = 0; i < 8; i++) {
        int newRow = location[0] + moves[i][0];
        int newCol = location[1] + moves[i][1];
        if (newRow < 0 || newRow >= height || newCol < 0 || newCol >= width) {
            continue;
        }
        if (position[newRow][newCol][1] != 0) {
            continue;
        }
        int*** newPosition = CopyPosition(position);
        newPosition[newRow][newCol][1] = activePlayer;
        builds[count] = MoveDirections(newPosition);
        count++;
        FreePosition(newPosition);
    }
    FreeMoves(moves);
    return;
}

int PrimitiveValue(int*** position) {
    int activePlayer = FindActivePlayer(position);
    int location[2];
    FindLocation(position, activePlayer, &location[0], &location[1]);
    int value = 0;
    //check if current player is on the opponent's baseline
    if ((activePlayer == 1 && location[0] == 0) || (activePlayer == 2 && location[0] == height-1)) {
        value = "WIN";
    }
    //check if opponent is on the current player's baseline
    else if ((activePlayer == 1 && location[0] == height-1) || (activePlayer == 2 && location[0] == 0)) {
        value = "LOSS";
    }
    return value;
}

int WonCheck(int*** position) {
    int activePlayer = FindActivePlayer(position);
    int location[2];
    FindLocation(position, activePlayer, &location[0], &location[1]);
    //check if current player is on the opponent's baseline
    if ((activePlayer == 1 && location[0] == 0) || (activePlayer == 2 && location[0] == height-1)) {
        return 1;
    }
    //check if opponent is on the current player's baseline
    else if ((activePlayer == 1 && location[0] == height-1) || (activePlayer == 2 && location[0] == 0)) {
        return -1;
    }
    return 0;
}