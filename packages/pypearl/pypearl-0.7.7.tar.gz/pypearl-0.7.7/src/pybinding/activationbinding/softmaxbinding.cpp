#ifndef SOFTBINDING
#define SOFTBINDING
#include "softmaxbinding.hpp"

static void
PySoftmaxD_dealloc(PySoftmaxDObject *self)
{
    delete self->cpp_obj;

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
PySoftmaxD_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PySoftmaxDObject *self = (PySoftmaxDObject*)type->tp_alloc(type, 0);
    if (self) {
        self->cpp_obj = nullptr;
    }
    return (PyObject*)self;
}

static int
PySoftmaxD_init(PySoftmaxDObject *self, PyObject *args, PyObject *kwds)
{
    Py_ssize_t prev, cur;
    try {
        // allocate your C++ object
        self->cpp_obj = new SoftmaxD();
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static PyObject * 
PySoftmaxD_forward(PySoftmaxDObject *self, PyObject *arg){
    PySoftmaxDObject *soft_obj = (PySoftmaxDObject*) self;

    static char *kwlist[] = { (char*)"x", NULL };
    if (!PyObject_TypeCheck(arg, &PyArrayD2Type)) {
        PyErr_SetString(PyExc_TypeError, "forward() expects an ArrayD2");
        return NULL;
    }
    PyArrayD2Object *input_obj = (PyArrayD2Object*)arg;

    ArrayD2 out_cpp;
    try {
        out_cpp = soft_obj->cpp_obj->forward(*input_obj->cpp_obj, 8, 8);
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
PySoftmaxD_backward(PySoftmaxDObject *self, PyObject *arg){
    PySoftmaxDObject *soft_obj = (PySoftmaxDObject*) self;

    if (!PyObject_TypeCheck(arg, &PyArrayD2Type)) {
        PyErr_SetString(PyExc_TypeError, "forward() expects an ArrayD2");
        return NULL;
    }
    PyArrayD2Object *input_obj = (PyArrayD2Object*)arg;

    ArrayD2 out_cpp;
    try {
        out_cpp = soft_obj->cpp_obj->backward(*input_obj->cpp_obj);
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

PyMethodDef PySoftmaxD_methods[] = {
    {"forward", (PyCFunction)PySoftmaxD_forward, METH_O, "forward(x)->y"},
    {"backward", (PyCFunction)PySoftmaxD_backward, METH_O, "backward(x)->y"},
    {NULL, NULL, 0, NULL}
};

PyGetSetDef PySoftmaxD_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
};

PyTypeObject PySoftmaxDType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.Softmax",                  // tp_name
    sizeof(PySoftmaxDObject),           // tp_basicsize
    0,                                  // tp_itemsize
    (destructor)PySoftmaxD_dealloc,     // tp_dealloc
    0,                                  // tp_print (deprecated, safe to set 0)
    0,                                  // tp_getattr
    0,                                  // tp_setattr
    0,                                  // tp_reserved or tp_compare
    0,                                  // tp_repr
    0,                                  // tp_as_number
    0,                                  // tp_as_sequence
    0,                                  // tp_as_mapping
    0,                                  // tp_hash
    0,                                  // tp_call
    0,                                  // tp_str
    0,                                  // tp_getattro
    0,                                  // tp_setattro
    0,                                  // tp_as_buffer
    Py_TPFLAGS_DEFAULT,                 // tp_flags
    "Neural Network Softmax",           // tp_doc
    0,                                  // tp_traverse
    0,                                  // tp_clear
    0,                                  // tp_richcompare
    0,                                  // tp_weaklistoffset
    0,                                  // tp_iter
    0,                                  // tp_iternext
    PySoftmaxD_methods,                 // tp_methods
    0,                                  // tp_members
    PySoftmaxD_getset,                  // tp_getset
    0,                                  // tp_base
    0,                                  // tp_dict
    0,                                  // tp_descr_get
    0,                                  // tp_descr_set
    0,                                  // tp_dictoffset
    (initproc)PySoftmaxD_init,          // tp_init
    0,                                  // tp_alloc
    PySoftmaxD_new                      // tp_new
};



#endif