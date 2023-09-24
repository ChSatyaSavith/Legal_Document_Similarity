#Importing Libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pandas as pd
import PyPDF2
import docx
import os

#Importing Libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pandas as pd
import PyPDF2
import docx
import os

#Class For Similarity Checker
class LegalDocumentSimilarity:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        
        #Initializing the TF-IDF for Law Book if it Exists
        if os.path.exists('law_book.txt'):
            lines = []
            with open('law_book.txt') as file:
                for line in file:
                    lines.append(line.strip('\n'))
            self.book_lines = lines
            self.law_corpus_tfidf = self.vectorizer.fit_transform(lines)
            
    def update_embeddings(self,pdf_path,law_book_sentences='law_book.txt',book_path = True,folder_path = False):
        #Generating Lines for the Book User Passed
        self.book_lines = []
        if(book_path):
            text = ""
            with open(pdf_path, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
            self.book_lines = text.split('\n')
        elif(folder_path):
            for filename in os.listdir(pdf_path):
                if filename.endswith(".pdf"):
                    pdf_file_path = os.path.join(pdf_path, filename)
                    text = ""
                    with open(pdf_file_path, "rb") as pdf_file:
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        for page_num in range(len(pdf_reader.pages)):
                            page = pdf_reader.pages[page_num]
                            text += page.extract_text()
                    self.book_lines.extend(text.split('\n'))
        
        #Updating Text File of Law Books Here
        if os.path.exists(law_book_sentences):
            with open(law_book_sentences,'a') as file:
                for item in self.book_lines:
                    file.write(item+'\n')
        if not os.path.exists(law_book_sentences):
            with open(law_book_sentences,'w') as file:
                for item in self.book_lines:
                    file.write(item+'\n')
         
        #Creating Vectorizer for the Updated Law Book
        self.book_lines = []
        with open(law_book_sentences,'r') as file:
            for line in file:
                self.book_lines.append(line.strip('\n'))
                
        #Updating the Law Corpus TF-IDF
        self.law_corpus_tfidf = self.vectorizer.fit_transform(self.book_lines)
        
    def read_docx(self,pdf_path):
        #Reading all the Documents given the Folder Path
        self.doc_sentences = []
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
        doc_sentences = sent_tokenize(text)
        self.doc_sentences.extend(doc_sentences)
        self.document_tfidf = self.vectorizer.transform(self.doc_sentences)
        
    def checkSimilarity(self):
        similarity = []
        similarity_score = []  # List to store similarity scores

        for i, doc_sentence in enumerate(self.doc_sentences):
            similarities = cosine_similarity(self.document_tfidf[i], self.law_corpus_tfidf)
            index = similarities.argmax()
            similarity.append(self.book_lines[index])
            similarity_score.append(similarities[0][index])  # Store similarity score

        # Create a DataFrame with Doc_Sentences, Similar_Line, and Similarity_Score columns
        self.dataframe = pd.DataFrame()
        self.dataframe["Generated Document"] = self.doc_sentences
        self.dataframe['Similar_Line in Acts'] = similarity
        self.dataframe['Similarity_Score'] = similarity_score

        # Define a regular expression pattern to match rows with only numeric values or special characters
        pattern = r'^[0-9\W_]+$'

        # Filter out rows where either column contains only numeric values or special characters
        self.dataframe = self.dataframe[~(self.dataframe['Generated Document'].str.match(pattern) | self.dataframe['Similar_Line in Acts'].str.match(pattern))]
        self.dataframe['Generated Document'] = self.dataframe['Generated Document'].str.replace(r'\n', ' ').str.replace(r'[^a-zA-Z0-9\s]', '')
        self.dataframe['Similar_Line in Acts'] = self.dataframe['Similar_Line in Acts'].str.replace(r'\n', ' ').str.replace(r'[^a-zA-Z0-9\s]', '')
        self.percentage_match = (len(self.dataframe)/len(self.doc_sentences))*100
        
    
    def create_pdf(self,df, filename):
        c = canvas.Canvas(filename, pagesize=A4)

        # Define the starting position for text
        x, y = 50, A4[1] - 50  # Start from the top of the page
        num = 1
        for index, row in df.iterrows():
            question = row['Generated Document']
            answer = row['Similar_Line in Acts']
            number = row['Similarity_Score']

            # Write question, answer, and number to PDF
            c.setFont("Helvetica", 8)
            c.drawString(x, y, f"{num}) Question: {question[:130]}")
            y -= 20  # Move down for answer
            c.drawString(x, y, f"{question[130:]}")
            y-=20
            c.drawString(x, y, f"Answer: {answer}")
            y-=20
            c.drawString(x, y, f"Similarity: {number}")
            y -= 40  # Move down for the next question

            # Check if we need to start a new page
            if y < 50:
                c.showPage()
                y = A4[1] - 50  # Start from the top of the new page
            num+=1

        # Save the PDF file
        c.save()
        
    def save_Acts(self,path):
        self.create_pdf(self.dataframe,path)

