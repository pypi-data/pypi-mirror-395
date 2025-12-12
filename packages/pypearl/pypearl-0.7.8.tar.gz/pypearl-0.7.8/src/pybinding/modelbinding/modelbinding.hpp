#ifndef MODELBINDINGHPP
#define MODELBINDINGHPP
#include <Python.h>
#include "../../neuralnetwork/model/model.hpp"
#include "../../neuralnetwork/model/externalfunctions.hpp"
#include "../matrixbinding.hpp"

using CModel = Model<double>;

typedef struct {
  PyObject_HEAD
  CModel *cpp_obj;
} PyModelObject;

// Class Functions
static void PyModel_dealloc(PyModelObject *self);
static PyObject* PyModel_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int PyModel_init(PyModelObject *self, PyObject *args, PyObject *kwds);
static PyObject* PyModel_forwardGA(PyModelObject *self, PyObject *arg);
static PyObject* PyModel_addLayer(PyModelObject *self, PyObject *args);
static PyObject* PyModel_addReLU(PyModelObject *self, PyObject *Py_UNUSED);
static PyObject* PyModel_addSoftmax(PyModelObject *self, PyObject *Py_UNUSED);
static PyObject* PyModel_randomize(PyModelObject *self, PyObject *Py_UNUSED);
static PyObject* PyModel_loadModel(PyModelObject *self, PyObject *arg);
static PyObject* PyModel_saveModel(PyModelObject *self, PyObject *arg);

extern PyMethodDef PyModel_methods[];
extern PyGetSetDef PyModel_getset[];
extern PyTypeObject PyModelType;

// External Model Functions
PyObject* py_breed_models(PyObject* , PyObject* args);
PyObject* py_copy_model(PyObject*, PyObject* arg);

#endif