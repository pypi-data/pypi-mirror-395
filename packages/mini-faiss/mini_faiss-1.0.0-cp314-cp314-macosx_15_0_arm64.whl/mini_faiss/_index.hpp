#ifndef MINI_FAISS_INDEX_HPP
#define MINI_FAISS_INDEX_HPP

#include <vector>
#include <cstring>
#include <cmath>
#include <algorithm>
#include <queue>
#include <stdexcept>

namespace mini_faiss {

/// Distance metric type
enum class MetricType {
    L2,         // Squared Euclidean distance (minimize)
    INNER_PRODUCT  // Inner product (maximize, so we negate for consistent heap behavior)
};

/// Base index interface
class BaseIndex {
public:
    virtual ~BaseIndex() = default;

    int dimension() const { return d_; }
    size_t ntotal() const { return ntotal_; }

    virtual void add(const float* xb, size_t n) = 0;
    virtual void search(const float* xq, size_t nq, int k,
                       float* distances, int64_t* indices) const = 0;

protected:
    BaseIndex(int d) : d_(d), ntotal_(0) {}

    int d_;          // Vector dimension
    size_t ntotal_;  // Total number of vectors added
};

/// Flat index using L2 (squared Euclidean) distance
class IndexFlatL2 : public BaseIndex {
public:
    explicit IndexFlatL2(int d);

    void add(const float* xb, size_t n) override;
    void search(const float* xq, size_t nq, int k,
               float* distances, int64_t* indices) const override;

    const float* data() const { return data_.data(); }

private:
    std::vector<float> data_;  // Row-major layout: ntotal * d

    void compute_distances_l2(const float* queries, size_t nq, int k,
                             float* distances, int64_t* indices) const;
};

/// Flat index using inner product distance
class IndexFlatIP : public BaseIndex {
public:
    explicit IndexFlatIP(int d);

    void add(const float* xb, size_t n) override;
    void search(const float* xq, size_t nq, int k,
               float* distances, int64_t* indices) const override;

    const float* data() const { return data_.data(); }

private:
    std::vector<float> data_;  // Row-major layout: ntotal * d

    void compute_distances_ip(const float* queries, size_t nq, int k,
                             float* distances, int64_t* indices) const;
};

// ============================================================================
// Distance kernel implementations
// ============================================================================

/// Compute squared L2 distances from query batch to all database vectors
/// distances: output array of shape (nq, ntotal)
inline void l2_distance_batch(const float* queries, const float* db,
                             size_t nq, size_t nb, int d, float* distances) {
    // Precompute squared norms of database vectors
    std::vector<float> db_norms(nb, 0.0f);
    for (size_t i = 0; i < nb; ++i) {
        float norm = 0.0f;
        for (int j = 0; j < d; ++j) {
            float val = db[i * d + j];
            norm += val * val;
        }
        db_norms[i] = norm;
    }

    // Compute distances
    for (size_t i = 0; i < nq; ++i) {
        float q_norm = 0.0f;
        for (int j = 0; j < d; ++j) {
            float val = queries[i * d + j];
            q_norm += val * val;
        }

        for (size_t j = 0; j < nb; ++j) {
            float dot = 0.0f;
            for (int l = 0; l < d; ++l) {
                dot += queries[i * d + l] * db[j * d + l];
            }
            // L2^2 = ||q||^2 - 2*q·db + ||db||^2
            distances[i * nb + j] = q_norm - 2.0f * dot + db_norms[j];
        }
    }
}

/// Compute inner product from query batch to all database vectors
/// distances: output array of shape (nq, ntotal)
inline void inner_product_batch(const float* queries, const float* db,
                               size_t nq, size_t nb, int d, float* distances) {
    for (size_t i = 0; i < nq; ++i) {
        for (size_t j = 0; j < nb; ++j) {
            float dot = 0.0f;
            for (int l = 0; l < d; ++l) {
                dot += queries[i * d + l] * db[j * d + l];
            }
            distances[i * nb + j] = dot;
        }
    }
}

// ============================================================================
// Top-K selection
// ============================================================================

/// Select top-k smallest values (for L2, where smaller is better)
/// distances: flat array of nq*ntotal distances
/// ntotal: total number of database vectors
/// k: number of top results to keep
/// out_distances: output array of shape (nq, k)
/// out_indices: output array of shape (nq, k)
inline void select_topk_min(const float* distances, size_t nq, size_t ntotal, int k,
                           float* out_distances, int64_t* out_indices) {
    using MaxHeap = std::priority_queue<std::pair<float, int64_t>>;

    for (size_t i = 0; i < nq; ++i) {
        MaxHeap heap;  // max heap to track k smallest

        const float* row = distances + i * ntotal;

        // Add first k elements
        for (int j = 0; j < k && j < (int)ntotal; ++j) {
            heap.push({row[j], j});
        }

        // For remaining elements, maintain k smallest
        for (int j = k; j < (int)ntotal; ++j) {
            if (row[j] < heap.top().first) {
                heap.pop();
                heap.push({row[j], j});
            }
        }

        // Extract results (heap is max-heap, so order is reversed)
        std::vector<std::pair<float, int64_t>> results;
        while (!heap.empty()) {
            results.push_back(heap.top());
            heap.pop();
        }
        std::reverse(results.begin(), results.end());

        for (int j = 0; j < k; ++j) {
            out_distances[i * k + j] = results[j].first;
            out_indices[i * k + j] = results[j].second;
        }
    }
}

/// Select top-k largest values (for inner product, where larger is better)
/// distances: flat array of nq*ntotal distances
/// ntotal: total number of database vectors
/// k: number of top results to keep
/// out_distances: output array of shape (nq, k)
/// out_indices: output array of shape (nq, k)
inline void select_topk_max(const float* distances, size_t nq, size_t ntotal, int k,
                           float* out_distances, int64_t* out_indices) {
    using MinHeap = std::priority_queue<std::pair<float, int64_t>,
                                        std::vector<std::pair<float, int64_t>>,
                                        std::greater<std::pair<float, int64_t>>>;

    for (size_t i = 0; i < nq; ++i) {
        MinHeap heap;  // min heap to track k largest

        const float* row = distances + i * ntotal;

        // Add first k elements
        for (int j = 0; j < k && j < (int)ntotal; ++j) {
            heap.push({row[j], j});
        }

        // For remaining elements, maintain k largest
        for (int j = k; j < (int)ntotal; ++j) {
            if (row[j] > heap.top().first) {
                heap.pop();
                heap.push({row[j], j});
            }
        }

        // Extract results (min-heap gives largest first after reversing)
        std::vector<std::pair<float, int64_t>> results;
        while (!heap.empty()) {
            results.push_back(heap.top());
            heap.pop();
        }
        std::reverse(results.begin(), results.end());

        for (int j = 0; j < k; ++j) {
            out_distances[i * k + j] = results[j].first;
            out_indices[i * k + j] = results[j].second;
        }
    }
}

}  // namespace mini_faiss

#endif  // MINI_FAISS_INDEX_HPP
