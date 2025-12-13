import ctypes
from importlib import resources
from .utilities import GrammarianException, GrammarianCheck

class Grammarian:
    def __init__(self):
        #creating base paths
        ##base_path reprezents a path to the grammarian module file
        base_path = resources.files("grammarian.src")
        ##so_path is a path to the resoure grammar.so - a C shared library
        self.so_path = base_path.joinpath("grammar.so")
        ##file_path is a path to the file words_alpha.txt
        ##words_alpha contains 370099 words of english language
        self.file_path = ctypes.c_char_p(str(base_path.joinpath("words_alpha.txt")).encode('utf-8'))
        #preparing grammar.so functions 
        ##introducing .so library
        self.grammar_checker = ctypes.CDLL(self.so_path)
        ##introducing a check_word fuc, a basic function to check if a word is in words_alpha.txt
        self.check_word = self.grammar_checker.check_word
        ##check_words argtypes are arguments which the check_words takes: first, the word to check, than path 
        self.check_word.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        ##restype is a bool
        self.check_word.restype = ctypes.c_bool
        ##seek corect introduced 
        self.seek_corects = self.grammar_checker.seek_corects
        ##argtypes of seek_corect are set here: first word, than path, than how many words do you want back
        self.seek_corects.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        ##introducing fuc free, to free pointers 
        self.free = self.grammar_checker.free_words
    def check_grammar(self, word : str, size: int = 5)->GrammarianCheck:
            #if how many words you want to be returned is grated than 0, initialize char tab pointer as 
            # restype of seek_corect and char pointer && an size int as argtypes of free
            if size > 0:
                self.seek_corects.restype = ctypes.POINTER(size * ctypes.c_char_p)
                self.free.argtypes = [ctypes.POINTER(size * ctypes.c_char_p), ctypes.c_int]

            word = word.replace(" ", "").lower().strip(".,<>/?'\\|=+-_*()&^%$#@![]{}")
            if(len(word) > 46):
                raise GrammarianException("Word given is too long. Grammarian checks words 46 letter long or shorter")
            byte_word = ctypes.c_char_p(word.encode('utf-8'))
            if self.check_word(byte_word, self.file_path):
                return GrammarianCheck(is_correct=True)
            else:
                if size <= 0:
                     return GrammarianCheck(is_correct=False)
                size_c = ctypes.c_int(size)
                suggestions = self.seek_corects(byte_word, self.file_path, size_c)
                response : list[str] = []
                for i in range(size):
                    response.append(suggestions.contents[i].decode('utf-8'))
                self.free(suggestions, size_c)
                return GrammarianCheck(is_correct=False, suggestions=response)

# g = Grammarian()
# print(g.check_grammar("pizza"))



