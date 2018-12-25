import os
import tensorflow as tf
import numpy as np
from PIL import Image
from random import shuffle
from math import floor
from dir_traversal_tfrecord import tfrecord_auto_traversal


def resize_image(image_dir, output_dir):

    original_image = Image.open(image_dir)
    resize_image = original_image.resize((244, 244))
    resize_image.save(output_dir, "JPEG", optimizer=True)


def get_file_list_from_dir(datadir, extension=None):

    all_files = os.listdir(datadir)
    if extension == None:
        return list(filter( lambda x: os.path.isdir(os.path.join(datadir, x)), all_files))
    data_files = list(filter(lambda file: file.endswith(extension), all_files))
    return data_files

def tfrecord_auto_traversal():

    directory_to_be_searched = "./flowers/" # The directory to be traversed

    tfrecord_list = get_file_list_from_dir(directory_to_be_searched, ".tfrecord")

    print("files that end with tfrecord", tfrecord_list)

    return tfrecord_list


def split_training_and_testing_sets():

    data_dir = "./flowers/"
    folder_list = get_file_list_from_dir("./flowers/")

    for folder in folder_list:

        file_list = get_file_list_from_dir(os.path.join(data_dir, folder), ".jpg")
        shuffle(file_list)
        split = 0.7
        split_index = int(floor(len(file_list) * split))

        training = file_list[:split_index]
        testing = file_list[split_index:]

        for file in training:

            if not os.path.exists("./train/{0}/".format(folder)):
                os.makedirs("./train/{0}/".format(folder))

            resize_image(os.path.join(data_dir, folder, file), "./train/{0}/{1}".format(folder, file))

        for file in testing:

            if not os.path.exists("./test/{0}/".format(folder)):
                os.makedirs("./test/{0}/".format(folder))

            resize_image(os.path.join(data_dir, folder, file), "./test/{0}/{1}".format(folder, file))

def _parse_function(example):

    features = tf.parse_single_example(example, features={
        "image/encoded": tf.FixedLenFeature([], tf.string),
        "image/height": tf.FixedLenFeature([], tf.int64),
        "image/width": tf.FixedLenFeature([], tf.int64),
        "image/filename": tf.FixedLenFeature([], tf.string),
        "image/class/label": tf.FixedLenFeature([], tf.int64), })

    image_encode = features["image/encoded"]
    image_raw = tf.image.decode_jpeg(image_encode, channels=3)
    label = tf.one_hot(features["image/class/label"] - 1, 5)
    return image_raw, label


def read_TFRecord(dataset_name="train"):

    filename_queue = filter(lambda x: dataset_name in x, tfrecord_auto_traversal())
    filename_queue = list(map(lambda x: os.path.join("flowers/", x), filename_queue))

    print("the file queue is ", filename_queue)
    dataset = tf.data.TFRecordDataset(filename_queue)

    dataset = dataset.map(_parse_function)

    if dataset_name == "train":
        dataset = dataset.batch(batch_size=10)
        dataset = dataset.shuffle(buffer_size=10)

    else:
        dataset = dataset.batch(batch_size=1)

    iterator = dataset.make_initializable_iterator()

    return iterator


if __name__ == "__main__":
    pass
    # split_training_and_testing_sets()
    # read_TFRecord("validation")
