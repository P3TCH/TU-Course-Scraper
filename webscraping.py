import pandas as pd
import requests
from bs4 import BeautifulSoup

def thai_text(thai):
	return_text = ''
	thai_all = ['%A1', '%A2', '%A3', '%A4', '%A5', '%A6', '%A7', '%A8', '%A9', '%AA', '%AB', '%AC', '%AD', '%AE', '%AF', '%B0', '%B1', '%B2', '%B3', '%B4', '%B5', '%B6', '%B7', '%B8', '%B9', '%BA', '%BB', '%BC', '%BD', '%BE', '%BF', '%C0', '%C1', '%C2', '%C3', '%C4', '%C5', '%C6', '%C7', '%C8', '%C9', '%CA', '%CB', '%CC', '%CD', '%CE', '%CF', '%D0', '%D1', '%D2', '%D3', '%D4', '%D5', '%D6', '%D7', '%D8', '%D9', '%DA', '%DB', '%DC', '%DD', '%DE', '%DF', '%E0', '%E1', '%E2', '%E3', '%E4', '%E5', '%E6', '%E7', '%E8', '%E9', '%EA', '%EB', '%EC', '%ED', '%EE', '%EF', '%F0', '%F1', '%F2', '%F3', '%F4', '%F5', '%F6', '%F7', '%F8', '%F9', '%FA', '%FB']
	for i in thai:
		if ord(i) > 3584 and ord(i) < 3677:
			i = thai_all[ord(i) - 3585]
		return_text += i

	return return_text


# Get the HTML from the URL
row = []
print('---------------------------------\n  Welcome to TU Course Scraper! \n\tCreated by: P3TCH\n\tv0.0.1 \n---------------------------------')
url = input('Enter Start URL: ')
page = 1

while(1):
	print('Page: ' + str(page))
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'lxml')
	d = soup.find('table', {'cellpadding' : '3'})

	# course code
	course_code_temp = d.find_all('a', {'href' : '#current'})
	course_code = []
	for i in course_code_temp:
		course_code.append(i.text)

	#print(course_code)

	# course name
	course_name = []

	course_name_temp = d.find_all('tr', {'valign' : 'TOP'})
	for i in course_name_temp:
		cn = i.find_all('font', {'size' : '2'})
		full_cn = cn[3]
		cut_cn = str(full_cn)[15:]
		sp_cn = cut_cn.split('<')
		cn_done = sp_cn[0]
		course_name.append(cn_done)

	#print(course_name)

	# teacher name
	teacher_name = []
	teacher_name_temp = d.find_all('tr', {'valign' : 'TOP'})

	# for i in teacher_name_temp:
	# 	tn = i.find_all('font', {'size' : '2'})
	# 	full_tn = tn[4]
	# 	name = str(full_tn.text).encode('ISO-8859-1').decode('ISO-8859-11')
	# 	teacher_name.append(name)

	for ta in teacher_name_temp:
		all_teach_name = ''
		tn = ta.find_all('font', {'size' : '2'})
		full_tn = tn[4]
		names = str(full_tn).encode('ISO-8859-1').decode('ISO-8859-11')

		spli = names.split('<br/>')

		if len(spli) == 2: #for 1 name
			first_name = spli[1].split(';">')
			first_name = first_name[len(first_name) - 1].split('</font>')
			first_name = first_name[0]
			all_teach_name += first_name
		elif len(spli) == 3: #for 2 name
			first_name = spli[1].split(';">')
			first_name = first_name[len(first_name) - 1]
			all_teach_name += first_name + '\n'

			last_name = spli[len(spli)-1].split('</font>')
			last_name = last_name[0]
			all_teach_name += last_name
		else: #for more than 2 name
			first_name = spli[1].split(';">')
			first_name = first_name[len(first_name) - 1]
			spli.pop(0)
			spli.pop(0)
			last_name = spli[len(spli)-1].split('</font>')
			last_name = last_name[0]
			spli.pop(len(spli)-1)

			# print(first_name)
			# for i in spli:
			# 	print(i)
			# print(last_name)

			all_teach_name += first_name + '\n'
			for i in spli:
				all_teach_name += i + '\n'
			all_teach_name += last_name
		teacher_name.append(all_teach_name)
	#print(teacher_name)

	# course room
	course_room = []

	course_room_temp = d.find_all('tr', {'valign' : 'TOP'})

	for i in course_room_temp:
		cr = i.find('u')
		try:
			full_cr = cr.text
		except:
			full_cr = 'N/A'
		course_room.append(full_cr)

	#print(course_room)

	for i in range(len(course_code)):
		row.append([course_code[i], course_name[i], teacher_name[i], course_room[i]]) #add to row

	try:
		next_url = d.find_all('td', {'colspan' : '3'})
		next_url = next_url[0].find_all('a')
		if page == 1:
			next = next_url[0]['href']
		else:
			next = next_url[1]['href']
		url = 'https://web.reg.tu.ac.th/registrar/' + thai_text(str(next).encode('ISO-8859-1').decode('ISO-8859-11'))
		page += 1
		#print(url)
	except:
		print('No more page')
		break

try:
	df = pd.DataFrame(row, columns=['Course Code', 'Course Name', 'Teacher Name', 'Course Room'])
	df.to_csv('course.csv', index=False, encoding='utf-8-sig')
	print('Saved to course.csv file.')
	print('Done. :D   By.P3TCH')
except:
	print('Error to save csv file. :(')




