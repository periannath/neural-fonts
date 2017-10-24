# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

import argparse
import glob
import os
import cPickle as pickle
import random


def pickle_examples(paths, train_path, val_path, train_val_split=0.1, fixed_sample=False):
    """
    Compile a list of examples into pickled format, so during
    the training, all io will happen in memory
    """
    if fixed_sample:
        with open(train_path, 'wb') as ft:
            with open(val_path, 'wb') as fv:
                for p in paths:
                    label = int(os.path.basename(p).split("_")[0])
                    uni = os.path.basename(p).split("_")[1]
                    with open(p, 'rb') as f:
#                        print("img %s" % p, label)
                        img_bytes = f.read()
                        example = (label, uni, img_bytes)
                        if "val" in p:
#                            print("img %s is saved in val.obj" % p)
                            # validation set
                            pickle.dump(example, fv)
                        else:
                            # training set
#                            print("img %s is saved in train.obj" % p)
                            pickle.dump(example, ft)
                return
    with open(train_path, 'wb') as ft:
        with open(val_path, 'wb') as fv:
            for p in paths:
                label = int(os.path.basename(p).split("_")[0])
                with open(p, 'rb') as f:
                    print("img %s" % p, label)
                    img_bytes = f.read()
                    r = random.random()
                    example = (label, img_bytes)
                    if r < train_val_split:
                        pickle.dump(example, fv)
                    else:
                        pickle.dump(example, ft)


parser = argparse.ArgumentParser(description='Compile list of images into a pickled object for training')
parser.add_argument('--dir', dest='dir', required=True, help='path of examples')
parser.add_argument('--save_dir', dest='save_dir', required=True, help='path to save pickled files')
parser.add_argument('--split_ratio', type=float, default=0.1, dest='split_ratio',
                    help='split ratio between train and val')
parser.add_argument('--fixed_sample', dest='fixed_sample', default=0, help='binarize fixed samples (we distiguish train/validation data with its file name).')
args = parser.parse_args()

if __name__ == "__main__":
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    train_path = os.path.join(args.save_dir, "train.obj")
    val_path = os.path.join(args.save_dir, "val.obj")
    pickle_examples(glob.glob(os.path.join(args.dir, "*.png")), train_path=train_path, val_path=val_path,
                    train_val_split=args.split_ratio, fixed_sample=args.fixed_sample)
#    pickle_examples(sorted(glob.glob(os.path.join(args.dir, "*.png")), key=lambda e: float(os.path.splitext(os.path.basename(e))[0].replace("_","").replace("train","").replace("val",""))), train_path=train_path, val_path=val_path,
#                    train_val_split=args.split_ratio, fixed_sample=args.fixed_sample)
