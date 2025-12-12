#ifndef ArbitraryLossBindingTPP
#define ArbitraryLossBindingTPP

#include "arbitrarylossbinding.hpp"

static void PyLS64_dealloc(PyLS64 *self)
{
    delete self->data->saved_inputs;

    delete self->data->dinputs;

    delete self->data->y_true;

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* PyLS64_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyLS64 *self = (PyLS64*)type->tp_alloc(type, 0);
    if (self) {
        self->data = nullptr;
    }
    return (PyObject*)self;
}

static int PyCCE64_init(PyLS64 *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {NULL};  

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "", kwlist)) {
        return -1;  
    }

    Py_ssize_t prev, cur;
    try {
        self->data = new LossStruct<double>{0x0, nullptr, nullptr, nullptr};
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static PyObject* PyLS64_forward(PyLS64 *self, PyObject *args){
    PyLS64 *activation = (PyLS64*) self;

    PyObject *input_arg;
    PyObject *y_true_arg;
    
    if (!PyArg_ParseTuple(args, "OO", &input_arg, &y_true_arg)) {
        return NULL;
    }
    
    if (!PyObject_TypeCheck(input_arg, &PyArrayD2Type)) {
        PyErr_SetString(PyExc_TypeError, "forward() expects first argument to be ArrayD2");
        return NULL;
    }
    
    if (!PyObject_TypeCheck(y_true_arg, &PyArrayI1Type)) {
        PyErr_SetString(PyExc_TypeError, "forward() expects second argument to be ArrayI1");
        return NULL;
    }
    
    PyArrayD2Object *input_obj = (PyArrayD2Object*)input_arg;
    PyArrayI1Object *y_true_obj = (PyArrayI1Object*)y_true_arg;

    double out_cpp;

    try {
        out_cpp = lossForward<double>(input_obj->cpp_obj, (*activation->data), (void*)y_true_obj->cpp_obj);
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }

    return PyFloat_FromDouble(out_cpp);
}

// Fix
static PyObject * PyLS64_backward(PyLS64 *self, PyObject *args){
    PyLS64 *activation = (PyLS64*) self;

    PyObject *input_arg;
    PyObject *y_true_arg;
    
    if (!PyArg_ParseTuple(args, "OO", &input_arg, &y_true_arg)) {
        return NULL;
    }
    
    if (!PyObject_TypeCheck(input_arg, &PyArrayD2Type)) {
        PyErr_SetString(PyExc_TypeError, "forward() expects first argument to be ArrayD2");
        return NULL;
    }
    
    if (!PyObject_TypeCheck(y_true_arg, &PyArrayI1Type)) {
        PyErr_SetString(PyExc_TypeError, "forward() expects second argument to be ArrayI1");
        return NULL;
    }
    
    PyArrayD2Object *input_obj = (PyArrayD2Object*)input_arg;
    PyArrayI1Object *y_true_obj = (PyArrayI1Object*)y_true_arg;

    ArrayD2* out_cpp;
    try {
        out_cpp = lossBackward<double>(input_obj->cpp_obj, (*activation->data), (void*)y_true_obj->cpp_obj);
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }

    // Allocate a new Python ArrayD2 object
    PyObject *out_py = PyArrayD2Type.tp_new(&PyArrayD2Type, NULL, NULL);
    if (!out_py) return NULL;

    // Steal the C++ result into its cpp_obj
    ((PyArrayD2Object*)out_py)->cpp_obj = new ArrayD2(std::move((*out_cpp)));

    return out_py;
}

// Fix
PyMethodDef PyLS64_methods[]{
    {"forward", (PyCFunction)PyLS64_forward, METH_VARARGS, "forward(x)->y"},
    {"backward", (PyCFunction)PyLS64_backward, METH_VARARGS, "backward(x)->y"},
    {NULL, NULL, 0, NULL}
};

PyGetSetDef PyLS64_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
};

PyTypeObject PyCCE64Type{
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.CCE64",                          // tp_name
    sizeof(PyLS64),                   // tp_basicsize
    0,                                       // tp_itemsize
    (destructor)PyLS64_dealloc,            // tp_dealloc
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
    "Neural Network CCE Loss",                 // tp_doc
    0,                                       // tp_traverse
    0,                                       // tp_clear
    0,                                       // tp_richcompare
    0,                                       // tp_weaklistoffset
    0,                                       // tp_iter
    0,                                       // tp_iternext
    PyLS64_methods,                         // tp_methods
    0,                                       // tp_members
    PyLS64_getset,                          // tp_getset
    0,                                       // tp_base
    0,                                       // tp_dict
    0,                                       // tp_descr_get
    0,                                       // tp_descr_set
    0,                                       // tp_dictoffset
    (initproc)PyCCE64_init,                 // tp_init
    0,                                       // tp_alloc
    PyLS64_new,                             // tp_new
};

#endif