# Comparison of sota models to image quality improvement
> Abstract  
> The main aim of this paper is to investigate existing methods of improving picture quality, compare their characteristics, choose the best one and write a microservice to improve video quality.  
<p align="center">

## 1) Introduction
After reading several articles:  

* https://arxiv.org/pdf/2011.14132.pdf  
* https://arxiv.org/pdf/1704.02470.pdf  
* https://arxiv.org/pdf/1912.04958.pdf  
* https://www4.comp.polyu.edu.hk/~cslzhang/paper/PAMI_LUT.pdf  
* https://www.waqaszamir.com/publication/zamir-2022-mirnetv2/zamir-2022-mirnetv2.pdf  

you can understand that the task of improving the picture quality is now evolving mainly in two directions: the first - recovery using GANs and solving the problems associated with them. The second one is the point solution of the problem by means of convolutional neural networks and their modifications (solving the problem of super resolution, denoising, debluring, etc.).  
	
<!-- ![image](https://user-images.githubusercontent.com/52531828/173533373-f6eb35c4-2f50-4072-beb9-8a645c43d6c2.png) -->

If we talk about the highlighted articles, the first one looked at approaches in general, to improve the quality of medical photos. The second was about using the SP (super resolution) method for the cameras of various phones. The third is about the artefacts that appear as a result of the generation of GAN's and how to deal with them. The fourth and fifth are quite modern approaches to solve problems of sp and image enchancment in general.  


In addition to the usual comparison, I tried to take exactly those methods that would improve the quality of face recognition (which is why the problem of GANs is so relevant, because significant artifacts can occur in the process of generation). After studying the article ( https://arxiv.org/pdf/1805.11519.pdf ), I came to a conclusion that at the initial stage I should study the methods of super resolution (although in the process of research it turned out that the task of denoising is closely intertwined with it). In addition, my task is more about studying general methods of improving image quality. But in the process, the assignment was supplemented. It became necessary to pay more attention to denoising and deblurring models.  

I chose classic SSIM and PSNR metrics for model comparison. I chose them because I wanted to make a comparison by method: take an image, do various transformations with it (reduce the dimensionality, impose noise), restore the image and compare it to what it was before all the transformations. And these metrics are perfect for that. Here, ${MAX_I}$ is the maximum possible pixel value of the image.  
<p align="center">
	<img width="720" height="200" src="https://user-images.githubusercontent.com/52531828/173359294-c17eca23-b92c-41cb-a225-1d04f693d9ad.png">
</p>
<p align="center">
	<img width="720" height="200" src="https://user-images.githubusercontent.com/52531828/173359383-c2424538-8fe7-430b-b282-cabaca33ec61.png">
</p>

However, these metrics have disadvantages. For example, a blurry picture will give better quality than a picture with clear boundaries but slightly offset from the original picture. I used my own images of different sizes, some of them with random Gaussian noise and small amount of 240\*320 images, as most of the models are geared up for working with images of small sizes. Noise mapping proved to be useful, as some models behaved very strangely.   

<p align="center">
	<img width="200" height="300" src="https://user-images.githubusercontent.com/52531828/173360180-a6d8043f-92d9-48e1-9c4a-0083874f8bca.jpg">
	<img width="200" height="300" src="https://user-images.githubusercontent.com/52531828/173360201-6bf42825-6385-48aa-b97a-a5006ca1b27c.jpg">
</p>

MIRNetv2 sp model results, after imposing random noise.  
I did not take ready-made datasets, as most of the models have already been tested on them, I checked on my own pictures.

## Running models
### I took a popular model to start with  Real-ESRGAN (https://github.com/ai-forever/Real-ESRGAN)
 <a href="https://colab.research.google.com/drive/1dho25zlQl84ZR3A223V-4DFp5P2YXgIn?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="google colab logo"></a>
 <p align="center">
	<img width="100" height="160" src="https://user-images.githubusercontent.com/52531828/173386929-bdb50123-9012-4165-a337-05d0b50c3e7a.jpg">
	<img width="240" height="320" src="https://user-images.githubusercontent.com/52531828/173386948-85064451-be59-4a01-a444-f4dca9573d57.jpg">
</p>

<p align="center">
	<img width="100" height="160" src="https://user-images.githubusercontent.com/52531828/173389235-1499f5c0-b852-4305-8a9e-8c5ddb3c1baf.jpg">
	<img width="240" height="320" src="https://user-images.githubusercontent.com/52531828/173389249-26b4f2d0-b71b-4918-b9c0-f33bc3ac2912.jpg">
</p>
<p align="center">
	<img width="100" height="160" src="https://user-images.githubusercontent.com/52531828/173390974-b8d43d62-9ce2-4d2a-9100-fc38d85e7e49.jpg">
	<img width="240" height="320" src="https://user-images.githubusercontent.com/52531828/173390992-47541113-4d51-482a-b15d-91741e9a9406.jpg">
</p>




SSIM  - 0.35955440170235103  
PSNR - 29.957596648972494  
Processing time - 10 second video was processed in 2.5 minutes
The model does an excellent upscale, but before that you need to remove the noise from the picture.

### MIRNetv2   
[https://github.com/swz30/MIRNet](https://github.com/swz30/MIRNetv2)     

<a href="https://colab.research.google.com/drive/1dho25zlQl84ZR3A223V-4DFp5P2YXgIn?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="google colab logo"></a>  
solves several problems: SP, denoising, low-light enchansment

<p align="center">
	<img width="200" height="300" src="https://user-images.githubusercontent.com/52531828/173377670-3c773420-e730-48e9-8f7f-bf2a8fe1c089.jpg">
	<img width="200" height="300" src="https://user-images.githubusercontent.com/52531828/173377708-04606cef-4904-444d-9b1c-ce05bc3f5e69.jpg">
</p>
<p align="center">
	<img width="400" height="400" src="https://user-images.githubusercontent.com/52531828/173377744-52cd0e9c-ea74-470a-b154-3417047f00b3.jpg">
	<img width="400" height="400" src="https://user-images.githubusercontent.com/52531828/173377779-9b3c05b5-4ac1-4201-873e-1955f51c02bb.jpg">
</p>    

Results on noisy images  
SSIM  - 0.6983962014317513  
PSNR - 29.185384360348813  
Tried doing the processing by batches. However, the model takes up 14 GB of video memory when the image passes through the network, so it was not possible to test.  
Overall, the model handles a lot of tasks quite well, but is memory-hungry. (I may have run it wrong. This model is advised to be paralleled) 
Processing time - a 10-second video was processed in 4.5 minutes 


### PAMI_LUT   
https://github.com/HuiZeng/Image-Adaptive-3DLUT   
<a href="https://colab.research.google.com/drive/1Elq4oGfXyCHcfpyujccmy1Yf8JO3MbJH?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="google colab logo"></a>  
The model doesn't deal with noise at all  
<p align="center">
	<img width="200" height="300" src="https://user-images.githubusercontent.com/52531828/174430765-7b04084f-058c-4983-9a3e-9633e7dbc378.jpg">
	<img width="200" height="300" src="https://user-images.githubusercontent.com/52531828/174430782-c1ae8155-88ee-4dca-ab63-df4bae424b71.jpg">
</p>
<p align="center">
	<img width="400" height="400" src="https://user-images.githubusercontent.com/52531828/174430816-4dec8431-4a5d-48b9-9612-52d5061ae23e.jpg">
	<img width="400" height="400" src="https://user-images.githubusercontent.com/52531828/174430820-960d7038-2810-4bac-b512-8576a8a4150e.jpg">
</p> 



	
It has proven to be the best in terms of processing time. However, the quality gain is negligible. (mainly lowlight enhancement and added contrast) 
сюда вставлю гифки результатов обработки видео

### VRT
https://github.com/jingyunliang/vrt    
<a href="https://colab.research.google.com/drive/1jiOd9iQQi_OLXU7IvG6w8JT6xq2sdFog"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="google colab logo"></a>  
The model is new and runs extremely slowly. The developers themselves write that they did not run the model on a video with more than six frames. In the discussions, people advise to deblurr the model. Ignoring these drawbacks, the deblurring quality of the model is impressive. 

### iSeeBetter
https://github.com/amanchadha/iSeeBetter  
<a href="https://colab.research.google.com/drive/10aWv_Ou_AibAzFE9Px6WdVxEqeQqmiYX?authuser=1#scrollTo=pZIlhY8UNFST"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="google colab logo"></a>  
In the process of doing the job, it turned out that a simple upscaling would suffice. The iSeeBetter model was chosen. The model shows excellent results, however it takes an average of 2.3 seconds to process each frame (640\*360) on Tesla T4 , when upscaling is only 2x (1280\*720), 7 GB of video memory is required. A minimum of 16GB of video memory is required to upscale by a factor of 4.  
![до](https://user-images.githubusercontent.com/52531828/174415201-b727045b-bede-4d20-acdb-03be04fc942a.png)
![после](https://user-images.githubusercontent.com/52531828/174415196-62fdbbc6-b102-46b4-9f9a-2c5417a4c1ed.png)


# ToDo  
* Перевести на английский  
* добавить описание метрик  
* сделать обработку изображений батчами, а не по одной   


## Микро сервис
Нужно найти оптимальный под видео. Тут сейчас нужно найти годную real time модель, чтобы вдальнейшем запихнуть её в flask сервис.
