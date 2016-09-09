from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import csv
import time

def getCommentsAndReplies(FILE_NAME, browser):
	DEBUG_ENABLE = 0
	with open(FILE_NAME) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			try:
				print(row['articleUrl'])
				print(row['articleObjId'])
				articleObjId = row['articleObjId']
				browser.get(row['articleUrl'])

				# get author pic url
				authorPicUrl = browser.find_element_by_xpath("//a[@class='avatar']").find_element_by_tag_name('img').get_attribute('src')
				print('@'*9)
				print(authorPicUrl)
				with open('authorPicUrl.csv', 'a') as csvfile:
					fieldnames = ['authorIconUrl']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
					writer.writerow({'authorIconUrl': authorPicUrl})


				commentList = browser.find_element_by_xpath("//div[@id='comment-list']")
				for comment in commentList.find_elements_by_css_selector('div.note-comment.clearfix'):
					#print (comment)
					commentId = comment.get_attribute('id')
					commenterUrl = comment.find_element_by_tag_name('a').get_attribute('href')
					commenterName = comment.find_element_by_class_name('author-name').text
					commentContent = comment.find_element_by_class_name('content').find_elements_by_tag_name('p')[1].text
					commentTime = comment.find_element_by_class_name('reply-time').find_element_by_tag_name('a').text
					print("*****Got comment")
					print(commenterUrl)
					print(commenterName)
					print(commentContent)
					print(commentTime)
					#print (commentFloor)
					#find comment author image url
					# browserForImg = webdriver.Firefox()
					# browserForImg.get(commenterUrl)
					# commentPicUrl = browserForImg.find_element_by_xpath("//div[@class='avatar']").find_element_by_tag_name('img').get_attribute('src')
					# browserForImg.quit()
					# time.sleep(1)
					commentPicUrl = comment.find_element_by_tag_name('img').get_attribute('src')
					

					print(commentPicUrl)
					#print (commentLikes)
					childCommentAuthor = ''
					maleskineAuthor = ''
					childCommentContent = ''
					hasReply = 'true'
				
					try:
						replyList = []
						childCommentList = comment.find_elements_by_class_name('child-comment')
						for childComment in childCommentList:
							childCommentAuthor = childComment.find_element_by_class_name('blue-link').text
							maleskineAuthor = childComment.find_element_by_class_name('maleskine-author').text.split('@')[-1]
							childCommentContentList = childComment.find_element_by_tag_name('p').text.rsplit('@')[-1].lstrip(maleskineAuthor).split()
							if len(childCommentContentList) == 0:
								childCommentContent = ''
							else:
								childCommentContent = childCommentContentList[0]
							# save to list
							replyList.append({'replyWho': maleskineAuthor, 'replyContent': childCommentContent,
								'replyAuthor': childCommentAuthor, 'commentId': commentId})
							print(">>>>>>>>Got child comment")
							print(childCommentAuthor)
							print(maleskineAuthor)
							print(childCommentContent)
						
						# write reply list to csv
						with open('replys.csv', 'a') as csvfile:
							reply_fieldnames = ['replyWho', 'replyContent', 'replyAuthor', 'commentId']
							writer = csv.DictWriter(csvfile, fieldnames=reply_fieldnames)

							for reply in replyList:
								writer.writerow(reply)

					except NoSuchElementException as e:
						print('except:', e)
						hasReply = 'false'
					finally:
						print(commentId)
						#print(hasReply)
						print(commentTime)
						#print(articleObjId)
						
						#write comment csv
						with open('comments.csv', 'a') as csvfile:
							fieldnames = ['hasReply', 'commentId', 'commenterTimer', 'commenterName', 'commentContent', 'articleObjId', 'commenterUrl', 'commentPicUrl']
							writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
							writer.writerow({'hasReply': hasReply, 'commentId': commentId, 'commenterTimer': commentTime, 'commenterName': commenterName, 'commentContent': commentContent, 'articleObjId': articleObjId, 'commenterUrl': commenterUrl, 'commentPicUrl':commentPicUrl})
			except NoSuchElementException as e:
				print('except: ', e)

			if DEBUG_ENABLE == 1:
					break;
	browser.quit()

def writeCsvHeader(fileName, openMode, fieldnames):
	with open(fileName, openMode) as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

if __name__ == '__main__':

	REPLY_CSV = 'replys.csv'
	COMMENT_CSV = 'comments.csv'
	AUTHOR_PIC_CSV = 'authorPicUrl.csv'
	DEBUG_ENABLE = 1
	FILE_NAME = 'articleTest12.csv'
	browser = webdriver.Firefox()

	writeCsvHeader(REPLY_CSV, 'w', ['replyWho', 'replyContent', 'replyAuthor', 'commentId'])
	writeCsvHeader(COMMENT_CSV, 'w', ['hasReply', 'commentId', 'commenterTimer', 'commenterName', 'commentContent', 'articleObjId', 'commenterUrl', 'commentPicUrl'])
	writeCsvHeader(AUTHOR_PIC_CSV, 'w', ['authorIconUrl'])

	# open reply csv
	# with open('replys.csv', 'w') as csvfile:
	# 	reply_fieldnames = ['replyWho', 'replyContent', 'replyAuthor', 'commentId']
	# 	writer = csv.DictWriter(csvfile, fieldnames=reply_fieldnames)
	# 	writer.writeheader()
	# # open comment csv
	# with open('comments.csv', 'w') as csvfile:
	# 	fieldnames = ['hasReply', 'commentId', 'commenterTimer', 'commenterName', 'commentContent', 'articleObjId', 'commenterUrl', 'commentPicUrl']
	# 	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	# 	writer.writeheader()
	# # open article author picture url
	# with open('authorPicUrl.csv', 'w') as csvfile:
	# 	fieldnames = ['authorPicUrl']
	# 	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	# 	writer.writeheader()

	getCommentsAndReplies(FILE_NAME, browser)

