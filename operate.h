#ifndef _OPERATE_H
#define _OPERATE_H
#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "architecture.h"
#include "vector.h"
// SWAP and RELIC not use on battle
enum operation {};
/*
FOCUS
ATTACK number_of_cards card_index(s)
DEFENSE number_of_cards card_index(s)
MOVE number_of_cards card_index(s) left/right
USE_A_SKILL basic_card_index skill_card_index
USE_A_SPECIAL special_card_index
BUY_A_CARD card_type(basic(0)/skill(1)) card_locates(attack:0, defense:1, move:2) card_level(none is 0)
GET_SPECIAL card_id
DRAW(draw a card) player
SHUFFLE_DECK player
GIVE_UP hand/deck/use card_index
REMOVE hand/graveyard/deck card_index
SAVECARD card_locates(attack:0, defense:1, move:2) card_index
LOADCARD card_locates(attack:0, defense:1, move:2)
REDUCE_DAMAGE value
TAKE_A_CARD to_hand/to_graveyards card_type(basic(0)/skill(1)) card_locates(attack:0, defense:1, move:2) card_level(none is 0)
CHOOSE value
SEND_A_CARD target_player hand/deck/deck_top/graveyard card_id
DROP_A_CARD targer_player deck_top/hand
SET_LOCATE player locate
BACK_A_CARD target_player card_index to_deck/to_hand
GET_TOKEN
USE_TOKEN value
SHOW_CARDS target_player numbers
CHANGE_IDENTITY identity(紅心皇后:1 瘋帽子:2 柴郡貓:3)
RANDOM_DROP_A_CARDS target_player
SET_TENTACALE locate
SET_DESTINY target_player(none:-1) card_type(basic(0)/skill(1)) card_locates(attack:0, defense:1, move:2) card_level(none is 0)
FLIP_DESTINY_TO_RED target_player(none:-1) card_type(basic(0)/skill(1)) card_locates(attack:0, defense:1, move:2) card_level(none is 0)
END
*/
void setup(game* status);
void turnStart(game status);
void dropCard(game status);
void showCard(game status, vector* showingCard, int32_t numbers);
void moveCharactor(game status);
bool updateOperate(game* status, vector* operate);
#endif