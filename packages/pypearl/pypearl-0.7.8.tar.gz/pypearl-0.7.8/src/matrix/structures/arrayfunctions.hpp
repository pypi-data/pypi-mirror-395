#ifndef ArrayFunctions_HPP
#define ArrayFunctions_HPP

#include "array.hpp"
#include <cstdint>


template <typename NumType = float>
bool checkEquality2D(Array<NumType, 2>& arr1, Array<NumType, 2>& arr2);

#include "arrayfunctions.tpp"
#endif
