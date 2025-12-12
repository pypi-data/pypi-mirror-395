#ifndef CCEBINDINGHPP
#define CCEBINDINGHPP
#include <Python.h>
#include "../../neuralnetwork/loss/cceloss.hpp"
#include "../matrixbinding.hpp"

using CCED = LossCCE<double>;

typedef struct {
  PyObject_HEAD
  CCED *cpp_obj;
} PyCCEDObject;

static void PyCCED_dealloc(PyCCEDObject *self);
static PyObject* PyCCED_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int PyCCED_init(PyCCEDObject *self, PyObject *args, PyObject *kwds);
static PyObject* PyCCED_forward(PyCCEDObject *self, PyObject *arg, PyObject *kwds);

extern PyMethodDef PyCCED_methods[];
extern PyGetSetDef PyCCED_getset[];
extern PyTypeObject PyCCEDType;

#endif