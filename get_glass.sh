nohup python ./src/get_pair_glass.py \
     --img-root-folder=/workspace/data/megaface2_refinedet_align_112x112/aligned_imgs_clean \
     --img-score-path=./result.txt \
     --save-root=./img \
     --threshold=0.98 \
     --not-glasses-threshold=0.1 \
     > ./run.log 2>&1 &
