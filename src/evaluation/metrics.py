import numpy as np

def hit_ratio_at_k(recommended_list, ground_truth, k):
    """
    Calculates Hit Ratio @ K.
    Returns 1 if any ground truth item is in the top K recommended items, else 0.
    """
    top_k = recommended_list[:k]
    for item in top_k:
        if item in ground_truth:
            return 1.0
    return 0.0

def ndcg_at_k(recommended_list, ground_truth, k):
    """
    Calculates Normalized Discounted Cumulative Gain (NDCG) @ K.
    Evaluates ranking quality, giving higher scores to relevant items at the top.
    """
    top_k = recommended_list[:k]
    dcg = 0.0
    idcg = 0.0
    
    for i, item in enumerate(top_k):
        if item in ground_truth:
            # log base 2 of (rank + 1). Rank is 1-indexed, so i + 2
            dcg += 1.0 / np.log2(i + 2)
            
    # Ideal DCG (all ground truth items are ranked at the top)
    for i in range(min(len(ground_truth), k)):
        idcg += 1.0 / np.log2(i + 2)
        
    if idcg == 0:
        return 0.0
    return dcg / idcg

def intra_list_diversity_at_k(recommended_list, item_embeddings, k):
    """
    Calculates Intra-List Diversity (ILD) @ K.
    Measures the average pairwise distance (1 - cosine similarity) between all items in the Top K list.
    Higher ILD means the recommendations are more diverse.
    """
    top_k = recommended_list[:k]
    if k < 2 or len(top_k) < 2:
        return 0.0
        
    diversity_sum = 0.0
    pairs = 0
    
    for i in range(len(top_k)):
        for j in range(i + 1, len(top_k)):
            emb_i = item_embeddings[top_k[i]]
            emb_j = item_embeddings[top_k[j]]
            
            # Cosine similarity
            dot_product = np.dot(emb_i, emb_j)
            norm_i = np.linalg.norm(emb_i)
            norm_j = np.linalg.norm(emb_j)
            
            if norm_i > 0 and norm_j > 0:
                sim = dot_product / (norm_i * norm_j)
            else:
                sim = 0.0
                
            distance = 1.0 - sim
            diversity_sum += distance
            pairs += 1
            
    if pairs == 0:
        return 0.0
        
    return diversity_sum / pairs
