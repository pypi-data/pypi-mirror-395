#pragma once

#ifndef DENSEHPP
#define DENSEHPP

#include <random>
#include <exception>
#include <iostream>
#include <cmath>
#include <vector>

#include <Python.h>
using std::size_t;

#include "../../matrix/structures/ndarray.hpp"

typedef struct {
    PyObject_HEAD
    
    // Not actually needed and definitely restricts flexibility of mixed precision options BUT who does mixed precision neural networks.
    // Since every ndarray here is a pointer it would require 2 calls to memory to get the datatype of a layer instead of 1 that's why this is here.
    uint8_t dtype;

    ndarray* saved_inputs;

    ndarray* biases;
    ndarray* weights;

    ndarray* outputs;
    ndarray* dinputs;

    ndarray* dbiases;
    ndarray* dweights;

    bool momentum;
} dense;

// Python handling
static void dense_dealloc(dense *self);
static PyObject * dense_str(dense *self);
static PyObject * dense_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int dense_init(dense *self, PyObject *args, PyObject *kwds);
static ndarray* PyDense_weights(dense *self);

extern PyMethodDef dense_methods[];
extern PyGetSetDef dense_getset[];
extern PyTypeObject denseType;


#include "dense.cpp"

#endif