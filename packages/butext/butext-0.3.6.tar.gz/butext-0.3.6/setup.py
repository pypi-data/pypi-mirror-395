from setuptools import setup, find_packages

setup(
    name='butext',
    version='0.3.6',
    description='https://butext.readthedocs.io/en/latest/',
    long_description="BUtext focuses on text processing techniques commonly used in Natural Language Processing (NLP). Natural Language Processing is important for many applications. When given a very large body of text, there is only so much a human can do to analyze it. Imagine trying to find the word count of a book you are reading? That would be very difficult and impractical, so it’s better to have a computer do it as it takes milliseconds to perform. That’s just one area where Natural Language Processing is useful. In essence, Natural Language Processing allows computers to understand and interpret text, far beyond our capabilities. When a computer can understand text, it can learn from it and make predictive models, sentiment analysis, chatbots, and even artificial intelligence through text generation. BUtext allows a seamless experience for text processing and preparing text for natural language processing and machine learning purposes.",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn'
    ]
)