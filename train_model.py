import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# paths
train_path = "dataset/train"
valid_path = "dataset/valid"
test_path = "dataset/test"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# ======================
# DATA GENERATOR
# ======================

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    zoom_range=0.2,
    horizontal_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1
)

valid_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    train_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

valid_data = valid_datagen.flow_from_directory(
    valid_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

test_data = test_datagen.flow_from_directory(
    test_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# ======================
# PRETRAINED MODEL
# ======================

base_model = MobileNetV2(
    input_shape=(224,224,3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False

# ======================
# CUSTOM HEAD
# ======================

x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.5)(x)

output = layers.Dense(5, activation='softmax')(x)

model = models.Model(inputs=base_model.input, outputs=output)

# ======================
# COMPILE
# ======================

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ======================
# CALLBACKS
# ======================

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.3,
    patience=3
)

# ======================
# TRAIN
# ======================

history = model.fit(
    train_data,
    validation_data=valid_data,
    epochs=20,
    callbacks=[early_stop, reduce_lr]
)

# ======================
# UNFREEZE FOR FINE TUNING
# ======================

base_model.trainable = True

for layer in base_model.layers[:100]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history_fine = model.fit(
    train_data,
    validation_data=valid_data,
    epochs=10
)

# ======================
# SAVE MODEL
# ======================

model.save("model/plant_disease_model.h5")

print("Model saved!")

# ======================
# TEST
# ======================

test_loss, test_acc = model.evaluate(test_data)

print("Test Accuracy:", test_acc)