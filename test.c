#include <fcntl.h>
#include <getopt.h>
#include <limits.h>
#include <math.h>
#include <regex.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#include "./client.h"
#include "./vector.h"
game g;
char characterName[10][30] = {"Red Riding Hood", "Snow White", "Sleeping Beauty", "Alice", "Mulan", "Kaguya", "Little Mermaid", "Match Girl", "Dorothy", "Scheherazade"};
char cardName[177][30] = {
    "unknown",    "LV1Attack",  "LV2Attack",  "LV3Attack",  "LV1防禦牌",    "LV2防禦牌",    "LV3防禦牌",    "LV1移動牌",    "LV2移動牌",  "LV3移動牌",  "通用牌",     "快速射擊",   "精準射擊",
    "致命狙擊",   "能量護盾",   "電流護盾",   "終極護盾",   "彈道噴射",     "火力噴射",     "暴怒噴射",     "餓狼吞噬",     "系統入侵",   "復仇之雨",   "水晶碎片",   "水晶漩渦",   "水晶風暴",
    "玷污的恩惠", "玷污的盛筵", "玷污的狂歡", "破碎的幻想", "破碎的現實",   "破碎的命運",   "七蛇之怒",     "魔鏡之雨",     "醞釀之災",   "心靈震顫",   "心靈之怒",   "心靈狂怒",   "爆裂之鎖",
    "爆裂之骨",   "爆裂之魂",   "黑暗碰觸",   "黑暗糾纏",   "黑暗絞殺",     "喚醒沉睡",     "白日夢魘",     "血脈重鑄",     "開啟牌局",   "扭轉牌局",   "操控牌局",   "魔力技巧",   "精神幻術",
    "帽子戲法",   "詭異的敏捷", "詭異的隱蔽", "詭異的詭異", "無休止的派對", "精彩的奇妙日", "遊戲盡在掌控", "不容小覷",     "勢不可擋",   "堅不可摧",   "以靜制動",   "以柔克剛",   "以弱勝強",
    "永不退縮",   "毫不留情",   "絕不饒恕",   "氣沖雲霄",   "直面混沌",     "雷霆一擊",     "領悟的光芒",   "領悟的榮耀",   "領悟的化身", "困惑的回聲", "久遠的回響", "神性的召換", "專注的自省",
    "頓悟的決心", "痛徹的淨化", "炙熱的竹刀", "注定的審判", "躁動的血性",   "海妖的召喚",   "海妖的歌聲",   "海妖的尖嘯",   "洶湧之怒",   "噴薄之怒",   "復仇之怒",   "深淵的蠶食", "深淵的入侵",
    "深淵的征服", "人魚復興",   "遠古甦醒",   "淨化之潮",   "虛幻的願望",   "隱密的期望",   "無厭的奢望",   "惡魔的祭品",   "惡魔的賭注", "惡魔的契約", "失重的靈魂", "虧欠的靈魂", "殘破的靈魂",
    "地獄烈焰",   "厄運降臨",   "貪婪詛咒",   "目標確認",   "目標鎖定",     "目標清除",     "思想刺探",     "深度搜索",     "讀取完畢",   "發現敵蹤",   "進入視野",   "使命終結",   "獅子",
    "鐵皮人",     "稻草人",     "消除夢境",   "銷毀記憶",   "扼殺存在",     "浸沒之網",     "沈迷之網",     "消融之網",     "監視之眼",   "操縱之手",   "支配之腦",   "系統刪除",   "無法自拔",
    "切斷通路",   "中毒1",      "中毒2",      "中毒3",      "火柴",         "過載燃燒",     "兜帽系統",     "變異感應",     "板載緩存",   "水晶之棺",   "墮落之劫",   "劇毒之蝕",   "至純之毒",
    "放血療法",   "血祭之禮",   "精神屏障",   "強制治療",   "砍掉她的頭",   "仙境降臨",     "我們全是瘋子", "開始我的表演", "氣慣全身",   "主宰命運",   "長驅直入",   "暴風前夕",   "懲戒時刻",
    "血色月光",   "靈性本能",   "月下沉思",   "暴風之蝕",   "神秘共鳴",     "海的女兒",     "暗潮湧動",     "痛苦的儀式",   "放縱的渴望", "魔鬼的凝視", "火焰的捉弄", "欲望的捉弄", "命運的捉弄",
    "殺戮指令",   "超越機器",   "獲准極刑",   "無所遁形",   "命運之手",     "改寫欲望",     "重組思想",     "童話編織者"};
char identityName[4][30] = {"", "紅心皇后", "瘋帽子", "柴郡貓"};
void printPlayer(player nowP) {
    printf("character: %s\n", characterName[nowP.character]);
    printf("life: %hhd/%hhd(gate:%hhd)\n", nowP.life, nowP.maxlife, nowP.specialGate);
    printf("sheild: %hhd/%hhd\n", nowP.defense, nowP.maxdefense);
    printf("energy: %hhd/25\n", nowP.energy);
    printf("locate: %hhd\n", nowP.locate[1]);
    printf("hand(%u): ", nowP.hand.SIZE);
    // printf("%llu\n", (uint64_t)((void *)&nowP.hand.SIZE) - (uint64_t)((void *)&nowP.hand));
    for (int i = 0; i < nowP.hand.SIZE; ++i) {
        if (nowP.hand.array[i] <= -1) continue;
        if (nowP.hand.array[i] >= 177) continue;

        printf("%s(%d) ", cardName[nowP.hand.array[i]], nowP.hand.array[i]);
    }
    printf("\n");

    printf("graveyard(%d): ", nowP.graveyard.SIZE);
    for (int i = 0; i < nowP.graveyard.SIZE; ++i) {
        if (nowP.graveyard.array[i] <= -1) continue;
        if (nowP.graveyard.array[i] >= 177) continue;
        printf("%s(%d) ", cardName[nowP.graveyard.array[i]], nowP.graveyard.array[i]);
    }
    printf("\n");

    printf("using cards: ");
    for (int i = 0; i < nowP.usecards.SIZE; ++i) {
        if (nowP.usecards.array[i] <= -1) continue;
        if (nowP.usecards.array[i] >= 177) continue;
        printf("%s(%d) ", cardName[nowP.usecards.array[i]], nowP.usecards.array[i]);
    }
    printf("\n");

    printf("attack skill buy deck: ");
    for (int i = 0; i < nowP.attackSkill.SIZE; ++i) {
        if (nowP.attackSkill.array[i] == -1) continue;
        printf("%s(%d) ", cardName[nowP.attackSkill.array[i]], nowP.attackSkill.array[i]);
    }
    printf("\n");

    printf("defense skill buy deck: ");
    for (int i = 0; i < nowP.defenseSkill.SIZE; ++i) {
        if (nowP.defenseSkill.array[i] == -1) continue;
        printf("%s(%d) ", cardName[nowP.defenseSkill.array[i]], nowP.defenseSkill.array[i]);
    }
    printf("\n");

    printf("move skill buy deck: ");
    for (int i = 0; i < nowP.moveSkill.SIZE; ++i) {
        if (nowP.moveSkill.array[i] == -1) continue;
        printf("%s(%d) ", cardName[nowP.moveSkill.array[i]], nowP.moveSkill.array[i]);
    }
    printf("\n");

    printf("special skill deck: ");
    for (int i = 0; i < nowP.specialDeck.SIZE; ++i) {
        if (nowP.specialDeck.array[i] == -1) continue;
        printf("%s(%d) ", cardName[nowP.specialDeck.array[i]], nowP.specialDeck.array[i]);
    }
    printf("\n");

    printf("twist: ");
    for (int i = 0; i < nowP.metamorphosis.SIZE; ++i) {
        if (nowP.metamorphosis.array[i] == -1) continue;

        printf("%s(%d) ", cardName[nowP.metamorphosis.array[i]], nowP.metamorphosis.array[i]);
    }
    printf("\n");
    printf("character special:\n");
    int i;
    switch (g.players[0].character) {
        case 0:
            for (i = 0; i < 3; ++i) {
                if (nowP.redHood.saveCard[i] < 0) {
                    printf("unknown(%d) ", nowP.redHood.saveCard[i]);
                }
                printf("%s(%d) ", cardName[nowP.redHood.saveCard[i]], nowP.redHood.saveCard[i]);
            }
            printf("\n");
            break;
        case 1:
            printf("remind Posion(%ld):", nowP.snowWhite.remindPosion.SIZE);
            for (i = 0; i < nowP.snowWhite.remindPosion.SIZE; ++i) {
                printf("%d ", nowP.snowWhite.remindPosion.array[i] - 130);
            }
            printf("\n");
            break;
        case 2:
            if (nowP.sleepingBeauty.AWAKEN) printf("AWAKENED\n");
            printf("AWAKEN TOKEN: %d\n", nowP.sleepingBeauty.AWAKEN_TOKEN);
            printf("\"and they woke up\" remind count:%d\n", nowP.sleepingBeauty.dayNightmareDrawRemind);
            printf("atk rise: %d(remind %d time)", nowP.sleepingBeauty.atkRise, nowP.sleepingBeauty.atkRiseTime);
            if (nowP.sleepingBeauty.usedmeta1) printf("used twist \"BLOODLETTING\"");
            if (nowP.sleepingBeauty.usedmeta2) printf("used twist \"BLOOD RITE\"");
            break;
        case 3:
            printf("now identity: %s(%d)\n", identityName[nowP.alice.identity], nowP.alice.identity);
            printf("basic card rise: %d\n", nowP.alice.riseBasic);
            printf("restarted time: %d\n", nowP.alice.havedrestart);
            if (nowP.alice.restartTurn) printf("will restart\n");
            break;
        case 4:
            printf("QI TOKEN: %d/12\n", nowP.mulan.KI_TOKEN);
            printf("extra card you can draw by spend QI: %d\n", nowP.mulan.extraCard);
            printf("extra card you can draw: %d\n", nowP.mulan.extraDraw);
            break;
        case 5:
            if (nowP.kaguya.useDefenseAsATK) printf("used SWIFT REPRISAL\n");
            if (nowP.kaguya.useMoveTarget) printf("used UNCANNY INSTINCT\n");

            break;
        case 6:

            break;
        case 7:
            printf("remind Match: %d\n", nowP.matchGirl.remindMatch);
            if (nowP.matchGirl.pushedMatch) printf("used special rule\n");
            break;
        case 8:
            printf("COMBO TOKEN:%d/12\n", nowP.dorothy.COMBO_TOKEN);
            if (nowP.dorothy.canCombo) printf("can COMBO\n");

            break;
        case 9:
            for (i = 0; i < nowP.scheherazade.destiny_TOKEN_locate.SIZE; ++i) {
                if (nowP.scheherazade.destiny_TOKEN_type.array[i] == 1) {
                    printf("\033[34m");
                } else if (nowP.scheherazade.destiny_TOKEN_type.array[i] == 2) {
                    printf("\033[31m");
                }
                printf("%d", nowP.scheherazade.destiny_TOKEN_locate.array[i]);
                printf("\033[0m ");
            }
            printf("now selecting TOKEN: %d\n", nowP.scheherazade.selectToken);
            break;
        default:
            break;
    }
}
void printGame() {
    printf("now player: %d\n", g.now_turn_player_id);

    printf("player 0: \n");
    printPlayer(g.players[0]);
    if (g.players[0].character == 6) {
        printf("tantacle locate:");
        for (int i = 0; i < g.tentacle_TOKEN_locate.SIZE; ++i) {
            printf("%d ", g.tentacle_TOKEN_locate.array[i]);
        }
        printf("\n");
    }
    printf("player 1: \n");
    printPlayer(g.players[1]);
    if (g.players[1].character == 6) {
        printf("tantacle locate:");
        for (int i = 0; i < g.tentacle_TOKEN_locate.SIZE; ++i) {
            printf("%d ", g.tentacle_TOKEN_locate.array[i]);
        }
        printf("\n");
    }
    printf("ATK 1:%d 2:%d 3:%d\n", g.basicBuyDeck[0][0].SIZE, g.basicBuyDeck[0][1].SIZE, g.basicBuyDeck[0][2].SIZE);
    printf("DEF 1:%d 2:%d 3:%d\n", g.basicBuyDeck[1][0].SIZE, g.basicBuyDeck[1][1].SIZE, g.basicBuyDeck[1][2].SIZE);
    printf("MOV 1:%d 2:%d 3:%d\n", g.basicBuyDeck[2][0].SIZE, g.basicBuyDeck[2][1].SIZE, g.basicBuyDeck[2][2].SIZE);
    printf("WILD :%d\n", g.basicBuyDeck[3][0].SIZE);
    printf("now atk: %d\n", g.nowATK);
    printf("now def: %d\n", g.nowDEF);
    printf("now mov: %d\n", g.nowMOV);
    printf("total damage: %d\n", g.totalDamage);
    printf("now using card: %s(%d)\n", cardName[g.nowUsingCardID], g.nowUsingCardID);
}
int main(int argc, char **argv) {
    init_client();
    int8_t doneCharacter[10] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
    send_data(doneCharacter, 10);
    while (1) {
        receive(&g);
        int8_t temp8;
        int32_t temp32;
        bool chooseType = 0;
        printGame();
        switch (g.status) {
            case CHOOSE_IDENTITY:
                printf("CHOOSE_IDENTITY(1:紅心皇后 2:瘋帽子 3:柴郡貓)\n");
                chooseType = 1;
                break;
            case CHOOSE_TENTACLE_LOCATION:
                printf("CHOOSE_TENTACLE_LOCATION(tentacle location)\n");
                break;
            case CHOOSE_SPECIAL_CARD:
                printf("CHOOSE_SPECIAL_CARD(special card id)\n");
                break;
            case APPEND_DESTINY_TOKEN:
                printf("APPEND_DESTINY_TOKEN(-1,-2,-3 meaning skill(atk/def/mov), 1~10 meaning basic(atk/def/mov/general))\n");
                break;
            case SET_TARGET_LOCATE_TO_NEARBY:
                printf("SET_TARGET_LOCATE_TO_NEARBY(set location(1~9))\n");
                break;
            case CHOOSE_MOVE:
                printf(
                    "CHOOSE_MOVE\n(choose moves\n"
                    "(0:focus, 1-3:use basic cards(1:atk,2:def,3:mov),\n"
                    "4:use a skill card, 5:use a special card, 6:buy a card,\n"
                    "7:metamorphosis, 8:charactor special move,9:drop poison\n"
                    "10:end))\n");
                break;
            case BUY_CARD_TYPE:
                printf("BUY_CARD_TYPE(-1,-2,-3 meaning skill(atk/def/mov), 1~10 meaning basic(atk/def/mov/general))\n");
                break;
            case REMOVE_HG:
                printf("REMOVE_HG(for remove card, choose hand or graveyard(negtive:graveyard, positive:hand, value:index of card, **1 base**)\n");
                break;
            case DROP_H:
                printf("DROP_H(for drop card, choose hand(value:index of card, **1 base**))\n");
                break;
            case USE_ATK:
                printf("USE_ATK(for use atk basic card, choose hand(value:index of card, **1 base**, 0 is meaning stop use))\n");
                break;
            case USE_DEF:
                printf("USE_DEF(for use def basic card, choose hand(value:index of card, **1 base**, 0 is meaning stop use))\n");
                break;
            case USE_MOV:
                printf("USE_MOV(for use mov basic card, choose hand(value:index of card, **1 base**, 0 is meaning stop use))\n");
                break;
            case USE_POSION:
                printf("USE_POSION(for use posion card, choose hand(value:index of card, **1 base**))\n");
                break;
            case CHOOSE_MOVING_DIR:
                printf("CHOOSE_MOVING_DIR(moving face(0:left, 1:right))\n");
                chooseType = 1;
                break;
            case USE_SKILL:
                printf("USE_SKILL(for use skill card, choose hand(value:index of card, **1 base**))\n");
                break;
            case TRIGGER_COMBO:
                printf("TRIGGER_COMBO(0:NO 1:YES)\n");
                chooseType = 1;
                break;
            case USEBASIC:
                printf("USEBASIC(for use skill card, choose basic card from hand(value:index of card, **1 base**))\n");
                break;
            case KNOCKBACK:
                printf("KNOCKBACK(knockback enemy distanse(hint:check avilable value on player's last use card))\n");
                break;
            case MOVE_TARGET:
                printf("MOVE_TARGET(move target(return locate after move))\n");
                break;
            case PUT_TARGET_POSITION:
                printf("PUT_TARGET_POSITION(choose number of posion you want to push to target's deck(hint:check avilable value on player's last use card and skill that you used))\n");
                break;
            case SHUFFLE_POSION_TO_DECK:
                printf("SHUFFLE_POSION_TO_DECK(shuffle posion to deck instead of put into graveyard(1:yes, 0:no))\n");
                chooseType = 1;
                break;
            case CHOOSE_CARD_BACK:
                printf("CHOOSE_CARD_BACK(shuffle back the target card from graveyard to deck(0:cancel, value:index of card, **1 base**))\n");
                break;
            case SLEEP_ATK_HERTSELF:
                printf("SLEEP_ATK_HERTSELF(sleeping beauty's skill hert herself(hint:you can check the last card you use to avoid cheating))\n");
                break;
            case USE_AWAKEN_TOKEN:
                printf("USE_AWAKEN_TOKEN(use awaken token when using skill(at most 3))\n");
                chooseType = 1;
                break;
            case LOST_LIFE_FOR_USESKILL:
                printf("LOST_LIFE_FOR_USESKILL(sleeping beauty's metamorphosis, (choose lose 0(not trigger),2,4,6 life))\n");
                chooseType = 1;
                break;
            case RECYCLE_CARD:
                printf("RECYCLE_CARD(sleeping beauty's metamorphosis, (choose a card from graveyard(0 is not trigger, 1 base)))\n");
                break;
            case CHOOSECARDS:
                printf("CHOOSECARDS(choose a card from nowShowingCards(return card id))\n");
                break;
            case TAKE_TO_HAND:
                printf("TAKE_TO_HAND(get card instead put it from graveyards (return 0 or 1))\n");
                chooseType = 1;
                break;
            case CHANGE_IDENTITY:
                printf("CHANGE_IDENTITY(change identity or not(check last use card to check which you will change)(return 0:no or 1:yes))\n");
                chooseType = 1;
                break;
            case CHOOSE_MOVE_DIS:
                printf("CHOOSE_MOVE_DIS(choose the moving distanse(check last use card to confirm limit of move distanse))\n");
                chooseType = 1;
                break;
            case SEND_CARD:
                printf("SEND_CARD(for sending card to target, choose hand or graveyard(negtive:graveyard, positive:hand, value:index of card, **1 base**, 0 is stop sending))\n");
                break;
            case GET_KI:
                printf("GET_KI(get ki by drop defense card or general card(return index of card, **1 base**, 0 is meaning not use))\n");
                break;
            case SPEND_KI_FOR_ATK:
                printf("SPEND_KI_FOR_ATK(use ki for atk metamorphosis (return the number of KI you want to use))\n");
                break;
            case SPEND_KI_FOR_DRAW:
                printf("SPEND_KI_FOR_DRAW(use ki for defense skill (return the number of KI you want to use))\n");
                break;
            case SPEND_KI_FOR_MOV:
                printf("SPEND_KI_FOR_MOV(use ki for move metamorphosis (return the number of KI you want to use))\n");
                break;
            case DROP_ONE_DRAW_ONE:
                printf("DROP_ONE_DRAW_ONE(for drop card, choose hand(value:index of card, **1 base**, 0 is not do it))\n");
                break;
            case PUT_TO_ANOTHER_SIDE:
                printf("PUT_TO_ANOTHER_SIDE(choose move target to another side or not)\n");
                chooseType = 1;
                break;
            case CHOOSE_MOVE_NEARBY:
                printf("CHOOSE_MOVE_NEARBY(move to the locate next to target(-1:left, 1:right, 0:no move))\n");
                chooseType = 1;
                break;
            case KEEP_OR_BACK:
                printf("KEEP_OR_BACK(keep the card or drop it(1:keep, 0:drop, the card store in nowusingCardID))\n");
                chooseType = 1;
                break;
            case LOST_LIFE_FOR_REMOVECARD:
                printf("LOST_LIFE_FOR_REMOVECARD(kaguya's skill, (1:lost, 0:no))\n");
                chooseType = 1;
                break;
            case KAGUYA_MOVE_TARGET:
                printf("KAGUYA_MOVE_TARGET(kaguya's move metamorphosis(-n:left, n:right, n is distance))\n");
                chooseType = 1;
                break;
            case MOVE_TO_TANTACLE:
                printf("MOVE_TO_TANTACLE(locate you choose(should in tentacle_TOKEN_locate or your original locate))\n");
                break;
            case CHOOSE_TANTACLE:
                printf("CHOOSE_TANTACLE(choose a tantacle)\n");
                break;
            case MOVE_TANTACLE:
                printf("MOVE_TANTACLE(move a tantacle you choose(locate after move tantacle))\n");
                break;
            case DROPCARD_MOVE_TANTACLE:
                printf("DROPCARD_MOVE_TANTACLE(drop a card for moving tantacle(value:index of card, **1 base**))\n");
                break;
            case SPEND_ENERGY:
                printf("SPEND_ENERGY(spend energy for rise the atk(0 is meaning not use))\n");
                break;
            case SPEND_LIFE:
                printf("SPEND_LIFE(spend life for draw card(0 is meaning not use))\n");
                break;
            case RECYCLE_MATCH:
                printf("RECYCLE_MATCH(get back the match from target's graveyard(check the max value you can recycle from target's graveyard and the card you use))\n");
                break;
            case DROP_CARD:
                printf("DROP_CARD(choose a card to drop/save(0 is end, 1 base))\n");
                break;
            case SPEND_COMBO:
                printf("SPEND_COMBO(spend combo token for ultra skill(send number of tokens you use))\n");
                break;
            case FLIP_TOKEN_TO_RED:
                printf("FLIP_TOKEN_TO_RED(-1,-2,-3 meaning skill(atk/def/mov), 1~10 meaning basic(atk/def/mov/general), 0 is not flip)\n");
                chooseType = 1;
                break;
            case CHOOSE_TOKEN:
                printf("CHOOSE_TOKEN(choose a destiny token for action(index of tokens, -1 is give up))\n");
                chooseType = 1;
                break;
            case TOKEN_GOAL:
                printf("TOKEN_GOAL(choose location of the token you choose for moving(-1,-2,-3 meaning skill(atk/def/mov), 1~10 meaning basic(atk/def/mov/general)))\n");
                chooseType = 1;
                break;
            case GET_ULTRA:
                printf("GET_ULTRA(choose a special card to hand when your life lower than gate first time)\n");
                chooseType = 1;
                break;
            case USE_METAMORPHOSIS:
                printf("USE_METAMORPHOSIS(trigger a active metamorphosis(return index of metamorphosis, 0 base))\n");
                break;
            default:
                destroy_client();
                return 0;
        }
        if (chooseType) {
            scanf("%hhd", &temp8);
            send_data(&temp8, sizeof(temp8));
        } else {
            scanf("%d", &temp32);
            send_data(&temp32, sizeof(temp32));
        }
    }
    destroy_client();
}