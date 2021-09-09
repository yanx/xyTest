
- - - - - - - - - - -
Command Procedure
- - - - - - - - - - -

Run script with system - Command Prompt (Windows) / Terminal (Unix)


# Test Step - start with run - 
[run]

  - cd to the location. By default, the location is the folder of case-config

	goto = /Users/yanxin/git/goTestTools/testCenter/bin   
	
  - command script

	cmd = python3 test_login.py ::TYPE:: true  # run the command

Special Character replace :

::TYPE::  -  test type

::B::  -  %