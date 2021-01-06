My base model consisted of the following:
* 1 Conv2D layer with 32 filters [relu]
* 1 MaxPooling2D with pool size (2,2)
* 1 Hidden Layer with 64 nodes w/ dropout of 0.1 [relu]
* 1 Output Layer [sigmoid]

Throughout my testing, I hoped to find a model that was not only accurate/loss-minimizing, but also had decent speed. First, I experimented with dropout. A higher dropout leads to lower training accuracy and greater loss. However, when I chose a low dropout like 0.1, I realized that the testing accuracy suffered. So I thought a 0.3 dropout kept a better balance between training and testing accuracy. Next, I experimented with pooling size, especially (3,3) vs. (2,2). I discovered that (3,3) pooling for the first Conv2D layer was much faster (from ~20s to ~11s per epoch), but it lowered accuracy too much, so I kept a (2,2) pool size. Later, I recalled that the lecture mentioned testing with multiple convolutions and poolings, so that is what I tried. At first, there was only slight improvement. Then I had the idea to make the second convolution layer more precise with 64 filters instead of 32. The run time increased somewhat, but the improvement far outweighed it. Finally, the last change that helped to improve my model's accuracy was increasing the number of nodes in the hidden layer from 64 to 512. Beyond 512, the improvement was neglible at the expense of run time. Overall, my final model has a testing accuracy that is >97% and averages ~19s per epoch in training. The activation functions used in the lecture worked well for this problem, so I decided not to change those.

Below is the final model that reflects my experimentation:
* 1 Conv2D layer with 32 filters [relu]
* 1 MaxPooling2D with pool size (2,2)
* 1 Conv2D layer with 64 filters [relu]
* 1 MaxPooling2D with pool size (2,2)
* 1 Hidden Layer with 512 nodes w/ dropout of 0.2 [relu]
* 1 Output Layer [sigmoid]