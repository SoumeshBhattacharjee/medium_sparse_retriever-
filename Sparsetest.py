import unittest
from sparse_matrix import generate_sparse_matrix

class TestGenerateSparseMatrix(unittest.TestCase):
    def test_valid_parameters(self):
        # Test with valid parameters
        num_products = 100
        num_pincodes = 30
        min_pincodes_per_product = 3
        max_pincodes_per_product = 25
        chunk_size = 10

        # Test the function
        generated_matrix = generate_sparse_matrix(num_products, num_pincodes, min_pincodes_per_product, max_pincodes_per_product, chunk_size)

        self.assertIsNotNone(generated_matrix)
        self.assertEqual(generated_matrix.shape, (num_products, num_pincodes))

    def test_large_input(self):
        # Test with large input parameters
        num_products = 100000
        num_pincodes = 10000
        min_pincodes_per_product = 3
        max_pincodes_per_product = 9999
        chunk_size = 1000

        sparse_matrix = generate_sparse_matrix(num_products, num_pincodes, min_pincodes_per_product, max_pincodes_per_product, chunk_size)

        self.assertIsNotNone(sparse_matrix)
        self.assertEqual(sparse_matrix.shape, (num_products, num_pincodes))

    def test_edge_cases(self):
        # Test with edge cases (e.g., smallest and largest possible values)
        num_products = 1
        num_pincodes = 1
        min_pincodes_per_product = 1
        max_pincodes_per_product = 1
        chunk_size = 1

        sparse_matrix = generate_sparse_matrix(num_products, num_pincodes, min_pincodes_per_product, max_pincodes_per_product, chunk_size)

        self.assertIsNotNone(sparse_matrix)
        self.assertEqual(sparse_matrix.shape, (num_products, num_pincodes))
   
    def test_random_parameters(self):
        # Test with random parameters
        num_products = 100
        num_pincodes = 50
        min_pincodes_per_product = 1
        max_pincodes_per_product = 10
        chunk_size = 50

        sparse_matrix = generate_sparse_matrix(num_products, num_pincodes, min_pincodes_per_product, max_pincodes_per_product, chunk_size)

        self.assertIsNotNone(sparse_matrix)
        self.assertEqual(sparse_matrix.shape, (num_products, num_pincodes))

    def test_min_max_values(self):
        # Test with minimum and maximum values
        num_products = 1
        num_pincodes = 1
        min_pincodes_per_product = 1
        max_pincodes_per_product = 1
        chunk_size = 1

        sparse_matrix = generate_sparse_matrix(num_products, num_pincodes, min_pincodes_per_product, max_pincodes_per_product, chunk_size)

        self.assertIsNotNone(sparse_matrix)
        self.assertEqual(sparse_matrix.shape, (num_products, num_pincodes))


    def test_max_chunk_size(self):
        # Test with maximum chunk size
        num_products = 100
        num_pincodes = 50
        min_pincodes_per_product = 1
        max_pincodes_per_product = 10
        chunk_size = 1000000

        sparse_matrix = generate_sparse_matrix(num_products, num_pincodes, min_pincodes_per_product, max_pincodes_per_product, chunk_size)

        self.assertIsNotNone(sparse_matrix)
        self.assertEqual(sparse_matrix.shape, (num_products, num_pincodes))

if __name__ == '__main__':
    unittest.main()
