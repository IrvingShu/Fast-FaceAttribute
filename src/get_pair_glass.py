import os
import sys
import argparse
import shutil


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--img-root-folder', type=str, help='img root folder')
    parser.add_argument('--img-score-path', type=str, help='img list path')
    parser.add_argument('--save-root', type=str, help='img list path')
    parser.add_argument('--threshold', type=str, help='img list path')
    parser.add_argument('--not-glasses-threshold', type=str, help='img list path')

    return parser.parse_args(argv)


def get_label_featurelist_dict(path):
    with open(path) as f:
        lines = f.readlines()
        label_img_dict = dict()
        current_label = ''
        img_list = []
        i = 0
        class_num = 0

        test = []
        for line in lines:
            i = i + 1
            label = line.strip().split('/')[0]
            test.append(label)
            if label != current_label:
                class_num = class_num + 1
                if len(img_list) > 0:
                    label_img_dict[current_label] = img_list
                    img_list = []
                current_label = label
                img_list.append(line.strip())
                if i == len(lines):
                    label_img_dict[current_label] = img_list
            else:
                img_list.append(line.strip())
                if i == len(lines):
                    label_img_dict[current_label] = img_list
        return label_img_dict, class_num


def main(args):
    print('===> args:\n', args)
    img_root = args.img_root_folder
    score_path = args.img_score_path
    save_root = args.save_root
    threshold = float(args.threshold)
    not_glasses_threshold = float(args.not_glasses_threshold)
    
    label_score_dict, num_class = get_label_featurelist_dict(score_path)
    
    count = 0
    for key in label_score_dict:
        glass_pair = []

        glass_finished = 0
        no_glass_finished = 0

        for i in range(len(label_score_dict[key])):
       
            line_list = label_score_dict[key][i].strip().split(' ')
            img_name = line_list[0]
            glass_score = line_list[2]
            if float(glass_score) > threshold and glass_finished == 0:
                glass_pair.append(img_name)
                glass_finished = 1
                print(img_name, glass_score, 'have')

            if float(glass_score) < not_glasses_threshold and no_glass_finished == 0:
                glass_pair.append(img_name)
                no_glass_finished = 1

                print(img_name, glass_score, 'no')
        print(glass_pair)
        if len(glass_pair) > 1:
            for j in range(len(glass_pair)):
                save_path = os.path.join(save_root, glass_pair[j].split('/')[0])
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                    shutil.copy2(os.path.join(img_root, glass_pair[j]), save_path)
                else:
                    shutil.copy2(os.path.join(img_root, glass_pair[j]), save_path)



if __name__ == '__main__':
    main(parse_args(sys.argv[1:]))
