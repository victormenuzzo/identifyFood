# identifyfood

Done by Victor Antonio Menuzzo and Paula Giovanna Rodrigues(gitlab.com/paula_portfolio)

### To run the superpixels identification file with mask (know the label of each superpixels):
```
python identificaSP.py --image [local and image name]
```
after --image write exactly the location of the image

### To run the feature extract file change these vectors(fundo, prato and alimentos) with the labels obtained:
```
python criaDados.py
```
remember to provide the name of the image inside the code

### To run the classifier file:
```
python classifica.py
```
remember to provide the name of the image(test image) inside the code
