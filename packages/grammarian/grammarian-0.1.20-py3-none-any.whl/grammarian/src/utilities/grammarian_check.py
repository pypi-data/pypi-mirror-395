class GrammarianCheck:
    def __init__(self, is_correct : bool, suggestions : list[str] = None):
        self.is_correct : bool = is_correct
        self.suggestions = suggestions
    def __str__(self):
        if self.is_correct:
            return f"Correct"
        else:
            if self.suggestions != None:
                return ' '.join(self.suggestions)
            else:
                return "Incorrect"