# -*- coding: utf-8 -*-
"""
CPSC 599 module: src.languages.english_canadian

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

def _amplifyContent(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, previous_phoneme_parameters, remaining_phoneme_parameter_count, previous_sound_parameters, following_sound_parameters, parameters):
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
	@type previous_phoneme_parameters: list
	@param previous_phoneme_parameters: A collection of all parameters that
	    appear as part of this phoneme, prior to the parameter-set currently
	    being manipulated.
	@type remaining_phoneme_parameter_count: int
	@param remaining_phoneme_parameter_count: The number of parameter-sets yet
	    to be processed as part of this phoneme.
	@type previous_sound_parameters: list
	@param previous_sound_parameters: A list of all preceding parameter-sets
	    introduced prior to the current paramter-set by language rules.
	@type following_sound_parameters: list
	@param following_sound_parameters: A list of all preceding parameter-sets
	    introduced after to the current paramter-set by language rules.
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
	
def _degradePitch(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, previous_phoneme_parameters, remaining_phoneme_parameter_count, previous_sound_parameters, following_sound_parameters, parameters):
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
	@type previous_phoneme_parameters: list
	@param previous_phoneme_parameters: A collection of all parameters that
	    appear as part of this phoneme, prior to the parameter-set currently
	    being manipulated.
	@type remaining_phoneme_parameter_count: int
	@param remaining_phoneme_parameter_count: The number of parameter-sets yet
	    to be processed as part of this phoneme.
	@type previous_sound_parameters: list
	@param previous_sound_parameters: A list of all preceding parameter-sets
	    introduced prior to the current paramter-set by language rules.
	@type following_sound_parameters: list
	@param following_sound_parameters: A list of all preceding parameter-sets
	    introduced after to the current paramter-set by language rules.
	@type parameters: list(33)
	@param parameters: A collection of parameters associated with the sound
	    currently being procesed.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if not is_question:
		decay_ratio = 1.0 - (0.05 / (word_position + remaining_words))
		return ([], [], 1.0 / (decay_ratio ** word_position))
	return ([], [], 1.0)
	
def _emphasizeSpeech(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, previous_phoneme_parameters, remaining_phoneme_parameter_count, previous_sound_parameters, following_sound_parameters, parameters):
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
	@type previous_phoneme_parameters: list
	@param previous_phoneme_parameters: A collection of all parameters that
	    appear as part of this phoneme, prior to the parameter-set currently
	    being manipulated.
	@type remaining_phoneme_parameter_count: int
	@param remaining_phoneme_parameter_count: The number of parameter-sets yet
	    to be processed as part of this phoneme.
	@type previous_sound_parameters: list
	@param previous_sound_parameters: A list of all preceding parameter-sets
	    introduced prior to the current paramter-set by language rules.
	@type following_sound_parameters: list
	@param following_sound_parameters: A list of all preceding parameter-sets
	    introduced after to the current paramter-set by language rules.
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
	
def _inflectQuestionPitch(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, previous_phoneme_parameters, remaining_phoneme_parameter_count, previous_sound_parameters, following_sound_parameters, parameters):
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
	@type previous_phoneme_parameters: list
	@param previous_phoneme_parameters: A collection of all parameters that
	    appear as part of this phoneme, prior to the parameter-set currently
	    being manipulated.
	@type remaining_phoneme_parameter_count: int
	@param remaining_phoneme_parameter_count: The number of parameter-sets yet
	    to be processed as part of this phoneme.
	@type previous_sound_parameters: list
	@param previous_sound_parameters: A list of all preceding parameter-sets
	    introduced prior to the current paramter-set by language rules.
	@type following_sound_parameters: list
	@param following_sound_parameters: A list of all preceding parameter-sets
	    introduced after to the current paramter-set by language rules.
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
					if word[0] == u'\u028d' or word in(u'hæw', u'hu', u'hum'): #'wh'
						return _inflectQuestionPitch_fall(remaining_words)
						
		if remaining_words == 0:
			return _inflectQuestionPitch_rise(preceding_phonemes, following_phonemes)
			
		word = u''.join(preceding_phonemes + [ipa_character] + following_phonemes)
		if word in (u'hæw', u'hu', u'hum', u'\u028d\u025b\u0279', '\u028d\u0259t', '\u028d\u025bn' u'\u028d\u028cj'): #where, what, when, why
			return _inflectQuestionPitch_initial_rise()
	return ([], [], 1.0)
	
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
		return ([], [], 1.075) #Lower pitch slightly on the second-last word.
	return ([], [], 1.125) #Lower pitch a bit more on the last word.
	
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
	return ([], [], (-0.05 + rise_ratio ** position))
	
def _lengthenTerminal(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, previous_phoneme_parameters, remaining_phoneme_parameter_count, previous_sound_parameters, following_sound_parameters, parameters):
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
	@type previous_phoneme_parameters: list
	@param previous_phoneme_parameters: A collection of all parameters that
	    appear as part of this phoneme, prior to the parameter-set currently
	    being manipulated.
	@type remaining_phoneme_parameter_count: int
	@param remaining_phoneme_parameter_count: The number of parameter-sets yet
	    to be processed as part of this phoneme.
	@type previous_sound_parameters: list
	@param previous_sound_parameters: A list of all preceding parameter-sets
	    introduced prior to the current paramter-set by language rules.
	@type following_sound_parameters: list
	@param following_sound_parameters: A list of all preceding parameter-sets
	    introduced after to the current paramter-set by language rules.
	@type parameters: list(33)
	@param parameters: A collection of parameters associated with the sound
	    currently being procesed.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if remaining_words == 0 and not ipa_character == u'\u0259' and ipa_character in ipa.VOWELS:
		parameters[32] *= 1.5 #Increase duration.
	return ([], [], 1.0)
	
def _liquidateVowels(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, previous_phoneme_parameters, remaining_phoneme_parameter_count, previous_sound_parameters, following_sound_parameters, parameters):
	"""
	Extends the sound of a liquid when it is immediately followed by a vowel.
	
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
	@type previous_phoneme_parameters: list
	@param previous_phoneme_parameters: A collection of all parameters that
	    appear as part of this phoneme, prior to the parameter-set currently
	    being manipulated.
	@type remaining_phoneme_parameter_count: int
	@param remaining_phoneme_parameter_count: The number of parameter-sets yet
	    to be processed as part of this phoneme.
	@type previous_sound_parameters: list
	@param previous_sound_parameters: A list of all preceding parameter-sets
	    introduced prior to the current paramter-set by language rules.
	@type following_sound_parameters: list
	@param following_sound_parameters: A list of all preceding parameter-sets
	    introduced after to the current paramter-set by language rules.
	@type parameters: list(33)
	@param parameters: A collection of parameters associated with the sound
	    currently being procesed.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if remaining_phoneme_parameter_count == 0 and following_phonemes and ipa_character in ipa.LIQUIDS and following_phonemes[0] in ipa.VOWELS:
		vowel_values = ipa.IPA_PARAMETERS[following_phonemes[0]]
		values = zip(parameters[:32], vowel_values[:32])
		return ([], [[(l + v * 2) / 3 for (l, v) in values] + [int(vowel_values[32] * 0.25)]], 1.0) #Compensate for universal blending; add 50% of both sounds for 25% of the vowel's length.
	return ([], [], 1.0)
	
def _quoteSpeech(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, previous_phoneme_parameters, remaining_phoneme_parameter_count, previous_sound_parameters, following_sound_parameters, parameters):
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
	@type previous_phoneme_parameters: list
	@param previous_phoneme_parameters: A collection of all parameters that
	    appear as part of this phoneme, prior to the parameter-set currently
	    being manipulated.
	@type remaining_phoneme_parameter_count: int
	@param remaining_phoneme_parameter_count: The number of parameter-sets yet
	    to be processed as part of this phoneme.
	@type previous_sound_parameters: list
	@param previous_sound_parameters: A list of all preceding parameter-sets
	    introduced prior to the current paramter-set by language rules.
	@type following_sound_parameters: list
	@param following_sound_parameters: A list of all preceding parameter-sets
	    introduced after to the current paramter-set by language rules.
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
	
def _shortenDipthong(ipa_character, preceding_phonemes, following_phonemes, word_position, remaining_words, previous_words, sentence_position, remaining_sentences, is_quoted, is_emphasized, is_content, is_question, is_exclamation, previous_phoneme_parameters, remaining_phoneme_parameter_count, previous_sound_parameters, following_sound_parameters, parameters):
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
	@type previous_phoneme_parameters: list
	@param previous_phoneme_parameters: A collection of all parameters that
	    appear as part of this phoneme, prior to the parameter-set currently
	    being manipulated.
	@type remaining_phoneme_parameter_count: int
	@param remaining_phoneme_parameter_count: The number of parameter-sets yet
	    to be processed as part of this phoneme.
	@type previous_sound_parameters: list
	@param previous_sound_parameters: A list of all preceding parameter-sets
	    introduced prior to the current paramter-set by language rules.
	@type following_sound_parameters: list
	@param following_sound_parameters: A list of all preceding parameter-sets
	    introduced after to the current paramter-set by language rules.
	@type parameters: list(33)
	@param parameters: A collection of parameters associated with the sound
	    currently being procesed.
	
	@rtype: tuple(3)
	@return: A list of parameter-sets that precede this sound, a list of
	    parameter-sets that follow this sound, and an f0 multiplier.
	
	@author: Sydni Bennie
	"""
	if preceding_phonemes and ipa_character in ipa.VOWELS and preceding_phonemes[-1] in ipa.VOWELS:
		parameters[32] *= 0.5 #Reduce duration.
	return ([], [], 1.0)
	

	
RULE_FUNCTIONS = (
 _liquidateVowels,
 _inflectQuestionPitch,
 _amplifyContent,
 _emphasizeSpeech,
 _quoteSpeech,
 _degradePitch,
 _lengthenTerminal,
 _shortenDipthong,
) #: A collection of all functions to call, in order, to apply this language's rules. 