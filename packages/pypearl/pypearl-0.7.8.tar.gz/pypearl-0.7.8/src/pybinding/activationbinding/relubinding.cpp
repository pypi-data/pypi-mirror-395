#ifndef RELUBINDING
#define RELUBINDING
#include "relubinding.hpp"

static void
PyReLUD_dealloc(PyReLUDObject *self)
{
    delete self->cpp_obj;

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
PyReLUD_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyReLUDObject *self = (PyReLUDObject*)type->tp_alloc(type, 0);
    if (self) {
        self->cpp_obj = nullptr;
    }
    return (PyObject*)self;
}

static int
PyReLUD_init(PyReLUDObject *self, PyObject *args, PyObject *kwds)
{
    Py_ssize_t prev, cur;
    try {
        // allocate your C++ object
        self->cpp_obj = new ReLUD();
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static PyObject * 
PyReLUD_forward(PyReLUDObject *self, PyObject *arg){
    PyReLUDObject *relu_obj = (PyReLUDObject*) self;

    static char *kwlist[] = { (char*)"x", NULL };
    if (!PyObject_TypeCheck(arg, &PyArrayD2Type)) {
        PyErr_SetString(PyExc_TypeError, "forward() expects an ArrayD2");
        return NULL;
    }
    PyArrayD2Object *input_obj = (PyArrayD2Object*)arg;

    ArrayD2 out_cpp;
    try {
        out_cpp = relu_obj->cpp_obj->forward(*input_obj->cpp_obj, 8, 8);
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }

    // Allocate a new Python ArrayD2 object
    PyObject *out_py = PyArrayD2Type.tp_new(&PyArrayD2Type, NULL, NULL);
    if (!out_py) return NULL;

    // Steal the C++ result into its cpp_obj
    ((PyArrayD2Object*)out_py)->cpp_obj = new ArrayD2(std::move(out_cpp));

    return out_py;
}

static PyObject * 
PyReLUD_backward(PyReLUDObject *self, PyObject *arg){
    PyReLUDObject *relu_obj = (PyReLUDObject*) self;

    if (!PyObject_TypeCheck(arg, &PyArrayD2Type)) {
        PyErr_SetString(PyExc_TypeError, "forward() expects an ArrayD2");
        return NULL;
    }
    PyArrayD2Object *input_obj = (PyArrayD2Object*)arg;

    ArrayD2 out_cpp;
    try {
        out_cpp = relu_obj->cpp_obj->backward(*input_obj->cpp_obj);
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }

    // Allocate a new Python ArrayD2 object
    PyObject *out_py = PyArrayD2Type.tp_new(&PyArrayD2Type, NULL, NULL);
    if (!out_py) return NULL;

    // Steal the C++ result into its cpp_obj
    ((PyArrayD2Object*)out_py)->cpp_obj = new ArrayD2(std::move(out_cpp));

    return out_py;
}

PyMethodDef PyReLUD_methods[] = {
    {"forward", (PyCFunction)PyReLUD_forward, METH_O, "forward(x)->y"},
    {"backward", (PyCFunction)PyReLUD_backward, METH_O, "backward(x)->y"},
    {NULL, NULL, 0, NULL}
};

PyGetSetDef PyReLUD_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
};

PyTypeObject PyReLUDType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.ReLU",                          // tp_name
    sizeof(PyReLUDObject),                   // tp_basicsize
    0,                                       // tp_itemsize
    (destructor)PyReLUD_dealloc,            // tp_dealloc
    0,                                       // tp_vectorcall_offset / tp_print (deprecated)
    0,                                       // tp_getattr
    0,                                       // tp_setattr
    0,                                       // tp_as_async / tp_compare
    0,                                       // tp_repr
    0,                                       // tp_as_number
    0,                                       // tp_as_sequence
    0,                                       // tp_as_mapping
    0,                                       // tp_hash
    0,                                       // tp_call
    0,                                       // tp_str
    0,                                       // tp_getattro
    0,                                       // tp_setattro
    0,                                       // tp_as_buffer
    Py_TPFLAGS_DEFAULT,                      // tp_flags
    "Neural Network Layer",                 // tp_doc
    0,                                       // tp_traverse
    0,                                       // tp_clear
    0,                                       // tp_richcompare
    0,                                       // tp_weaklistoffset
    0,                                       // tp_iter
    0,                                       // tp_iternext
    PyReLUD_methods,                         // tp_methods
    0,                                       // tp_members
    PyReLUD_getset,                          // tp_getset
    0,                                       // tp_base
    0,                                       // tp_dict
    0,                                       // tp_descr_get
    0,                                       // tp_descr_set
    0,                                       // tp_dictoffset
    (initproc)PyReLUD_init,                 // tp_init
    0,                                       // tp_alloc
    PyReLUD_new,                             // tp_new
};



#endif