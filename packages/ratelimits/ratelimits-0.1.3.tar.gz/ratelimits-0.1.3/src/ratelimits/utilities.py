
# break list into smaller chunks of len size 
def batch_generator(l_items, size):
  """sublist of elements from list l_items split in batch of length size

  Args:
      l_items (list): list of elements to be split
      size (int): output length of the batch

  Yields:
      list: sublist of elements from list l_items split in batch of length size
  """
  for i in range(0, len(l_items), size):
    yield l_items[i:i+size]
    
# batch_generator = lambda l, batch_size: (l[i:i+batch_size] for i in range(0, len(l), batch_size))