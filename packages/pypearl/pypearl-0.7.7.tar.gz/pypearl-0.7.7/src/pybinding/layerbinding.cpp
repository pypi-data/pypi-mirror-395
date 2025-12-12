#ifndef LAYERBINDING
#define LAYERBINDING
#include "layerbinding.hpp"

static void
PyLayerD_dealloc(PyLayerDObject *self)
{
    delete self->cpp_obj;

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
PyLayerD_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyLayerDObject *self = (PyLayerDObject*)type->tp_alloc(type, 0);
    if (self) {
        self->cpp_obj = nullptr;
    }
    return (PyObject*)self;
}

static int
PyLayerD_init(PyLayerDObject *self, PyObject *args, PyObject *kwds)
{
    Py_ssize_t prev, cur;
    static char *kwlist[] = { (char*)"prev_layer_size", (char*)"layer_size", nullptr };
    // require one integer argument: size
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "nn", kwlist, &prev, &cur))
        return -1;

    try {
        // allocate your C++ object
        self->cpp_obj = new LayerD((size_t)prev, (size_t)cur, false);
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static PyObject* PyLayerD_forward(PyLayerDObject *self, PyObject *arg){
    PyLayerDObject *layer_obj = (PyLayerDObject*) self;

    if (!PyObject_TypeCheck(arg, &PyArrayD2Type)) {
        PyErr_SetString(PyExc_TypeError, "forward(x) expects an ArrayD2");
        return NULL;
    }
    PyArrayD2Object *input_obj = (PyArrayD2Object*)arg;

    ArrayD2 out_cpp;
    try {
        out_cpp = layer_obj->cpp_obj->forward(*input_obj->cpp_obj);
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

static PyObject* PyLayerD_backward(PyLayerDObject *self, PyObject *arg){
    PyLayerDObject *layer_obj = (PyLayerDObject*) self;

    if (!PyObject_TypeCheck(arg, &PyArrayD2Type)) {
        PyErr_SetString(PyExc_TypeError, "forward(x) expects an ArrayD2");
        return NULL;
    }
    PyArrayD2Object *input_obj = (PyArrayD2Object*)arg;

    ArrayD2 out_cpp;
    try {
        out_cpp = layer_obj->cpp_obj->backward(*input_obj->cpp_obj);
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


PyMethodDef PyLayerD_methods[] = {
    {"forward", (PyCFunction)PyLayerD_forward, METH_O, "forward(x)->y"},
    {"backward", (PyCFunction)PyLayerD_backward, METH_O, "backward"},
    {NULL, NULL, 0, NULL}
};

PyGetSetDef PyLayerD_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
};

PyTypeObject PyLayerDType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.Layer",                 // tp_name
    sizeof(PyLayerDObject),         // tp_basicsize
    0,                              // tp_itemsize
    (destructor)PyLayerD_dealloc,   // tp_dealloc
    0,                              // tp_vectorcall_offset or tp_print
    0,                              // tp_getattr
    0,                              // tp_setattr
    0,                              // tp_reserved / tp_compare
    0,                              // tp_repr
    0,                              // tp_as_number
    0,                              // tp_as_sequence
    0,                              // tp_as_mapping
    0,                              // tp_hash 
    0,                              // tp_call
    0,                              // tp_str
    0,                              // tp_getattro
    0,                              // tp_setattro
    0,                              // tp_as_buffer
    Py_TPFLAGS_DEFAULT,             // tp_flags
    "Neural Network Layer",         // tp_doc
    0,                              // tp_traverse
    0,                              // tp_clear
    0,                              // tp_richcompare
    0,                              // tp_weaklistoffset
    0,                              // tp_iter
    0,                              // tp_iternext
    PyLayerD_methods,               // tp_methods
    0,                              // tp_members
    PyLayerD_getset,                // tp_getset
    0,                              // tp_base
    0,                              // tp_dict
    0,                              // tp_descr_get
    0,                              // tp_descr_set
    0,                              // tp_dictoffset
    (initproc)PyLayerD_init,        // tp_init
    0,                              // tp_alloc
    PyLayerD_new                    // tp_new
};


#endif