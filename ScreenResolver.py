#-*- coding: utf-8 -*-
from win32gui import SetFocus, WindowFromPoint, ShowWindow, GetCursorPos, GetDesktopWindow, GetWindowRect, SetActiveWindow, SetForegroundWindow
from win32ui import GetForegroundWindow
from pymouse import PyMouse
from pykeyboard import PyKeyboardEvent
from pykeyboard import PyKeyboard
import win32clipboard as clipboard

import time
import logging

class Screen(object):
	#init_mode 
	#  1. auto -> use precached setting or if not precached setting, initialize it
	#  2. interactive -> initialize it no matter if it's precached or not
	def __init__(self, init_mode="auto"):
		self.mouse = PyMouse()
		self.keyboard = PyKeyboard()
		self.cmd_whnd = GetForegroundWindow() #object of PyCWnd
		self.bid_whnd = WindowFromPoint(self.mouse.position())
		#get screen resolution
		self.resolution = self.__get_screen_resolution() 
		logging.debug("Screen resolution is {0} x {1}".format(self.resolution[2], self.resolution[3]))
		#TODO use a config file to pre-cache all know resolutions and corresponding control positions

		if init_mode == "interactive":
			logging.debug("User chose to initialize screen settings")
			self._init_first_phase_control_positions()
			self._init_second_phase_control_positions()
		elif self.resolution == (0, 0, 1280, 800):
			logging.debug("Using pre-defined settings")
			#position for myself
			self.cmd_window_pos = (0, 569, 1280, 200)

			#controls for phase 2		
			#the positions below are positions when web page is maximized on my computer
			self.custom_px_field_pos = (906, 379) #TODO To initialize 
			self.custom_px_btn_pos = (976, 379)
			self.plus_300_btn_pos = (827, 453)
			self.bid_btn_pos = (983, 487)
			self.ok_btn_pos = (740, 556)
			self.cxl_btn_pos = (961, 556) 
			self.ok_after_bid_pos = (828, 539)  
			self.error_btn_pos = (834, 546)

			self.px_field_pos = (856, 483) 
			self.verify_code_pos = (828, 464) 

			self.first_phase_px_field_1_pos = (763, 586)
			self.first_phase_px_field_2_pos = (820, 597)
			self.first_phase_verify_code_field_pos = (724, 594)
		else:
			logging.debug("Could not find pre-defined settings for this screen resolution setup, initializing settings")
			self._init_first_phase_control_positions()
			self._init_control_positions()
		
		#restructure cmd window and bid web page per controls positions initialized above		
		#self.__prepare_screen()

	def __get_screen_resolution(self):
		desk_win_handle = GetDesktopWindow()
		return GetWindowRect(desk_win_handle)

	def __get_control_position(self, control_name, variable_name, control_type):
		just_place_holder = raw_input()
		if (control_type == "button"):
			pos = self.mouse.position()
		else:#control_type == "input"
			pos = GetCursorPos()
		print "self.%s = (%d, %d)" % (variable_name, pos[0], pos[1])
		return pos
	
	def __get_control_position_by_mouse(self, control_name, variable_name):
		print "Move mouse to {0} field and then press Enter to confirm".format(control_name)
		return self.__get_control_position(control_name, variable_name, "button")

	#not used cause if i click on the field, cmd window looses the focus already
	def __get_control_position_by_cursor(self, control_name, variable_name):
		print "Click in {0} field and then press Enter to confirm".format(control_name)
		return self.__get_control_position(control_name, variable_name, "input")

	def _init_first_phase_control_positions(self):
		self.first_phase_px_field_1_pos = self.__get_control_position_by_mouse("first phase price 1", "first_phase_px_field_1_pos")
		self.first_phase_px_field_2_pos = self.__get_control_position_by_mouse("first phase price 2", "first_phase_px_field_2_pos")
		self.first_phase_verify_code_field_pos = self.__get_control_position_by_mouse("first phase verification code", "first_phase_verify_code_field_pos")

	def _init_second_phase_control_positions(self):
		self.custom_px_field_pos = self.__get_control_position_by_mouse("customerized price field", "custom_px_field_pos")
		self.custom_px_btn_pos = self.__get_control_position_by_mouse("customerized price button", "custom_px_btn_pos")
		self.plus_300_btn_pos = self.__get_control_position_by_mouse("+300 button", "plus_300_btn_pos")
		self.px_field_pos = self.__get_control_position_by_mouse("price field", "px_field_pos")
		self.bid_btn_pos = self.__get_control_position_by_mouse("bid button", "bid_btn_pos")
		self.verify_code_pos = self.__get_control_position_by_mouse("verification code", "verify_code_pos")
		self.ok_btn_pos = self.__get_control_position_by_mouse("ok button", "ok_btn_pos")
		self.cxl_btn_pos = self.__get_control_position_by_mouse("cancel button", "cxl_btn_pos")
		self.ok_after_bid_pos = self.__get_control_position_by_mouse("another ok button", "ok_after_bid_pos")
		self.error_btn_pos = self.__get_control_position_by_mouse("error button", "error_btn_pos")

	#it also returns the current cmd dialog for later use
	def __prepare_screen(self):
		#TODO : RESET WINDOW SIZE TO MAKE IT WOKR PERFECTLY WITH THE POSITIONS BELOW
		#put the cmd dialog at top most
		self.cmd_whnd.SetWindowPos(-1, self.cmd_window_pos, 0x0040) #top_most:-1

		#maximize the bid window, which is a webpage at the moment
		ShowWindow(self.bid_whnd, 3)#MAX:3
		
		self.__bring_myself_to_Foreground()

	def _bring_bid_window_to_Foreground(self):
		SetForegroundWindow(self.bid_whnd)
		#TODO　which one works better
		SetActiveWindow(self.bid_whnd)
		SetFocus(self.bid_whnd)#TODO not sure if it works or not

	def __bring_myself_to_Foreground(self):
		self.cmd_whnd.SetForegroundWindow()

	def __double_click_at_pos(self, position):
		logging.debug("Double click at position (%d, %d)" % (position[0], position[1]))
		self.mouse.click(position[0], position[1], 1)

	def __single_click_at_pos(self, position, num=1):
		logging.debug("Single click at position (%d, %d)" % (position[0], position[1]))
		self.mouse.click(position[0], position[1], 1, num)

	def __copy_text(self, text):
		clipboard.OpenClipboard()
		clipboard.EmptyClipboard()
		clipboard.SetClipboardText(text)
		clipboard.CloseClipboard()

	def __paste(self, text):
		# self.keyboard.press_keys([self.keyboard.control_key, 'v'])
		for c in text:
			self.keyboard.press_key(c) #type_string may still be slow
			time.sleep(0.1)

	def single_click_at_pos(self, position):
		self.__single_click_at_pos(position)
		self.__bring_myself_to_Foreground()

	#text - plain text value to copy/paste
	#pos - to where the text value should be pasted to - it should points to somewhere paste makes sense, like input field
	def copy_and_paste_at_pos(self, text, pos):
		#TODO 点击出价然后输入验证码的时候，拍牌界面失去焦点，验证码输入框也就失去焦点了，
		#再用bring to foreground之后也并没有把焦点自动设置到验证码输入框，然后用鼠标模拟single click的操作也并没有把
		#焦点重置到验证码输入框 
		#下次可以尝试以下方法
		#0. Use SetActiveWindow in bring_bid_window_to_Foreground
		#1. 手动返回拍牌界面，看焦点是否重置到验证码输入框
		#2. DoubleClick是否work？#no idea how to do double click
		#3. Win32有没有setFocus的操作？ SetFocus(self.bid_whnd)#TODO not sure if it works or not

		self._bring_bid_window_to_Foreground() #SetFocus(self.bid_whnd)#TODO not sure if it works or not
		time.sleep(0.5)
		logging.debug("Click on verification code input field")
		self.__single_click_at_pos(pos, 2)#don't use public single_click_at_pos method cause it brings myself to foreground afterwards
		logging.debug("Paste verification code: {0} to the input field".format(text))
		# Use clipboard to copy and pase ####self.copy_text(text)
		# self.__copy_text(text)
		self.__paste(text)
		self.__bring_myself_to_Foreground()
	
	def click_customized_px_btn(self):
		logging.debug("Cick on customerized price button")
		self.single_click_at_pos(self.custom_px_btn_pos)

	def click_plus300_px_btn(self):
		logging.debug("Click on plus 300 price button")
		self.single_click_at_pos(self.plus_300_btn_pos)

	def click_bid_btn(self):
		logging.debug("Click on bid button")
		self.single_click_at_pos(self.bid_btn_pos)
	
	def click_ok_btn(self):
		logging.debug("Click on ok button")
		self.single_click_at_pos(self.ok_btn_pos)

	def click_cxl_btn(self):
		logging.debug("Click on cancel button")
		self.single_click_at_pos(self.cxl_btn_pos)

	def click_ok_after_bid_btn(self):
		logging.debug("Click on ok_after_bid button")
		self.single_click_at_pos(self.ok_after_bid_pos)

	def click_error_btn(self):
		logging.debug("Click on error button")
		self.single_click_at_pos(self.error_btn_pos)

	def enter_manual_input_px(self, px):
		logging.debug("Copy and paste manual px to price field")
		self.copy_and_paste_at_pos(px, self.px_field_pos)

	def enter_verify_code(self, verification_code):
		# logging.debug("click on verification code field")
		# screen.single_click_at_pos(screen.verify_code_pos)
		# key.type_string(verification_code) #type_string may still be slow
		logging.debug("Copy and paste to verification code {0} field".format(verification_code))
		self.copy_and_paste_at_pos(verification_code, self.verify_code_pos)

def main():
	logging.basicConfig(format="%(asctime)-15s %(levelname)s %(message)s %(filename)s", level=logging.DEBUG)
	screen = Screen()
	# screen._init_first_phase_control_positions()
	# screen._init_second_phase_control_positions()

if __name__ == "__main__":
	main()