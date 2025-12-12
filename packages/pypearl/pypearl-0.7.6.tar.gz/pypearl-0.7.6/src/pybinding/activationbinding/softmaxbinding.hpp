#ifndef SOFTBINDINGHPP
#define SOFTBINDINGHPP
#include <Python.h>
#include "../../neuralnetwork/activation/softmaxactivation.hpp"
#include "../matrixbinding.hpp"

using SoftmaxD = ActivationSoftMax<double>;

typedef struct {
  PyObject_HEAD
  SoftmaxD *cpp_obj;
} PySoftmaxDObject;

static void PySoftmaxD_dealloc(PySoftmaxDObject *self);
static PyObject* PySoftmaxD_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int PySoftmaxD_init(PySoftmaxDObject *self, PyObject *args, PyObject *kwds);
static PyObject* PySoftmaxD_forward(PySoftmaxDObject *self, PyObject *arg);
static PyObject* PySoftmaxD_backward(PySoftmaxDObject *self, PyObject *arg);

extern PyMethodDef PySoftmaxD_methods[];
extern PyGetSetDef PySoftmaxD_getset[];
extern PyTypeObject PySoftmaxDType;

#endif