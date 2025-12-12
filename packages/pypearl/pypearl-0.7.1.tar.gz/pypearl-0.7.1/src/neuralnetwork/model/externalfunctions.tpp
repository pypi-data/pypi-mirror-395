#ifndef MODELEXTERNAL
#define MODELEXTERNAL

#include "externalfunctions.hpp"

template <typename NumType>
Model<NumType>* breedModels(Model<NumType>& model1, Model<NumType>& model2, NumType prop){
    Model<NumType> *model = new Model<NumType>();

    static thread_local std::mt19937 gen{ std::random_device{}() };

    std::uniform_real_distribution<NumType> dist(static_cast<NumType>(0), static_cast<NumType>(1));

    for(size_t i = 0; i < model1.layers.size(); i++){
        model->addLayer((*model1.layers[i]));
        for(size_t j = 0; j < model1.layers[i]->weights.shape[0]; j++){
            for(size_t k = 0; k < model1.layers[i]->weights.shape[1]; k++){
                if(dist(gen) > prop){
                    model->layers[i]->weights[j][k] = model1.layers[i]->weights[j][k];
                }
                else{
                    model->layers[i]->weights[j][k] = model2.layers[i]->weights[j][k];
                }
            }
        }
        for(size_t j = 0; j < model1.layers[i]->biases.len; j++){
                if(dist(gen) > prop){
                    model->layers[i]->biases[j] = model1.layers[i]->biases[j];
                }
                else{
                    model->layers[i]->biases[j] = model2.layers[i]->biases[j];
                }
        }
        if(i < model1.activations.size()){
            model->addActivationByByte((model1.activations[i]->type));
        }
    }

    return model;
}

template <typename NumType>
Model<NumType>* copyModel(Model<NumType>& model){
    Model<NumType> *cmodel = new Model<NumType>();
    size_t max = model.layers.size();
    for(size_t i = 0; i < max; i++){
        Layer<NumType> *layer = new Layer<NumType>(model.layers[i]->weights.shape[0], model.layers[i]->weights.shape[1], false);
        layer->deepcopy(model.layers[i]);
        cmodel->addLayer((*layer));
    }
    size_t maxa = model.activations.size();
    for(size_t i = 0; i < maxa; i++){
        cmodel->addActivationByByte(model.activations[i]->type);
    }

    return cmodel;
}


#endif