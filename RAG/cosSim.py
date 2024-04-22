import numpy as np

def cosine_similarity(A, B):
    dot_product = np.dot(A, B)
    norm_a = np.linalg.norm(A)
    norm_b = np.linalg.norm(B)
    return dot_product / (norm_a * norm_b)

vector_A = np.array([1, 2, 3])
vector_B = np.array([4, 5, 6])
vector_C = np.array([7, 8, 9])

cos_sim_AC = cosine_similarity(vector_A, vector_C)
print(cos_sim_AC)

cos_sim_AB = cosine_similarity(vector_A, vector_B)
print(cos_sim_AB)