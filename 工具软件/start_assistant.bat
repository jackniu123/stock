@echo off

if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~0"" h",0)(window.close)&&exit
:begin
python D:\��Ҫɾ��ţ�ְֵĳ���\__main.py

pause
