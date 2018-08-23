nohup python ./src/predict.py \
     --img-root-folder=/workspace/data/megaface2_refinedet_align_112x112/aligned_imgs_clean \
     --img-list-path=/workspace/data/megaface2_refinedet_align_112x112/below_10_img.lst \
     --model-prototxt-path=./models/mini/SHUNet_Attr.prototxt \
     --model-path=./models/mini/SHUNet_Attr.caffemodel \
     --save-list-path=./result.txt \
     > ./run.log 2>&1 &
