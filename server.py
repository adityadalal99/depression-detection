import depression_sentiment_analysis

if __name__ == '__main__':
    depression_sentiment_analysis.initial_run()
    while True:
        if input() == 'exit':
            break
        else:
            depression_sentiment_analysis.get_score_of_tweet()
