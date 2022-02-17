import numpy
import pandas as pd
import gensim
from gensim.models import Word2Vec
#requires Cython==0.29.23
from gensim.models.keyedvectors import KeyedVectors

#STill unable to get model to run by uploading just from binary-- though it did work once and i was able to write/save the format to trig-vectors-phrase.txt
#model = KeyedVectors.load_word2vec_format('trig-vectors-phrase.bin', binary=True, encoding='latin-1')
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

bias_words_df_2 = bias_words_df.explode("most_similar_words", ignore_index=True)
bias_words_df_2['new_word_id'] = range(1, 1 + len(bias_words_df_2))
# bias_words_df_2[['similar_word','similarity_score']] =
words_sep = pd.DataFrame(bias_words_df_2['most_similar_words'].values.tolist(), index = df.index)
words_sep['new_word_id'] = range(1, 1 + len(bias_words_df_2))
bias_words_3 = bias_words_df_2.merge(words_sep, on = 'new_word_id')
#bias_words_3['similar_word'], bias_words_3['score'] = bias_words_3[3],bias_words_3[4]

bias_words_3= bias_words_3.rename(columns={0: "similar_word", 1: "score"})
bias_words_3["Relevant_to_study"] = ""
bias_words_3.to_csv("bias_lexicon_stem_and_similar_round1.csv")

