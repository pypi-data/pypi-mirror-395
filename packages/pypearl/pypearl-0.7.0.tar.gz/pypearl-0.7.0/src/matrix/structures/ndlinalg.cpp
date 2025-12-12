#ifndef NDLINALG_C
#define NDLINALG_C

#ifdef __cplusplus
extern "C" {
#endif

#include "ndarray.hpp"

/*
 * Layout of the file:
 * - Helper inlines (when I put them in other files it caused duplicate symbol errors unless I unlined)
 * - Default GEMM (hardware nonspecialized)
 * - 
 * - 
 * 
 */

/*
 * SECTION 1: Inline Functions
 */

inline void fastGet1D4(ndarray* arr, size_t pos, void* loc){
    memcpy(loc, arr->data+pos, 4);
}

inline void fastGet1D8(ndarray* arr, size_t pos, void* loc){
    memcpy(loc, arr->data+pos, 8);
}

inline void fastGet1DX(ndarray* arr, size_t pos, void* loc, size_t byte_count){
    memcpy(loc, arr->data+pos, byte_count);
}

inline void fastSet1D4(ndarray* arr, size_t pos, void* val){
    memcpy(arr->data+pos, val, 4);
}

inline void fastSet1D8(ndarray* arr, size_t pos, void* val){
    memcpy(arr->data+pos, val, 8);
}

inline void fastSet1DX(ndarray* arr, size_t pos, void* val, size_t byte_count){
    memcpy(arr->data+pos, val, byte_count);
}

/*
 * SECTION 2: GEMM
 */

// A general GEMM. It's unoptimized but secure.
void GEMM(ndarray* A, ndarray* B, ndarray* C, ndarray* alpha, ndarray* beta){

    if(A->nd != 2 || B->nd != 2 || C->nd != 2){
        perror("Critical NDGEMM Error: A, B, C must be 2x2");
        exit(EXIT_FAILURE); 
        return;
    }
    if(B->dims[0] != A->dims[1]){
        perror("Critical NDGEMM Error: Inner dimensions of A, B must align");
        exit(EXIT_FAILURE); 
        return;
    }
    if(C->dims[0] != A->dims[0] || C->dims[1] != B->dims[1]){
        perror("Critical NDGEMM Error: C must be of shape(A.shape(0), B.shape(1))");
        exit(EXIT_FAILURE); 
        return;
    }   

    // determine if alpha and beta are used
    bool alpha_bypass = false;
    bool beta_bypass = false;
    if(!alpha){
        alpha_bypass = true;
    } 
    else if(alpha && alpha->nd != 0){
        perror("alpha must be a ndarray scalar, ignoring alpha");
        alpha_bypass = true;
    }

    if(!beta){
        beta_bypass= true;
    } 
    else if(beta && beta->nd != 0){
        perror("beta must be a ndarray scalar, ignoring beta");
        beta_bypass = true;
    }

    u_int8_t dtype = A->dtype;
    if(dtype != B->dtype || dtype != C->dtype || (!alpha_bypass && dtype != alpha->dtype) || (!beta_bypass && dtype != beta->dtype)){
        perror("Critical NDGEMM Error: Mixed precision is not allowed.");
        exit(EXIT_FAILURE); 
        return;

    }
    bool c_blank = false;
    if(dtype == 0x0){
        c_blank = true;
        float check;
        for(size_t i = 0; i < C->dims[0]; i++){
            for (size_t j = 0; j < C->dims[1]; j++){
                fastGet2D4(C, i, j, &check);
                if(check != 0){
                    c_blank = false;
                }
            }
        }
    }
    if(dtype == 0x1){
        c_blank = true;
        double check;
        for(size_t i = 0; i < C->dims[0]; i++){
            for (size_t j = 0; j < C->dims[1]; j++){
                fastGet2D4(C, i, j, &check);
                if(check != 0){
                    c_blank = false;
                }
            }
        }
    }   

    if(!beta_bypass && !c_blank){
        if(dtype == 0x0){
            float b_val;
            fastGet1D4(beta, 0, &b_val);
            for(size_t i = 0; i < C->dims[0]; i++){
                for(size_t j = 0; j < C->dims[1]; j++){
                    fastMultFloat32(*C, i, j, b_val);
                }
            }
        }
        else if(dtype == 0x1){
            double b_val;
            fastGet1D8(beta, 0, &b_val);
            for(size_t i = 0; i < C->dims[0]; i++){
                for(size_t j = 0; j < C->dims[1]; j++){
                    fastMultFloat64(*C, i, j, b_val);
                }
            }
        }
    }
    if(alpha_bypass){
        if(A->dtype == 0x0){
            size_t i_max = A->dims[0];
            size_t j_max = B->dims[1];
            size_t k_max = A->dims[1];
            float a_ik; // put input on stack
            float b_jk; // put weight on stack
            float c_ij;
            printf("%0x", A->data);
            for(size_t i = 0; i < i_max; i++){
                for(size_t j = 0; j < j_max; j++){
                    c_ij = 0;
                    for(size_t k = 0; k < k_max; k++){
                        fastGet2D4(A, i, k, &a_ik);
                        fastGet2D4(B, k, j, &b_jk);
                        c_ij += a_ik*b_jk;
                    }
                    fastSet2D4(C, i, j, &c_ij);
                }
            }
        }
        else if(A->dtype == 0x1){
            size_t i_max = A->dims[0];
            size_t j_max = B->dims[1];
            size_t k_max = A->dims[1];
            double a_ik; // put input on stack
            double b_jk; // put weight on stack
            double c_ij;
            for(size_t i = 0; i < i_max; i++){
                for(size_t j = 0; j < j_max; j++){
                    c_ij = 0;
                    for(size_t k = 0; k < k_max; k++){
                        fastGet2D8(A, i, k, &a_ik);
                        fastGet2D8(B, k, j, &b_jk);
                        c_ij += a_ik*b_jk;
                    }
                    fastSet2D8(C, i, j, &c_ij);
                }
            }
        }
    }
    else{
        if(A->dtype == 0x0){
            float a_val;
            fastGet1D4(alpha, 0, &a_val);
            size_t i_max = A->dims[0];
            size_t j_max = B->dims[1];
            size_t k_max = A->dims[1];
            float a_ik; // put input on stack
            float b_jk; // put weight on stack
            float c_ij;
            for(size_t i = 0; i < i_max; i++){
                for(size_t j = 0; j < j_max; j++){
                    c_ij = 0;
                    for(size_t k = 0; k < k_max; k++){
                        fastGet2D4(A, i, k, &a_ik);
                        fastGet2D4(B, k, j, &b_jk);
                        c_ij += a_ik*b_jk;
                    }
                    c_ij *= a_val;
                    fastSet2D4(C, i, j, &c_ij);
                }
            }
        }
        else if(A->dtype == 0x1){
            double a_val;
            fastGet1D8(alpha, 0, &a_val);
            size_t i_max = A->dims[0];
            size_t j_max = B->dims[1];
            size_t k_max = A->dims[1];
            double a_ik; // put input on stack
            double b_jk; // put weight on stack
            double c_ij;
            for(size_t i = 0; i < i_max; i++){
                for(size_t j = 0; j < j_max; j++){
                    c_ij = 0;
                    for(size_t k = 0; k < k_max; k++){
                        fastGet2D8(A, i, k, &a_ik);
                        fastGet2D8(B, k, j, &b_jk);
                        c_ij += a_ik*b_jk;
                    }
                    fastSet2D8(C, i, j, &c_ij);
                }
            }
        }

    }
}

#ifdef __cplusplus
}
#endif
#endif