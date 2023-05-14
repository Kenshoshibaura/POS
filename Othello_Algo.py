#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
import numpy as np
import FunctionModules as fm
import os
import time
from tqdm import tqdm

columnList = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
rowList = {'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7}
Inv_columnList = {v:k for k, v in columnList.items()}
Inv_rowList = {v:k for k, v in rowList.items()}

Point = [50,-20,10,3,3,10,-20,50,-20,-40,-1,-1,-1,-1,-40,-20,
        10,-1,3,1,1,3,-1,10,3,-1,1,0,0,1,-1,3,
        3,-1,1,0,0,1,-1,3,10,-1,3,1,1,3,-1,10,
        -20,-40,-1,-1,-1,-1,-40,-20,50,-20,10,3,3,10,-20,50]

def Evaluation_board2(get_board_pattern,turn,enable_count):
    score = 0
    stone,blank = 0,0
    stone_dif = 0
    weight_dif = 0
    for y in range(0,8):
        for x in range(0,8):
            if str(get_board_pattern[y][x]) == str(turn):
                stone_dif += 1
                stone += 1
                weight_dif += Point[y*8+x]
            elif str(get_board_pattern[y][x]) == "0":
                blank += 1
            else:
                stone_dif -= 1
                stone += 1
                weight_dif -= Point[y*8+x]
    #print("Point:"+str(my_weight)+","+str(your_weight))
    if stone < 20: #序盤 A:最大20石差 * 3 = -60 ~ 60 B:最大20候補 * 6 = -6 ~ 108 C:重み 最大180 // 4 = -45 ~ 45 D:確定最大20石 * ? = -?? ~ ??
        score = (stone_dif * 3) + ((enable_count - 2) * 6) + (weight_dif // 4)
    elif stone < 50: #中盤 A:最大50石差 * 2 = -100 ~ 100 B:最大20候補 * 12 = -36 ~ 216 C:重み 最大320 / 2 = -160 ~ 160 D:確定最大50石 * ? = -?? ~ ??
        score = (stone_dif * 2) + ((enable_count - 2) * 12) + (weight_dif // 2)
    elif stone < 58: #終盤A A:最大55石差 * 4 = -220 ~ 220 B:最大20候補 * 3 = -3 ~ 54 C:重み 最大300? / 6 = -50 ~ 50 D:確定最大55石 * ? = -?? ~ ??
        score = (stone_dif * 4) + ((enable_count - 2) * 3) + (weight_dif // 6)
    elif stone < 62: #終盤B A:最大60石差 * 5 = -300 ~ 300 D:確定最大60石 * ? = -?? ~ ??
        score = (stone_dif * 5)
    else: #最終盤 A:最大64石差 * 10 = -640 ~ 640 完成済み
        score = (stone_dif * 10)

    #print("stone:"+str(stone)+" enable:"+str(enable_count)+" + score:"+str(score))
    return score
def AB2(now_board,my_turn,next_posi_enable,search_count,search,file_search):
    your_turn = change_turn(my_turn)
    my_turn_score = -100000
    my_turn_select = ""
    if search == search_count:
        text = tqdm(next_posi_enable)
    else:
        text = next_posi_enable
    for m,my_candidate in enumerate(text):
        demo_after_me = get_prediction_board(now_board,my_turn,my_candidate)
        demo_after_me_2 = np.array(demo_after_me)
        your_enable = search_enable(demo_after_me_2,your_turn)
        if not your_enable:
            your_enable.append('pass')
        your_turn_score = 100000
        score_pre = -100000
        for y,your_candidate in enumerate(your_enable):
            demo_after_you = get_prediction_board(demo_after_me_2,your_turn,your_candidate)
            demo_after_you_2 = np.array(demo_after_you)
            my_enable = search_enable(demo_after_you_2,my_turn)
            if not my_enable:
                my_enable.append('pass')
            if search_count > 1:
                score_pre,select_new = AB2(demo_after_you_2,my_turn,my_enable,search_count-1,search,file_search)
            elif search_count <= 1:
                for l,last_candidate in enumerate(my_enable):
                    demo_last = get_prediction_board(demo_after_me_2,my_turn,last_candidate)
                    demo_last_2 = np.array(demo_last)
                    last_enable = search_enable(demo_last_2,your_turn)
                    #score_new = Evaluation_board(demo_last,my_turn)
                    score_new = Evaluation_board2(demo_last,my_turn,len(last_enable))
                    if score_new > score_pre:
                        score_pre = score_new
                    if score_pre > your_turn_score:
                        break
            if score_pre < your_turn_score:
                your_turn_score = score_pre
            if your_turn_score < my_turn_score:
                break
        if search == search_count:
            addwrite(file_search,my_candidate,your_turn_score)
        if your_turn_score > my_turn_score:
            my_turn_score = your_turn_score
            my_turn_select = my_candidate
    return my_turn_score,my_turn_select

class AI_choice:

    def __init__(self):
        pass

    def get_next_posi(self, diagrams, next_dia_all, next_diaList, turn):
        #print("---"+str(turn)+"の次の手の探索を開始します---")
        #着手可能手抽出 next_posi_enable
        next_posi_enable = search_enable_first(next_dia_all,turn)
        #現在の盤面取得・変換 get_board_pattern,ow_board_pattern
        get_board_pattern,now_board_pattern = board_conversion(next_dia_all)

        #検索するファイル名作成 file_search
        file_search = "brain/" + str(turn) + "/" + now_board_pattern + ".csv"

        #ファイルが存在するか探索
        if (os.path.exists(file_search)) == True:
            start = time.time()
            score,select = search_maxscore(file_search)
            finish = time.time() - start
            print("探索成功："+select+"を着手します "+str(score)+" time:"+str(finish))

        else: #新規盤面(ファイルが存在しない)場合 MiniMax探索を実行
            start = time.time()
            score,select = AB2(get_board_pattern,turn,next_posi_enable,2,2,file_search)
            finish = time.time() - start
            print("新規盤面："+select+"を着手します score(AB):"+str(score)+" time:"+str(finish))

        return select

class random_choice:

    def __init__(self):
        pass

    def get_next_posi(self, diagrams, next_dia_all, next_diaList, turn):
        next_posi_enable = []
        for i in range(0,8):
            for j in range(0,8):
                if next_dia_all[i,j] == turn + 4:
                    next_posi_enable.append(str(Inv_columnList[j])+str(Inv_rowList[i]))
        select = random.choice(next_posi_enable)
        return select
class max_choice:

    def __init__(self):
        pass

    def get_next_posi(self, diagrams, next_dia_all, next_diaList, turn):
        next_count = []
        for next_dia in next_diaList:
            next_count.append((next_dia==turn).sum() + (next_dia==turn+2).sum() + (next_dia==turn+4).sum())

        next_count = np.array(next_count)
        targets = np.where(next_count == next_count.max())

        target = random.choice(targets[0])
        next_dia = next_diaList[target]
        tmp = np.where(next_dia == turn+4)

        next_posi = str(Inv_columnList[tmp[1][0]])+str(Inv_rowList[tmp[0][0]])

        return next_posi
