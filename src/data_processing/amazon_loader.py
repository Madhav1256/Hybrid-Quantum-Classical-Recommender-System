import os
import pandas as pd
import torch
from torch_geometric.data import HeteroData
import json

class AmazonDatasetLoader:
    def __init__(self, raw_reviews_path, raw_meta_path, output_dir, k_core=5):
        self.raw_reviews_path = raw_reviews_path
        self.raw_meta_path = raw_meta_path
        self.output_dir = output_dir
        self.k_core = k_core
        os.makedirs(self.output_dir, exist_ok=True)
        
    def _k_core_filter(self, df):
        """Iteratively filters the dataset so every user and item has >= k_core interactions."""
        print(f"Original shape: {df.shape}")
        iteration = 1
        while True:
            user_counts = df['user_id'].value_counts()
            item_counts = df['parent_asin'].value_counts()
            
            valid_users = user_counts[user_counts >= self.k_core].index
            valid_items = item_counts[item_counts >= self.k_core].index
            
            new_df = df[(df['user_id'].isin(valid_users)) & (df['parent_asin'].isin(valid_items))]
            
            if len(new_df) == len(df):
                break
            df = new_df
            print(f"Iteration {iteration}: {df.shape}")
            iteration += 1
            
        print(f"Final shape after {self.k_core}-core filtering: {df.shape}")
        return df

    def process(self):
        print(f"Loading reviews from {self.raw_reviews_path}...")
        # Load interactions
        # We only need user_id, parent_asin, rating, timestamp
        df = pd.read_json(self.raw_reviews_path, lines=True)
        df = df[['user_id', 'parent_asin', 'rating', 'timestamp']]
        
        # Apply k-core filter to reduce sparsity and ensure GNN has enough signal
        print(f"Applying {self.k_core}-core filtering...")
        df = self._k_core_filter(df)
        
        # ID Mappings
        print("Creating integer ID mappings...")
        unique_users = df['user_id'].unique()
        unique_items = df['parent_asin'].unique()
        
        user2id = {uid: i for i, uid in enumerate(unique_users)}
        item2id = {iid: i for i, iid in enumerate(unique_items)}
        
        df['user_id_mapped'] = df['user_id'].map(user2id)
        df['item_id_mapped'] = df['parent_asin'].map(item2id)
        
        # Save mappings and filtered interactions
        print("Saving mappings and filtered interactions...")
        mapping_path = os.path.join(self.output_dir, 'mappings.json')
        with open(mapping_path, 'w') as f:
            json.dump({'user2id': user2id, 'item2id': item2id}, f)
            
        interactions_path = os.path.join(self.output_dir, 'interactions.csv')
        df.to_csv(interactions_path, index=False)
        
        # Create PyTorch Geometric HeteroData
        print("Building PyTorch Geometric HeteroData graph...")
        data = HeteroData()
        
        # Edges
        edge_index = torch.tensor([df['user_id_mapped'].values, df['item_id_mapped'].values], dtype=torch.long)
        # Ratings as edge weights/attributes
        edge_weight = torch.tensor(df['rating'].values, dtype=torch.float32)
        
        data['user'].num_nodes = len(unique_users)
        data['item'].num_nodes = len(unique_items)
        data['user', 'rates', 'item'].edge_index = edge_index
        data['user', 'rates', 'item'].edge_weight = edge_weight
        
        # Undirected graph for message passing
        data['item', 'rated_by', 'user'].edge_index = edge_index.flip([0])
        data['item', 'rated_by', 'user'].edge_weight = edge_weight
        
        graph_path = os.path.join(self.output_dir, 'graph.pt')
        torch.save(data, graph_path)
        
        print(f"Data processing complete! Processed {data['user'].num_nodes} users and {data['item'].num_nodes} items.")
        print(f"Files saved to {self.output_dir}")
        return data

if __name__ == "__main__":
    # Define paths
    REVIEWS_PATH = "data/raw/amazon_reviews_2023/All_Beauty/raw/review_categories/All_Beauty.jsonl"
    META_PATH = "data/raw/amazon_reviews_2023/All_Beauty/raw/meta_categories/meta_All_Beauty.jsonl"
    OUTPUT_DIR = "data/processed/amazon_all_beauty"
    
    loader = AmazonDatasetLoader(REVIEWS_PATH, META_PATH, OUTPUT_DIR, k_core=5)
    loader.process()
