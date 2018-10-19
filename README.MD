HOW TO INSTALL?

1.  Install Python3.5+
2.  Run "pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r required_package.txt" in command
3.  Install JDK
4.  Install Android SDK
5.  Install APPIUM SERVER
6.  Install Mysql Server

-------------------------------------------------------------------------
HOW TO EXECUTION?

SERVER:

0.  Build up Mysql database, move to Server folder and run "python manage.py migrate"
1.  Config database server name and database name in file "Server/Guest/setting.py"
2.  Move to Server folder and run "python manage.py runserver IP:Port"


CLIENT:

1.  Move to Client folder and run "python Slave.py"


-----------------------------------------------------------------------------
2018 Oct 18

By Kang

if you have any questions, please send email to me(jjleekang@outlook.com).
