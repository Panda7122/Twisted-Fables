#ifndef _ARCHITECTURE_H
#define _ARCHITECTURE_H
#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "vector.h"
typedef struct _buyDeck {
    vector cards;
    // Scheherazade
    uint32_t destiny_TOKEN;  // 0:none 1:blue 2:red
} buyDeck;
typedef struct _player {
    int8_t team;  // for 2v2 mode
    uint8_t locate[2];
    uint8_t character;
    uint8_t maxlife;
    uint8_t life;
    uint8_t maxdefense;
    uint8_t defense;
    uint8_t energy;
    uint8_t specialGate;
    vector hand;
    vector deck;
    vector usecards;
    vector graveyard;
    vector metamorphosis;
    buyDeck attackSkill;
    buyDeck defenseSkill;
    buyDeck moveSkill;
    vector specialDeck;
    // Little Red Riding Hood 0
    struct {
    } redHood;

    // Snow White 1
    struct {
        vector remindPosion;
    } snowWhite;

    // sleeping Beauty 2
    struct {
        uint32_t AWAKEN_TOKEN;
        int8_t AWAKEN;  // awaken(1) or sleep(0)
        int8_t dayNightmareDrawRemind;
        int32_t atkRise;
        int32_t atkRiseTime;
    } sleepingBeauty;

    // alice 3
    struct {
        uint8_t identity;  // 0:none 1:紅心皇后 2:瘋帽子 3:柴郡貓
    } alice;

    // Mulan 4
    struct {
        uint32_t KI_TOKEN;

    } mulan;

    // kaguya 5
    struct {
    } kaguya;

    // mermaid 6
    struct {
    } mermaid;

    // Match Girl 7
    struct {
        uint32_t remindMatch;
    } matchGirl;

    // dorothy 8
    struct {
        uint32_t COMBO_TOKEN;
        bool canCombo;
    } dorothy;

    // Scheherazade 9
    struct {
    } scheherazade;
} player;
enum state { CHOOSE_CARD_TO_USE };
/*
state                         return type  meaning
CHOOSE_IDENTITY               int8_t       1:紅心皇后 2:瘋帽子 3:柴郡貓
CHOOSE_TENTACLE_LOCATION      int32_t      tentacle location
CHOOSE_SPECIAL_CARD           int32_t      special card id
CHOOSE_DESTINY_TOKEN          game         game status after set a DESTINY_TOKEN
SET_TARGET_LOCATE_TO_NEARBY   int32_t      set location(1~9)
CHOOSE_MOVE                   int32_t      choose moves
                                           (0:focus, 1-3:use basic cards(1:atk,2:def,3:mov),
                                            4:use a skill card, 5:use a special card, 6:buy a card,
                                            7:metamorphosis, 8:charactor special move,9:drop poison
                                            10:end)
BUY_CARD_TYPE                 int32_t      -1,-2,-3 meaning skill(atk/def/mov), 1,2,3,4 meaning basic(atk/def/mov/general)
BUY_CARD_LV                   int32_t      choose the card level you want to buy(lv1 2 or 3)

REMOVE_HG                     int32_t      for remove card, choose hand or graveyard(negtive:graveyard, positive:hand, value:index of card, **1 base**)
DROP_H                        int32_t      for drop card, choose hand(value:index of card, **1 base**)
USE_ATK                       int32_t      for use atk basic card, choose hand(value:index of card, **1 base**, 0 is meaning stop use)
USE_DEF                       int32_t      for use def basic card, choose hand(value:index of card, **1 base**, 0 is meaning stop use)
USE_MOV                       int32_t      for use mov basic card, choose hand(value:index of card, **1 base**, 0 is meaning stop use)
CHOOSE_MOVING_DIR             int8_t       moving face(0:left, 1:right)
USE_SKILL                     int32_t      for use skill card, choose hand(value:index of card, **1 base**)
TRIGGER_COMBO                 int8_t       0:NO 1:YES(you dont need to implement this if you didn't implement dorothy)
USEBASIC                      int32_t      for use skill card, choose basic card from hand(value:index of card, **1 base**)
KNOCKBACK                     int32_t      knockback enemy distanse(hint:check avilable value on player's last use card)
PUTTARGETPOSITION             int32_t      choose number of posion you want to push to target's deck(hint:check avilable value on player's last use card and skill that you used)
SLEEPATKHERTSELF              int32_t      sleeping beauty's skill hert herself(hint:you can check the last card you use to avoid cheating)
CHOOSECARDS                   int32_t      choose a card from nowShowingCards(return card id)
TAKE_TO_HAND                  int8_t       get card instead put it from graveyards (return 0 or 1)
CHANGE_IDENTITY               int8_t       change identity or not(check last use card to check which you will change)(return 0:no or 1:yes)
CHOOSE_MOVE_DIS               int8_t       choose the moving distanse(check last use card to confirm limit of move distanse)


*/
typedef struct _game {
    player players[4];
    int8_t now_turn_player_id;
    int8_t playerMode;  // 1v1 MODE(0) or 2v2 MODE(1)
    int8_t relicMode;
    // mermaid
    vector tentacle_TOKEN_locate;

    // 1v1 MODE is from 1 to 9
    uint32_t relic[11];
    vector relicDeck;
    vector relicGraveyard;
    buyDeck basicBuyDeck[4][3];  // attack(0) LV1~3 defense(1) LV1~3 move(2) LV1~3 generic(3)
    enum state status;
    // metadata (for using basic card)
    int32_t nowATK;
    int32_t nowDEF;
    int32_t nowMOV;
    int32_t nowUsingCardID;
    vector nowShowingCards;
} game;

#endif