#pragma once

#include <Python.h>
#include "../../matrix/matrix.hpp"
#include "../../neuralnetwork/activation/arbitraryactivation.hpp"

using AL = ActivationLayer;  

typedef struct {
    PyObject_HEAD
    AL* data;  
} PyAL;

static void PyAL_dealloc(PyAL *self);
static PyObject* PyAL_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int PyAL_init(PyAL *self, PyObject *args, PyObject *kwds);

static int PyReLU_init(PyAL *self, PyObject *args, PyObject *kwds);
static int PyLinear_init(PyAL *self, PyObject *args, PyObject *kwds);
static int PySigmoid_init(PyAL *self, PyObject *args, PyObject *kwds);
static int PyStep_init(PyAL *self, PyObject *args, PyObject *kwds);
static int PyLeakyReLU_init(PyAL *self, PyObject *args, PyObject *kwds);
static int PySoftmax_init(PyAL *self, PyObject *args, PyObject *kwds);
static int PyReverseReLU_init(PyAL *self, PyObject *args, PyObject *kwds);

static ndarray* PyAL_forward(PyAL *self, PyObject *arg);
static ndarray * PyAL_backward(PyAL *self, PyObject *arg);

extern PyMethodDef PyAL_methods[];
extern PyGetSetDef PyAL_getset[];
extern PyTypeObject PyALType;

extern PyTypeObject PyRELUType;
extern PyTypeObject PyLinearType;
extern PyTypeObject PySigmoidType;
extern PyTypeObject PyLeakyReLUType;
extern PyTypeObject PySoftmaxType;
extern PyTypeObject PyStepType;
extern PyTypeObject PyReverseReLUType;

#include "arbitraryactivationbinding.cpp"