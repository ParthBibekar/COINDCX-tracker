# COINDCX-Tracker

A Crypto investment Tracker using COINDCX api.
API documentation: https://docs.coindcx.com/#terms-and-conditions

To use enter the api and secret keys in `api.json` file and run `main.py`.
You will have to manually enter your investment as the API doesn't support wallet history.
***
## TODO

- [x] Print wallet and portfolio
- [x] Calculate profit/loss represent in a graph 
- [ ] Track orders
- [ ] Detailed analysis of each trade

***
## Screenshots
![Screenshot_20211119_030523](https://user-images.githubusercontent.com/76177177/142500485-1fbe3411-d042-4375-a5dc-ead5aa93803d.png)


![Screenshot_20211119_030150](https://user-images.githubusercontent.com/76177177/142500205-77ae55c1-3f24-4c67-92e7-d789a70f6a8e.png)



You can create a cronjob(or any other schedular) which will run the script at a regular intervals and thus update the `coindcx_log.csv` 
