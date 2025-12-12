#ifndef SGDBINDINGHPP
#define SGDBINDINGHPP
#include <Python.h>
#include "../../neuralnetwork/optimizer/sgdoptimizer.hpp"
#include "../matrixbinding.hpp"
#include "../layerbinding.hpp"

using SGDD = OptimizerSGD<double>;

typedef struct {
  PyObject_HEAD
  SGDD *cpp_obj;
} PySGDDObject;

static void PySGDD_dealloc(PySGDDObject *self);
static PyObject* PySGDD_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int PySGDD_init(PySGDDObject *self, PyObject *args, PyObject *kwds);
static void PySGDD_layer(PySGDDObject *self, PyObject *arg);

extern PyMethodDef PySGDD_methods[];
extern PyGetSetDef PySGDD_getset[];
extern PyTypeObject PySGDDType;

#endif