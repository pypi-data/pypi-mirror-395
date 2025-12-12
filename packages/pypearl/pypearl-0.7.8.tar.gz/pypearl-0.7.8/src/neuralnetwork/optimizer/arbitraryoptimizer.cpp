#ifndef ArbitraryOptim_CPP
#define ArbitraryOptim_CPP

#include <cmath>

#include "arbitraryoptimizer.hpp"

void update_params(optim* self){
    self->learning_rate = self->original_learning_rate*(1.0f/(1.0f + self->decay_rate * self->iterations));
    self->iterations++;
}

void optimize_layer(dense* layer, optim& self){
    if(self.type == 0x0){
        // If your fuzzer took you here, either your entry point is wrong, or someone is using my library poorly, assuming the glitch has something to do with layer->weights having a bad value.
        if(layer->dtype == 0x0){
            float lr = (float)self.learning_rate;
            float amount;
            
            for(size_t i = 0; i < layer->weights->dims[0]; i++){
                for(size_t j = 0; j < layer->weights->dims[1]; j++){

                    fastGet2D4(layer->dweights, i, j, &amount);

                    amount *= -lr;

                    fastIncFloat32(layer->weights, i, j, amount);
                }
            }

            for(size_t i = 0; i < layer->biases->dims[0]; i++){
                fastGet1D4Index(layer->dbiases, i, &amount);

                amount*=lr;
                ((float*)(layer->biases->data+layer->biases->strides[0]*i))[0] -= amount;
            }
        }
        else if(layer->dtype == 0x1){
            double amount;
            for(size_t i = 0; i < layer->weights->dims[0]; i++){
                for(size_t j = 0; j < layer->weights->dims[1]; j++){
                    fastGet2D8(layer->dweights, i, j, &amount);
                    amount *= -self.learning_rate;

                    fastIncFloat64(layer->weights, i, j, amount);
                }
            }            
            for(size_t i = 0; i < layer->biases->dims[0]; i++){
                fastGet1D8Index(layer->dbiases, i, &amount);

                amount*=self.learning_rate;
                ((double*)(layer->biases+layer->biases->strides[0]*i))[0] -= amount;
            }


        }
    }
}


static PyObject* Py_optimize_layer(optim *self, PyObject *args)
{
    dense * layer = NULL;

    // Parse Python-level call: loss.forward(outputs, y_true)
    if (!PyArg_ParseTuple(args, "O", &layer)) {
        return NULL;
    }

    optimize_layer(layer, *self);
    Py_RETURN_NONE;
}

static PyObject* Py_update_params(optim *self)
{
    update_params(self);
    Py_RETURN_NONE;
}


static void optim_dealloc(optim *self)
{
    // This isn't an error, it's 2 ints, 3 doubles, it can handle itself.
}

static PyObject* optim_str(optim *self)
{
    _PyUnicodeWriter w; 
    _PyUnicodeWriter_Init(&w);
    w.min_length = 128;
    _PyUnicodeWriter_WriteASCIIString(&w, "Optimizer", 9);
    return _PyUnicodeWriter_Finish(&w);
}

static PyObject *
optim_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    (void)args;
    (void)kwds;
    optim *self = (optim*)type->tp_alloc(type, 0);

    return (PyObject*)self;
}

// categorical cross entropy
static int
GD_init(optim *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {
        (char *)"learning_rate",
        (char *)"decay_rate",
        NULL
    };

    double learning_rate = 0.01;
    double decay_rate = 0.0;


    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|dd", kwlist, &learning_rate, &decay_rate, NULL)) {
        return -1;  
    }
    self->type = 0x0;

    self->learning_rate = learning_rate;

    self->decay_rate = decay_rate;

    return 0;
}

PyMethodDef optim_methods[] = {
    {
        "optimize_layer",
        (PyCFunction)Py_optimize_layer,
        METH_VARARGS,  // because we're using a tuple of args
        PyDoc_STR("Optimizer Layer")
    },
    {
        "update_params",
        (PyCFunction)Py_update_params,
        METH_NOARGS,  // because we're using a tuple of args
        PyDoc_STR("Updates Parameters")
    },

    {NULL, NULL, 0, NULL}
};

PyGetSetDef optim_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
}; 

PyTypeObject optimGDType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.gd",               // tp_name
    sizeof(optim),                  // tp_basicsize
    0,                               // tp_itemsize
    (destructor)optim_dealloc,   // tp_dealloc
    0,                               // tp_vectorcall_offset / tp_print
    0,                               // tp_getattr
    0,                               // tp_setattr
    0,                               // tp_reserved / tp_compare
    (reprfunc)optim_str,         // tp_repr
    0,                               // tp_as_number
    0,                               // tp_as_sequence
    0,                               // tp_as_mapping
    0,                               // tp_hash
    0,                               // tp_call
    (reprfunc)optim_str,         // tp_str
    0,                               // tp_getattro
    0,                               // tp_setattro
    0,                               // tp_as_buffer
    Py_TPFLAGS_DEFAULT,              // tp_flags
    "Gradient Descent Optimizer",              // tp_doc
    0,                               // tp_traverse
    0,                               // tp_clear
    0,                               // tp_richcompare
    0,                               // tp_weaklistoffset
    0,                               // tp_iter
    0,                               // tp_iternext
    optim_methods,               // tp_methods
    0,                               // tp_members
    optim_getset,                // tp_getset
    0,                               // tp_base
    0,                               // tp_dict
    0,                               // tp_descr_get
    0,                               // tp_descr_set
    0,                               // tp_dictoffset
    (initproc)GD_init,        // tp_init
    0,                               // tp_alloc
    optim_new                    // tp_new
};

#endif