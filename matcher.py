from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def match_jobs(resume_text, jobs):
    job_descriptions = [job['description'] for job in jobs]
    resume_embedding = model.encode([resume_text])
    job_embeddings = model.encode(job_descriptions)

    scores = cosine_similarity(resume_embedding, job_embeddings)[0]

    ranked = sorted(zip(jobs, scores), key=lambda x: x[1], reverse=True)
    return ranked
