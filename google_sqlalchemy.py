import csv
import logging

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from datetime import datetime
from sys import argv

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.NOTSET)

Base = declarative_base()

class Google(Base):
	__tablename__ = 'google_alchemy2'
	id = Column(Integer, primary_key = True)
	test_suite_name = Column(String(2**11), nullable=False)
	change_request = Column(Integer, nullable=False)
	stage = Column(String(2**7), index=True, nullable=False)
	test_status = Column(String(2**7), index=True, nullable=False)
	launch_time = Column(DateTime, nullable=False)
	execution_time = Column(Integer, nullable=False)
	test_size = Column(String(2**7), index=True, nullable=False)
	shard_number = Column(Integer, nullable=False)
	run_number = Column(Integer, nullable=False)
	test_language = Column(String(2**7), index=True, nullable=False)

	def __init__(self, test_suite_name, change_request, stage, test_status, launch_time, execution_time, test_size, shard_number, run_number, test_language):
		self.test_suite_name = test_suite_name
		self.change_request = change_request
		self.stage = stage
		self.test_status = test_status
		self.launch_time = launch_time
		self.execution_time = execution_time
		self.test_size = test_size
		self.shard_number = shard_number
		self.run_number = run_number
		self.test_language = test_language


engine = create_engine('mysql+pymysql://root@127.0.0.1/google?passwd=sunset820&')

Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# date_object = datetime.strptime('1:00:00:02', '%m:%H:%M:%S')
# print str(date_object)

# myobject = Google('ts1', 1, 'post', 'failed', date_object, 1111, 'large', 222, 333, 'py')

# Comment out
with open(argv[1], 'rb') as csvfile:
	data = csv.reader(csvfile, delimiter=',')	
	for row in data:
		try:			
			test_suite_name = row[0]
			change_request = int(row[1])
			stage = row[2].upper()
			test_status = row[3].upper()		
			launch_time = datetime.strptime(row[4], '%m:%H:%M:%S')
			execution_time = int(row[5])
			test_size = row[6].upper()
			shard_number = int(row[7])
			run_number = int(row[8])
			test_language = row[9].upper()					

			session.add(Google(test_suite_name, change_request, stage, test_status, launch_time, execution_time, test_size, shard_number, run_number, test_language))	
			session.commit()			

		except ValueError:			
			print str(row)

csvfile.close()				
# Comment out end