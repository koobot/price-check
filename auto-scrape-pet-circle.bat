@echo on

rem activate anaconda prompt
call C:\ProgramData\Anaconda3\Scripts\activate.bat

rem activate python environment
call conda activate price-check

rem run web scrape script
call python "D:\Documents\Python\price-check\scrape-pet-circle.py"
