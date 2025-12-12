#ifndef ArbitraryBindingTPP
#define ArbitraryBindingTPP

#include "arbitraryactivationbinding.hpp"

static void PyAL_dealloc(PyAL *self)
{

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* PyAL_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyAL *self = (PyAL*)type->tp_alloc(type, 0);
    if (self) {
        self->data = nullptr;
    }
    return (PyObject*)self;
}

static int PyAL_init(PyAL *self, PyObject *args, PyObject *kwds)
{
    Py_ssize_t prev, cur;
    try {
        //self->data = new ActivationLayer{0x0, nullptr, nullptr, 0.0f, nullptr, false, 0.0f, 0.0f};
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static int PyReLU_init(PyAL *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"minimum", NULL};  
    double minimum = 0.0;  

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|d", kwlist, &minimum)) {
        return -1;  
    }

    Py_ssize_t prev, cur;
    try {
        // Obscure the hardcoded 0.0 branch micro optimization behind something no one ever has to see in Python because no Python programmer will ever use this on their own
        if(minimum == 0.0){
            self->data = new ActivationLayer{0x1, nullptr, nullptr, nullptr, nullptr, false, nullptr, nullptr};
        }
        else{
            ndarray* minval = arrayScalarCInit(&minimum, 0x1);
            self->data = new ActivationLayer{0x0, nullptr, nullptr, minval, nullptr, false, nullptr, nullptr};
        }
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static int PyLinear_init(PyAL *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"m", "b", "flow", NULL};  
    double m = 1.0;
    double b = 0.0;
    int flowint = 1;  
    
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|ddp", kwlist, &m, &b, &flowint)) {
        return -1;  
    }
    bool flow = false;
    if(kwds && PyDict_GetItemString(kwds, "flow")) flow = (flowint != 0);

    Py_ssize_t prev, cur;
    try {
        // Obscure the hardcoded 0.0 branch micro optimization behind something no one ever has to see in Python because no Python programmer will ever use this on their own
        if(b == 0.0){
            if(m == 1.0){
                if(flow==true){
                    // Optimized Linear with no logits (literally just a foward and backward return the EXACT ADDRESS that was inputted)
                    self->data = new ActivationLayer{0x5, nullptr, nullptr, nullptr, nullptr, false, nullptr, nullptr};
                }
                else{

                    // Copies a saved inputs, copies an outputs copies a dvalues -> dinputs. Literally the worst and most evil function ever. Do nothing in O(n^2) time. The fact I am supporting this for someone who might want it should warrant a nobel peace prize if this library ever gets more than 5 users.
                    self->data = new ActivationLayer{0x4, nullptr, nullptr, nullptr, nullptr, false, nullptr, nullptr};
                }
            }
            else{
                // Linear with a slope. Needs some optimization, but your welcome for saving a variable load and add instruction per value.
                ndarray* slope = arrayScalarCInit(&m, 0x1);

                self->data = new ActivationLayer{0xa, nullptr, nullptr, nullptr, nullptr, false, slope, nullptr};
            }
        }
        else{
            // Linear with a slope and an offset. Backpass for 0xa and 0xb are the same branch
            ndarray* slope = arrayScalarCInit(&m, 0x1);
            ndarray* intercept = arrayScalarCInit(&b, 0x1);

            self->data = new ActivationLayer{0xb, nullptr, nullptr, nullptr, nullptr, false, slope, intercept};
        }
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static int PySigmoid_init(PyAL *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {NULL};  

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "", kwlist)) {
        return -1;  
    }

    Py_ssize_t prev, cur;
    try {
        // Why is this simpler than linear well bc no args but still
        self->data = new ActivationLayer{0x6, nullptr, nullptr, nullptr, nullptr, false, nullptr, nullptr};

    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static int PyLeakyReLU_init(PyAL *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"minimum", "alpha", NULL};  
    double minimum = 0.0;
    double alpha = 0.0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|dd", kwlist, &minimum, &alpha)) {
        return -1;  
    }

    Py_ssize_t prev, cur;
    try {
        // Check if it's even leaky
        if(alpha == 0.0){
            if(minimum == 0.0){
                // Put in a 0 ReLU
                self->data = new ActivationLayer{0x1, nullptr, nullptr, nullptr, nullptr, false, nullptr, nullptr};
            }
            else{
                ndarray* minval = arrayScalarCInit(&minimum, 0x1);

                // Put in an arbitrary minimum ReLU
                self->data = new ActivationLayer{0x0, nullptr, nullptr, minval, nullptr, false, nullptr, nullptr};
            }
        }
        else{
            ndarray* minval = arrayScalarCInit(&minimum, 0x1);
            ndarray* alphaval = arrayScalarCInit(&alpha, 0x1);

            // Actual Leaky ReLU
            self->data = new ActivationLayer{0x3, nullptr, nullptr, minval, nullptr, false, alphaval, nullptr};
        }
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static int PyStep_init(PyAL *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"minimum", "maximum", "flip", NULL};  
    double minimum = 1.0f;
    double maximum = 0.0f;
    double flip = 0.0f;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|ddd", kwlist, &minimum, &maximum, &flip)) {
        return -1;  
    }

    Py_ssize_t prev, cur;

    try {
        ndarray* minval = arrayScalarCInit(&flip, 0x1);
        ndarray* alphaval = arrayScalarCInit(&maximum, 0x1);
        ndarray* betaval = arrayScalarCInit(&minimum, 0x1);
        // Actual Leaky ReLU
        self->data = new ActivationLayer{0x7, nullptr, nullptr, minval, nullptr, false, alphaval, betaval};
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static int PySoftmax_init(PyAL *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = { NULL};  
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "", kwlist)) {
        return -1;  
    }

    Py_ssize_t prev, cur;

    try {
        self->data = new ActivationLayer{0x2, nullptr, nullptr, nullptr, nullptr, false, nullptr, nullptr};
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static int PyReverseReLU_init(PyAL *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"maximum", NULL};  
    double maximum = 0.0;  
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|d", kwlist, &maximum)) {
        return -1;  
    }


    Py_ssize_t prev, cur;
    try {
        ndarray* maxval = arrayScalarCInit(&maximum, 0x1);

        // If this function becomes popular I'll probably optimize for now it's one path
        self->data = new ActivationLayer{0xc, nullptr, nullptr, maxval, nullptr, false, nullptr, nullptr};
        
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static ndarray* PyAL_forward(PyAL *self, PyObject *arg){

    PyAL *activation = (PyAL*) self;

    static char *kwlist[] = { (char*)"x", NULL };
    if (!PyObject_TypeCheck(arg, &ndarrayType)) {
        PyErr_SetString(PyExc_TypeError, "forward() expects an ndarray");
        return NULL;
    }
    ndarray *input = (ndarray*)arg;
    try {
        ndarray *y = activationForward(input, (*activation->data));
        if(y){
            return y;
        }
        else{
            PyErr_SetString(PyExc_TypeError, "Never called forward");
            return NULL;
        }
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }
}

static ndarray * PyAL_backward(PyAL *self, PyObject *arg){
    PyAL *activation = (PyAL*) self;

    if (!PyObject_TypeCheck(arg, &ndarrayType)) {
        PyErr_SetString(PyExc_TypeError, "backward() expects an ndarray");
        return NULL;
    }
    ndarray *input = (ndarray*)arg;

    try {
        std::cout << "Calling back" << std::endl;
        ndarray* y = activationBackward(input, (*activation->data));
        if(y){
            return y;
        }
        else{
            PyErr_SetString(PyExc_TypeError, "You must call forward before backward");
            return NULL;
        }
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }

}

PyMethodDef PyAL_methods[]{
    {"forward", (PyCFunction)PyAL_forward, METH_O, "forward(x)->y"},
    {"backward", (PyCFunction)PyAL_backward, METH_O, "backward(x)->y"},
    {NULL, NULL, 0, NULL}
};

PyGetSetDef PyAL_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
};

PyTypeObject PyALType{
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.activation",                          // tp_name
    sizeof(PyAL),                   // tp_basicsize
    0,                                       // tp_itemsize
    (destructor)PyAL_dealloc,            // tp_dealloc
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
    "Neural Network Activation",                 // tp_doc
    0,                                       // tp_traverse
    0,                                       // tp_clear
    0,                                       // tp_richcompare
    0,                                       // tp_weaklistoffset
    0,                                       // tp_iter
    0,                                       // tp_iternext
    PyAL_methods,                         // tp_methods
    0,                                       // tp_members
    PyAL_getset,                          // tp_getset
    0,                                       // tp_base
    0,                                       // tp_dict
    0,                                       // tp_descr_get
    0,                                       // tp_descr_set
    0,                                       // tp_dictoffset
    (initproc)PyAL_init,                 // tp_init
    0,                                       // tp_alloc
    PyAL_new,                             // tp_new
};

PyTypeObject PyRELUType{
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.RELU",                          // tp_name
    sizeof(PyAL),                   // tp_basicsize
    0,                                       // tp_itemsize
    (destructor)PyAL_dealloc,            // tp_dealloc
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
    "Neural Network ReLU Activation",                 // tp_doc
    0,                                       // tp_traverse
    0,                                       // tp_clear
    0,                                       // tp_richcompare
    0,                                       // tp_weaklistoffset
    0,                                       // tp_iter
    0,                                       // tp_iternext
    PyAL_methods,                         // tp_methods
    0,                                       // tp_members
    PyAL_getset,                          // tp_getset
    0,                                       // tp_base
    0,                                       // tp_dict
    0,                                       // tp_descr_get
    0,                                       // tp_descr_set
    0,                                       // tp_dictoffset
    (initproc)PyReLU_init,                 // tp_init
    0,                                       // tp_alloc
    PyAL_new,                             // tp_new
};

PyTypeObject PyLinearType{
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.Linear",                          // tp_name
    sizeof(PyAL),                   // tp_basicsize
    0,                                       // tp_itemsize
    (destructor)PyAL_dealloc,            // tp_dealloc
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
    "Neural Network Linear Activation",                 // tp_doc
    0,                                       // tp_traverse
    0,                                       // tp_clear
    0,                                       // tp_richcompare
    0,                                       // tp_weaklistoffset
    0,                                       // tp_iter
    0,                                       // tp_iternext
    PyAL_methods,                         // tp_methods
    0,                                       // tp_members
    PyAL_getset,                          // tp_getset
    0,                                       // tp_base
    0,                                       // tp_dict
    0,                                       // tp_descr_get
    0,                                       // tp_descr_set
    0,                                       // tp_dictoffset
    (initproc)PyLinear_init,                 // tp_init
    0,                                       // tp_alloc
    PyAL_new,                             // tp_new
};

PyTypeObject PySigmoidType{
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.Sigmoid",                          // tp_name
    sizeof(PyAL),                   // tp_basicsize
    0,                                       // tp_itemsize
    (destructor)PyAL_dealloc,            // tp_dealloc
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
    "Neural Network Sigmoid Activation",                 // tp_doc
    0,                                       // tp_traverse
    0,                                       // tp_clear
    0,                                       // tp_richcompare
    0,                                       // tp_weaklistoffset
    0,                                       // tp_iter
    0,                                       // tp_iternext
    PyAL_methods,                         // tp_methods
    0,                                       // tp_members
    PyAL_getset,                          // tp_getset
    0,                                       // tp_base
    0,                                       // tp_dict
    0,                                       // tp_descr_get
    0,                                       // tp_descr_set
    0,                                       // tp_dictoffset
    (initproc)PySigmoid_init,                 // tp_init
    0,                                       // tp_alloc
    PyAL_new,                             // tp_new
};

PyTypeObject PyLeakyReLUType{
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.LeakyReLU",                          // tp_name
    sizeof(PyAL),                   // tp_basicsize
    0,                                       // tp_itemsize
    (destructor)PyAL_dealloc,            // tp_dealloc
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
    "Neural Network Leaky ReLU Activation",                 // tp_doc
    0,                                       // tp_traverse
    0,                                       // tp_clear
    0,                                       // tp_richcompare
    0,                                       // tp_weaklistoffset
    0,                                       // tp_iter
    0,                                       // tp_iternext
    PyAL_methods,                         // tp_methods
    0,                                       // tp_members
    PyAL_getset,                          // tp_getset
    0,                                       // tp_base
    0,                                       // tp_dict
    0,                                       // tp_descr_get
    0,                                       // tp_descr_set
    0,                                       // tp_dictoffset
    (initproc)PyLeakyReLU_init,                 // tp_init
    0,                                       // tp_alloc
    PyAL_new,                             // tp_new
};

PyTypeObject PyStepType{
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.Step",                          // tp_name
    sizeof(PyAL),                   // tp_basicsize
    0,                                       // tp_itemsize
    (destructor)PyAL_dealloc,            // tp_dealloc
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
    "Neural Network Step Activation",                 // tp_doc
    0,                                       // tp_traverse
    0,                                       // tp_clear
    0,                                       // tp_richcompare
    0,                                       // tp_weaklistoffset
    0,                                       // tp_iter
    0,                                       // tp_iternext
    PyAL_methods,                         // tp_methods
    0,                                       // tp_members
    PyAL_getset,                          // tp_getset
    0,                                       // tp_base
    0,                                       // tp_dict
    0,                                       // tp_descr_get
    0,                                       // tp_descr_set
    0,                                       // tp_dictoffset
    (initproc)PyStep_init,                 // tp_init
    0,                                       // tp_alloc
    PyAL_new,                             // tp_new
};

// There's no way I'll ever track down all the random comments in this library
PyTypeObject PySoftmaxType{
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.Softmax",                          // tp_name
    sizeof(PyAL),                   // tp_basicsize
    0,                                       // tp_itemsize
    (destructor)PyAL_dealloc,            // tp_dealloc
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
    "Neural Network Softmax Activation",                 // tp_doc
    0,                                       // tp_traverse
    0,                                       // tp_clear
    0,                                       // tp_richcompare
    0,                                       // tp_weaklistoffset
    0,                                       // tp_iter
    0,                                       // tp_iternext
    PyAL_methods,                         // tp_methods
    0,                                       // tp_members
    PyAL_getset,                          // tp_getset
    0,                                       // tp_base
    0,                                       // tp_dict
    0,                                       // tp_descr_get
    0,                                       // tp_descr_set
    0,                                       // tp_dictoffset
    (initproc)PySoftmax_init,                 // tp_init
    0,                                       // tp_alloc
    PyAL_new,                             // tp_new
};

PyTypeObject PyReverseReLUType{
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.ReverseReLU",                          // tp_name
    sizeof(PyAL),                   // tp_basicsize
    0,                                       // tp_itemsize
    (destructor)PyAL_dealloc,            // tp_dealloc
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
    "Neural Network Softmax Activation",                 // tp_doc
    0,                                       // tp_traverse
    0,                                       // tp_clear
    0,                                       // tp_richcompare
    0,                                       // tp_weaklistoffset
    0,                                       // tp_iter
    0,                                       // tp_iternext
    PyAL_methods,                         // tp_methods
    0,                                       // tp_members
    PyAL_getset,                          // tp_getset
    0,                                       // tp_base
    0,                                       // tp_dict
    0,                                       // tp_descr_get
    0,                                       // tp_descr_set
    0,                                       // tp_dictoffset
    (initproc)PyReverseReLU_init,                 // tp_init
    0,                                       // tp_alloc
    PyAL_new,                             // tp_new
};

#endif