import csv
import logging

import pdb

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from sqlalchemy import func

from datetime import datetime

from collections import defaultdict

from sys import argv


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.NOTSET)

Base = declarative_base()

class Google(Base):
	__tablename__ = 'test'
	id = Column(Integer, primary_key = True)
	test_suite_name = Column(String(2**11), nullable = False)
	test_suite_mapped_id = Column(String(2**7), nullable = False)
	change_request = Column(Integer, nullable = False)
	stage = Column(String(2**7), index = True, nullable = False)
	test_status = Column(String(2**7), index = True, nullable = False)
	launch_time = Column(DateTime, nullable = False)
	execution_time = Column(Integer, nullable = False)
	test_size = Column(String(2**7), index = True, nullable = False)
	shard_number = Column(Integer, nullable = False)
	run_number = Column(Integer, nullable = False)
	test_language = Column(String(2**7), index = True, nullable = False)

	def __init__(self, test_suite_name, test_suite_mapped_id, change_request, stage, test_status, launch_time, execution_time, test_size, shard_number, run_number, test_language):
		self.test_suite_name = test_suite_name
		self.test_suite_mapped_id = test_suite_mapped_id
		self.change_request = change_request
		self.stage = stage
		self.test_status = test_status
		self.launch_time = launch_time
		self.execution_time = execution_time
		self.test_size = test_size
		self.shard_number = shard_number
		self.run_number = run_number
		self.test_language = test_language

	def __repr__(self):
		return "<Google(mapped_id='%s', change_request='%d', shard_number='%d', status='%s', launch_time='%s', execution_time='%d', test_size='%s', test_language='%s')>" \
		% (self.test_suite_mapped_id, self.change_request, self.shard_number, self.test_status, self.launch_time, self.execution_time, self.test_size, self.test_language)

# engine = create_engine('mysql+pymysql://rkrasniq@cse.unl.edu/rkrasniq?passwd=ob8{i5&')
engine = create_engine('mysql+pymysql://root@127.0.0.1/google?passwd=sunset820&')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# date_object = datetime.strptime('31:00:00:02', '%m:%H:%M:%S')
# print str(date_object)

# myobject = Google('ts1', 1, 'post', 'failed', date_object, 1111, 'large', 222, 333, 'py')

mapped_id = defaultdict(lambda: "")
idx = 1

# Comment out
"""
with open(argv[1], 'rb') as csvfile:
	data = csv.reader(csvfile, delimiter=',')	
	for row in data:
		try:			
			test_suite_name = row[0]
			if mapped_id[test_suite_name] == "":
				mapped_id[test_suite_name] = "T" + str(idx)
				idx+=1
				test_suite_mapped_id = mapped_id[test_suite_name]
			else:
				test_suite_mapped_id = mapped_id[test_suite_name]
			change_request = int(row[1])
			stage = row[2].upper()
			test_status = row[3].upper()		
			launch_time = datetime.strptime(row[4], '%d:%H:%M:%S')
			execution_time = int(row[5])
			test_size = row[6].upper()
			shard_number = int(row[7])
			run_number = int(row[8])
			test_language = row[9].upper()					

			session.add(Google(test_suite_name, test_suite_mapped_id, change_request, stage, test_status, launch_time, execution_time, test_size, shard_number, run_number, test_language))	
			session.commit()			

		except ValueError:			
			print str(row)

csvfile.close()				
# Comment out end
"""
# flaky_query = "SELECT * FROM google_dataset WHERE stage=\"POST\" GROUP BY test_suite_mapped_id, change_request, shard_number ORDER BY test_suite_mapped_id, change_request,shard_number ASC"
# session.query(Google).from_statement(flaky_query).all()

data = session.query(Google).filter(Google.stage == "POST") \
.order_by(Google.test_suite_mapped_id.asc(), Google.change_request.asc(), Google.shard_number.asc()) \
.all()
# .group_by(Google.test_suite_mapped_id, Google.change_request, Google.shard_number) \

prev = data[0]

f_to_p = 0
f_to_f = 0
p_to_f = 0
p_to_p = 0

trans_change_dict = defaultdict(lambda: [()])
for r in data[1:]:
	if r.test_suite_mapped_id == prev.test_suite_mapped_id and r.change_request == prev.change_request:
		trans_change_dict[prev.test_suite_mapped_id].append(prev.change_request)
		if r.test_status != prev.test_status:
			if prev.test_status == "FAILED":			
				f_to_p += 1							
			else:
				p_to_f += 1
		else:
			if prev.test_status == "FAILED":
				f_to_f += 1
			else:
				p_to_p += 1	
	elif r.test_suite_mapped_id == prev.test_suite_mapped_id and r.change_request != prev.change_request:
		trans_change_dict[prev.test_suite_mapped_id] = 

		for test_suite_mapped_id in trans_change_dict.keys():
			lst = trans_change_dict[test_suite_mapped_id]
			occurrence = dict((i,lst.count(i)) for i in lst)
			for change_request in occurrence:
				print "test_suite_mapped_id= %s\t change_request= %d, f->p transition: %d" % (test_suite_mapped_id, change_request, f_to_p / float(occurrence[change_request]))
				print "test_suite_mapped_id: %s\t change_request= %d, p->f transition: %d" % (test_suite_mapped_id, change_request, p_to_f) / float(occurrence[change_request])
				print "test_suite_mapped_id: %s\t change_request= %d, f->f transition: %d" % (test_suite_mapped_id, change_request, f_to_f) / float(occurrence[change_request])
				print "test_suite_mapped_id: %s\t change_request= %d, p->p transition: %d" % (test_suite_mapped_id, change_request, p_to_p) / float(occurrence[change_request])
		f_to_p = 0
		f_to_f = 0
		p_to_f = 0
		p_to_p = 0
	else:
		print "what up!"

	prev = r	

# print session.query(func.count(Google.id)).scalar() 
