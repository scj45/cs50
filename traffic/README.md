<!-- document (in at least a paragraph or two) your experimentation process. What did you try? What worked well? What didn’t work well? What did you notice? -->

<!-- ideas for experimentation
different numbers of convolutional and pooling layers
different numbers and sizes of filters for convolutional layers
different pool sizes for pooling layers
different numbers and sizes of hidden layers
dropout
-->

The original model had a speed of 3ms/step, 0.0547 accuracy and 3.5044 loss. Lowering the dropout to 0.3 from 0.5 only marginally increased accuracy to 0.0553 and decreased loss to 3.5044, again marginal. Changing the pool size to 3,3 had almost no effect on accuracy nor loss.

Increasing the number of units in the hidden layer to 512 made the most difference, bringing the accuracy up to 0.8978 and loss down to 0.5836. Although increasing the units even more to 768 brought the accuracy up to 0.9135, the loss increased to 0.6372 and the speed to 5ms/step.


In the end, lowering dropout to 0.0 kept the speed to 4ms/step but increased accuracy to 0.9280 and loss was decreased to 0.5262. Both 64 and 32 filters were tried. Using 32 filters meant that accuracy could reach 0.9331, while loss could get as low as 0.4296 at the speed of 3ms/step.
