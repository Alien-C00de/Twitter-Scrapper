# Twitter-Scrapper
This code is Scrapping Twitter data and create a world cloud using the tweets.

Code work with the following command. Use max 10 to 50 tweet for faster performance and also to avoid getting block.

1. for single twitter account —> output save in the CSV format.
   
python twitter.py -u elonmusk -l 10
![image](https://github.com/Alien-C00de/Twitter-Scrapper/assets/138598543/4efd686c-dbb9-45c5-89e9-f64194f88b41)

2. To fetch more than one user tweet use following command with list of account provided in txt file. —> output saves in the CSV format

python twitter.py -f usernames.txt -l 1

3. To check the wordcloud use following command with the saved CSV file.
python twitter.py -w elonmusk_1697470902.csv
![image](https://github.com/Alien-C00de/Twitter-Scrapper/assets/138598543/dde70da9-8c02-4871-b0ad-2ff85c0ee602)

Following library are required to run the program
   1. pip install pandas
   2. pip install wordcloud
   3. pip install numpy
   4. pip install matplotlib
   5. pip install Pillow
