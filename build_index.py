import numpy as np, faiss
from sentence_transformers import SentenceTransformer

docs = [l.strip() for l in open('data/all_text.txt', encoding='utf-8') if l.strip()]
model = SentenceTransformer('intfloat/multilingual-e5-base')
emb = model.encode(docs).astype('float32')
np.save('data/embeddings.npy', emb)

dim = emb.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(emb)
faiss.write_index(index, 'data/faiss.index')
print('DONE INDEX')