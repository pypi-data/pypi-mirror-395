#ifndef NDITER_C
#define NDITER_C

#ifdef __cplusplus
extern "C" {
#endif

#include "ndarray.hpp"
/*
 * Layout of the file:
 * - It's just loops
 *
 * The following functions are just loops for various types of functions,
 *      there's probably a more efficient way to do this code wise with
 *      void pointers and such but I don't fully trust that would compile
 *      as fast, and I also just don't know how to do it tbh.
 */

void ndForeach(ndarray* arr, func visit){
    char* cur_elem = arr->data;
    
    size_t* cur_idx = (size_t*)malloc(arr->nd*sizeof(size_t));
    for(size_t i = 0; i < arr->nd; i++) cur_idx[i] = 0;

    for(;;){
        (*visit)(cur_elem, cur_idx, arr->nd);
        for(ssize_t k = (ssize_t)arr->nd-1; k >=0; k--){
            cur_idx[k]++;
            cur_elem+=arr->strides[k];

            if(cur_idx[k]<arr->dims[k]){
                goto next_element;
            }
            cur_elem -= arr->strides[k]*arr->dims[k];
            cur_idx[k] = 0;
        }
        break;
        next_element:
        ;
    }
}

// For each for element and dtype
void ndForeachED(ndarray* arr, funcED visit, double val){
    char* cur_elem = arr->data;
    
    size_t* cur_idx = (size_t*)malloc(arr->nd*sizeof(size_t));
    for(size_t i = 0; i < arr->nd; i++) cur_idx[i] = 0;

    for(;;){
        (*visit)(cur_elem, arr->dtype, val);
        for(ssize_t k = (ssize_t)arr->nd-1; k >=0; k--){
            cur_idx[k]++;
            cur_elem+=arr->strides[k];

            if(cur_idx[k]<arr->dims[k]){
                goto next_element;
            }
            cur_elem -= arr->strides[k]*arr->dims[k];
            cur_idx[k] = 0;
        }
        break;
        next_element:
        ;
    }
}

void ndForeachND(ndarray* arr, ndarray* other, funcND2 visit){
    char* cur_elem = arr->data;
    char* other_elem = other->data;
    
    size_t* cur_idx = (size_t*)malloc(arr->nd*sizeof(size_t));
    for(size_t i = 0; i < arr->nd; i++) cur_idx[i] = 0;

    for(;;){
        (*visit)(cur_elem, other_elem, arr->dtype);
        for(ssize_t k = (ssize_t)arr->nd-1; k >=0; k--){
            cur_idx[k]++;
            cur_elem += arr->strides[k];
            other_elem += other->strides[k];

            if(cur_idx[k] < arr->dims[k]){
                goto next_element;
            }
            cur_elem -= arr->strides[k] * arr->dims[k];
            other_elem -= other->strides[k] * other->dims[k];
            cur_idx[k] = 0;
        }
        break;
        next_element:
        ;
    }
}

#ifdef __cplusplus
}
#endif
#endif