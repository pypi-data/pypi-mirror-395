#                                 Apache License
#                           Version 2.0, January 2004
#                        http://www.apache.org/licenses/


## Import Packages
##-------------------
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from tqdm import tqdm
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input, Flatten, MaxPooling1D, Conv1D
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import root_mean_squared_error


## Utility Functions
##-------------------
'''Utility functions for EGAIN.
(1) mcar_missing: Randomly delete from arr_cols (ncols=0: from the entire data, ncols>0: from a random selection of cols) to create data with MCAR.
(2) mar_missing: Randomly delete from col_miss based on col_ctrl ranks to create data with MAR.
(3) mnar_missing: Randomly delete from df_col to create data with MNAR.
(4) rmse_loss: Calculate RMSE between full_data and imputed_data for missing values in data_x.
(5) plot_losses: Plot the loss functions over iterations.
(6) rounding: Round imputed data based on input data decimals.
'''

def mcar_missing(arr_cols: np.ndarray, ncols: np.ndarray, miss_rate: float, random_seed=None):
  '''Randomly delete from arr_cols (ncols=0: from the entire data, ncols>0: from a random selection of cols) to create data with MCAR.'''
  if random_seed is not None:
    np.random.seed(random_seed)
  data = arr_cols.copy()
  if ncols == 0:
    # uniform random vector
    u = np.random.uniform(size=data.shape)
    # missing values where u <= miss_rate
    mask = (u <= miss_rate)
    data[mask] = np.nan
  else:
    # Randomly select ncols columns
    selected_cols = np.random.choice(arr_cols.shape[1], ncols, replace=False)
    for col in selected_cols:
      # uniform random vector
      u = np.random.uniform(size=data.shape[0])
      # missing values where u <= miss_rate
      mask = (u <= miss_rate)
      data[mask, col] = np.nan
  return data


def mar_missing(col_miss: np.ndarray, col_ctrl: np.ndarray, miss_rate: float, random_seed=None):
  '''Randomly delete from col_miss based on col_ctrl ranks to create data with MAR.'''
  if random_seed is not None:
    np.random.seed(random_seed)
  data = col_miss.copy()
  # Compute the percentile ranks of the ctrl column
  ranks = np.argsort(col_ctrl, axis=0).argsort(axis=0) + 1
  ranks = ranks / col_ctrl.shape[0]  # Normalize ranks
  # Calculate probabilities based on the ranks to achieve the desired missing rate
  if miss_rate <= 0.5:
    probs = 2 * miss_rate * ranks
  else:
    probs = 1 - 2 * (1 - miss_rate) * (1 - ranks)
  # uniform random vector
  u = np.random.uniform(size=data.shape)
  # missing values where u <= miss_rate
  mask = (u <= probs)
  data[mask] = np.nan
  return data


def mnar_missing(col_miss: np.ndarray, miss_rate: float, missing_on='high', random_seed=None):
  '''Randomly delete from col_miss to create data with MNAR.'''
  if random_seed is not None:
    np.random.seed(random_seed)
  data = df_col.copy()
  # Compute the percentile ranks
  sorted_indices = np.argsort(col_miss, axis=0)
  ranks = np.empty_like(sorted_indices, dtype=float)
  ranks[sorted_indices] = (np.arange(1, col_miss.shape[0] + 1) / col_miss.shape[0])
  # Invert ranks for missing_on='low' direction
  if missing_on == 'low':
    ranks = 1 - ranks
  # Calculate probabilities based on the ranks to achieve the desired missing rate
  if miss_rate <= 0.5:
    probs = 2 * miss_rate * ranks
  else:
    probs = 1 - 2 * (1 - miss_rate) * (1 - ranks)
  # Clip probabilities to ensure they are between 0 and 1
  probs = np.clip(probs, 0, 1)
  # uniform random vector
  u = np.random.uniform(size=data.shape)
  # missing values where u <= miss_rate
  mask = (u <= probs)
  data[mask] = np.nan
  return data


def rmse_loss (full_data: np.ndarray, data_x: np.ndarray, imputed_data: np.ndarray):
  '''Calculate RMSE between full_data and imputed_data for missing values in data_x.'''
  scaler = MinMaxScaler()
  norm_parameters = scaler.fit(full_data)
  full_data = scaler.transform(full_data)
  imputed_data = scaler.transform(imputed_data)
  data_m = 1 - np.isnan(data_x)
  # Only for missing values:  valid_indices = (1-data_m)
  rmse = root_mean_squared_error(full_data*(1-data_m), imputed_data*(1-data_m))
  return rmse


def plot_losses(d_losses, g_losses, g_temp_losses, mse_losses):
  '''Plot the loss functions over iterations.'''
  plt.figure(figsize=(12, 6))
  # Plot Discriminator and Generator Losses
  plt.subplot(1, 2, 1)
  plt.plot(d_losses, label='Discriminator Loss', color='red')
  plt.plot(g_losses, label='Generator Loss', color='blue')
  plt.xlabel('Iterations')
  plt.ylabel('Loss')
  #plt.title('Discriminator and Generator Losses')
  plt.legend()
  # Plot MSE and ENT Losses
  plt.subplot(1, 2, 2)
  plt.plot(g_temp_losses, label=r'$\mathcal{L}_G$ Loss', color='purple')
  plt.plot(mse_losses, label=r'$\alpha \cdot \mathcal{L}_M$ Loss', color='green')
  plt.xlabel('Iterations')
  plt.ylabel('Loss')
  #plt.title('GTemp and MSE Losses')
  plt.legend()
  plt.tight_layout()
  plt.show()


def rounding (data_x, imputed_data):
  '''Round imputed data based on data_x decimals.'''
  rounded_data = imputed_data.copy()
  max_places = np.zeros(data_x.shape[1], dtype=int)
  for col in range(data_x.shape[1]):
      for row in data_x[:, col]:
          if not np.isfinite(row):
              continue
          val_str = str(row).split('.')
          if len(val_str) > 1:
              max_places[col] = max(max_places[col], len(val_str[1]))
      rounded_data[:, col] = np.round(rounded_data[:, col], decimals=max_places[col])
  return rounded_data


## EGAIN Function
##-------------------
def EGAIN (data_x, egain_parameters, retrain=False, plots=False):
  '''Imputes missing values in data_x.
  data_x: data with missing values
  egain_parameters: input dictionary of EGAIN parameters
  retrain: True/False, whether to retrain the generator or not
  plots: True/False, whether to plot the losses or not
  '''
  # System params
  batch_size = egain_parameters['batch_size']
  hint_rate = egain_parameters['hint_rate']
  alpha = egain_parameters['alpha']
  iterations = egain_parameters['iterations']

  # Other params
  no, dim = data_x.shape
  h_dim = int(dim)

  # Mask matrix
  data_m = 1 - np.isnan(data_x)

  # Normalization
  scaler = MinMaxScaler()
  norm_parameters = scaler.fit(data_x)
  norm_data = scaler.transform(data_x)
  norm_data_x = np.nan_to_num(norm_data, 0)

  ## Architecture
  ##--------------------
  # Define Generator Model
  def build_generator():
    x_input = Input(shape=(dim, 2))  # 3D Input
    h1 = Conv1D(filters=dim, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='glorot_normal')(x_input)
    h2 = MaxPooling1D(pool_size=dim, data_format="channels_first", padding='same')(h1)
    h3 = Flatten()(h2)
    h4 = Dense(h_dim, activation='relu', kernel_initializer='glorot_normal')(h3)
    h5 = Dense(h_dim, activation='relu', kernel_initializer='glorot_normal')(h4)
    output = Dense(dim, activation='sigmoid')(h5)
    return Model(x_input, output)

  # Define Discriminator Model
  def build_discriminator():
    x_input = Input(shape=(dim, 2))  # 3D Input
    h1 = Conv1D(filters=dim, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='glorot_normal')(x_input)
    h2 = MaxPooling1D(pool_size=dim, data_format="channels_first", padding='same')(h1)
    h3 = Flatten()(h2)
    h4 = Dense(h_dim, activation='relu', kernel_initializer='glorot_normal')(h3)
    h5 = Dense(h_dim, activation='relu', kernel_initializer='glorot_normal')(h4)
    output = Dense(dim, activation='sigmoid')(h5)
    return Model(x_input, output)

  generator = build_generator()
  discriminator = build_discriminator()

  ## Structure
  ##--------------------
  @tf.function
  def train_step(X_mb, M_mb, H_mb):
    # Convert to float tensors
    X_mb = tf.cast(X_mb, tf.float32)
    M_mb = tf.cast(M_mb, tf.float32)
    H_mb = tf.cast(H_mb, tf.float32)
    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        # Generator
        G_sample = generator(tf.stack([X_mb, M_mb], axis=-1))
        # Combine with observed data
        Hat_X = (M_mb * X_mb) + ((1 - M_mb) * G_sample)
        # Discriminator
        D_prob = discriminator(tf.stack([Hat_X, H_mb], axis=-1))
        ## GAIN loss
        D_loss = 10*-tf.reduce_mean(M_mb * tf.math.log(D_prob + 1e-8) + (1 - M_mb) * tf.math.log(1. - D_prob + 1e-8))
        G_loss_temp = -tf.reduce_mean((1 - M_mb) * tf.math.log(D_prob + 1e-8))
        MSE_loss = tf.reduce_mean(tf.square(M_mb * X_mb - M_mb * G_sample))
        G_loss = G_loss_temp + (alpha * MSE_loss)

    gradients_of_discriminator = disc_tape.gradient(D_loss, discriminator.trainable_variables)
    gradients_of_generator = gen_tape.gradient(G_loss, generator.trainable_variables)

    optimizer_D.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))
    optimizer_G.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))

    return D_loss, G_loss_temp, MSE_loss, G_loss

  optimizer_D = tf.keras.optimizers.Adam()
  optimizer_G = tf.keras.optimizers.Adam()

  ## Iterations
  ##--------------------
  # Initialize
  checkpoint_path = "best_generator.weights.h5"
  checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, save_best_only=True, save_weights_only=True, monitor='loss', mode='min')
  best_loss = float('inf')

  if retrain:
    generator.load_weights(checkpoint_path)

  if plots:
    d_losses, g_temp_losses, mse_losses, g_losses = [], [], [], []

  for it in tqdm(range(iterations)):
    # Sample batch
    batch_idx = np.random.permutation(no)[:batch_size]
    X_mb = norm_data_x[batch_idx, :]
    M_mb = data_m[batch_idx, :]
    # Sample random noise
    Z_mb = np.random.uniform(low=0, high=1., size=[batch_size, dim])
    # Combine random noise with observed vectors
    X_mb = (M_mb * X_mb) + ((1 - M_mb) * Z_mb)
    # Sample hint vectors
    B_mb = np.random.binomial(n=1, p=hint_rate, size=[batch_size, dim])
    H_mb = (B_mb * M_mb) + (0.5 * (1 - B_mb))
    # Calculate loss
    D_loss_curr, G_loss_temp_curr, MSE_loss_curr, G_loss_curr = train_step(X_mb, M_mb, H_mb)

    if plots:
      d_losses.append(D_loss_curr)
      g_temp_losses.append(G_loss_temp_curr)
      mse_losses.append(alpha*MSE_loss_curr)
      g_losses.append(G_loss_curr)

    if G_loss_curr < best_loss:
        best_loss = G_loss_curr
        generator.save_weights(checkpoint_path)

  generator.load_weights(checkpoint_path)

  # Plot the loss curves after training
  if plots:
    plot_losses(d_losses, g_losses, g_temp_losses, mse_losses)

  ## Final Imputation
  ##--------------------
  X_mb = norm_data_x
  M_mb = data_m
  Z_mb = np.random.uniform(low=0, high=1., size=[no, dim])
  X_mb = (M_mb * X_mb) + ((1 - M_mb) * Z_mb)

  ## Return imputed data
  imputed_data = generator(tf.stack([X_mb, M_mb], axis=-1)).numpy()
  imputed_data = (data_m * norm_data_x) + ((1 - data_m) * imputed_data)

  # Renormalization
  imputed_data = scaler.inverse_transform(imputed_data)
  imputed_data = rounding(data_x, imputed_data)

  return imputed_data