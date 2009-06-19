# -*- coding: utf-8 -*-
"""
CPSC 599 module: src.language_rules

Purpose
=======
 Contains a collection of rules to apply to phonemes.
 
Language
========
 This file applies to Canadian English.
 
Legal
=====
 All code, unless otherwise indicated, is original, and subject to the
 terms of the GPLv2, which is provided in COPYING.
 
 (C) Neil Tallim, Sydni Bennie, 2009
"""
import src.ipa as ipa

def _inflectQuestionPitch(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, parameters):
	"""
	Changes the pitch at the end of a question-sentence, rising in most cases,
	and falling in the case of a 'wh' question.
	
	This function may modify the input parameter-set.
	
	@type ipa_character: unicode
	@param ipa_character: The character, representative of a phoneme, being
	    processed.
	@type preceding_phonemes: sequence
	@param preceding_phonemes: A collection of all phonemes, in order, that
	    precede the current IPA character in the current word.
	@type following_phonemes: sequence
	@param following_phonemes: A collection of all phonemes, in order, that
	    follow the current IPA character in the current word.
	@type word_position: int
	@param word_position: The current word's position in its sentence, indexed
	    from 1.
	@type remaining_words: int
	@param remaining_words: The number of words remaining before the end of the
	    sentence is reached, not including the current word.
	@type previous_words: sequence
	@param previous_words: A collection of all words that have been previously
	    synthesized.
	@type sentence_position: int
	@param sentence_position: The current sentence's position in its paragraph,
	    indexed from 1.
	@type remaining_sentences: int
	@param remaining_sentences: The number of sentences remaining before the end
	    of the paragraph is reached, not including the current sentence.
	@type is_quoted: bool
	@param is_quoted: True if the current word is part of a quoted body.
	@type is_emphasized: bool
	@param is_emphasized: True if the current word is part of an emphasized body.
	@type is_content: bool
	@param is_content: True if the current word was marked as a content word.
	@type is_question: bool
	@param is_question: True if the current sentence ends with a question mark.
	@type is_exclamation: bool
	@param is_exclamation: True if the current sentence ends with an exclamation
	    mark.
	@type parameters: list(33)
	@param parameters: A collection of parameters associated with the sound
	    currently being procesed.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if not ipa_character == u'\u0259' and is_question and ipa_character in ipa.VOWELS: #No schwas allowed.
		if remaining_words <= 1: #Ignore questions and early positions in sentences.
			if previous_words:
				for word in previous_words:
					if word[0] == u'\u028d' or word in(u'hæw', 'hu'):
						return _inflectQuestionPitch_fall(remaining_words)
						
		if remaining_words == 0:
			return _inflectQuestionPitch_rise(preceding_phonemes, following_phonemes)
			
		word = u''.join(preceding_phonemes + [ipa_character] + following_phonemes)
		if word in (u'hæw', u'hu', u'\u028d\u025b\u0279', '\u028d\u0259t', '\u028d\u025bn' u'\u028d\u028cj'):
			return _inflectQuestionPitch_initial_rise()
	return ([], [], 1.0)
	
def _inflectQuestionPitch_rise(preceding_phonemes, following_phonemes):
	"""
	Implements the rising-intonation branch of question-inflection.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	position = len([p for p in preceding_phonemes if p in ipa.VOWELS])
	rise_ratio = 1.0 - (0.11 / (position + len([p for p in following_phonemes if p in ipa.VOWELS]) + 1))
	return ([], [], (rise_ratio ** position))
	
def _inflectQuestionPitch_initial_rise():
	"""
	Implements the rising-intonation branch of question-inflection. to a word
	that starts a question segment.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	return ([], [], 0.9) #Increase pitch.
	
def _inflectQuestionPitch_fall(remaining_words):
	"""
	Implements the falling-intonation branch of question-inflection.
	
	@type remaining_words: int
	@param remaning_words: The number of words remaining before the end of the
	    sentence is reached, not including the current word.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if remaining_words == 1:
		return ([], [], 1.05) #Lower pitch slightly on the second-last word.
	return ([], [], 1.1) #Lower pitch a bit more on the last word.
	
def _amplifyContent(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, parameters):
	"""
	Increases the emphasis placed on a word identified as content-bearing in a
	sentence.
	
	This function may modify the input parameter-set.
	
	@type ipa_character: unicode
	@param ipa_character: The character, representative of a phoneme, being
	    processed.
	@type preceding_phonemes: sequence
	@param preceding_phonemes: A collection of all phonemes, in order, that
	    precede the current IPA character in the current word.
	@type following_phonemes: sequence
	@param following_phonemes: A collection of all phonemes, in order, that
	    follow the current IPA character in the current word.
	@type word_position: int
	@param word_position: The current word's position in its sentence, indexed
	    from 1.
	@type remaining_words: int
	@param remaining_words: The number of words remaining before the end of the
	    sentence is reached, not including the current word.
	@type previous_words: sequence
	@param previous_words: A collection of all words that have been previously
	    synthesized.
	@type sentence_position: int
	@param sentence_position: The current sentence's position in its paragraph,
	    indexed from 1.
	@type remaining_sentences: int
	@param remaining_sentences: The number of sentences remaining before the end
	    of the paragraph is reached, not including the current sentence.
	@type is_quoted: bool
	@param is_quoted: True if the current word is part of a quoted body.
	@type is_emphasized: bool
	@param is_emphasized: True if the current word is part of an emphasized body.
	@type is_content: bool
	@param is_content: True if the current word was marked as a content word.
	@type is_question: bool
	@param is_question: True if the current sentence ends with a question mark.
	@type is_exclamation: bool
	@param is_exclamation: True if the current sentence ends with an exclamation
	    mark.
	@type parameters: list(33)
	@param parameters: A collection of parameters associated with the sound
	    currently being procesed.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if is_content and not ipa_character == u'\u0259':
		parameters[5] *= 1.25 #Boost f1.
		if ipa_character in ipa.VOWELS:
			parameters[32] *= 1.1 #Increase duration, just a little.
			return ([], [], 0.95) #Increase pitch, just a little.
	return ([], [], 1.0)
	
def _degradePitch(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, parameters):
	"""
	Lowers the pitch exponentially over the course of a spoken sentence.
	
	This function may modify the input parameter-set.
	
	@type ipa_character: unicode
	@param ipa_character: The character, representative of a phoneme, being
	    processed.
	@type preceding_phonemes: sequence
	@param preceding_phonemes: A collection of all phonemes, in order, that
	    precede the current IPA character in the current word.
	@type following_phonemes: sequence
	@param following_phonemes: A collection of all phonemes, in order, that
	    follow the current IPA character in the current word.
	@type word_position: int
	@param word_position: The current word's position in its sentence, indexed
	    from 1.
	@type remaining_words: int
	@param remaining_words: The number of words remaining before the end of the
	    sentence is reached, not including the current word.
	@type previous_words: sequence
	@param previous_words: A collection of all words that have been previously
	    synthesized.
	@type sentence_position: int
	@param sentence_position: The current sentence's position in its paragraph,
	    indexed from 1.
	@type remaining_sentences: int
	@param remaining_sentences: The number of sentences remaining before the end
	    of the paragraph is reached, not including the current sentence.
	@type is_quoted: bool
	@param is_quoted: True if the current word is part of a quoted body.
	@type is_emphasized: bool
	@param is_emphasized: True if the current word is part of an emphasized body.
	@type is_content: bool
	@param is_content: True if the current word was marked as a content word.
	@type is_question: bool
	@param is_question: True if the current sentence ends with a question mark.
	@type is_exclamation: bool
	@param is_exclamation: True if the current sentence ends with an exclamation
	    mark.
	@type parameters: list(33)
	@param parameters: A collection of parameters associated with the sound
	    currently being procesed.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if not is_question:
		decay_ratio = 1.0 - (0.1 / (word_position + remaining_words))
		return ([], [], 1.0 / (decay_ratio ** word_position))
	return ([], [], 1.0)
	
def _quoteSpeech(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, parameters):
	"""
	Raises the pitch and volume of quoted speech while shortening its duration.
	
	This function may modify the input parameter-set.
	
	@type ipa_character: unicode
	@param ipa_character: The character, representative of a phoneme, being
	    processed.
	@type preceding_phonemes: sequence
	@param preceding_phonemes: A collection of all phonemes, in order, that
	    precede the current IPA character in the current word.
	@type following_phonemes: sequence
	@param following_phonemes: A collection of all phonemes, in order, that
	    follow the current IPA character in the current word.
	@type word_position: int
	@param word_position: The current word's position in its sentence, indexed
	    from 1.
	@type remaining_words: int
	@param remaining_words: The number of words remaining before the end of the
	    sentence is reached, not including the current word.
	@type previous_words: sequence
	@param previous_words: A collection of all words that have been previously
	    synthesized.
	@type sentence_position: int
	@param sentence_position: The current sentence's position in its paragraph,
	    indexed from 1.
	@type remaining_sentences: int
	@param remaining_sentences: The number of sentences remaining before the end
	    of the paragraph is reached, not including the current sentence.
	@type is_quoted: bool
	@param is_quoted: True if the current word is part of a quoted body.
	@type is_emphasized: bool
	@param is_emphasized: True if the current word is part of an emphasized body.
	@type is_content: bool
	@param is_content: True if the current word was marked as a content word.
	@type is_question: bool
	@param is_question: True if the current sentence ends with a question mark.
	@type is_exclamation: bool
	@param is_exclamation: True if the current sentence ends with an exclamation
	    mark.
	@type parameters: list(33)
	@param parameters: A collection of parameters associated with the sound
	    currently being procesed.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if is_quoted:
		parameters[27] += 5 #Boost bypass gain.
		parameters[32] *= 0.925 #Reduce duration.
		return ([], [], 0.975) #Increase pitch.
	return ([], [], 1.0)
	
def _emphasizeSpeech(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, parameters):
	"""
	Raises the pitch and volume of bolded speech while lengthening its duration.
	
	This function may modify the input parameter-set.
	
	@type ipa_character: unicode
	@param ipa_character: The character, representative of a phoneme, being
	    processed.
	@type preceding_phonemes: sequence
	@param preceding_phonemes: A collection of all phonemes, in order, that
	    precede the current IPA character in the current word.
	@type following_phonemes: sequence
	@param following_phonemes: A collection of all phonemes, in order, that
	    follow the current IPA character in the current word.
	@type word_position: int
	@param word_position: The current word's position in its sentence, indexed
	    from 1.
	@type remaining_words: int
	@param remaining_words: The number of words remaining before the end of the
	    sentence is reached, not including the current word.
	@type previous_words: sequence
	@param previous_words: A collection of all words that have been previously
	    synthesized.
	@type sentence_position: int
	@param sentence_position: The current sentence's position in its paragraph,
	    indexed from 1.
	@type remaining_sentences: int
	@param remaining_sentences: The number of sentences remaining before the end
	    of the paragraph is reached, not including the current sentence.
	@type is_quoted: bool
	@param is_quoted: True if the current word is part of a quoted body.
	@type is_emphasized: bool
	@param is_emphasized: True if the current word is part of an emphasized body.
	@type is_content: bool
	@param is_content: True if the current word was marked as a content word.
	@type is_question: bool
	@param is_question: True if the current sentence ends with a question mark.
	@type is_exclamation: bool
	@param is_exclamation: True if the current sentence ends with an exclamation
	    mark.
	@type parameters: list(33)
	@param parameters: A collection of parameters associated with the sound
	    currently being procesed.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if is_emphasized and ipa_character not in ipa.STOPS:
		parameters[27] += 5 #Boost bypass gain.
		parameters[32] *= 1.1 #Increase duration.
		return ([], [], 0.95) #Increase pitch, sligthly.
	return ([], [], 1.0)
	
def _lengthenTerminal(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, parameters):
	"""
	Lengthens the duration of each vowel in the final word of a sentence.
	
	This function may modify the input parameter-set.
	
	@type ipa_character: unicode
	@param ipa_character: The character, representative of a phoneme, being
	    processed.
	@type preceding_phonemes: sequence
	@param preceding_phonemes: A collection of all phonemes, in order, that
	    precede the current IPA character in the current word.
	@type following_phonemes: sequence
	@param following_phonemes: A collection of all phonemes, in order, that
	    follow the current IPA character in the current word.
	@type word_position: int
	@param word_position: The current word's position in its sentence, indexed
	    from 1.
	@type remaining_words: int
	@param remaining_words: The number of words remaining before the end of the
	    sentence is reached, not including the current word.
	@type previous_words: sequence
	@param previous_words: A collection of all words that have been previously
	    synthesized.
	@type sentence_position: int
	@param sentence_position: The current sentence's position in its paragraph,
	    indexed from 1.
	@type remaining_sentences: int
	@param remaining_sentences: The number of sentences remaining before the end
	    of the paragraph is reached, not including the current sentence.
	@type is_quoted: bool
	@param is_quoted: True if the current word is part of a quoted body.
	@type is_emphasized: bool
	@param is_emphasized: True if the current word is part of an emphasized body.
	@type is_content: bool
	@param is_content: True if the current word was marked as a content word.
	@type is_question: bool
	@param is_question: True if the current sentence ends with a question mark.
	@type is_exclamation: bool
	@param is_exclamation: True if the current sentence ends with an exclamation
	    mark.
	@type parameters: list(33)
	@param parameters: A collection of parameters associated with the sound
	    currently being procesed.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if remaining_words == 0 and not ipa_character == u'\u0259' and ipa_character in ipa.VOWELS:
		parameters[32] *= 1.5
	return ([], [], 1.0)
	
def _shortenDipthong(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, parameters):
	"""
	Reduces the length of a vowel that immediately follows another vowel in a
	word.
	
	This function may modify the input parameter-set.
	
	@type ipa_character: unicode
	@param ipa_character: The character, representative of a phoneme, being
	    processed.
	@type preceding_phonemes: sequence
	@param preceding_phonemes: A collection of all phonemes, in order, that
	    precede the current IPA character in the current word.
	@type following_phonemes: sequence
	@param following_phonemes: A collection of all phonemes, in order, that
	    follow the current IPA character in the current word.
	@type word_position: int
	@param word_position: The current word's position in its sentence, indexed
	    from 1.
	@type remaining_words: int
	@param remaining_words: The number of words remaining before the end of the
	    sentence is reached, not including the current word.
	@type previous_words: sequence
	@param previous_words: A collection of all words that have been previously
	    synthesized.
	@type sentence_position: int
	@param sentence_position: The current sentence's position in its paragraph,
	    indexed from 1.
	@type remaining_sentences: int
	@param remaining_sentences: The number of sentences remaining before the end
	    of the paragraph is reached, not including the current sentence.
	@type is_quoted: bool
	@param is_quoted: True if the current word is part of a quoted body.
	@type is_emphasized: bool
	@param is_emphasized: True if the current word is part of an emphasized body.
	@type is_content: bool
	@param is_content: True if the current word was marked as a content word.
	@type is_question: bool
	@param is_question: True if the current sentence ends with a question mark.
	@type is_exclamation: bool
	@param is_exclamation: True if the current sentence ends with an exclamation
	    mark.
	@type parameters: list(33)
	@param parameters: A collection of parameters associated with the sound
	    currently being procesed.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if preceding_phonemes and ipa_character in ipa.VOWELS and preceding_phonemes[-1] in ipa.VOWELS:
		parameters[32] *= 0.5
	return ([], [], 1.0)
	
RULE_FUNCTIONS = (
 _inflectQuestionPitch,
 _amplifyContent,
 _emphasizeSpeech,
 _quoteSpeech,
 _degradePitch,
 _lengthenTerminal,
 _shortenDipthong,
) #: A collection of all functions to call, in order, to apply this language's rules. 
