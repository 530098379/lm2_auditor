# windows安装依赖命令
pip install requests  
pip install xlwt  
pip install xlrd  
pip install BeautifulSoup  

# Windows下，命令行显示汉字
1、打开CMD.exe命令行窗口  
2、通过 chcp命令改变代码页，UTF-8的代码页为65001  
chcp 65001  
执行该操作后，代码页就被变成UTF-8了。但是，在窗口中仍旧不能正确显示UTF-8字符。  
3、修改窗口属性，改变字体  
在命令行标题栏上点击右键，选择"属性"->"字体"，将字体修改为"FangSong"，然后点击确定将属性应用到当前窗口  

# MacOS安装pip
curl https://bootstrap.pypa.io/get-pip.py | python3  

# MacOS安装依赖命令
pip3 install requests  
pip3 install xlwt  
pip3 install xlrd  
pip3 install BeautifulSoup  
