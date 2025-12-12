
# import torch
# from torch.utils.data import Dataset
from pathlib import Path
from datasets import load_dataset, DatasetDict, Image as datasets_image
from typing import Optional, Callable
import os


# class ImageClassificationDataset(Dataset):
#     """
#     image classification dataset.

#     This dataset reads metadata from a single Parquet file and constructs
#     image paths on-the-fly to reduce initialization time and memory usage.

#     Args:
#         data_dir (str): The root directory where datasets are stored.
#         dataset_name (str): The specific name of the dataset folder.
#         split (str): The data split to use (e.g., 'train', 'test').
#         transform (callable, optional): A function/transform that takes in a PIL image
#             and returns a transformed version.
#     """
#     def __init__(
#         self,
#         data_dir: str,
#         dataset_name: str,
#         split: str,
#         transform: Optional[Callable] = None
#     ):
#         self.data_dir = data_dir
#         self.dataset_name = dataset_name
#         self.split = split
#         self.transform = transform

#         metadata_path = Path(data_dir) / dataset_name / "metadata.parquet"
#         if not metadata_path.exists():
#             raise FileNotFoundError(f"Metadata file not found at {metadata_path}")
        
#         # Load the entire split into memory once. This is efficient.
#         dataset_split = load_dataset("parquet", data_files=str(metadata_path))["train"].filter(lambda x: x['split'] == split)

        
#         self.root_dir = Path(data_dir) / dataset_name
#         self.relative_paths = dataset_split['file_path']
#         self.labels = dataset_split['label']
        
#         # Ensure the data is consistent
#         assert len(self.relative_paths) == len(self.labels), "Mismatch between number of images and labels."

#     def __len__(self) -> int:
#         return len(self.labels)

#     def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
#         label = self.labels[idx]

#         image_path = self.root_dir / self.relative_paths[idx]

#         try:
#             image = Image.open(image_path).convert("RGB")
#         except FileNotFoundError:
#             raise FileNotFoundError(f"Image file not found at {image_path}. "
#                                     f"Check if your parquet file paths are correct relative to '{self.root_dir}'.")

#         if self.transform:
#             image = self.transform(image)

#         return image, label

# class TextGenerationDataset(Dataset):
#     """
#     A PyTorch Dataset for loading instruction-response pairs for text generation.
    
#     This class reads sharded Parquet files, extracts user instructions and
#     assistant responses from a 'messages' column, and stores them for retrieval.
#     """
#     def __init__(self, data_dir: str, dataset_name: str, split: str):
#         """
#         Loads and processes the instruction-response data.
#         """
#         # --- 1. Loading of Instruction and Response Part ---

#         # Construct the full path to the directory containing the split's data files
#         split_path = Path(data_dir) / dataset_name / split
#         if not split_path.exists():
#             raise FileNotFoundError(f"Data directory for split '{split}' not found at {split_path}")

#         raw_dataset = load_dataset("parquet", data_files=str(split_path)+"/*.parquet",)['train']

#         # Initialize lists to hold our processed data
#         self.instructions: List[str] = []
#         self.responses: List[str] = []
        
#         # Iterate through the raw dataset to parse the 'messages' column
#         for example in raw_dataset:
#             messages = example['messages']
            
#             # Ensure the conversation has at least a user and assistant turn
#             if len(messages) >= 2 and messages[0]['role'] == 'user' and messages[1]['role'] == 'assistant':
#                 self.instructions.append(messages[0]['content'])
#                 self.responses.append(messages[1]['content'])
#             # Malformed examples are skipped

#     def __len__(self) -> int:
#         """
#         Returns the total number of instruction-response pairs.
#         """
#         return len(self.instructions)

#     def __getitem__(self, idx: int) -> Dict[str, str]:
#         """
#         Retrieves the instruction and response at a given index.

#         Note: In a full pipeline, you would tokenize the text here or in a
#         data collator to prepare it for the model. This example returns
#         the raw text for clarity.
#         """
#         return {
#             "instruction": self.instructions[idx],
#             "response": self.responses[idx]
#         }




def create_chatml_dataset(data_dir: str, dataset_name: str) -> DatasetDict:
    
    # 1. Validation Logic: Ensure it looks like a valid conversation
    def is_valid_conversation(example):
        msgs = example['messages']
        # Must be a list, have at least 2 turns
        if not isinstance(msgs, list) or len(msgs) < 2:
            return False
        # ChatML expects specific roles: user/assistant/system
        return (msgs[0]['role'] == 'user' and msgs[1]['role'] == 'assistant')

    ds_splits = {}

    splits = os.listdir(Path(data_dir) / dataset_name)
    print(splits)
    for split in splits:
        # Load raw data
        split_path = Path(data_dir) / dataset_name / split
        raw_ds = load_dataset("parquet", data_files=str(split_path / "*.parquet"), split="train")

        # 2. Filter but KEEP the 'messages' column
        processed_ds = raw_ds.filter(is_valid_conversation)
        
        
        ds_splits[split] = processed_ds

    return DatasetDict(ds_splits)


def create_image_classification_dataset(
    data_dir: str, 
    dataset_name: str, 
    transform: Optional[Callable] = None
) -> DatasetDict:
    """
    Creates a Hugging Face DatasetDict for image classification.
    
    This function reads a 'metadata.parquet' file, resolves absolute image paths,
    casts the image column to the native Hugging Face Image feature (lazy loading),
    and groups the data by the 'split' column.

    Args:
        data_dir (str): The root directory where datasets are stored.
        dataset_name (str): The specific name of the dataset folder.
        transform (callable, optional): A function/transform that takes in a PIL image
            and returns a transformed version (e.g., torchvision transforms).
            If provided, it is applied via set_transform.

    Returns:
        DatasetDict: A dictionary containing the splits (e.g., 'train', 'test').
                     Accessing an item returns {'image': PIL.Image, 'label': int, ...}
                     or transformed tensors if a transform is provided.
    """
    root_dir = Path(data_dir) / dataset_name
    metadata_path = root_dir / "structure.parquet"

    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found at {metadata_path}")

    # 1. Load the metadata
    # We load as 'train' initially because load_dataset returns a DatasetDict 
    # with a default key when loading a single file.
    raw_dataset = load_dataset("parquet", data_files=str(metadata_path), split="train")

    # 2. Convert relative paths to absolute paths
    # We create a new column 'image' which contains the full path string
    def add_absolute_path(example):
        return {"image": str(root_dir / example["file_path"])}

    dataset_with_paths = raw_dataset.map(add_absolute_path)

    # 3. Cast the 'image' column to the native Image feature
    # This tells HF to load the file as a PIL Image when accessed
    features = dataset_with_paths.features.copy()
    features["image"] = datasets_image()
    dataset_with_images = dataset_with_paths.cast(features)

    # 4. Separate into a DatasetDict based on the 'split' column
    # We identify unique splits in the metadata
    unique_splits = set(dataset_with_images["split"])
    
    ds_splits = {}
    for split_name in unique_splits:
        # Filter the dataset for this specific split
        ds_splits[split_name] = dataset_with_images.filter(lambda x: x["split"] == split_name)
        
        # Cleanup: Remove columns that are likely no longer needed for training
        # (Keeping 'label' and 'image', removing 'file_path' and 'split' to clean up)
        ds_splits[split_name] = ds_splits[split_name].remove_columns(["file_path", "split"])

    final_dataset_dict = DatasetDict(ds_splits)

    # 5. Apply transforms if provided
    if transform:
        def apply_transform(batch):
            # HF transforms expect a batch dict: {'image': [img1, img2], 'label': [0, 1]}
            # We apply the transform to every image in the batch
            batch["pixel_values"] = [transform(img.convert("RGB")) for img in batch["image"]]
            return batch

        # set_transform is "lazy" - it runs on-the-fly when data is accessed
        final_dataset_dict.set_transform(apply_transform)

    return final_dataset_dict

# # #print sample image from the dataset
# if __name__ == "__main__":
#     dataset = ImageClassificationDataset(data_dir="downloaded_datasett",dataset_name="microsoft-cats_vs_dogs",split="train")
#     import matplotlib.pyplot as plt

#     image, label = dataset[100]
    
#     #save image
#     plt.imshow(image)
#     plt.title(f"Label: {label}")
#     plt.savefig("sample_image.png")
#     plt.show()

#     text_dataset = TextGenerationDataset(data_dir="/home/mlops/abolfazl/tools/data_platform/ryn/data/data_restructure/text_generation_test_output", dataset_name="restructured_text_dataset", split="validation")

#     sample = text_dataset[10]
#     print("Instruction:", sample["instruction"])
#     print("Response:", sample["response"])

