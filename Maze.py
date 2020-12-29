# -*- coding: utf-8 -*-

from tkinter import Button
from tkinter import Tk
from tkinter import Canvas

import numpy as np


class Maze(object):

    def __init__(self):
        self.blockcolorIndex = 0
        self.blockcolor = ['black', 'green', 'red', 'purple']  # 设置障碍为黑色，起点为绿色 终点为红色，路径为紫色
        self.mapStatus = np.ones((8, 8), dtype=int)  # 地图状态数组（全0数组） 1无障碍 0障碍
        self.startpoint = 'start'  # 起点
        self.endpoint = 'end'  # 终点
        self.selectedStart = False  # 是否选了起点 默认否
        self.selectedEnd = False  # 是否选了终点 默认否
        self.openList = []  # open表
        self.closeList = []  # close表
        self.isOK = False  # 是否已经结束
        self.route = []  # 路径列表

        self.root = Tk()
        self.root.title('A*算法实现迷宫')
        self.root.geometry("1050x600+200+50") #设置窗口大小


        self.btn_obstacle = Button(self.root, text="选择障碍", command=self.selectobstacle)
        self.btn_obstacle.pack(side='left',anchor='n')
        self.btn_start = Button(self.root, text="选择起点", command=self.selectstart)
        self.btn_start.pack(side='left',anchor='n')
        self.btn_end = Button(self.root, text="选择终点", command=self.selectend)
        self.btn_end.pack(side='left',anchor='n')
        self.btn_pathfinding = Button(self.root, text="开始寻路", command=self.selectaction)
        self.btn_pathfinding.pack(side='left',anchor='n')
        self.btn_restart = Button(self.root, text="重新游戏", command=self.selectrestart)
        self.btn_restart.pack(side='left',anchor='n')
        self.canvas = Canvas(self.root, width=500, height=500, bg="white")
        self.canvas.pack(side='left')
        for i in range(1, 10):
            self.canvas.create_line(50, 50 * i, 450, 50 * i)  # 横线
            self.canvas.create_line(50 * i, 50, 50 * i, 450)  # 竖线
        self.canvas.bind("<Button-1>", self.drawMapBlock)# 将画布绑定到迷宫区域
        self.root.mainloop()

    #重新开始
    def selectrestart(self):
        self.mapStatus = np.ones((8, 8), dtype=int)  # 地图状态数组（全0数组） 1无障碍 0障碍
        self.startPoint = 'start'
        self.endpoint = 'end'
        self.selectedStart = False  # 是否选了起点 默认否
        self.selectedEnd = False  # 是否选了终点 默认否
        self.openList = []  # open表
        self.closeList = []  # close表
        self.isOK = False  # 是否已经结束
        self.route = []
        self.canvas.destroy()
        self.canvas = Canvas(self.root, width=500,height=500, bg="white")
        self.canvas.pack(side='left')
        for i in range(1, 10):
            self.canvas.create_line(50, 50 * i, 450, 50 * i)  # 横线
            self.canvas.create_line(50 * i, 50, 50 * i, 450)  # 竖线
        self.canvas.bind("<Button-1>", self.drawMapBlock)# 将画布绑定到迷宫区域

    #颜色设置
    def selectobstacle(self):
        self.blockcolorIndex = 0  #黑色
    def selectstart(self):
        if not self.selectedStart:
            self.blockcolorIndex = 1  # 绿色
        else:
            self.blockcolorIndex = 0  # 黑色
    def selectend(self):
        if not self.selectedEnd:
            self.blockcolorIndex = 2  # 红色
        else:
            self.blockcolorIndex = 0  # 黑色
    def selectaction(self):
        self.blockcolorIndex = 0  # 黑色
        self.AstarMap()
        self.route.pop(-1)
        self.route.pop(0)
        for i in self.route:
            self.canvas.create_rectangle((i.x + 1) * 50, (i.y + 1) * 50, (i.x + 2) * 50, (i.y + 2) * 50, fill='purple')

    def AstarMap(self):
        # 将起点放到open表中
        self.openList.append(self.startPoint)
        while (not self.isOK):
            # 先检查终点是否在open表中 ，没有继续，有则结束
            if self.inOpenList(self.endpoint) != -1:  # 在open表中
                self.isOK = True  #
                self.end = self.openList[self.inOpenList(self.endpoint)]
                self.route.append(self.end)
                self.te = self.end
                while (self.te.parentPoint != 0):
                    self.te = self.te.parentPoint
                    self.route.append(self.te)
            else:
                self.sortOpenList()  # 将估值最小的节点放在index = 0
                Minnode = self.openList[0]  # 估值最小节点
                self.openList.pop(0)
                self.closeList.append(Minnode)
                # 开拓 Minnode节点，并放到open 表
                if Minnode.x - 1 >= 0:  # 没有越界
                    if (self.mapStatus[Minnode.y][Minnode.x - 1]) != 0:  # 非障碍,可开拓
                        self.temp1 = mapPoint(Minnode.x - 1, Minnode.y, Minnode.distanceStart + 1,
                                              self.endpoint.x, self.endpoint.y, Minnode)
                        if self.inOpenList(self.temp1) != -1:  # open表存在相同的节点
                            if self.temp1.evaluate() < self.openList[self.inOpenList(self.temp1)].evaluate():
                                self.openList[self.inOpenList(self.temp1)] = self.temp1
                        elif self.inCloseList(self.temp1) != -1:  # 否则查看close表是否存在相同的节点（存在）
                            if self.temp1.evaluate() < self.closeList[self.inCloseList(self.temp1)].evaluate():
                                self.closeList[self.inCloseList(self.temp1)] = self.temp1
                        else:  # open 、 close表都不存在 temp1
                            self.openList.append(self.temp1)

                if Minnode.x + 1 < 8:
                    if (self.mapStatus[Minnode.y][Minnode.x + 1]) != 0:  # 非障碍,可开拓
                        self.temp2 = mapPoint(Minnode.x + 1, Minnode.y, Minnode.distanceStart + 1,
                                              self.endpoint.x, self.endpoint.y, Minnode)
                        if self.inOpenList(self.temp2) != -1:  # open表存在相同的节点
                            if self.temp2.evaluate() < self.openList[self.inOpenList(self.temp2)].evaluate():
                                self.openList[self.inOpenList(self.temp2)] = self.temp2
                        elif self.inCloseList(self.temp2) != -1:  # 否则查看close表是否存在相同的节点（存在）
                            if self.temp2.evaluate() < self.closeList[self.inCloseList(self.temp2)].evaluate():
                                self.closeList[self.inCloseList(self.temp2)] = self.temp2
                        else:
                            self.openList.append(self.temp2)

                if Minnode.y - 1 >= 0:
                    if (self.mapStatus[Minnode.y - 1][Minnode.x]) != 0:  # 非障碍,可开拓
                        self.temp3 = mapPoint(Minnode.x, Minnode.y - 1, Minnode.distanceStart + 1,
                                              self.endpoint.x, self.endpoint.y, Minnode)
                        if self.inOpenList(self.temp3) != -1:  # open表存在相同的节点
                            if self.temp3.evaluate() < self.openList[self.inOpenList(self.temp3)].evaluate():
                                self.openList[self.inOpenList(self.temp3)] = self.temp3
                        elif self.inCloseList(self.temp3) != -1:  # 否则查看close表是否存在相同的节点（存在）
                            if self.temp3.evaluate() < self.closeList[self.inCloseList(self.temp3)].evaluate():
                                self.closeList[self.inCloseList(self.temp3)] = self.temp3
                        else:
                            self.openList.append(self.temp3)

                if Minnode.y + 1 < 8:
                    if (self.mapStatus[Minnode.y + 1][Minnode.x]) != 0:  # 非障碍,可开拓
                        self.temp4 = mapPoint(Minnode.x, Minnode.y + 1, Minnode.distanceStart + 1,
                                              self.endpoint.x, self.endpoint.y, Minnode)

                        if self.inOpenList(self.temp4) != -1:  # open表存在相同的节点
                            if self.temp4.evaluate() < self.openList[self.inOpenList(self.temp4)].evaluate():
                                self.openList[self.inOpenList(self.temp4)] = self.temp4
                        elif self.inCloseList(self.temp4) != -1:  # 否则查看close表是否存在相同的节点（存在）
                            if self.temp4.evaluate() < self.closeList[self.inCloseList(self.temp4)].evaluate():
                                self.closeList[self.inCloseList(self.temp4)] = self.temp4
                        else:
                            self.openList.append(self.temp4)

    def drawMapBlock(self, event):
        x, y = event.x, event.y
        if (50 <= x <= 450) and (50 <= y <= 450):
            i = int((x // 50) - 1)
            j = int((y // 50) - 1)
            # 记录下起止点，并不能选择多个起点或者多个终点
            if self.blockcolorIndex == 1 and not self.selectedStart:
                self.startPoint = mapPoint(i, j, 0, 0, 0, 0)
                self.selectedStart = True
                self.canvas.create_rectangle((i + 1) * 50, (j + 1) * 50, (i + 2) * 50, (j + 2) * 50,
                                             fill=self.blockcolor[self.blockcolorIndex])
                self.blockcolorIndex = 0
            elif self.blockcolorIndex == 2 and not self.selectedEnd:
                self.endpoint = mapPoint(i, j, 0, 0, 0, 0)
                self.selectedEnd = True
                self.canvas.create_rectangle((i + 1) * 50, (j + 1) * 50, (i + 2) * 50, (j + 2) * 50,
                                             fill=self.blockcolor[self.blockcolorIndex])
                self.blockcolorIndex = 0
            else:
                self.canvas.create_rectangle((i + 1) * 50, (j + 1) * 50, (i + 2) * 50, (j + 2) * 50,
                                             fill=self.blockcolor[self.blockcolorIndex])
                self.mapStatus[j][i] = self.blockcolorIndex

    # 检查终点是否在open表中
    def endInOpenList(self):
        for i in self.openList:
            if self.endpoint[0] == i.x and self.endpoint[1] == i.y:
                return True
        return False

    # 将节点加进open表前，检查该节点是否在open表中
    def inOpenList(self, p1):
        for i in range(0, len(self.openList)):
            if p1.judge(self.openList[i]):
                return i
        return -1

    # 将节点加进open表前，检查该节点是否在close表中
    # 若在返回索引，不在返回-1
    def inCloseList(self, p1):
        for i in range(0, len(self.closeList)):
            if p1.judge(self.closeList[i]):
                return i
        return -1

    # 估值最小节点排在index = 0
    def sortOpenList(self):
        if len(self.openList) > 0:
            if len(self.openList) > 1:
                for i in range(1, len(self.openList)):
                    if self.openList[i].evaluate() < self.openList[0].evaluate():
                        self.t = self.openList[0]
                        self.openList[0] = self.openList[i]
                        self.openList[i] = self.t


class mapPoint(object):
    def __init__(self, x, y, distanceStart, endX, endY, parentPoint):
        self.x = x
        self.y = y#当前节点的坐标位置
        self.distanceStart = distanceStart#记录下由起点走到该节点的耗散值（由起点走到该节点的路径的距离，该节点的下一个节点会加1）
        self.endX = endX
        self.endY = endY#目标节点
        self.parentPoint = parentPoint  # 前一个节点

    def evaluate(self):#评估函数
        return self.distanceStart + abs(self.x - self.endX) + abs(self.y - self.endY)

    def judge(self, point):#判断两个节点是否是同一个位置
        if point.x == self.x and point.y == self.y:
            return True
        else:
            return False


def main():
 Maze()


if __name__ == '__main__':
    main()