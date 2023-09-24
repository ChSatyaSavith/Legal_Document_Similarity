# Legal_Document_Similarity
The **Legal_Document_Similarity** class is designed for comparing legal documents to a corpus of legal text using TF-IDF vectorization and cosine similarity, allowing for the identification of similar legal content within documents.
````
git clone https://github.com/ChSatyaSavith/Legal_Document_Similarity.git
````
## Installation
### Dependencies
Legal_Document_Similarity requires:
- numpy (>=1.23.5)
- pandas (>=1.5.2)
- scikit-learn (>=1.2.2)
- nltk (>=3.8.1)
- python-docx (>=0.8.11)
- PyPDF2 (>=3.0.1)
- reportlab (>=3.6.8)

Installing requirements using ``pip``

    pip install -r requirements.txt



## Documentation

````
update_embeddings(pdf_path,law_book_sentences='law_book.txt',book_path = True,folder_path = False)
````
- Either pass the path of folder which contains law documents in which case set book_path = False and set folder_path = True or pass the path of law document in which case set book_path = True and set folder_path = False
- law_book_sentences contains the path of where the law book will be saved at
- Only call update_embeddings if you want to update the law book otherwise there is no need to call it

````
read_docx(folder_path)
````
- Pass the pdf path of the generated document

````
checkSimilarity()
````
- Checks the similarity between the generated document and the law book
- Create a dataframe which has three columns Generated_Document, Similar_Line in Acts and Similarity_Score
- Also creates a variable percentage_match which tells us the percentage of match between the generated document and the law book

````
save_Acts(path)
````
- Saves the dataframe in question, answer and similarity score format at the specified path

## Sample Code
````
from Similarity import LegalDocumentSimilarity
obj = LegalDocumentSimilarity()
obj.read_docx(pdf_path)
obj.checkSimilarity()
obj.save_Acts('output.pdf')
````
