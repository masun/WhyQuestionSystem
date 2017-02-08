from nltk.token import WSTokenizer
from nltk.draw.plot import Plot
#Extract a list of words from the corpus
corpus = open('corpus.txt').read()
tokens = WSTokenizer().tokenize(corpus)
# Count up how many times each word length occurs wordlen_count_list = []
for token in tokens:
	wordlen = len(token.type())
	# Add zeros until wordlen_count_list is long enough
	while wordlen >= len(wordlen_count_list):
		wordlen_count_list.append(0)
		# Increment the count for this word length
		wordlen_count_list[wordlen] += 1 
		Plot(wordlen_count_list)
