from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer

texto = """A tecnologia está transformando o mundo. 
Muitas empresas estão investindo em inteligência artificial para automatizar tarefas."""

# Aplicar RAKE
rake = Rake(language="portuguese", min_length=2)
rake.extract_keywords_from_text(texto)
rake_keywords = rake.get_ranked_phrases()[:5]  # Pega as 5 palavras-chave mais importantes

# Aplicar TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([texto])
feature_names = vectorizer.get_feature_names_out()
tfidf_scores = dict(zip(feature_names, tfidf_matrix.toarray()[0]))

# Ordenar palavras pelo peso no TF-IDF
sorted_tfidf = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)

# Exibir os resultados combinados
print("\n\nPalavras-chave RAKE:", rake_keywords)
print("\n\nPalavras-chave TF-IDF:", sorted_tfidf[:5])
print("\n")