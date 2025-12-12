#pragma once

#include <Python.h>
#include "../../matrix/matrix.hpp"
#include "../../neuralnetwork/loss/arbitraryloss.hpp"

using LS64 = LossStruct<double>;  

typedef struct {
    PyObject_HEAD
    LS64* data;  
} PyLS64;

static void PyLS64_dealloc(PyLS64 *self);
static PyObject* PyLS64_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int PyLS64_init(PyLS64 *self, PyObject *args, PyObject *kwds);

// Loss Initializers
static int PyCCE64_init(PyLS64 *self, PyObject *args, PyObject *kwds);

static PyObject* PyLS64_forward(PyLS64 *self, PyObject *args);
static PyObject * PyLS64_backward(PyLS64 *self, PyObject *args);

extern PyMethodDef PyLS64_methods[];
extern PyGetSetDef PyLS64_getset[];
extern PyTypeObject PyLS64Type;

// Loss Types
extern PyTypeObject PyCCE64Type;

#include "arbitrarylossbinding.cpp"