#ifndef ARRAYFUNCTIONS_TPP
#define ARRAYFUNCTIONS_TPP

#include "arrayfunctions.hpp"

template <typename NumType>
bool checkEquality2D(Array<NumType, 2>& arr1, Array<NumType, 2>& arr2){
    if(arr1.shape[0]!=arr2.shape[0] || arr1.shape[1] != arr2.shape[1]){
        return false;
    }

    // maybe I'm wrong but this feels like it would take less instructions to load if we just put the LCV's on the stack
    size_t imax = arr1.shape[0];
    size_t jmax = arr1.shape[1];
    for(size_t i = 0; i < imax; i++){
        for(size_t j = 0; j < jmax; j++){
            if(arr1[i][j] != arr2[i][j]){
                return false;
            }
        }
    }
    return true;
}


// delta refers to lowercase delta, not uppercase delta. I googled that before so you should know it.

template <typename NumType>
bool checkEquality2DLoose(Array<NumType, 2>& arr1, Array<NumType, 2>& arr2, NumType delta){
    if(arr1.shape[0]!=arr2.shape[0] || arr1.shape[1] != arr2.shape[1]){
        return false;
    }

    // maybe I'm wrong but this feels like it would take less instructions to load if we just put the LCV's on the stack
    size_t imax = arr1.shape[0];
    size_t jmax = arr1.shape[1];
    for(size_t i = 0; i < imax; i++){
        for(size_t j = 0; j < jmax; j++){
            if(abs(arr1[i][j]*(1+delta)) > abs(arr2[i][j]) || abs(arr1[i][j]*(1-delta)) < abs(arr2[i][j]) ){
                return false;
            }
        }
    }
    return true;
}

#endif