#!/bin/bash

rm build -R
rm models -R

for format in ONNX tflite ncnn "executorch --hw-acceleration XNNPACK" "executorch --hw-acceleration Vulkan"
do
	for quantization in float32 float16 "int8 --calibration-dataset Random"
	do
		echo "Converting to $format with quantization $quantization"
		ai-parade convert FooBarModel weights.pth $format --quantize $quantization --output models 
		echo -e "Done\n"
	done
done