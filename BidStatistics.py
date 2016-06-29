#-*- coding: utf-8 -*-

import time

'''
time_enter_px 			输入价格的时间
time_px_ready 			价格输好的时间

time_enter_verify_code 	输入验证码的时间 
time_verify_code_ready 	验证码输好的时间

time_submit_px			提交价格的时间
time_accepted_by_server	价格提交到服务器的时间 

??? 最好能够统计读秒数据
'''
class BidTimeData(object):
	def __init__(self):
		self.time_enter_px = None
		self.time_px_ready = None
		
		self.time_enter_verify_code = None
		self.time_verify_code_ready = None

		self.time_submit_px = None
		self.time_accepted_by_server = None

	def time_verify_code_input(self):
		return self.time_verify_code_ready - self.time_enter_verify_code if self.time_verify_code_ready else None

	def time_for_px_input(self):
		return self.time_px_ready - self.time_enter_px if self.time_px_ready else None

	def round_trip(self):
		return self.time_accepted_by_server - self.time_submit_px if self.time_accepted_by_server else None

	def str(self):
		return "verify_code:{0}, px_round_trip:{1}, px_enter_delay:{2}"\
				.format(self.time_verify_code_input(), self.round_trip(), self.time_for_px_input())
'''
This class is designed to support the following functionalities so far:
1. 获取每个重要步骤的本地时间以及对应的服务器时间，计算本地到服务器的round trip；
	因为在不同的时间段有不同的round trip；所以这个类需要能够统计不同时间的round trip，
2. ideally，基于统计的round trip，给出提前量的建议

重要的本地-服务器时间
1. 提交之后似乎在到达服务器之前还有两秒左右的排队时间，应该把这个时间也考虑进去

'''
class StatisticsType(object):
	verify_code = 0
	px_round_trip = 1
	px_enter_delay = 2

#i don't consider multi-thread logging yet for now
class BidStatistics(object):
	def __init__(self):
		self.statistics_maps = {} # key:value => time:statistics_data
		self.current_statistics = {} # key:value => statistics_type:key_value

	def __str__(self):
		result = ""
		for (statistics_time,bid_time_data) in self.statistics_maps.items():
			result += "{0} => {1}\n".format(statistics_time, bid_time_data.str())
		return result

	def start_logging(self, statistics_type):
		key = time.strftime("%d")
		bid_time_data = self.statistics_maps.get(key, BidTimeData())
		if statistics_type == StatisticsType.verify_code:
			bid_time_data.time_enter_verify_code = time.time()
		elif statistics_type == StatisticsType.px_round_trip:
			bid_time_data.time_submit_px = time.time()
		elif statistics_type == StatisticsType.px_enter_delay:
			bid_time_data.time_enter_px = time.time()
		else:
			#log warning
			return
		self.statistics_maps[key] = bid_time_data
		self.current_statistics[statistics_type] = key

	def end_logging(self, statistics_type):
		key = self.current_statistics.pop(statistics_type)
		bid_time_data = self.statistics_maps[key]
		if statistics_type == StatisticsType.verify_code:
			bid_time_data.time_verify_code_ready = time.time()
		elif statistics_type == StatisticsType.px_round_trip:
			bid_time_data.time_accepted_by_server = time.time()
		elif statistics_type == StatisticsType.px_enter_delay:
			bid_time_data.time_px_ready = time.time()
		else:
			#log warning
			return

def main():
	bid_statistics = BidStatistics()
	bid_statistics.start_logging(StatisticsType.verify_code)
	time.sleep(0.3)
	bid_statistics.end_logging(StatisticsType.verify_code)

	bid_statistics.start_logging(StatisticsType.px_round_trip)
	time.sleep(0.5)
	bid_statistics.end_logging(StatisticsType.px_round_trip)

	bid_statistics.start_logging(StatisticsType.px_enter_delay)
	time.sleep(0.6)
	bid_statistics.end_logging(StatisticsType.px_enter_delay)

	print bid_statistics

if __name__ == "__main__":
	main()
