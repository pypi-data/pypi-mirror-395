# V-Nova VC-6 codec python module

## Usage

Main codec functionality is inside the `codec` module that can be imported as follow:

```python
from vnova.vc6_opencl import codec as vc6codec
```

or if you have installed the CUDA codec:

```python
from vnova.vc6_cu12 import codec as vc6codec
```

Then you can create codecs and start transcoding. For complete examples see provided sample codes

```python
# setup encoder and decoder instances
    encoder = vc6codec.EncoderSync(
        1920, 1080, vc6codec.CodecBackendType.CPU, vc6codec.PictureFormat.RGB_8, vc6codec.ImageMemoryType.CPU)
    encoder.set_generic_preset(vc6codec.EncoderGenericPreset.LOSSLESS)
    # Using double resolution to demonstrate reconfiguration later
    decoder = vc6codec.DecoderSync(1920, 1080, vc6codec.CodecBackendType.CPU, vc6codec.PictureFormat.RGB_8, vc6codec.ImageMemoryType.CPU)
    # encode file to memory
    encoded_image = encoder.read("example_1920x1080_rgb8.rgb")
    # decode memory to memory
    decoder.write(encoded_image.memoryview, "reconstruction_example_1920x1080_rgb8.rgb")
    encoded_image.release()
```

### GPU memory output
In case of cuda package (vc6_cu12), decoder output can be a device memory. To enable this feature create the decoder with specifying `GPU_DEVICE` as the output memory type. With that, the output images will have `__cuda_array_interface__` and can be used with other libraries like cupy, pytorch and nvimagecodec.


```python
    import cupy
    # setup GPU decoder instances with CUDA device output
    decoder = vc6codec.DecoderSync(1920, 1080, vc6codec.CodecBackendType.GPU, vc6codec.PictureFormat.RGB_8, vc6codec.ImageMemoryType.CUDA_DEVICE)
    # decode from file
    decoded_image = decoder.read("example_1920x1080_rgb8.vc6")
    # Make a cupy array from decoded image, download to cpu and write to file
    cuarray = cupy.asarray(decoded_image)
    with open("reconstruction_example_1920x1080_rgb8.rgb", "wb") as decoded_file:
        decoded_file.write(cuarray.get())
```

Both for sync and async decoders, accessing `__cuda_array_interface__` is blocking and implicitly waits on the result to be ready in the image.

The `__cuda_array_interface__` always contains a one-dimension data of unsigned-8bit type like the CPU version. Adjusting dimensions (or the type in case of 10-bit formats) is up to the user.

### Environment variables

Variables OCL_BIN_LOC and OCL_DEVICE can be set to be used as gpu binary cache location and hint to selecting target GPU respectively. For more details refer to VC6-SDK documentation.

```cmd
export OCL_BIN_LOC=./tmp/clbin
export OCL_DEVICE=nvidia
```
Variable CUDA_BIN_LOC serves the same purpose for CUDA version
