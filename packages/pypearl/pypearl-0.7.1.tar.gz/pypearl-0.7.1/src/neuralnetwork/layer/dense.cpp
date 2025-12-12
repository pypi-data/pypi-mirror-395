#ifndef DENSETPP
#define DENSETPP

#include "dense.hpp"

//#include <cblas.h>

//#include <arm_neon.h>

#include <chrono>
#include <random>

// I was getting deterministic weight init before this
inline auto make_seed() {
    std::random_device rd; 
    auto time = std::chrono::high_resolution_clock::now()
                    .time_since_epoch().count();

    std::seed_seq seq{ rd(),
                       static_cast<unsigned>(time & 0xFFFFFFFF),
                       static_cast<unsigned>(time >> 32) };
    std::mt19937 gen(seq); 
    return gen;
}

static void
dense_dealloc(dense *self)
{
    if(self->saved_inputs)
    Py_DECREF(self->saved_inputs);

    if(self->biases)
    Py_DECREF(self->biases);
    if(self->weights)
    Py_DECREF(self->weights);

    if(self->outputs)
    Py_DECREF(self->outputs);
    if(self->dinputs)
    Py_DECREF(self->dinputs);

    if(self->dbiases)
    Py_DECREF(self->dbiases);
    if(self->dweights)
    Py_DECREF(self->dweights);

}



static PyObject* dense_str(dense *self)
{
    _PyUnicodeWriter w; 
    _PyUnicodeWriter_Init(&w);
    w.min_length = 128;
    _PyUnicodeWriter_WriteASCIIString(&w, "Dense", 5);
    return _PyUnicodeWriter_Finish(&w);
}

static PyObject *
dense_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    (void)args;
    (void)kwds;
    dense *self = (dense*)type->tp_alloc(type, 0);
    if (self) {
        self->saved_inputs = nullptr;
        self->biases = nullptr;
        self->weights = nullptr;
        self->outputs = nullptr;
        self->dinputs = nullptr;
        self->dbiases = nullptr;
        self->dweights = nullptr;
    }

    return (PyObject*)self;

}

// Layer Forward Generic Compiler Invariant
ndarray* denseForwardGen(ndarray* inputs, dense& self){
    // put maxes on stack before loops.
    size_t i_max = inputs->dims[0]; // number of samples
    size_t j_max = self.biases->dims[0]; // number of outputs
    size_t k_max = inputs->dims[1]; // number of weights/input sample size

    size_t output_shape [2];
    output_shape[0] = i_max;
    output_shape[1] = j_max;

    auto dtype = self.dtype;

    if(inputs->dtype != self.dtype){
        PyErr_SetString(PyExc_TypeError, "Input array data type does not line up with regular datatype. I see no reason to support mixed precision dot products they're way too inefficient. I'll just make something to flip a network between float and double as a NEW OBJECT. But no line your types up.");
        return NULL;
    }
    ndarray* outputs = arrayCInit(2, dtype, output_shape);
    ndarray* saved_inputs = arrayCInit(2, dtype, inputs->dims);
    
    if(inputs->dtype == 0x0){
        for(size_t i = 0; i < inputs->dims[0]; i++){
            for(size_t j = 0; j < inputs->dims[1]; j++){
                fastMove2D4(inputs, i, j, saved_inputs, i, j);
            }
        }
        float inputval; // put input on stack
        float weightval; // put weight on stack
        float sum;
        for(size_t i = 0; i < i_max; i++){
            for(size_t j = 0; j < j_max; j++){
                fastGet1D4Index(self.biases, j, &sum);
                for(size_t k = 0; k < k_max; k++){
                    fastGet2D4(inputs, i, k, &inputval);
                    fastGet2D4(self.weights, j, k, &weightval);
                    sum += inputval*weightval;
                }
                fastSet2D4(outputs, i, j, &sum);
            }
        }
        
    }
    if(inputs->dtype == 0x1){
        double inputval; // put input on stack
        double weightval; // put weight on stack
        double sum;
        for(size_t i = 0; i < inputs->dims[0]; i++){
            for(size_t j = 0; j < inputs->dims[1]; j++){
                fastMove2D8(inputs, i, j, saved_inputs, i, j);
            }
        }

        for(size_t i = 0; i < i_max; i++){
            for(size_t j = 0; j < j_max; j++){
                fastGet1D8Index(self.biases, j, &sum);
                for(size_t k = 0; k < k_max; k++){
                    fastGet2D8(inputs, i, k, &inputval);
                    fastGet2D8(self.weights, j, k, &weightval);
                    sum += inputval*weightval;
                }
                fastSet2D8(outputs, i, j, &sum);
            }
        }
    }
    self.saved_inputs = saved_inputs;
    return outputs;

}

// Layer Forward Generic Compiler Invariant
ndarray* denseBackwardGen(ndarray* dval, dense& self){
    // put maxes on stack before loops.
    size_t i_max = dval->dims[0]; // number of samples
    size_t j_max = self.biases->dims[0]; // number of outputs
    size_t k_max = dval->dims[1]; // number of weights/input sample size

    size_t output_shape [2];
    output_shape[0] = i_max;
    output_shape[1] = j_max;

    auto dtype = self.dtype;

    if(dval->dtype != self.dtype){
        PyErr_SetString(PyExc_TypeError, "Input array data type does not line up with regular datatype. I see no reason to support mixed precision dot products they're way too inefficient. I'll just make something to flip a network between float and double as a NEW OBJECT. But no line your types up.");
        return NULL;
    }
    
    ndarray* dYT = transpose(dval);

    ndarray* dweights = arrayCInit(2, dtype, self.weights->dims);
    
    GEMM(dYT, self.saved_inputs, dweights, NULL, NULL);
    float temp;
    for(size_t i = 0; i < dweights->dims[0]; i++){
        for(size_t j = 0; j < dweights->dims[1]; j++){
            fastGet2D4(dweights, i, j, &temp);
            temp /= dval->dims[0];

            fastSet2D4(dweights, i, j, &temp);
        }
    }

    ndarray* dbiases = arrayCInit(1, dtype, self.biases->dims);

    float tmp;
    for (size_t j = 0; j < dbiases->dims[0]; j++) {
        float sum = 0.0f;
        for (size_t i = 0; i < dval->dims[0]; i++) {
            fastGet2D4(dval, i, j, &tmp);
            sum += tmp;
        }
        sum /= (float)dval->dims[0];
        fastSet1D4Index(dbiases, j, &sum); 
    }

    if(self.dweights){
        Py_DECREF((PyObject*)self.dweights);
    }
    if(self.dbiases){
        Py_DECREF((PyObject*)self.dbiases);
    }
    self.dweights = dweights;
    self.dbiases = dbiases;
    ndarray* wT = transpose(self.weights);

    size_t dX_shape [2];
    dX_shape[0] = self.saved_inputs->dims[0];
    dX_shape[1] = self.saved_inputs->dims[1];

    ndarray* dX = arrayCInit(2, dtype, dX_shape);

    GEMM(dval, self.weights, dX, NULL, NULL);


    return dX;
}

// Reimplement
ndarray* denseForwardARMMac(ndarray* inputs, dense& layer){
    /*size_t outputsShape[2] = {input.shape[0], biases.len};
    outputs = Array<NumType, 2>(outputsShape);
    size_t arr[2] = {input.shape[0], weights.shape[0]};
    inputSave = Array<NumType, 2>(arr);

    if(input.shape[1]!= weights.shape[0]){
        return Array<NumType, 2>();
    }

    double * weightsdata = weights.data;
    size_t weightsstride0 = weights.stride[0];
    double * inputdata = input.data;
    size_t sizes[2];
    sizes[1] = weights.shape[0];
    sizes[0] = weights.shape[1];
    Array<double, 2> weightsT = Array<double, 2>(sizes);
    for(size_t i = 0; i < sizes[0]; i++){
        for(size_t j = 0; j < sizes[1]; j++){
            weightsT.fastSet2D(i, j, weights.fastGet2D(j, i));
        }
    }

    size_t weightsshape0 = weights.shape[0];
    double * weightsTdata = weightsT.data;
    for(size_t k = 0; k < input.shape[0]; k++){                
        size_t input_inner = k*input.stride[0];
        double * curinputdata = &inputdata[input_inner];
        size_t inputSave_inner = k*inputSave.stride[0];
        size_t output_inner = k*outputs.stride[0];
        for(size_t i = 0; i < biases.len; i++){
            size_t output_loc = output_inner+i;
            size_t weights_outer = i*weightsT.stride[0];
            double * curweightsTdata = &weightsTdata[weights_outer];
            outputs.data[output_loc] = 0.0f;

            float64x2_t accs[6] = {vdupq_n_f64(0.0), vdupq_n_f64(0.0), 
            vdupq_n_f64(0.0), vdupq_n_f64(0.0), vdupq_n_f64(0.0), vdupq_n_f64(0.0)};

            // I forget why I did it this way but for some reason I think it mattered. I'm referring to j above loop.
            size_t j = 0;
            for(; j+11 < weightsshape0; j+=12){
                __builtin_prefetch(curweightsTdata + j + 64, 0, 1);
                __builtin_prefetch(curinputdata + j + 64, 0, 1);
                
                float64x2_t nextinputs1 = vld1q_f64(curinputdata+j);
                float64x2_t nextweights1 = vld1q_f64(curweightsTdata+j);
                accs[0] = vfmaq_f64(accs[0], nextinputs1, nextweights1);

                float64x2_t nextinputs2 = vld1q_f64(curinputdata + j +  2);
                float64x2_t nextweights2 = vld1q_f64(curweightsTdata + j +  2);
                accs[1] = vfmaq_f64(accs[1], nextinputs2, nextweights2);

                float64x2_t nextinputs3 = vld1q_f64(curinputdata + j +  4);
                float64x2_t nextweights3 = vld1q_f64(curweightsTdata + j +  4);
                accs[2] = vfmaq_f64(accs[2], nextinputs3, nextweights3);

                float64x2_t nextinputs4 = vld1q_f64(curinputdata + j +  6);
                float64x2_t nextweights4 = vld1q_f64(curweightsTdata + j +  6);
                accs[3] = vfmaq_f64(accs[3], nextinputs4, nextweights4);

                float64x2_t nextinputs5 = vld1q_f64(curinputdata + j +  8);
                float64x2_t nextweights5 = vld1q_f64(curweightsTdata + j +  8);
                accs[4] = vfmaq_f64(accs[4], nextinputs5, nextweights5);

                float64x2_t nextinputs6 = vld1q_f64(curinputdata + j +  10);
                float64x2_t nextweights6 = vld1q_f64(curweightsTdata + j +  10);
                accs[5] = vfmaq_f64(accs[5], nextinputs6, nextweights6);

            }
            for(; j < weights.shape[0]; j++){
                outputs.data[output_loc] += curinputdata[j] * curweightsTdata[j];
            }
            outputs.data[output_loc] += vaddvq_f64(accs[0]) +
                                        vaddvq_f64(accs[1]) +
                                        vaddvq_f64(accs[2]) +
                                        vaddvq_f64(accs[3]) + 
                                        vaddvq_f64(accs[4]) +
                                        vaddvq_f64(accs[5]);

            outputs.data[output_loc] +=  biases.data[i*biases.stride];
        }
    }
    for(size_t k = 0; k < input.shape[0]; k++){                
        size_t input_inner = k*input.stride[0];
        double * curinputdata = &inputdata[input_inner];
        size_t inputSave_inner = k*inputSave.stride[0];
        size_t output_inner = k*outputs.stride[0];

        for(size_t j = 0; j < weights.shape[0]; j++){
            inputSave.data[inputSave_inner+j] = input.data[input_inner+j];
        }
    }
    return outputs;*/
}

static ndarray* PyDense_forward(dense *self, PyObject *arg){

    static char *kwlist[] = { (char*)"x", NULL };
    if (!PyObject_TypeCheck(arg, &ndarrayType)) {
        PyErr_SetString(PyExc_TypeError, "dense forward() expects an ndarray");
        return NULL;
    }
    ndarray *input = (ndarray*)arg;
    try {
        ndarray *y = denseForwardGen(input, (*self));
        if(y){
            return y;
        }
        else{
            PyErr_SetString(PyExc_TypeError, "Forward Pass Error");
            return NULL;
        }
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }
}

static ndarray* PyDense_backward(dense *self, PyObject *arg){

    static char *kwlist[] = { (char*)"dval", NULL };
    if (!PyObject_TypeCheck(arg, &ndarrayType)) {
        PyErr_SetString(PyExc_TypeError, "layer forward() expects an ndarray");
        return NULL;
    }
    ndarray *dval = (ndarray*)arg;
    try {
        ndarray *y = denseBackwardGen(dval, (*self));
        if(y){
            return y;
        }
        else{
            PyErr_SetString(PyExc_TypeError, "Backward Pass Error");
            return NULL;
        }
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }
}

static ndarray* PyDense_weights(dense *self){
    if(!self->weights){
        PyErr_SetString(PyExc_TypeError, "Weights array null");
        return NULL;
    }
    ndarray *output = (ndarray*)self->weights;
    ndincref(output);
    try {
        return output;
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }
}

static ndarray* PyDense_biases(dense *self){
    if(!self->biases){
        PyErr_SetString(PyExc_TypeError, "Biases array null");
        return NULL;
    }
    ndarray *output = (ndarray*)self->biases;
    ndincref(output);
    try {
        return output;
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }
}

static ndarray* PyDense_dweights(dense *self){
    if(!self->dweights){
        PyErr_SetString(PyExc_TypeError, "dweights array null");
        return NULL;
    }
    ndarray *output = (ndarray*)self->dweights;
    ndincref(output);
    try {
        return output;
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }
}


static ndarray* PyDense_dbiases(dense *self){
    if(!self->dbiases){
        PyErr_SetString(PyExc_TypeError, "dbiases array null");
        return NULL;
    }
    ndarray *output = (ndarray*)self->dbiases;
    ndincref(output);
    try {
        return output;
    } catch (const std::exception &e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
        return NULL;
    }
}

PyMethodDef dense_methods[] = {
    {"forward", (PyCFunction)PyDense_forward, METH_O, "forward(x)->y"},
    {"backward", (PyCFunction)PyDense_backward, METH_O, "backward(dval)->dval"},
    {"weights", (PyCFunction)PyDense_weights, METH_NOARGS, "Return weights ndarray"},
    {"biases", (PyCFunction)PyDense_biases, METH_NOARGS, "Return biases ndarray"},
    {"dbiases", (PyCFunction)PyDense_dbiases, METH_NOARGS, "Return dbiases ndarray"},
    {"dweights", (PyCFunction)PyDense_dweights, METH_NOARGS, "Return dweights ndarray"},
    {NULL, NULL, 0, NULL}
};

PyGetSetDef dense_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
}; 

static int
dense_init(dense *self, PyObject *args, PyObject *kwds)
{
    // Considered PyTorch syntax here then I was like which one is actually  more intuitive, out_features or neurons? This is way easier.
    static char *kwlist[] = { (char*)"prev_layer_size", (char*)"neurons", (char*)"dtype", NULL };
    
    const char *dtypeStr = NULL;
    ssize_t prev_layer;
    ssize_t neurons;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "ii|z", kwlist, &prev_layer, &neurons, &dtypeStr))
        return -1;

    uint8_t dtype = 0x1;
    size_t datalength = 8;

    // Parse dType
    if(!dtypeStr){
        dtype = 0x1;
        datalength = 8;
    }
    else if(strcmp(dtypeStr, "float32") == 0){
        dtype = 0x0;
        datalength = 4;
    }
    else if(strcmp(dtypeStr, "double") == 0 || strcmp(dtypeStr, "float") == 0 || strcmp(dtypeStr, "float64") == 0){
        dtype = 0x1;
        datalength = 8;
    }
    else if(strcmp(dtypeStr, "int32") == 0){
        dtype = 0x2;
        datalength = 4;
    }
    else if(strcmp(dtypeStr, "long") == 0 || strcmp(dtypeStr, "int") == 0 || strcmp(dtypeStr, "int64") == 0){
        dtype = 0x3;
        datalength = 8;
    }

    
    size_t bias_shape [1];
    bias_shape[0] = neurons;
    size_t weight_shape [2];
    weight_shape[0] = neurons;
    weight_shape[1] = prev_layer;

    self->dtype = dtype;

    self->biases = arrayCInit(1, dtype, bias_shape);
    self->weights = arrayCInit(2, dtype, weight_shape);
    // everything else can stay null for now
    if(dtype == 0x0){
        std::uniform_real_distribution<float> dis(-sqrt(6.0f/(prev_layer+neurons)), sqrt(6.0f/(prev_layer+neurons)));
        auto gen = make_seed();
        float temp;
        for(ssize_t i = 0; i < neurons; i++){
            temp = 0.5f*dis(gen);
            fastSet1D4Index(self->biases, i, &temp);
        }
        for(ssize_t i = 0; i < neurons; i++){
            for(ssize_t j = 0; j < prev_layer; j++){
                temp = 0.5f*dis(gen);
                fastSet2D4(self->weights, i, j, &temp);
            }
        }
    }

    else if(dtype == 0x1){
        std::uniform_real_distribution<double> dis(-sqrt(6.0f/(prev_layer+neurons)), sqrt(6.0f/(prev_layer+neurons)));

        auto gen = make_seed();
        double temp;
        for(size_t i = 0; i < neurons; i++){
            temp = 0.5f*dis(gen);
            fastSet1D8Index(self->biases, i, &temp);
        }
        for(size_t i = 0; i < neurons; i++){
            for(size_t j = 0; j < prev_layer; j++){
                temp = 0.5f*dis(gen);
                fastSet2D8(self->weights, i, j, &temp);
            }
        }
    }

    else{
        return -1;
    }

    self->momentum = false;
    return 0;
    
}


PyTypeObject denseType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.Dense",               // tp_name
    sizeof(dense),                  // tp_basicsize
    0,                               // tp_itemsize
    (destructor)dense_dealloc,   // tp_dealloc
    0,                               // tp_vectorcall_offset / tp_print
    0,                               // tp_getattr
    0,                               // tp_setattr
    0,                               // tp_reserved / tp_compare
    (reprfunc)dense_str,         // tp_repr
    0,                               // tp_as_number
    0,                               // tp_as_sequence
    0,                               // tp_as_mapping
    0,                               // tp_hash
    0,                               // tp_call
    (reprfunc)dense_str,         // tp_str
    0,                               // tp_getattro
    0,                               // tp_setattro
    0,                               // tp_as_buffer
    Py_TPFLAGS_DEFAULT,              // tp_flags
    "Dense",              // tp_doc
    0,                               // tp_traverse
    0,                               // tp_clear
    0,                               // tp_richcompare
    0,                               // tp_weaklistoffset
    0,                               // tp_iter
    0,                               // tp_iternext
    dense_methods,               // tp_methods
    0,                               // tp_members
    dense_getset,                // tp_getset
    0,                               // tp_base
    0,                               // tp_dict
    0,                               // tp_descr_get
    0,                               // tp_descr_set
    0,                               // tp_dictoffset
    (initproc)dense_init,        // tp_init
    0,                               // tp_alloc
    dense_new                    // tp_new
};

/*
template <typename NumType>
Array<NumType, 2> Layer<NumType>::forward(Array<NumType, 2> const& input){
    size_t outputsShape[2] = {input.shape[0], biases.len};
    outputs = Array<NumType, 2>(outputsShape);
    size_t arr[2] = {input.shape[0], weights.shape[0]};
    inputSave = Array<NumType, 2>(arr);

    if(input.shape[1]!= weights.shape[0]){
        return Array<NumType, 2>();
    }
    /*Stopwatch w;
    size_t M = input.shape[0];
    size_t K = input.shape[1];
    size_t N = biases.len;        

    cblas_dgemm(CblasRowMajor,
                CblasNoTrans,       
                CblasTrans,        
                M, N, K,
                1.0,
                input.data,   K,   
                weights.data, K,   
                0.0,
                outputs.data, N);   
    auto gemmc = w.elapsed();
    std::cout << "BLAS: " <<  gemmc << std::endl;
    w.reset();
    double * weightsdata = weights.data;
    size_t weightsstride0 = weights.stride[0];
    double * inputdata = input.data;
    size_t sizes[2];
    sizes[1] = weights.shape[0];
    sizes[0] = weights.shape[1];
    Array<double, 2> weightsT = Array<double, 2>(sizes);
    for(size_t i = 0; i < sizes[0]; i++){
        for(size_t j = 0; j < sizes[1]; j++){
            weightsT.fastSet2D(i, j, weights.fastGet2D(j, i));
        }
    }
    //std::cout << weights.shape[0] << ", "<< weights.shape[1] << "\n" << weightsT.shape[0] << ", "<< weightsT.shape[1] << std::endl;
    size_t weightsshape0 = weights.shape[0];
    double * weightsTdata = weightsT.data;
    for(size_t k = 0; k < input.shape[0]; k++){                
        size_t input_inner = k*input.stride[0];
        double * curinputdata = &inputdata[input_inner];
        size_t inputSave_inner = k*inputSave.stride[0];
        size_t output_inner = k*outputs.stride[0];
        for(size_t i = 0; i < biases.len; i++){
            size_t output_loc = output_inner+i;
            size_t weights_outer = i*weightsT.stride[0];
            double * curweightsTdata = &weightsTdata[weights_outer];
            outputs.data[output_loc] = 0.0f;

            float64x2_t accs[6] = {vdupq_n_f64(0.0), vdupq_n_f64(0.0), 
            vdupq_n_f64(0.0), vdupq_n_f64(0.0), vdupq_n_f64(0.0), vdupq_n_f64(0.0)};

            //double accs[8] = {};

            size_t j = 0;
            for(; j+11 < weightsshape0; j+=12){
                //outputs.data[output_loc] += weights.data[j*weights.stride[0]+weights_outer];
                //(k, i, input.fastGet2D(k, j) * weights.fastGet2D(j, i));
                __builtin_prefetch(curweightsTdata + j + 64, 0, 1);
                __builtin_prefetch(curinputdata + j + 64, 0, 1);
                
                float64x2_t nextinputs1 = vld1q_f64(curinputdata+j);
                float64x2_t nextweights1 = vld1q_f64(curweightsTdata+j);
                accs[0] = vfmaq_f64(accs[0], nextinputs1, nextweights1);

                float64x2_t nextinputs2 = vld1q_f64(curinputdata + j +  2);
                float64x2_t nextweights2 = vld1q_f64(curweightsTdata + j +  2);
                accs[1] = vfmaq_f64(accs[1], nextinputs2, nextweights2);

                float64x2_t nextinputs3 = vld1q_f64(curinputdata + j +  4);
                float64x2_t nextweights3 = vld1q_f64(curweightsTdata + j +  4);
                accs[2] = vfmaq_f64(accs[2], nextinputs3, nextweights3);

                float64x2_t nextinputs4 = vld1q_f64(curinputdata + j +  6);
                float64x2_t nextweights4 = vld1q_f64(curweightsTdata + j +  6);
                accs[3] = vfmaq_f64(accs[3], nextinputs4, nextweights4);

                float64x2_t nextinputs5 = vld1q_f64(curinputdata + j +  8);
                float64x2_t nextweights5 = vld1q_f64(curweightsTdata + j +  8);
                accs[4] = vfmaq_f64(accs[4], nextinputs5, nextweights5);

                float64x2_t nextinputs6 = vld1q_f64(curinputdata + j +  10);
                float64x2_t nextweights6 = vld1q_f64(curweightsTdata + j +  10);
                accs[5] = vfmaq_f64(accs[5], nextinputs6, nextweights6);

                
                /*auto off = j+weights_outer;
                accs[0] += curinputdata[j] * weightsTdata[off];
                off++;
                accs[1] += curinputdata[ (j+1)] * weightsdata[off];
                off++;
                accs[2] += curinputdata[ (j+2)] * weightsdata[off];
                off ++;
                accs[3] += curinputdata[ (j+3)] * weightsdata[off];
                off ++;
                accs[4] += curinputdata[ (j+4)] * weightsdata[off];
                off ++;

                accs[5] += curinputdata[ (j+5)] * weightsdata[off];
                off ++;

                accs[6] += curinputdata[ (j+6)] * weightsdata[off];
                off ++;

                accs[7] += curinputdata[ (j+7)] * weightsdata[off];

                
                //fastSet2D(k, j, input.fastGet2D(k, j));
                
            }
            for(; j < weights.shape[0]; j++){
                outputs.data[output_loc] += curinputdata[j] * curweightsTdata[j];
            }

            outputs.data[output_loc] +=      vaddvq_f64(accs[0]) +
                                            vaddvq_f64(accs[1]) +
                                            vaddvq_f64(accs[2]) +
                                            vaddvq_f64(accs[3]) + vaddvq_f64(accs[4]) +
                                            vaddvq_f64(accs[5]);
            //outputs.data[output_loc] += accs[0] + accs[1] + accs[2] + accs[3] + accs[4] + accs[5] + accs[6] + accs[7];
            outputs.data[output_loc] +=  biases.data[i*biases.stride];

        }



    }
    //auto x = w.elapsed();
    //std::cout << "My Code: " << x << "\n" <<  "Blas is " << (x/gemmc)<<  "times faster than me"<< std::endl;

        for(size_t k = 0; k < input.shape[0]; k++){                
        size_t input_inner = k*input.stride[0];
        double * curinputdata = &inputdata[input_inner];
        size_t inputSave_inner = k*inputSave.stride[0];
        size_t output_inner = k*outputs.stride[0];


                for(size_t j = 0; j < weights.shape[0]; j++){
                inputSave.data[inputSave_inner+j] = input.data[input_inner+j];
                /*inputSave.data[inputSave_inner+(j+1)*inputSave.stride[1]] = input.data[input_inner+(j+1)*inputSave.stride[1]];
                inputSave.data[inputSave_inner+(j+2)*inputSave.stride[1]] = input.data[input_inner+(j+2)*inputSave.stride[1]];
                inputSave.data[inputSave_inner+(j+3)*inputSave.stride[1]] = input.data[input_inner+(j+3)*inputSave.stride[1]];
                inputSave.data[inputSave_inner+(j+4)*inputSave.stride[1]] = input.data[input_inner+(j+4)*inputSave.stride[1]];
                inputSave.data[inputSave_inner+(j+5)*inputSave.stride[1]] = input.data[input_inner+(j+5)*inputSave.stride[1]];
            }
            }/*
    size_t N = biases.len;
 size_t K = weightsshape0;

 for (size_t k = 0; k < input.shape[0]; ++k) {
    const double* curinputdata = inputdata + k * input.stride[0];
    size_t output_inner = k * outputs.stride[0];

    size_t i = 0;
    for (; i + 3 < N; i += 4) {
        float64x2_t acc0 = vdupq_n_f64(0.0);
        float64x2_t acc1 = vdupq_n_f64(0.0);
        float64x2_t acc2 = vdupq_n_f64(0.0);
        float64x2_t acc3 = vdupq_n_f64(0.0);

        const double* w0 = weightsTdata + (i+0)*K;
        const double* w1 = weightsTdata + (i+1)*K;
        const double* w2 = weightsTdata + (i+2)*K;
        const double* w3 = weightsTdata + (i+3)*K;

        size_t j = 0;
        for (; j + 1 < K; j += 2) {
            float64x2_t xv  = vld1q_f64(curinputdata + j);
            acc0 = vfmaq_f64(acc0, xv, vld1q_f64(w0 + j));
            acc1 = vfmaq_f64(acc1, xv, vld1q_f64(w1 + j));
            acc2 = vfmaq_f64(acc2, xv, vld1q_f64(w2 + j));
            acc3 = vfmaq_f64(acc3, xv, vld1q_f64(w3 + j));
        }

        double sum0 = vaddvq_f64(acc0);
        double sum1 = vaddvq_f64(acc1);
        double sum2 = vaddvq_f64(acc2);
        double sum3 = vaddvq_f64(acc3);

        for (; j < K; ++j) {
            double xj = curinputdata[j];
            sum0 += xj * w0[j];
            sum1 += xj * w1[j];
            sum2 += xj * w2[j];
            sum3 += xj * w3[j];
        }

        outputs.data[output_inner + i+0] = sum0 + biases.data[i+0];
        outputs.data[output_inner + i+1] = sum1 + biases.data[i+1];
        outputs.data[output_inner + i+2] = sum2 + biases.data[i+2];
        outputs.data[output_inner + i+3] = sum3 + biases.data[i+3];
    }

    // tail outputs
    for (; i < N; ++i) {
        double sum = 0.0;
        const double* w = weightsTdata + i*K;
        for (size_t j = 0; j < K; ++j)
            sum += curinputdata[j] * w[j];
        outputs.data[output_inner + i] = sum + biases.data[i];
    }
}

    return outputs;
}

template <typename NumType>
Array<NumType, 1> Layer<NumType>::forwardRL(Array<NumType, 1> const& input){
    auto* in = new Array<NumType, 1>(weights.shape[0]);
    auto* out = new Array<NumType, 1>(biases.len);

    for(int i = 0; i < in->len; i++){
        (*in)[i] = input[i];
    }
    for(int i = 0; i < biases.len; i++){
        (*out)[i] = biases[i];
        for(int j = 0; j < weights.shape[0]; j++){
            (*out)[i] += (*in)[j] * weights[j][i];
        }
    }
    inputsRL.push_back(in);
    outputsRL.push_back(out);
    return (*out); // FIX WHEN MOVE CONSTRUCTOR IS ADDED TO ARRAY CLASS I KNOW IT SHOULD ALREADY EXIST DON'T JUDGE ME
}

template <typename NumType>
Array<NumType, 1> Layer<NumType>::forwardGA(Array<NumType, 1> const& input){
    auto* in = new Array<NumType, 1>(weights.shape[0]);
    auto* out = new Array<NumType, 1>(biases.len);

    for(int i = 0; i < in->len; i++){
        (*in)[i] = input[i];
    }
    for(int i = 0; i < biases.len; i++){
        (*out)[i] = biases[i];
        for(int j = 0; j < weights.shape[0]; j++){
            (*out)[i] += (*in)[j] * weights[j][i];
        }
    }
    return (*out); // FIX WHEN MOVE CONSTRUCTOR IS ADDED TO ARRAY CLASS I KNOW IT SHOULD ALREADY EXIST DON'T JUDGE ME
}

template <typename NumType>
void Layer<NumType>::endEpisodeRL(){
    size_t epSize = inputsRL.size();
    size_t inArr[2] = {epSize, weights.shape[0]};
    inputSave = Array<NumType, 2>(inArr);
    size_t outArr[2] = {epSize, biases.len};
    outputs = Array<NumType, 2>(outArr);
    for(size_t i = 0; i < epSize; i++){
        for(size_t j = 0; j < weights.shape[0]; j++){
            inputSave[i][j] = (*inputsRL[i])[j];
        }
        for(size_t j = 0; j < biases.len; j++){
            outputs[i][j] = (*outputsRL[i])[j];
        }
        delete inputsRL[i];
        delete outputsRL[i];
    }
    inputsRL.clear();
    outputsRL.clear();
}

template <typename NumType>
Array<NumType, 2> Layer<NumType>::backward(Array<NumType, 2>& dvalues){
    dbiases = Array<NumType, 1>(biases.len);
    for(size_t j = 0; j < biases.len; j++){
            dbiases.data[j] = dvalues.data[dvalues.stride[1]*j];
    }

    for(size_t i = 1; i < dvalues.shape[0]; i++){ // colARowB
        for(size_t j = 0; j < weight_inner_size; j++){ // colB
            dbiases.data[j] += dvalues.data[i*dvalues.stride[0]+j*dvalues.stride[1]];
        }
    }


    size_t sizes[2] = {inputSave.shape[1], dvalues.shape[1]};
    dweights = Array<NumType, 2>(sizes);
    for(size_t i = 0; i < inputSave.shape[1]; i++){
        auto off = i*dweights.stride[0];
        for(size_t j = 0; j < dvalues.shape[1]; j++){
            dweights.data[off+j] = 0;
        }
    }

    /*for(size_t k = 0; k < inputSave.shape[0]; k++){
        auto inputSave_outer =  k*inputSave.stride[0];
        auto dvalues_outer = k*dvalues.stride[0];
        for(size_t j = 0; j < inputSave.shape[1]; j++){

            size_t inputSave_loc = inputSave_outer+j*inputSave.stride[1];
            size_t dweights_outer = j*dweights.stride[0];
            double accs[8] = {};
            for(size_t i = 0; i +7 < dvalues.shape[1]; i+=8){
                dweights.data[dweights_outer+i] += inputSave.data[inputSave_loc]* dvalues.data[dvalues_outer+i*dvalues.stride[1]];
            }
        }
    }
    size_t inF  = inputSave.shape[1];
    size_t outF = dvalues.shape[1];
    size_t B    = inputSave.shape[0];

    cblas_dgemm(
    CblasRowMajor, CblasTrans, CblasNoTrans,
    inF,               outF,     B,
    1.0,
    inputSave.data,   inputSave.stride[0],
    dvalues.data,     dvalues.stride[0],
    0.0,
    dweights.data,          dweights.stride[0]);

    //dweights = (inputSave.transpose()) * dvalues;

    //Stopwatch w;
    size_t sizes2[2] = {dvalues.shape[0], weights.shape[0]};
    auto dinputs = Array<NumType, 2>(sizes2);
    for(size_t i = 0; i < dvalues.shape[0]; i++){
        auto off = i*dinputs.stride[0];
        for(size_t j = 0; j < weights.shape[0]; j++){
            dinputs.data[off+j] = 0;
        }
    }
    const int B2 = dvalues.shape[0]; 
    const int O = dvalues.shape[1];  
    const int I = weights.shape[0]; 

    const int lda = dvalues.stride[0];   
    const int ldb = weights.stride[0];  
    const int ldc = dinputs.stride[0]; 

    cblas_dgemm(
        CblasRowMajor,   
        CblasNoTrans,   
        CblasTrans,  
        B2, 
        I, 
        O,   
        1.0, 
        dvalues.data,  lda, 
        weights.data, ldb, 
        0.0,     
        dinputs.data, ldc); 

    //auto r = dvalues * (weights.transpose());
    return dinputs;

}

template <typename NumType>
void Layer<NumType>::randomize(NumType strength){
    std::uniform_real_distribution<NumType> weightRandomizer(-strength, strength);
    for(size_t i = 0; i < weights.shape[0]; i++){
        for(size_t j = 0; j < weights.shape[1]; j++){
            weights[i][j] += weightRandomizer(gen);
            if(weights[i][j] > 1){
                weights[i][j] = 1;
            }
            else if(weights[i][j] < -1){
                weights[i][j] = -1;
            }

        }
    }
    for(size_t i = 0; i <biases.len; i++){
        biases[i] += weightRandomizer(gen);
        if(biases[i] > 1){
            biases[i] = 1;
        }
        else if (biases[i] < -1){
            biases[i] = -1;
        }
    }
}

template <typename NumType>
void Layer<NumType>::deepcopy(const Layer<NumType>* other){
    for(size_t i = 0; i < weights.shape[0]; i++){
        for(size_t j = 0; j < weights.shape[1]; j++){
            weights[i][j] = other->weights[i][j];
        }
    }
    for(size_t i = 0; i < biases.len; i++){
        biases[i] = other->biases[i];
    }
    return;
}
*/
#endif