import numpy
import pandas as pd
import gensim
from gensim.models import Word2Vec
#requires Cython==0.29.23
from gensim.models.keyedvectors import KeyedVectors


model = KeyedVectors.load_word2vec_format('trig-vectors-phrase.bin', binary=True, encoding='latin-1')
model2 = KeyedVectors.load_word2vec_format('trig-vectors-phrase.txt', binary=False)

# stigma OR bias OR stereotype OR abuser OR stereotype
# NIDA: https://www.drugabuse.gov/nidamed-medical-health-professionals/health-professions-education/words-matter-terms-to-use-avoid-when-talking-about-addiction
# Included: Addict, User, Abuser, Junkie, Alcoholic, Drunk, Habit, Dirty,
# Added in this study: stigma, bias, stereotype, shame, blame (From studies on stigma, bias, and types of stigmatization referenced in literature)
# Not included: clean, addicted baby, opioid substitution replacement therapy, medication-assisted treatment, former addict, reformed adict

bias_stem_words = ["user","abuser","junkie","alcoholic", "drunk", "habit", "dirty", "stigma","bias","stereotype","shame","blame"]
bias_words_df = pd.DataFrame({
    'stem_word': bias_stem_words
})

bias_words_df['most_similar_words'] = bias_words_df['stem_word'].apply(model2.most_similar)
bias_words_df.to_csv("bias_lexicon_stem_and_similar.csv")
print(bias_words_df)

