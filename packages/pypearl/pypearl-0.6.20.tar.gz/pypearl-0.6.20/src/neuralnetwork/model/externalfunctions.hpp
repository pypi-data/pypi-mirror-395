#ifndef MODELEXTERNALHPP
#define MODELEXTERNALHPP
#include "model.hpp"
#include "../layer/layer.hpp"

template <typename NumType>
Model<NumType>* breedModels(Model<NumType>& model1, Model<NumType>& model2, NumType prop);

template <typename NumType>
Model<NumType>* copyModel(Model<NumType>& models);

#include "externalfunctions.tpp"
#endif