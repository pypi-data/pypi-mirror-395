#ifndef NDARRAY
#define NDARRAY

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <Python.h> 
#include <unicodeobject.h> 

/*
 * NDArray Object
 * 
 * The following is a class for NDArrays, used whenever arrays are needed to store data.
 * They support:
 * - Multiple datatypes (int, long, float, double)
 * - 0-65 dimensional tensors (0 being scalar)
 * - Linear Algebra
 */

/*
 * Editors Notes
 * 
 * This section was originally intended to be a small class to support the library but it is slowly turning into a sublibrary.
 * I'm not trying to replace NumPy, I just want my arrays to be internal for optimization purposes on O(n^3) functions.
 * 
 * I kinda couldn't decide between camal case and underscores for var names because I was simulataneously thinking in Python and C.
 * Also has anyone else ever noticed some words look better in camel case and some look better with underscore.
 * 
 * As useless as this may seem, being able to explain this array object got me through my last round on a data science interview so 
 * that's cool.
 */ 

/*
 * Data Types
 * 0x0: float32
 * 0x1: float64
 * 0x2: int32
 * 0x3: int64
 */

typedef struct {
    PyObject_HEAD
    // dimensions
    size_t nd;
    // shape owned by this view
    size_t* dims;
    // strides owned by this view
    size_t* strides;
    // first pointer references data shared
    char* data;
    // See comment above Data Types
    uint8_t dtype;
    // LENGTH 1 ARRAY/just a pointer to a long shared
    size_t* refs;
    // data for the first array shared
    char* originaldata;

} ndarray;

// func type functions
typedef void (*func)(void* elem, const size_t* idx, size_t nd);
typedef void (*funcED)(void* elem, uint8_t dtype, double val);
typedef void (*funcND2)(void* elem, void* other, uint8_t dtype);

void zero4(void* elem, const size_t* idx, size_t nd);
void zero8(void* elem, const size_t* idx, size_t nd);

void ndForeach(ndarray* arr, func visit);
void ndForeachED(ndarray* arr, funcED visit, double val);
void ndForeachND(ndarray* arr, ndarray* other, funcND2 visit);

void ndPrint(ndarray* arr);

// Python handling
static void ndarray_dealloc(ndarray *self);
static PyObject * ndarray_str(ndarray *self);
static PyObject * ndarray_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int ndarray_init(ndarray *self, PyObject *args, PyObject *kwds);
extern PyMethodDef ndarray_methods[];
extern PyGetSetDef ndarray_getset[];
extern PyTypeObject ndarrayType;

// C Functions
ndarray* arrayCInit(size_t nd, u_int8_t dtype, size_t* dims);
ndarray* arrayCInitCopy(ndarray* other);
ndarray* arrayScalarCInit(void* value, u_int8_t dtype);
ndarray* arrayCViewCreate(ndarray* old);
void ndincref(ndarray* self);
void nddecref(ndarray* self);
int arrayGetElement(ndarray arr, void* out, size_t* idx);
int arraySetElement(ndarray arr, void* in, size_t* idx);

void fastGet1D4Index(ndarray* arr, size_t pos, void* loc);
void fastGet1D8Index(ndarray* arr, size_t pos, void* loc);
void fastGet1DXIndex(ndarray* arr, size_t pos, void* loc, size_t byte_count);
void fastSet1D4Index(ndarray* arr, size_t pos, void* val);
void fastSet1D8Index(ndarray* arr, size_t pos, void* val);
void fastSet1DXIndex(ndarray* arr, size_t pos, void* val, size_t byte_count);

void fastGet2D4(ndarray* arr, size_t i, size_t j, void* out);
void fastGet2D8(ndarray* arr, size_t i, size_t j, void* out);
void fastSet2D4(ndarray* arr, size_t i, size_t j, void* in);
void fastSet2D8(ndarray* arr, size_t i, size_t j, void* in);
void fastScalar4(ndarray* arr, void* out);
void fastScalar8(ndarray* arr, void* out);
void fastIncInt32(ndarray arr, size_t i, size_t j, int32_t val);
void fastIncInt64(ndarray arr, size_t i, size_t j, void* out);
void printElemI32(void* elem, const size_t* idx, size_t nd);
void fastMove2D4(ndarray* in, size_t i, size_t j, ndarray* out, size_t i2, size_t j2);
void fastMove2D8(ndarray* in, size_t i, size_t j, ndarray* out, size_t i2, size_t j2);

void fastIncFloat32(ndarray* arr, size_t i, size_t j, float val);
void fastIncFloat64(ndarray* arr, size_t i, size_t j, double val);
void fastMultFloat32(ndarray* arr, size_t i, size_t j, float val);
void fastMultFloat64(ndarray* arr, size_t i, size_t j, double val);

ndarray* transpose(ndarray* self);
void GEMM(ndarray* A, ndarray* B, ndarray* C, ndarray* alpha, ndarray* beta);

// Math

void ndadd(void* data, uint8_t dtype, double val);
void ndsub(void* data, uint8_t dtype, double val);
void ndmult(void* data, uint8_t dtype, double val);
void nddiv(void* data, uint8_t dtype, double val);
void ndaddnd(void* data, void* other, uint8_t dtype);

static PyObject* PyNDArray_add(ndarray *self, PyObject *arg);
static PyObject* PyNDArray_sub(ndarray *self, PyObject *arg);
static PyObject* PyNDArray_mult(ndarray *self, PyObject *arg);
static PyObject* PyNDArray_div(ndarray *self, PyObject *arg);

// Python Functions
static PyObject* PyNDArray_shape(ndarray *self);
static ndarray* PyNDArray_transpose(ndarray *self, PyObject *arg);
static ndarray* PyNDArray_dot(ndarray *self, PyObject *arg);


#ifdef __cplusplus
}
#endif

#endif