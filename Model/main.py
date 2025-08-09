import string

def load_FAQ(filepath):
               faq_dict={}
               current_question=None

               with open(filepath,'r',encoding='utf-8') as f:
                       for line in f:
                              line=line.strip()
                              if line.startswith("Q:"):
                                       current_question=line[2:].strip.lower()
                              elif line.startswith("A:") and current_question:
                                      answer=line[2:].strip
                                      faq_dict[current_question]=answer
                                      current_question=None
               return faq_dict

def normalize(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation)).strip()
