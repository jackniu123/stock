@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~0"" h",0)(window.close)&&exit
:begin
rem set path=D:\test\Miniconda3;D:\test\Miniconda3\Scripts
python D:\不要删除牛爸爸的程序\工具软件\stock_assistant_new_stock_informer.py
ping 127.0.0.1 -n 11 >nul
python D:\不要删除牛爸爸的程序\工具软件\stock_assistant_price_alert.py
pause
