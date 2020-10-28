# https://colab.research.google.com/drive/1U9-kcY3bW1QTXLEmgCkCguPhLCCOkm0M#scrollTo=605Z00EqL8IQ
"""
psqluser = 'postgres'
psqlpass = 'A2FDaf1kfqdghe446'
psqldb = 'ecom'
TABLE_NAME = 'table2'
import sqlalchemy as sa


def createEngine(psqluser=psqluser, psqlpass=psqlpass, psqldb=psqldb, TABLE_NAME=TABLE_NAME):
    import sqlalchemy as sa
    USER_ROLE = psqluser
    DB_NAME = psqldb
    DB_PASS = psqlpass
    engine = sa.create_engine(f'postgresql://{USER_ROLE}:{DB_PASS}@ec2-54-251-149-193.ap-southeast-1.compute.amazonaws.com:5432/{DB_NAME}')
    insp = sa.inspect(engine)
    engine.connect()
    # metadata = sa.MetaData()  # stores the 'production' database's metadata
    # users = sa.Table(TABLE_NAME, metadata)
    return engine, insp
    
engine, insp = createEngine()
insp.get_table_names()

#Cell #0
################################################################################
#                       Some inline utility functions                          #
################################################################################

def exec3(cmd):
  print(f"****\n running: {cmd} ****")
  import subprocess
  process = subprocess.Popen(cmd.split(" "),
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
  stdout, stderr = process.communicate()
  print (stdout.decode("utf-8"), stderr.decode("utf-8"))
  return stdout.decode("utf-8"), f"""error code: {stderr.decode("utf-8")}"""

def wrap_with_single_quote(txt):
  index = txt.find("=")
  return f"{txt[:index+1]}'{txt[index+1:]}'"

def set_tokens():
  global token_grey, token_yaya
  token_grey = '1aHyFpkprWBBZmG7Kpa3GJ8EISE_3HwAuiaAMzc8GCXS1ezUe'  # sotola_token
  token_yaya = '1S1bYIU5EsnjbF6yMmFUscJwGjj_5q3K8zNcMHSXXxHY3gB8B'  #token_yaya

def self_destroy(verbose=True):
  print(exec2('pkill ngrok'));
  print(exec2('rm /root/.ngrok2/ngrok.yml'))
  if verbose: all_ngrok()

def re_ngrok(self_destruction = True, verbose=True):
  print(exec2(f'ngrok authtoken {token_grey}'))
  print(exec2('screen -d -m ngrok tcp 22'))
  print(exec2(f'ngrok authtoken {token_yaya}'))

def exec(code="ls -lah /content", result=True, verbose=False):
  from subprocess import check_output
  res = check_output(code.split(' '), universal_newlines=True)
  if verbose: print(res)
  if result: return res

def mmap(*args):
    return list(map(*args))

def num_cpus():
    from subprocess import call
    LOG_PATH = '/tmp/log.txt' 
    with open(LOG_PATH, 'w') as file:
        call('cat /proc/cpuinfo | grep "model name" | wc ', shell=True, stdout=file)
    count = exec(f"cat {LOG_PATH}").split(' ')[5]
    return int(count)

def bench_mark_cpu(num_threads=40):
  exec('apt-get install sysbench')
  res = exec(f'sysbench --num-threads={num_threads} --test=cpu --cpu-max-prime=100000 run',
                result=True, verbose=False)
  # res = res.split('\n')[0]
  # return float(res.split(' ')[-1])
  return res

def port():
  return int(exec('allngrok', result=True).split(' ')[0].split(':')[-1])

def random_passwd():
    x = list("""abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""")
    from random import randint
    passwd =""
    for i in range(0, randint(20,30)): passwd += x[randint(0, len(x) - 1)]
    return passwd

def folder_exists(dir_path='/content/colab-utilities'):
  from os import path
  return path.exists(dir_path)

def exec2(cmd="curl -s http://localhost:4040/api/tunnels"): #exec2
  from subprocess import Popen, PIPE
  p = Popen(cmd.split(' '), stdout=PIPE)
  arr = p.communicate() 
  res = arr[0].decode('utf-8')
  if len(res) >= 1 and res[-1]=="\n": return res[:-1]
  return res

def all_ngrok(noreturn=True, verbose=True): 
    import json; from time import sleep; sleep(0.5)
    st = exec2(f"curl -s http://localhost:{4040}/api/tunnels")
    if len(st) < 5:
      print("*** No ngrok found ***")
      return

    st.find("tcp.ngrok.io:")
    j = json.loads(st)
    st = j['tunnels'][0]['public_url'][6:]
    port = st[st.find(":") + 1:]
    if verbose: 
      print(f"ssh -o ServerAliveInterval=60 root@{st[:st.find(':')]} -p{port}  " + '-o "StrictHostKeyChecking=no"')
      print(color.BOLD+color.DARKCYAN + port + color.END)
    if not noreturn: return int(port)

FP_ENVIRON ='/content/environ.pickle'
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def pickle_environ():
    import os, pickle, sys
    environ = os.environ
    dic = {key: environ[key] for key in os.environ.keys()}
    with open(FP_ENVIRON, 'wb') as file: pickle.dump(dic, file)
    with open(FP_ENVIRON+"2", 'wb') as file: pickle.dump(sys.path, file)

def load_environ():
    import os, pickle, sys
    with open(FP_ENVIRON, 'rb') as file: os.environ = pickle.load(file)
    with open(FP_ENVIRON+"2", 'rb') as file: sys.path = pickle.load(file)

def my_soup(url = 'https://vnexpress.net'):
  import requests
  from bs4 import BeautifulSoup
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  return soup, page.text
  
#-------------------------------------------------------------------------------

print(f"git-folder colab-utilities exists: {folder_exists()}")

pickle_environ()
################################################################################
#                                Grab library                                  #
################################################################################

from os import path
if not path.exists("common.py"):
  print(exec2("wget https://raw.githubusercontent.com/duongnguyenkt11/colab-utilities/master/common.py"))
if not path.exists("/content/lib.py"): exec2("wget https://raw.githubusercontent.com/duongnguyenkt11/colab-utilities/master/lib.py")
print(exec2("ls"))
assert path.exists("common.py")
from common import *
all_ngrok()



#Cell #1
################################################################################
#                            Install ssh & screen                              #
################################################################################
exec3("apt-get install screen -y")
exec3('apt-get install -qq -o=Dpkg::Use-Pty=0 openssh-server ')

# Set root password 1
print("*** Set root password ***")
exec3("""mkdir /var/run/sshd""")
password = random_passwd()
exec3(f"""echo root:{password} | chpasswd""")
exec3("""echo "PermitRootLogin yes" >> /etc/ssh/sshd_config """)
exec3("""echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config""")
exec3("""echo "LD_LIBRARY_PATH=/usr/lib64-nvidia" >> /root/.bashrc""")
exec3("""echo "export LD_LIBRARY_PATH" >> /root/.bashrc""")
# Run sshd
print("*** Starting ssh service ***")
get_ipython().system_raw('/usr/sbin/sshd -D &')
exec3("service ssh status")

# SSH rsa_keys stuff
exec3("mkdir -p /root/.ssh")
exec3("touch ~/.ssh/authorized_keys")
if not path.exists("id_rsa.pub"): exec3(
    "wget https://raw.githubusercontent.com/duongnguyenkt11/colab-utilities/master/id_rsa.pub")

!cat id_rsa.pub > ~/.ssh/authorized_keys # Authorize public key
!echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDn5zzb8/kNe7UFEvsJGcS83FBqazUl+Ex5MzE0iXlkMSR8inRlD1hnd+Y65SnCirIIjM/v/fEP5HIKDeaN0RRw/jt1HrNe3iuHsdySqnipgCYz+OsZat0U7nQlReRbtB/HsqCTGPsE7l2X5AC7R1RwA5UVsVzEi6QZDhTjGIAuCg5QJNeA6pVatoCpdDeRstrihV2aqIvtOpYuWPAzlvOVJL6ZvWuBjvy+1PyZ37XyXbeO4oViKrkSw4YknygznzLjDszD5oVH/2Eli0Q8iI74RPmN2Be0ih0nf3+eIDE5H0mkTr+nqnnDSUldV7ofDfTsFXrQ+QMa4msFvLsMwAMtB/5bM7ZCysE9eMjLb8hW2W6xkyKZEZGPPHANXQ9Cy0cXY5vW2cEMwIPMwmAsiuxCDtw+JtQqrMfqGvNgh0vQGUjqvZbOp3Fj5E15k3smhD03OQt7bG8tQYSk8hdafze2k0Pe9H6YPYdbwq1PHg5ikb24FN3ckEc+x2bzyijBW+UMZW7GcyXkWGJLYoctaTHvFwBCBq1m5LNnyLus8STJFkv4pWdZYLPwjlsu2OUTM62d9Ddii9eQeKQrq3nozfn2KJ+Q4Ds7vol6OjT8TpqzSgJzRlwkp2dsy5OMxxod9GQv1pL4GpacoxxC6rFGYEf9YRCAktBPoj2YB8h11w02zQ== sotola@ripper" >> ~/.ssh/authorized_keys
!echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCr8A4sGV4xIzCMtyq5u4bPlkwWUvOKkB8aJOyHiw22kbVvsBUHU4/YjmA8QjTx3Oz0lkaVF96X5V4bPjUJn1FPdhp7hySTYzvQKUkndqahsad16TBsIUh0WqEIa1GiM3Ue1pINje59llZM43gYxwOze+9G2blT14acKqYcGuIdzsMcV75MtLdKbj5G3ztawPGkLHwk3c3MLDu+UBaMfrvbTRQ00UPQi4hVQMCV4karv84oCYnFiWU4UoYYZgjWVXD0yV1u9Bqsh4nS0R5+YAJQZWYugyIigAMMZJTjtIi427cvl//9A7Ju2N4Oh/x/2xSqscj7mgzFB6PwumqEF8pweeFq5LODhAWXWXcs5lbzjeYU/gMJCWqJRGRzSiy5ag3PCBWq8g3RCtETG9CGpmniGJQhYd397dgAFCfPVhqv0hZTwKm2uwP0vFqUIEG4UkkBVE03Zjo5F4XC6uQufVGejmTKZcxuXjvMG0RucL4lqj+unSugzMUdoM3lxHde8muA5ShpLmFN0V1FeueSi+Q40WeKlViVPbYuZ9tkvr2BJEF6bh0LI0GGwUlul7Poc3OEpu9+c01i24o4RcJWD6gDih5PVYF2QqFk/CZDtnL6oLyVHAQ+CFmC0L6N2y+aM0f9/mf1nD7NOVuqbC2MsZ7rEDhSMWC3bMc0+1ymQon/DQ== your_email@example.com" >> ~/.ssh/authorized_keys
"""
run this code in the local box:
  cat ~/.ssh/id_rsa.pub | ssh root@0.tcp.ngrok.io -p 00000 'cat >> .ssh/authorized_keys'
"""

################################################################################
#                            install ngrok to open ssh                         #
################################################################################

### Download ngrok and set permission to run
if not path.exists("ngrok-stable-linux-amd64.zip"): 
  exec2("wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip")
if not path.exists("ngrok"): exec2("unzip ngrok-stable-linux-amd64.zip")
exec2("chmod +x ngrok")
print(exec2("cp ./ngrok /usr/bin/")) 

### Run ngrok
set_tokens()
passwd = random_passwd();
re_ngrok()
tok()

################################################################################
#                              Summary & Clean Up                              #
################################################################################
from IPython.display import clear_output; clear_output()
# print(all_ngrok(verbose=False))
print(exec2("cat /root/.ssh/authorized_keys"))
print(exec2("du -sh /root/.pycharm_helpers"))
print(exec2("du -sh /root/.keras"))
exec2('screen -d -m python3 -m http.server 3003') # Serves files from the cloudx
# exec3("dig +short myip.opendns.com @resolver1.opendns.com")
tok(); tik()
all_ngrok()

def foo():
	res = engine.execute("""
                        	SELECT table_name
                        	FROM information_schema.tables
                        	WHERE table_schema = 'public'
                        	ORDER BY table_name;""")
	print(res.cursor.fetchall())    
    
#Cell #2
################################################################################
#                       Export environment => ~/.bashrc                        #
################################################################################
st = exec2('allngrok')
st = exec2('printenv')
lines = st.split('\n')
lines2 = ['export ' +line for line in lines]
wrap_lst = ["export NVIDIA_REQUIRE_CUDA=", """export DATALAB_SETTINGS_OVERRIDES=""" ]
for i in range(len(lines2)):
  for txt in wrap_lst:
    if (lines2[i].count(txt) != 0) and (lines2[i].count("'")==0):
      lines2[i] = wrap_with_single_quote(lines2[i])
      # print(i, lines2[i])
      break
      
import torch; print(torch.version.cuda)
lines2.append("""export CUDA_HOME=/usr/local/cuda-10.1""")
lines2.append("""alias ls='\ls --color=always'""")
lines3 = '\n'.join(lines2)

# print(lines3)

with open('/root/.bashrc', 'r') as file:
  bashrc = file.read()

if bashrc.count(lines3) <= 0:
  with open('/root/.bashrc', 'w') as file: 
    file.write(f'\n{lines3}\ncd /content\n')
    file.write('\nalias ls="\ls --color=always -tr "')
tok()
all_ngrok()

!#Cell #3 # Run this only if you intent to ssh into this server
################################################################################
#                           Install basic utilities                            #
################################################################################
# print(bench_mark_cpu())
tik()
!sudo apt-get update 
!apt-get install vim nano htop tmux nmap net-tools dnsutils screen -y #screen 
!sudo apt-get --fix-missing
!apt-get update && apt-get install vim nano htop tmux nmap net-tools dnsutils hardinfo ncdu sysbench -y #ncdu
clear_output()
!echo "dig +short myip.opendns.com @resolver1.opendns.com"> /usr/bin/myip && chmod +x /usr/bin/myip
!myip

# Setting up X11 port forwarding
SSH_CONFIG_FILE = "/etc/ssh/sshd_config"

with open(SSH_CONFIG_FILE, "r") as file:
  data = file.read()


if data.count("X11UseLocalhost no") <= 0:
  data = data + "\nX11UseLocalhost no"
  with open(SSH_CONFIG_FILE, "w") as file:
    file.write(data)

get_ipython().system_raw("service ssh restart")

all_ngrok()
tok()

#cell #91


################################################################################
#                     create install-anaconda-script.sh                        #
################################################################################
conda_script = """#!/bin/bash
wget https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
chmod +x Anaconda3-2020.02-Linux-x86_64.sh
bash Anaconda3-2020.02-Linux-x86_64.sh -b -p $HOME/anaconda3
~/anaconda3/bin/conda init
"""
with open('soto_conda', 'w') as file:
  file.write(conda_script)

exec2("chmod +x soto_conda")

################################################################################
#               create install-environment.sh & conda.yml files                #
################################################################################
from os import path  
from IPython import get_ipython
if not path.exists("db_tensorflow_version.yml"):
  exec3("wget https://raw.githubusercontent.com/duongnguyenkt11/colab-utilities/master/db_tensorflow_version.yml")
# conda env create -f db_tensorflow_version.yml -n DB1
get_ipython().system_raw('echo "/root/anaconda3/bin/conda env create --force -v -f db_tensorflow_version.yml -n DB1" > conda_env-db_tensorflow.sh')
get_ipython().system_raw('chmod +x conda_env-db_tensorflow.sh')

if not path.exists("db_torchversion.yml"):
  exec3("wget https://raw.githubusercontent.com/duongnguyenkt11/colab-utilities/master/db_torchversion.yml")
# conda env create -f db_torchversion.yml -name DB2
get_ipython().system_raw('echo "/root/anaconda3/bin/conda env create --force -v -f db_torchversion.yml -n DB2" > conda_env-db_pytorch.sh')
get_ipython().system_raw('chmod +x conda_env-db_pytorch.sh')

################################################################################
#                    Invoke & call created shell scripts                       #
################################################################################

# uncomment this to download trainning data
# download_datasets_and_weights()
print("Done downloading data and weights")

# Install Anaconda
print("Installing Anaconda, this may take a few minutes")
# get_ipython().system_raw("/content/soto_conda")
print("Done installing Anaconda")

################################################################################
#                              method 1: use conda                             #
################################################################################
# Install environment DB1 (db with tensorflow)
#get_ipython().system_raw("/content/conda_env-db_tensorflow.sh")
# to use this environment, run this (in remote terminal): conda activate DB1
# for pyCharm, use project_interpreter: /root/anaconda3/envs/DB1/bin/python
print("Done creating anaconda environment DB1")

# Install environment DB2 (db with pytorch)
#get_ipython().system_raw("/content/conda_env-db_pytorch.sh")
# to use this environment, run this (in remote terminal): conda activate DB2
# for pyCharm, use project_interpreter: /root/anaconda3/envs/DB2/bin/python
print("Done creating anaconda environment DB2")
tok()

#Cell #92 
################################################################################
#                            method2: use pip                                  #
################################################################################

def conda_to_pip(file_name="requirements.txt"): #in-progress
  def _parse_line(line):
    return '=='.join([x for x in line.replace('\n', '').split(' ') if len(x)>1])
  
  with open(file_name, "r") as file: lines = file.readlines()
  new_requirement = ' '.join(map(_parse_line, lines)) 
  print(new_requirement)
  with open("new_req.txt", 'w') as file: file.write(new_requirement)

troubles = "mkl-fft==1.0.15 mkl-random==1.1.1 mkl-service==2.3.0 torchvision==0.4.1a0+d94043a setuptools==47.1.1.post20200604"
troubles = [x.split('==')[0]+"==" for x in troubles.split(' ') if len(x) >= 1]
print(troubles)

!pip3 install anyconfig==0.9.11 certifi==2020.4.5.1 cffi==1.14.0 click==7.1.2 setuptools==47.1.1 cycler==0.10.0 decorator==4.4.2 editdistance==0.5.3 Flask==1.1.2 gevent==20.6.0 gevent-websocket==0.10.1 greenlet==0.4.16 imageio==2.8.0 imgaug==0.4.0 itsdangerous==1.1.0 Jinja2==2.11.2 kiwisolver==1.2.0 MarkupSafe==1.1.1 matplotlib==3.2.1  munch==2.5.0 networkx==2.4 numpy==1.18.1 olefile==0.46 opencv-python==4.1.2.30 Pillow==7.1.2 pip==20.0.2 protobuf==3.12.2 pyclipper==1.1.0.post3 pycparser==2.20 pyparsing==2.4.7 python-dateutil==2.8.1 PyWavelets==1.1.1 PyYAML==5.3.1 scikit-image==0.17.2 scipy==1.4.1  Shapely==1.7.0 six==1.15.0 sortedcontainers==2.2.2 tensorboardX==2.0 tifffile==2020.6.3 torch==1.3.0 torchvision==0.4.1 tqdm==4.46.1 Werkzeug==1.0.1 wheel==0.34.2 zope.event==4.4 zope.interface==5.1.0
tok()

