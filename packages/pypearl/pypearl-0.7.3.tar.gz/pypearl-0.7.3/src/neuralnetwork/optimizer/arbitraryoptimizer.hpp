#ifndef ArbitraryOptim_HPP
#define ArbitraryOptim_HPP

#include <Python.h>
#include "../../matrix/structures/ndarray.hpp"
#include "../layer/dense.hpp"

struct optim {
    PyObject_HEAD
    /*
     * Types:
     * 0x0: Standard Gradient Descent
     */
    uint8_t type;

    uint64_t iterations;

    // This costs 2 double->float conversions per layer optimized and in exchange allows for optimizers to be dtype invariant
    double learning_rate;

    double decay_rate;

    double original_learning_rate;

};

// Python handling
static void optim_dealloc(optim *self);
static PyObject * optim_str(optim *self);
static PyObject * optim_new(PyTypeObject *type, PyObject *args, PyObject *kwds);

// Initializers for different function types
static int GD_init(optim *self, PyObject *args, PyObject *kwds);

extern PyMethodDef optim_methods[];
extern PyGetSetDef optim_getset[];
extern PyTypeObject optimGDType;


// Functions to get loss working
void optimize_layer(dense* layer, optim& self);
#include "arbitraryoptimizer.cpp"

#endif