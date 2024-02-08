import numpy as np
from scipy.sparse import csr_matrix, save_npz
from tqdm import tqdm
import time
import threading

def generate_sparse_matrix(num_products, num_pincodes, min_pincodes_per_product, max_pincodes_per_product, chunk_size=1000, max_concurrent_tasks=10):
    rows = []
    cols = []
    data = []

    start_time = time.time()  # Record start time
    progress_bar = tqdm(total=num_products, desc="Generating")  # Initialize tqdm progress bar
    semaphore = threading.Semaphore(max_concurrent_tasks)  # Semaphore to control concurrent tasks
    
    def generate_chunk(chunk_start):
        for product_id in range(chunk_start, min(chunk_start + chunk_size, num_products)):
            semaphore.acquire()  # Acquire semaphore
            num_pincodes_for_product = np.random.randint(min_pincodes_per_product, max_pincodes_per_product + 1)
            selected_pincodes = np.random.choice(num_pincodes, num_pincodes_for_product, replace=False)

            # Set values
            for pincode in selected_pincodes:
                rows.append(product_id)
                cols.append(pincode)
                data.append(True)

            semaphore.release()  # Release semaphore

            # Update tqdm progress bar
            progress_bar.update(1)
    
    threads = []
    for chunk_start in range(0, num_products, chunk_size):
        thread = threading.Thread(target=generate_chunk, args=(chunk_start,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    progress_bar.close()
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print("\nTime taken to generate sparse matrix:", elapsed_time, "seconds")

    # Convert lists to NumPy arrays
    rows = np.array(rows)
    cols = np.array(cols)
    data = np.array(data)

    # Create CSR matrix
    sparse_matrix = csr_matrix((data, (rows, cols)), shape=(num_products, num_pincodes))

    # Save sparse matrix to file
    save_npz("sparse_matrix.npz", sparse_matrix)

    return sparse_matrix

# Parameters
num_products = 1000000
num_pincodes = 1000
min_pincodes_per_product = 3
max_pincodes_per_product = 9999
chunk_size = 1000
max_concurrent_tasks = 10  # Adjust as needed

# Generate sparse matrix
sparse_matrix = generate_sparse_matrix(num_products, num_pincodes, min_pincodes_per_product, max_pincodes_per_product, chunk_size, max_concurrent_tasks)

print("Sparse matrix generated successfully and saved to 'sparse_matrix.npz'.")
print("Shape of the sparse matrix:", sparse_matrix.shape)
