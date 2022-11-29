# L6

## Scope
1. Serving
2. API
3. SPA

## Tasks
1. **Models preparation**
  - save the models trained during [Lab 4](https://github.com/Large-scale-data-processing/l4-2019-base)

2. **API preparation**
  - option A:
    - create Flask (or other) APP
    - create a local spark context
    - load models
    - expose models using REST API
    - create inference methods
  - option B:
    - use a model serving tool (MLeap, ONNX)
    - if this tool does not support JSON or if it requires any transformations of the input data, add a simple REST API (e.g., using Flask) before it


3. **APP creation**
  - create appropriate GUI to enter data required for inference
  - consume exposed API
  - the GUI should reflect the inputs of the trained models, i.e., if you predict the subreddit based on the title and text of a post, the application should have two text inputs for these fields and a label that will contain the output of the model
  - option A: create a SPA app (using React, Angular, VUE, etc.)
  - option B: use Streamlit

4. **Deployment**
  - wrap all components into Kubernetes objects (as Helm templates)
  - deploy them into your cluster

Resources:
- [ONNX + raw](https://towardsdatascience.com/how-to-containerize-models-trained-in-spark-f7ed9265f5c9)
- [MLeap - StackOverflow](https://stackoverflow.com/a/49781272)
- [MLeap - Model serving](https://mleap-docs.combust.ml/mleap-serving/)
- [MLeap - PySpark](https://mleap-docs.combust.ml/py-spark/)
- [Streamlit](https://www.streamlit.io/)
