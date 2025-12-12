"""
    PyJAMAS is Just A More Awesome Siesta
    Copyright (C) 2018  Rodrigo Fernandez-Gonzalez (rodrigo.fernandez.gonzalez@utoronto.ca)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
from typing import Optional, Tuple

import skimage.io as sio
import skimage.morphology as sm
import skimage.measure as sme
import skimage.transform as st
import scipy.ndimage as ndimage

import keras
import keras.backend as kb
import keras.layers as kl
import keras.models as km
import numpy
import torch

from pyjamas.rimage.rimml.classifier_types import classifier_types
from pyjamas.rimage.rimutils import rimutils
from pyjamas.rimage.rimml.rimneuralnet import rimneuralnet


class ReSCUNet(rimneuralnet):
    CLASSIFIER_TYPE: str = classifier_types.RESCUNET.value
    CONCATENATION_LEVEL: int = 1

    def __init__(self, parameters: Optional[dict] = None):
        self.X_train_mask = None
        self.concatenation_level: int = parameters.get('concatenation_level', ReSCUNet.CONCATENATION_LEVEL)
        super().__init__(parameters)

        if type(self.step_sz) == int:  # backwards compatibility with how some models were saved
            self.step_sz = (self.step_sz, self.step_sz)

    def build_network(self, input_shape: Tuple, n_classes: int) -> km.Model:
        _epsilon = keras.ops.convert_to_tensor(kb.epsilon(), numpy.float32)

        # several input layers for data preprocessing steps
        input_layer = keras.Input(shape=input_shape, name="image_input")

        # the shape of the weight maps has to be such that it can be element-wise
        # multiplied to the softmax output.
        weight_input_layer = keras.Input(shape=input_shape[:2] + (n_classes,))
        mask_input_layer = keras.Input(shape=input_shape, name="mask_input")

        # ensure that the concatenation level is between 0 to 4, inclusive
        if self.concatenation_level < 0 or self.concatenation_level > 4:
            print("Invalid concatenation level, setting concatenation level to 0.")
            self.concatenation_level = 0

        curr_level = 0
        if self.concatenation_level == curr_level:
            in1 = [kl.Concatenate()([input_layer, mask_input_layer])]
        else:
            in1 = [input_layer]

        # adding the layers; image convolutions
        conv1 = kl.Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(in1[0])
        conv1 = kl.Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv1)
        conv1 = kl.Dropout(0.1)(conv1)
        mpool1 = kl.MaxPool2D()(conv1)

        if self.concatenation_level > curr_level:
            # mask convolutions
            convm1 = kl.Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(mask_input_layer)
            convm1 = kl.Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(convm1)
            convm1 = kl.Dropout(0.1)(convm1)
            mpoolm1 = kl.MaxPool2D()(convm1)

        curr_level += 1
        if self.concatenation_level == curr_level:
            in2 = [kl.Concatenate()([mpool1, mpoolm1])]
        else:
            in2 = [mpool1]

        conv2 = kl.Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(in2[0])
        conv2 = kl.Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv2)
        conv2 = kl.Dropout(0.2)(conv2)
        mpool2 = kl.MaxPool2D()(conv2)

        if self.concatenation_level > curr_level:
            # mask convolutions
            convm2 = kl.Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(mpoolm1)
            convm2 = kl.Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(convm2)
            convm2 = kl.Dropout(0.2)(convm2)
            mpoolm2 = kl.MaxPool2D()(convm2)

        curr_level += 1
        if self.concatenation_level == curr_level:
            in3 = [kl.Concatenate()([mpool2, mpoolm2])]
        else:
            in3 = [mpool2]

        conv3 = kl.Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(in3[0])
        conv3 = kl.Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv3)
        conv3 = kl.Dropout(0.3)(conv3)
        mpool3 = kl.MaxPool2D()(conv3)

        if self.concatenation_level > curr_level:
            # mask convolutions
            convm3 = kl.Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(mpoolm2)
            convm3 = kl.Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(convm3)
            convm3 = kl.Dropout(0.3)(convm3)
            mpoolm3 = kl.MaxPool2D()(convm3)

        curr_level += 1
        if self.concatenation_level == curr_level:
            in4 = [kl.Concatenate()([mpool3, mpoolm3])]
        else:
            in4 = [mpool3]

        conv4 = kl.Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(in4[0])
        conv4 = kl.Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv4)
        conv4 = kl.Dropout(0.4)(conv4)
        mpool4 = kl.MaxPool2D()(conv4)

        if self.concatenation_level > curr_level:
            convm4 = kl.Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(mpoolm3)
            convm4 = kl.Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(convm4)
            convm4 = kl.Dropout(0.4)(convm4)
            mpoolm4 = kl.MaxPool2D()(convm4)

        curr_level += 1
        if self.concatenation_level == curr_level:
            in5 = [kl.Concatenate()([mpool4, mpoolm4])]
        else:
            in5 = [mpool4]

        conv5 = kl.Conv2D(1024, 3, activation='relu', padding='same', kernel_initializer='he_normal')(in5[0])
        conv5 = kl.Conv2D(1024, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv5)
        conv5 = kl.Dropout(0.5)(conv5)

        up6 = kl.Conv2DTranspose(512, 2, strides=2, kernel_initializer='he_normal', padding='same')(conv5)
        conv6 = kl.Concatenate()([up6, conv4])
        conv6 = kl.Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv6)
        conv6 = kl.Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv6)
        conv6 = kl.Dropout(0.4)(conv6)

        up7 = kl.Conv2DTranspose(256, 2, strides=2, kernel_initializer='he_normal', padding='same')(conv6)
        conv7 = kl.Concatenate()([up7, conv3])
        conv7 = kl.Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv7)
        conv7 = kl.Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv7)
        conv7 = kl.Dropout(0.3)(conv7)

        up8 = kl.Conv2DTranspose(128, 2, strides=2, kernel_initializer='he_normal', padding='same')(conv7)
        conv8 = kl.Concatenate()([up8, conv2])
        conv8 = kl.Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv8)
        conv8 = kl.Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv8)
        conv8 = kl.Dropout(0.2)(conv8)

        up9 = kl.Conv2DTranspose(64, 2, strides=2, kernel_initializer='he_normal', padding='same')(conv8)
        conv9 = kl.Concatenate()([up9, conv1])
        conv9 = kl.Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv9)
        conv9 = kl.Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv9)
        conv9 = kl.Dropout(0.1)(conv9)

        c10 = kl.Conv2D(n_classes, 1, activation='softmax', kernel_initializer='he_normal', name="unet-activation")(
            conv9)

        # Add a few non-trainable layers to mimic the computation of the cross-entropy loss,
        # so that the actual loss function just has to perform the aggregation.
        c11 = kl.Lambda(lambda x: x / keras.ops.sum(x, len(x.shape) - 1, True))(c10)
        c11 = kl.Lambda(lambda x: keras.ops.clip(x, _epsilon, 1. - _epsilon))(c11)
        c11 = kl.Lambda(lambda x: keras.ops.log(x))(c11)
        weighted_sm = kl.multiply([c11, weight_input_layer])

        return km.Model(inputs=[input_layer, weight_input_layer, mask_input_layer], outputs=[weighted_sm])

    def _process_training_data(self) -> bool:
        """
        Loads and scales training data (previous masks).
        :return:
        """
        super()._process_training_data()

        train_ids = next(os.walk(self.positive_training_folder))[1]

        # Get and resize train previous masks
        self.X_train_mask = numpy.zeros((len(train_ids), self.train_image_size[0], self.train_image_size[1], 1), dtype=bool)

        for n, id_ in enumerate(train_ids):
            path = os.path.join(self.positive_training_folder, id_)

            prev_mask_file = os.path.join(path, "prev_mask", os.listdir(os.path.join(path, "prev_mask"))[0])
            prev_mask = numpy.zeros((self.train_image_size[0], self.train_image_size[1], 1), dtype=bool)
            prev_mask_ = sio.imread(prev_mask_file)
            prev_mask_ = numpy.expand_dims(st.resize(prev_mask_, (self.train_image_size[0], self.train_image_size[1]), order=0,
                                                     mode='constant', preserve_range=True), axis=-1)

            max_value = numpy.max(numpy.max(prev_mask_))
            prev_mask_ = numpy.round(numpy.divide(prev_mask_, numpy.full(prev_mask_.shape, max_value)))
            prev_mask_ = numpy.multiply(prev_mask_, numpy.full(prev_mask_.shape, max_value))
            prev_mask = numpy.maximum(prev_mask, prev_mask_)
            self.X_train_mask[n] = prev_mask

        return True

    def _get_training_inputs(self) -> list:
        return [self.X_train, self.W_train, self.X_train_mask]

    def predict(self, image: numpy.ndarray, prev_mask: numpy.ndarray) -> (numpy.ndarray, numpy.ndarray):
        if image is None or image is False:
            return False
        if prev_mask is None or prev_mask is False:
            return False

        if image.ndim == 3:
            image = image[0, :, :]
        if prev_mask.ndim == 3:
            prev_mask = prev_mask[0, :, :]

        testImage = image / self.scaler

        # CONVERT TO TORCH ---------------------------------------
        image_input = self.classifier.input[0]
        prev_mask_input = self.classifier.input[2]
        softmax_output = self.classifier.get_layer('unet-activation').output
        predictor = keras.Model(inputs=[image_input, prev_mask_input], outputs=softmax_output)
        # END CONVERT TO TORCH ------------------------------------

        with torch.no_grad():  # no gradient tracking (faster inference).
            # Keep these on GPU as PyTorch tensors for faster computation
            device = 'cpu'
            if torch.mps.is_available():
                device = torch.device("mps")
            elif torch.cuda.is_available():
                device = torch.device("cuda")

            testLabel = torch.zeros(testImage.shape, dtype=torch.bool, device=device)
            testProb = torch.zeros(testImage.shape, dtype=torch.float32, device=device)
            half_width = int(self.train_image_size[1] / 2)
            half_height = int(self.train_image_size[0] / 2)
            for animage, therow, thecol in rimutils.generate_subimages(testImage, self.train_image_size[0:2],
                                                                       self.step_sz, True):
                prev_mask_subimage = prev_mask[(therow - half_height):(therow + half_height),
                                               (thecol - half_width):(thecol + half_width)]

                if numpy.sum(prev_mask_subimage) == 0:  # empty prev mask in this subimage, skip area
                    continue

                yhat = predictor([numpy.expand_dims(animage, axis=0), numpy.expand_dims(prev_mask_subimage, axis=0)], training=False)
                yhat_class = torch.argmax(yhat[0], axis=-1)
                p = torch.amax(yhat[0], axis=-1)

                testLabel[(therow - half_height):(therow + half_height), (thecol - half_width):(thecol + half_width)] \
                    = torch.logical_or(testLabel[(therow - half_height):(therow + half_height),
                                       (thecol - half_width):(thecol + half_width)], yhat_class)
                testProb[(therow - half_height):(therow + half_height), (thecol - half_width):(thecol + half_width)] = p

            # Only convert to NumPy and leave the GPU at the very end
            testLabel = testLabel.cpu().numpy()
            testProb = testProb.cpu().numpy()

            # perform postprocessing to fill holes and take only the one object that best matches the previous mask
            testLabel = ndimage.binary_fill_holes(testLabel)
            labelled_mask = sme.label(testLabel)
            region_ids = numpy.unique(labelled_mask[labelled_mask > 0])
            if len(region_ids) > 1:
                best_IOU = None
                best_id = None
                for this_id in region_ids:
                    this_region = labelled_mask == this_id
                    intersection = numpy.sum(numpy.logical_and(this_region, prev_mask))
                    union = numpy.sum(numpy.logical_or(this_region, prev_mask))
                    this_IOU = intersection / union
                    if best_id is None or this_IOU > best_IOU:
                        best_IOU = this_IOU
                        best_id = this_id
                testLabel = labelled_mask == best_id

        if self.erosion_width is not None and self.erosion_width != 0:
            self.object_array = numpy.asarray(rimutils.extract_contours(
                sm.dilation(sm.label(sm.binary_erosion(testLabel, sm.square(self.erosion_width)), connectivity=1),
                            sm.square(self.erosion_width))), dtype=object)
        else:
            self.object_array = numpy.asarray(rimutils.extract_contours(sm.label(testLabel, connectivity=1)),
                                              dtype=object)
        self.prob_array = testProb

        return self.object_array.copy(), self.prob_array.copy()

    def save(self, filename: str) -> bool:
        self.save_dict.update({
            'classifier_type': ReSCUNet.CLASSIFIER_TYPE,
            'concatenation_level': self.concatenation_level,
        })
        return super().save(filename)
