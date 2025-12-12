#ifndef MODELHPP
#define MODELHPP

#include <stdio.h>
#include "../layer/layer.hpp"
#include "../activation/reluactivation.hpp"
#include "../activation/softmaxactivation.hpp"
#include <stdint.h>

typedef uint8_t byte;
typedef uint16_t word;
typedef uint32_t dword32;
typedef uint64_t qword64;



template <typename NumType = float>
class Model
{
    private:
        bool is64;
        using LayerT = Layer<NumType>;
        using ActT   = BaseActivation<NumType>;


        

    public:
        std::vector<LayerT* > layers;       
        std::vector<ActT* >   activations; 

        Model();
        ~Model();
        void addLayer(Layer<NumType>& layer);
        void addReLU(ActivationReLU<NumType>& relu);
        void addSoftmax(ActivationSoftMax<NumType>& soft);

        void addActivationByByte(byte act);

        Array<NumType, 2> forward(Array<NumType, 2> const& X);
        Array<NumType, 1> forwardRL(Array<NumType, 1> const& X);
        Array<NumType, 1> forwardGA(Array<NumType, 1> const& X);
        void randomize(NumType strength);
        
        // Model saves must have less than 5535 layers.
        void saveModel(const char *path);
        int loadModel(const char *path);

};

static std::uint16_t low16(size_t v);
static std::uint32_t low32(size_t v);
static std::uint16_t read16(const byte* data, size_t index);
static std::uint32_t read32(const byte* data, size_t index);
static std::uint64_t read64(const byte* data, size_t index);
static void write32(std::vector<char>& output, dword32 bytes);
static void write64(std::vector<char>& output, qword64 bytes);

#include "model.tpp"

#endif