"""
This is an adaptable example script for using selenium across multiple webbrowsers simultaneously. This makes use of
two queues - one to store idle webworkers and another to store data to pass to any idle webworkers in a selenium function
"""
from multiprocessing import Queue, cpu_count
from threading import Thread
from selenium import webdriver
import logging
import os
from os.path import expanduser
from seleniumwire import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from json import loads, dumps
from time import time
from tqdm import tqdm  # Progress bar UI
from openpyxl import load_workbook
from datetime import datetime

DEBUG = False
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.system("ulimit -n 2048")

BASE_PATH = os.getcwd()
INPUT_STOCK_IDS_PATH = 'input_stock_ids.txt'
NUM_RETRIES = 10
HOME = expanduser("~")
SAVE_PATH = HOME+"/Downloads/"

def make_new_driver():
		chrome_options = Options()
		chrome_capabilities = DesiredCapabilities().CHROME
		chrome_capabilities['pageLoadStrategy'] = 'none'
		wire_options = {
				'disable_encoding': True
		}
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-infobars")
		chrome_options.add_argument("start-maximized")
		chrome_options.add_argument('window-size=1920x1480')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument('--disable-dev-shm-usage')

		driver = webdriver.Chrome(options=chrome_options, desired_capabilities=chrome_capabilities, seleniumwire_options=wire_options)
		driver.implicitly_wait(0)
		return driver


def json_to_row(data):
		d = data['data']
		return [d['name'], d['uscc'], d['businessScope'],
											d['score'],
											d['creditStatus'],
											d['indicatorList'][0]['score'],
											d['indicatorList'][0]['childList'][0]['score'],
											d['indicatorList'][0]['childList'][1]['score'],
											d['indicatorList'][1]['score'],
											d['indicatorList'][1]['childList'][0]['score'],
											d['indicatorList'][1]['childList'][1]['score'],
											d['indicatorList'][2]['score'],
											d['indicatorList'][2]['childList'][0]['score'],
											d['indicatorList'][2]['childList'][1]['score'],
											d['indicatorList'][2]['childList'][2]['score'],
											d['indicatorList'][3]['score'],
											d['indicatorList'][3]['childList'][0]['score'],
											d['indicatorList'][3]['childList'][1]['score'],
											d['indicatorList'][3]['childList'][2]['score'],
											d['indicatorList'][4]['score'],
											d['indicatorList'][4]['childList'][0]['score'],
											d['indicatorList'][4]['childList'][1]['score'], d['creditRank']]


def scrape_a_company(driver, id, pbar, depth=0):
		start_time = time()
		waiter = WebDriverWait(driver, 60, ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,))
		driver.get(
				f"https://credit.zj.gov.cn/jyh/#/home/searchResult?condition={id}&type=&source=object")
		try:
				list_button = waiter.until(
						EC.presence_of_element_located((By.CLASS_NAME, "ivu-table-row")))
				# hovered_list_button = driver.find_element_by_css_selector('#ivu-table-row-hover')
				action_chain = ActionChains(
						driver).move_to_element(list_button).click()
				action_chain.perform()

				request = driver.wait_for_request(
						'/router/api/p/creditSearchCityArchivalInfo', 30)
				archivalInfoData = loads(request.response.body)
				company_name = archivalInfoData['data']['name']
				with open(f"{BASE_PATH}/raw_data/{company_name}.json", 'wb') as f:
						f.write(dumps(archivalInfoData, ensure_ascii=False,
													indent=2).encode('utf8'))
				excel_rows.append(json_to_row(archivalInfoData))
				end_time = time()
				pbar.update(1)
				pbar.set_postfix({
						'ID': id,
						'Name': company_name,
						'Time': f"{end_time-start_time:.2f}s"
				})
		except TimeoutException:
				if depth < NUM_RETRIES:
						print(f"NOTE: #{depth+1} retry for ID '{id}' ....")
						scrape_a_company(driver, id, pbar, depth=depth+1)
				else:
						print(f"\n--> WARN: ID '{id}' not saved\n")
						unsaved_ids.append(id)
		finally:
				del driver.requests  # Driver reused for future requests - must clear


def selenium_queue_listener(data_queue, worker_queue, file_write_queue, pbar):
		"""
		Monitor a data queue and assign new pieces of data to any available web workers to action
		:param data_queue: The python FIFO queue containing the data to run on the web worker
		:type data_queue: Queue
		:param worker_queue: The queue that holds the IDs of any idle workers
		:type worker_queue: Queue
		:rtype: None
		"""
		logger.info("Selenium func worker started")
		while True:
				current_data = data_queue.get()
				if current_data == 'STOP':
						# If a stop is encountered then kill the current worker and put the stop back onto the queue
						# to poison other workers listening on the queue
						logger.info("STOP encountered, killing worker thread")
						data_queue.put(current_data)
						file_write_queue.put(current_data)
						break
				else:
						logger.info(f"Got the item {current_data} on the data queue")
				# Get the ID of any currently free workers from the worker queue
				worker_id = worker_queue.get()
				worker = selenium_workers[worker_id]
				# Assign current worker and current data to your selenium function
				scrape_a_company(worker, current_data, pbar)
				# Put the worker back into the worker queue as  it has completed it's task
				worker_queue.put(worker_id)
		return

# if __name__ == '__main__':
# 	input_ids = None
# 	with open(INPUT_STOCK_IDS_PATH) as f:
# 		input_ids = [l.strip() for l in f.readlines()]
# 	driver = make_new_driver()
# 	try:
# 		for id in input_ids:
# 			scrape_a_company(driver, id)
# 	finally:
# 		driver.quit()


if __name__ == '__main__':
		print("Warming up! 🌤")
		# Some example data to pass the the selenium processes, this will just cause a sleep of time i
		# This data can be a list of any datatype that can be pickled
		input_ids = None
		with open(INPUT_STOCK_IDS_PATH) as f:
				input_ids = [l.strip() for l in f.readlines()] + ['STOP']

		pbar = tqdm(total=len(input_ids)-1)
		# Create the threes queues to hold the data and the IDs for the selenium workers and the output data to save
		selenium_data_queue = Queue()
		worker_queue = Queue()
		file_write_queue = Queue()

		# Create Selenium processes and assign them a worker ID
		# This ID is what needs to be put on the queue as Selenium workers cannot be pickled
		# By default, make one selenium process per cpu core with cpu_count
		# TODO: Change the worker creation code to be your webworker of choice e.g. PhantomJS
		worker_ids = list(range(cpu_count()//2)) if not DEBUG else [0,1]

		selenium_workers = {i: make_new_driver() for i in worker_ids}
		for worker_id in worker_ids:
				worker_queue.put(worker_id)

		# Create one new queue listener thread per selenium worker and start them
		logger.info("Starting selenium background processes")
		selenium_processes = [Thread(target=selenium_queue_listener,
																 args=(selenium_data_queue, worker_queue, file_write_queue, pbar)) for i in worker_ids]  # + \
		try:
			unsaved_ids = []
			excel_rows = []
			for p in selenium_processes:
					p.daemon = True
					p.start()

			# Add each item of data to the data queue, this could be done over time so long as the selenium queue listening
			# processes are still running
			logger.info("Adding data to data queue")
			for d in input_ids:
					selenium_data_queue.put(d)

			# Wait for all selenium queue listening processes to complete, this happens when the queue listener returns
			logger.info("Waiting for Queue listener threads to complete")
			for p in selenium_processes:
					p.join()
			
			excel = load_workbook(f"{BASE_PATH}/template_headers.xlsx")
			for row in excel_rows:
				excel.worksheets[0].append(row)
			now = ":".join(datetime.now().isoformat().split(":")[:-1])
			excel.save(f"{SAVE_PATH}/ZJ_scores_{now}.xlsx")


			print(f"Victory! Excel sheet saved at ZJ_scores_{now}.xlsx 🥳"+"\n\n"+str(len(unsaved_ids)) +
						" IDs were not saved. Please manually add the rest below:\n\n- "+'\n- '.join(unsaved_ids))
		finally:
			# Quit all the web workers elegantly in the background
			logger.info("Tearing down web workers")
			print(f"Stopping app early. Excel sheet not generated! Wait for it to finish next time 🙃")
			for b in selenium_workers.values():
					b.quit() # Prevent memory leak 