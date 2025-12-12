#ifndef CCEBINDING
#define CCEBINDING
#include "modelbinding.hpp"

static void
PyModel_dealloc(PyModelObject *self)
{
    delete self->cpp_obj;

    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
PyModel_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyModelObject *self = (PyModelObject*)type->tp_alloc(type, 0);
    if (self) {
        self->cpp_obj = nullptr;
    }
    return (PyObject*)self;
}

static int
PyModel_init(PyModelObject *self, PyObject *args, PyObject *kwds)
{
    try {
        self->cpp_obj = new CModel();
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return -1;
    }
    return 0;
}

static PyObject * 
PyModel_forwardGA(PyModelObject *self, PyObject *arg){

    if (!PyObject_TypeCheck(arg, &PyArrayD1Type)) {
        PyErr_SetString(PyExc_TypeError, "expected ArrayD1");
        return nullptr;
    }
    PyArrayD1Object *x_obj = reinterpret_cast<PyArrayD1Object*>(arg);

    ArrayD1 cpp_obj;
    try {
        cpp_obj = self->cpp_obj->forwardGA(*x_obj->cpp_obj);
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }

    PyArrayD1Object* py_out =
        PyObject_New(PyArrayD1Object, &PyArrayD1Type);
    if (!py_out) {
        PyErr_NoMemory();
        return nullptr;
    }
    try {
        py_out->cpp_obj = new Array<double, 1>(std::move(cpp_obj));
    } catch (...) {
        Py_DECREF(py_out);         
        PyErr_NoMemory();
        return nullptr;
    }

    return reinterpret_cast<PyObject*>(py_out);

}

static PyObject*
PyModel_addLayer(PyModelObject *self, PyObject *args){
    int prev_size;
    int cur_size;

    if (!PyArg_ParseTuple(args, "ii", &prev_size, &cur_size)) {
        return nullptr;                                
    }

    //super inefficient I know. It's disgusting. I'm lazy, it's a sunny Sunday and I'm chilling outside on my laptop just got home from church trying to do some nice relaxing python binding I'll make it efficient later.
    Layer<double> layer = Layer<double>(prev_size, cur_size, false);
    
    try {
        self->cpp_obj->addLayer(layer);
    } catch (const std::exception& e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return nullptr;
    }

    Py_RETURN_NONE;    
}

static PyObject* PyModel_addReLU(PyModelObject *self, PyObject *Py_UNUSED){
    ActivationReLU<double> relu = ActivationReLU<double>();
    try{
        self->cpp_obj->addReLU(relu);
    }
    catch(const std::exception& e){
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return nullptr;
    }
    Py_RETURN_NONE;
}

static PyObject* PyModel_addSoftmax(PyModelObject *self, PyObject *Py_UNUSED){
    ActivationSoftMax<double> soft = ActivationSoftMax<double>();
    try{
        self->cpp_obj->addSoftmax(soft);
    }
    catch(const std::exception& e){
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return nullptr;
    }
    Py_RETURN_NONE;
}

static PyObject* PyModel_randomize(PyModelObject *self, PyObject *arg){
    double strength = PyFloat_AsDouble(arg);
    if (strength == -1.0 && PyErr_Occurred())
        return nullptr;

    try{
        self->cpp_obj->randomize(strength);
    }
    catch(const std::exception& e){
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return nullptr;
    }
    Py_RETURN_NONE;

}
static PyObject* PyModel_loadModel(PyModelObject *self, PyObject *arg){
    const char* path = PyUnicode_AsUTF8(arg);            
    if (!path) {                                      
        return NULL;                    
    }

    int rc;
    try {
        rc = self->cpp_obj->loadModel(path);
    } catch (const std::exception& e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }

    if (rc != 0) {                 
        PyErr_SetString(PyExc_RuntimeError, "model.loadModel() failed");
        return NULL;
    }

    Py_RETURN_NONE;
}
static PyObject* 
PyModel_saveModel(PyModelObject *self, PyObject *arg){
    const char* path = PyUnicode_AsUTF8(arg);            
    if (!path) {                                      
        return NULL;                    
    }

    try {
        self->cpp_obj->saveModel(path);
    } catch (const std::exception& e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }

    Py_RETURN_NONE;
}
        /*void addLayer(Layer<NumType>& layer);
        void addReLU(ActivationReLU<NumType>& relu);
        void addSoftmax(ActivationSoftMax<NumType>& soft);
        void randomize(NumType strength);
        
        // Model saves must have less than 5535 layers.
        void saveModel(const char *path);
        int loadModel(const char *path);*/



/*static PyObject * 
PyCCED_backward(PyModelObject *self, PyObject *args, PyObject *kwds){
    PyArrayD2Object *output_obj = NULL;  
    PyArrayI2Object *actual_obj = NULL;  

    static char *kwlist[] = { "output", "actual", NULL };

    if (!PyArg_ParseTupleAndKeywords(
            args, kwds,
            "O!O!",                   
            kwlist,
            &PyArrayD2Type, &output_obj,
            &PyArrayI2Type, &actual_obj))
    {
        return NULL;
    }

    PyObject *out_py = PyArrayD2Type.tp_new(&PyArrayD2Type, NULL, NULL);
    try {
        ArrayD2 grad_cpp = self->cpp_obj->backwardClass(*actual_obj->cpp_obj, *output_obj->cpp_obj);
        ((PyArrayD2Object *)out_py)->cpp_obj = new ArrayD2(std::move(grad_cpp));
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }

    return out_py;

}*/


PyMethodDef PyModel_methods[] = {
    {"forwardGA", (PyCFunction)PyModel_forwardGA, METH_O, "forwardGA(x)->output"},
    {"save_model", (PyCFunction)PyModel_saveModel, METH_O, "Saves a model to a file"},
    {"load_model", (PyCFunction)PyModel_loadModel, METH_O, "Loads a model from a file"},
    {"add_softmax", (PyCFunction)PyModel_addSoftmax, METH_NOARGS, "Adds a softmax to the model"},
    {"add_relu", (PyCFunction)PyModel_addReLU, METH_NOARGS, "Adds a relu to the model"},
    {"add_layer", (PyCFunction)PyModel_addLayer, METH_VARARGS, "Adds a layer to the model"},
    {"randomize", (PyCFunction)PyModel_randomize, METH_O, "Adds a different random number (-arg, +arg) to each weight"},
    {NULL, NULL, 0, NULL}
};

PyGetSetDef PyModel_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
};

PyTypeObject PyModelType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.Model",                  // tp_name
    sizeof(PyModelObject),           // tp_basicsize
    0,                                // tp_itemsize
    (destructor)PyModel_dealloc,     // tp_dealloc
    0,                                // tp_vectorcall_offset (or tp_print in older Python)
    0,                                // tp_getattr
    0,                                // tp_setattr
    0,                                // tp_reserved / tp_compare
    0,                                // tp_repr
    0,                                // tp_as_number
    0,                                // tp_as_sequence
    0,                                // tp_as_mapping
    0,                                // tp_hash 
    0,                                // tp_call
    0,                                // tp_str
    0,                                // tp_getattro
    0,                                // tp_setattro
    0,                                // tp_as_buffer
    Py_TPFLAGS_DEFAULT,              // tp_flags
    "Neural Network Model",          // tp_doc
    0,                                // tp_traverse
    0,                                // tp_clear
    0,                                // tp_richcompare
    0,                                // tp_weaklistoffset
    0,                                // tp_iter
    0,                                // tp_iternext
    PyModel_methods,                 // tp_methods
    0,                                // tp_members
    PyModel_getset,                  // tp_getset
    0,                                // tp_base
    0,                                // tp_dict
    0,                                // tp_descr_get
    0,                                // tp_descr_set
    0,                                // tp_dictoffset
    (initproc)PyModel_init,          // tp_init
    0,                                // tp_alloc
    PyModel_new                      // tp_new
};

PyObject*
py_breed_models(PyObject* , PyObject* args)
{
    PyModelObject* m1;
    PyModelObject* m2;
    double prop;

    if (!PyArg_ParseTuple(args, "O!O!d",
            &PyModelType, &m1,
            &PyModelType, &m2,
            &prop))
    {
        return nullptr;                              
    }

    Model<double>* cpp_new;
    try {
        cpp_new = breedModels(*m1->cpp_obj, *m2->cpp_obj, prop);
    } catch (const std::exception& e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return nullptr;
    }

    PyModelObject* py_new =
        PyObject_New(PyModelObject, &PyModelType);
    if (!py_new) {
        delete cpp_new;
        return PyErr_NoMemory();
    }
    py_new->cpp_obj = cpp_new;
    return reinterpret_cast<PyObject*>(py_new);
}

PyObject*
py_copy_model(PyObject*, PyObject* arg)
{
    PyModelObject* src;
    if (!PyObject_TypeCheck(arg, &PyModelType)) {
        PyErr_SetString(PyExc_TypeError, "expected Model object");
        return nullptr;
    }
    src = reinterpret_cast<PyModelObject*>(arg);

    Model<double>* cpp_new;
    try {
        cpp_new = copyModel(*src->cpp_obj);
    } catch (const std::exception& e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return nullptr;
    }

    PyModelObject* py_new =
        PyObject_New(PyModelObject, &PyModelType);
    if (!py_new) {
        delete cpp_new;
        return PyErr_NoMemory();
    }
    py_new->cpp_obj = cpp_new;
    return reinterpret_cast<PyObject*>(py_new);
}


#endif