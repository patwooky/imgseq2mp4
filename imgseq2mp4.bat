@echo off 
REM echo %0
REM echo %*
echo %~dp0
REM R:\Pipeline\App_VHQ\Python27x64\python.exe %~dp020190927_imgseq2mp4_v001_01.py %*
R:\Pipeline\App_VHQ\Python27x64\python.exe  %~dp0imgseq2mp4.py %*
@pause