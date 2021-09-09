import os
import sys
import time
import re
import shutil
import filecmp
import traceback
import configparser
from xyTest.util.format_operation import OPERATION_FORMAT

class OperationFile(object):

	""" 
	An abstract class
	"""
	__instance = None

	def __init__(self,
				 name="OperationFile",
				 *args, **kwargs):
		"""	 """

		self.name = name
		self.set_char_constant()
		self.set_file_constant()
		self.set_base_object()
#		self.set_log_location()

	def set_char_constant(self):
		# in db
		self.ch_default_root = "DEFAULT_FILE_ROOT"
		
		self.ch_split = "-::-"
		self.ch_special ="&&"
		self.ch_dic_split = "{:}"
		self.ch_dic_equal = "{=}"
		self.ch_outside = "{OUTSIDE}"
		self.ch_pass = "!!!PASS"
		self.ch_fail = "!!!FAIL"
		self.ch_nothing = "!!!Nothing"
		
		self.lst_ch_url = ['http://', 'https://', 'ftp://']
		
		self.false_value = [None, 'None', 'none', 'NONE', False, 'False', 'false', 'FALSE', 'NO', 'No', 'no']
		self.empty_value = ["", '', " ", "  ", "   ", (), [], {}, '()','[]', '{}']
		self.zero_value = ['0', '0.0', '0.00', 0, 0.0, 0.00, 'Zero', 'zero', 'ZERO']
		self.bad_all = self.false_value + self.empty_value + self.zero_value
		
		self.yes_value = ['yes', 'Yes', 'YES', 'True', 'TRUE', True, 'true', 'OK', 'ok']

		self.accepted_readable_character = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
							 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
							 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
							 '-', '_', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

		self.accepted_writable_character = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
								 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
								 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
								 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
								 '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
								 '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '=', '+',
								 '(', ')', '[', ' ]', '{', '}', ' ',
								 '?', ',', '.', '|', '<', '>',
								 '/', '\\', '\'', '"', ':', ';']

		self.unaccepted_character = [u'\u0193' , ]
		
		# To store log and other values of case/test/session
	def set_base_object(self):
		self.base_object = self
		self.current_object = self

	def set_current_object(self, obj):
		self.current_object = obj
		
		# For log and config files
	def set_file_constant(self):
		self.uilog = None
		self.info = {'log':[]}
		self.admin_mode = True
		
		self.format_config = '.ini'
		self.format_env = '.xml'
		self.general_count = 0
		self.len_max_path = 250
		
		self.path_user_documents = self.get_user_documents()
# 		self.path_tmp_dir = self.get_tmp_dir()

# === === === === === === === === === === === ===
# Log/Report ---
# === === === === === === === === === === === ===
	# temporary data between apps,
	def set_tmp_location(self, tmp=None):
		if not tmp:
			tmp = self.path_user_documents
		p_version = self.path_join(tmp, ["version"])
		self.path_tmp_version = self.create_dir(p_version)
	
	# Log folder
	def set_log_location(self, root=None):
# 		from xyTest.util.format_operation import OPERATION_FORMAT
# 		print ("set_log_location  =", root)
		if not root:
			root = self.path_user_documents

		self.name_debug = OPERATION_FORMAT.log_name(name='debug')
		p_debug = self.path_join(root, ["Debug"])
		self.path_debug = self.create_dir(p_debug)
		self.file_debug = self.path_join(self.path_debug, [self.name_debug])
		
		self.name_command = OPERATION_FORMAT.log_name(name='test')
		p_command = self.path_join(root, ["Testing"])
		self.path_command = self.create_dir(p_command)
		self.base_file_command = self.path_join(self.path_command, [self.name_command])
		self.file_current_command = self.base_file_command
# 		print ("self.file_current_command = ", self.file_current_command)
		p_report= self.path_join(root, ["Report"])
		self.path_report = self.create_dir(p_report)


	def set_command_log_file(self, ses):
		self.path_current_command = None
		self.file_current_command = None
# 		from xyTest.util.format_operation import OPERATION_FORMAT

		try:
			base_name=  '%s_%s' % ('test', ses)
			name_sess = OPERATION_FORMAT.log_name(name=base_name)
			if name_sess:
				self.file_current_command = self.path_join(self.path_command, [name_sess])
		except: 
			print ("Error - OperationFile.set_command_log_file - cat= %s" % str(ses))
			self.file_current_command = self.base_file_command
			

	def set_test_log_folder(self, nam):
		self.path_current_command = None
		self.path_current_command = self.path_join(self.path_command, [nam])
		if self.admin_mode:
			OPERATION_FILE.create_dir(self.path_current_command)
		return self.path_current_command
		
	def set_case_log_file(self, obj, casename):
		self.file_current_command = None
		try:
			self.current_object = obj
			self.file_current_command = self.path_join(self.path_current_command, [str(casename)+'.log'])
		except: 
			print ("Error - OperationFile.set_case_log_file - %s - %s" % (self.path_current_command, casename))
			self.set_suite_log_file()
			pass
		
		return self.file_current_command

	def set_suite_log_file(self, obj=None):
		self.file_current_command = self.base_file_command
		if obj == None:
			self.current_object = self.base_object
		else:
			self.current_object = obj

# === === === === === === === === === === === ===
# Boolean is_ ---
# === === === === === === === === === === === ===

	def is_true(self, v):
		if v in self.bad_all:
			return False
		else:
			return True


	def is_empty(self, v):
		if v in self.empty_value:
			return True
		else:
			return False

	def is_zero(self, v):
		if v in self.zero_value:
			return True
		else:
			return False

	def is_yes(self, v):
		str_v = str(v).lower().strip()
		if str_v in self.yes_value:
			return True
		else:
			return False

		
	def is_url(self, v):
		for ch_url in self.lst_ch_url:
			if ch_url in v:
				return True
		return False


	def is_string(self, s):
		return isinstance(s, str)
# 		PY3 = sys.version_info[0] == 3
# 		if PY3:
# 			return isinstance(s, str)
# 		else:
# 			return isinstance(s, basestring)
	# list
	def are_eq(self, a, b):
		return set(a) == set(b) and len(a) == len(b)
	

	# zip file.  check file modify time.  If doesn't change, it is complete
	def is_complete(self, fi):
		check_time = 100
		mtime1 = os.path.getmtime(fi)
		time.sleep(check_time)
		mtime2 = os.path.getmtime(fi)

		if mtime1 == mtime2:
			return True
		else:
			return False

	# try obj attribute
	def is_true_attr(self):
		pass

	# math
	def try_divide(self, a, b):
		if self.is_zero(b):
			return a/0.0001
		else:
			return a/b

# === === === === === === === === === === === ===
# string / list / dictionary operation ---
# === === === === === === === === === === === ===
	# dic key --> value
	def get_key_value(self, d, k):
		if isinstance(d, dict):
			ks = d.keys()
			if k in ks:
				return d[k]
		return False

	def check_key_value(self, d, k):
		value = self.get_key_value(d, k)
		if self.is_true(value):
			return True
		return False
	
	# dic value --> key
	def get_value_key(self, d, val):
		try:
			lst = []
			for k, v in d.items():
				if v == val:
					lst.append(k)
					
			return lst
		except Exception as e:
			msg = "%s - %s \n Eror: %s" % (self.name, "get_value_key", str(e))
			self.sys_error_message(msg)

	# list - check if all list vale is true
	def list_range_is_true(self, d, num):
		for x in range(num):
			if not self.is_true(d[x]):
				return False
		return True
	
	# list --> list
	def remove_duplicate(self, lst, ignore=[]):
		if (type(lst) != type([])) or (lst == []):
			return lst
		else:
			newlist = []

			for i in lst:
				add = False
				i=i.decode('utf-8', 'ignore')
				if ignore:
					for j in ignore:
						if (j in i) and (i not in newlist):
							add = True
							
				if add:
					newlist.append(i)

			return newlist


	def sum_of_list(self, first, second):
		
		return [x + y for x, y in zip(first, second)]
	

	# order with pre- int value
	def order_of_list(self, lst):
		d = {}
		result= []
		for k in lst:
			l_k = k.split('_')
			try:
				one_int = int(l_k[0])
				d[one_int] = k
			except:	 # gl_first
				lst.sort()
				return lst
			
		ind = d.keys()
		ind.sort()
		for i in ind:
			result.append(d[i])
		return result
			

	# string/list --> list
	# return item position in a list
	def list_item_position(self, lst, itm):
		return [i for i,x in enumerate(lst) if x == itm]


	# string/list --> list
	def get_error(self, lst, string_error="error"):
		get_result = []
		if type(lst) == type([]):
			for itm in lst:
				sub_result = self.get_error(itm, string_error)
				get_result = get_result + sub_result
		elif type(lst) == type(""):
			if string_error in lst:
				get_result.append(lst)

		else:
			return get_result

		return get_result


	# Dictionary --> list
	def get_element_in_dic(self, d={}):
		"""return a list of all element in a dictionary include elements of sub-dictionary  """
		lst = []
		if not d == {}:
#			for key in d.keys():
#				item = d[key]
			for key, item in d.items():
				if type(item) == type({}):
					lst = lst + self.get_element_in_dic(item)
				elif item != None:
					lst.append(item)
				else:
					pass

			return lst
		

	# dictionary --> string
	def dic_to_string(self, di, split='\n', ch=" : "):
		result = []
		if di:
			for k, v in di.items():
				str_v = self.get_str(v, split=split, ch=ch)
				k_v = ch.join([k, str_v])
				result.append(k_v)
			
		return split.join(result)
	
#		return split.join([ch.join((k, str(di[k]))) for k in sorted(di, key=di. get, reverse=rev)])

	# list --> string
	def list_to_string(self, lst, split='\n', ch=" : "):

		result = []
		if lst:
			for itm in lst:
				str_v = self.get_str(itm, split=split, ch=ch)
				result.append(str_v)
		return split.join(result)

	
	def get_str(self, ob, split='\n', ch=" : "):
		
		result = None
		if isinstance(ob, dict):
			result = self.dic_to_string(ob, split=split, ch=ch)
		elif isinstance(ob, list):
			result = self.list_to_string(ob, split=split, ch=ch)
		elif isinstance(ob, str):
			result = ob
		else:
			result = str(ob) 
		return result
	

	def get_limit_string(self, st, num=88):
		
		ch = str(st)
		if len(ch) < num:
			return ch
		else:
			return ch[0:num]+'...'


# === === === === === === === === === === === ===
# sub-folder Search Operations ---
# === === === === === === === === === === === ===

	# int - bit For example, 1k = 1024
	def get_folder_size(self, start_path='.'):

		total_size = 0
		for dirpath, dirnames, filenames in os.walk(start_path):
			for f in filenames:
				fp = os.path.join(dirpath, f)
				total_size += os.path.getsize(fp)
		return total_size

	# search if sub folder exists under 'path' 
	def exist_subfolder(self, path, ignore=[]):
		"""search if sub folder exists under 'path' """

		if not os.path.exists(path):
			self.sys_error_message("%s does not exist." % path)
			return False

		if os.path.isfile(path):
			self.sys_error_message("%s is a file." % path)
			return False
		
		for fn in os.listdir(path):
			dirfile = self.path_join(path, fn)
			if os.path.isdir(dirfile):
				if not fn in ignore:
					return True

		return False

	def get_dic_of_subfolder(self, head_dir):
		"""Return a dictionary of the full paths of sub-folder
		under directory 'head_dir'
		key: name of sub-folder
		value: full path of sub-folder """
		dic_dir = {}

		try:
			if os.path.isdir(head_dir):
				for fn in os.listdir(head_dir):
					dirfile = self.path_join(head_dir, fn)
					if os.path.isdir(dirfile):
						dic_dir[fn] = dirfile

		except Exception as msg:

			print("wrong path in file_operation.get_dic_of_subfolder() = ", head_dir)
			print (msg)
			dic_dir = {}
			pass


		return dic_dir

	def get_list_of_named_subfolder(self, head_dir, dir_name):
		"""Return a list of the full paths of the sub-directories
		under directory 'head_dir' named 'dir_name'"""
		dirList = []
		for fn in os.listdir(head_dir):
			dirfile = self.path_join(head_dir, fn)
			if os.path.isdir(dirfile):
				if fn.upper() == dir_name.upper():
					dirList.append(dirfile)
				else:
					dirList += self.get_list_of_named_subfolder(dirfile, dir_name)
		return dirList

# === === === === === === === === === === === ===
# file search operation ---
# === === === === === === === === === === === ===

	def get_dic_of_file(self, head_dir):

		"""Return a dictionary of the full paths file
		under directory 'head_dir'
		key: name of file
		value: full path of file """
		dic_file = {}

		if os.path.isdir(head_dir):
			for fn in os.listdir(head_dir):
				dirfile = self.path_join(head_dir, fn)
				if os.path.isfile(dirfile):
					dic_file[fn] = dirfile

		return dic_file

	def get_full_file_list(self, head_dir, sub_folder=False):
		"""Return a list of the full paths of files under directory 'head_dir'
		sub_folder : deep search in sub folder"""

		fileList = []
		for fn in os.listdir(head_dir):
			dirfile = self.path_join(head_dir, fn)
			if os.path.isdir(dirfile):
				if sub_folder:
					fileList += self.get_full_file_list(dirfile)
			else:
				fileList.append(dirfile)

		return fileList

	def get_full_file_list_advance(self, head_dir, includes=[], excludes=[], join_or=[]):
		import fnmatch

		# transform glob patterns to regular expressions
		re_includes = r'|'.join([fnmatch.translate(x) for x in includes])
		re_excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'
		re_join_or = r'|'.join([fnmatch.translate(x) for x in join_or])
		result = []

		for root, dirs, files in os.walk(head_dir):

			dirs[:] = [self.path_join(root, d) for d in dirs]
			# file name match join_or
			files = [f for f in files if re.match(re_join_or, f)]

			files = [self.path_join(root, f) for f in files]
			# exclude/include/
			if not excludes == []:
				files = [f for f in files if not re.match(re_excludes, f)]
			files = [f for f in files if re.match(re_includes, f)]

			for fname in files:
				result.append(fname)
		return result
	
	
	def get_regression_file_list(self, test_dir, file_type=[], ignore_folder=[], ignore_file=[], ignore=[]):
		
		import fnmatch
		
		re_file_type = r'|'.join([fnmatch.translate(x) for x in file_type])
		re_ignore_folder = r'|'.join([fnmatch.translate(x) for x in ignore_folder]) or r'$.'
		re_ignore_file = r'|'.join([fnmatch.translate(x) for x in ignore_file]) or r'$.'
		result = []

		for root, dirs, files in os.walk(test_dir):
			if not ignore_folder == []:
				dirs[:] = [d for d in dirs if not re.match(re_ignore_folder, d)]
			dirs[:] = [self.path_join(root, d) for d in dirs]

			if not ignore_file == []:
				files = [f for f in files if not re.match(re_ignore_file, f)]
				
			files = [f for f in files if re.match(re_file_type, f)]
			files = [self.path_join(root, f) for f in files]

			for fname in files:
				add_it = True
				for ig in ignore:

					if ig in fname:
						add_it = False
						break

				if add_it:
					result.append(fname)
		return result


	def get_named_file_list(self, head_dir, name, sub_folder=True, force=False):
		"""search name of files under head_dir, the name can be a string list """
		list_lower = []
		if type(name) == type([]):
			for f in name:
				list_lower.append(str(f).lower())
		elif type(name) == type(""):
			list_lower.append(str(name).lower())
		else:
			msg = "Failed to file.get_named_file_list : name = %s" % (str(name))
			print  (msg)

		fileList = []
		for fn in os.listdir(head_dir):
			dirfile = self.path_join(head_dir, fn)
			if os.path.isdir(dirfile):
				if sub_folder:
					fileList += self.get_named_file_list(dirfile, name, sub_folder, force)
			else:
				file_lower = fn.lower()
				if force:
					for item in list_lower:
						if str(item) in file_lower:
							fileList.append(dirfile)
							break
				elif file_lower in list_lower:
					fileList.append(dirfile)
				else:
					pass

		return fileList

	def has_named_file(self, head_dir, name):
		for dirname, dirnames, filenames in os.walk(head_dir):
			for filename in filenames:
				if name in filename:
					return True

		return False

	def get_pre_ext_file_list(self, head_dir, pre, ext, sub_folder=False):
		"""Return a list of the files under directory 'head_dir' with pre_*.ext
		sub_folder : deep search in sub folder"""

		filelist= []
		for fn in os.listdir(head_dir):
			dirfile = self.path_join(head_dir, fn)
			if os.path.isdir(dirfile):
				if sub_folder:
					filelist += self.get_pre_ext_file_list(dirfile, pre, ext, sub_folder)
			else:
				if fn.startswith(pre) and fn.endswith(ext):
					filelist.append(dirfile)

		return filelist

# === === === === === === === === === === === ===
# Path , file Operation, file name and ext ---
# === === === === === === === === === === === ===
# 	def rmdir(self, path):
# 		if not os.path.isdir(path):
# 			self.sys_error_message("%s does not exist. Remove operation not performed." % path)
# 			return
# 		shutil.rmtree(path)

	def delete(self, path):
		if os.path.isdir(path):
			shutil.rmtree(path)
		elif os.path.isfile(path):
			os.remove(path)
		else:
			self.sys_error_message("%s does not exist. Delete operation not performed." % path)


	def check_path_long_name(self, path):
		# remote submit path does not allow "\\\\?\\" 
		try:
			if str(path)[0] in ['/', '\\']:
				return path
		except:
			pass
		try:
			if sys.platform in ['cygwin', 'win32']:
				prefix = u"\\\\?\\" 
				if "/" in path :
					path = path.replace("/", "\\")
				new_path = prefix + os.path.normpath(path)
				return new_path
			else:
				return path

		except Exception as e:
#			self.message_exception()
			msg= "error in check_path_long_name:", e
			print  (msg)


	def move(self, srcPath=None, destPath=None, force=False, check=False):
		"""	 """
		if (not check):
			if (
				(None == srcPath) or 
				(None == destPath) or 
				(not os.path.exists(srcPath)) or 
				(os.path.exists(destPath) and not force)
				):
				return
		else:
			if None == srcPath:
				self.sys_error_message("Source equal None. Move operation not performed.")
				return
	
			if None == destPath:
				self.sys_error_message("Destination equal None. Move operation not performed.")
				return
	
			if not os.path.exists(srcPath):
				self.sys_error_message("Source %s does not exist. Move operation not performed." % srcPath)
				return 
	
			if os.path.exists(destPath) and not force:
				self.sys_error_message("Destination %s already exists. Move operation not performed." % destPath)
				return
		shutil.move(srcPath, destPath)

	def create_dir(self, path, errorOnExist=False):
		"""	 """
		str_path = str(path)
		if os.path.isdir(str_path):
			if errorOnExist:
				self.sys_error_message("Path %s already exists. Path not performed." % str_path)
			return str_path
		os.makedirs(str_path)
		return str_path


	def check_make_dirs(self, path):
		str_path = str(path)
		try:
			if not os.path.exists(str_path):
					if (len(path) > self.len_max_path):
						if (not os.path.exists(self.check_path_long_name(str_path))):
							os.makedirs(self.check_path_long_name(str_path))
					else:
						os.makedirs(str_path) # os.makedirs( str_path, 0755 );
		except Exception as e:
			msg = "os.makedirs - %s \n Eror: %s" % (str_path, str(e))
			self.sys_error_message(msg)
			pass



	def copy(self, srcPath, destPath, force=False, check=False):
		"""	 """
		if (not check):
			if (
				(not os.path.exists(srcPath)) or 
				(os.path.exists(destPath) and not force)
				):
				return
		else:
			if not os.path.exists(srcPath):
				self.sys_error_message("Source %s does not exist. Copy operation not performed." % srcPath)
				return
			if os.path.exists(destPath) and not force:
				self.sys_error_message("Destination %s already exists. Copy operation not performed." % destPath)
				return
		if os.path.exists(destPath) and force:
			self.delete(destPath)
		if os.path.isdir(srcPath):
			self.copy_dir(srcPath, destPath)
		else:
			self.check_copy_file(srcPath, destPath)
	
	
	def copy_file(self, srcPath, destPath, ext=[], size=0):

		"""copy file to dest dir.  for filter file ext """
		if os.path.isdir(srcPath):
			for fn in os.listdir(srcPath):
				dirfile = self.path_join(srcPath, fn)
				if os.path.isfile(dirfile):
					this_copy = False
					if (ext == []) or (not isinstance(ext, list)):
						this_copy = True
					else:
						this_ext = self.get_file_extension(fn)
						if this_ext in ext:
							this_copy = True
					
					if this_copy and size:
						size_file = os.path.getsize(dirfile)
						if size_file > size*1024:
							this_copy = False

					if this_copy:
						file_to = self.path_join(destPath, fn)
						self.copy(dirfile, file_to)

		return 
	
	# check file before copy.  fix too long file path
	def check_copy_file(self, from_, to_):
		
		try:
			### copy file if too long
			if (len(from_) > self.len_max_path) or (len(to_) > self.len_max_path):
				new_from_ = self.check_path_long_name(from_)
				new_to_ = self.check_path_long_name(to_)
				shutil.copyfile(new_from_, new_to_)
			else:
				shutil.copyfile(from_, to_)
		except Exception as e:
			msg = "shutil.copyfile - from - %s - to - %s - \n Eror: %s" % (from_, to_, str(e))
			self.sys_error_message(msg)
			pass
		
		
	def copy_dir(self, source, target, lst_dir_ignore=None, lst_file_ignore=None):
		
		self.check_make_dirs(target)
		source = self.format_path(source)
		target = self.format_path(target)

		if not lst_dir_ignore:
			lst_dir_ignore = ['.svn']
		if not lst_file_ignore:
			lst_file_ignore = ['.pyc', '.pyo', '.fs']

		lst_file_fullname = ['.DS_Store', 'Thumbs.db']
		
		for root, dirs, files in os.walk(source):
			for dir_ignore in lst_dir_ignore:
				if dir_ignore in dirs:
					dirs.remove(dir_ignore)  # don't visit .svn directories

			for this_file in files:
				if os.path.splitext(this_file)[-1] in lst_file_ignore:
					continue
				
				if this_file in lst_file_fullname:
					continue

				from_ = self.path_join(root, this_file)
				to_ = from_.replace(source, target, 1)

				to_directory = os.path.split(to_)[0]
				
				self.check_make_dirs(to_directory)

				### copy file if too long
				self.check_copy_file(from_, to_)
				
	
# 	def opj(self, path):
# 	    """Convert paths to the platform-specific separator"""
# 	    str = apply(os.path.join, tuple(path.split('/')))
# 	    # HACK: on Linux, a leading / gets lost...
# 	    if path.startswith('/'):
# 	        str = '/' + str
# 	    return str

	def opj(self, path):
		"""Convert paths to the platform-specific separator"""
		st = os.path.join(*tuple(path.split('/')))
		# HACK: on Linux, a leading / gets lost...
		if path.startswith('/'):
			st = '/' + st
		return st


	def is_python_script(self, path):
		"""	"""
		if os.path.isfile(path):
			extention = self.get_file_extension(path)
			if extention == 'py':
				return True
		return False

	# 
	def check_win_path(self, path):
		result = str(path)
		if sys.platform == 'win32':
			result = result.replace("/", "\\")
		return result


	def format_path(self, path):
		result = str(path).replace("\\", "/")
		return result
	
	# get parent/grand parent folder path
	def path_off(self, path, par=1):
		result = str(path)
		try:
			for i in range(0, par):
#				result = os.path.split(result)[0]
				result = self.get_parent_dir(result)
			return result

		except Exception as msg:
			self.sys_error_message(msg)


	def path_join(self, path, lst=[]):
		result = str(path)
		new_lst = []
		new_path = path
		
		if not (self.is_true(path) and self.is_true(lst)):
			return path
		try:
# 			if isinstance(lst, basestring) or isinstance(lst, str):
			if isinstance(lst, str):
				if "\\" in lst or "/" in lst:
					lst = lst.replace("\\", "/")
					new_lst = lst.split("/")
				else:
					new_path = os.path.join(path, str(lst))
					result = str(new_path).replace("\\", "/")
					return result
			elif type(lst) == type([]):
				new_lst = lst
			else:
				msg = "Error in util.file.path_join.  Unknow lst: \n Path = %s\n list = %s" % (path,  str(lst))
				self.sys_error_message(msg)
				return path

			for item in new_lst:
				if item !='':
					new_path = self.path_join(new_path, str(item))

			return new_path

		except Exception as msg:
			er = "Error in util.file.path_join: \n Path = %s\n list = %s \n Exception = " % (path,  lst, msg)
			self.sys_error_message(er)
			return path


	def url_path_join(self, parts):
		return '/'.join([x.strip('/') for x in parts])


	def get_last_dir(self, path):
		"""get last directory name """
		
		strPath = str(path)

		if not os.path.isdir(strPath):
			self.sys_error_message("The folder %s is not exist." % strPath)
			return None
		
		return os.path.basename(os.path.normpath(path))


	def get_parent_dir(self, path):
		dir_parent =  os.path.abspath(os.path.join(path, os.path.pardir))
		return dir_parent


	# remove part (shorter) from a long path 
	def get_subpath(self, shorter, longer):
		""" longer - shorter """
		remove = self.format_path(shorter)
		full_path = self.format_path(longer)
		result = full_path.replace(remove, '')
		return result


	def get_file_name(self, path):
		result = None
		strPath = str(path)
		try:
			if "/" in strPath:
				fileName = strPath.split("/")[-1]
			elif "\\" in strPath:
				fileName = strPath.split("\\")[-1]
			result = fileName
		except:
			pass
		
		return result
	
	# remove short from long path, and return others as a string
	def get_name_subpath(self, shorter, longer):
		
		remove = self.format_path(shorter)
		full_path = self.format_path(longer)
		sub = full_path.replace(remove, '')
		replac = sub.replace("/", '_')
		reslt = result = replac.split(".")[0]
		if reslt[0] == '_':
			result = result[1:]
		return result
	

	def get_file_name_and_ext(self, path):
		nam = None
		ext = None
		file_name = ""
		try:
			if "/" in path or "\\" in path:
				file_name = self.get_file_name(str(path))
			else:
				file_name = str(path)
			if "." in file_name:
				na_split = file_name.split(".")
				nam = na_split[0]
				ext= na_split[-1]
		except:
			pass
		return nam, ext


	def get_file_extension(self, path):
		nam, ext = self.get_file_name_and_ext(path)
		return ext


	def get_file_short_name(self, path):
		nam, ext = self.get_file_name_and_ext(path)
		return nam


	def extend_file_name(self, name, prex=None, suffix=None, ext=None):
		try:
			result = None
			file_name = str(name)
			na_split = file_name.split(".")
			na = file_name[0:file_name.rindex(".")]
			et= na_split[-1]

			if prex:
				na = str(prex) + na
			if suffix:
				na = na + str(suffix)
			if not ext:
				ext = et
				
			result = "%s.%s" % (na, ext)
			return result
	
		except:
			print ("Failed - extent_file_name")
		
		return result

# === === === === === === === === === === === ===
# File Input and output ---
# === === === === === === === === === === === ===
	# file open
	def file_read(self, path):
		if not os.path.exists(path):
			self.sys_error_message("%s not exists." % path)
			return None
		try:
			if os.path.isfile(path):
				fileHandle = open (path, 'r')
				content = fileHandle.read()
				fileHandle.close() 
				return content
			else:
				return None
			
		except Exception as msg:
			self.sys_error_message(str(msg))


	def file_read_json(self, fi):
		if os.path.isfile(fi):
			import json
			with open(fi, "r") as f:
				json_data = json.load(f)
# 			print ('json_data = ', json_data)
			return json_data
		else:
			self.sys_error_message("not exists - json file - %s" % str(fi))
			return None

	def file_read_readme(self, pa, fi="readme.md"):
		filetext = None
		path_readme = self.path_join(pa, fi)
# 		print ("path_readme = ", path_readme)
		if os.path.isfile(path_readme):
			filetext = self.file_read(path_readme)
			return filetext
		else:
			return False


	def file2list(self, path):
		try:
			if os.path.isfile(path):
				fileHandle = open(path, 'r')
				content = fileHandle.readlines()
				fileHandle.close() 
				new_contnet = []
				for li in content:
					new_li = str(li).strip()
					for ch in self.unaccepted_character:
						if ch in new_li:
							print ("Warning --- remove %s from %s, in line - %s" % (ch, path, new_li))
							new_li = new_li.replace(ch, '')
					new_contnet.append(new_li)
				return new_contnet
			else:
				return []
			
		except Exception as msg:
			self.sys_error_message(msg)


	def file_to_dic(self, path, ch=None):

		dic_result = {}
		
		if not ch:
			ch = self.ch_split   #	"-::-"
			
		try:
			lst = self.file2list(path)
			for lin in lst:
				if ch in lin and len(lin) > 5:
					info_line = lin.split(ch)
					title = info_line[0].strip()
					value = info_line[1].strip()
					
					dic_result[title] = value
							
			return dic_result
			
		except Exception as msg:
			self.sys_error_message(msg)

	def dic_to_file(self, path, d, ch=None):
		if not ch:
			ch = self.ch_split   #	"-::-"
			
		data=""
		for k, v in d.items():
			val = str(k) + "	 " + self.ch_split + "	 " + str(v) + "\n"
			data += val
		
		self.file_write(path, data, "w")

		
	def file_write(self, path, data=None, flag="w"):
		try:
			fileHandle = open(path, flag)
		
			if data:
				new_data = self.get_str(data)
				fileHandle.write(new_data)
				
			fileHandle.close() 
			return True
	
		except Exception as msg:
			self.sys_error_message(msg)
			
			
	# report template file translate to report
	def tmp_to_file(self, dic_info, tmp, out=None, ch=None):
		if not ch:
			ch = self.ch_split   #	"-::-"
		lst_tmp = tmp
		
		try:
			if os.path.isfile(tmp):
				lst_tmp = self.file2list(tmp)
		except:
			pass
		
		if isinstance(lst_tmp, list):
			file_content = ''
			for line in lst_tmp:
				if ch in line:
					for k in dic_info.keys():
						if k in line:
							line = line.replace(k, str(dic_info[k]))
				file_content = file_content + line + "\n"
				
			if out:
				if self.is_true(file_content):
					try:
						self.file_write(out, file_content)
					except:
						msg = "tmp_to_file - Failed to write file: %s" % (str(out))
						self.sys_error_message(msg) 

			return file_content
		else:
			msg = "tmp_to_file - error in lst_tmp: %s" % (str(lst_tmp))
			self.sys_error_message(msg) 


	def write_a_report(self, nam, msg, typ='html'):
		try:
			path_html = self.path_join(self.path_report, nam)
	
			fileHandle = open(path_html, 'w')
			if typ=='html':
				msg = msg.replace('<br>', '')
			fileHandle.write(msg)
			fileHandle.close() 
			return path_html
		except: 
			print ("Error - OperationFile.write_a_report - name= %s" % str(nam))
			pass
			return False


# === === === === === === === === === === === ===
# Directory, clean, zip, upload	 --- 
# === === === === === === === === === === === ===
	def zipdir(self, zipath, output, ty='zip'):
		shutil.make_archive(output, 'zip', zipath)
		return zipath


	def unzipdir(self, zipfile):
		shutil.unpack_archive(zipfile)


	def clean_dir(self, top):
		# Delete everything reachable from the directory named in 'top',
		# assuming there are no symbolic links.
		# CAUTION:  This is dangerous!  For example, if top == '/', it
		# could delete all your disk files.
		for root, dirs, files in os.walk(top, topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))

	def clean_empty_dir(self, top):
		for root, dirs, files in os.walk(top,topdown=False):
			for name in dirs:
				fname = self.path_join(root,name)
				try:
					if not os.listdir(fname): #to check wither the dir is empty
						os.removedirs(fname)
				except:
					pass

	def clean_dir_day(self, head_dir, day=-1):
		dirList = []
		for fn in os.listdir(head_dir):
			dirfile = self.path_join(head_dir, fn)
			this_day = os.stat(dirfile).st_ctime
			day_diff = int((time.time() -this_day)/86400)
			
			if day > 0:
				if day_diff > day:
					self.delete(dirfile)


	def clean_dir_advance(self, top, size=None, lst_file=[], lst_dir=[]):
		# size: int K
		for root, dirs, files in os.walk(top):
			for file in files: 
				path_file = os.path.join(root, file)
				remove_file = False
				if lst_file:
					for n in lst_file:
						if n in file:
							remove_file = True
							break
				if (not remove_file) and size:
					size_file = os.path.getsize(path_file)
					if size_file > size*1024:
						remove_file = True
							
				if remove_file:
					try:
						os.remove(path_file)
						print ("remove file:  %s" % str(path_file))
					except Exception as msg:
						self.sys_error_message(msg)
						pass
		

	
	# backup with date
	def backup_dir(self, src, dest, title="_backup"):
			# get current time
		
		current_time = time.localtime(time.time())
		format_date_day = "%Y-%m-%d"
		current_date = time.strftime(format_date_day, current_time)

		name_folder = "%s_%s" % (title, current_date)
	
		path_folder = self.path_join(dest, [name_folder])
		print ("backup to %s\n" % path_folder)
		
		if os.path.isdir(path_folder):
			self.delete(path_folder)
			
		if not os.path.isdir(path_folder):
			os.mkdir(path_folder)
		
		# backup 
		lst_src = []
		if type(src) == type([]):
			lst_src = src
		else:
			lst_src.append(os.path.abspath(lst_src))
		
		for k in lst_src:
			if os.path.isdir(k):
				d_name = self.get_last_dir(k)
				n_path = self.path_join(path_folder, [d_name])
				self.copy_dir(k, n_path)
				print ( "Backup directory %s\n" % (k))
			elif os.path.isfile(k):
				f_name = self.get_file_name(k)
				f_path = self.path_join(path_folder, [f_name])
				self.copy(k, f_path)
				print ( "Backup file %s\n" % (k))
			else:
				print ( "Failed to backup %s, unknown path\n" % (k))

	
	# update new and modified file
	def upload_dir(self, source, target, lst_dir_ignore=None, lst_file_ignore=None):
	
		print ( "------ Start update folder %s from %s ------" % (target, source))
		self.check_make_dirs(target)
	
		if not lst_dir_ignore:
			lst_dir_ignore = ['.svn']
		if not lst_file_ignore:
			lst_file_ignore = ['.pyc', '.pyo', '.fs']
			
		lst_file_fullname = ['.DS_Store', 'Thumbs.db']
	
		for root, dirs, files in os.walk(source):
			for dir_ignore in lst_dir_ignore:
				if dir_ignore in dirs:
					dirs.remove(dir_ignore)  # don't visit .svn directories
			
			
			for this_file in files:
				if os.path.splitext(this_file)[-1] in lst_file_ignore:
					continue
				
				if this_file in lst_file_fullname:
					continue
	
				from_ = os.path.join(root, this_file)
				to_ = from_.replace(source, target, 1)
				to_directory = os.path.split(to_)[0]
				
				self.check_make_dirs(to_directory)
				do_copy = False
				if os.path.isfile(from_):
					if os.path.isfile(to_):
						
						# get modification time:
						from_m_t = os.path.getmtime(from_)
						to_m_t = os.path.getmtime(to_)
						# updated file should be copy
						if (from_m_t - to_m_t) > 10:
							if not filecmp.cmp(from_, to_):
								do_copy = True
					
					# new file added
					else: # if os.path.isfile(to_):
						do_copy = True

					if do_copy:
						try:
							if os.path.isfile(to_):
								print ( 'Removing old file %s ...' % (to_))
								os.remove(to_)
								
							print ( 'Copying %s to %s...' % (from_, to_))
							self.check_copy_file(from_, to_)
#							shutil.copyfile(from_, to_)
	
						except Exception as e:
							print ( "upload_dir - Error: ", e)
#							pass
	
		print ( "------ Finish update folder %s from %s ------" % (target, source))
	
# === === === === === === === === === === === ===
# operation file system ---
# === === === === === === === === === === === ===
	def get_tmp_dir(self):
		import tempfile
		path_tmp =  tempfile.gettempdir() 
		if not os.path.isdir(path_tmp):
			self.sys_error_message("Path Error: %s" % path_tmp)
			return None
		return path_tmp

	def get_user_documents(self):
		try:
			user_documents = os.path.expanduser(r'~/Documents')
	# 		print (user_documents)
			if not os.path.isdir(user_documents):
				self.sys_error_message("Path Error: %s" % user_documents)
				return None
			return user_documents
		except:
			return None

	
	def getHost(self, path):
		storageHostName = ""
		if len(path)> 0:
			path = self.format_path(path)
			# Determine what the path split character is
			backSlashCount = path.count("\\")
			frontSlashCount = path.count("/")
			
			if backSlashCount > 0 and frontSlashCount > 0:
				self.sys_error_message("Path Error: %s" % path)
				return None
			
			elif backSlashCount > 0:
				pathSeparator = "\\"
				
			else: 
				pathSeparator = "/"
				
			splitePath = path.split(pathSeparator)
		
			for j in range (0, len(splitePath)):
				if not splitePath[j] == '':
					storageHostName = splitePath[j]
					break
				
		return str(storageHostName)
	

# === === === === === === === === === === === ===
#  config - read and write ---
# === === === === === === === === === === === ===

	# translate config-path-option,  to absolute path
	def get_specail_path_option(self, val):
		try:
			result = str(val).strip()
			if self.ch_outside in result:
				result = val.replace(self.ch_outside, "")
			result = os.path.expandvars(result.strip())
			result = self.format_path(result.strip())
			
			if os.path.isabs(result):
				if os.path.isdir(result) or os.path.isfile(result):
					return result
				elif os.path.isdir(os.path.split(result)[0]) :
					return result
				else:
					print ("Warning - Could not find absolute pathname - %s - Please check your config " % (result))
					return False
			else:
				return False
		except:
			return False
			pass
	

	def read_ini_config(self, fi):
		try:
			if not os.path.isfile(fi):
				print ("Error: read_ini_config - No such file - %s " % str(fi))
				return False
			else:
				config = configparser.ConfigParser()
				config.optionxform=str
				config.read(fi)
				return config

	
		except Exception as e:
			print ("file_operation - read_ini_config- %s - Exception - %s" % ( str(fi), str(e)) )
	

	def pass_one_config_option(self, config, sec, opt, obj, atr, ty=None):
		try:
			get_opt = self.try_one_option(config, sec, opt, ty)
			setattr(obj, atr, get_opt)
			return True
		except Exception as e:
			msg = "pass_one_config_option - %s - %s - value=%s" % (sec, opt, get_opt)
			self.message_command(self, "Exception", msg, e)
			return False


	def try_one_option(self, config, sec, opt, ty=None):
		try:
			if config.has_option(sec, opt):
				val = config.get(sec, opt)
				# random string
				if "--SR--" in val:
					rs = OPERATION_FORMAT.str_random()
					val = val.replace("--SR--", rs)
				if "--SL--" in val:
					rsl = OPERATION_FORMAT.str_random_long()
					val = val.replace("--SL--", rsl)
				
				val_new = None
				if ty == 'int':
					val_new = config.getint(sec, opt)
				elif ty == 'list':
					if ',' in val:
						val_new = [x.strip() for x in val.split(',')]
					else:
						val_new = val.split()
				elif ty == 'dic':
					if ',' in val:
						val_lst = [x.strip() for x in val.split(',')]
					else:
						val_lst = val.split()
					lst = []
					for itm in val_lst:
						items = itm.split(":")
						if len(items) != 2:
							self.message_command(self, "Error", 'Error dic item - '+itm)
						else:
							lst.append((items[0], items[1]))
					val_new = dict(lst)
				else:
					val_new = val
				return val_new
			else:
				return None
			
		except Exception as e:
			msg = "try_one_option - %s - %s - value=%s" % (sec, opt, val)
			self.message_command(self, "Exception", msg, e)
			return None

		
# >>> from ConfigParser import ConfigParser
# >>> config = ConfigParser()
# >>> config.read('test.ini')
# >>> config._sections
# {'First Section': {'var': 'value', '__name__': 'First Section', 'key': 'item'}, 'Second Section': {'__name__': 'Second Section', 'otherkey': 'otheritem', 'othervar': 'othervalue'}}
# >>> config._sections['First Section']
# {'var': 'value', '__name__': 'First Section', 'key': 'item'}

# === === === === === === === === === === === ===
#  file/log write and print ---
# === === === === === === === === === === === ===

	# Create a function that can print progress on one line dynamically
	def print_dynamic(self, msg):
		sys.stdout.write("\r" + msg)
		sys.stdout.flush()


	def sys_error_message(self, msg):
# 		print >> sys.stderr, msg
		sys.stderr.write( msg )



	def debug(self, cls, msg):

		import inspect
		
		name_class = cls.__class__.__name__
		name_caller = inspect.stack()[2][3]

		if type(msg) == type([]):
			mew_msg = self.list_to_string(msg, split=' | ')
		else:
			mew_msg = str(msg)
		
		t=time.localtime(time.time())
		current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
		
# 		current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
		data = "DEBUG [%s] \t[ Class: %s ] \t[ Function: %s ] \t%s\n" % (current_time, str(name_class), str(name_caller), mew_msg)
		
		self.sys_error_message(data)

		try:
			self.file_write(self.file_debug, data, 'a')
		except Exception as e:
			msg = "Error in OperationFile.debug - Exception e=" , e
			print (msg)
			pass

			
	def message_command(self, cls, level, ms='No-Message', e=None):
		
		try:
			try:
				name_class = cls.__class__.__name__
			except:
				name_class = str(cls)
				
			t=time.localtime(time.time())
			current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
			lel = str(level).upper()
# 			current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
			logmsg = "[Class: %s - Level: %s] %s %s"  %  (name_class, lel, self.ch_split, str(ms))
# 			data = "\n%s - [Class: %s - Level: %s] %s %s\n"  %  (current_time, name_class, lel, self.ch_split, str(ms))
			data = "\n%s - %s\n"  %  (current_time, logmsg)
# 			self.current_object.add_log_report(lel, data)
			if self.uilog:
				self.uilog.write(logmsg)
			if e:
				data += (str(e))
			self.current_object.add_log_report(lel, data)
			
			if e:
				e_msg = self.message_exception()
				data += e_msg

# 				for frame in traceback.extract_tb(sys.exc_info()[2]):
# 					fname,lineno,fn,text = frame
# 					data += ("Error in %s on line %d --- %s --- %s\n" % (fname, lineno, fn, text))
			print (data)
			
			try:
				if self.admin_mode:
					self.file_write(self.file_current_command, data, 'a')
			except:
				#print ("Not able to write command log in file - " + str(self.file_current_command))
				pass
			
		except Exception as e:
			msg = "Error in OperationFile.message_command - Exception e=" , e
			print (msg)
			pass


	def message_exception(self):
		msg = ''
		for frame in traceback.extract_tb(sys.exc_info()[2]):
			fname, lineno, fn, text = frame
			this_line = "Error in %s on line %d --- %s --- %s\n" % (fname, lineno, fn, text)
			msg += this_line
# 			print("Error in %s on line %d" % (fname, lineno))
# 			print("Error in %s on line %d --- %s --- %s\n" % (fname, lineno, fn, text))
		return msg

	
# === === === === === === === === === === === ===
#  info ---
# === === === === === === === === === === === ===

	def add_log_report(self, lel, log):
		lst_key =  list(self.info.keys())
		if not lel in lst_key:
			self.info[lel] = []
		self.info[lel].append(log)
		self.info['log'].append(log)
		
	def file_info(self, fi):

		(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fi)
		lst = []
		lst.append("\n========================================\n")
		lst.append("check file - %s " % fi)
		lst.append("-------------------------")
		lst.append("mode: " + str(mode) )
		lst.append("ino: " + str(ino) )
		lst.append("dev: " + str(dev) )
		lst.append("nlink: " + str(nlink) )
		lst.append("uid: " + str(uid) )
		lst.append("gid: " + str(gid) )
		lst.append("size: " + str(size) )
		lst.append("atime: " + str(atime) )
		lst.append("mtime: " + str(mtime) )
		lst.append("ctime: " + str(ctime) )
		lst.append("\n========================================\n")
		
		return self.list_to_string(lst, "\n")

	def get_info(self):
		return self.info
	
	
		
OPERATION_FILE = OperationFile()

if __name__ == '__main__':
	OPERATION_FILE.set_file_constant()
	print (OPERATION_FILE.message_exception())
	print (OPERATION_FILE.path_user_documents)
	print (OPERATION_FILE.set_log_location())
