#ifndef MODEL
#define MODEL

#include "model.hpp"
#include <bit>

#define handle

static std::uint16_t low16(size_t v)
{
    return static_cast<std::uint16_t>(v & 0xFFFFu);   
}

static std::uint32_t low32(size_t v)
{
    return static_cast<std::uint32_t>(v & 0xFFFFFFFFu);   
}

static std::uint16_t read16(const byte* data, size_t index){
    return static_cast<word>(static_cast<byte>(data[index])) | 
        (static_cast<word>(static_cast<byte>(data[index + 1])) << 8);
}

static std::uint32_t read32(const byte* data, size_t index){
    return static_cast<dword32>(static_cast<byte>(data[index])) | 
        (static_cast<dword32>(static_cast<byte>(data[index + 1])) << 8) |
        (static_cast<dword32>(static_cast<byte>(data[index + 2])) << 16) |
        (static_cast<dword32>(static_cast<byte>(data[index + 3])) << 24);
}

static std::uint64_t read64(const byte* data, size_t index){
    return static_cast<qword64>(static_cast<byte>(data[index])) | 
        (static_cast<qword64>(static_cast<byte>(data[index + 1])) << 8) |
        (static_cast<qword64>(static_cast<byte>(data[index + 2])) << 16) |
        (static_cast<qword64>(static_cast<byte>(data[index + 3])) << 24) |
        (static_cast<qword64>(static_cast<byte>(data[index + 4])) << 32) |
        (static_cast<qword64>(static_cast<byte>(data[index + 5])) << 40) |
        (static_cast<qword64>(static_cast<byte>(data[index + 6])) << 48) |
        (static_cast<qword64>(static_cast<byte>(data[index + 7])) << 56);

}



static void write32(std::vector<char>& output, dword32 bytes){
    output.push_back(static_cast<byte>(bytes & 0xFF));
    output.push_back(static_cast<byte>((bytes >> 8) & 0xFF));
    output.push_back(static_cast<byte>((bytes >> 16) & 0xFF));
    output.push_back(static_cast<byte>((bytes >> 24) & 0xFF));
}

static void write64(std::vector<char>& output, qword64 bytes){
    output.push_back(static_cast<byte>(bytes & 0xFF));
    output.push_back(static_cast<byte>((bytes >> 8) & 0xFF));
    output.push_back(static_cast<byte>((bytes >> 16) & 0xFF));
    output.push_back(static_cast<byte>((bytes >> 24) & 0xFF));

    output.push_back(static_cast<byte>((bytes >> 32) & 0xFF));
    output.push_back(static_cast<byte>((bytes >> 40) & 0xFF));
    output.push_back(static_cast<byte>((bytes >> 48) & 0xFF));
    output.push_back(static_cast<byte>((bytes >> 56) & 0xFF));

}


template <typename NumType>
Model<NumType>::Model()
{
    is64 = (sizeof(NumType) == 8);
}

template <typename NumType>
Model<NumType>::~Model()
{
    for(size_t i = 0; i < layers.size(); i++){
        delete layers[i];
    }
    layers.clear();
    
    for(size_t i = 0; i < activations.size(); i++){
        delete activations[i];
    }
    activations.clear();
}

template <typename NumType>
void Model<NumType>::addLayer(Layer<NumType>& layer)
{
    Layer<NumType>* layerNew = new Layer<NumType>(layer.weights.shape[0], layer.weights.shape[1], false);
    layerNew->deepcopy(&layer);
    layers.push_back(layerNew);
}



template <typename NumType>
void Model<NumType>::addReLU(ActivationReLU<NumType>& relu)
{
    ActivationReLU<NumType>* reluNew = new ActivationReLU<NumType>();
    activations.push_back(reluNew);
}

template <typename NumType>
void Model<NumType>::addSoftmax(ActivationSoftMax<NumType>& soft){
    ActivationSoftMax<NumType>* softNew = new ActivationSoftMax<NumType>();
    activations.push_back(softNew);
}

template <typename NumType>
Array<NumType, 2> Model<NumType>::forward(Array<NumType, 2> const& X)
{
    return Array<NumType, 2>();
}

template <typename NumType>
Array<NumType, 1> Model<NumType>::forwardRL(Array<NumType, 1> const& X)
{
    return Array<NumType, 1>();
}

template <typename NumType>
Array<NumType, 1> Model<NumType>::forwardGA(Array<NumType, 1> const& X)
{
    size_t l = layers.size();
    size_t a = activations.size();
    Array<NumType, 1> output = X;
    for(size_t i = 0; i < l; i++){
        output = layers[i]->forwardGA(output);
        if(i < a){
            output = activations[i]->forwardRL(output);
        }
    }
    return output;
}

template <typename NumType>
void Model<NumType>::saveModel(const char *path)
{
    /*
     * Model binary file:
     * {byte [0-1]: layer count, 65535 max layers. Becomes value nLayers, important for reading later}
     * {byte [2-nLayers): activation function description byte. could probably be 2 descriptions per byte but I don't want to think that much}
     * {byte [nLayers-maxlen): Weights. First 4 bytes: input size, then 4 bytes layer 1 size, then layer 1 weights. Note that a model of type float couldn't load a model of type doubles weights because of this.}
     */
    if(!path){
        fprintf(stderr, "Pass a valid path.");
        return;
    }
    const char *dot = strrchr(path, '.');
    bool ends = dot && strcmp(dot, ".aimodel") == 0;
    if(strlen(path)>190){
        fprintf(stderr, "Path name too short.");
        return;
    }
    char openpath[200];
    strcpy(openpath, path);
    if(!ends){
        strcat(openpath, ".aimodel");
    }
    FILE * outfile = fopen(openpath, "wb");
    if(!outfile){
        fprintf(stderr, "Failed to open an output file. Model save failed.");
        return;
    }
    std::vector<char> output;
    size_t nLayers = layers.size();
    // Unnecessary 8(?) bytes of condition and jump statement are going through your cpu because potential hackers mean we can't have nice things. Yes I entered 5535 correctly, it is completely arbitrary.
    if(nLayers > 5535){
        fprintf(stderr, "Model save failed, models must have less than 5535 layers.");
        return;
    }
    if(nLayers == 0){
        fprintf(stderr, "You must have layers to save a model");
        return;
    }
    // If your an actual engineer in need of more than 5535 layers please contact me brodymassad@gmail.com I'll update the repo same day.
    // GPT 4 has 120 layers so I don't think any computer at the time I'm writing this 2025 can even handle your model.
    if(is64){
        output.push_back(static_cast<byte>(0x01));
    }
    else{
        output.push_back(static_cast<byte>(0x00));
    }
    word layersize = low16(nLayers);
    output.push_back(static_cast<byte>(layersize & 0xFF)); 
    output.push_back(static_cast<byte>(layersize >> 8 & 0xFF)); 
    for(word i = 0; i < layersize ; i++){
        if (i < activations.size())
            output.push_back(activations[i]->type);
        else output.push_back(0x00);
    }
    dword32 prev_size = low32(layers[0]->weights.shape[0]);
    write32(output, prev_size);
    // Is it cleaner for the if to be inside the loop? Yes. Faster? No. #cleancodeisslowcode.
    if(is64){
        for(word i = 0; i < layersize; i++){
            dword32 cur_size = low32(layers[i]->weights.shape[1]);
            write32(output, cur_size);
            for(dword32 j = 0; j < prev_size; j++){
                for(dword32 k = 0; k < cur_size; k++){
                    double d = layers[i]->weights[j][k];
                    qword64 weight = std::bit_cast<qword64 >(d);
                    write64(output, weight);
                }
            }
            for(dword32 k = 0; k < cur_size; k++){
                double d = layers[i]->biases[k];
                qword64 bias = std::bit_cast<qword64 >(d);
                write64(output, bias);
            }
            prev_size = cur_size;
        }
    }
    else{
        for(word i = 0; i < layersize; i++){
            dword32 cur_size = low32(layers[i]->weights.shape[1]);
            write32(output, cur_size);
            for(dword32 j = 0; j < prev_size; j++){
                for(dword32 k = 0; k < cur_size; k++){
                    float f = layers[i]->weights[j][k];
                    dword32 weight = std::bit_cast<dword32 >(f);
                    write32(output, weight);
                }
            }
            for(dword32 k = 0; k < cur_size; k++){
                float f = layers[i]->biases[k];
                dword32 bias = std::bit_cast<dword32 >(f);
                write32(output, bias);
            }
            prev_size = cur_size;
        }
    }
    fwrite(output.data(), 1, output.size(), outfile);
    fclose(outfile);

}

template <typename NumType>
void Model<NumType>::addActivationByByte(byte act){
    switch (act){
        case 0x00:
            break;
        case 0x01: {
            ActivationReLU<NumType> * relu = new ActivationReLU<NumType>();
            activations.push_back(relu);
            break;
        }
        case 0x02: {
            ActivationSoftMax<NumType> * soft = new ActivationSoftMax<NumType>();
            activations.push_back(soft);
            break;
        }
        default:
            break;
    }
}

template <typename NumType>
int Model<NumType>::loadModel(const char *path)
{
    /*
     * Model binary file:
     * {byte [0-1]: layer count, 65535 max layers. Becomes value nLayers, important for reading later}
     * {byte [2-nLayers): activation function description byte. could probably be 2 descriptions per byte but I don't want to think that much}
     * {byte [nLayers-maxlen): Weights. First 4 bytes: input size, then 4 bytes layer 1 size, then layer 1 weights. Note that a model of type float couldn't load a model of type doubles weights because of this.}
     * I know this is a really simple way to do this but I felt cool because all the string compression theorems from theoretical CS class and turing machines.
     */
    if(!path){
        fprintf(stderr, "Pass a valid path.");
        return -1;
    }
    const char *dot = strrchr(path, '.');
    bool ends = dot && strcmp(dot, ".aimodel") == 0;
    if(strlen(path)>190){
        fprintf(stderr, "Path name too short.");
        return -1;
    }
    char openpath[200];
    strcpy(openpath, path);
    if(!ends){
        strcat(openpath, ".aimodel");
    }
    FILE * infile = fopen(openpath, "rb");
    if(!infile){
        fprintf(stderr, "Failed to open input file. Model creation failed.");
        return -1;
    }

    fseek(infile, 0, SEEK_END);
    size_t fsize = ftell(infile);
    rewind(infile);
    byte *data = static_cast<byte*>(std::malloc(fsize));
    fread(data, 1, fsize, infile);
    fclose(infile);
    if(data[0] != is64){
        fprintf(stderr, "Model is not the right shape");
        return -1;
    }
    
    layers.clear();
    activations.clear();
    size_t nLayers = read16(data, 1);
    for(size_t i = 3; i < nLayers+3; i++){
        addActivationByByte(static_cast<byte>(data[i]));
    }
    dword32 prev_size = read32(data, 3+nLayers);
    for(size_t i = 7+nLayers; i < fsize; ){
        dword32 cur_size = read32(data, i);
        i+=4;

        // I feel so paranoid writing this line below.
        // And there's totally gonna be some simple stack overflow in the strcpy up top or something.
        size_t totSize = ((size_t)cur_size)*((size_t)prev_size); 
        //std::cout << cur_size << " " << prev_size << std::endl;

        if(i+(totSize*sizeof(NumType)) > fsize){
            fprintf(stderr, "Corrupted aimodel file. If you don't think this is an error, send me your file.");
            return -1;
        }
        Layer<NumType>* layer = new Layer<NumType>(prev_size, cur_size, false);
        if(is64){
            for(dword32 j = 0; j < prev_size; j++){
                for(dword32 k = 0; k < cur_size; k++){
                    layer->weights[j][k] = std::bit_cast<double >(read64(data, i));
                    
                    i += sizeof(NumType);
                }
            }
            for(dword32 k = 0; k < cur_size; k++){
                layer->biases[k] = std::bit_cast<double >(read64(data, i));
                i+= sizeof(NumType);

            }

        }
        else{
            for(dword32 j = 0; j < prev_size; j++){
                for(dword32 k = 0; k < cur_size; k++){
                    layer->weights[j][k] = std::bit_cast<float >(read32(data, i));
                    
                    i += sizeof(NumType);
                }
            }
            for(dword32 k = 0; k < cur_size; k++){
                layer->biases[k] = std::bit_cast<float >(read32(data, i));
                i+= sizeof(NumType);

            }
        }
        layers.push_back(layer);
        prev_size = cur_size;
    }

    return 0;
}

template <typename NumType>
void Model<NumType>::randomize(NumType strength){
    size_t max = layers.size();
    for(size_t i = 0; i < max; i++){
        layers[i]->randomize(strength);
    }
}


#endif