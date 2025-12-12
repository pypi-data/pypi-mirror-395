#ifndef LAYERBINDINGHPP
#define LAYERBINDINGHPP
#include <Python.h>
#include "../neuralnetwork/layer/layer.hpp"
#include "matrixbinding.hpp"

using LayerD = Layer<double>;

typedef struct {
  PyObject_HEAD
  LayerD *cpp_obj;
} PyLayerDObject;



static void PyLayerD_dealloc(PyLayerDObject *self);
static PyObject* PyLayerD_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int PyLayerD_init(PyLayerDObject *self, PyObject *args, PyObject *kwds);
static PyObject* PyLayerD_forward(PyLayerDObject *self, PyObject *arg);
static PyObject* PyLayerD_backward(PyLayerDObject *self, PyObject *arg);

extern PyMethodDef PyLayerD_methods[];
extern PyGetSetDef PyLayerD_getset[];
extern PyTypeObject PyLayerDType;

#endif