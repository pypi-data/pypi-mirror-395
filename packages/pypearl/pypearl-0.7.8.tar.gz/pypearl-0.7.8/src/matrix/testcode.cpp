// test_dot_robust.cpp
#include "matrix.hpp"
#include <iostream>
#include <stdexcept>

int main() {
    bool all_ok = true;

    // ——————————————————————————————————
    // 1) Vector·Vector → scalar (correct)
    try {
        std::size_t len = 3;
        std::size_t shape1[1] = { len };
        Array<int,1> v1(shape1), v2(shape1);

        // v1 = [1,2,3], v2 = [4,5,6]
        for (std::size_t i = 0; i < len; ++i) {
            v1[i] = int(i + 1);
            v2[i] = int(i + 4);
        }

        // expected = 1*4 + 2*5 + 3*6 = 32
        int expect = 1*4 + 2*5 + 3*6;
        int dot = v1 * v2;
        if (dot != expect) {
            std::cerr << "[v·v correct] got " << dot
                      << ", want " << expect << "\n";
            all_ok = false;
        } else {
            std::cout << "✅ v·v (correct) passed\n";
        }
    } catch (...) {
        std::cerr << "[v·v correct] threw unexpected exception\n";
        all_ok = false;
    }

    // 1b) Vector·Vector → scalar (length mismatch → exception)
    try {
        std::size_t shapeA[1] = { 3 };
        std::size_t shapeB[1] = { 4 };
        Array<int,1> a(shapeA), b(shapeB);
        (void)(a * b);
        std::cerr << "[v·v mismatch] no exception thrown\n";
        all_ok = false;
    } catch (const std::length_error&) {
        std::cout << "✅ v·v (mismatch) threw length_error\n";
    } catch (...) {
        std::cerr << "[v·v mismatch] threw wrong exception type\n";
        all_ok = false;
    }

    // ——————————————————————————————————
    // 2) Matrix×Vector → column-matrix (correct)
    try {
        std::size_t rows = 2, cols = 3;
        std::size_t shapeM[2] = { rows, cols };
        Array<int,2> M(shapeM);

        // M = [ [1, 2, 3],
        //       [4, 5, 6] ]
        for (std::size_t i = 0; i < rows; ++i)
            for (std::size_t j = 0; j < cols; ++j)
                M[i][j] = int(i*cols + j + 1);

        std::size_t shapeV[1] = { cols };
        Array<int,1> v(shapeV);
        v[0] =  7; v[1] =  8; v[2] =  9;

        // expected column = [1*7+2*8+3*9; 4*7+5*8+6*9] = [50; 122]
        Array<int,2> mv = M * v;
        int exp0 = 1*7 + 2*8 + 3*9;   // 50
        int exp1 = 4*7 + 5*8 + 6*9;  // 122

        if (mv[0][0] != exp0 || mv[1][0] != exp1) {
            std::cerr << "[M×v correct] got [" 
                      << mv[0][0] << "; " << mv[1][0]
                      << "], want [" << exp0 << "; " << exp1 << "]\n";
            all_ok = false;
        } else {
            std::cout << "✅ M×v (correct) passed\n";
        }
    } catch (...) {
        std::cerr << "[M×v correct] threw unexpected exception\n";
        all_ok = false;
    }

    // 2b) Matrix×Vector → exception (inner dim mismatch)
    try {
        std::size_t shapeM[2] = { 3, 2 };
        Array<int,2> M(shapeM);
        std::size_t shapeV[1] = { 3 };        // mismatch: M.cols=2, v.len=3
        Array<int,1> v(shapeV);
        (void)(M * v);
        std::cerr << "[M×v mismatch] no exception thrown\n";
        all_ok = false;
    } catch (const std::length_error&) {
        std::cout << "✅ M×v (mismatch) threw length_error\n";
    } catch (...) {
        std::cerr << "[M×v mismatch] threw wrong exception type\n";
        all_ok = false;
    }

    // ——————————————————————————————————
    // 3) Matrix×Matrix → matrix (correct, non-square → non-square result)
    try {
        // A: 2×3, B: 3×4 → C: 2×4
        std::size_t shapeA[2] = { 2, 3 };
        std::size_t shapeB[2] = { 3, 4 };
        Array<int,2> A(shapeA), B(shapeB);

        // fill A row-major: [ [1,2,3], [4,5,6] ]
        for (std::size_t i = 0; i < 2; ++i)
            for (std::size_t j = 0; j < 3; ++j)
                A[i][j] = int(i*3 + j + 1);

        // fill B row-major: 
        // [ [ 1,  2,  3,  4],
        //   [ 5,  6,  7,  8],
        //   [ 9, 10, 11, 12] ]
        for (std::size_t i = 0; i < 3; ++i)
            for (std::size_t j = 0; j < 4; ++j)
                B[i][j] = int(i*4 + j + 1);

        Array<int,2> C = A * B;  // should be 2×4

        // compute & check all 8 entries
        for (std::size_t i = 0; i < 2; ++i) {
            for (std::size_t j = 0; j < 4; ++j) {
                int expected = 0;
                for (std::size_t k = 0; k < 3; ++k)
                    expected += A[i][k] * B[k][j];
                if (C[i][j] != expected) {
                    std::cerr << "[A×B correct] mismatch at ["<<i<<"]["<<j<<"] = "
                              << C[i][j] << ", want " << expected << "\n";
                    all_ok = false;
                }
            }
        }
        std::cout << "✅ A×B (non-square→non-square) passed\n";
    } catch (...) {
        std::cerr << "[A×B non-square] threw unexpected exception\n";
        all_ok = false;
    }

    // 3b) Matrix×Matrix → exception (inner dim mismatch)
    try {
        std::size_t shapeA[2] = { 2, 2 };
        std::size_t shapeB[2] = { 3, 2 };
        Array<int,2> A(shapeA), B(shapeB);
        (void)(A * B);
        std::cerr << "[A×B mismatch] no exception thrown\n";
        all_ok = false;
    } catch (const std::length_error&) {
        std::cout << "✅ A×B (mismatch) threw length_error\n";
    } catch (...) {
        std::cerr << "[A×B mismatch] threw wrong exception type\n";
        all_ok = false;
    }

    std::cout << (all_ok
        ? "🎉 All dot-product shape & content tests passed!\n"
        : "❌ Some dot-product tests failed.\n");
    return all_ok ? 0 : 1;
}
