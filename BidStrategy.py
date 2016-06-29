#-*- coding: utf-8 -*-
from ScreenResolver import Screen
from BidStatistics import *

import logging

class Strategy(object):
	def __init__(self, screen):
		self.screen = screen
		self.statistics = BidStatistics()

	# Before calling this method, the verfication code input interface is expected
	# This method does the following things
	# 1.提示并等待验证码输入，以回车结束输入
	# 2.获取用户输入的验证码
	# 3.根据auto_submit决定再次等待用户输入还是自动提交
	def enter_verify_code_and_submit_px(self, auto_submit=False):
		self.statistics.start_logging(StatisticsType.verify_code)
		print u"输入验证码然后回车: "
		logging.debug("Waiting for verification code input")
		verification_code = raw_input()

		self.screen.enter_verify_code(verification_code)
		self.statistics.end_logging(StatisticsType.verify_code)

		self.statistics.start_logging(StatisticsType.px_round_trip)
		if auto_submit is False:
			print u"输入（回车：提交； A：取消；）："
			logging.debug("Waiting for enter to submit price")
			input_text = raw_input()
			if input_text == "A" or input_text == "a":
				logging.debug("Cancelling current price")
				self.screen.click_cxl_btn()
				self.start_a_new_bid()
				return
		else: #auto submit, system calculates the best submit time and wait until it, if alread passed, submit immediately
			# $$$$TODO
			print "do nothing for now, TODO, using timer"

		logging.debug("Submitting price to bid server")

		#TODO -> how to resolve submit result?
		self.screen.click_ok_btn()
		self.statistics.end_logging(StatisticsType.px_round_trip) #TODO, this is not accurate though
		self.post_submit_px()

		self.start_a_new_bid()

	# there is an assumption here that we are back in the main page
	def start_a_new_bid(self):
		print u"选择拍牌策略 -（回车：当前价+自定义加价；A：当前价+300；S：手动输入价格 D：结束拍卖）:"
		input_text = raw_input()
		if input_text == "A" or input_text == "a":
			self.bid_plus300_px()
		elif input_text == "S" or input_text == "s":
			self.bid_manual_input_px()
		elif input_text == "D" or input_text == "d":
			return #return, exit bid
		else:
			self.bid_customized_px()

	def confirm_bid_strategy_or_start_a_new_one(self, strategy_text):
		print u"使用 {0} 策略，（回车：继续, A：取消）".format(strategy_text)
		input_text = raw_input()
		if input_text == "A" or input_text == "a":
			logging.debug("User cancelled the current strategy, going back to main interface")
			self.start_a_new_bid()
			return False
		else:
			return True

	# Cleanup and prepare for next price input
	def post_submit_px(self):
		#we don't know whether or not it succeeds, so click on both possible buttons
		#if error happens, this click can bring us back to main screen,ddd
		#otherwise, it clicks on just the screen, does no effect
		self.screen.click_error_btn()
		#if succeeds, this click can bring us back to main screen,
		#otherwise, the previous click will bring us back to main screen, and this click does no effect
		self.screen.click_ok_after_bid_btn()

	#px_btn_pos could be +300 button position or custormised button position
	def bid_plus300_px(self, auto_submit=False):
		log_info = "========Using plus 300 strategy ========"
		logging.info(log_info)	
		if not self.confirm_bid_strategy_or_start_a_new_one(u"当前最低价+300"): 
			return

		self.screen.click_plus300_px_btn()
		self.screen.click_bid_btn()

		self.enter_verify_code_and_submit_px(auto_submit)

	def bid_manual_input_px(self, auto_submit=False):
		log_info = "========Using manual input px strategy ========"
		logging.info(log_info)
		if not self.confirm_bid_strategy_or_start_a_new_one(u"手动输入价格"): 
			return

		print u"输入拍牌价格然后回车："
		px = raw_input()
		self.screen.enter_manual_input_px(px)
		self.screen.click_bid_btn()

		self.enter_verify_code_and_submit_px(auto_submit)

	def bid_customized_px(self, auto_submit=False):
		log_info = "========Using customized px strategy ========"
		logging.info(log_info)
		if not self.confirm_bid_strategy_or_start_a_new_one(u"当前最低价+自定义加价幅度"): 
			return

		self.screen.click_customized_px_btn()
		self.screen.click_bid_btn()
		
		self.enter_verify_code_and_submit_px(auto_submit)

def main():
	logging.basicConfig(format="%(asctime)-15s %(levelname)s %(message)s %(filename)s", level=logging.DEBUG)
	strategy = Strategy(Screen())
	strategy.bid_plus300_px()

	print strategy.statistics

if __name__ == "__main__":
	main()