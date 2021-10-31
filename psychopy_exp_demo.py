# -*- coding: utf-8 -*-
from psychopy import visual, core, event, gui
import random
import openpyxl  # 导入所需的包

event.globalKeys.add(
    key="escape", func=core.quit, name="shutdown"
)  # 全局退出键为键盘左上角的Esc，即Escape
n, m, p = 0, 0, 0
demo_order = list(range(10))  # 练习10个trial
order = list(range(20))  # 正式实验使用trial的数量，这里以20为例
random.shuffle(demo_order)
random.shuffle(order)  # 把练习和正式实验的出现顺序随机变换
demo_judge_list = []
judge_list = []
rowlist = []  # 设置三个空列表，前两个用来记录被试的选择，最后一个记录实验最终数据
file = openpyxl.Workbook()  # 生成一个excel文件，sheet名字为test，分别记录启动项、目标项、正确答案、被试的选择、反应时间
sheet = file.active
sheet.title = "test"
sheet["A1"] = "prime"
sheet["B1"] = "target"
sheet["C1"] = "value"
sheet["D1"] = "judgement"
sheet["E1"] = "reaction_time"
demo_prime_list = ["#练习时启动项的列表"]
demo_target_list = ["#练习时目标项的列表"]
demo_value_list = ["#练习时正确答案的列表"]
prime_list = ["#正式实验时启动项的列表"]
target_list = ["#正式实验时目标项的列表"]
value_list = ["#正式实验时正确答案的列表"]
intro_text = u"""实验指导语"""
practice_end_text = u"""练习结束后的提示"""
rest_text = u"""休息语"""
end_text = u"""实验结束语"""  # 使用unicode防止出现文字乱码


def intro():  # 显示实验指导语的函数
    intro_t = visual.TextStim(
        win,
        text=intro_text,
        height=0.09,  # 文本、字体大小、位置坐标、颜色、加粗、斜体
        pos=(0.0, 0.0),
        color="black",
        bold=False,
        italic=False,
    )
    intro_t.draw()
    win.flip()
    core.wait(0)
    event.waitKeys(keyList=["q"])  # 按Q键结束指导语，进入实验


def rest():  # 显示休息语的函数
    rest_t = visual.TextStim(
        win,
        text=rest_text,
        height=0.09,
        pos=(0.0, 0.0),
        color="black",
        bold=False,
        italic=False,
    )
    rest_t.draw()
    win.flip()
    core.wait(0)
    event.waitKeys()  # 按任意键退出


def end():  # 显示实验结束语的函数
    end_t = visual.TextStim(
        win,
        text=end_text,
        height=0.09,
        pos=(0.0, 0.0),
        color="black",
        bold=False,
        italic=False,
    )
    end_t.draw()
    win.flip()
    core.wait(0)
    for row in rowlist:
        sheet.append(row)
    file.save(
        "{0}{1}{2}.xlsx".format(info["number"], info["name"], info["age"])
    )  # 保存实验数据，文件名为“序号+姓名+年龄"
    event.waitKeys()
    win.close()
    core.quit()  # 实验结束，窗口退出


def practice():  # 练习部分的过程
    global m, p  # 声明全局变量m,p
    attention = visual.TextStim(
        win,
        text="+",
        height=0.3,
        pos=(0.0, 0.0),
        color="red",
        bold=False,
        italic=False,
    )
    attention.draw()
    win.flip()
    core.wait(0.3)  # 每个trial之前出现一个红色的+号注视点，停留300ms
    attention = visual.TextStim(
        win,
        text=" ",
        height=0.3,
        pos=(0.0, 0.0),
        color="white",
        bold=False,
        italic=False,
    )
    attention.draw()
    win.flip()
    core.wait(0.2)  # 空屏200ms
    prime = demo_prime_list[demo_order[m]]  # 按照启动项随机后的顺序
    prime_video = prime + ".mp4"  # 具体文件名，支持多种视频格式
    mov_1 = visual.MovieStim3(win, prime_video)
    while mov_1.status != visual.FINISHED:
        mov_1.draw()
        win.flip()
        if event.getKeys(keyList=["p"]):  # 按P键暂停视频并跳过它
            mov_1.pause()
            break
    target = demo_target_list[demo_order[m]]  # 按照目标项随机后的顺序
    word_text = visual.TextStim(
        win,
        text=target,
        height=0.5,
        pos=(0.0, 0.0),
        color="black",
        bold=False,
        italic=False,
    )
    word_text.draw()
    win.flip()
    core.wait(0)
    judge = event.waitKeys(keyList=["f", "j"])  # 按F、J键分别代表一种含义，这里以“真、假”为例
    if judge[0] == "f":
        demo_judge_list.append("真")
    else:
        demo_judge_list.append("假")
    if demo_judge_list[m] == demo_value_list[demo_order[m]]:  # 如果被试的选择与正确答案一致，则p增加1
        p += 1
    m += 1  # 每进行一个trial后, m增加1
    if m == 10 and p >= 8:  # 当10次练习结束且正确率达到80%，展示练习结束语
        practice_end()
    elif m == 10 and p < 8:  # 当10次练习结束但正确率没有达到80%，m归0，继续练习
        m -= 10
        practice()
    while m < 10:  # m小于10时，调用自身，实现练习次数为10次(m从0到9)
        practice()


def practice_end():  # 显示练习结束语的函数
    global m
    m -= 10  # m归0，使继续练习成为可能
    prac_t = visual.TextStim(
        win,
        text=practice_end_text,
        height=0.09,
        pos=(0.0, 0.0),
        color="black",
        bold=False,
        italic=False,
    )
    prac_t.draw()
    win.flip()
    core.wait(0)
    choice = event.waitKeys(keyList=["q", "p"])
    if choice[0] == "q":  # 按Q键继续练习，按P键进入正式实验
        practice()
    else:
        test()


def test():  # 正式实验的过程，大部分与练习相同
    global n
    attention = visual.TextStim(
        win, text="+", height=0.3, pos=(0.0, 0.0), color="red", bold=False, italic=False
    )
    attention.draw()
    win.flip()
    core.wait(0.3)
    attention = visual.TextStim(
        win,
        text=" ",
        height=0.3,
        pos=(0.0, 0.0),
        color="white",
        bold=False,
        italic=False,
    )
    attention.draw()
    win.flip()
    core.wait(0.2)
    prime = prime_list[order[n]]
    prime_video = prime + ".mp4"
    mov_1 = visual.MovieStim3(win, prime_video)
    while mov_1.status != visual.FINISHED:
        mov_1.draw()
        win.flip()
        if event.getKeys(keyList=["p"]):
            mov_1.pause()
            break
    target = target_list[order[n]]
    if "-" not in target:  # 在我们的目标项中分别有文本和图片，而图片的文件名中有“-”符号
        word_text = visual.TextStim(
            win,
            text=target,
            height=0.5,
            pos=(0.0, 0.0),
            color="black",
            bold=False,
            italic=False,
        )
        word_text.draw()
    else:
        target_pic = target + ".png"
        word_pic = visual.ImageStim(win, image=target_pic)
        word_pic.draw()
    win.flip()
    timer = core.Clock()  # 使用计时器
    timer.reset()  # 当目标项出现在屏幕上，开始计时
    core.wait(0)
    judge = event.waitKeys(keyList=["f", "j"])
    if judge[0] == "f":
        judge_list.append("真")
    else:
        judge_list.append("假")
    timeUse = timer.getTime()  # 当被试做出选择，计时结束
    value = value_list[order[n]]
    rowlist.append([prime, target, value, judge_list[n], timeUse])  # 每次添加实验记录的五个值的一行数据
    n += 1  # 每进行一个trial后, n增加1
    if n % 10 == 0:  # 每进行10个trial，展示休息语
        rest()
    if n == 20:  # 当做完20个trial，实验结束
        end()
    while n < 20:  # n小于20时，调用自身
        test()


if __name__ == "__main__":
    info = {"name": "", "age": "", "number": ""}  # 弹出对话框记录被试的姓名、年龄、实验序号
    infoDlg = gui.DlgFromDict(
        dictionary=info, title=u"Basic information", order=["name", "age", "number"]
    )
    if infoDlg.OK:
        win = visual.Window(fullscr=True, color="Silver")  # 建立一个Psychopy的全屏窗口，背景为银灰色
        intro()  # 展示实验指导语
        practice()  # 进入实验的练习部分
    if infoDlg.OK == False:  # 被试不填写基本信息则无法进入实验，防止漏填
        core.quit()
