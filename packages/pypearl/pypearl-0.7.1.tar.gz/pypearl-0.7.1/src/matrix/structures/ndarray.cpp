#ifndef NDARRAY_C
#define NDARRAY_C

#ifdef __cplusplus
extern "C" {
#endif

#include "ndarray.hpp"

#include "nditer.cpp"
#include "ndmath.cpp"
#include "ndlinalg.cpp"
#include "ndcinit.cpp"

/*inline void fastGet1D4(ndarray* arr, size_t pos, void* loc){
    memcpy(loc, arr->data+pos, 4);
}

inline void fastGet1D8(ndarray* arr, size_t pos, void* loc){
    memcpy(loc, arr->data+pos, 8);
}

inline void fastGet1DX(ndarray* arr, size_t pos, void* loc, size_t byte_count){
    memcpy(loc, arr->data+pos, byte_count);
}

inline void fastSet1D4(ndarray* arr, size_t pos, void* val){
    memcpy(arr->data+pos, val, 4);
}

inline void fastSet1D8(ndarray* arr, size_t pos, void* val){
    memcpy(arr->data+pos, val, 8);
}

inline void fastSet1DX(ndarray* arr, size_t pos, void* val, size_t byte_count){
    memcpy(arr->data+pos, val, byte_count);
}*/

void fastScalar4(ndarray* arr, void* out){
    memcpy(out, arr->data, 4);
}

void fastScalar8(ndarray* arr, void* out){
    memcpy(out, arr->data, 8);
}

void fastGet1D4Index(ndarray* arr, size_t pos, void* loc){
    memcpy(loc, arr->data+arr->strides[0]*pos, 4);
}

void fastGet1D8Index(ndarray* arr, size_t pos, void* loc){
    memcpy(loc, arr->data+arr->strides[0]*pos, 8);
}

void fastGet1DXIndex(ndarray* arr, size_t pos, void* loc, size_t byte_count){
    memcpy(loc, arr->data+arr->strides[0]*pos, byte_count);
}

void fastSet1D4Index(ndarray* arr, size_t pos, void* val){
    memcpy(arr->data+arr->strides[0]*pos, val, 4);
}

void fastSet1D8Index(ndarray* arr, size_t pos, void* val){
    memcpy(arr->data+arr->strides[0]*pos, val, 8);
}

inline void fastSet1DXIndex(ndarray* arr, size_t pos, void* val, size_t byte_count){
    memcpy(arr->data+arr->strides[0]*pos, val, byte_count);
}

void fastScalar4Index(ndarray* arr, void* out){
    memcpy(out, arr->data, 4);
}

void fastScalar8Index(ndarray* arr, void* out){
    memcpy(out, arr->data, 8);
}

double getDoubleFromPyObject(PyObject* value){
    return PyFloat_Check(value) ? PyFloat_AsDouble(value) : PyFloat_CheckExact(value) ? PyFloat_AsDouble(value) : PyNumber_Check(value) ? PyFloat_AsDouble(value) : (PyErr_SetString(PyExc_TypeError, "expected number"), (double)0);
}

inline PyObject* returnData1D(ndarray *arr, size_t pos){
    // F32
    if(arr->dtype == 0x0){
        float x;
        fastGet1D4(arr, pos, &x);
        return PyFloat_FromDouble((double) x);
    }
    // float64
    if(arr->dtype == 0x1){
        double x;
        fastGet1D8(arr, pos, &x);
        return PyFloat_FromDouble(x);
    }
    // int 32
    if(arr->dtype == 0x2){
        int32_t x;
        fastGet1D4(arr, pos, &x);
        return PyLong_FromLong((long) x);
    }
    // int 64
    if(arr->dtype == 0x3){
        int64_t x;
        fastGet1D8(arr, pos, &x);
        return PyLong_FromLongLong((long long) x);
    }
    return NULL;
}

inline int setData1D(ndarray *arr, size_t offset, PyObject *value){
        // F32
        if(arr->dtype == 0x0){
            double temp = getDoubleFromPyObject(value);
            float x = (float)temp;
            fastSet1D4(arr, offset, &x);
            return 0;
        }
        // float64
        if(arr->dtype == 0x1){
            double x = getDoubleFromPyObject(value);
            fastSet1D8(arr, offset, &x);
            return 0;
        }
        // int 32
        if(arr->dtype == 0x2){
            long long temp = PyLong_AsLongLong(value);
            int32_t x = (int32_t) temp;
            fastSet1D4(arr, offset, &x);
            return 0;
        }
        // int 64
        if(arr->dtype == 0x3){
            long long temp = PyLong_AsLongLong(value);
            int64_t x = (int64_t) temp;
            fastSet1D8(arr, offset, &x);
            return 0;
        }
        return -1;
}

inline PyObject* subarrayDM1(ndarray *arr, size_t offset){
    size_t nd = arr->nd-1;

    // New strides and dims because these can be copied O(nd) and are easier to keep separate for future changes like transposing
    size_t* dims;
    size_t* strides;
    
    dims = (size_t*) malloc(nd * sizeof(size_t));
    strides = (size_t*) malloc(nd * sizeof(size_t));

    memcpy(dims, arr->dims+1, sizeof(size_t)*nd);
    memcpy(strides, arr->strides+1, sizeof(size_t)*nd);
    
    ndarray *obj = (ndarray *)ndarrayType.tp_alloc(&ndarrayType, 0);

    

    obj->nd = nd;
    obj->dims = dims;
    obj->strides = strides;
    obj->data = arr->data+offset;
    obj->dtype = arr->dtype;
    obj->refs = arr->refs;
    obj->originaldata = arr->originaldata;
    obj->refs += 1;
    return (PyObject* )obj;
}

void zero4(void* elem, const size_t* idx, size_t nd){
    (void)nd;
    (void)idx;
    *(int32_t*)elem = 0x0;
}

void zero8(void* elem, const size_t* idx, size_t nd){
    (void)nd;
    (void)idx;
    *(int64_t*)elem = 0x0;
}

// Just use Py_INCREF, this is deprecated.
void ndincref(ndarray* self){
    Py_INCREF(self);
    return;
}

// Just use Py_DECREF, this is deprecated.
void nddecref(ndarray* self){
    Py_DECREF(self);
    return;
}

static void
ndarray_dealloc(ndarray *self)
{
    if(self->refs){
        size_t c = (*self->refs)-1;

        if(c<=0){
            free(self->originaldata);
            free(self->refs);
        }
        *self->refs = c;
    }
    free(self->strides);
    free(self->dims);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

inline PyObject* arrayElementToPyUnicode(ndarray* arr, size_t* idx){
    size_t pos = 0;
    for(size_t i = 0; i < arr->nd; i++){
        pos += arr->strides[i]*idx[i];
    }
    if(arr->dtype == 0x0){
        float f;
        memcpy(&f, arr->data + pos, sizeof f);
        PyObject *pyf = PyFloat_FromDouble((double)f);
        if (!pyf) return NULL;
        PyObject *s = PyObject_Str(pyf);
        Py_DECREF(pyf);

        return s;
    }
    if(arr->dtype == 0x1){
        double f;
        memcpy(&f, arr->data + pos, sizeof f);
        PyObject *pyf = PyFloat_FromDouble((double)f);
        if (!pyf) return NULL;
        PyObject *s = PyObject_Str(pyf);
        Py_DECREF(pyf);

        return s;
    }
    if(arr->dtype == 0x2){
        int32_t f;
        memcpy(&f, arr->data + pos, sizeof f);
        PyObject *pyf = PyLong_FromLong((long)f);
        if (!pyf) return NULL;
        PyObject *s = PyObject_Str(pyf);
        Py_DECREF(pyf);

        return s;
    }
    if(arr->dtype == 0x3){
        int64_t f;
        memcpy(&f, arr->data + pos, sizeof f);
        PyObject *pyf = PyLong_FromLongLong((long long)f);
        if (!pyf) return NULL;
        PyObject *s = PyObject_Str(pyf);
        Py_DECREF(pyf);

        return s;
    }

    return NULL;

}

// not super efficient because the syscalls and python are way so slower and it's only bound by nd bc print per sub array is capped at 6
static void recursiveprint(ndarray *arr, size_t* idx, size_t dim, _PyUnicodeWriter *w){
    
    _PyUnicodeWriter_WriteASCIIString(w, "[", 1);
    if(dim == arr->nd-1){
        _PyUnicodeWriter_WriteASCIIString(w, " ", 1);

        if(arr->dims[dim]<=6){
            for(size_t i = 0; i < arr->dims[dim]; i++){
                idx[dim] = i;
                PyObject *num = arrayElementToPyUnicode(arr, idx);
                _PyUnicodeWriter_WriteStr(w, num); Py_DECREF(num);
                _PyUnicodeWriter_WriteASCIIString(w, " ", 1);
            }
        }
        else{
            idx[dim] = 0;
            PyObject *num = arrayElementToPyUnicode(arr, idx);
            _PyUnicodeWriter_WriteStr(w, num); Py_DECREF(num);
            _PyUnicodeWriter_WriteASCIIString(w, " ", 1);

            idx[dim] = 1;
            num = arrayElementToPyUnicode(arr, idx);
            _PyUnicodeWriter_WriteStr(w, num); Py_DECREF(num);
            _PyUnicodeWriter_WriteASCIIString(w, " ", 1);

            idx[dim] = 2;
            num = arrayElementToPyUnicode(arr, idx);
            _PyUnicodeWriter_WriteStr(w, num); Py_DECREF(num);
            _PyUnicodeWriter_WriteASCIIString(w, " ", 1);

            _PyUnicodeWriter_WriteASCIIString(w, "...", 3);

            idx[dim] = arr->dims[dim]-3;
            num = arrayElementToPyUnicode(arr, idx);
            _PyUnicodeWriter_WriteStr(w, num); Py_DECREF(num);
            _PyUnicodeWriter_WriteASCIIString(w, " ", 1);

            idx[dim] -= 1;
            num = arrayElementToPyUnicode(arr, idx);
            _PyUnicodeWriter_WriteStr(w, num); Py_DECREF(num);
            _PyUnicodeWriter_WriteASCIIString(w, " ", 1);

            idx[dim] -= 1;
            num = arrayElementToPyUnicode(arr, idx);
            _PyUnicodeWriter_WriteStr(w, num); Py_DECREF(num);
            _PyUnicodeWriter_WriteASCIIString(w, " ", 1);
        }
    }
    else{
        if(arr->dims[dim]<=6){
            idx[dim] = 0;

            for(size_t i = 0; i < arr->dims[dim]; i++){
                recursiveprint(arr, idx, dim+1, w);
                idx[dim]+=1;
            }
        }
        else{
            idx[dim]=0;

            recursiveprint(arr, idx, dim+1, w);
            idx[dim]+=1;
            recursiveprint(arr, idx, dim+1, w);
            idx[dim]+=1;
            recursiveprint(arr, idx, dim+1, w);

            _PyUnicodeWriter_WriteASCIIString(w, "\n...\n", 5);

            idx[dim]=arr->dims[dim]-3;
            recursiveprint(arr, idx, dim+1, w);
            idx[dim]+=1;
            recursiveprint(arr, idx, dim+1, w);
            idx[dim]+=1;
            recursiveprint(arr, idx, dim+1, w);
        }

    }
    _PyUnicodeWriter_WriteASCIIString(w, "]", 1);
    if(dim != 0 && idx[dim-1] != arr->dims[dim-1]-1){
        _PyUnicodeWriter_WriteASCIIString(w, "\n", 1);
        if(dim != arr->nd-1){
            _PyUnicodeWriter_WriteASCIIString(w, "\n", 1);
        }
    }

}

static PyObject *
ndarray_str(ndarray *self)
{
    size_t* idx;
    idx = (size_t*)malloc(self->nd*sizeof(size_t));
    for(size_t i = 0; i < self->nd; i++){
        idx[i] = 0;
    }
    _PyUnicodeWriter w; 
    _PyUnicodeWriter_Init(&w);
    w.min_length = 128;
    if(self->nd == 0){
        PyObject* num = arrayElementToPyUnicode(self, NULL);
        _PyUnicodeWriter_WriteStr(&w, num); Py_DECREF(num);
        return _PyUnicodeWriter_Finish(&w);
    }
    recursiveprint(self, idx, 0, &w);
    _PyUnicodeWriter_WriteASCIIString(&w, ", shape(", 8);
    for(size_t i = 0; i < self->nd; i++){
        int64_t f;
        memcpy(&f, self->dims + i, sizeof f);
        PyObject *pyf = PyLong_FromLongLong((long long)f);
        if (!pyf) return NULL;
        PyObject *s = PyObject_Str(pyf);
        Py_DECREF(pyf);
        _PyUnicodeWriter_WriteStr(&w, s);
        Py_DECREF(s);
        if(i < self->nd-1){
            _PyUnicodeWriter_WriteASCIIString(&w, ", ", 2);
        }
        else{
            _PyUnicodeWriter_WriteASCIIString(&w, ")", 1);
        }
    }
    return _PyUnicodeWriter_Finish(&w);
}


static PyObject *
ndarray_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    (void)args;
    (void)kwds;
    ndarray *self = (ndarray*)type->tp_alloc(type, 0);
    if (self) {
        self->data = NULL;
        self->strides = NULL;
        self->dims = NULL;
        self->refs = NULL;
        self->originaldata = NULL;
    }

    return (PyObject*)self;

}

static int
ndarray_init(ndarray *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = { (char*)"shape", (char*)"zeros", (char*)"dtype", (char*) "scalar", NULL };
    
    PyObject *shape_obj = NULL;
    // 1 means zero everything, 0 means leave normal
    PyObject* PyZeros = Py_True;
    const char *dtypeStr = NULL;
    PyObject* scalar = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OOzO", kwlist, &shape_obj, &PyZeros, &dtypeStr, &scalar))
        return -1;

    if (!PyBool_Check(PyZeros)) {
        PyErr_SetString(PyExc_TypeError, "'zeros' must be a bool");
        return -1;
    }

    int zeros = (PyZeros == Py_True);
    size_t nd;
    size_t* dims;
    size_t* strides;

    uint8_t dtype = 0x1;
    size_t datalength = 8;

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

    if (shape_obj && shape_obj != Py_None) {

        if (!PySequence_Check(shape_obj)) {
            PyErr_SetString(PyExc_TypeError, "'shape' must be a sequence of positive integers");
            return -1;
        }
        PyObject *fast = PySequence_Fast(shape_obj, "shape must be a sequence");
        if (!fast) return -1;

        nd = PySequence_Fast_GET_SIZE(fast);
        if (nd <= 0) {
            Py_DECREF(fast);
            PyErr_SetString(PyExc_ValueError, "'shape' must be non-empty");
            return -1;
        }
        dims = (size_t*) malloc(nd * sizeof(size_t));

        strides = (size_t*) malloc(nd * sizeof(size_t));

        if (!dims) { Py_DECREF(fast); PyErr_NoMemory(); return -1; }
        size_t size = datalength;
        for (ssize_t i = (ssize_t)nd-1; i >= 0; i--) {

            PyObject *item = PySequence_Fast_GET_ITEM(fast, i);
            Py_ssize_t v = PyNumber_AsSsize_t(item, PyExc_OverflowError);
            if (v == -1 && PyErr_Occurred()) {
                return -1;  // conversion/overflow error already set
            }
            if (v < 0) {
                PyErr_SetString(PyExc_ValueError, "dimension must be non-negative");
                return -1;
            }
            dims[i] = (size_t)v;
            strides[i] = size;
            size *= dims[i];
        }
        Py_DECREF(fast);

        char* data;
        data = (char*) malloc(size * datalength * sizeof(char));
        
        size_t *refs = (size_t*) malloc(sizeof(size_t));
        // Don't think of refs as an array mentally, this is just so that a bad compiler wouldn't waste time putting an 8 byte 1 on the stack just to put it into refs because that would be ridiculuous
        refs[0] = 1;

        self->nd = nd;
        self->dims = dims;
        self->strides = strides;
        self->data = data;
        self->dtype = dtype;
        self->refs = refs;
        self->originaldata = data;

        if(zeros && (dtype == 0x1 || dtype == 0x3)){
            ndForeach(self, zero8);
        }
        if(zeros && (dtype == 0x0 || dtype == 0x2)){
            ndForeach(self, zero4);
        }
        return 0;
    }

    else if(scalar){
        char* data;
        data = (char*) malloc(datalength * sizeof(char));
        size_t nd = 0;
        size_t* dims = NULL;
        size_t* strides = NULL;
        char* originalData = data;
        size_t *refs = (size_t*) malloc(sizeof(size_t));
        // Don't think of refs as an array mentally, this is just so that a bad compiler wouldn't waste time putting an 8 byte 1 on the stack just to put it into refs because that would be ridiculuous
        refs[0] = 1;

        self->nd = 0;
        self->strides = strides;
        self->dims = dims;
        self->originaldata = originalData;
        self->data = data;
        self->refs = refs;
        self->dtype = dtype;
        
        if(self->dtype == 0x0){
            double temp = getDoubleFromPyObject(scalar);
            float x = (float)temp;
            fastSet1D4(self, 0, &x);
        }
        // float64
        if(self->dtype == 0x1){
            double x = getDoubleFromPyObject(scalar);
            fastSet1D8(self, 0, &x);
        }
        // int 32
        if(self->dtype == 0x2){
            long long temp = PyLong_AsLongLong(scalar);
            int32_t x = (int32_t) temp;
            fastSet1D4(self, 0, &x);
        }
        // int 64
        if(self->dtype == 0x3){
            long long temp = PyLong_AsLongLong(scalar);
            int64_t x = (int64_t) temp;
            fastSet1D8(self, 0, &x);
        }
        return 0;
    }
    return -1;
}

int arraySetElement(ndarray arr, void* in, size_t* idx){
    char* start_idx = arr.data;
    for(size_t i = 0; i < arr.nd; i++){
        if(idx[i] >= arr.dims[i]){
            return -1;
        }
        start_idx += idx[i]*arr.strides[i];
    }
    if(arr.dtype == 0x0 || arr.dtype == 0x2){
        memcpy(start_idx, in, 4);
        return 0;
    }
    else if(arr.dtype == 0x1 || arr.dtype == 0x3){
        memcpy(start_idx, in, 8);
        return 0;
    }

    else{
        return -1;
    }
}

int arrayGetElement(ndarray arr, void* out, size_t* idx){
    char* start_idx = arr.data;
    for(size_t i = 0; i < arr.nd; i++){
        if(idx[i] >= arr.dims[i]){
            return -1;
        }

        start_idx += idx[i]*arr.strides[i];
    }

    if(arr.dtype == 0x0 || arr.dtype == 0x2){
        memcpy(out, start_idx, 4);
        return 0;
    }
    else if(arr.dtype == 0x1 || arr.dtype == 0x3){
        memcpy(out, start_idx, 8);
        return 0;
    }

    else{
        return -1;
    }
}

// Unsafe fast get
void fastGet2D4(ndarray* arr, size_t i, size_t j, void* out){
    memcpy(out,arr->data+arr->strides[0]*i+arr->strides[1]*j, 4);
}

// Unsafe fast get
void fastGet2D8(ndarray* arr, size_t i, size_t j, void* out){
    memcpy(out, arr->data+arr->strides[0]*i+arr->strides[1]*j, 8);
}

// Unsafe fast get
void fastMove2D4(ndarray* in, size_t i, size_t j, ndarray* out, size_t i2, size_t j2){
    memcpy(out->data+out->strides[0]*i2+out->strides[1]*j2,in->data+in->strides[0]*i+in->strides[1]*j, 4);
}

// Unsafe fast move
void fastMove2D8(ndarray* in, size_t i, size_t j, ndarray* out, size_t i2, size_t j2){
    memcpy(out->data+out->strides[0]*i2+out->strides[1]*j2,in->data+in->strides[0]*i+in->strides[1]*j, 8);
}



// Unsafe fast set
void fastSet2D4(ndarray* arr, size_t i, size_t j, void* in){
    memcpy(arr->data+arr->strides[0]*i+arr->strides[1]*j, in, 4);
}

// Unsafe fast set
void fastSet2D8(ndarray* arr, size_t i, size_t j, void* in){
    memcpy(arr->data+arr->strides[0]*i+arr->strides[1]*j, in, 8);
}

// int32 fast inc
void fastIncInt32(ndarray arr, size_t i, size_t j, int32_t val){
    int32_t x = (*(int32_t*) (arr.data+arr.strides[0]*i+arr.strides[1]*j));
    x+=val;
    fastSet2D4(&arr, i, j, &x);
}

// Unsafe fast get
void fastIncInt64(ndarray arr, size_t i, size_t j, void* out){
    memcpy(out, arr.data+arr.strides[1]*i+arr.strides[0]*j, 8);
}

void fastIncFloat32(ndarray* arr, size_t i, size_t j, float val){
    float x = (*(float*) (arr->data+arr->strides[0]*i+arr->strides[1]*j));
    x+=val;
    fastSet2D4(arr, i, j, &x);
}

void fastIncFloat64(ndarray* arr, size_t i, size_t j, double val){
    double x = (*(double*) (arr->data+arr->strides[0]*i+arr->strides[1]*j));
    x+=val;
    fastSet2D8(arr, i, j, &x);
}

void fastMultFloat32(ndarray* arr, size_t i, size_t j, float val){
    float x = (*(float*) (arr->data+arr->strides[0]*i+arr->strides[1]*j));
    x*=val;
    fastSet2D4(arr, i, j, &x);
}

void fastMultFloat64(ndarray* arr, size_t i, size_t j, double val){
    double x = (*(double*) (arr->data+arr->strides[0]*i+arr->strides[1]*j));
    x*=val;
    fastSet2D8(arr, i, j, &x);
}


void printElemI32(void* elem, const size_t* idx, size_t nd){
    (void)idx;
    int32_t* val = (int32_t*) elem;
    printf("[");
    for(size_t i = 0; i < nd; i++){
        printf(" %lu ", idx[i]);
    }
    printf("]: %d\n", (*val));
}

void ndPrint(ndarray* arr){
    ndForeach(arr, printElemI32);
}

// Py Function Implementations


ndarray* transpose(ndarray* self){
    ndarray* output = arrayCViewCreate(self);
    if(output->nd == 0x2){
        size_t temp = output->dims[0];
        output->dims[0] = output->dims[1];
        output->dims[1] = temp;
        temp = output->strides[0];
        output->strides[0] = output->strides[1];
        output->strides[1] = temp;
    }
    return output;
}

// Py Function Wrappers

static ndarray* PyNDArray_dot(ndarray *self, PyObject *arg){

    if (!PyObject_TypeCheck(arg, &ndarrayType)) {
        PyErr_SetString(PyExc_TypeError, "layer forward() expects an ndarray");
        return NULL;
    }
    ndarray *B = (ndarray*)arg;

    size_t c_shape[2];
    c_shape[0] = self->dims[0];
    c_shape[1] = B->dims[1];
    ndarray *C = arrayCInit(2, self->dtype, c_shape);
    GEMM(self, B, C, NULL, NULL);
    return C;
}

static ndarray* PyNDArray_transpose(ndarray *self, PyObject *arg){

    if (!PyObject_TypeCheck(arg, &ndarrayType)) {
        PyErr_SetString(PyExc_TypeError, "layer forward() expects an ndarray");
        return NULL;
    }
    
    ndarray* newView = transpose(self);

    return newView;
}

static PyObject* PyNDArray_shape(ndarray *self){
    if(!self){
        PyErr_SetString(PyExc_TypeError, "null points don't have shape (This is probably an issue with the library).");
        return NULL;
    }
    if(!self->dims){
        PyErr_SetString(PyExc_TypeError, "Somehow your array doesn't have dims.");
        return NULL;
    }
    PyObject* output = PyTuple_New(self->nd);
    if (!output) {
        PyErr_SetString(PyExc_TypeError, "Python error allocated tuple for shape.");
        return NULL; 
    }

    for(size_t i = 0; i < self->nd; i++){
        PyTuple_SetItem(output, i, PyLong_FromLong(self->dims[i]));
    }

    return output;
}


PyMethodDef ndarray_methods[] = {
    /*{"get", (PyCFunction)PyArrayD1_get, METH_VARARGS,
     "get(index) -> float\n\n"
     "Return the element at position `index` (0-based)."},
     {"set", (PyCFunction)PyArrayD1_set, METH_VARARGS, "set(index)->float\n\n"
     "Change the element at position index"},*/
    {"shape", (PyCFunction)PyNDArray_shape, METH_NOARGS, "shape of array"},
    {"dot", (PyCFunction)PyNDArray_dot, METH_O, "A dot B"},
    {"transpose", (PyCFunction)PyNDArray_transpose, METH_O, "transposes an array"},
    {"add", (PyCFunction)PyNDArray_add, METH_O, "adds a number to an array"},
    {"sub", (PyCFunction)PyNDArray_sub, METH_O, "subtracts a number from an array"},
    {"mult", (PyCFunction)PyNDArray_mult, METH_O, "multiplies a number to an array"},
    {"div", (PyCFunction)PyNDArray_div, METH_O, "divides a number from an array"},
    {NULL, NULL, 0, NULL}
};

PyGetSetDef ndarray_getset[] = {
    {NULL, NULL, NULL, NULL, NULL}
}; 
static PyObject* ndarray_subscript(PyObject *self, PyObject *key){
    ndarray *arr = (ndarray *)self;
    if(PyTuple_Check(key)){
        size_t nd = (size_t)PyTuple_GET_SIZE(key);
        size_t pos = 0;
        for(size_t i = 0; i < nd; i++){
            PyObject* item = PyTuple_GET_ITEM(key, i);
            Py_ssize_t idx_temp = PyLong_AsSsize_t(item);
            size_t idx = (size_t)idx_temp;
            if(idx >= arr->dims[i]){
                PyErr_SetString(PyExc_TypeError, "index out of range");
                return NULL;
            }
            pos += arr->strides[i]*idx;
        }
        return returnData1D(arr, pos);
    }
    else if(PyLong_Check(key)){
        size_t offset = (size_t)PyLong_AsLong(key);
        if(arr->nd == 1){
            return returnData1D(arr, arr->strides[0]*offset);
        }
        // could just be an else as I have no plans to support scalars but if I change my mind I don't want to create a bug so we're adding like 2 unnecessary instructions but arr->nd should be in a reg so it's not that bad.
        else if(arr->nd > 1){
            return subarrayDM1(arr, arr->strides[0]*offset);
        }
    }

    PyErr_SetString(PyExc_TypeError, "index type not supported");
    return NULL;
}
static int ndarray_ass_subscript(PyObject *self, PyObject *key, PyObject *value){
    ndarray *arr = (ndarray *)self;
    if(PyTuple_Check(key)){
        size_t nd = (size_t)PyTuple_GET_SIZE(key);
        size_t pos = 0;
        for(size_t i = 0; i < nd; i++){
            PyObject* item = PyTuple_GET_ITEM(key, i);
            Py_ssize_t idx_temp = PyLong_AsSsize_t(item);
            size_t idx = (size_t)idx_temp;
            if(idx >= arr->dims[i]){
                PyErr_SetString(PyExc_TypeError, "index out of range");
                return -1;
            }
            pos += arr->strides[i]*idx;
        }
        // F32
        if(arr->dtype == 0x0){
            double temp = getDoubleFromPyObject(value);
            float x = (float)temp;
            fastSet1D4(arr, pos, &x);
            if (PyErr_Occurred()) {return -1;}
            return 0;
        }
        // float64
        if(arr->dtype == 0x1){
            double x = getDoubleFromPyObject(value);
            fastSet1D8(arr, pos, &x);
            if (PyErr_Occurred()) {return -1;}
            return 0;
        }
        // int 32
        if(arr->dtype == 0x2){
            long long temp = PyLong_AsLongLong(value);
            int32_t x = (int32_t) temp;
            fastSet1D4(arr, pos, &x);
            if (PyErr_Occurred()) {return -1;}
            return 0;
        }
        // int 64
        if(arr->dtype == 0x3){
            long long temp = PyLong_AsLongLong(value);
            int64_t x = (int64_t) temp;
            fastSet1D8(arr, pos, &x);
            if (PyErr_Occurred()) {return -1;}
            return 0;
        }
        return -1;
    }
    else if(PyLong_Check(key)){
        size_t offset = (size_t)PyLong_AsLong(key);
        if(arr->nd == 1){
            setData1D(arr, arr->strides[0]*offset, value);
            return 0;
        }
        // could just be an else as I have no plans to support scalars but if I change my mind I don't want to create a bug so we're adding like 2 unnecessary instructions but arr->nd should be in a reg so it's not that bad.
        else if(arr->nd > 1){
            PyErr_SetString(PyExc_TypeError, "I agree a partial array copy should exist but it doesn't at the moment just because it would take like half an hour to make. If it's causing you an issue send me an email brodymassad@gmail.com and I'll try to push it ASAP. For now just replace element wise with a loop (sorry).");
            return -1;
            //return subarrayDM1(arr, arr->strides[0]*offset);
        }
    }

    PyErr_SetString(PyExc_TypeError, "index type not supported");
    return -1;
}

static Py_ssize_t ndarray_mp_length(PyObject *self_obj) {
    ndarray *self = (ndarray*)self_obj;
    return (Py_ssize_t)(self->dims[0]);
}

static PyMappingMethods ndarray_as_mapping = {
    .mp_length        = ndarray_mp_length,
    .mp_subscript     = ndarray_subscript,
    .mp_ass_subscript = ndarray_ass_subscript,
};

static PyNumberMethods ndarray_as_number = {
    /* nb_add */                  PyNDArray_add_new,        // a + b
    /* nb_subtract */             PyNDArray_sub_new,   // a - b
    /* nb_multiply */             PyNDArray_mult_new,   // a * b
    /* nb_remainder */            0,                  // a % b
    /* nb_divmod */               0,                  // divmod(a, b)
    /* nb_power */                0,                  // a ** b
    /* nb_negative */             0,   // -a
    /* nb_positive */             0,                  // +a
    /* nb_absolute */             0,                  // abs(a)
    /* nb_bool */                 0,                  // bool(a)
    /* nb_invert */               0,                  // ~a
    /* nb_lshift */               0,                  // a << b
    /* nb_rshift */               0,                  // a >> b
    /* nb_and */                  0,                  // a & b
    /* nb_xor */                  0,                  // a ^ b
    /* nb_or */                   0,                  // a | b
    /* nb_int */                  0,                  // int(a) / __int__
    /* nb_reserved */             0,                  // reserved / legacy
    /* nb_float */                0,                  // float(a) / __float__

    /* nb_inplace_add */          PyNDArray_add,       // a += b
    /* nb_inplace_subtract */     PyNDArray_sub,       // a -= b
    /* nb_inplace_multiply */     PyNDArray_mult,       // a *= b
    /* nb_inplace_remainder */    0,                  // a %= b
    /* nb_inplace_power */        0,                  // a **= b
    /* nb_inplace_lshift */       0,                  // a <<= b
    /* nb_inplace_rshift */       0,                  // a >>= b
    /* nb_inplace_and */          0,                  // a &= b
    /* nb_inplace_xor */          0,                  // a ^= b
    /* nb_inplace_or */           0,                  // a |= b

    /* nb_floor_divide */         0,                  // a // b
    /* nb_true_divide */          PyNDArray_div_new,    // a / b
    /* nb_inplace_floor_divide */ 0,                  // a //= b
    /* nb_inplace_true_divide */  PyNDArray_div,   // a /= b

    /* nb_index */                0,                  // a.__index__()

    /* nb_matrix_multiply */      0,                  // a @ b
    /* nb_inplace_matrix_multiply */ 0                // a @= b
};

PyTypeObject ndarrayType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pypearl.ndarray",               // tp_name
    sizeof(ndarray),         // tp_basicsize
    0,                               // tp_itemsize
    (destructor)ndarray_dealloc,   // tp_dealloc
    0,                               // tp_vectorcall_offset / tp_print
    0,                               // tp_getattr
    0,                               // tp_setattr
    0,                               // tp_reserved / tp_compare
    (reprfunc)ndarray_str,         // tp_repr
    &ndarray_as_number,                               // tp_as_number
    0,                               // tp_as_sequence
    &ndarray_as_mapping,                               // tp_as_mapping
    0,                               // tp_hash
    0,                               // tp_call
    (reprfunc)ndarray_str,         // tp_str
    0,                               // tp_getattro
    0,                               // tp_setattro
    0,                               // tp_as_buffer
    Py_TPFLAGS_DEFAULT,              // tp_flags
    "nD Array",              // tp_doc
    0,                               // tp_traverse
    0,                               // tp_clear
    0,                               // tp_richcompare
    0,                               // tp_weaklistoffset
    0,                               // tp_iter
    0,                               // tp_iternext
    ndarray_methods,               // tp_methods
    0,                               // tp_members
    ndarray_getset,                // tp_getset
    0,                               // tp_base
    0,                               // tp_dict
    0,                               // tp_descr_get
    0,                               // tp_descr_set
    0,                               // tp_dictoffset
    (initproc)ndarray_init,        // tp_init
    0,                               // tp_alloc
    ndarray_new                    // tp_new
};

#ifdef __cplusplus
}
#endif

#endif

//python3 setup.py clean --all
///opt/homebrew/bin/python3 setup.py build_ext --inplace -v
// python3 test.py  