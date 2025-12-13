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

from typing import Optional, Tuple
from abc import abstractmethod

import os
import numpy
import gzip
import pickle
import matplotlib.pyplot as plt
import skimage.io as sio
import skimage.morphology as sm
import skimage.segmentation as ss
import skimage.transform as st

import keras
import keras.models as km
import keras.optimizers as ko
import keras.utils as ku
import keras.callbacks as kc

import torch
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.tensorboard import SummaryWriter

import pyjamas.pjscore
from pyjamas.rimage.rimml.rimml import rimml
from pyjamas.rutils import RUtils


class rimneuralnet(rimml):
    OUTPUT_CLASSES: int = 2
    BATCH_SIZE: int = 1
    EPOCHS: int = 100
    LEARNING_RATE: float = 0.001
    STEP_SIZE: Tuple[int, int] = (rimml.TRAIN_IMAGE_SIZE[0]//8, rimml.TRAIN_IMAGE_SIZE[1]//8)
    EROSION_WIDTH: int = 0
    PATIENCE: int = 5
    SAVE_BEST_ONLY_FLAG: bool = True
    SAVE_CHECKPOINTS_FLAG: bool = True
    EARLY_STOPPER_FLAG: bool = True
    LR_SCHEDULER_FLAG: bool = True
    LOG_FLAG: bool = True

    VALIDATION_SPLIT: float = 0.1
    EARLY_STOPPER: dict = {'active': EARLY_STOPPER_FLAG, 'kwargs': {'patience': PATIENCE}}
    LR_SCHEDULER: dict = {'active': LR_SCHEDULER_FLAG, 'kwargs': {'patience': PATIENCE}}  # ReduceLROnPlateau callback
    MODEL_CHECKPOINT: dict = {'active': SAVE_CHECKPOINTS_FLAG, 'kwargs': {'save_best_only': SAVE_BEST_ONLY_FLAG}}
    LOGGING: dict = {'active': LOG_FLAG, 'kwargs': {}}

    def __init__(self, parameters: Optional[dict] = None):
        super().__init__(parameters)

        self.positive_training_folder: str = parameters.get('positive_training_folder')
        self.save_folder: str = parameters.get('save_folder')

        # Size of training images (rows, columns).
        self.train_image_size: Tuple[int, int] = parameters.get('train_image_size', rimneuralnet.TRAIN_IMAGE_SIZE)  # (row, col)
        self.step_sz: Tuple[int, int] = parameters.get('step_sz', rimneuralnet.STEP_SIZE)

        self.scaler: int = parameters.get('scaler', 1)  # max pixel value of the training set.

        self.X_train: numpy.ndarray = None
        self.Y_train: numpy.ndarray = None
        self.W_train: numpy.ndarray = None

        self.save_dict: dict = {}

        self.object_array: numpy.ndarray = None
        self.prob_array: numpy.ndarray = None

        self.output_classes: int = parameters.get('output_classes', rimneuralnet.OUTPUT_CLASSES)
        self.learning_rate: float = parameters.get('learning_rate', rimneuralnet.LEARNING_RATE)
        self.input_size: Tuple[int, int] = parameters.get('train_image_size', rimneuralnet.TRAIN_IMAGE_SIZE)
        self.epochs: int = parameters.get('epochs', rimneuralnet.EPOCHS)
        self.mini_batch_size: int = parameters.get('mini_batch_size', rimneuralnet.BATCH_SIZE)
        self.erosion_width: int = parameters.get('erosion_width', rimneuralnet.EROSION_WIDTH)
        self.step_sz = parameters.get('step_sz', rimneuralnet.STEP_SIZE)
        self.validation_split = parameters.get('validation_split', rimneuralnet.VALIDATION_SPLIT)

        self.early_stopper = parameters.get('early_stopper', rimneuralnet.EARLY_STOPPER)
        self.lr_scheduler = parameters.get('lr_scheduler', rimneuralnet.LR_SCHEDULER)
        self.model_checkpoint = parameters.get('model_checkpoint', rimneuralnet.MODEL_CHECKPOINT)
        self.logging = parameters.get('logging', rimneuralnet.LOGGING)

        classifier_representation = parameters.get('classifier')
        if type(classifier_representation) is km.Model:
            self.classifier = classifier_representation
        else:
            if len(self.input_size) == 2:
                self.input_size = self.input_size + (1,)

        self.classifier = self.build_network(self.input_size, self.output_classes)
        adam = ko.Adam(learning_rate=self.learning_rate)
        self.classifier.compile(adam, loss=self.pixelwise_loss)
        if type(classifier_representation) is list:
            self.classifier.set_weights(classifier_representation)

        self.device = None
        if torch.mps.is_available():
            self.device = torch.device("mps")
        elif torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")

    @abstractmethod
    def build_network(self, input_shape: Tuple, n_classes: int) -> km.Model:
        pass

    @staticmethod
    def pixelwise_loss(target, output):
        """
        A custom function defined to simply sum the pixelwise loss.
        This function doesn't compute the crossentropy loss, since that is made a
        part of the model's computational graph itself.
        Parameters
        ----------
        target : keras.tensor
            A tensor corresponding to the true labels of an image.
        output : keras.tensor
            Model output
        Returns
        -------
        keras.tensor
            A tensor holding the aggregated loss.
        """
        return - keras.ops.sum(target * output,
                               len(output.shape) - 1)

    """def fit(self):
        self._process_training_data()
        inputs = self._get_training_inputs()
        callbacks = self._build_callbacks()

        self.classifier.fit(inputs, self.Y_train, batch_size=self.mini_batch_size, epochs=self.epochs,
                            validation_split=self.validation_split, callbacks=callbacks if callbacks else None)
        return True"""

    def fit(self):
        self._process_training_data()
        inputs = self._get_training_inputs()
        callbacks = self._build_callbacks()

        logs = {}
        writer = None

        if self.logging['active']:
            log_dir = os.path.join(self.save_folder, 'logs')
            os.makedirs(log_dir, exist_ok=True)
            writer = SummaryWriter(log_dir)

        # Convert to torch tensors
        tensor_inputs = [torch.tensor(inp, dtype=torch.float32).to(self.device) for inp in inputs]
        Y_train = torch.tensor(self.Y_train, dtype=torch.float32).to(self.device)

        # Split validation data
        n_samples = len(tensor_inputs[0])
        val_size = int(n_samples * self.validation_split)
        train_size = n_samples - val_size

        # Split data
        train_inputs = [inp[:train_size] for inp in tensor_inputs]
        val_inputs = [inp[train_size:] for inp in tensor_inputs]
        train_Y, val_Y = Y_train[:train_size], Y_train[train_size:]

        # Create DataLoaders
        train_dataset = TensorDataset(*train_inputs, train_Y)
        train_loader = DataLoader(train_dataset, batch_size=self.mini_batch_size, shuffle=True)

        if self.validation_split > 0 and val_size > 0:
            val_dataset = TensorDataset(*val_inputs, val_Y)
            val_loader = DataLoader(val_dataset, batch_size=self.mini_batch_size, shuffle=False)

        # Setup optimizer (keep the same learning rate)
        optimizer = torch.optim.Adam(self.classifier.parameters(), lr=self.learning_rate)

        # Initialize callback state
        best_loss = float('inf')
        patience_counter = 0
        lr_patience_counter = 0

        avg_val_loss = 0.
        avg_train_loss = 0.

        # Training loop
        for epoch in range(self.epochs):
            # Training phase
            self.classifier.train()
            train_loss = 0.0
            n_train_batches = 0

            for batch_data in train_loader:
                # Unpack: last element is Y, everything before is model inputs
                *batch_inputs, batch_Y = batch_data

                optimizer.zero_grad()

                # Forward pass - note your model expects [X, W] as inputs
                outputs = self.classifier(batch_inputs)

                # Your custom loss (already includes the weight map in the output)
                loss = -torch.sum(batch_Y * outputs, dim=-1).mean()

                loss.backward()
                optimizer.step()

                train_loss += loss.item()
                n_train_batches += 1

            avg_train_loss = train_loss / n_train_batches

            # Validation phase
            if self.validation_split > 0 and val_size > 0:
                self.classifier.eval()
                val_loss = 0.0
                n_val_batches = 0

                with torch.no_grad():
                    for batch_data in val_loader:
                        *batch_inputs, batch_Y = batch_data

                        outputs = self.classifier(batch_inputs)
                        loss = -torch.sum(batch_Y * outputs, dim=-1).mean()
                        val_loss += loss.item()
                        n_val_batches += 1

                avg_val_loss = val_loss / n_val_batches
                monitor_loss = avg_val_loss
                print(f"Epoch {epoch + 1}/{self.epochs} - loss: {avg_train_loss:.4f} - val_loss: {avg_val_loss:.4f}")
            else:
                monitor_loss = avg_train_loss
                print(f"Epoch {epoch + 1}/{self.epochs} - loss: {avg_train_loss:.4f}")

            logs = {
                'loss': avg_train_loss,
                'val_loss': avg_val_loss if self.validation_split > 0 else None
            }

            # Log to TensorBoard (if active)
            if writer:
                writer.add_scalar('Loss/train', avg_train_loss, epoch)
                if self.validation_split > 0:
                    writer.add_scalar('Loss/validation', avg_val_loss, epoch)
                writer.add_scalar('Learning_rate', optimizer.param_groups[0]['lr'], epoch)

            # Handle Early Stopping
            if self.early_stopper['active']:
                if monitor_loss < best_loss:
                    best_loss = monitor_loss
                    patience_counter = 0
                    # Save best weights
                    if self.model_checkpoint['active'] and self.model_checkpoint['kwargs'].get('save_best_only', True):
                        for callback in callbacks:
                            if isinstance(callback, SaveCallback):
                                callback.on_epoch_end(epoch, logs)
                else:
                    patience_counter += 1
                    if patience_counter >= self.early_stopper['kwargs']['patience']:
                        print(f"Early stopping triggered at epoch {epoch + 1}")
                        break

            # Handle Learning Rate Reduction
            if self.lr_scheduler['active']:
                if monitor_loss < best_loss:
                    lr_patience_counter = 0
                else:
                    lr_patience_counter += 1
                    if lr_patience_counter >= self.lr_scheduler['kwargs']['patience']:
                        old_lr = optimizer.param_groups[0]['lr']
                        new_lr = old_lr * 0.1  # Default factor for ReduceLROnPlateau
                        optimizer.param_groups[0]['lr'] = new_lr
                        print(f"Reducing learning rate to {new_lr}")
                        lr_patience_counter = 0

            # Call other callbacks (logging, model checkpoint)
            for callback in callbacks:
                if not isinstance(callback, SaveCallback) or not self.model_checkpoint['kwargs'].get('save_best_only',
                                                                                                     True):
                    if hasattr(callback, 'on_epoch_end'):
                        callback.on_epoch_end(epoch, logs)

        # Call on_train_end for callbacks
        for callback in callbacks:
            if hasattr(callback, 'on_train_end'):
                callback.on_train_end(logs)

        if writer:
            writer.close()

        return True

    def _process_training_data(self) -> bool:
        """
        Loads and scales training data and calculates weight maps.
        :return:
        """
        train_ids = next(os.walk(self.positive_training_folder))[1]

        # Get and resize train images and masks
        self.X_train = numpy.zeros((len(train_ids), self.train_image_size[0], self.train_image_size[1], 1), dtype=numpy.uint16)
        self.Y_train = numpy.zeros((len(train_ids), self.train_image_size[0], self.train_image_size[1], 1), dtype=bool)
        self.W_train = numpy.zeros((len(train_ids), self.train_image_size[0], self.train_image_size[1], 1), dtype=float)
        print('Resizing train images and masks and calculating weight maps ... ')

        for n, id_ in enumerate(train_ids):
            path = os.path.join(self.positive_training_folder, id_)
            im_file = os.path.join(path, "image", os.listdir(os.path.join(path, "image"))[0])
            img = sio.imread(im_file)
            if img.ndim == 3:
                img = img[0, :, :]
            img = numpy.expand_dims(st.resize(img, (self.train_image_size[0], self.train_image_size[1]), order=3,
                                              mode='constant', preserve_range=True), axis=-1)
            self.X_train[n] = img
            msk_file = os.path.join(path, "mask", os.listdir(os.path.join(path, "mask"))[0])
            mask = numpy.zeros((self.train_image_size[0], self.train_image_size[1], 1), dtype=bool)
            mask_ = sio.imread(msk_file)
            mask_ = numpy.expand_dims(st.resize(mask_, (self.train_image_size[0], self.train_image_size[1]), order=0,
                                                mode='constant', preserve_range=True), axis=-1)
            mask = numpy.maximum(mask, mask_)
            weights = self.weight_map(mask)
            self.Y_train[n] = mask
            self.W_train[n, :, :, 0] = weights

        self.scaler = numpy.amax(self.X_train)
        self.X_train = self.X_train / self.scaler

        wmap = numpy.zeros((self.X_train.shape[0], self.train_image_size[0], self.train_image_size[1], 2),
                           dtype=numpy.float32)
        wmap[..., 0] = self.W_train.squeeze()
        wmap[..., 1] = self.W_train.squeeze()
        self.W_train = wmap

        self.Y_train = ku.to_categorical(self.Y_train)
        return True

    def weight_map(self, binmasks: numpy.ndarray, w0: float = 10., sigma: float = 5., show: bool = False):
        """Compute the weight map for a given mask, as described in Ronneberger et al.
        (https://arxiv.org/pdf/1505.04597.pdf)
        """

        labmasks = sm.label(binmasks)
        n_objs = numpy.amax(labmasks)

        if n_objs == 0:
            # No objects, return uniform weights
            return numpy.ones_like(binmasks, dtype=numpy.float32)

        nrows, ncols = labmasks.shape[:2]

        # Move to GPU
        labmasks_gpu = torch.from_numpy(labmasks).to(self.device)
        masks = torch.zeros((n_objs, nrows, ncols), device=self.device)
        distMap = torch.zeros((nrows * ncols, n_objs), device=self.device)

        # Create meshgrid on GPU
        X1_gpu = torch.arange(nrows, device=self.device).repeat_interleave(ncols)
        Y1_gpu = torch.arange(ncols, device=self.device).repeat(nrows)

        for i in range(n_objs):
            mask = torch.squeeze(labmasks_gpu == i + 1)

            mask_cpu = mask.cpu().numpy()
            bounds = ss.find_boundaries(mask_cpu, mode='inner')
            X2, Y2 = numpy.nonzero(bounds)

            if len(X2) == 0:
                # No boundary pixels, skip this object
                mask[i] = mask
                continue

            # Move boundary coordinates to GPU
            X2_gpu = torch.from_numpy(X2).to(self.device).float()
            Y2_gpu = torch.from_numpy(Y2).to(self.device).float()

            xSum = (X2_gpu.reshape(-1, 1) - X1_gpu.reshape(1, -1)) ** 2
            ySum = (Y2_gpu.reshape(-1, 1) - Y1_gpu.reshape(1, -1)) ** 2
            distMap[:, i] = torch.sqrt(xSum + ySum).min(dim=0)[0]
            masks[i] = mask

        ix = torch.arange(distMap.shape[0], device=self.device)
        if distMap.shape[1] == 1:
            d1 = distMap.ravel()
            border_loss_map = w0 * torch.exp((-1 * (d1) ** 2) / (2 * (sigma ** 2)))
        else:
            if distMap.shape[1] == 2:
                # Get indices of 2 smallest distances
                _, indices = torch.topk(distMap, k=2, dim=1, largest=False)
                d1_ix, d2_ix = indices[:, 0], indices[:, 1]
            else:
                _, indices = torch.topk(distMap, k=2, dim=1, largest=False)
                d1_ix, d2_ix = indices[:, 0], indices[:, 1]

            d1 = distMap[ix, d1_ix]
            d2 = distMap[ix, d2_ix]
            border_loss_map = w0 * torch.exp((-1 * (d1 + d2) ** 2) / (2 * (sigma ** 2)))
        xBLoss = torch.zeros((nrows, ncols), device=self.device)
        xBLoss[X1_gpu, Y1_gpu] = border_loss_map
        # class weight map
        loss = torch.zeros((nrows, ncols), device=self.device)
        masks_sum = masks.sum()
        w_1 = 1 - masks_sum / loss.numel()
        w_0 = 1 - w_1

        mask_sum_dim0 = masks.sum(dim=0)
        loss[mask_sum_dim0 == 1] = w_1
        loss[mask_sum_dim0 == 0] = w_0

        ZZ = xBLoss + loss

        ZZ_cpu = ZZ.cpu().numpy()
        # ZZ = resize(ZZ, outsize, preserve_range=True)
        if show:
            plt.imshow(ZZ_cpu)
            plt.colorbar()
            plt.axis('off')
        return ZZ_cpu

    def _get_training_inputs(self):
        return [self.X_train, self.W_train]

    def _build_callbacks(self):
        callbacks = []
        if self.early_stopper['active']:
            if self.validation_split > 0:
                monitor = 'val_loss'
            else:
                raise Warning("Using early stopping without a validation split is not recommended. "
                              "Setting early stopping to monitor train loss.")
                monitor = 'train_loss'
            callbacks.append(kc.EarlyStopping(monitor, restore_best_weights=True, **self.early_stopper['kwargs']))
        if self.lr_scheduler['active']:
            callbacks.append(kc.ReduceLROnPlateau(monitor='val_loss' if self.validation_split > 0 else 'train_loss',
                                                  **self.lr_scheduler['kwargs']))

        if self.model_checkpoint['active']:  # add saving last so that it occurs after all other callback operations
            callbacks.append(SaveCallback(self, monitor='val_loss' if self.validation_split > 0 else 'train_loss',
                                          **self.model_checkpoint['kwargs']))

        # Set model reference for all callbacks
        for callback in callbacks:
            callback.set_model(self.classifier)

        return callbacks

    def build_save_dict(self) -> bool:
        self.save_dict.update({
            'positive_training_folder': self.positive_training_folder,
            'train_image_size': self.train_image_size,
            'scaler': self.scaler,
            'epochs': self.epochs,
            'mini_batch_size': self.mini_batch_size,
            'learning_rate': float(self.classifier.optimizer.learning_rate),
            'classifier': self.classifier.get_weights(),
            'step_sz': self.step_sz,
            'erosion_width': self.erosion_width,
            'early_stopper': self.early_stopper,
            'lr_scheduler': self.lr_scheduler,
            'model_checkpoint': self.model_checkpoint,
            'logging': self.logging,
        })
        return True

    def save(self, filename: str) -> bool:
        self.build_save_dict()
        return RUtils.pickle_this(self.save_dict, RUtils.set_extension(filename, pyjamas.pjscore.PyJAMAS.classifier_extension))


class SaveCallback(kc.Callback):
    """This is quite slow, use the ModelCheckpoint callback and implement a "load model weights" in the IO menu?"""

    def __init__(self, neuralnet: rimneuralnet, save_best_only: bool = True, monitor: str = 'val_loss'):
        super().__init__()

        if neuralnet.save_folder is None or neuralnet.save_folder == "" or neuralnet.save_folder is False:
            self.save_folder = os.getcwd()
        else:
            self.save_folder = neuralnet.save_folder

        self.neuralnet = neuralnet
        self.save_best_only = save_best_only
        self.monitor = monitor
        if save_best_only:
            self.best_loss = numpy.inf

    def on_epoch_end(self, epoch, logs=None):
        if self.save_best_only and logs[self.monitor] < self.best_loss:
            self.neuralnet.save(os.path.join(self.save_folder, "ckpt_best.cfr"))
            self.best_loss = logs[self.monitor]
        elif not self.save_best_only:
            self.neuralnet.save(os.path.join(self.save_folder, f"ckpt_epoch{epoch:03d}.cfr"))
        return {"epoch": epoch, "logs": logs}

    def on_train_end(self, logs):
        if self.save_best_only:
            fh = gzip.open(os.path.join(self.save_folder, "ckpt_best.cfr"), "rb")
            best_cfr = pickle.load(fh)
            fh.close()
            self.neuralnet.classifier.set_weights(best_cfr["classifier"])
        self.neuralnet.save(os.path.join(self.save_folder, "ckpt_final.cfr"))
