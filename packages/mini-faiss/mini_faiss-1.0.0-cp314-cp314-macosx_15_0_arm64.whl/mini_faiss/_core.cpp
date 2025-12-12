#include "_index.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <stdexcept>
#include <cstring>
#include <vector>

namespace py = pybind11;
using namespace mini_faiss;

// ============================================================================
// IndexFlatL2 Implementation
// ============================================================================

IndexFlatL2::IndexFlatL2(int d) : BaseIndex(d) {}

void IndexFlatL2::add(const float* xb, size_t n) {
    if (xb == nullptr) {
        throw std::invalid_argument("Input pointer cannot be null");
    }
    data_.insert(data_.end(), xb, xb + n * d_);
    ntotal_ += n;
}

void IndexFlatL2::compute_distances_l2(const float* queries, size_t nq, int k,
                                       float* distances, int64_t* indices) const {
    if (ntotal_ == 0) {
        throw std::runtime_error("Index is empty; cannot search");
    }

    // Allocate temporary distance matrix
    std::vector<float> dist_matrix(nq * ntotal_);

    // Compute all distances
    l2_distance_batch(queries, data_.data(), nq, ntotal_, d_, dist_matrix.data());

    // Select top-k
    select_topk_min(dist_matrix.data(), nq, ntotal_, k, distances, indices);
}

void IndexFlatL2::search(const float* xq, size_t nq, int k,
                        float* distances, int64_t* indices) const {
    if (k <= 0) {
        throw std::invalid_argument("k must be positive");
    }
    if ((int)ntotal_ < k) {
        throw std::invalid_argument("k cannot exceed number of indexed vectors");
    }
    compute_distances_l2(xq, nq, k, distances, indices);
}

// ============================================================================
// IndexFlatIP Implementation
// ============================================================================

IndexFlatIP::IndexFlatIP(int d) : BaseIndex(d) {}

void IndexFlatIP::add(const float* xb, size_t n) {
    if (xb == nullptr) {
        throw std::invalid_argument("Input pointer cannot be null");
    }
    data_.insert(data_.end(), xb, xb + n * d_);
    ntotal_ += n;
}

void IndexFlatIP::compute_distances_ip(const float* queries, size_t nq, int k,
                                       float* distances, int64_t* indices) const {
    if (ntotal_ == 0) {
        throw std::runtime_error("Index is empty; cannot search");
    }

    // Allocate temporary distance matrix
    std::vector<float> dist_matrix(nq * ntotal_);

    // Compute all distances
    inner_product_batch(queries, data_.data(), nq, ntotal_, d_, dist_matrix.data());

    // Select top-k (max for inner product)
    select_topk_max(dist_matrix.data(), nq, ntotal_, k, distances, indices);
}

void IndexFlatIP::search(const float* xq, size_t nq, int k,
                        float* distances, int64_t* indices) const {
    if (k <= 0) {
        throw std::invalid_argument("k must be positive");
    }
    if ((int)ntotal_ < k) {
        throw std::invalid_argument("k cannot exceed number of indexed vectors");
    }
    compute_distances_ip(xq, nq, k, distances, indices);
}

// ============================================================================
// pybind11 Bindings
// ============================================================================

PYBIND11_MODULE(_core, m) {
    m.doc() = "Mini-FAISS C++ core module for vector similarity search";

    // IndexFlatL2 Python binding
    py::class_<IndexFlatL2>(m, "IndexFlatL2")
        .def(py::init<int>(), py::arg("d"),
             "Initialize IndexFlatL2 with vector dimension d")
        .def("add", [](IndexFlatL2& self, py::array_t<float> xb) {
            // Validate input
            if (xb.ndim() != 2) {
                throw std::invalid_argument("Input must be 2D array");
            }
            if (xb.shape(1) != self.dimension()) {
                throw std::invalid_argument(
                    "Vector dimension mismatch: expected " +
                    std::to_string(self.dimension()) + ", got " +
                    std::to_string(xb.shape(1)));
            }

            auto buf = xb.request();
            self.add(static_cast<const float*>(buf.ptr), xb.shape(0));
        }, py::arg("xb"), "Add vectors to index")

        .def("search", [](IndexFlatL2& self, py::array_t<float> xq, int k) {
            // Validate input
            if (xq.ndim() != 2) {
                throw std::invalid_argument("Query array must be 2D");
            }
            if (xq.shape(1) != self.dimension()) {
                throw std::invalid_argument(
                    "Query dimension mismatch: expected " +
                    std::to_string(self.dimension()) + ", got " +
                    std::to_string(xq.shape(1)));
            }

            auto nq = xq.shape(0);
            auto buf = xq.request();

            // Allocate output arrays
            std::vector<float> distances_vec(nq * k);
            std::vector<int64_t> indices_vec(nq * k);

            // Perform search
            self.search(static_cast<const float*>(buf.ptr), nq, k,
                       distances_vec.data(), indices_vec.data());

            // Convert to NumPy arrays
            py::array_t<float> distances(std::vector<ssize_t>{nq, k});
            py::array_t<int64_t> indices(std::vector<ssize_t>{nq, k});

            auto dist_buf = distances.request();
            auto idx_buf = indices.request();

            std::memcpy(dist_buf.ptr, distances_vec.data(), distances_vec.size() * sizeof(float));
            std::memcpy(idx_buf.ptr, indices_vec.data(), indices_vec.size() * sizeof(int64_t));

            return py::make_tuple(distances, indices);
        }, py::arg("xq"), py::arg("k"), "Search for top-k nearest neighbors")

        .def("ntotal", &IndexFlatL2::ntotal, "Get total number of indexed vectors")
        .def("dimension", &IndexFlatL2::dimension, "Get vector dimension");

    // IndexFlatIP Python binding
    py::class_<IndexFlatIP>(m, "IndexFlatIP")
        .def(py::init<int>(), py::arg("d"),
             "Initialize IndexFlatIP with vector dimension d")
        .def("add", [](IndexFlatIP& self, py::array_t<float> xb) {
            // Validate input
            if (xb.ndim() != 2) {
                throw std::invalid_argument("Input must be 2D array");
            }
            if (xb.shape(1) != self.dimension()) {
                throw std::invalid_argument(
                    "Vector dimension mismatch: expected " +
                    std::to_string(self.dimension()) + ", got " +
                    std::to_string(xb.shape(1)));
            }

            auto buf = xb.request();
            self.add(static_cast<const float*>(buf.ptr), xb.shape(0));
        }, py::arg("xb"), "Add vectors to index")

        .def("search", [](IndexFlatIP& self, py::array_t<float> xq, int k) {
            // Validate input
            if (xq.ndim() != 2) {
                throw std::invalid_argument("Query array must be 2D");
            }
            if (xq.shape(1) != self.dimension()) {
                throw std::invalid_argument(
                    "Query dimension mismatch: expected " +
                    std::to_string(self.dimension()) + ", got " +
                    std::to_string(xq.shape(1)));
            }

            auto nq = xq.shape(0);
            auto buf = xq.request();

            // Allocate output arrays
            std::vector<float> distances_vec(nq * k);
            std::vector<int64_t> indices_vec(nq * k);

            // Perform search
            self.search(static_cast<const float*>(buf.ptr), nq, k,
                       distances_vec.data(), indices_vec.data());

            // Convert to NumPy arrays
            py::array_t<float> distances(std::vector<ssize_t>{nq, k});
            py::array_t<int64_t> indices(std::vector<ssize_t>{nq, k});

            auto dist_buf = distances.request();
            auto idx_buf = indices.request();

            std::memcpy(dist_buf.ptr, distances_vec.data(), distances_vec.size() * sizeof(float));
            std::memcpy(idx_buf.ptr, indices_vec.data(), indices_vec.size() * sizeof(int64_t));

            return py::make_tuple(distances, indices);
        }, py::arg("xq"), py::arg("k"), "Search for top-k nearest neighbors")

        .def("ntotal", &IndexFlatIP::ntotal, "Get total number of indexed vectors")
        .def("dimension", &IndexFlatIP::dimension, "Get vector dimension");
}
