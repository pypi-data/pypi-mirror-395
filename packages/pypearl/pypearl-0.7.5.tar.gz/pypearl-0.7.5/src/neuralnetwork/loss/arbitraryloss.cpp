#ifndef ArbitraryLoss_TPP
#define ArbitraryLoss_TPP

#include <cmath>

#include "arbitraryloss.hpp"

ndarray* lossForward(ndarray* inputs, loss& self, ndarray* y_true){
    if(self.type == 0x0){
        if(y_true->nd == 1){
            if(y_true->dtype != 0x3){
                PyErr_SetString(PyExc_TypeError, "y_true must be of type long. If you're using int32, it currently doesn't autocast. Switch your type.");
                return NULL;
            }
            if(inputs->dtype == 0x0){
                
                size_t max = inputs->dims[0];
                float totals[max];
                ssize_t j;
                float temp;
                for(size_t i = 0; i < max; i++){
                    fastGet1D8Index(y_true, i, &j);
                    fastGet2D4(inputs, i, j, &temp);
                    totals[i] = std::fmax(std::fmin(temp,1),0);
                } 
                
                float sum = 0.0f;

                for(size_t i = 0; i < max; i++){
                    sum+=  -log(totals[i]);
                }

                float output = sum/((float)max);
                return arrayScalarCInit(&output, 0x0);
            }
        }
    }

}

ndarray* lossBackward(ndarray* inputs, loss& self, ndarray* y_true){
    if(self.type == 0x0){
        ndarray* dinputs = arrayCInit(2, inputs->dtype, inputs->dims);
        if(self.dinputs){
            Py_DecRef((PyObject*) self.dinputs);
        }
        self.dinputs = dinputs;
        if(y_true->nd == 1){
            if(y_true->dtype != 0x3){
                PyErr_SetString(PyExc_TypeError, "y_true must be of type long. If you're using int32, it currently doesn't autocast. Switch your type.");
                return NULL;
            }
            else if(y_true->dtype == 0x2){
                // Implement this. Probably needed as a general array function, so not gonna bother atm.
            }
            if(y_true->dims[0] != inputs->dims[0] || y_true ->nd != 1){
                PyErr_SetString(PyExc_TypeError, "y_true must be a 1 dimensional vector with the index of the correct class in all places.");
                return NULL;
            }
            if(inputs->dtype == 0x0){
                size_t length = inputs->dims[0];
                const float invN = float(1.0) / float(length);

                const float eps  = float(1e-12);

                float pyi;
                size_t j;
                float num;
                for (size_t i = 0; i < length; ++i) {
                    fastGet1D8Index(y_true, i, &j); // THIS IS SUPPOSED TO BE 8 BYTES DO NOT CHANGE
                    fastGet2D4(inputs, i, j, &pyi);
                    if (pyi < eps) pyi = eps;
                    num = -invN / pyi;
                    fastSet2D4(dinputs, i, j, &num);
                }
                ndincref(dinputs);
                return dinputs;
            }
        }
    }
    /*if(loss.type == 0x1){

        void* mem = std::malloc(sizeof(Array<NumType,2>));
        if (!mem) throw std::bad_alloc{};
        auto* p = new (mem) Array<NumType,2>(inputs->shape); 

        loss.dinputs = p;

        for (size_t i = 0; i < inputs->shape[0]; i++) {

            for (size_t j = 0; j < inputs->shape[1]; j++) {
                loss.dinputs->fastSet2D(i, j, inputs->fastGet2D(i, j));

                if (j == y_true[i]) {
                    loss.dinputs->fastInc2D(i, j, -1.0f);
                }

                loss.dinputs->fastSet2D(i, j, loss.dinputs->fastGet2D(i, j)/inputs->shape[0]);
            }
        }

        return loss.dinputs;
    }*/
}

static ndarray* Py_loss_forward(loss *self, PyObject *args)
{
    ndarray *outputs = NULL;
    ndarray *y_true  = NULL;

    // Parse Python-level call: loss.forward(outputs, y_true)
    if (!PyArg_ParseTuple(args, "OO", &outputs, &y_true)) {
        return NULL;
    }

    ndarray* output = lossForward(outputs, *self, y_true);
    Py_IncRef((PyObject*) output);
    return output;
}

static ndarray* Py_loss_backward(loss *self, PyObject *args)
{
    ndarray *outputs = NULL;
    ndarray *y_true  = NULL;

    // Parse Python-level call: loss.forward(outputs, y_true)
    if (!PyArg_ParseTuple(args, "OO", &outputs, &y_true)) {
        return NULL;
    }

    ndarray* output = lossBackward(outputs, *self, y_true);

    return output;
}

static void
loss_dealloc(loss *self)
{
    if(self->dinputs)
    nddecref(self->dinputs);

    if(self->saved_inputs)
    nddecref(self->saved_inputs);

    if(self->y_true)
    nddecref(self->y_true);
}

static PyObject* loss_str(loss *self)
{
    _PyUnicodeWriter w; 
    _PyUnicodeWriter_Init(&w);
    w.min_length = 128;
    _PyUnicodeWriter_WriteASCIIString(&w, "Loss", 4);
    return _PyUnicodeWriter_Finish(&w);
}

static PyObject *
loss_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    (void)args;
    (void)kwds;
    loss *self = (loss*)type->tp_alloc(type, 0);
    if (self) {
        self->y_true = nullptr;
        self->dinputs = nullptr;
        self->saved_inputs = nullptr;
    }

    return (PyObject*)self;
}

// categorical cross entropy
static int
CCE_init(loss *self, PyObject *args, PyObject *kwds)
{
    /*if (!PyArg_ParseTupleAndKeywords(args, kwds, "", NULL)) {
        std::cout << "ERROR HERE" << std::endl;
        return -1;  
    }*/
    self->type = 0x0;
    return 0;
}

PyMethodDef loss_methods[] = {
    {
        "forward",
        (PyCFunction)Py_loss_forward,
        METH_VARARGS,  // because we're using a tuple of args
        PyDoc_STR("forward(outputs, y_true) -> loss_value")
    },
    {
        "backward",
        (PyCFunction)Py_loss_backward,
        METH_VARARGS,
        PyDoc_STR("backward(outputs, y_true) -> dinputs")
    },
    {NULL, NULL, 0, NULL}
};

PyGetSetDef loss_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
}; 

PyTypeObject lossCCEType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.cce",               // tp_name
    sizeof(loss),                  // tp_basicsize
    0,                               // tp_itemsize
    (destructor)loss_dealloc,   // tp_dealloc
    0,                               // tp_vectorcall_offset / tp_print
    0,                               // tp_getattr
    0,                               // tp_setattr
    0,                               // tp_reserved / tp_compare
    (reprfunc)loss_str,         // tp_repr
    0,                               // tp_as_number
    0,                               // tp_as_sequence
    0,                               // tp_as_mapping
    0,                               // tp_hash
    0,                               // tp_call
    (reprfunc)loss_str,         // tp_str
    0,                               // tp_getattro
    0,                               // tp_setattro
    0,                               // tp_as_buffer
    Py_TPFLAGS_DEFAULT,              // tp_flags
    "Categorical Cross Entropy Loss",              // tp_doc
    0,                               // tp_traverse
    0,                               // tp_clear
    0,                               // tp_richcompare
    0,                               // tp_weaklistoffset
    0,                               // tp_iter
    0,                               // tp_iternext
    loss_methods,               // tp_methods
    0,                               // tp_members
    loss_getset,                // tp_getset
    0,                               // tp_base
    0,                               // tp_dict
    0,                               // tp_descr_get
    0,                               // tp_descr_set
    0,                               // tp_dictoffset
    (initproc)CCE_init,        // tp_init
    0,                               // tp_alloc
    loss_new                    // tp_new
};

#endif