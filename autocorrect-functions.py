

#process data function
def process_data(file_name):
    """
    Input: 
        A file_name which is found in your current directory. You just have to read it in. 
    Output: 
        words: a list containing all the words in the corpus (text file you read) in lower case. 
    """
    import re
    words = [] 

    #read file & replace \n with ' '
    with open(file_name, 'r', encoding='utf-8') as corpus:
        corpus = corpus.read().replace('\n', ' ')
    
    #convert all to lower case & get words
    corpus = corpus.lower();
    words = re.findall(r'\w+', corpus);
    
    return words


#get word counts & probabilities
def get_count(word_l):
    '''
    Input:
        word_l: a set of words representing the corpus. 
    Output:
        word_count_dict: The wordcount dictionary where key is the word and value is its frequency.
    '''
    
    #dict with word counts
    word_count_dict = {};
    
    #get word counts for each word
    for w in word_l:
        word_count_dict[w] = word_count_dict.get(w, 0) + 1
            
    return word_count_dict


def get_probs(word_count_dict):
    '''
    Input:
        word_count_dict: The wordcount dictionary where key is the word and value is its frequency.
    Output:
        probs: A dictionary where keys are the words and the values are the probability that a word will occur. 
    '''
    probs = {}  
    
    #get word probabilities for each word
    for word in word_count_dict:
        probs[word] = word_count_dict[word]/sum(word_count_dict.values())
    
    return probs


#modify letters of word
def delete_letter(word, verbose=False):
    '''
    Input:
        word: the string/word for which you will generate all possible words 
                in the vocabulary which have 1 missing character
    Output:
        delete_l: a list of all possible strings obtained by deleting 1 character from word
    '''
    
    #get all possible deletes from splits & store in lists
    split_l = [(word[:i], word[i:]) for i in range(len(word)+1) if len(word[i:]) > 0]
    delete_l = [word1 + word2[1:] for word1, word2 in split_l]
    
    if verbose: print(f"input word {word}, \nsplit_l = {split_l}, \ndelete_l = {delete_l}")

    return delete_l

def switch_letter(word, verbose=False):
    '''
    Input:
        word: input string
     Output:
        switches: a list of all possible strings with one adjacent charater switched
    ''' 

    
    #get all possible splits then construct list of switches
    split_l = [(word[:i], word[i:]) for i in range(len(word)+1) if len(word[i:]) > 0];
    switch_l = [L + R[1] + R[0] + R[2:] for L, R in split_l if len(R)>1];
    
    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nswitch_l = {switch_l}") 

    return switch_l


def replace_letter(word, verbose=False):
    '''
    Input:
        word: the input string/word 
    Output:
        replaces: a list of all possible strings where we replaced one letter from the original word. 
    ''' 
    #all possible letters
    letters = 'abcdefghijklmnopqrstuvwxyz'
    
    #get splits
    split_l = [(word[:i], word[i:]) for i in range(len(word)+1) if len(word[i:]) > 0]
        
    #get set of replaces
    replace_set = set([a+c+b[1:] for a, b in split_l for c in letters])
    for w, w1 in split_l: replace_set.discard(w); replace_set.discard(w1);
        
    # turn the set back into a list and sort it, for easier viewing
    replace_l = sorted(list(replace_set))
    
    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nreplace_l {replace_l}")   
    
    return replace_l


def insert_letter(word, verbose=False):
    '''
    Input:
        word: the input string/word 
    Output:
        inserts: a set of all possible strings with one new letter inserted at every offset
    ''' 
    #get letters & list for inserts to return
    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_l = []
    
    #get all splits & possible inserts
    split_l = [(word[:i], word[i:]) for i in range(len(word)+1) if len(word[i:]) >= 0];
    insert_l = [a+c+b for a, b in split_l for c in letters];
    
    if verbose: print(f"Input word {word} \nsplit_l = {split_l} \ninsert_l = {insert_l}")
    
    return insert_l


#edit one or two letters of word
def edit_one_letter(word, allow_switches = True):
    """
    Input:
        word: the string/word for which we will generate all possible wordsthat are one edit away.
    Output:
        edit_one_set: a set of words with one possible edit. Please return a set. and not a list.
    """
    #create set
    edit_one_set = set()
    
    #add all possible variations to list
    l1 = insert_letter(word, verbose=False); 
    l1 = l1 + replace_letter(word, verbose=False);
    l1 = l1 + delete_letter(word, verbose=False); 
    
    #if switches are allowed add to list
    if allow_switches: l1 = l1 + switch_letter(word);
        
    #create set 
    edit_one_set = set(l1)

    return edit_one_set


def edit_two_letters(word, allow_switches = True):
    '''
    Input:
        word: the input string/word 
    Output:
        edit_two_set: a set of strings with all possible two edits
    '''
    
    edit_two_set = set()
    
    #
    tmp_edit_one_set = edit_one_letter(word)
    for mod_word in tmp_edit_one_set:
        edit_two_set = edit_two_set.union(edit_one_letter(mod_word))
    
    return edit_two_set


#get corrections for word
def get_corrections(word, probs, vocab, word_count_dict, n=2, verbose = False):
    '''
    Input: 
        word: a user entered string to check for suggestions
        probs: a dictionary that maps each word to its probability in the corpus
        vocab: a set containing all the vocabulary
        n: number of possible word corrections you want returned in the dictionary
    Output: 
        n_best: a list of tuples with the most probable n corrected words and their probabilities.
    '''
    from collections import Counter
    import numpy as np, pandas as pd
    
    suggestions = []
    n_best = []
    
    #
    if word in vocab:
        return word;
    elif edit_one_letter(word, allow_switches = True).intersection(vocab):
        suggestions = edit_one_letter(word, allow_switches = True).intersection(vocab);
    elif edit_two_letters(word, allow_switches = True).intersection(vocab):
        suggestions = edit_two_letters(word, allow_switches = True).intersection(vocab);
    else: 
        return word

    best_words = {};
    for word1 in suggestions:
        if word1 in vocab:
            best_words[word1] = get_probs(word_count_dict)[word1]
    
    n_best = Counter(best_words).most_common(n)

    
    if verbose: print("entered word = ", word, "\nsuggestions = ", suggestions)

    return n_best






