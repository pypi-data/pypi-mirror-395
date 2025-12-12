#ifndef RELUBINDINGHPP
#define RELUBINDINGHPP
#include <Python.h>
#include "../../neuralnetwork/activation/reluactivation.hpp"
#include "../matrixbinding.hpp"

using ReLUD = ActivationReLU<double>;

typedef struct {
  PyObject_HEAD
  ReLUD *cpp_obj;
} PyReLUDObject;

static void PyReLUD_dealloc(PyReLUDObject *self);
static PyObject* PyReLUD_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int PyReLUD_init(PyReLUDObject *self, PyObject *args, PyObject *kwds);
static PyObject* PyReLUD_forward(PyReLUDObject *self, PyObject *arg);
static PyObject * PyReLUD_backward(PyReLUDObject *self, PyObject *arg);

extern PyMethodDef PyReLUD_methods[];
extern PyGetSetDef PyReLUD_getset[];
extern PyTypeObject PyReLUDType;

#endif