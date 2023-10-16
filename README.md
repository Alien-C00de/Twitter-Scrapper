# Twitter-Scrapper
This code is Scrapping Twitter data and create a world cloud using the tweets.

Code work with the following command. Use max 10 to 50 tweet for faster performance and also to avoid getting block.

1. for single twitter account —> output save in the CSV format.
   
   python twitter.py -u elonmusk -l 10
![image](https://github.com/Alien-C00de/Twitter-Scrapper/assets/138598543/4efd686c-dbb9-45c5-89e9-f64194f88b41)

2. To fetch more than one user tweet use following command with list of account provided in txt file. —> output saves in the CSV format

   python twitter.py -f usernames.txt -l 1
![image](https://github.com/Alien-C00de/Twitter-Scrapper/assets/138598543/29cf1e58-5cec-45d2-ae76-7790d5ceaad0)

3. To check the wordcloud use following command with the saved CSV file.

   python twitter.py -w elonmusk_1697470902.csv
   
![image](https://github.com/Alien-C00de/Twitter-Scrapper/assets/138598543/f5603ba5-1c63-487f-9a8a-ebf5b26f7c1f)

Following library are required to run the program
   1. pip install pandas
   2. pip install wordcloud
   3. pip install numpy
   4. pip install matplotlib
   5. pip install Pillow
