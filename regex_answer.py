import re
import nltk
import en
be_verbs = ["am", 'is', "are", "been", "being", "was", "were" ]
modal_verbs = ["can", "could", "shall", "should", "will", "would", "may", "might"]
auxiliary_verbs_do = ["do", "does"]

negative_auxiliary_verbs_do = ["don't", "didn't", "doesn't", "isn't"]
auxiliary_verbs_have = ["have", "has"]

def question_transform_to_regex(question):
	print question
	tagged_question = nltk.pos_tag(question.split())
	print tagged_question

	tagged_question = tagged_question[1:]
	if tagged_question[0][0] == "did":
		tagged_question = from_did_to_past_tense(tagged_question)
	elif tagged_question[0][0] in be_verbs:
		be_verbs_formulation(tagged_question)
	elif tagged_question[0][0] in modal_verbs:
		modal_verbs_formulation(tagged_question)
	elif tagged_question[0][0] in auxiliary_verbs_do:
		auxiliary_verbs_do_formulation(tagged_question)
	elif tagged_question[0][0] in negative_auxiliary_verbs_do:
		tagged_question = negative_verbs_formulation(tagged_question)


	print [x[0] for x in tagged_question]

def be_verbs_formulation(tagged_question):
	pass

def modal_verbs_formulation(tagged_question):
	pass

def auxiliary_verbs_do_formulation(tagged_question):
	return tagged_question[1:]

def negative_verbs_formulation(tagged_question):
	for x in range(len(tagged_question[1:])):
		
		if tagged_question[x][1] == 'NN' or tagged_question[x][1] == 'NNS':
			#print x
			y = x
			while tagged_question[y+1][1] == 'NN' or tagged_question[y+1][1] == 'NNS':
				y+=1
			#print y
			return tagged_question[1:y+1] + [tagged_question[0]] + tagged_question[y+1:]

def from_did_to_past_tense(tagged_question):
	for x in range(len(tagged_question[1:])):
		if tagged_question[x][1] != 'VBP':
			#print x
			y = x
			while tagged_question[y][1] != 'VBP':
				y+=1
			#print y
 			#print tagged_question[y][0]
 			#print en.verb.past(tagged_question[y][0])
 			#print tagged_question[1:y+1][0]
 			#print tagged_question[y+1:][0]
			return tagged_question[1:y] + [(en.verb.past(tagged_question[y][0]),"VBD")] + tagged_question[y+1:]

def main():
	question_transform_to_regex("Why did barnett newman say he painted")
	
if __name__ == '__main__':
	main()