## Docker image for training roleml model in 32 bits

Build (optional)  : 

```
docker build -t canisback/roleml_train_32 .
```

Run and extract the trained model in ./model : 
```
docker run -v $(pwd)/model:/app/model:Z canisback/roleml_train_32
```