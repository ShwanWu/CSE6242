1. Install tensorflow first
2. Follow https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md to install tensorflow object detection API.
3. Follow https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/running_pets.md and https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/running_locally.md to prepair data, train the model and evaluate the model.
4. Export the model by using the export_inference_graph.py
5. Get the result by running py -3 myrun.py >> result.csv