# Сравнение моделей для улучшения качества изображения
> Abstract  
> Основная цель данной работы - изучить существующие методы улучшения качества картинки, сравнить их характеристики, выбрать наилучшую и написать микро сервис для улучшения качества видео.
<p align="center">

## 1) Рассмотрение статей
Прочитав несколько статей:  

* https://arxiv.org/pdf/2011.14132.pdf  
* https://arxiv.org/pdf/1704.02470.pdf  
* https://arxiv.org/pdf/1912.04958.pdf  
* https://www4.comp.polyu.edu.hk/~cslzhang/paper/PAMI_LUT.pdf  
* https://www.waqaszamir.com/publication/zamir-2022-mirnetv2/zamir-2022-mirnetv2.pdf  

можно понять, что задача улучшения качества картинки сейчас развивается в основном в двух направлениях: первое - восстановление с помощью GAN'ов и решение проблем, связанных с ними. Второе - точечное решение проблемы с помощью сверточных нейронных сетей и их модификаций (решение задачи super resolution, denoising, debluring и т.д.).  

Если говорить про конкретно выделенные статьи, то в первой рассматривались подходы в целом, для улучшения качества медицинских фотографий. Вторая - про использование метода SP (super resolution) для камер различных телефонов. Третья - про артефакты, которые появляются в результате генерации ганов и борьбы с ними. Четвертая и пятая - достаточно современные подходы для решения задач sp и в целом image enchancment'а.  

Помимо обычного сравнения я попробовал взять именно те методы, которые помогут улучшить качество распознавания лиц (поэтому так актуальна проблема GAN'ов, ведь в процессе генерации могут возникать значительные артефакты). Изучив статью ( https://arxiv.org/pdf/1805.11519.pdf ), я пришел к выводу, что на начальном этапе стоит изучать методы именно super resolution (хоть и в процессе исследования выяснилось, что задача denoising'а с этим тесно переплетается). К тому же, моя задача больше про изучение общих методов улучшния качества изображений.   

Метрики для сравнения моделей я выбрал классические SSIM и PSNR. Выбор остановился на них, так как хотелось бы построить сравнение по методу: взять картинку, сделать с ней различные преобразования (снизить размерность, наложить шум), восстановить изображение и сравнить его с тем, что было до всех преобразований. И данные метрики идеально подходят для этого.
<p align="center">
	<img width="720" height="200" src="https://user-images.githubusercontent.com/52531828/173359294-c17eca23-b92c-41cb-a225-1d04f693d9ad.png">
</p>
<p align="center">
	<img width="720" height="200" src="https://user-images.githubusercontent.com/52531828/173359383-c2424538-8fe7-430b-b282-cabaca33ec61.png">
</p>

Но несмотря на качество этих метрик они тоже не лишены недостатков. Например, размытая картинка будет выдавать качество лучше, нежели картинка с четкими границами, но немного смещенная отностельно изначальной. В качестве данных я использовал свои картинки различных размерностей, их же, но со случайным гауссовским шумом и небольшое количество картинок размера 240*320, т.к. большинство моделей заточено под работу с изображениями малых размерностей. Наложение шума оказалось полезным, т.к. некоторые модели ведут себя неадекватно. 
<p align="center">
	<img width="200" height="300" src="https://user-images.githubusercontent.com/52531828/173360180-a6d8043f-92d9-48e1-9c4a-0083874f8bca.jpg">
	<img width="200" height="300" src="https://user-images.githubusercontent.com/52531828/173360201-6bf42825-6385-48aa-b97a-a5006ca1b27c.jpg">
</p>

результаты модели MIRNetv2 sp, после наложения случайного шума.  
Готовые датасеты я не брал, т.к. большинство моделей на них уже проверено.

## Запуск моделей
### Для начала я взял популярную модель Real-ESRGAN (https://github.com/ai-forever/Real-ESRGAN)
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
Время обработки - 10 секундное видео обрабатывалось 2.5 минуты
Модель отлично делает upscale, однако до этого нужно убрать шум с картинки.

### MIRNetv2 (https://github.com/swz30/MIRNet)

<a href="https://colab.research.google.com/drive/1dho25zlQl84ZR3A223V-4DFp5P2YXgIn?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="google colab logo"></a>  
решает несколько задач: SP, denoising, low-light enchansment

<p align="center">
	<img width="200" height="300" src="https://user-images.githubusercontent.com/52531828/173377670-3c773420-e730-48e9-8f7f-bf2a8fe1c089.jpg">
	<img width="200" height="300" src="https://user-images.githubusercontent.com/52531828/173377708-04606cef-4904-444d-9b1c-ce05bc3f5e69.jpg">
</p>
<p align="center">
	<img width="400" height="400" src="https://user-images.githubusercontent.com/52531828/173377744-52cd0e9c-ea74-470a-b154-3417047f00b3.jpg">
	<img width="400" height="400" src="https://user-images.githubusercontent.com/52531828/173377779-9b3c05b5-4ac1-4201-873e-1955f51c02bb.jpg">
</p>  
Результаты на зашумленных изображениях
SSIM  - 0.6983962014317513 
PSNR - 29.185384360348813    
Сюда я еще добавлю характеристики, т.к. она неплохо справляется со множеством задач
Время обработки - 10 секундное видео обрабатывалось 2.5 минуты


### PAMI_LUT (https://github.com/HuiZeng/Image-Adaptive-3DLUT)
 <a href="https://colab.research.google.com/drive/1Elq4oGfXyCHcfpyujccmy1Yf8JO3MbJH?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="google colab logo"></a>
 
она показала себя лучшей с точки зрения времени обработки  повышает разрешение картинки  
сюда вставлю гифки результатов обработки видео

## Микро сервис
Нужно найти оптимальный под видео. Тут сейчас нужно найти годную real time модель, чтобы вдальнейшем запихнуть её в flask сервис.
