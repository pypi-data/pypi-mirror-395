#ifndef ArbitraryLoss_HPP
#define ArbitraryLoss_HPP

#include "../../matrix/structures/ndarray.hpp"

struct loss {
    PyObject_HEAD
    /*
     * Types:
     * 0x0: CCE Loss (Unfused with softmax)
     */
    uint8_t type;
    ndarray* saved_inputs;

    // Will always be Array<NumType, 2> or Array<int, 1>, I believe it shouldn't effect efficiency as it will always be cast in switch statements.
    ndarray* y_true;

    ndarray* dinputs;

};

// Python handling
static void loss_dealloc(loss *self);
static PyObject * loss_str(loss *self);
static PyObject * loss_new(PyTypeObject *type, PyObject *args, PyObject *kwds);

// Initializers for different function types
static int CCE_init(loss *self, PyObject *args, PyObject *kwds);

extern PyMethodDef loss_methods[];
extern PyGetSetDef loss_getset[];
extern PyTypeObject lossCCEType;


// Functions to get loss working
ndarray* lossForward(ndarray* inputs, loss& layer, ndarray* y_true);
// The arguments technically aren't needed and you can just copy in the previous function but that makes lossForward n->n^2 in some cases
ndarray* lossBackward(ndarray* inputs, loss& layer, ndarray* y_true);



#include "arbitraryloss.cpp"

#endif