import os
import codecs
import numpy as np
import pandas
import string
from stemming.porter2 import stem
import unicodedata
import sys
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation

if __name__ == '__main__':
	stopWords = set(stopwords.words('english'))
	remove_punct_map = dict.fromkeys(i for i in range(sys.maxunicode)
									 if unicodedata.category(chr(i)).startswith('P'))

	directory = "/Users/mattanderson/Documents/QC_Hackathon_MA/app/speak_up/"
	output_directory = "/Users/mattanderson/Documents/QC_Hackathon_MA/app/"

	aggregate_files = []

	dictionary_terms = {}

	for filename in os.listdir(directory):
		if filename != ".DS_Store":
			for text_file in os.listdir(directory + filename):
				with open(directory + filename + '/' + text_file,'rb') as file_1:
					aggregate_files.append([filename,text_file, file_1.read().decode('utf-8','ignore').encode('ascii','ignore').decode('utf-8')])
				
	for contents in aggregate_files:
		text_vals = contents[2].split(' ')
		clean_text_vals = []
		split_contents = []
		for item in text_vals:
			item = item.lower().replace('\n','')
			item = item.translate(remove_punct_map)
			item = item.strip()
			item = stem(item)
			if item != '' and item not in stopWords:
				clean_text_vals.append(item)
		split_contents.append(clean_text_vals)
		dictionary_terms.update({contents[0] + '_'	+ contents[1] : split_contents})

	term_doc_freq = {}
	for keyvals in dictionary_terms.keys():
		unique_words = {}
		for value in dictionary_terms[keyvals]:
			for word in value:
				if word in unique_words.keys():
					counter = unique_words[word] + 1
					unique_words[word] = counter
				else:
					unique_words.update({word:1})

		term_doc_freq.update({keyvals : unique_words})	

	unique_term_doc_freq = {}

	for keyvals in term_doc_freq.keys():
		for word in term_doc_freq[keyvals].keys():
			if word not in unique_term_doc_freq.keys() and len(word) < 25:
				unique_term_doc_freq.update({word:term_doc_freq[keyvals][word]})
			elif len(word) < 25:
				unique_term_doc_freq[word] += term_doc_freq[keyvals][word]

		
	get_frame = pandas.DataFrame()

	get_frame['Key'] = unique_term_doc_freq.keys()
	get_frame['Value'] = unique_term_doc_freq.values()

	get_frame = get_frame.sort_values('Value',ascending = 0)


	term_to_document =[]
	for keyvals in unique_term_doc_freq.keys():
		update_records = []
		for records in term_doc_freq.keys():
			if keyvals in term_doc_freq[records].keys():
				update_records.append(term_doc_freq[records][keyvals])
			else:
				update_records.append(0)
		term_to_document.append(update_records)


		
		
	frames = pandas.DataFrame(term_to_document, columns = term_doc_freq.keys(), index=unique_term_doc_freq.keys())

	frames['word_frequency'] = frames.sum(axis =1)
	frames = frames.sort_values('word_frequency', ascending = 0)

	vector_to_topic = frames.head(500)
	vector_to_topic = vector_to_topic.drop('word_frequency',axis=1)

	U, s, V = np.linalg.svd(vector_to_topic.T.values)

	s_matrix = pandas.DataFrame(s)
	#s_matrix.to_csv("c:\\users\\freddyca911\\desktop\\file2.csv")

	U_matrix = pandas.DataFrame(U)
	#U_matrix.to_csv("c:\\users\\freddyca911\\desktop\\file3.csv")

	V_matrix = pandas.DataFrame(V)
	#V_matrix.to_csv("c:\\users\\freddyca911\\desktop\\file4.csv")

	vector_to_topic.to_csv(output_directory + "top_words.csv")

	topic_model2 = LatentDirichletAllocation(n_topics=25).fit(vector_to_topic.T)

	no_top_words = 10

	topics_print = []
	def display_topics(model, feature_names, no_top_words):
		for topic_idx, topic in enumerate(model.components_):
			#print (" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
			topics_print.append(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
		return topics_print
							

	topics = display_topics(topic_model2, frames.T.columns, no_top_words)

	topics_frame = pandas.DataFrame(topics)
	topics_frame.to_csv(output_directory + "topics.csv")
	print("Testing")
	'''
	dicts_1 = pandas.DataFrame(term_doc_freq)
	dicts_1 = dicts_1.fillna(0)
	dicts_1['word_frequency'] = dicts_1.sum(axis =1)
	dicts_1 = dicts_1.sort_values('word_frequency')

	vector_to_topic = dicts_1.head(500)
	vector_to_topic = vector_to_topic.reset_index()
	vector_to_topic = vector_to_topic.drop('word_frequency', axis = 1)
	vector_to_topic = vector_to_topic.dropna()
	#vector_to_topic = vector_to_topic.as_matrix()

	vector_to_topic.T.to_csv("c:\\users\\freddyca911\\desktop\\file5.csv")

	U, s, V = np.linalg.svd(vector_to_topic.T.values, full_matrices = True)

	s_matrix = pandas.DataFrame(s)
	s_matrix.to_csv("c:\\users\\freddyca911\\desktop\\file2.csv")

	U_matrix = pandas.DataFrame(U)
	U_matrix.to_csv("c:\\users\\freddyca911\\desktop\\file3.csv")

	V_matrix = pandas.DataFrame(V)
	V_matrix.to_csv("c:\\users\\freddyca911\\desktop\\file4.csv")

	term_frequencies = dicts_1
	term_frequencies = term_frequencies[['word_frequency']]
	term_frequencies = term_frequencies.sort_values('word_frequency', ascending = 0)
	term_frequencies = term_frequencies.head(100)

	dicts_1.to_csv("c:\\users\\freddyca911\\desktop\\file.csv")
	term_frequencies.plot.bar()
	plt.show()



	'''
