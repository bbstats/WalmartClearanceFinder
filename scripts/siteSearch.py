import walmart
import threading
import time

lock = threading.Lock()

STARTTIME = time.time()

THREADS = 30
RESULTS = []
URL_VALS = []
COMPLETED = []
#walmart.search_walmart("iphone", "2265")


#print len(walmart.get_all_facets("https://www.walmart.com/search/api/preso?query=a&cat_id=0&stores=1123&prg=mWeb"))

def search():
	while len(URL_VALS) > 0:
		try:
			lock.acquire()
			if len(URL_VALS) > 0:
				url = URL_VALS.pop(0)
				lock.release()
				info = walmart.network_request(url).json()
				for val in info['items']:
					lock.acquire()
					if val['usItemId'] not in COMPLETED:
						COMPLETED.append(val['usItemId'])
						RESULTS.append(val)
						print("{} | Item #{}".format(val['usItemId'], len(COMPLETED)))
					lock.release()
			else:
				lock.release()
		except Exception as exp:
			print exp


if __name__ == '__main__':
	searchTerm = raw_input("Search Term: ")
	URL_VALS += walmart.gen_search_urls(searchTerm)


	threads = [threading.Thread(target=search) for _ in range(THREADS)]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	print("{} items found in {} seconds".format(len(COMPLETED), time.time() - STARTTIME))