# Analyze Text with a TextAnalyzer object!
#
# By: 

import unittest # import the library needed for testing
import math

class TextAnalyzer:

    def __init__(self, filepath):
        """Initializes the TextAnalyzer object, using the file at filepath""" 
        f = open(filepath, 'r')
        self.lines = f.readlines() #list of lines
        f.close()       

        self.lower_case_lines = [] #list of lines where all words are lower case
        for line in self.lines:
            self.lower_case_lines.append(line.lower())

        self.list_words = []
        for line in self.lower_case_lines:
            for word in line.split():
                stripped_word = word.strip('?!,.')
                self.list_words.append(stripped_word)

        self.list_unique_words = [] #unsorted list of unique words
        for word in self.list_words:
            if word not in self.list_unique_words:
                self.list_unique_words.append(word)

        self.sorted_words = sorted(self.list_unique_words) #sorted list of unique words

    def line_count(self):
        """Returns the number of lines in the file"""
        return len(self.lines)

    def word_count(self):
        """Returns the number of words in the file. A word is defined as any 
        text that is separated by whitespace (spaces, newlines, or tabs).
        followed by punctuation (like ? or !)."""
        num_words = 0
        for word in self.list_words:
            num_words += 1
        
        return num_words
        

    def vocabulary(self):
        """Returns a list of the unique words in the text, sorted in 
        alphabetical order. Capitalization should be ignored, so 'Cat' is the
        same word as 'cat'. The returned words should be all lower-case."""
        return self.sorted_words

    def num_unique_words(self):
        """Returns the number of unique words in the text. Capitalization 
        should be ignored, so 'Cat' is the same word as 'cat'."""
        count = 0
        for word in self.list_unique_words:
            count += 1
        
        return count
        
    def frequencies(self):
        """Returns a dictionary of the words in the text and the count of how 
        many times they appear. The words are the keys, and the counts are the
        values. All the words should be lower case. The order of the keys 
        doesn't matter."""
        unique_words_dict = {}
        for word in self.list_words:
            if word not in unique_words_dict:
                unique_words_dict[word] = 1
            else:
                unique_words_dict[word] += 1
        
        return unique_words_dict

    def frequency_of(self, word):
        """Returns the number of times word appears in the text. Capitalization 
        should be ignored, so 'Cat' is the same word as 'cat'."""
        lower_case_word = word.lower()
        return self.frequencies().get(lower_case_word, 0)

    def percent_frequencies(self):
        """Returns a dictionary of the words in the text and the fraction of 
        the text. The words are the keys, and the counts are the
        values. All the words should be lower case. The order of the keys 
        doesn't matter."""
        d = self.frequencies()
        dict_percentages = {}

        for word in d:
            if word not in dict_percentages:
                dict_percentages[word] = self.frequency_of(word) / self.word_count()

        return dict_percentages

    def most_common(self, n=1):
        """Returns a list of the most common n words in the text. By default,
        n is 1. The returned words should be in alphabetical order.
        
        There might be a case where multiple words have the same frequency,
        but you can only return some of them due to the n value. In that case,
        return the ones that come first alphabetically."""
        freq = self.frequencies()
        
        sort_alpha = sorted(self.list_unique_words)
        sort_value = sorted(sort_alpha, reverse = True, key = lambda x:freq[x])

        n_most_common = sort_value[:n]
        return sorted(n_most_common)

    def similarity_with(self, other_text_analyzer, n=10):
        """Extra credit. Calculates the similarity between this text and 
        the other text using cosine similarity. See project specification
        for details."""

        #for magnitude of vector passed in as the object
        d = self.percent_frequencies()
        sorted_dict_percentages1 = sorted(d, reverse = True, key = lambda x:d[x]) #sort dictionary by value
        text_1_words = sorted_dict_percentages1[:n]

        #for magnitude of vector passed in as the parameter
        d2 = other_text_analyzer.percent_frequencies()
        sorted_dict_percentages2 = sorted(d2, reverse = True, key = lambda x:d2[x])
        text_2_words = sorted_dict_percentages2[:n]

        #make a list of unique words thaat are a combination of the n most frequent words from both files
        unique_words = []
        for word in text_1_words:
            if word not in unique_words:
                unique_words.append(word)
        for word in text_2_words:
            if word not in unique_words:
                unique_words.append(word)

        #magnitude of vector 1
        magnitude1 = 0
        for word in unique_words:
            magnitude1 += (d.get(word,0) ** 2)

        magnitude1 = math.sqrt(magnitude1)

        #magnitude of vector 2
        magnitude2 = 0
        for word in unique_words:
            magnitude2 += (d2.get(word,0) ** 2)

        magnitude2 = math.sqrt(magnitude2)

        #get dot product
        dot_prod = 0
        for word in unique_words:
            dot_prod += (d.get(word,0.0) * d2.get(word,0.0))
        
        return dot_prod / (magnitude1 * magnitude2)
        

# These are the tests. The main() is all the way at the bottom.

class TestLineCount(unittest.TestCase):

    def test_line_count_tiny1(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_1.txt")
        self.assertEqual(ta.line_count(), 1)
        self.assertEqual(ta.line_count(), 1) # Check that it works when called a second time
        
    def test_line_count_tiny3(self):    
        ta = TextAnalyzer("files_for_testing/tinyfile_4.txt")
        self.assertEqual(ta.line_count(), 3)
        self.assertEqual(ta.line_count(), 3) # Check that it works when called a second time

    def test_line_count_the_victors(self):    
        ta = TextAnalyzer("files_for_testing/the_victors.txt")
        self.assertEqual(ta.line_count(), 33)
        self.assertEqual(ta.line_count(), 33) # Check that it works when called a second time


class TestWordCount(unittest.TestCase):
    
    def test_word_count_tiny1(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_1.txt")
        self.assertEqual(ta.word_count(), 3)
        self.assertEqual(ta.word_count(), 3) # Check that it works when called a second time
        
    def test_word_count_tiny3(self):    
        ta = TextAnalyzer("files_for_testing/tinyfile_3.txt")
        self.assertEqual(ta.word_count(), 8)
        self.assertEqual(ta.word_count(), 8) # Check that it works when called a second time

    def test_word_count_the_victors(self):    
        ta = TextAnalyzer("files_for_testing/the_victors.txt")
        self.assertEqual(ta.word_count(), 175)
        self.assertEqual(ta.word_count(), 175) # Check that it works when called a second time

class TestFrequencies(unittest.TestCase):

    def test_frequencies_tiny1(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_1.txt")
        self.assertEqual(ta.frequencies()['i'], 1)
        self.assertEqual(ta.frequencies()['love'], 1)
        self.assertEqual(ta.frequencies()['cats'], 1)

    def test_frequencies_tiny3(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_3.txt")
        self.assertEqual(ta.frequencies()['i'], 1)
        self.assertEqual(ta.frequencies()['love'], 1)
        self.assertEqual(ta.frequencies()['cats'], 1)
        self.assertEqual(ta.frequencies()['so'], 4)
        self.assertEqual(ta.frequencies()['much'], 1)

    def test_frequencies_tiny4(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_4.txt")
        self.assertEqual(ta.frequencies()['i'], 3)
        self.assertEqual(ta.frequencies()['love'], 3)
        self.assertEqual(ta.frequencies()['cats'], 1)
        self.assertEqual(ta.frequencies()['so'], 12)
        self.assertEqual(ta.frequencies()['much'], 3)
        self.assertEqual(ta.frequencies()['dogs'], 1)
        self.assertEqual(ta.frequencies()['parakeets'], 1)

class TestFrequencyOf(unittest.TestCase):

    def test_frequency_of_tiny1(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_1.txt")
        self.assertEqual(ta.frequency_of('i'), 1)
        self.assertEqual(ta.frequency_of('love'), 1)
        self.assertEqual(ta.frequency_of('cats'), 1)
        self.assertEqual(ta.frequency_of('dogs'), 0)
        self.assertEqual(ta.frequency_of('I'), 1)
        self.assertEqual(ta.frequency_of('LOVE'), 1)

    def test_frequency_of_tiny3(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_3.txt")
        self.assertEqual(ta.frequency_of('i'), 1)
        self.assertEqual(ta.frequency_of('love'), 1)
        self.assertEqual(ta.frequency_of('cats'), 1)
        self.assertEqual(ta.frequency_of('so'), 4)
        self.assertEqual(ta.frequency_of('much'), 1)
        self.assertEqual(ta.frequency_of('dogs'), 0)

    def test_frequency_of_tiny4(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_4.txt")
        self.assertEqual(ta.frequency_of('i'), 3)
        self.assertEqual(ta.frequency_of('love'), 3)
        self.assertEqual(ta.frequency_of('cats'), 1)
        self.assertEqual(ta.frequency_of('so'), 12)
        self.assertEqual(ta.frequency_of('much'), 3)
        self.assertEqual(ta.frequency_of('dogs'), 1)
        self.assertEqual(ta.frequency_of('parakeets'), 1)
        self.assertEqual(ta.frequency_of('ferrets'), 0)

class TestVocabulary(unittest.TestCase):

    def test_vocabulary_tiny1(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_1.txt")
        self.assertEqual(ta.vocabulary(), ['cats', 'i', 'love'])

    def test_vocabulary_tiny3(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_3.txt")
        self.assertEqual(ta.vocabulary(), ['cats', 'i', 'love', 'much', 'so'])

    def test_vocabulary_tiny4(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_4.txt")
        self.assertEqual(ta.vocabulary(), ['cats', 'dogs', 'i', 'love', 'much', 'parakeets', 'so'])

class TestNumUniqueWords(unittest.TestCase):

    def test_num_unique_words_tiny1(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_1.txt")
        self.assertEqual(ta.num_unique_words(), 3)

    def test_num_unique_words_tiny3(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_3.txt")
        self.assertEqual(ta.num_unique_words(), 5)

    def test_num_unique_words_tiny4(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_4.txt")
        self.assertEqual(ta.num_unique_words(), 7)

    def test_num_unique_words_thevictors(self):
        ta = TextAnalyzer("files_for_testing/the_victors.txt")
        self.assertEqual(ta.num_unique_words(), 56)

class TestPercentFrequencyOf(unittest.TestCase):

    def test_percent_frequency_of_tiny1(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_1.txt")
        self.assertIn('i', ta.percent_frequencies())
        self.assertIn('love', ta.percent_frequencies())
        self.assertIn('cats', ta.percent_frequencies())
        self.assertAlmostEqual(ta.percent_frequencies()['i'], 1/3)
        self.assertAlmostEqual(ta.percent_frequencies()['love'], 1/3)
        self.assertAlmostEqual(ta.percent_frequencies()['cats'], 1/3)

    def test_percent_frequency_of_tiny3(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_3.txt")
        self.assertIn('i', ta.percent_frequencies())
        self.assertIn('love', ta.percent_frequencies())
        self.assertIn('cats', ta.percent_frequencies())
        self.assertIn('so', ta.percent_frequencies())
        self.assertIn('much', ta.percent_frequencies())
        self.assertAlmostEqual(ta.percent_frequencies()['i'], 1/8)
        self.assertAlmostEqual(ta.percent_frequencies()['love'], 1/8)
        self.assertAlmostEqual(ta.percent_frequencies()['cats'], 1/8)
        self.assertAlmostEqual(ta.percent_frequencies()['so'], 4/8)
        self.assertAlmostEqual(ta.percent_frequencies()['much'], 1/8)

    def test_percent_frequency_of_tiny4(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_4.txt")
        self.assertAlmostEqual(ta.percent_frequencies()['i'], 3/24)
        self.assertAlmostEqual(ta.percent_frequencies()['love'], 3/24)
        self.assertAlmostEqual(ta.percent_frequencies()['cats'], 1/24)
        self.assertAlmostEqual(ta.percent_frequencies()['so'], 12/24)
        self.assertAlmostEqual(ta.percent_frequencies()['much'], 3/24)
        self.assertAlmostEqual(ta.percent_frequencies()['dogs'], 1/24)
        self.assertAlmostEqual(ta.percent_frequencies()['parakeets'], 1/24)

class TestMostCommon1(unittest.TestCase):

    def test_most_common_1_tiny3(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_3.txt")
        self.assertEqual(ta.most_common(), ['so'])

    def test_most_common_1_tiny4(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_4.txt")
        self.assertEqual(ta.most_common(), ['so'])

class TestMostCommonOutOfRange(unittest.TestCase):

    def test_most_common_oor_multiple_tiny1(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_1.txt")
        self.assertEqual(ta.most_common(0), [])
        self.assertEqual(ta.most_common(4), ['cats', 'i', 'love'])

class TestMostCommonMultipleClearCases(unittest.TestCase):

    def test_most_common_multiple_tiny1(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_1.txt")
        self.assertEqual(ta.most_common(3), ['cats', 'i', 'love'])

    def test_most_common_multiple_tiny4(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_4.txt")
        self.assertEqual(ta.most_common(4), ['i', 'love', 'much', 'so'])

class TestMostCommonMultiple(unittest.TestCase):

    def test_most_common_multiple_inbetween_tiny1(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_1.txt")
        self.assertEqual(ta.most_common(1), ['cats'])
        self.assertEqual(ta.most_common(2), ['cats', 'i'])

    def test_most_common_multiple_inbetween_tiny3(self):
        ta = TextAnalyzer("files_for_testing/tinyfile_3.txt")
        self.assertEqual(ta.most_common(2), ['cats', 'so'])
        self.assertEqual(ta.most_common(3), ['cats', 'i', 'so'])
        self.assertEqual(ta.most_common(4), ['cats', 'i', 'love', 'so'])


# Uncomment the lines below to run the unit tests for the extra credit

class TestSimilarity(unittest.TestCase):
    def test_similarity_when_all_same(self):
        ta1 = TextAnalyzer("files_for_testing/tinyfile_1.txt")
        ta2 = TextAnalyzer("files_for_testing/tinyfile_1.txt") 
        self.assertAlmostEqual(ta1.similarity_with(ta2, 1), 1.0)
        self.assertAlmostEqual(ta1.similarity_with(ta2, 2), 1.0)
        self.assertAlmostEqual(ta1.similarity_with(ta2, 3), 1.0)
        self.assertAlmostEqual(ta1.similarity_with(ta2), 1.0)

    def test_similarity_when_all_different(self):
        ta1 = TextAnalyzer("files_for_testing/tinyfile_1.txt")
        ta2 = TextAnalyzer("files_for_testing/tinyfile_2.txt") 
        self.assertAlmostEqual(ta1.similarity_with(ta2, 1), 0.0)
        self.assertAlmostEqual(ta1.similarity_with(ta2, 2), 0.0)
        self.assertAlmostEqual(ta1.similarity_with(ta2, 3), 0.0)
        self.assertAlmostEqual(ta1.similarity_with(ta2), 0.0)

    def test_similarity_when_somewhat_different_corrected(self):
        ta1 = TextAnalyzer("files_for_testing/tinyfile_1.txt")
        ta2 = TextAnalyzer("files_for_testing/tinyfile_3.txt") 
        self.assertAlmostEqual(ta1.similarity_with(ta2, 1), 0.242535625)
        self.assertAlmostEqual(ta1.similarity_with(ta2, 2), 0.333333333) 
        self.assertAlmostEqual(ta1.similarity_with(ta2, 3), 0.397359707) 
        self.assertAlmostEqual(ta1.similarity_with(ta2), 0.3872983346) #this is the only test in this method that passes

def main():
    
    # You can uncomment out some of these lines to do some simple tests
    # with print statements before you are ready to run all the unit tests 
    # Or, use your own print statements here as well!
    #fightsong = TextAnalyzer('files_for_testing/fightsong.txt')
    fightsong = TextAnalyzer('files_for_testing/tinyfile_4.txt')
    print("Line count is ", fightsong.line_count())
    print("Word count is ", fightsong.word_count())
    print("Vocabulary is ", fightsong.vocabulary())
    print("Frequencies are ", fightsong.frequencies())
    print("Percent frequencies are ", fightsong.percent_frequencies())
    print("Most common is ", fightsong.most_common())
    print("Most common 3 are ", fightsong.most_common(3))
    

    #Un-comment this line when you are ready to run the unit tests.
    unittest.main(verbosity=2)

    # Un-comment the lines below when you want to test the extra credit
    # or uncomment the class TestSimilarity above
    #ta1 = TextAnalyzer("files_for_testing/tinyfile_1.txt")
    #ta2 = TextAnalyzer("files_for_testing/tinyfile_1.txt") 
    #print(ta1.similarity_with(ta2, 3))
    #ta1 = TextAnalyzer("files_for_testing/tinyfile_1.txt")
    #ta2 = TextAnalyzer("files_for_testing/tinyfile_2.txt") 
    #print(ta1.similarity_with(ta2, 3))

if __name__ == "__main__":
    main()