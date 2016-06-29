#-*- coding: utf-8 -*-

from ScreenResolver import Screen
from BidStrategy import Strategy

import logging
from datetime import datetime

def main():
	current_time_stamp = datetime.now().strftime("%Y%m%d%H")
	file_name = "Log/AutoBid_" + current_time_stamp + ".log"
	log_format = "%(asctime)-15s %(levelname)s %(message)s %(filename)s"
	logging.basicConfig(filename=file_name, format=log_format, level=logging.DEBUG)

	logging.info("========================================")
	logging.info("=======         START BID         ======")
	logging.info("========================================")

	print u"输入（回车：自动初始化界面； A：手动初始化界面；S：退出系统；）："
	input_text = raw_input()
	if input_text == "A" or input_text == "a":
		init_mode = "interactive"
	elif input_text == "S" or input_text == "s":
		return 
	else:
		init_mode = "auto"

	screen = Screen(init_mode)

	strategy = Strategy(screen)
	strategy.start_a_new_bid()

if __name__ == "__main__":
	main()


# IN PROGRESS TODO
#8. TODO 6: Screen need to support more init mode as well as more types of screen(especially different resolution)

# FINISHED TODO 
#6. TODO 4: Logger for standard output, i don't need debug log at all, disable it
#3. TODO 1: After submit px, we may need to wait for another enter to click on ok and then input px again
#4. TODO 2: At the start of the system, allow user to choose which strategy to use

# PENDING TODO
		#TODO 点击出价然后输入验证码的时候，拍牌界面失去焦点，验证码输入框也就失去焦点了，
		#再用bring to foreground之后也并没有把焦点自动设置到验证码输入框，然后用鼠标模拟single click的操作也并没有把
		#焦点重置到验证码输入框 
		#下次可以尝试以下方法
		#1. 手动返回拍牌界面，看焦点是否重置到验证码输入框
		#2. Win32有没有setFocus的操作？

#11. TODO 训练看自己输入四位数字平均需要多长时间
#2. 提交之后似乎在到达服务器之前还有两秒左右的排队时间，应该把这个时间也考虑进去
#5. TODO 3: For customized px strategy, allow user to setup customized px
#9. TODO 7: 需要统计几个时间 1. 输入价格的时间 2.输入验证码的时间 3.价格提交到服务器的时间 4.最好能够统计读秒数据
#7. TODO 5: I need a test mode(which need Screen refactor) so that when debugging the system, click can do different thing casue there is not actual any button to click

# TODO Next Bid Time
#1. 似乎用PyKeyboard一次性输入或者用clipboard copy paste 都不被接受，下次尝试一个数字一个数字的输入
#10. TODO 8：可以通过系统返回的错误信息以及当前显示的系统时间估算出自己到服务器的网络延时，分别在低峰时和高峰时测试一次