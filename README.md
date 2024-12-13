# stock_analysis
SQL and python scripts for analysing my stock portfolio


Used Oracle DB in backend to stock data.
Multiple tables like buy_stocks and sell_stocks to store the stock data 
Developed plsql procedure to update buy and sell charges and consolidate all data into one table
Used python script to automate data loading
Used pandas ,cx_oracle and yfinance libaries in python
yfinance libary and alphavantage api used to fetch current stock value for analysis
By consolidating all data into a snapshot table it made easy to analys each day profit and the current stock value
created views to diplay different data from the snapshot table
