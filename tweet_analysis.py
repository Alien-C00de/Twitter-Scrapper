import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import os

class TwitterAnalysis:

    def __init__(self) -> None:
        pass

    # Read in the data
    def read_data(self, filename):
        os.system('clear')
        df = pd.read_csv(filename, sep="\t",  encoding= 'ISO-8859-1', on_bad_lines='skip')  
        self.__create_WordCloud(df)
        

    # Create a wordcloud
    def __create_WordCloud(self, df):

        STOPWORDS.update(['will', 'the', 'a', 'an', 'https']) 
        mask = np.array(Image.open("twitter_mask.png"))
        wordcloud = WordCloud(width = 350,
                        height = 350,
                        max_words = 1000,
                        min_font_size = 5,
                        max_font_size = 200, mask= mask,
                        stopwords = STOPWORDS,
                        background_color="white").generate(' '.join(df['content']))
        print("[+] Wordcloud created")
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()

