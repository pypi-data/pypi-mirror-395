#ifndef NDCINIT_C
#define NDCINIT_C

#ifdef __cplusplus
extern "C" {
#endif

#include "ndarray.hpp"


// WARNING DOES NOT WORK IF YOU EVER ADD A TYPE OF DATA THAT IS NOT 4n BYTES n \in \Z_{>0}
ndarray* arrayCInit(size_t nd, u_int8_t dtype, size_t* shape){
    // If you're following a segfault here, chances are nd > len(shape). I can't really check that in this function easily.
    // Initialize dims
    size_t* dims;
    dims = (size_t*) malloc(nd * sizeof(size_t));

    size_t* strides;
    strides = (size_t*) malloc(nd * sizeof(size_t));


    size_t datalength = 0x0;
    if(dtype == 0x0 || dtype == 0x2){
        datalength = 0x4;
    }
    else if (dtype == 0x1 || dtype == 0x3){
        datalength = 0x8;
    }
    char* data;

    if(datalength == 0x0){
        fprintf(stderr, "65 dimensions is max!\n");
        exit(EXIT_FAILURE); 
    }

    size_t size = datalength;

    // Let's my LCV be a long, old numpy docs say max dims is 64 so I am one upping NumPy
    if(nd > 66){
        fprintf(stderr, "65 dimensions is max!\n");
        exit(EXIT_FAILURE); 
    }
    if(nd == 0){
        fprintf(stderr, "You wrote 0 dimensions!\n");
        exit(EXIT_FAILURE); 
    }
    // Initialize dims and strides
    for(long i = nd-1; i >= 0; i--){
        dims[i] = shape[i];
        strides[i] = size;
        size *= shape[i];
    }

    // If your fuzzer brought you here the bug is that even negative dimensions can pass this check. I don't want nd many checks.
    if(size <= 0){
        fprintf(stderr, "All dimensions must be positive!\n");
        exit(EXIT_FAILURE); 
    }    
    
    data = (char*) malloc(size * sizeof(char));

    /*ndarray obj = {nd, dims, strides, data, dtype};

    ndForeach(&obj, zero4);

    return obj;*/
    ndarray *obj = (ndarray *)ndarrayType.tp_alloc(&ndarrayType, 0);
    obj->nd = nd;
    obj->dims = dims;
    obj->strides = strides;
    obj->data = data;
    obj->dtype = dtype;
    size_t *refs = (size_t*) malloc(sizeof(size_t));
    // Don't think of refs as an array mentally, this is just so that a bad compiler wouldn't waste time putting an 8 byte 1 on the stack just to put it into refs because that would be ridiculuous
    refs[0] = 1;
    obj->refs = refs;
    obj->originaldata = data;
    if(dtype == 0x1 || dtype == 0x3){
        ndForeach(obj, zero8);
    }
    if(dtype == 0x0 || dtype == 0x2){
        ndForeach(obj, zero4);
    }
    return obj;
}

// WARNING DOES NOT WORK IF YOU EVER ADD A TYPE OF DATA THAT IS NOT 4n BYTES n \in \Z_{>0}
ndarray* arrayScalarCInit(void* value, u_int8_t dtype){
    
    size_t datalength = 0x0;
    if(dtype == 0x0 || dtype == 0x2){
        datalength = 0x4;
    }
    else if (dtype == 0x1 || dtype == 0x3){
        datalength = 0x8;
    }
    char* data;

    if(datalength == 0x0){
        fprintf(stderr, "65 dimensions is max!\n");
        exit(EXIT_FAILURE); 
    }

    size_t size = datalength;

    
    data = (char*) malloc(datalength * sizeof(char));

    /*ndarray obj = {nd, dims, strides, data, dtype};

    ndForeach(&obj, zero4);

    return obj;*/
    ndarray *obj = (ndarray *)ndarrayType.tp_alloc(&ndarrayType, 0);
    if (!obj) {
        // tp_alloc already set the Python error
        return NULL;
    }

    obj->nd = 0;
    obj->dims = nullptr;
    obj->strides = nullptr;
    obj->data = data;
    obj->dtype = dtype;
    size_t *refs = (size_t*) malloc(sizeof(size_t));
    // Don't think of refs as an array mentally, this is just so that a bad compiler wouldn't waste time putting an 8 byte 1 on the stack just to put it into refs because that would be ridiculuous
    refs[0] = 1;
    obj->refs = refs;
    obj->originaldata = data;
    if(dtype == 0x1 || dtype == 0x3){
        memcpy(obj->data, value, 8);
    }
    if(dtype == 0x0 || dtype == 0x2){
        memcpy(obj->data, value, 4);
    }

    return obj;
}


// WARNING DOES NOT WORK IF YOU EVER ADD A TYPE OF DATA THAT IS NOT 4n BYTES n \in \Z_{>0}
ndarray* arrayCViewCreate(ndarray* old){
    // If you're following a segfault here, chances are nd > len(shape). I can't really check that in this function easily.
    // Initialize dims
    size_t* dims;
    dims = (size_t*) malloc(old->nd * sizeof(size_t));

    size_t* strides;
    strides = (size_t*) malloc(old->nd * sizeof(size_t));



    for(long i = 0; i < old->nd; i++){
        dims[i] = old->dims[i];
        strides[i] = old->strides[i];
    }


    ndarray *obj = (ndarray *)ndarrayType.tp_alloc(&ndarrayType, 0);
    obj->nd = old->nd;
    obj->dims = dims;
    obj->strides = strides;
    obj->data = old->data;
    obj->dtype = old->dtype;
    
    // Don't think of refs as an array mentally, this is just so that a bad compiler wouldn't waste time putting an 8 byte 1 on the stack just to put it into refs because that would be ridiculuous
    old->refs[0] += 1;
    obj->refs = old->refs;
    obj->originaldata = old->originaldata;

    return obj;
}

// I'm fully aware memcopy is a simpler way to do this, but I'm afraid some compilers might not optimize it as efficiently as they could (and totally didn't just want to ctrl c + ctrl v). I'm hoping this library gets popular becuase there's like 2 years of quality comments in here, usually wrote while listening to kesha.
void copy(void* self, void* other, uint8_t dtype){

    if(dtype == 0x0){
        float* s = (float*)self;
        float* o = (float*) other;
        s[0] = o[0];
    }

    if(dtype == 0x1){
        double* s = (double*) self;
        double* o = (double*)other;
        s[0] = o[0];
    }

    if(dtype == 0x2){
        int32_t* s = (int32_t*)self;
        int32_t* o = (int32_t*) other;
        s[0] = o[0];
    }

    if(dtype == 0x3){
        int64_t* o = (int64_t*)other;
        int64_t* s = (int64_t*) self;
        s[0] = o[0];
    }

    return;
}

ndarray* arrayCInitCopy(ndarray* other){
    // If you're following a segfault here, chances are nd > len(shape). I can't really check that in this function easily.
    // Initialize dims
    size_t* dims;
    size_t* strides;

    if(other->nd > 0){
        dims = (size_t*) malloc(other->nd * sizeof(size_t));

        strides = (size_t*) malloc(other->nd * sizeof(size_t));
    }

    size_t datalength = 0x0;
    if(other->dtype == 0x0 || other->dtype == 0x2){
        datalength = 0x4;
    }
    else if (other->dtype == 0x1 || other->dtype == 0x3){
        datalength = 0x8;
    }
    char* data;

    if(datalength == 0x0){
        fprintf(stderr, "65 dimensions is max!\n");
        exit(EXIT_FAILURE); 
    }

    size_t size = datalength;

    // Let's my LCV be a long, old numpy docs say max dims is 64 so I am one upping NumPy
    if(other->nd > 66){
        fprintf(stderr, "65 dimensions is max!\n");
        exit(EXIT_FAILURE); 
    }
    // Initialize dims and strides
    for(long i = other->nd-1; i >= 0; i--){
        dims[i] = other->dims[i];
        strides[i] = size;
        size *= other->dims[i];
    }

    // If your fuzzer brought you here the bug is that even negative dimensions can pass this check. I don't want nd many checks.
    if(size <= 0){
        fprintf(stderr, "All dimensions must be positive!\n");
        exit(EXIT_FAILURE); 
    }    
    
    data = (char*) malloc(size * sizeof(char));

    /*ndarray obj = {nd, dims, strides, data, dtype};

    ndForeach(&obj, zero4);

    return obj;*/
    ndarray *obj = (ndarray *)ndarrayType.tp_alloc(&ndarrayType, 0);
    obj->nd = other->nd;
    obj->dims = dims;
    obj->strides = strides;
    obj->data = data;
    obj->dtype = other->dtype;
    size_t *refs = (size_t*) malloc(sizeof(size_t));
    // Don't think of refs as an array mentally, this is just so that a bad compiler wouldn't waste time putting an 8 byte 1 on the stack just to put it into refs because that would be ridiculuous
    refs[0] = 1;
    obj->refs = refs;
    obj->originaldata = data;
    ndForeachND(obj, other, copy);
    return obj;
}

#ifdef __cplusplus
}
#endif

#endif
