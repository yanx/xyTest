
- - - - - - - - - - -
JMeter Procedure
- - - - - - - - - - -

Run script with system - Command Prompt (Windows) / Terminal (Unix)


# Test Step - start with run - 
[run]

  - cd to the folder contains jmx file. By default, the location is the folder of case-config

	goto = test_jmeter/user_active/  
	
jmx = user_active_full # the jmx file name is user_active_full.jmx

users = 300    # run 300 users

rampup = 30    # in 30 seconds

loops = 10    # loops 10 times

csv = image_ids.csv, image_ids2.csv, image_ids3.csv    #  need the three files when run jmx

