import gensim
from gensim.models import KeyedVectors
# Make sure pip install gensim==3.8.1
from gensim.models.word2vec import Word2Vec

model = Word2Vec.load("400features_10minwords_5context")
# stigma OR bias OR stereotype OR abuser OR stereotype
stigma_words = model.wv.most_similar("stigma")
print(stigma_words)
bias_words = model.wv.most_similar("bias")
print(bias_words)
stereotype_words = model.wv.most_similar("stereotype")
print(stereotype_words)
abuser_words = model.wv.most_similar("abuser")
print(abuser_words)
addict_words = model.wv.most_similar("addict")
print(addict_words)

#build into table/list


