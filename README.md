ad-hoc tool do not expect too much, enough for educational purposes

# Usage
### Export images from CIFAR10 to PNG
`python main.py --data data_batch_2.bin --mode 0`

### Merge png files from <folder> (must be in base directory) into file.bin
`python main.py --out file.bin --all <folder> --mode 1 `

### Export single image to CIFAR10
`python main.py --data image.png --out file.bin --mode 1 `

source: [Cifar-10 doc](https://www.cs.toronto.edu/~kriz/cifar.html) (binary version)
