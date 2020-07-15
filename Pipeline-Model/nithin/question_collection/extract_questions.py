import csv
import random
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from os import listdir
from os.path import isfile, join

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
def main():
	# table = random.randint(0,300)
	# file = "Responses:"+str(table) +".csv"
	# for i in range(tables):
	all_entries = []
	onlyfiles = [f for f in listdir('responses') if isfile(join('responses', f))]
	# onlyfiles = sorted(onlyfiles)
	for f in onlyfiles:
		file = f
		table = f.split(':')[1].split('.')[0]
		print(table)
		try:
			fh = open('responses/' + file, 'r')
			csv_reader = csv.reader(fh, delimiter=',')
			line_count = 0
			COLUMN_NAMES = {
				'Timestamp':[0], 
				'Email Address':[1], 
				'Question:':[2,6,10,14,18,22,26,30,34,38], 
				'Row(s) that contain(s) the answer, separated by commas:':[3,7,11,15,19,23,27,31,35,39], 
				'Answer Text:':[4,8,12,16,20,24,28,32,36,40], 
				'Question Type:':[5,9,13,17,21,25,29,33,37,41]
			}  
			
			for row in csv_reader:
				if line_count == 0:
					
					line_count += 1
				else:
					if not row[1]:
						continue
					print(str(table) + " " + row[1])
					table_id = str(table)
					email = row[1]

					item_row = [table_id,email]
					# print(row[COLUMN_NAMES['Question:'][0]])
					for index in COLUMN_NAMES['Question:']:
						if row[index]:
							all_entries.append(item_row + [row[index]] + [row[index+2]] + [row[index + 3]])
							# print(row[index])	

					line_count += 1
		except IOError:
			print(file + " not found")
	all_entries = sorted(all_entries,key=lambda x: int(x[0]))
	all_entries.insert(0,['Table id','Email','Question','Answer','QuestionType'])
	# print(all_entries)
	with open("seeeded_questions.csv","w") as out_csv:
		csvWriter = csv.writer(out_csv,delimiter=',')
		csvWriter.writerows(all_entries)
	# print('Processed {line_count} lines.')

if __name__ == '__main__':
	main()
	
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server()
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('drive', 'v3', credentials=creds)
	folder_id = '1a3jZUUSz0KFNzlXsfqXGz5cEWF49o98c'
	file_metadata = {
		'name': 'seeeded_questions.csv',
		'mimeType': 'application/vnd.google-apps.spreadsheet',
		'parents': [folder_id]
	}
	media = MediaFileUpload('seeeded_questions.csv',
							mimetype='text/csv',
							resumable=True)
	file = service.files().create(body=file_metadata,
										media_body=media,
										fields='id').execute()
	print ('File ID: ' + file.get('id'))


