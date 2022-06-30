
import torch
from torch_geometric.data import InMemoryDataset


class paDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super(paDataset, self).__init__(root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def raw_file_names(self):
        return []
    @property
    def processed_file_names(self):
        return ['../input/pa.dataset']

    def download(self):
        pass
    
    def process(self, data):
        
        data_list = []

        data_list.append(data)
        
        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])
