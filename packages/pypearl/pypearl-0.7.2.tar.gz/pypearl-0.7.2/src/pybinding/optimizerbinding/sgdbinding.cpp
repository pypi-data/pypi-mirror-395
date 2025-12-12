#ifndef SGDBINDING
#define SGDBINDING
#include "sgdbinding.hpp"

static void
PySGDD_dealloc(PySGDDObject *self)
{
    delete self->cpp_obj;

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
PySGDD_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PySGDDObject *self = (PySGDDObject*)type->tp_alloc(type, 0);
    if (self) {
        self->cpp_obj = nullptr;
    }
    return (PyObject*)self;
}

static int
PySGDD_init(PySGDDObject *self, PyObject *args, PyObject *kwds)
{
    Py_ssize_t prev, cur;
    try {
        // allocate your C++ object
        self->cpp_obj = new SGDD(0.001);
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static PyObject*
PySGDD_optimize(PySGDDObject *self, PyObject *arg){

    if (!PyObject_TypeCheck(arg, &PyLayerDType)) {
        PyErr_SetString(PyExc_TypeError, "forward() expects an ArrayD2");
        return NULL;
    }
    PyLayerDObject *input_obj = (PyLayerDObject*)arg;

    try {
        self->cpp_obj->optimize_layer(*input_obj->cpp_obj);
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }


    Py_RETURN_NONE;
}


PyMethodDef PySGDD_methods[] = {
    {"optimize", (PyCFunction)PySGDD_optimize, METH_O, "layer->optimized layer"},
    {NULL, NULL, 0, NULL}
};

PyGetSetDef PySGDD_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
};

PyTypeObject PySGDDType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.SGD",                   // tp_name
    sizeof(PySGDDObject),           // tp_basicsize
    0,                               // tp_itemsize
    (destructor)PySGDD_dealloc,     // tp_dealloc
    0,                               // tp_vectorcall_offset (or tp_print in older versions)
    0,                               // tp_getattr
    0,                               // tp_setattr
    0,                               // tp_reserved / tp_compare
    0,                               // tp_repr
    0,                               // tp_as_number
    0,                               // tp_as_sequence
    0,                               // tp_as_mapping
    0,                               // tp_hash 
    0,                               // tp_call
    0,                               // tp_str
    0,                               // tp_getattro
    0,                               // tp_setattro
    0,                               // tp_as_buffer
    Py_TPFLAGS_DEFAULT,              // tp_flags
    "Neural Network SGD",            // tp_doc
    0,                               // tp_traverse
    0,                               // tp_clear
    0,                               // tp_richcompare
    0,                               // tp_weaklistoffset
    0,                               // tp_iter
    0,                               // tp_iternext
    PySGDD_methods,                  // tp_methods
    0,                               // tp_members
    PySGDD_getset,                   // tp_getset
    0,                               // tp_base
    0,                               // tp_dict
    0,                               // tp_descr_get
    0,                               // tp_descr_set
    0,                               // tp_dictoffset
    (initproc)PySGDD_init,           // tp_init
    0,                               // tp_alloc
    PySGDD_new                       // tp_new
};

#endif