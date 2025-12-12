#include "neuralnetwork.hpp"
#include "./activation/arbitraryactivation.hpp"
#include "../utilities/utilities.hpp"
#include <sanitizer/lsan_interface.h>


int main(){

    ActivationLayer<double> leakyrelu = {0x3, nullptr, nullptr, /*minimum*/2, nullptr, true, /*alpha*/0.3};

   /*int maxreps = 3;
    Model<double> model = Model<double>();
    Layer<double> l1 = Layer<double>(4, 1000, false);
    Layer<double> l2 = Layer<double>(1000, 1000, false);
    Layer<double> l3 = Layer<double>(1000, 2, false);
    ActivationLayer<double> relu = {0x1, nullptr, nullptr, 0, nullptr, true}; 
    ActivationLayer<double> relu2 = {0x1, nullptr, nullptr, 0, nullptr, true}; 
    ActivationLayer<double> soft = {0x2, nullptr, nullptr, 0, nullptr, true};

    ActivationReLU<double> r1 = ActivationReLU<double>();    
    ActivationReLU<double> r2 = ActivationReLU<double>();    
    ActivationSoftMax<double> r3 = ActivationSoftMax<double>();     
 
    LossCCE<double> loss = LossCCE<double>();
    OptimizerSGD<double> sgd = OptimizerSGD<double>(0.001);   
  
 
    std::random_device rd;    
    std::mt19937 gen(rd());
    std::uniform_real_distribution<double> dist(0.0, 1.0 );

    size_t s[2] = {100, 4};
    Array<double, 2> arr = Array<double, 2>(s);
    for(size_t i = 0; i < 100; i++){
        for(size_t j = 0; j < 4; j++){
            double r = dist(gen); 
            arr[i][j] = r;  // Replace with however you write to arr

        } 
    } 
    size_t d[2] = {100, 2}; 
    Array<int, 2> y = Array<int, 2>(d);
    for(size_t i = 0; i < 100; i++){ 
        y[i][0] = 1;
    } 

    double sum = 0.0f;
    Stopwatch watch;        
     
    for(int i = 0; i < maxreps; i++){   
        watch.reset();
        auto o1 = l1.forward(arr);
        auto a1 = r1.forward(o1, 1, 1);  

        auto o2 = l2.forward(a1); 
        auto a2 = r2.forward(o2, 1, 1); 
        std::cout << a2.toString() << std::endl;

        auto o3 = l3.forward(a2);     
        //std::cout << o3.toString() << std::endl;

        auto a3 = r3.forward(o3, 1, 1); 
        std::cout << a3.toString() << std::endl;
        auto l = loss.forwardClass(a3, 100, 2, y);
        auto b7 = loss.backwardClass(y, a3);

        auto b6 = r3.backward(loss.dvalues);
        auto b5 = l3.backward(b6);
        auto b4 = r2.backward(b5);
        auto b3 = l2.backward(b4);
        auto b2 = r1.backward(b3);
        auto b1 = l1.backward(b2);
        auto time = watch.elapsed(); 

        //sgd.optimize_layer(l3);
        //sgd.optimize_layer(l2);
        //sgd.optimize_layer(l1);
 
        auto t = watch.elapsed();
        std::cout << t << std::endl;
        sum += t;
    } 
        std::cout << "SWITCHING" << std::endl;
    double sum2 = 0.0f;
    for(int i = 0; i < maxreps; i++){   
        watch.reset();
        auto o12 = l1.forward(arr);
        auto a12 = activationForward<double>(&o12, relu2); 
        //std::cout << a1.toString() << std::endl;
        auto o22 = l2.forward(*a12); 
        auto a22 = activationForward<double>(&o22, relu); 
        std::cout << a22->toString() << std::endl;

        auto o32 = l3.forward(*a22);     
        //std::cout << o3.toString() << std::endl; 
        auto a32 = activationForward(&o32, soft);//r3.forward(o32, 1, 1); 
        std::cout << a32->toString() << std::endl;
        auto lv2 = loss.forwardClass(*a32, 100, 2, y);
        auto b72 = loss.backwardClass(y, *a32);

        //auto b62 = r3.backward(loss.dvalues); 
        auto b62 = activationBackward<double>(&loss.dvalues, soft);

        auto b52 = l3.backward(*b62);
        auto b42 = activationBackward<double>(&b52, relu);
        auto b32 = l2.backward(*b42);
        auto b22 = activationBackward<double>(&b32, relu2);
        auto b12 = l1.backward(*b22);
        auto timepassed = watch.elapsed(); 


        freeActivationLogits(soft);
        freeActivationLogits(relu);
        freeActivationLogits(relu2);
        
        //sgd.optimize_layer(l3);
        //sgd.optimize_layer(l2);
        //sgd.optimize_layer(l1);
 
        auto tpassed = watch.elapsed();
        std::cout << tpassed << std::endl;
        sum2 += tpassed;
    } 
    
    std::cout << "Sum 1: " << sum << "\nSum 2: " << sum2 << "\nRatio: " << sum/sum2 << std::endl;
    //std::cout << "Equality: " << checkEquality2D(*a32, a3) << "\n" << a32->toString() << "\n" << a3.toString() << std::endl;
    */
    return 0;   
}    