// unfused_softmax_cce_tests.cpp
#include <cmath>
#include <cstdio>
#include <cassert>
#include <random>
#include <algorithm>
#include "neuralnetwork.hpp"
#include "./activation/arbitraryactivation.hpp"
#include "./loss/arbitraryloss.hpp"
#include "../utilities/utilities.hpp"

// ===== Reference implementations =====

// Softmax forward (numerically stable)
static void softmax_forward_ref(const double* x, double* y, size_t n) {
    double max_x = x[0];
    for (size_t i = 1; i < n; i++) {
        if (x[i] > max_x) max_x = x[i];
    }
    
    double sum = 0.0;
    for (size_t i = 0; i < n; i++) {
        y[i] = std::exp(x[i] - max_x);
        sum += y[i];
    }
    
    for (size_t i = 0; i < n; i++) {
        y[i] /= sum;
    }
}

// CCE Loss forward: L = -sum(y_true * log(y_pred))
// For one-hot encoded labels: L = -log(y_pred[true_class])
static double cce_forward_ref(const double* y_pred, int true_class, size_t n) {
    // Clamp to avoid log(0)
    const double epsilon = 1e-15;
    double y_clipped = std::max(epsilon, std::min(1.0 - epsilon, y_pred[true_class]));
    return -std::log(y_clipped);
}

// CCE backward (unfused): dL/dy_pred = -y_true / y_pred
// For one-hot: gradient is -1/y_pred[true_class] at true class, 0 elsewhere
static void cce_backward_ref(const double* y_pred, int true_class, double* grad, size_t n) {
    const double epsilon = 1e-15;
    for (size_t i = 0; i < n; i++) {
        if (i == (size_t)true_class) {
            double y_clipped = std::max(epsilon, std::min(1.0 - epsilon, y_pred[i]));
            grad[i] = -1.0 / y_clipped;
        } else {
            grad[i] = 0.0;
        }
    }
}

// Softmax backward: dL/dx_i = y_i * (dL/dy_i - sum_j(y_j * dL/dy_j))
static void softmax_backward_ref(const double* y, const double* dL_dy, double* dL_dx, size_t n) {
    double dot = 0.0;
    for (size_t i = 0; i < n; i++) {
        dot += y[i] * dL_dy[i];
    }
    
    for (size_t i = 0; i < n; i++) {
        dL_dx[i] = y[i] * (dL_dy[i] - dot);
    }
}

// Combined: softmax + CCE backward (for verification)
// Known result: dL/dx = y_pred - y_true (when fused)
static void softmax_cce_backward_ref(const double* y_pred, int true_class, double* grad, size_t n) {
    for (size_t i = 0; i < n; i++) {
        if (i == (size_t)true_class) {
            grad[i] = y_pred[i] - 1.0;
        } else {
            grad[i] = y_pred[i];
        }
    }
}

static inline bool almost_equal(double u, double v, double tol = 1e-7) {
    return std::abs(u - v) <= tol;
}

static inline bool almost_equal_rel(double u, double v, double rel_tol = 1e-6, double abs_tol = 1e-10) {
    const double diff = std::abs(u - v);
    const double max_val = std::max(std::abs(u), std::abs(v));
    return diff <= abs_tol || diff <= rel_tol * max_val;
}

static void cleanup_activation(ActivationLayer<double>& L) {
    if (L.outputs)      { delete L.outputs;      L.outputs = nullptr; }
    if (L.saved_inputs) { delete L.saved_inputs; L.saved_inputs = nullptr; }
    if (L.dinputs)      { delete L.dinputs;      L.dinputs = nullptr; }
}

// ===================== Test 1: CCE Loss Only (with pre-computed softmax) =====================
void test_cce_only() {
    std::printf("\n=== Test 1: CCE Loss Only ===\n");
    
    const size_t batch_size = 4, num_classes = 5;
    size_t shape[2] = {batch_size, num_classes};
    
    // Pre-computed softmax probabilities (manually set to valid probabilities)
    Array<double, 2> y_pred(shape);
    const double probs[4][5] = {
        {0.1, 0.2, 0.5, 0.15, 0.05},  // true class: 2
        {0.7, 0.1, 0.1, 0.05, 0.05},  // true class: 0
        {0.05, 0.05, 0.1, 0.7, 0.1},  // true class: 3
        {0.2, 0.2, 0.2, 0.2, 0.2}     // true class: 1 (uniform)
    };
    
    for (size_t i = 0; i < batch_size; i++) {
        for (size_t j = 0; j < num_classes; j++) {
            y_pred[i][j] = probs[i][j];
        }
    }
    
    // True labels (class indices)
    Array<int, 1> y_true_arr(batch_size);
    int true_labels[4] = {2, 0, 3, 1};
    for (size_t i = 0; i < batch_size; i++) {
        y_true_arr[i] = true_labels[i];
    }
    
    // Create loss layer
    LossStruct<double> cce_loss = {
        0x0,        // type: CCE unfused
        nullptr,    // saved_inputs
        &y_true_arr,// y_true
        nullptr     // dinputs
    };
    
    // ---- Forward pass ----
    double loss = lossForward<double>(&y_pred, cce_loss, (void*)&y_true_arr);
    
    // Compute reference loss
    double loss_ref = 0.0;
    for (size_t i = 0; i < batch_size; i++) {
        double row_pred[num_classes];
        for (size_t j = 0; j < num_classes; j++) {
            row_pred[j] = y_pred[i][j];
        }
        loss_ref += cce_forward_ref(row_pred, true_labels[i], num_classes);
    }
    loss_ref /= batch_size;  // Average loss
    
    bool loss_ok = almost_equal(loss, loss_ref, 1e-6);
    std::printf("Loss: got=%.10f ref=%.10f %s\n", loss, loss_ref, loss_ok ? "OK" : "FAIL");
    
    // ---- Backward pass ----
    Array<double, 2>* dL_dy_pred = lossBackward<double>(&y_pred, cce_loss, (void*)&y_true_arr);
    assert(dL_dy_pred && "lossBackward returned nullptr");
    
    // Verify gradients
    bool grad_ok = true;
    for (size_t i = 0; i < batch_size; i++) {
        double row_pred[num_classes], row_grad_ref[num_classes];
        for (size_t j = 0; j < num_classes; j++) {
            row_pred[j] = y_pred[i][j];
        }
        
        cce_backward_ref(row_pred, true_labels[i], row_grad_ref, num_classes);
        
        for (size_t j = 0; j < num_classes; j++) {
            double got = (*dL_dy_pred)[i][j];
            double ref = row_grad_ref[j] / batch_size;  // Averaged gradient
            
            if (!almost_equal_rel(got, ref, 1e-5, 1e-9)) {
                std::printf("Gradient mismatch at (%zu,%zu): got=%.10f ref=%.10f\n", i, j, got, ref);
                grad_ok = false;
            }
        }
    }
    
    std::printf("CCE gradients: %s\n", grad_ok ? "OK" : "FAIL");
}

// ===================== Test 2: Softmax + CCE (Unfused) =====================
void test_softmax_cce_unfused() {
    std::printf("\n=== Test 2: Softmax + CCE (Unfused) ===\n");
    
    const size_t batch_size = 5, num_classes = 4;
    size_t shape[2] = {batch_size, num_classes};
    
    // Raw logits (input to softmax)
    Array<double, 2> logits(shape);
    const double logit_vals[5][4] = {
        {2.0, 1.0, 0.1, -1.0},
        {0.5, 0.5, 0.5, 0.5},
        {10.0, 5.0, 1.0, 0.0},
        {-2.0, -1.0, 0.0, 1.0},
        {1.5, 2.5, 3.5, 4.5}
    };
    
    for (size_t i = 0; i < batch_size; i++) {
        for (size_t j = 0; j < num_classes; j++) {
            logits[i][j] = logit_vals[i][j];
        }
    }
    
    // True labels
    Array<int, 1> y_true_arr(batch_size);
    int true_labels[5] = {0, 2, 0, 3, 3};
    for (size_t i = 0; i < batch_size; i++) {
        y_true_arr[i] = true_labels[i];
    }
    
    // Create activation layer
    ActivationLayer<double> softmax = {
        0x2, nullptr, nullptr, 0.0, nullptr, true, 0.0, 0.0
    };
    
    // Create loss layer
    LossStruct<double> cce_loss = {
        0x0, nullptr, &y_true_arr, nullptr
    };
    
    // ---- Forward: Logits -> Softmax -> CCE ----
    Array<double, 2>* probs = activationForward<double>(&logits, softmax);
    assert(probs && "Softmax forward failed");
    
    double loss = lossForward<double>(probs, cce_loss, (void*)&y_true_arr);
    
    // Compute reference
    double loss_ref = 0.0;
    for (size_t i = 0; i < batch_size; i++) {
        double row_logits[num_classes], row_probs[num_classes];
        for (size_t j = 0; j < num_classes; j++) {
            row_logits[j] = logits[i][j];
        }
        softmax_forward_ref(row_logits, row_probs, num_classes);
        loss_ref += cce_forward_ref(row_probs, true_labels[i], num_classes);
    }
    loss_ref /= batch_size;
    
    bool loss_ok = almost_equal(loss, loss_ref, 1e-6);
    std::printf("Loss: got=%.10f ref=%.10f %s\n", loss, loss_ref, loss_ok ? "OK" : "FAIL");
    
    // ---- Backward: CCE -> Softmax -> Logits ----
    Array<double, 2>* dL_dprobs = lossBackward<double>(probs, cce_loss, (void*)&y_true_arr);
    assert(dL_dprobs && "CCE backward failed");
    
    Array<double, 2>* dL_dlogits = activationBackward<double>(dL_dprobs, softmax);
    assert(dL_dlogits && "Softmax backward failed");
    
    // Verify end-to-end gradient (should match fused formula)
    bool grad_ok = true;
    for (size_t i = 0; i < batch_size; i++) {
        double row_probs[num_classes], row_grad_ref[num_classes];
        for (size_t j = 0; j < num_classes; j++) {
            row_probs[j] = (*probs)[i][j];
        }
        
        // The unfused chain should equal the fused result
        softmax_cce_backward_ref(row_probs, true_labels[i], row_grad_ref, num_classes);
        
        for (size_t j = 0; j < num_classes; j++) {
            double got = (*dL_dlogits)[i][j];
            double ref = row_grad_ref[j] / batch_size;
            
            if (!almost_equal_rel(got, ref, 1e-5, 1e-9)) {
                std::printf("End-to-end gradient mismatch at (%zu,%zu): got=%.10f ref=%.10f\n", i, j, got, ref);
                grad_ok = false;
            }
        }
    }
    
    std::printf("End-to-end gradients: %s\n", grad_ok ? "OK" : "FAIL");
    
    cleanup_activation(softmax);
}

// ===================== Test 3: Verify intermediate gradients =====================
void test_intermediate_gradients() {
    std::printf("\n=== Test 3: Intermediate Gradient Verification ===\n");
    
    const size_t batch_size = 3, num_classes = 3;
    size_t shape[2] = {batch_size, num_classes};
    
    Array<double, 2> logits(shape);
    const double logit_vals[3][3] = {
        {1.0, 2.0, 3.0},
        {0.0, 0.0, 0.0},
        {-1.0, 1.0, 2.0}
    };
    
    for (size_t i = 0; i < batch_size; i++) {
        for (size_t j = 0; j < num_classes; j++) {
            logits[i][j] = logit_vals[i][j];
        }
    }
    
    Array<int, 1> y_true_arr(batch_size);
    int true_labels[3] = {2, 1, 0};
    for (size_t i = 0; i < batch_size; i++) {
        y_true_arr[i] = true_labels[i];
    }
    
    ActivationLayer<double> softmax = {0x2, nullptr, nullptr, 0.0, nullptr, true, 0.0, 0.0};
    LossStruct<double> cce_loss = {0x0, nullptr, &y_true_arr, nullptr};
    
    // Forward
    Array<double, 2>* probs = activationForward<double>(&logits, softmax);
    (void)lossForward<double>(probs, cce_loss, (void*)&y_true_arr);
    
    // Backward step 1: CCE gradient
    Array<double, 2>* dL_dprobs = lossBackward<double>(probs, cce_loss, (void*)&y_true_arr);
    
    // Verify CCE gradients match reference
    bool cce_grad_ok = true;
    for (size_t i = 0; i < batch_size; i++) {
        double row_probs[num_classes], row_cce_grad_ref[num_classes];
        for (size_t j = 0; j < num_classes; j++) {
            row_probs[j] = (*probs)[i][j];
        }
        
        cce_backward_ref(row_probs, true_labels[i], row_cce_grad_ref, num_classes);
        
        for (size_t j = 0; j < num_classes; j++) {
            double got = (*dL_dprobs)[i][j];
            double ref = row_cce_grad_ref[j] / batch_size;
            
            if (!almost_equal_rel(got, ref, 1e-5, 1e-9)) {
                std::printf("CCE grad mismatch at (%zu,%zu): got=%.10f ref=%.10f\n", i, j, got, ref);
                cce_grad_ok = false;
            }
        }
    }
    std::printf("CCE intermediate gradients: %s\n", cce_grad_ok ? "OK" : "FAIL");
    
    // Backward step 2: Softmax gradient
    Array<double, 2>* dL_dlogits = activationBackward<double>(dL_dprobs, softmax);
    
    // Verify softmax gradients
    bool softmax_grad_ok = true;
    for (size_t i = 0; i < batch_size; i++) {
        double row_probs[num_classes], row_dL_dprobs[num_classes], row_softmax_grad_ref[num_classes];
        for (size_t j = 0; j < num_classes; j++) {
            row_probs[j] = (*probs)[i][j];
            row_dL_dprobs[j] = (*dL_dprobs)[i][j];
        }
        
        softmax_backward_ref(row_probs, row_dL_dprobs, row_softmax_grad_ref, num_classes);
        
        for (size_t j = 0; j < num_classes; j++) {
            double got = (*dL_dlogits)[i][j];
            double ref = row_softmax_grad_ref[j];
            
            if (!almost_equal_rel(got, ref, 1e-5, 1e-9)) {
                std::printf("Softmax grad mismatch at (%zu,%zu): got=%.10f ref=%.10f\n", i, j, got, ref);
                softmax_grad_ok = false;
            }
        }
    }
    std::printf("Softmax intermediate gradients: %s\n", softmax_grad_ok ? "OK" : "FAIL");
    
    cleanup_activation(softmax);
}

// ===================== Test 4: Edge cases =====================
void test_edge_cases() {
    std::printf("\n=== Test 4: Edge Cases ===\n");
    
    const size_t batch_size = 4, num_classes = 3;
    size_t shape[2] = {batch_size, num_classes};
    
    Array<double, 2> logits(shape);
    // Edge cases: very confident correct, very confident wrong, uniform, extreme values
    const double logit_vals[4][3] = {
        {100.0, 0.0, 0.0},      // Very confident, correct
        {0.0, 0.0, 100.0},      // Very confident, wrong
        {0.0, 0.0, 0.0},        // Uniform
        {-100.0, -100.0, 0.0}   // Extreme negative
    };
    
    for (size_t i = 0; i < batch_size; i++) {
        for (size_t j = 0; j < num_classes; j++) {
            logits[i][j] = logit_vals[i][j];
        }
    }
    
    Array<int, 1> y_true_arr(batch_size);
    int true_labels[4] = {0, 0, 1, 2};
    for (size_t i = 0; i < batch_size; i++) {
        y_true_arr[i] = true_labels[i];
    }
    
    ActivationLayer<double> softmax = {0x2, nullptr, nullptr, 0.0, nullptr, true, 0.0, 0.0};
    LossStruct<double> cce_loss = {0x0, nullptr, &y_true_arr, nullptr};
    
    Array<double, 2>* probs = activationForward<double>(&logits, softmax);
    double loss = lossForward<double>(probs, cce_loss, (void*)&y_true_arr);
    
    // Check for NaN or Inf
    bool valid = !std::isnan(loss) && !std::isinf(loss);
    std::printf("Loss stability (no NaN/Inf): %s (loss=%.10f)\n", valid ? "OK" : "FAIL", loss);
    
    Array<double, 2>* dL_dprobs = lossBackward<double>(probs, cce_loss, (void*)&y_true_arr);
    Array<double, 2>* dL_dlogits = activationBackward<double>(dL_dprobs, softmax);
    
    bool grad_valid = true;
    for (size_t i = 0; i < batch_size; i++) {
        for (size_t j = 0; j < num_classes; j++) {
            if (std::isnan((*dL_dlogits)[i][j]) || std::isinf((*dL_dlogits)[i][j])) {
                grad_valid = false;
                std::printf("Invalid gradient at (%zu,%zu): %.10f\n", i, j, (*dL_dlogits)[i][j]);
            }
        }
    }
    std::printf("Gradient stability (no NaN/Inf): %s\n", grad_valid ? "OK" : "FAIL");
    
    cleanup_activation(softmax);
}

int main() {
    test_cce_only();
    test_softmax_cce_unfused();
    test_intermediate_gradients();
    test_edge_cases();
    
    std::printf("\n=== All Tests Complete ===\n");
    return 0;
}

// sigmoid_forward_tests.cpp
/*#include <cmath>
#include <cstdio>
#include <cassert>
#include <random>
#include "neuralnetwork.hpp"
#include "./activation/arbitraryactivation.hpp"
#include "../utilities/utilities.hpp"


// Your headers:
#include "activation/arbitraryactivation.hpp"  // ActivationLayer, activationForward
#include "loss/arbitraryloss.hpp"

// ===== Reference helpers for Softmax =====
// Softmax: y_i = exp(x_i) / sum_j(exp(x_j))
// For numerical stability, subtract max before exp
static void softmax_forward_ref(const double* x, double* y, size_t n) {
    // Find max for numerical stability
    double max_x = x[0];
    for (size_t i = 1; i < n; i++) {
        if (x[i] > max_x) max_x = x[i];
    }
     
    // Compute exp(x - max) and sum
    double sum = 0.0;
    for (size_t i = 0; i < n; i++) {
        y[i] = std::exp(x[i] - max_x);
        sum += y[i];
    }
    
    // Normalize
    for (size_t i = 0; i < n; i++) {
        y[i] /= sum;
    }
}

// Softmax backward: dL/dx_i = y_i * (dL/dy_i - sum_j(y_j * dL/dy_j))
static void softmax_backward_ref(const double* y, const double* dY, double* dX, size_t n) {
    // Compute dot product: sum_j(y_j * dL/dy_j)
    double dot = 0.0;
    for (size_t i = 0; i < n; i++) {
        dot += y[i] * dY[i];
    }
    
    // Compute gradient
    for (size_t i = 0; i < n; i++) {
        dX[i] = y[i] * (dY[i] - dot);
    }
}

static inline bool almost_equal(double u, double v, double tol = 1e-12) {
    return std::abs(u - v) <= tol;
}

static void cleanup_activation(ActivationLayer<double>& L) {
    if (L.outputs)      { delete L.outputs;      L.outputs = nullptr; }
    if (L.saved_inputs) { delete L.saved_inputs; L.saved_inputs = nullptr; }
    if (L.dinputs)      { delete L.dinputs;      L.dinputs = nullptr; }
}

// ===================== Test 1: Small hand-crafted forward/backward =====================
void test_softmax_small() {
    ActivationLayer<double> softmax = {
        0x2,        // type: Softmax
        nullptr,    // saved_inputs
        nullptr,    // dinputs
        0.0,        // relmin (unused)
        nullptr,    // outputs
        true,       // outputOwnership
        0.0,        // alpha (unused)
        0.0         // beta (unused)
    };

    const size_t rows = 5, cols = 4;
    size_t s[2] = {rows, cols};
    Array<double,2> X(s), dY(s);

    // Test various scenarios: normal values, large values (numerical stability), zeros
    const double vals[rows][cols] = {
        {1.0,  2.0,  3.0,  4.0},      // ascending
        {0.0,  0.0,  0.0,  0.0},      // all zeros (uniform distribution)
        {-1.0, -2.0, -3.0, -4.0},     // negative values
        {10.0, 20.0, 30.0, 40.0},     // large values (test numerical stability)
        {1.5,  1.5,  1.5,  1.5}       // all equal (uniform distribution)
    };
    
    for (size_t i = 0; i < rows; i++)
        for (size_t j = 0; j < cols; j++)
            X[i][j] = vals[i][j];

    // Upstream gradient: non-uniform
    for (size_t i = 0; i < rows; i++)
        for (size_t j = 0; j < cols; j++)
            dY[i][j] = 0.5 + 0.1 * double(i) + 0.02 * double(j);

    // ---- Forward ----
    Array<double,2>* Y = activationForward<double>(&X, softmax);
    assert(Y && "activationForward(Softmax) returned nullptr");

    bool fwd_ok = true;
    double ref_y[cols];
    
    for (size_t i = 0; i < rows; i++) {
        // Extract row for reference computation
        double row_x[cols];
        for (size_t j = 0; j < cols; j++) {
            row_x[j] = X[i][j];
        }
        
        // Compute reference softmax for this row
        softmax_forward_ref(row_x, ref_y, cols);
        
        // Check outputs
        double sum = 0.0;
        for (size_t j = 0; j < cols; j++) {
            const double y = (*Y)[i][j];
            sum += y;
            
            if (!almost_equal(y, ref_y[j], 1e-12)) {
                std::printf("[Softmax fwd] MISMATCH at (%zu,%zu): y=%.17g ref=%.17g\n",
                            i, j, y, ref_y[j]);
                fwd_ok = false;
            }
            
            // Check that softmax outputs are in [0, 1]
            if (y < 0.0 || y > 1.0) {
                std::printf("[Softmax fwd] OUT OF RANGE at (%zu,%zu): y=%.17g\n", i, j, y);
                fwd_ok = false;
            }
        }
        
        // Check that row sums to 1.0
        if (!almost_equal(sum, 1.0, 1e-12)) {
            std::printf("[Softmax fwd] ROW SUM MISMATCH at row %zu: sum=%.17g (should be 1.0)\n", i, sum);
            fwd_ok = false;
        }
    }

    // ---- Backward ----
    Array<double,2>* dX_ptr = activationBackward<double>(&dY, softmax);
    Array<double,2>* dX = dX_ptr ? dX_ptr : softmax.dinputs;
    assert(dX && "activationBackward(Softmax) must return or set dinputs");

    bool bwd_ok = true;
    double ref_dx[cols];
    
    for (size_t i = 0; i < rows; i++) {
        // Extract row data
        double row_y[cols], row_dy[cols];
        for (size_t j = 0; j < cols; j++) {
            row_y[j] = (*Y)[i][j];
            row_dy[j] = dY[i][j];
        }
        
        // Compute reference gradient for this row
        softmax_backward_ref(row_y, row_dy, ref_dx, cols);
        
        // Check gradients
        for (size_t j = 0; j < cols; j++) {
            const double dx = (*dX)[i][j];
            if (!almost_equal(dx, ref_dx[j], 1e-11)) {
                std::printf("[Softmax bwd] dX MISMATCH at (%zu,%zu): dX=%.17g ref=%.17g\n",
                            i, j, dx, ref_dx[j]);
                bwd_ok = false;
            }
        }
    }

    std::printf("[Softmax small] forward=%s backward=%s\n",
                fwd_ok ? "OK" : "FAIL",
                bwd_ok ? "OK" : "FAIL");

    cleanup_activation(softmax);
}

// ===================== Test 2: Random forward/backward =====================
void test_softmax_random() {
    ActivationLayer<double> softmax = {0x2, nullptr, nullptr, 0.0, nullptr, true, 0.0, 0.0};

    const size_t rows = 100, cols = 8;
    size_t s[2] = {rows, cols};
    Array<double,2> X(s), dY(s);

    std::mt19937_64 rng(0xCAFEBABEULL);
    std::normal_distribution<double> dist_x(0.0, 5.0);
    std::uniform_real_distribution<double> dist_dy(0.1, 1.0);

    for (size_t i = 0; i < rows; i++) {
        for (size_t j = 0; j < cols; j++) {
            X[i][j] = dist_x(rng);
            dY[i][j] = dist_dy(rng);
        }
    }

    // Forward
    Array<double,2>* Y = activationForward<double>(&X, softmax);
    assert(Y);

    bool fwd_ok = true;
    double ref_y[cols];
    
    for (size_t i = 0; i < rows && fwd_ok; i++) {
        double row_x[cols];
        for (size_t j = 0; j < cols; j++) {
            row_x[j] = X[i][j];
        }
        
        softmax_forward_ref(row_x, ref_y, cols);
        
        double sum = 0.0;
        for (size_t j = 0; j < cols; j++) {
            const double y = (*Y)[i][j];
            sum += y;
            
            if (!almost_equal(y, ref_y[j], 1e-11)) {
                std::printf("[Softmax rand] fwd MISMATCH at (%zu,%zu): y=%.17g ref=%.17g\n",
                            i, j, y, ref_y[j]);
                fwd_ok = false;
                break;
            }
        }
        
        if (fwd_ok && !almost_equal(sum, 1.0, 1e-11)) {
            std::printf("[Softmax rand] ROW SUM at row %zu: sum=%.17g\n", i, sum);
            fwd_ok = false;
        }
    }

    // Backward
    Array<double,2>* dX_ptr = activationBackward<double>(&dY, softmax);
    Array<double,2>* dX = dX_ptr ? dX_ptr : softmax.dinputs;
    assert(dX);

    bool bwd_ok = true;
    double ref_dx[cols];
    
    for (size_t i = 0; i < rows && bwd_ok; i++) {
        double row_y[cols], row_dy[cols];
        for (size_t j = 0; j < cols; j++) {
            row_y[j] = (*Y)[i][j];
            row_dy[j] = dY[i][j];
        }
        
        softmax_backward_ref(row_y, row_dy, ref_dx, cols);
        
        for (size_t j = 0; j < cols; j++) {
            const double dx = (*dX)[i][j];
            if (!almost_equal(dx, ref_dx[j], 1e-10)) {
                std::printf("[Softmax rand] bwd MISMATCH at (%zu,%zu): dX=%.17g ref=%.17g\n",
                            i, j, dx, ref_dx[j]);
                bwd_ok = false;
                break;
            }
        }
    }

    std::printf("[Softmax random] forward=%s backward=%s\n",
                fwd_ok ? "OK" : "FAIL",
                bwd_ok ? "OK" : "FAIL");

    cleanup_activation(softmax);
}

// ===================== Test 3: Numerical stability with extreme values =====================
void test_softmax_extreme() {
    ActivationLayer<double> softmax = {0x2, nullptr, nullptr, 0.0, nullptr, true, 0.0, 0.0};

    const size_t rows = 4, cols = 3;
    size_t s[2] = {rows, cols};
    Array<double,2> X(s), dY(s);

    // Extreme test cases
    const double vals[rows][cols] = {
        {100.0, 200.0, 300.0},      // Very large values
        {-100.0, -200.0, -300.0},   // Very negative values
        {1e-10, 2e-10, 3e-10},      // Very small values
        {1000.0, 1000.1, 1000.0}    // Nearly equal large values
    };
    
    for (size_t i = 0; i < rows; i++)
        for (size_t j = 0; j < cols; j++)
            X[i][j] = vals[i][j];

    for (size_t i = 0; i < rows; i++)
        for (size_t j = 0; j < cols; j++)
            dY[i][j] = 1.0;

    Array<double,2>* Y = activationForward<double>(&X, softmax);
    assert(Y);

    bool ok = true;
    for (size_t i = 0; i < rows; i++) {
        double sum = 0.0;
        for (size_t j = 0; j < cols; j++) {
            const double y = (*Y)[i][j];
            
            // Check for NaN or Inf
            if (std::isnan(y) || std::isinf(y)) {
                std::printf("[Softmax extreme] NaN/Inf at (%zu,%zu): y=%.17g\n", i, j, y);
                ok = false;
            }
            
            // Check range [0, 1]
            if (y < 0.0 || y > 1.0) {
                std::printf("[Softmax extreme] OUT OF RANGE at (%zu,%zu): y=%.17g\n", i, j, y);
                ok = false;
            }
            
            sum += y;
        }
        
        if (!almost_equal(sum, 1.0, 1e-10)) {
            std::printf("[Softmax extreme] ROW SUM at row %zu: sum=%.17g\n", i, sum);
            ok = false;
        }
    }

    std::printf("[Softmax extreme values] %s\n", ok ? "OK" : "FAIL");

    cleanup_activation(softmax);
}

int main() {
    test_softmax_small();
    test_softmax_random();
    test_softmax_extreme();
    return 0;
}

/*
// ===== Reference helpers for PReLU with minimum hinge m =====
static inline double prelu_min_forward_ref(double x, double m, double a) {
    // Continuous hinge at m
    return (x > m) ? x : (m + a * (x - m));
}
static inline double prelu_min_dx_ref(double x, double m, double a) {
    // Tie rule: x == m uses positive branch (slope 1)
    return (x >= m) ? 1.0 : a;
}
static inline double prelu_min_da_contrib(double x, double m, double dY) {
    // ∂y/∂a = (x - m) for x <= m; tie at x==m contributes 0 either way
    return (x < m) ? dY * (x - m) : 0.0;
}
static inline bool almost_equal(double u, double v, double tol = 1e-12) {
    return std::abs(u - v) <= tol;
}
static void cleanup_activation(ActivationLayer<double>& L) {
    if (L.outputs)      { delete L.outputs;      L.outputs = nullptr; }
    if (L.saved_inputs) { delete L.saved_inputs; L.saved_inputs = nullptr; }
    if (L.dinputs)      { delete L.dinputs;      L.dinputs = nullptr; }
}

// ===================== Test 1: Small hand-crafted forward/backward =====================
void test_prelu_min_small() {
    const double a = 0.25;  // alpha (learnable)
    const double m = 2.0;   // relmin hinge
    ActivationLayer<double> prelu = {
        0x8,        // type: PReLU single-param
        nullptr,    // saved_inputs
        nullptr,    // dinputs
        m,          // relmin
        nullptr,    // outputs
        true,       // outputOwnership (not important here)
        a,          // alpha
        0.0         // beta (will hold dL/da)
    };

    const size_t rows = 6, cols = 4;
    size_t s[2] = {rows, cols};
    Array<double,2> X(s), dY(s);

    // Cover below m, at m, above m, near-m tiny values
    const double vals[rows][cols] = {
        {-3.0, -1.0,  0.0,  1.5},           // below m
        { 1.9,  1.99, 2.0,  2.01},          // around m
        { 2.5,  3.0,  10.0, 2.0000001},     // above m
        {-10., -0.1,  1.0,  2.0},           // mix, includes exactly m
        { 2.0,  0.5, -3.3,  100.0},         // includes at m, far below, far above
        { 1.999999, 2.0, 2.000001, 1.5}     // near the hinge
    };
    for (size_t i=0;i<rows;i++)
        for (size_t j=0;j<cols;j++)
            X[i][j] = vals[i][j];

    // Upstream gradient: non-uniform but deterministic
    for (size_t i=0;i<rows;i++)
        for (size_t j=0;j<cols;j++)
            dY[i][j] = 0.5 + 0.1*double(i) + 0.01*double(j);

    // ---- Forward ----
    Array<double,2>* Y = activationForward<double>(&X, prelu);
    assert(Y && "activationForward(PReLU:min) returned nullptr");

    bool fwd_ok = true;
    for (size_t i=0;i<rows;i++) {
        for (size_t j=0;j<cols;j++) {
            const double x  = X[i][j];
            const double y  = (*Y)[i][j];
            const double yr = prelu_min_forward_ref(x, m, a);
            if (!almost_equal(y, yr)) {
                std::printf("[PReLU:min fwd] MISMATCH at (%zu,%zu): y=%.17g ref=%.17g (x=%.17g, m=%.17g, a=%.3f)\n",
                            i, j, y, yr, x, m, a);
                fwd_ok = false;
            }
        }
    }

    // ---- Backward ----
    prelu.beta = 0.0;  // reset accumulator if your impl accumulates into beta
    Array<double,2>* dX_ptr = activationBackward<double>(&dY, prelu);
    Array<double,2>* dX = dX_ptr ? dX_ptr : prelu.dinputs;
    assert(dX && "activationBackward(PReLU:min) must return or set dinputs");

    bool bwd_ok = true;
    double beta_ref = 0.0;
    for (size_t i=0;i<rows;i++) {
        for (size_t j=0;j<cols;j++) {
            const double x    = X[i][j];
            const double grad = dY[i][j];
            const double dxr  = prelu_min_dx_ref(x, m, a) * grad;
            const double dx   = (*dX)[i][j];
            if (!almost_equal(dx, dxr)) {
                std::printf("[PReLU:min bwd] dX MISMATCH at (%zu,%zu): dX=%.17g ref=%.17g (x=%.17g, dY=%.17g, m=%.17g, a=%.3f)\n",
                            i, j, dx, dxr, x, grad, m, a);
                bwd_ok = false;
            }
            beta_ref += prelu_min_da_contrib(x, m, grad);
        }
    }

    bool beta_ok = almost_equal(prelu.beta, beta_ref, 1e-12);
    if (!beta_ok) {
        std::printf("[PReLU:min bwd] beta MISMATCH: beta=%.17g ref=%.17g\n", prelu.beta, beta_ref);
    }

    std::printf("[PReLU:min small] forward=%s backward=%s dL/da=%s\n",
                fwd_ok ? "OK" : "FAIL",
                bwd_ok ? "OK" : "FAIL",
                beta_ok ? "OK" : "FAIL");

    cleanup_activation(prelu);
}

// ===================== Test 2: Random forward/backward near the hinge =====================
void test_prelu_min_random() {
    const double a = 0.25;
    const double m = 2.0;
    ActivationLayer<double> prelu = {0x8, nullptr, nullptr, m, nullptr, true, a, 0.0};

    const size_t rows = 120, cols = 4;
    size_t s[2] = {rows, cols};
    Array<double,2> X(s), dY(s);

    std::mt19937_64 rng(0xBADA55ULL);
    std::normal_distribution<double> dist_x(m, 2.0);       // center at m to hit both sides
    std::uniform_real_distribution<double> dist_dy(0.1, 1.2);

    for (size_t i=0;i<rows;i++) {
        for (size_t j=0;j<cols;j++) {
            X[i][j]  = dist_x(rng);
            dY[i][j] = dist_dy(rng);
        }
    }

    (void)activationForward<double>(&X, prelu);

    prelu.beta = 0.0;
    Array<double,2>* dX_ptr = activationBackward<double>(&dY, prelu);
    Array<double,2>* dX = dX_ptr ? dX_ptr : prelu.dinputs;
    assert(dX);
 
    bool dx_ok = true;
    double beta_ref = 0.0;
    for (size_t i=0;i<rows && dx_ok;i++) {
        for (size_t j=0;j<cols;j++) {
            const double x = X[i][j];
            const double got = (*dX)[i][j];
            const double ref = prelu_min_dx_ref(x, m, a) * dY[i][j];
            if (!almost_equal(got, ref, 1e-12)) {
                std::printf("[PReLU:min rand] dX MISMATCH at (%zu,%zu): dX=%.17g ref=%.17g (x=%.17g, m=%.17g, a=%.3f)\n",
                            i, j, got, ref, x, m, a);
                dx_ok = false;
                break;
            }
            beta_ref += prelu_min_da_contrib(x, m, dY[i][j]);
        }
    }

    bool beta_ok = almost_equal(prelu.beta, beta_ref, 1e-10);
    if (!beta_ok) {
        std::printf("[PReLU:min rand] beta MISMATCH: beta=%.17g ref=%.17g\n", prelu.beta, beta_ref);
    }

    std::printf("[PReLU:min random] dX=%s dL/da=%s\n",
                dx_ok ? "OK" : "FAIL",
                beta_ok ? "OK" : "FAIL");

    cleanup_activation(prelu);
}
 
int main() {
    test_prelu_min_small();
    test_prelu_min_random();
    return 0;
}
*/