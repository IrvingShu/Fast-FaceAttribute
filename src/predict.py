import numpy as np
import sys,os
import argparse
import time

#caffe_root = '/workspace/data/qyc/qyc_work/face_attribute/caffe'
#sys.path.insert(0, caffe_root + 'python')
import caffe

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--img-root-folder', type=str, help='img root folder')
    parser.add_argument('--img-list-path', type=str, help='img list path')
    parser.add_argument('--model-prototxt-path', type=str, help='model prototxt path')
    parser.add_argument('--model-path', type=str, help='model path')

    parser.add_argument('--save-list-path', type=str, help='save attribute path')
    return parser.parse_args(argv)


def get_face_attribute(net, img_root_folder, img_list_path, save_list_path):

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))
    transformer.set_raw_scale('data', 255)
    transformer.set_channel_swap('data', (2, 1, 0))

    with open(img_list_path) as f, open(save_list_path, 'w') as f1:
        lines = f.readlines()
        count = 0
        print ('total num:%d' % (len(lines)))
        for line in lines:
            img_name = line.strip()
            count += 1
            if count % 10000 == 0:
                print('Processing: ', float(count) / len(lines))
            im = caffe.io.load_image(os.path.join(img_root_folder, img_name))
            net.blobs['data'].reshape(1, 3, 112, 92)
            net.blobs['data'].data[...] = transformer.preprocess('data', im)
            out = net.forward()
            gender_score = net.blobs['gender_prob'].data[0].flatten()[1]
            glass_score = net.blobs['glasses_prob'].data[0].flatten()[1]
            hat_score = net.blobs['hat_prob'].data[0].flatten()[1]
            mask_score = net.blobs['mask_prob'].data[0].flatten()[1]

            f1.write(img_name + ' ' + str(gender_score) + ' ' + str(glass_score) + ' ' + str(hat_score) + ' ' + str(mask_score) + '\n')


def main(args):
    print('===> args:\n', args)

    img_root_folder = args.img_root_folder
    img_list_path = args.img_list_path
    save_list_path = args.save_list_path

    model_prototxt_path = args.model_prototxt_path
    model_path = args.model_path

    net = caffe.Net(model_prototxt_path, model_path, caffe.TEST)
    get_face_attribute(net, img_root_folder, img_list_path, save_list_path)


if __name__ == '__main__':
    start_time = time.time()
    main(parse_args(sys.argv[1:]))
    end_time = time.time()
    print('time cost: %f' % (end_time - start_time))
