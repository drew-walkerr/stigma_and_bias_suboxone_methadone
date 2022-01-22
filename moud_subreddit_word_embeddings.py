import gensim
from gensim.models import KeyedVectors
# Make sure pip install gensim==3.8.1
from gensim.models.word2vec import Word2Vec

model = Word2Vec.load("400features_10minwords_5context")
# stigma OR bias OR stereotype OR abuser OR stereotype
# NIDA: https://www.drugabuse.gov/nidamed-medical-health-professionals/health-professions-education/words-matter-terms-to-use-avoid-when-talking-about-addiction
# Included: Addict, User, Abuser, Junkie, Alcoholic, Drunk, Habit, Dirty,
# Not included: clean, addicted baby, opioid substitution replacement therapy, medication-assisted treatment, former addict, reformed adict
print model.most_similar("addict")
print model.most_similar("user")
print model.most_similar("abuser")
print model.most_similar("junkie")
print model.most_similar("alcoholic")
print model.most_similar("drunk")
print model.most_similar("habit")
print model.most_similar("dirty")
print model.most_similar("stigma")
print model.most_similar("bias")
print model.most_similar("stereotype")

# stigma_words = model.wv.most_similar("stigma")


#build into table/list


