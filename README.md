# Neural-fonts - GAN을 활용한 한글 폰트 제작 프로젝트

<p align="center">
  <img src="assets/NanumBrush-gen15.png">
</p>

GAN을 사용하여 한글 폰트를 자동으로 만들어 주는 프로젝트입니다. 

디자이너가 399자만 만들면 딥러닝을 통해서 해당 폰트의 style 정보를 훈련하여 11,172자의 완성형 한글을 생성합니다.

중국 폰트를 생성하는 [zi2zi](https://github.com/kaonashi-tyc/zi2zi)를 한글에 맞게 수정하여 사용하였습니다.

## Gallery
### 필기체 (나눔 붓 폰트)
Original         | Generated
|-------------------------|-------------------------|
![NanumBrush Original](assets/NanumBrush-org15.png) | ![NanumBrush Generated](assets/NanumBrush-gen15.png)  

### 고딕체 (푸른전남 폰트)
Original         | Generated
|-------------------------|-------------------------|
![PureunJeonnam Original](assets/Pureun-org15.png) | ![PureunJeonnam Generated](assets/Pureun-gen15.png) 

## 사용법
### Requirement
* Python 2.7
* CUDA
* cudnn
* Tensorflow >= 1.0.1
* Pillow(PIL)
* numpy >= 1.12.1
* scipy >= 0.18.1
* imageio

### Preprocess
To avoid IO bottleneck, preprocessing is necessary to pickle your data into binary and persist in memory during training.

First run the below command to get the font images:

```sh
python font2img.py --src_font=src.ttf
                   --dst_font=tgt.otf
                   --sample_count=1000
                   --sample_dir=dir
                   --label=0
                   --filter=1
                   --fixed_sample=1
```
Use fixed_sample option to select 399 characters 
Four default charsets are offered: CN, CN_T(traditional), JP, KR. You can also point it to a one line file, it will generate the images of the characters in it. Note, **filter** option is highly recommended, it will pre sample some characters and filter all the images that have the same hash, usually indicating that character is missing. **label** indicating index in the category embeddings that this font associated with, default to 0.

After obtaining all images, run **package.py** to pickle the images and their corresponding labels into binary format:

```sh
python package.py --dir=image_directories
                  --save_dir=binary_save_directory
                  --split_ratio=[0,1]
```

After running this, you will find two objects **train.obj** and **val.obj** under the save_dir for training and validation, respectively.

### Experiment Layout
```sh
experiment/
└── data
    ├── train.obj
    └── val.obj
```
Create a **experiment** directory under the root of the project, and a data directory within it to place the two binaries. Assuming a directory layout enforce bettet data isolation, especially if you have multiple experiments running.
### Train
To start training run the following command

```sh
python train.py --experiment_dir=experiment 
                --experiment_id=0
                --batch_size=16 
                --lr=0.001
                --epoch=40 
                --sample_steps=50 
                --schedule=20 
                --L1_penalty=100 
                --Lconst_penalty=15
```
**schedule** here means in between how many epochs, the learning rate will decay by half. The train command will create **sample,logs,checkpoint** directory under **experiment_dir** if non-existed, where you can check and manage the progress of your training.

### Infer and Interpolate
After training is done, run the below command to infer test data:

```sh
python infer.py --model_dir=checkpoint_dir/ 
                --batch_size=16 
                --source_obj=binary_obj_path 
                --embedding_ids=label[s] of the font, separate by comma
                --save_dir=save_dir/
```

Also you can do interpolation with this command:

```sh
python infer.py --model_dir= checkpoint_dir/ 
                --batch_size=10
                --source_obj=obj_path 
                --embedding_ids=label[s] of the font, separate by comma
                --save_dir=frames/ 
                --output_gif=gif_path 
                --interpolate=1 
                --steps=10
                --uroboros=1
```

It will run through all the pairs of fonts specified in embedding_ids and interpolate the number of steps as specified. 

## Acknowledgements
Code derived and rehashed from:
* [zi2zi](https://github.com/kaonashi-tyc/zi2zi) by [kaonashi-tyc](https://github.com/kaonashi-tyc)

## License
[MIT License](https://raw.githubusercontent.com/JohnCoates/Aerial/master/LICENSE)