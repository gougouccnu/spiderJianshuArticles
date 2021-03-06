from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import csv
import time


def find(driver):
    element = driver.find_element_by_xpath("//ul[@class='article-list thumbnails']")
    if element:
        return element
    else:
        return False

def getArticles(FILE_NAME, browser, cid):

		#click get more button to get more article
		for x in range(0,8):
			print('load more: ' + str(x))
			browser.find_element_by_css_selector('button.ladda-button').click()
			browser.implicitly_wait(3)
		browser.implicitly_wait(10)
		#ul = browser.find_element_by_xpath("//ul[@class='article-list thumbnails']")
		ul = WebDriverWait(browser, 10).until(find)

		authorId = 0
		imgSrc = ''

		for li in ul.find_elements_by_tag_name('li'):
			try:
				#
				imgSrc = li.find_element_by_class_name('wrap-img').find_element_by_tag_name('img').get_attribute('src')
				authorName = li.find_element_by_tag_name('p').find_element_by_tag_name('a').text
				#
				authorUrl = li.find_element_by_tag_name('p').find_element_by_tag_name('a').get_attribute('href')
				articleCreatedTime = li.find_element_by_tag_name('p').find_element_by_tag_name('span').get_attribute('data-shared-at')
				articleTitle = li.find_element_by_tag_name('h4').text
				#
				articleUrl = str(li.find_element_by_tag_name('h4').find_element_by_tag_name('a').get_attribute('href'))
				list_footer = li.find_element_by_tag_name('div').find_element_by_tag_name('div')
				readTimes = list_footer.find_elements_by_tag_name('a')[0].text
				comments = list_footer.find_elements_by_tag_name('a')[1].text
				spanList = list_footer.find_elements_by_tag_name('span')
				likes = spanList[0].text
				if len(spanList) == 2:
					donate = spanList[1].text
				else:
					donate = 0
				#find author image url
				# browserForImg = webdriver.Firefox()
				# browserForImg.get(articleUrl)
				# authorImgUrl = browserForImg.find_element_by_xpath("//a[@class='avatar']").find_element_by_tag_name('img').get_attribute('src')
				# browserForImg.quit()
				# time.sleep(1)		

				print(imgSrc)
				print(authorName)
				#print(authorImgUrl)
				#print(authorUrl)
				print(articleCreatedTime)
				print(articleTitle)
				print(articleUrl)
				print(readTimes)
				print(comments)
				print(likes)
				print(donate)

				# get artileObjId from articleUrl
				articleObjId = articleUrl.rsplit('/')[-1]

				with open(FILE_NAME, 'a') as csvfile:
					fieldnames = ['id', 'author', 'cid', 'readTimes', 'comments', 'likes', 'donate', 'tag', 'authorIconUrl', 'pictureUrl', 'title', 'articleUrl', 'articleObjId']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
					writer.writerow({'id': authorId, 'author': authorName, 'cid': cid, 'readTimes': 4, 'comments': 5, 'likes': 2, 'donate': 5, 'tag': '你在哪里', 'pictureUrl': imgSrc, 'title': articleTitle, 'articleUrl': articleUrl, 'articleObjId': articleObjId})
				authorId = authorId + 1
			except NoSuchElementException as e:
				print('except:', e)
				imgSrc = ''
				
		print('END')
		#browser.quit()

if __name__ == "__main__":
	FILE_NAME = 'articleTest12.csv'

	with open(FILE_NAME, 'w') as csvfile:
		    fieldnames = ['id', 'author', 'cid', 'readTimes', 'comments', 'likes', 'donate', 'tag', 'authorIconUrl', 'pictureUrl', 'title', 'articleUrl', 'articleObjId']
		    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		    writer.writeheader()

	browser = webdriver.Firefox()
	browser.get('http://jianshu.com')
	print(browser)

	liId = 0
	# ulList = browser.find_element_by_xpath("//ul[@id='collection-categories-nav']")

	# for li in ulList.find_elements_by_tag_name('li'):
	# 	try:
	# 		print('liId is: ' + str(liId))
	# 		item = li.find_element_by_class_name('category').click()
	# 		browser.implicitly_wait(5)
	# 		print(browser)
	# 		getArticles(FILE_NAME, browser, liId)
	# 		liId += 1
	# 		browser.implicitly_wait(5)

	# 		ulList = browser.find_element_by_xpath("//ul[@id='collection-categories-nav']")
	# 		li = ulList.find_elements_by_tag_name('li')[1].find_element_by_class_name('category').send_keys('\n')
	# 		print('clicked')
	# 		browser.implicitly_wait(5)
	# 		getArticles(FILE_NAME, browser, liId)
	# 		break

	# 	except NoSuchElementException as e:
	# 		print('except: ', e)
	while  liId < 10:
		try:
			print('liId is: ' + str(liId))
			ul = browser.find_element_by_xpath("//ul[@id='collection-categories-nav']")
			# use send keys or could not find button
			li = ul.find_elements_by_tag_name('li')[liId].find_element_by_class_name('category').send_keys('\n')
			print('clicked')
			browser.implicitly_wait(10)
			getArticles(FILE_NAME, browser, liId)
			liId += 1

		except NoSuchElementException as e:
			print('except: ', e)
